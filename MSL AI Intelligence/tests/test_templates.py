from unittest import TestCase

import tests._path  # noqa: F401

from msl_ai_intelligence.example_data import EXAMPLE_OPPORTUNITY
from msl_ai_intelligence.templates import render_opportunity_brief


class TemplateTests(TestCase):
    def test_render_contains_core_sections(self) -> None:
        markdown = render_opportunity_brief(EXAMPLE_OPPORTUNITY)

        self.assertIn("# Example NSCLC Trial Opportunity", markdown)
        self.assertIn("## Evidence Spine", markdown)
        self.assertIn("## SWOT Bridge", markdown)
        self.assertIn("## Elevator Pitch", markdown)
