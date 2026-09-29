"""
Pre-scored candidate data based on the Kargo Hiring Rubric v1.
Scores are computed from the 8 past-hire CVs provided as demo candidates.

PM Rubric (weights):
  1. Hands-On Operations Background  30%
  2. Unassigned Fixes That Others Adopted  20%
  3. Owns Failure and Pressure Openly  20%
  4. Core PM Craft (JD fit)  30%

SPM Rubric (weights):
  1. Hands-On Operations Background  25%
  2. Unassigned Fixes That Others Adopted  20%
  3. Owns Failure and Pressure Openly  20%
  4. Integration and Platform Depth  20%
  5. Senior Ownership Without a Layer Above  15%

Weighted total = sum(score/5 * weight)
"""

CANDIDATES = [
    {
        "id": "lavanya_iyer",
        "name": "Lavanya Iyer",
        "email": "lavanya.iyer.pm@gmail.com",
        "applied_role": "PM",
        "location": "Bengaluru (willing to relocate)",
        "summary": (
            "PM with 2 years in product roles, preceded by 3 years in supply chain "
            "planning and carrier operations at Mahindra Logistics (3PL). "
            "Sole PM at Portwise Technologies — shipped 6 features, killed 2 on usage data, "
            "wrote outage post-mortem, co-authored first API docs. Built carrier visibility "
            "dashboard adopted by 2 regional teams before moving into product."
        ),
        "current_role": "Product Manager, Portwise Technologies (Series A, Port & Logistics SaaS)",
        "years_experience": 5,  # 3 ops + 2 PM
        "pm_scores": {
            "ops_background":    {"score": 5, "weight": 30, "evidence": "3 years carrier operations & supply chain planning at Mahindra Logistics (3PL), managing 800+ shipments/month across South India"},
            "unassigned_fixes":  {"score": 5, "weight": 20, "evidence": "Visibility dashboard adopted by 2 other regional teams; same-day triage process created from scratch; carrier performance review process — none of these were assigned"},
            "owns_failure":      {"score": 5, "weight": 20, "evidence": "Killed 2 features on usage data despite strong qualitative demand; authored internal and customer-facing outage post-mortem and owned action items to closure"},
            "core_pm_craft":     {"score": 5, "weight": 30, "evidence": "6 features shipped, 2 killed; 3x weekly active use improvement in 30 days; discovery session that reduced support tickets 60%; co-wrote first formal API docs; engineering lead: 'she doesn't hedge'"},
        },
        "spm_scores": {
            "ops_background":       {"score": 5, "weight": 25, "evidence": "Same as PM. 3PL carrier operations — hands-on freight ops, not just vendor-side"},
            "unassigned_fixes":     {"score": 5, "weight": 20, "evidence": "Same as PM"},
            "owns_failure":         {"score": 5, "weight": 20, "evidence": "Same as PM"},
            "integration_platform": {"score": 4, "weight": 20, "evidence": "Sole PM for dock scheduling, carrier integration, and freight visibility; co-wrote first API docs; reduced integration timelines by 2 weeks. Clear ownership but limited explicit build-vs-configure decisions documented"},
            "senior_ownership":     {"score": 5, "weight": 15, "evidence": "Sole PM at Series A, reporting to product leadership with no senior PM layer above"},
        },
        "thin_evidence": [],
        "flags": ["Bengaluru-based — relocation to Mumbai not stated explicitly"],
        "probe_questions": [
            "Walk me through the carrier slot booking feature pivot — what exactly did you observe in discovery that triggered it, and how long from observation to decision?",
            "You killed two features on usage data. What was the qualitative demand signal that had looked compelling, and what did the usage data actually show?",
            "Tell me about the post-mortem you wrote. Who disagreed with your root cause, and how did you handle that?",
            "You built the visibility dashboard in Excel first then Tableau. Why didn't you build it properly the first time?",
        ],
    },
    {
        "id": "rohan_desai",
        "name": "Rohan Desai",
        "email": "rohan.desai.dev@gmail.com",
        "applied_role": "SPM",
        "location": "Mumbai",
        "summary": (
            "7 years across logistics operations (CHA at JNPT) and backend engineering "
            "at Clearfly Tech, building freight tracking platforms for 40+ forwarder clients. "
            "Built a B/L verification module over a weekend — 30 users in a month. "
            "Led vendor migration under pressure; introduced on-call rotation that cut P1 incidents 40%. "
            "Most senior engineer in the room — owns integration decisions end to end."
        ),
        "current_role": "Senior Software Engineer, Clearfly Tech Solutions (Freight Tech SaaS)",
        "years_experience": 7,
        "pm_scores": {
            "ops_background":    {"score": 5, "weight": 30, "evidence": "Operations Executive at Desai CHA & Logistics, JNPT — 3 years managing 180+ shipments/month, Bills of Lading, customs clearance, carrier coordination"},
            "unassigned_fixes":  {"score": 5, "weight": 20, "evidence": "Excel tracker built and adopted by 12-person ops team in 2 weeks (unassigned); B/L verification prototype over a weekend, 30 users in a month, now core product feature"},
            "owns_failure":      {"score": 5, "weight": 20, "evidence": "Vendor migration under time pressure with reliability risk — identified, executed, zero data loss, 60% processing lag reduction. Crisis + action + outcome."},
            "core_pm_craft":     {"score": 3, "weight": 30, "evidence": "Ships features with measurable outcomes (35% support reduction, 40% P1 reduction); works directly with ops users; no formal PM title or discovery practice documented"},
        },
        "spm_scores": {
            "ops_background":       {"score": 5, "weight": 25, "evidence": "3 years CHA operations, JNPT — freight documentation, carrier coordination, customs clearance"},
            "unassigned_fixes":     {"score": 5, "weight": 20, "evidence": "Same as PM, plus introduced structured code review and on-call rotation across the engineering team"},
            "owns_failure":         {"score": 5, "weight": 20, "evidence": "Same as PM"},
            "integration_platform": {"score": 5, "weight": 20, "evidence": "Lead engineer on core freight tracking platform; led vendor migration (build-vs-configure decision with data loss risk); owns carrier integration architecture"},
            "senior_ownership":     {"score": 5, "weight": 15, "evidence": "'Most senior engineer in the room' — sets architectural direction, mentors juniors, no product layer above him at clients"},
        },
        "thin_evidence": [],
        "flags": [],
        "probe_questions": [
            "You've been engineering, not PM. What tells you you'll succeed at the craft shift — discovery, prioritisation, saying no to engineering?",
            "Walk me through the B/L verification module — what made you build it that weekend instead of raising it as a ticket?",
            "The vendor migration: what was the moment you decided you had to do it, and what was the political cost inside the company?",
            "You translate field requirements into engineering spec 'without a product layer' — what does that process actually look like day to day?",
        ],
    },
    {
        "id": "meghna_tiwari",
        "name": "Meghna Tiwari",
        "email": "meghna.tiwari.cs@gmail.com",
        "applied_role": "PM",
        "location": "Mumbai",
        "summary": (
            "5 years across freight forwarding documentation (Coastline Freight Forwarders) "
            "and B2B SaaS customer success (Fieldstack Technologies). "
            "6% churn on her accounts vs 24% team average. Built the 30-60-90 onboarding "
            "framework now used by the full CS team. Resolved an overnight customs hold "
            "before the client noticed — classic crisis + fix + no escalation."
        ),
        "current_role": "Senior Customer Success Associate, Fieldstack Technologies (B2B SaaS, Field Ops)",
        "years_experience": 5,
        "pm_scores": {
            "ops_background":    {"score": 5, "weight": 30, "evidence": "Customer Relations & Documentation Executive at Coastline Freight Forwarders — managed 15-20 active shipments daily, export documentation, LC sets, pharma cold-chain coordination"},
            "unassigned_fixes":  {"score": 5, "weight": 20, "evidence": "Customer onboarding checklist became team standard, reducing onboarding queries 35%; 30-60-90 onboarding framework now used by full CS team — both self-initiated"},
            "owns_failure":      {"score": 5, "weight": 20, "evidence": "Overnight customs hold from documentation error — coordinated directly with CHA and customs officer through the night, shipment departed on schedule, client never notified. Specific crisis + direct action."},
            "core_pm_craft":     {"score": 2, "weight": 30, "evidence": "Identified undocumented product limitation, wrote internal bug report, managed customer communication through 6-week resolution. CS background — no shipped features, no formal discovery process documented"},
        },
        "spm_scores": None,
        "thin_evidence": [],
        "flags": [],
        "probe_questions": [
            "Your last PM-adjacent work was identifying a product limitation and coordinating the fix. Walk me through that — what did you actually do, and what would you have done differently if you'd been the PM?",
            "The 30-60-90 framework you built — what problem was it solving that the old process wasn't, and how did you know it was working?",
            "6% churn vs 24% team average is a striking gap. What are you doing differently from your colleagues?",
            "You've never shipped a product feature. What's your plan for the gap?",
        ],
    },
    {
        "id": "sunita_krishnamurthy",
        "name": "Sunita Krishnamurthy",
        "email": "urmila.sunita.k@gmail.com",
        "applied_role": "PM",
        "location": "Chennai / Mumbai",
        "summary": (
            "7 years in freight forwarding documentation and operations, now independent consultant. "
            "Managed 200+ shipments/month at Trident Freight Services, rebuilt intake workflow "
            "in a weekend when a vendor changed formats — process retained permanently. "
            "Certified IATA DGR. No PM experience, but deep domain fluency and "
            "a track record of unassigned improvements."
        ),
        "current_role": "Operations Consultant (Independent), Mumbai",
        "years_experience": 7,
        "pm_scores": {
            "ops_background":    {"score": 5, "weight": 30, "evidence": "4 years Documentation & Compliance Executive at Trident Freight — 200+ shipments/month, all modes, customs coordination, DGFT liaison"},
            "unassigned_fixes":  {"score": 5, "weight": 20, "evidence": "When vendor changed data export format without notice, independently redesigned the documentation intake workflow over a weekend — retained permanently. Unassigned, cross-team impact."},
            "owns_failure":      {"score": 5, "weight": 20, "evidence": "Vendor format change — proactive crisis response. DGFT compliance audit: identified 4 documentation gaps before inspection, all resolved. Also 2 customs inspections closed without penalties."},
            "core_pm_craft":     {"score": 1, "weight": 30, "evidence": "No PM experience. Consulting work includes workflow redesign and SOP development — closest to PM craft. THIN EVIDENCE on shipped features, discovery practice, engineering collaboration."},
        },
        "spm_scores": None,
        "thin_evidence": ["Core PM Craft — no evidence of shipped features, user discovery, or engineering collaboration"],
        "flags": ["Chennai-based; Mumbai listed as current city but confirm relocation intent"],
        "probe_questions": [
            "You've been deep in operations. What makes you think product management is the right next step rather than, say, head of ops at a logistics SaaS?",
            "You rebuilt the intake workflow when the vendor changed formats. If you'd been the PM responsible for the software the team was using, what would you have done before that vendor change happened?",
            "Walk me through the DGFT audit prep. How did you find the four gaps and what was your process?",
            "What do you think you'll find hardest about working in product — and what's your plan for it?",
        ],
    },
    {
        "id": "aditya_shetty",
        "name": "Aditya Shetty",
        "email": "aditya.shetty.sales@gmail.com",
        "applied_role": "PM",
        "location": "Mumbai",
        "summary": (
            "Enterprise SaaS sales at Stacksync (supply chain visibility), "
            "preceded by 2 years at JNPT port services — worked alongside terminal operations "
            "during peak periods. Ran a post-mortem on a 4-month lost deal and turned it into "
            "standard team practice. Consistently above 110% quota. "
            "No PM experience — strong ops grounding and commercial instinct."
        ),
        "current_role": "Senior Enterprise Sales Executive, Stacksync Technologies (Supply Chain Visibility SaaS)",
        "years_experience": 7,
        "pm_scores": {
            "ops_background":    {"score": 4, "weight": 30, "evidence": "Sales Executive at Jacaranda Port Services, JNPT — managed 25 freight forwarder/NVOCC clients, worked alongside terminal operations team during peak periods (berth windows, DO releases, documentation corrections)"},
            "unassigned_fixes":  {"score": 4, "weight": 20, "evidence": "Post-mortem on 4-month lost deal — documented root cause, shared with team, now standard pre-qualification practice. Not assigned; self-initiated and adopted by others."},
            "owns_failure":      {"score": 5, "weight": 20, "evidence": "4-month lost deal: specific failure (wrong economic buyer, misread of IT procurement cycle) + action (post-mortem) + lasting change (now standard team practice)"},
            "core_pm_craft":     {"score": 1, "weight": 30, "evidence": "No PM experience. Runs full enterprise sales cycles independently — closest to PM in discovery and structuring. THIN EVIDENCE on product delivery, engineering collaboration, feature prioritisation."},
        },
        "spm_scores": None,
        "thin_evidence": ["Core PM Craft — no evidence of product delivery or PM-specific work"],
        "flags": [],
        "probe_questions": [
            "You've been the person selling logistics software. Why do you want to be the person building it?",
            "In your JNPT years, you saw freight forwarder operations from the port side. What did you see that you think Kargo's current product is probably getting wrong?",
            "The Stacksync case study programme — what problem was it solving, and how did you know it worked?",
            "Walk me through the lost deal post-mortem. What did you find, and what was the hardest part of sharing it with the team?",
        ],
    },
    {
        "id": "vikram_nair",
        "name": "Vikram Nair",
        "email": "vikramnair.pm@gmail.com",
        "applied_role": "PM",
        "location": "Bengaluru (not stated Mumbai)",
        "summary": (
            "3 years PM experience at Springboard HR Technologies (Series B B2B SaaS). "
            "Shipped 12 features in 18 months, $180K incremental ARR, 34% adoption lift "
            "from UX redesign. Strong core PM craft. No logistics or operations exposure — "
            "came via MBA (XLRI) from HR tech. CV shows only wins. Reforge member, Product School certified."
        ),
        "current_role": "Product Manager, Springboard HR Technologies (Series B, HR Tech SaaS)",
        "years_experience": 3,
        "pm_scores": {
            "ops_background":    {"score": 1, "weight": 30, "evidence": "No operations exposure. Pure HR tech SaaS via MBA — no logistics, freight, or operations-heavy background."},
            "unassigned_fixes":  {"score": 3, "weight": 20, "evidence": "PRD template and sprint review process adopted by 4-person PM team — shows initiative, but within his assigned PM function. Score 3, not 5."},
            "owns_failure":      {"score": 1, "weight": 20, "evidence": "CV contains only wins. No failure, kill, setback or crisis mentioned. Vikram pattern: all positive outcomes."},
            "core_pm_craft":     {"score": 5, "weight": 30, "evidence": "12 features shipped in 18 months; $180K incremental ARR; 34% adoption increase via 40+ user interviews; 3-week reduction in time-to-first-value; clear outcomes on every bullet"},
        },
        "spm_scores": None,
        "thin_evidence": [],
        "flags": ["Bengaluru-based — relocation to Mumbai not mentioned", "No logistics or operations domain knowledge"],
        "probe_questions": [
            "Your CV is all wins. Tell me about something you shipped that didn't work — what happened and what did you do?",
            "You've spent your career in HR tech. What's your honest case for why that transfers to logistics operations software?",
            "You mention 40+ user interviews. What's the most uncomfortable thing you heard in discovery that you acted on?",
            "Kargo has no PM handbook, no design system, no sprint template. That's the opposite of what you've been building. What breaks first?",
        ],
    },
    {
        "id": "preetham_rao",
        "name": "Preetham Rao",
        "email": "preethamrao.dev@gmail.com",
        "applied_role": "PM",
        "location": "Bengaluru",
        "summary": (
            "Backend engineer at Cartexa (e-commerce, 3,200 employees) — "
            "strong technical execution: PostgreSQL indexing redesign, event-driven pipeline migration, "
            "3PL integrations via REST and SFTP. No ops exposure — classic 'Preetham pattern': "
            "built to ops teams from the vendor side. No PM experience, CV shows only wins."
        ),
        "current_role": "Software Engineer II (Backend), Cartexa India (E-commerce SaaS)",
        "years_experience": 5,
        "pm_scores": {
            "ops_background":    {"score": 2, "weight": 30, "evidence": "Integrated with 3PLs (Delhivery, Bluedart, Ecom Express) via REST and SFTP from inside Cartexa. Vendor-side integration, no hands-on ops role. Classic Preetham pattern — score 2."},
            "unassigned_fixes":  {"score": 3, "weight": 20, "evidence": "Internal monitoring dashboard surfaced a systemic coupon bug (₹12L/month loss) — but this was within his engineering role, not a cross-functional or ops-level unassigned fix. Score 3."},
            "owns_failure":      {"score": 1, "weight": 20, "evidence": "CV lists only wins — no failure, kill, setback or crisis mentioned anywhere."},
            "core_pm_craft":     {"score": 1, "weight": 30, "evidence": "No PM experience. Strong technical execution but no evidence of discovery, prioritisation, user-facing product decisions, or PM-level ownership."},
        },
        "spm_scores": None,
        "thin_evidence": ["Core PM Craft — no evidence of product management work"],
        "flags": ["Bengaluru-based — no mention of Mumbai relocation", "No PM or ops experience"],
        "probe_questions": [
            "You've been an excellent backend engineer. What makes you want to move into product?",
            "The coupon bug — how did you find it, and why hadn't someone already flagged it?",
            "Your 3PL integrations were technical. What did you learn about how the operations teams at Delhivery or Bluedart actually worked?",
            "What do you think the biggest gap in your preparation for a PM role is?",
        ],
    },
    {
        "id": "rahul_bose",
        "name": "Rahul Bose",
        "email": "rahul.bose.mktg@gmail.com",
        "applied_role": "PM",
        "location": "Mumbai",
        "summary": (
            "Marketing Manager at Ventus Fintech — owns full demand generation, "
            "₹2.4Cr pipeline sourced in FY24, built a 4-person team from scratch. "
            "No logistics or operations exposure. No PM experience. "
            "CV shows only wins. High marketing craft, wrong domain entirely for this rubric."
        ),
        "current_role": "Marketing Manager, Ventus Fintech (Series B, B2B SaaS)",
        "years_experience": 6,
        "pm_scores": {
            "ops_background":    {"score": 1, "weight": 30, "evidence": "No logistics or operations exposure. Pure B2B SaaS marketing across HR tech and fintech."},
            "unassigned_fixes":  {"score": 3, "weight": 20, "evidence": "Case study programme at Ventus — self-initiated, adopted by sales team as primary collateral. Within his assigned marketing function — score 3, not 5."},
            "owns_failure":      {"score": 1, "weight": 20, "evidence": "CV contains only wins. No failure, kill or crisis mentioned. Rahul pattern: all positive outcomes."},
            "core_pm_craft":     {"score": 1, "weight": 30, "evidence": "No PM experience. Strong marketing craft (demand gen, CAC reduction, team building) but no product delivery, discovery or engineering collaboration."},
        },
        "spm_scores": None,
        "thin_evidence": [],
        "flags": ["No logistics/operations background", "No PM experience — significant career pivot"],
        "probe_questions": [
            "This is a significant pivot. Walk me through your reasoning — why product, why logistics, why now?",
            "The case study programme — you say sales uses it as primary collateral. What would a PM have done differently in building that?",
            "What's the most complex product decision you've been close to — not made, but close to?",
            "Have you spent time inside a freight forwarder's office? What did you see?",
        ],
    },
]


def compute_score(scores_dict):
    """Compute weighted total from a scores dict."""
    if scores_dict is None:
        return None
    total = 0
    for criterion, data in scores_dict.items():
        total += (data["score"] / 5) * data["weight"]
    return round(total, 1)


def get_ranked_candidates():
    """Return candidates ranked by their applied-role score."""
    result = []
    for c in CANDIDATES:
        pm_total = compute_score(c["pm_scores"])
        spm_total = compute_score(c["spm_scores"])
        applied_score = spm_total if c["applied_role"] == "SPM" else pm_total
        result.append({**c, "pm_total": pm_total, "spm_total": spm_total, "applied_score": applied_score})
    return sorted(result, key=lambda x: (x["applied_score"] or 0), reverse=True)
