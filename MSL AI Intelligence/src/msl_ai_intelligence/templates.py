"""Markdown rendering helpers for opportunity briefs."""

from __future__ import annotations

from typing import Any, Mapping

from .scoring import ScoreReport, score_opportunity


def _bullet_list(values: Any) -> str:
    if not values:
        return "- Not specified"
    if isinstance(values, str):
        return f"- {values}"
    return "\n".join(f"- {value}" for value in values)


def _evidence_table(rows: list[Mapping[str, Any]]) -> str:
    if not rows:
        return "No evidence items provided."

    lines = [
        "| Claim | Source | Evidence level | Caveat |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {claim} | {source} | {level} | {caveat} |".format(
                claim=str(row.get("claim", "")),
                source=str(row.get("source", "")),
                level=str(row.get("evidence_level", "")),
                caveat=str(row.get("caveat", "")),
            )
        )
    return "\n".join(lines)


def _score_block(report: ScoreReport) -> str:
    missing = "None" if not report.missing_dimensions else ", ".join(report.missing_dimensions)
    lines = [
        f"- Weighted score: {report.weighted_score}/100",
        f"- Priority band: {report.priority_band}",
        f"- Missing scoring dimensions: {missing}",
    ]
    return "\n".join(lines)


def render_opportunity_brief(data: Mapping[str, Any]) -> str:
    """Render a trial opportunity input dictionary as a Markdown brief."""

    report = score_opportunity(data.get("scores", {}))
    concept = data.get("trial_concept", {})
    swot = data.get("swot_bridge", {})
    narratives = data.get("stakeholder_narratives", {})

    return f"""# {data.get("title", "Trial Opportunity Brief")}

## Strategic Hypothesis

{data.get("strategic_hypothesis", "Not specified")}

## Context

- Disease: {data.get("disease", "Not specified")}
- Setting: {data.get("setting", "Not specified")}
- Population: {data.get("population", "Not specified")}
- Geography: {data.get("geography", "Not specified")}

## Unmet Need

{data.get("unmet_need", "Not specified")}

## Evidence Spine

{_evidence_table(data.get("evidence", []))}

## Trial Concept

- Intervention: {concept.get("intervention", "Not specified")}
- Comparator: {concept.get("comparator", "Not specified")}
- Primary endpoint: {concept.get("primary_endpoint", "Not specified")}
- Secondary endpoints:
{_bullet_list(concept.get("secondary_endpoints"))}
- Biomarker strategy: {concept.get("biomarker_strategy", "Not specified")}
- RWE or pragmatic component: {concept.get("rwe_component", "Not specified")}

## SWOT Bridge

- Strength fit: {swot.get("strength_fit", "Not specified")}
- Weakness mitigation: {swot.get("weakness_mitigation", "Not specified")}
- Opportunity capture: {swot.get("opportunity_capture", "Not specified")}
- Threat response: {swot.get("threat_response", "Not specified")}

## Priority Score

{_score_block(report)}

## Stakeholder Narratives

- KOL: {narratives.get("kol", "Not specified")}
- HCP: {narratives.get("hcp", "Not specified")}
- Payer or HTA: {narratives.get("payer", "Not specified")}
- Patient or advocacy: {narratives.get("patient", "Not specified")}

## Elevator Pitch

{data.get("elevator_pitch", "Not specified")}
"""
