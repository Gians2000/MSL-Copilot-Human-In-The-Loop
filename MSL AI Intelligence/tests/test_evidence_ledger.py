from unittest import TestCase

import tests._path  # noqa: F401

from msl_agent.evidence import (
    ClaimType,
    ClinicalClaim,
    Confidence,
    EvidenceItem,
    EvidenceLedger,
    EvidenceValidationError,
    SourceType,
    validate_claims_against_sources,
)


class EvidenceLedgerTests(TestCase):
    def test_valid_claim_with_existing_source_passes(self) -> None:
        ledger = EvidenceLedger(
            sources=[
                EvidenceItem(
                    source_id="PMID:41104938",
                    source_type=SourceType.PUBMED,
                    title="Survival with osimertinib plus chemotherapy in EGFR-mutated advanced NSCLC",
                    url="https://pubmed.ncbi.nlm.nih.gov/41104938/",
                    identifiers=["PMID:41104938"],
                    supported_claims=["OS benefit was reported in FLAURA2 final analysis."],
                    confidence=Confidence.HIGH,
                )
            ],
            claims=[
                ClinicalClaim(
                    claim_text="FLAURA2 final analysis reported an OS benefit for osimertinib plus chemotherapy.",
                    source_ids=["PMID:41104938"],
                    claim_type=ClaimType.FACT,
                    confidence=Confidence.HIGH,
                    evidence_level="peer-reviewed phase III publication",
                    needs_human_review=False,
                )
            ],
        )

        result = validate_claims_against_sources(ledger)

        self.assertTrue(result.valid)
        self.assertEqual(result.issues, [])

    def test_claim_without_source_is_blocked_in_strict_mode(self) -> None:
        ledger = EvidenceLedger(
            claims=[
                ClinicalClaim(
                    claim_text="Unsupported clinical claim.",
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

    def test_missing_source_is_reported_in_non_strict_mode(self) -> None:
        ledger = EvidenceLedger(
            claims=[
                ClinicalClaim(
                    claim_text="Claim references a missing source.",
                    source_ids=["NCT00000000"],
                    claim_type=ClaimType.INTERPRETATION,
                    confidence=Confidence.LOW,
                    evidence_level="evidenza non identificata",
                    needs_human_review=True,
                )
            ]
        )

        result = validate_claims_against_sources(ledger, strict=False)

        self.assertFalse(result.valid)
        self.assertIn("missing source_ids", result.issues[0].issue)
