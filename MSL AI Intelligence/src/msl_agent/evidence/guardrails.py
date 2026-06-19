"""Methodological guardrails for hallucination-prone medical content."""

from __future__ import annotations

import re

from pydantic import BaseModel, Field

from .evidence_ledger import ClaimType, ClinicalClaim, Confidence


SUPERIORITY_TERMS = (
    "superior",
    "superiority",
    "better than",
    "more effective than",
    "piu efficace",
    "più efficace",
    "superiore",
)


class GuardrailIssue(BaseModel):
    """A compliance or evidence-methodology issue."""

    message: str
    severity: str = "error"


class GuardrailResult(BaseModel):
    """Structured result returned by guardrail checks."""

    permitted: bool
    needs_human_review: bool
    issues: list[GuardrailIssue] = Field(default_factory=list)


def validate_nct_identifier(
    nct_id: str,
    *,
    known_nct_ids: set[str] | None = None,
) -> GuardrailResult:
    """Validate an NCT identifier format and optional known-trial presence."""

    if not re.fullmatch(r"NCT\d{8}", nct_id):
        return GuardrailResult(
            permitted=False,
            needs_human_review=True,
            issues=[GuardrailIssue(message=f"invalid NCT identifier format: {nct_id}")],
        )

    if known_nct_ids is not None and nct_id not in known_nct_ids:
        return GuardrailResult(
            permitted=False,
            needs_human_review=True,
            issues=[GuardrailIssue(message=f"NCT identifier not found in retrieved trial set: {nct_id}")],
        )

    return GuardrailResult(permitted=True, needs_human_review=False)


def assess_superiority_claim(
    claim_text: str,
    *,
    has_head_to_head_source: bool,
) -> GuardrailResult:
    """Mark unsupported superiority claims as not permitted."""

    normalized = claim_text.casefold()
    contains_superiority_language = any(term in normalized for term in SUPERIORITY_TERMS)

    if contains_superiority_language and not has_head_to_head_source:
        return GuardrailResult(
            permitted=False,
            needs_human_review=True,
            issues=[
                GuardrailIssue(
                    message="comparative superiority claim requires head-to-head evidence or explicit indirect framing"
                )
            ],
        )

    return GuardrailResult(permitted=True, needs_human_review=False)


def assess_off_label_statement(
    claim_text: str,
    *,
    is_on_label: bool,
) -> GuardrailResult:
    """Flag off-label or jurisdiction-dependent content for human review."""

    if is_on_label:
        return GuardrailResult(permitted=True, needs_human_review=False)

    return GuardrailResult(
        permitted=True,
        needs_human_review=True,
        issues=[
            GuardrailIssue(
                message=f"off-label or jurisdiction-dependent statement requires human review: {claim_text}"
            )
        ],
    )


def missing_pubmed_source_claim(*, expected_pmid: str, claim_context: str) -> ClinicalClaim:
    """Return an explicit insufficient-evidence claim instead of inferring.

    This is used when a PubMed source expected by a workflow is unavailable.
    """

    return ClinicalClaim(
        claim_text=f"evidenza non identificata per {claim_context} ({expected_pmid})",
        source_ids=[],
        claim_type=ClaimType.FACT,
        confidence=Confidence.INSUFFICIENT,
        evidence_level="evidenza non identificata",
        needs_human_review=True,
    )


def validate_required_report_sections(markdown: str) -> GuardrailResult:
    """Check that a final report includes required evidence and limitation sections."""

    required = ("Evidence Ledger", "Limitations")
    missing = [section for section in required if section not in markdown]
    if missing:
        return GuardrailResult(
            permitted=False,
            needs_human_review=True,
            issues=[
                GuardrailIssue(message=f"final report missing required section: {section}")
                for section in missing
            ],
        )
    return GuardrailResult(permitted=True, needs_human_review=False)
