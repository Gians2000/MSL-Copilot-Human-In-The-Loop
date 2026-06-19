from unittest import TestCase

import tests._path  # noqa: F401

from msl_agent.evidence import (
    ClaimType,
    ClinicalClaim,
    Confidence,
    EvidenceLedger,
    EvidenceValidationError,
    assess_off_label_statement,
    assess_superiority_claim,
    missing_pubmed_source_claim,
    validate_claims_against_sources,
    validate_nct_identifier,
    validate_required_report_sections,
)


class HallucinationGuardrailTests(TestCase):
    def test_claim_without_source_is_blocked(self) -> None:
        ledger = EvidenceLedger(
            claims=[
                ClinicalClaim(
                    claim_text="A clinical claim without source.",
                    source_ids=[],
                    claim_type=ClaimType.FACT,
                    confidence=Confidence.INSUFFICIENT,
                    evidence_level="evidenza non identificata",
                    needs_human_review=True,
                )
            ]
        )

        with self.assertRaises(EvidenceValidationError):
            validate_claims_against_sources(ledger)

    def test_nonexistent_nct_is_flagged(self) -> None:
        result = validate_nct_identifier("NCT00000000", known_nct_ids={"NCT04035486"})

        self.assertFalse(result.permitted)
        self.assertTrue(result.needs_human_review)
        self.assertIn("not found", result.issues[0].message)

    def test_superiority_without_head_to_head_is_not_permitted(self) -> None:
        result = assess_superiority_claim(
            "Treatment A is superior to Treatment B in EGFR-mutated NSCLC.",
            has_head_to_head_source=False,
        )

        self.assertFalse(result.permitted)
        self.assertTrue(result.needs_human_review)

    def test_off_label_output_is_marked_for_human_review(self) -> None:
        result = assess_off_label_statement(
            "Discuss off-label use in a jurisdiction where the label is not verified.",
            is_on_label=False,
        )

        self.assertTrue(result.permitted)
        self.assertTrue(result.needs_human_review)

    def test_missing_pubmed_source_is_not_replaced_by_inference(self) -> None:
        claim = missing_pubmed_source_claim(
            expected_pmid="PMID:00000000",
            claim_context="unavailable PubMed abstract",
        )

        self.assertIn("evidenza non identificata", claim.claim_text)
        self.assertEqual(claim.source_ids, [])
        self.assertEqual(claim.confidence, Confidence.INSUFFICIENT)
        self.assertTrue(claim.needs_human_review)

    def test_final_report_contains_evidence_ledger_and_limitations(self) -> None:
        markdown = """# Brief

## Evidence Ledger

| Source | Claim |
|---|---|

## Limitations

- Internal draft.
"""

        result = validate_required_report_sections(markdown)

        self.assertTrue(result.permitted)
        self.assertFalse(result.needs_human_review)
