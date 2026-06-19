from unittest import TestCase

import tests._path  # noqa: F401

from msl_agent.agents import TrialOpportunityRequest, run_trial_opportunity_pipeline
from msl_agent.evidence import (
    ClaimType,
    ClinicalClaim,
    Confidence,
    EvidenceItem,
    SourceType,
)


class PipelineTests(TestCase):
    def test_pipeline_generates_structured_outputs_with_sources(self) -> None:
        request = TrialOpportunityRequest(
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
                    identifiers=["PMID:41104938"],
                    supported_claims=["FLAURA2 final OS analysis reported OS benefit."],
                    confidence=Confidence.HIGH,
                )
            ],
            clinical_trial_sources=[
                EvidenceItem(
                    source_id="NCT04035486",
                    source_type=SourceType.CLINICAL_TRIALS,
                    title="FLAURA2",
                    url="https://clinicaltrials.gov/study/NCT04035486",
                    identifiers=["NCT04035486"],
                    confidence=Confidence.HIGH,
                )
            ],
            candidate_claims=[
                ClinicalClaim(
                    claim_text="FLAURA2 final OS analysis reported an OS benefit for osimertinib plus chemotherapy.",
                    source_ids=["PMID:41104938"],
                    claim_type=ClaimType.FACT,
                    confidence=Confidence.HIGH,
                    evidence_level="peer-reviewed phase III publication",
                    needs_human_review=False,
                )
            ],
            unmet_need_topics=["first-line risk-adapted intensification"],
            swot_inputs={"opportunities": ["high-risk patient segmentation"]},
            narrative_inputs=["Hypothesis: high-risk EGFR-mutated NSCLC may need risk-adapted intensification."],
        )

        output = run_trial_opportunity_pipeline(request)

        self.assertTrue(output.input_validation.valid)
        self.assertTrue(output.compliance_review.passed)
        self.assertIn("Evidence Ledger", output.final_report.markdown)
        self.assertIn("Limitations and Assumptions", output.final_report.markdown)

    def test_pipeline_fails_safely_when_sources_are_missing(self) -> None:
        request = TrialOpportunityRequest(
            indication="NSCLC",
            scenario="unmet need identification for trial opportunity",
            audience="internal medical/scientific stakeholders",
        )

        output = run_trial_opportunity_pipeline(request)

        self.assertFalse(output.compliance_review.passed)
        self.assertTrue(output.compliance_review.requires_human_review)
        self.assertIn("evidenza non identificata", output.final_report.markdown)
        self.assertTrue(output.evidence_extraction.unsupported_items)
