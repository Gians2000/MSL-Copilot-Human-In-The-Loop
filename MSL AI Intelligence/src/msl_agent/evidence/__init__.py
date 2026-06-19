"""Evidence models and validation utilities."""

from .evidence_ledger import (
    ClaimType,
    ClinicalClaim,
    Confidence,
    EvidenceItem,
    EvidenceLedger,
    EvidenceValidationError,
    EvidenceValidationResult,
    SourceType,
    ValidationIssue,
    validate_claims_against_sources,
)
from .guardrails import (
    GuardrailIssue,
    GuardrailResult,
    assess_off_label_statement,
    assess_superiority_claim,
    missing_pubmed_source_claim,
    validate_nct_identifier,
    validate_required_report_sections,
)

__all__ = [
    "ClaimType",
    "ClinicalClaim",
    "Confidence",
    "EvidenceItem",
    "EvidenceLedger",
    "EvidenceValidationError",
    "EvidenceValidationResult",
    "SourceType",
    "ValidationIssue",
    "GuardrailIssue",
    "GuardrailResult",
    "assess_off_label_statement",
    "assess_superiority_claim",
    "missing_pubmed_source_claim",
    "validate_claims_against_sources",
    "validate_nct_identifier",
    "validate_required_report_sections",
]
