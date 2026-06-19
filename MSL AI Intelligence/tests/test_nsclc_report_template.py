from unittest import TestCase

import tests._path  # noqa: F401

from msl_agent.agents import TrialOpportunityRequest, run_trial_opportunity_pipeline
from msl_agent.reports import REQUIRED_REPORT_SECTIONS


class NSCLCReportTemplateTests(TestCase):
    def test_pipeline_report_contains_required_sections(self) -> None:
        output = run_trial_opportunity_pipeline(
            TrialOpportunityRequest(
                indication="NSCLC",
                scenario="unmet need identification for trial opportunity",
                audience="internal medical/scientific stakeholders",
            )
        )

        for section in REQUIRED_REPORT_SECTIONS:
            self.assertIn(section, output.final_report.markdown)

    def test_unsupported_clinical_content_is_rendered_as_evidence_gap(self) -> None:
        output = run_trial_opportunity_pipeline(
            TrialOpportunityRequest(
                indication="NSCLC",
                scenario="unmet need identification for trial opportunity",
                audience="internal medical/scientific stakeholders",
            )
        )

        self.assertIn("evidenza non identificata", output.final_report.markdown)
        self.assertIn("Human Review Checklist", output.final_report.markdown)
