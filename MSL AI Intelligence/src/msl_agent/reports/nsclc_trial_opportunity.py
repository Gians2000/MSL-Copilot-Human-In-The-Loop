"""Markdown template for NSCLC Trial Opportunity Brief reports."""

from __future__ import annotations

from typing import Any

from msl_agent.evidence import ClaimType, ClinicalClaim, EvidenceLedger


REQUIRED_REPORT_SECTIONS: tuple[str, ...] = (
    "Executive summary",
    "Clinical context",
    "Unmet needs",
    "Current evidence landscape",
    "Active/recent trials",
    "SWOT matching",
    "Trial opportunity hypothesis",
    "MSL discussion prompts",
    "Evidence Ledger",
    "Limitations and Assumptions",
    "Human Review Checklist",
)


def _source_rows(ledger: EvidenceLedger) -> str:
    if not ledger.sources:
        return "| evidenza non identificata | - | No source supplied | - | - |"
    return "\n".join(
        "| {source_id} | {source_type} | {title} | {url} | {date} |".format(
            source_id=source.source_id,
            source_type=source.source_type.value,
            title=source.title,
            url=source.url,
            date=source.date or "not specified",
        )
        for source in ledger.sources
    )


def _claim_rows(claims: list[ClinicalClaim]) -> str:
    if not claims:
        return "| fact | evidenza non identificata | evidenza non identificata | insufficient | yes |"
    return "\n".join(
        "| {claim_type} | {claim} | {sources} | {confidence} | {review} |".format(
            claim_type=claim.claim_type.value,
            claim=claim.claim_text,
            sources=", ".join(claim.source_ids) if claim.source_ids else "evidenza non identificata",
            confidence=claim.confidence.value,
            review="yes" if claim.needs_human_review else "no",
        )
        for claim in claims
    )


def _claims_by_type(ledger: EvidenceLedger, claim_type: ClaimType) -> list[str]:
    return [
        f"- [{', '.join(claim.source_ids)}] {claim.claim_text}"
        for claim in ledger.claims
        if claim.claim_type == claim_type and claim.source_ids
    ]


def _bullet(values: list[str], fallback: str = "evidenza non identificata") -> str:
    if not values:
        return f"- {fallback}"
    return "\n".join(f"- {value}" for value in values)


def render_nsclc_trial_opportunity_brief(
    *,
    request: Any,
    ledger: EvidenceLedger,
    unmet_needs: list[Any],
    swot: Any,
    narratives: list[Any],
    limitations: list[str],
    compliance: Any,
) -> str:
    """Render an NSCLC Trial Opportunity Brief in the required Markdown format."""

    observed = _claims_by_type(ledger, ClaimType.FACT)
    interpretations = _claims_by_type(ledger, ClaimType.INTERPRETATION)
    hypotheses = _claims_by_type(ledger, ClaimType.HYPOTHESIS)
    recommendations = _claims_by_type(ledger, ClaimType.RECOMMENDATION)
    unmet_lines = [
        f"{getattr(need, 'topic', 'evidenza non identificata')} ({getattr(need, 'status', 'needs_human_review')})"
        for need in unmet_needs
    ]
    narrative_lines = [
        getattr(narrative, "narrative", "evidenza non identificata") for narrative in narratives
    ]
    review_status = "required" if getattr(compliance, "requires_human_review", True) else "not required by automated checks"

    return f"""# NSCLC Trial Opportunity Brief

Status: internal draft - human review required

## Executive summary

- Indication: {request.indication}
- Scenario: {request.scenario}
- Audience: {request.audience}
- Automated compliance status: {review_status}

## Clinical context

- Data cutoff: {request.data_cutoff or "not specified"}
- This report separates observed evidence, interpretation, hypothesis, and recommendation.
- It does not provide individual treatment recommendations.

## Unmet needs

{_bullet(unmet_lines)}

## Current evidence landscape

### Observed evidence

{_bullet(observed)}

### Interpretation

{_bullet(interpretations)}

### Hypotheses

{_bullet(hypotheses)}

### Recommendations

{_bullet(recommendations)}

### Source table

| Source ID | Type | Title | URL | Date |
|---|---|---|---|---|
{_source_rows(ledger)}

## Active/recent trials

{_bullet([f"{source.title} ({', '.join(source.identifiers) or source.source_id})" for source in ledger.sources if source.source_type.value == "clinical_trials"])}

## SWOT matching

- Strengths: {', '.join(getattr(swot, 'strengths', [])) or 'evidenza non identificata'}
- Weaknesses: {', '.join(getattr(swot, 'weaknesses', [])) or 'evidenza non identificata'}
- Opportunities: {', '.join(getattr(swot, 'opportunities', [])) or 'evidenza non identificata'}
- Threats: {', '.join(getattr(swot, 'threats', [])) or 'evidenza non identificata'}

## Trial opportunity hypothesis

{_bullet(narrative_lines)}

## MSL discussion prompts

- Which source-linked unmet need is most clinically material?
- Which claims require Medical or Compliance review before external discussion?
- Which endpoint would make this opportunity payer-relevant?
- Which evidence gaps should be resolved before KOL engagement?

## Evidence Ledger

| Claim type | Claim | Sources | Confidence | Human review |
|---|---|---|---|---|
{_claim_rows(ledger.claims)}

## Limitations and Assumptions

{_bullet(limitations or ledger.limitations, fallback="No limitations recorded.")}

## Human Review Checklist

- Medical review: required
- Compliance review: required
- Market Access/Economics review: required for payer/value claims
- Off-label or jurisdiction-dependent statements: human review required
- Final status: internal draft only
"""
