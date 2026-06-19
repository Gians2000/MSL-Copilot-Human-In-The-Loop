"""End-to-end demo data for the MSL Agent PoC.

The demo uses public, verifiable source identifiers and mock strategic inputs.
It does not claim access to proprietary databases or company systems.
"""

from __future__ import annotations

import json
from pathlib import Path

from msl_agent.agents import TrialOpportunityRequest, run_trial_opportunity_pipeline
from msl_agent.evidence import (
    ClaimType,
    ClinicalClaim,
    Confidence,
    EvidenceItem,
    SourceType,
)


def build_nsclc_demo_request() -> TrialOpportunityRequest:
    """Build the minimal Chiesi-facing NSCLC demo request."""

    return TrialOpportunityRequest(
        indication="NSCLC",
        scenario="unmet need identification for trial opportunity",
        audience="internal medical/scientific stakeholders",
        data_cutoff="2026-06-19",
        literature_sources=[
            EvidenceItem(
                source_id="PMID:41104938",
                source_type=SourceType.PUBMED,
                title="Survival with osimertinib plus chemotherapy in EGFR-mutated advanced NSCLC",
                url="https://pubmed.ncbi.nlm.nih.gov/41104938/",
                date="2026",
                identifiers=["PMID:41104938", "DOI:10.1056/NEJMoa2510308"],
                supported_claims=[
                    "FLAURA2 final analysis reported an OS benefit for osimertinib plus chemotherapy."
                ],
                confidence=Confidence.HIGH,
            ),
            EvidenceItem(
                source_id="FDA:MARIPOSA-2024",
                source_type=SourceType.REGULATORY,
                title="FDA approval of lazertinib plus amivantamab-vmjw in EGFR-mutated NSCLC",
                url="https://www.fda.gov/drugs/resources-information-approved-drugs/fda-approves-lazertinib-amivantamab-vmjw-non-small-lung-cancer",
                date="2024-08-19",
                identifiers=["NCT04487080"],
                supported_claims=[
                    "FDA approved lazertinib plus amivantamab-vmjw for first-line EGFR exon19del/L858R NSCLC."
                ],
                confidence=Confidence.HIGH,
            ),
        ],
        clinical_trial_sources=[
            EvidenceItem(
                source_id="NCT05338970",
                source_type=SourceType.CLINICAL_TRIALS,
                title="HERTHENA-Lung02",
                url="https://clinicaltrials.gov/study/NCT05338970",
                date="status verified 2025-01",
                identifiers=["NCT05338970"],
                supported_claims=[
                    "HERTHENA-Lung02 evaluates patritumab deruxtecan versus platinum-based chemotherapy after third-generation EGFR TKI."
                ],
                confidence=Confidence.MODERATE,
            )
        ],
        candidate_claims=[
            ClinicalClaim(
                claim_text="FLAURA2 final analysis reported an OS benefit for osimertinib plus chemotherapy.",
                source_ids=["PMID:41104938"],
                claim_type=ClaimType.FACT,
                confidence=Confidence.HIGH,
                evidence_level="peer-reviewed phase III publication",
                needs_human_review=False,
            ),
            ClinicalClaim(
                claim_text="FDA approved lazertinib plus amivantamab-vmjw for first-line EGFR exon19del/L858R NSCLC.",
                source_ids=["FDA:MARIPOSA-2024"],
                claim_type=ClaimType.FACT,
                confidence=Confidence.HIGH,
                evidence_level="regulatory approval notice",
                needs_human_review=False,
            ),
            ClinicalClaim(
                claim_text="HERTHENA-Lung02 evaluates patritumab deruxtecan versus platinum-based chemotherapy after third-generation EGFR TKI.",
                source_ids=["NCT05338970"],
                claim_type=ClaimType.FACT,
                confidence=Confidence.MODERATE,
                evidence_level="ClinicalTrials.gov registry record",
                needs_human_review=True,
            ),
            ClinicalClaim(
                claim_text="A risk-adapted first-line intensification trial is a strategic hypothesis for high-risk EGFR-mutated NSCLC.",
                source_ids=["PMID:41104938", "FDA:MARIPOSA-2024"],
                claim_type=ClaimType.HYPOTHESIS,
                confidence=Confidence.LOW,
                evidence_level="strategic hypothesis grounded in multiple source-linked developments",
                needs_human_review=True,
            ),
        ],
        unmet_need_topics=[
            "first-line risk-adapted intensification",
            "post-osimertinib molecular assignment",
            "CNS-focused endpoint strategy",
        ],
        swot_inputs={
            "strengths": ["source-linked evidence ledger", "human-in-the-loop review model"],
            "weaknesses": ["mock demo data; no proprietary database integration"],
            "opportunities": ["trial opportunity prioritization", "KOL insight generation"],
            "threats": ["off-label interpretation risk", "local label and reimbursement variability"],
        },
        narrative_inputs=[
            "Hypothesis: a source-linked, risk-adapted NSCLC trial opportunity brief can focus KOL discussion on patient segments, endpoints, and evidence gaps instead of broad promotional claims."
        ],
    )


def run_nsclc_demo(*, output: Path, ledger_output: Path) -> None:
    """Generate demo Markdown and Evidence Ledger JSON files."""

    request = build_nsclc_demo_request()
    result = run_trial_opportunity_pipeline(request)
    provenance = """

## Demo Provenance

- Real/verifiable: public source identifiers, public URLs, PMID/NCT/FDA references.
- Mock: selected strategic topics, SWOT inputs, and narrative framing.
- Requires human validation: clinical interpretation, local label status, compliance review, access assumptions, and any external-use wording.
- Proprietary access: not used and not implied.
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    ledger_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result.final_report.markdown + provenance, encoding="utf-8")
    ledger_output.write_text(
        json.dumps(result.final_report.ledger.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
