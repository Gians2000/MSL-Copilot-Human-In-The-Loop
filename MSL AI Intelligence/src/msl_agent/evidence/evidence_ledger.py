"""Evidence Ledger models and claim-source validation.

The ledger is the anti-hallucination core of the PoC: clinical claims are only
valid when they point to source records that exist in the same ledger.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, HttpUrl, field_validator


class SourceType(str, Enum):
    """Supported source categories for traceable medical evidence."""

    PUBMED = "pubmed"
    DOI = "doi"
    CLINICAL_TRIALS = "clinical_trials"
    REGULATORY = "regulatory"
    GUIDELINE = "guideline"
    CONFERENCE = "conference"
    RWE = "rwe"
    MOCK_VERIFIABLE = "mock_verifiable"
    OTHER = "other"


class ClaimType(str, Enum):
    """Clinical claim classification used in reports."""

    FACT = "fact"
    INTERPRETATION = "interpretation"
    HYPOTHESIS = "hypothesis"
    RECOMMENDATION = "recommendation"


class Confidence(str, Enum):
    """Claim-level confidence."""

    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    INSUFFICIENT = "insufficient"


class EvidenceItem(BaseModel):
    """A verifiable evidence source used to support one or more claims."""

    source_id: str = Field(min_length=1)
    source_type: SourceType
    title: str = Field(min_length=1)
    url: HttpUrl | str
    date: str | None = None
    identifiers: list[str] = Field(default_factory=list)
    supported_claims: list[str] = Field(default_factory=list)
    confidence: Confidence = Confidence.MODERATE

    @field_validator("source_id")
    @classmethod
    def source_id_must_not_be_blank(cls, value: str) -> str:
        """Reject blank source identifiers."""

        stripped = value.strip()
        if not stripped:
            raise ValueError("source_id cannot be blank")
        return stripped


class ClinicalClaim(BaseModel):
    """A clinical statement that must be validated against evidence sources."""

    claim_text: str = Field(min_length=1)
    source_ids: list[str] = Field(default_factory=list)
    claim_type: ClaimType
    confidence: Confidence
    evidence_level: str = Field(min_length=1)
    needs_human_review: bool

    @field_validator("source_ids")
    @classmethod
    def source_ids_must_not_contain_blanks(cls, value: list[str]) -> list[str]:
        """Reject blank source identifiers while preserving caller order."""

        cleaned = [source_id.strip() for source_id in value]
        if any(not source_id for source_id in cleaned):
            raise ValueError("source_ids cannot contain blank values")
        return cleaned


class EvidenceLedger(BaseModel):
    """A complete set of sources and clinical claims for one output artifact."""

    sources: list[EvidenceItem] = Field(default_factory=list)
    claims: list[ClinicalClaim] = Field(default_factory=list)
    data_cutoff: str | None = None
    limitations: list[str] = Field(default_factory=list)

    def source_ids(self) -> set[str]:
        """Return all source identifiers available in the ledger."""

        return {source.source_id for source in self.sources}


class ValidationIssue(BaseModel):
    """A structured validation issue produced by ledger checks."""

    claim_text: str
    issue: str
    severity: str = "error"


class EvidenceValidationResult(BaseModel):
    """Result of validating claims against sources."""

    valid: bool
    issues: list[ValidationIssue] = Field(default_factory=list)


class EvidenceValidationError(ValueError):
    """Raised when strict evidence validation fails."""


def validate_claims_against_sources(
    ledger: EvidenceLedger,
    *,
    strict: bool = True,
) -> EvidenceValidationResult:
    """Validate that each clinical claim references existing sources.

    Args:
        ledger: Evidence ledger containing source records and clinical claims.
        strict: When true, raise EvidenceValidationError if validation fails.

    Returns:
        Structured validation result. In strict mode this is only returned when
        no blocking issues are present.
    """

    available_sources = ledger.source_ids()
    issues: list[ValidationIssue] = []

    for claim in ledger.claims:
        if not claim.source_ids:
            issues.append(
                ValidationIssue(
                    claim_text=claim.claim_text,
                    issue="clinical claim has no source_ids",
                )
            )
            continue

        missing = [source_id for source_id in claim.source_ids if source_id not in available_sources]
        if missing:
            issues.append(
                ValidationIssue(
                    claim_text=claim.claim_text,
                    issue=f"clinical claim references missing source_ids: {', '.join(missing)}",
                )
            )

    result = EvidenceValidationResult(valid=not issues, issues=issues)
    if strict and issues:
        details = "; ".join(issue.issue for issue in issues)
        raise EvidenceValidationError(f"Evidence validation failed: {details}")
    return result
