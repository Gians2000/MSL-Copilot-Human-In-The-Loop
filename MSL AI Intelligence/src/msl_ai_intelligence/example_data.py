"""Reusable example payloads for CLI initialization."""

EXAMPLE_OPPORTUNITY = {
    "title": "Example NSCLC Trial Opportunity",
    "disease": "NSCLC",
    "setting": "Metastatic first line",
    "population": "Driver-negative, non-squamous, PD-L1 low or negative",
    "geography": "Specify geography",
    "strategic_hypothesis": "A biologically selected combination strategy may improve durable disease control in a subgroup with limited benefit from current chemo-immunotherapy approaches.",
    "unmet_need": "Patients with driver-negative, PD-L1 low or negative metastatic NSCLC remain at risk for early progression and limited durable benefit.",
    "evidence": [
        {
            "claim": "Add an evidence-backed claim here.",
            "source": "Publication, label, guideline, congress, RWE study, or HTA source",
            "evidence_level": "Primary trial, RWE, guideline, HTA, or hypothesis",
            "caveat": "State maturity, subgroup size, indirectness, or other limitation.",
        }
    ],
    "trial_concept": {
        "intervention": "Investigational product or combination concept",
        "comparator": "Current standard of care",
        "primary_endpoint": "PFS, OS, EFS, DFS, ORR, DOR, or other justified endpoint",
        "secondary_endpoints": ["OS", "ORR", "DOR", "safety", "quality of life"],
        "biomarker_strategy": "PD-L1, NGS, resistance marker, immune signature, or exploratory biomarker plan",
        "rwe_component": "Optional pragmatic cohort, registry linkage, testing-rate analysis, or TTD follow-up",
    },
    "swot_bridge": {
        "strength_fit": "How the concept uses a product strength.",
        "weakness_mitigation": "How the design addresses a product weakness.",
        "opportunity_capture": "Which unmet need or evidence gap is captured.",
        "threat_response": "Which competitor, access, guideline, or implementation threat is addressed.",
    },
    "scores": {
        "clinical_unmet_need": 4,
        "evidence_gap": 4,
        "biological_rationale": 3,
        "differentiation": 3,
        "feasibility": 3,
        "competitive_urgency": 4,
        "access_relevance": 3,
        "narrative_power": 4,
        "patient_value": 4,
    },
    "stakeholder_narratives": {
        "kol": "This concept tests a clinically relevant subgroup where durable disease control remains uncertain.",
        "hcp": "The design focuses on a common treatment decision point and aims to clarify patient selection.",
        "payer": "The concept could reduce uncertainty around comparative value in a defined reimbursable population.",
        "patient": "The study is designed around the need for longer disease control with tolerable treatment burden.",
    },
    "elevator_pitch": "Current evidence leaves a clinically important gap for driver-negative, PD-L1 low or negative metastatic NSCLC. The proposed concept uses biomarker-informed selection to test whether a differentiated combination can improve durable disease control. A randomized study against current standard of care would prioritize PFS with OS, safety, quality of life, and RWE follow-up as key secondary evidence. The opportunity matters now because clinical differentiation, patient value, and access relevance all depend on proving benefit in the population least served by broad chemo-immunotherapy.",
}
