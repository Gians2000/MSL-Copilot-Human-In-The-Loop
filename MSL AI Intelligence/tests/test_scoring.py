from unittest import TestCase

import tests._path  # noqa: F401

from msl_ai_intelligence.scoring import priority_band, score_opportunity


class ScoringTests(TestCase):
    def test_high_priority_score(self) -> None:
        report = score_opportunity(
            {
                "clinical_unmet_need": 5,
                "evidence_gap": 5,
                "biological_rationale": 5,
                "differentiation": 5,
                "feasibility": 5,
                "competitive_urgency": 5,
                "access_relevance": 5,
                "narrative_power": 5,
                "patient_value": 5,
            }
        )

        self.assertEqual(report.weighted_score, 100.0)
        self.assertEqual(report.priority_band, "high-priority trial concept")
        self.assertEqual(report.missing_dimensions, ())

    def test_missing_dimensions_are_reported(self) -> None:
        report = score_opportunity({"clinical_unmet_need": 5})

        self.assertLess(report.weighted_score, 20)
        self.assertIn("evidence_gap", report.missing_dimensions)

    def test_priority_band_boundaries(self) -> None:
        self.assertEqual(priority_band(80), "high-priority trial concept")
        self.assertEqual(priority_band(65), "promising concept needing focused validation")
        self.assertEqual(priority_band(50), "exploratory evidence-building concept")
        self.assertEqual(priority_band(49.9), "deprioritize unless strategically required")
