#!/usr/bin/env python3
"""Render a trial opportunity JSON file into a Markdown brief.

This standalone helper intentionally uses only the Python standard library so
the skill remains usable even when the repository package is not installed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


WEIGHTS = {
    "clinical_unmet_need": 0.18,
    "evidence_gap": 0.13,
    "biological_rationale": 0.10,
    "differentiation": 0.13,
    "feasibility": 0.11,
    "competitive_urgency": 0.09,
    "access_relevance": 0.09,
    "narrative_power": 0.08,
    "patient_value": 0.09,
}


def _score(data: Mapping[str, Any]) -> tuple[float, list[str]]:
    scores = data.get("scores", {})
    missing: list[str] = []
    total = 0.0
    for name, weight in WEIGHTS.items():
        raw = scores.get(name)
        if raw is None:
            missing.append(name)
            continue
        value = max(1.0, min(5.0, float(raw)))
        total += value * weight
    return round((total / 5.0) * 100.0, 1), missing


def _items(values: Any) -> str:
    if not values:
        return "- Not specified"
    if isinstance(values, str):
        return f"- {values}"
    return "\n".join(f"- {item}" for item in values)


def _table(rows: list[Mapping[str, Any]]) -> str:
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


def render(data: Mapping[str, Any]) -> str:
    score, missing = _score(data)
    concept = data.get("trial_concept", {})
    swot = data.get("swot_bridge", {})
    narratives = data.get("stakeholder_narratives", {})
    missing_line = "None" if not missing else ", ".join(missing)

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

{_table(data.get("evidence", []))}

## Trial Concept

- Intervention: {concept.get("intervention", "Not specified")}
- Comparator: {concept.get("comparator", "Not specified")}
- Primary endpoint: {concept.get("primary_endpoint", "Not specified")}
- Secondary endpoints:
{_items(concept.get("secondary_endpoints"))}
- Biomarker strategy: {concept.get("biomarker_strategy", "Not specified")}
- RWE or pragmatic component: {concept.get("rwe_component", "Not specified")}

## SWOT Bridge

- Strength fit: {swot.get("strength_fit", "Not specified")}
- Weakness mitigation: {swot.get("weakness_mitigation", "Not specified")}
- Opportunity capture: {swot.get("opportunity_capture", "Not specified")}
- Threat response: {swot.get("threat_response", "Not specified")}

## Priority Score

- Weighted score: {score}/100
- Missing scoring dimensions: {missing_line}

## Stakeholder Narratives

- KOL: {narratives.get("kol", "Not specified")}
- HCP: {narratives.get("hcp", "Not specified")}
- Payer or HTA: {narratives.get("payer", "Not specified")}
- Patient or advocacy: {narratives.get("patient", "Not specified")}

## Elevator Pitch

{data.get("elevator_pitch", "Not specified")}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    rendered = render(data)
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
