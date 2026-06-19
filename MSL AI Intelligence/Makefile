PYTHON ?= python
PYTHONPATH ?= src

.PHONY: install test validate render demo post-refine install-skill

install:
	$(PYTHON) -m pip install -e .

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests

validate:
	$(PYTHON) scripts/validate_skill.py skills/msl-ai-intelligence

render:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m msl_ai_intelligence.cli render examples/nsclc_trial_opportunity.json

demo:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m msl_agent.cli demo --output examples/nsclc_trial_opportunity_brief.md --ledger-output examples/evidence_ledger_sample.json

post-refine:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m msl_agent.cli brief examples/nsclc_egfr_post_refine_request.json --output outputs/post_refine_NSCLC_EGFR_Trial_Opportunity_Brief_2026-06-19.md --ledger-output outputs/post_refine_NSCLC_EGFR_Evidence_Ledger_2026-06-19.json

install-skill:
	$(PYTHON) scripts/install_skill.py
