import os
import re

import google.generativeai as genai
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from data import CANDIDATES, compute_score, get_ranked_candidates

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "arjun@kargo.in")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

app = Flask(__name__)
_model = None
_supa = None


def get_supabase():
    global _supa
    if _supa is None and SUPABASE_URL and SUPABASE_KEY:
        from supabase import create_client
        _supa = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supa


def get_model():
    global _model
    if _model is None and GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel("gemini-flash-lite-latest")
    return _model


def build_candidate_context(candidate):
    pm_breakdown = "\n".join(
        f"  {k}: {v['score']}/5 — {v['evidence']}"
        for k, v in candidate["pm_scores"].items()
    )
    spm_breakdown = ""
    if candidate.get("spm_scores"):
        spm_breakdown = "\n".join(
            f"  {k}: {v['score']}/5 — {v['evidence']}"
            for k, v in candidate["spm_scores"].items()
        )
    flags = ", ".join(candidate.get("flags", [])) or "None"
    thin = ", ".join(candidate.get("thin_evidence", [])) or "None"
    return f"""
Candidate: {candidate['name']}
Applied role: {candidate['applied_role']}
Current role: {candidate['current_role']}
Total experience: {candidate['years_experience']} years
Location: {candidate['location']}
PM Score: {compute_score(candidate['pm_scores'])}/100
{f"SPM Score: {compute_score(candidate['spm_scores'])}/100" if candidate.get('spm_scores') else ""}
Summary: {candidate['summary']}

PM Rubric breakdown:
{pm_breakdown}
{f"SPM Rubric breakdown:{chr(10)}{spm_breakdown}" if spm_breakdown else ""}

Thin evidence flags: {thin}
Eligibility flags: {flags}

Suggested interview probes (from rubric analysis):
{chr(10).join(f"- {q}" for q in candidate['probe_questions'])}
""".strip()


def call_gemini(system_prompt, user_prompt):
    model = get_model()
    if not model:
        return None, "GEMINI_API_KEY not configured."
    try:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = model.generate_content(
            full_prompt,
            generation_config={"max_output_tokens": 1024},
            request_options={"timeout": 60},
        )
        return response.text, None
    except Exception as e:
        msg = str(e)
        if "429" in msg or "quota" in msg.lower():
            return None, "Free tier rate limit hit — wait 60 seconds and try again."
        return None, msg


@app.route("/")
def dashboard():
    candidates = get_ranked_candidates()
    supa = get_supabase()
    statuses = {}
    if supa:
        try:
            rows = supa.table("candidate_status").select("candidate_id,status").execute()
            statuses = {r["candidate_id"]: r["status"] for r in rows.data}
        except Exception:
            pass
    return render_template("dashboard.html", candidates=candidates, statuses=statuses)


@app.route("/api/brief/<candidate_id>")
def get_brief(candidate_id):
    candidate = next((c for c in CANDIDATES if c["id"] == candidate_id), None)
    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    supa = get_supabase()
    if supa:
        try:
            cached = supa.table("briefs").select("content").eq("candidate_id", candidate_id).execute()
            if cached.data:
                return jsonify({"brief": cached.data[0]["content"], "cached": True})
        except Exception:
            pass

    context = build_candidate_context(candidate)
    system = (
        "You are a hiring assistant for Kargo, a Series A logistics SaaS company in Mumbai. "
        "Arjun Mehta (founder) is the hiring manager. He has 45 minutes and needs to make a call. "
        "Write tightly. No padding. No headers that add no information."
    )
    prompt = f"""Based on this candidate's rubric analysis, write a concise interview brief for Arjun.

{context}

Format the brief as follows (use these exact headers):

WHO THEY ARE
2-3 sentences. Their arc: where they started, where they are, what's unusual about the path.

WHY THEY SCORED HERE
3-4 bullets. The specific signal from the CV that drove the score — quote evidence, not abstractions.

WHAT TO PROBE
3-4 questions Arjun should ask. Make each one specific to this candidate's profile — not generic PM interview questions. Each question should probe something the CV hints at but doesn't fully answer.

THE CALL
One sentence: what Arjun should be trying to confirm or rule out in this conversation."""

    text, error = call_gemini(system, prompt)
    if error:
        return jsonify({"error": error}), 502

    if supa:
        try:
            supa.table("briefs").upsert({"candidate_id": candidate_id, "content": text}).execute()
        except Exception:
            pass

    return jsonify({"brief": text})


