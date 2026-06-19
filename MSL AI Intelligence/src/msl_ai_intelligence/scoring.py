"""Scoring utilities for thoracic oncology trial opportunities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


DEFAULT_WEIGHTS: dict[str, float] = {
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


@dataclass(frozen=True)
class ScoreReport:
    weighted_score: float
    priority_band: str
    missing_dimensions: tuple[str, ...]
    dimension_scores: dict[str, float]


def _normalize(value: float) -> float:
    return max(1.0, min(5.0, float(value)))


def priority_band(weighted_score: float) -> str:
    """Return a priority label for a 0 to 100 weighted score."""

    if weighted_score >= 80:
        return "high-priority trial concept"
    if weighted_score >= 65:
        return "promising concept needing focused validation"
    if weighted_score >= 50:
        return "exploratory evidence-building concept"
    return "deprioritize unless strategically required"


def score_opportunity(
    scores: Mapping[str, float],
    weights: Mapping[str, float] | None = None,
) -> ScoreReport:
    """Score an opportunity using 1 to 5 dimension scores.

    Missing dimensions are ignored in the numerator and returned explicitly.
    The default denominator remains 5, so incomplete scorecards are visibly
    conservative rather than inflated.
    """

    active_weights = dict(weights or DEFAULT_WEIGHTS)
    total = 0.0
    missing: list[str] = []
    normalized: dict[str, float] = {}

    for dimension, weight in active_weights.items():
        if dimension not in scores:
            missing.append(dimension)
            continue
        value = _normalize(float(scores[dimension]))
        normalized[dimension] = value
        total += value * weight

    weighted_score = round((total / 5.0) * 100.0, 1)
    return ScoreReport(
        weighted_score=weighted_score,
        priority_band=priority_band(weighted_score),
        missing_dimensions=tuple(missing),
        dimension_scores=normalized,
    )
