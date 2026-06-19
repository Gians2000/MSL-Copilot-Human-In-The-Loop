import json
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import TestCase

import tests._path  # noqa: F401

from msl_agent.demo import build_nsclc_demo_request, run_nsclc_demo


class DemoTests(TestCase):
    def test_demo_request_matches_prompt_inputs(self) -> None:
        request = build_nsclc_demo_request()

        self.assertEqual(request.indication, "NSCLC")
        self.assertEqual(request.scenario, "unmet need identification for trial opportunity")
        self.assertEqual(request.audience, "internal medical/scientific stakeholders")

    def test_demo_writes_brief_and_ledger(self) -> None:
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            brief = base / "nsclc_trial_opportunity_brief.md"
            ledger = base / "evidence_ledger_sample.json"

            run_nsclc_demo(output=brief, ledger_output=ledger)

            self.assertIn("Demo Provenance", brief.read_text(encoding="utf-8"))
            payload = json.loads(ledger.read_text(encoding="utf-8"))
            self.assertIn("sources", payload)
            self.assertIn("claims", payload)