@app.route("/api/brief/<candidate_id>", methods=["DELETE"])
def clear_brief(candidate_id):
    supa = get_supabase()
    if supa:
        try:
            supa.table("briefs").delete().eq("candidate_id", candidate_id).execute()
        except Exception:
            pass
    return jsonify({"success": True})


@app.route("/api/email/<candidate_id>/<email_type>")
def get_email(candidate_id, email_type):
    if email_type not in ("invite", "reject"):
        return jsonify({"error": "Invalid email type"}), 400

    candidate = next((c for c in CANDIDATES if c["id"] == candidate_id), None)
    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    context = build_candidate_context(candidate)
    system = (
        "You are drafting emails for Arjun Mehta, founder of Kargo. "
        "Arjun is direct, genuine, and time-pressed. "
        "Emails should sound like a founder wrote them — not a recruiter. "
        "No corporate boilerplate. Short sentences. Specific where possible."
    )

    if email_type == "invite":
        prompt = f"""Draft an interview invitation email from Arjun to this candidate.

{context}

Requirements:
- From Arjun Mehta, Founder, Kargo
- Subject line should be specific to the candidate, not generic
- 4-6 sentences in the body — no more
- Reference one specific thing from their background that made Arjun want to speak with them
- Propose a 30-minute call this week; ask them to suggest times
- Warm but brief — founder tone, not HR tone
- End with: Arjun Mehta | Kargo

Return ONLY the email with subject and body. Format:
Subject: [subject line]

[body]"""
    else:
        prompt = f"""Draft a rejection email from Arjun to this candidate.

{context}

Requirements:
- From Arjun Mehta, Founder, Kargo
- 3-4 sentences — short and genuine
- Acknowledge something specific from their background (not generic "impressive profile")
- Be honest that it's not a fit right now without lengthy explanation
- Leave the door open if appropriate (only if their score is above 50)
- No corporate phrases like "we will keep your CV on file" or "we wish you all the best in your future endeavours"
- End with: Arjun Mehta | Kargo

Return ONLY the email with subject and body. Format:
Subject: [subject line]

[body]"""

    text, error = call_gemini(system, prompt)
    if error:
        return jsonify({"error": error}), 502

    lines = text.strip().split("\n")
    subject = ""
    body_lines = []
    in_body = False
    for line in lines:
        if line.lower().startswith("subject:"):
            subject = line[8:].strip()
        elif subject and not in_body and line.strip() == "":
            in_body = True
        elif in_body:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    if not subject:
        subject = f"Kargo — {'Interview invitation' if email_type == 'invite' else 'Your application'}"

    return jsonify({"subject": subject, "body": body, "to": candidate["email"]})


@app.route("/api/send-email", methods=["POST"])
def send_email():
    if not RESEND_API_KEY:
        return jsonify({"error": "RESEND_API_KEY not configured"}), 503

    data = request.get_json()
    to_email = data.get("to")
    subject = data.get("subject")
    body = data.get("body")
    candidate_id = data.get("candidate_id", "")
    email_type = data.get("email_type", "")

    if not all([to_email, subject, body]):
        return jsonify({"error": "Missing required fields"}), 400

    html_body = "<br>".join(line if line.strip() else "<br>" for line in body.split("\n"))

    resp = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
        json={"from": FROM_EMAIL, "to": [to_email], "subject": subject, "html": f"<p>{html_body}</p>"},
        timeout=15,
    )

    if resp.status_code in (200, 201):
        supa = get_supabase()
        if supa and candidate_id:
            try:
                supa.table("email_log").insert({
                    "candidate_id": candidate_id,
                    "email_type": email_type,
                    "to_email": to_email,
                    "subject": subject,
                    "body": body,
                    "status": "sent",
                }).execute()
            except Exception:
                pass
        return jsonify({"success": True, "message": f"Email sent to {to_email}"})
    else:
        return jsonify({"error": f"Resend API error: {resp.text}"}), 502


@app.route("/api/status/<candidate_id>", methods=["POST"])
def set_status(candidate_id):
    status = request.get_json().get("status")
    if status not in ("invited", "rejected", "in_progress", "none"):
        return jsonify({"error": "Invalid status"}), 400

    supa = get_supabase()
    if not supa:
        return jsonify({"error": "Supabase not configured"}), 503

    try:
        if status == "none":
            supa.table("candidate_status").delete().eq("candidate_id", candidate_id).execute()
        else:
            supa.table("candidate_status").upsert({"candidate_id": candidate_id, "status": status}).execute()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/candidates")
def list_candidates():
    return jsonify(get_ranked_candidates())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port, debug=True)
