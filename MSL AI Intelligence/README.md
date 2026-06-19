# MSL Agent

MSL Agent is a Python proof of concept for an evidence-first Medical Science Liaison intelligence assistant.
The initial therapeutic focus is oncology, with NSCLC used as the reference indication for examples and tests.

The repository is designed for internal medical/scientific use. It is not a diagnostic tool, is not a treatment
recommendation engine, and does not replace Medical, Legal, Regulatory, or Compliance review.

## What the PoC does

- Structures MSL trial opportunity briefs.
- Tracks clinical claims against verifiable sources.
- Separates observed evidence, interpretation, hypothesis, and MSL implication.
- Produces Markdown reports with an Evidence Ledger and limitations.
- Fails safely when evidence is missing instead of inventing unsupported content.
- Provides a minimal Chiesi-oriented demo using mock-but-verifiable data.

## Repository layout

```text
src/msl_agent/
  config/          Runtime settings and configuration helpers.
  data_sources/    Interfaces for literature, trial, regulatory, and future internal sources.
  evidence/        Evidence ledger models, validation, and anti-hallucination guardrails.
  agents/          Multi-step MSL brief generation pipeline.
  reports/         Markdown report templates and rendering helpers.

tests/             Unit and methodological robustness tests.
examples/          Demo inputs and generated outputs.
docs/              Methodology and compliance guardrails.
```

The earlier `src/msl_ai_intelligence` package is kept for compatibility with the original prototype. New PoC
work should target `src/msl_agent`.

## Installation

```bash
python -m pip install -e .
```

For a clean environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Run tests

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Run the demo

```bash
PYTHONPATH=src python -m msl_agent.cli demo \
  --output examples/nsclc_trial_opportunity_brief.md \
  --ledger-output examples/evidence_ledger_sample.json
```

The demo uses a small curated dataset with verifiable public references. It does not claim access to proprietary
Chiesi systems or databases.

## Generate a brief from JSON

```bash
PYTHONPATH=src python -m msl_agent.cli brief examples/nsclc_egfr_post_refine_request.json \
  --output outputs/post_refine_nsclc_trial_opportunity_brief.md
```

## Evidence and compliance model

Every clinical claim must be linked to a source such as a PMID, DOI, NCT number, ClinicalTrials.gov URL,
guideline, or regulatory document. Unsupported claims are either blocked or marked for human review depending
on the validation mode.

Required report sections:

- Evidence Ledger
- Limitations and Assumptions
- Human Review Checklist

## Human-in-the-loop status

This PoC is designed for internal draft generation only. A human reviewer must approve clinical, compliance,
and access-related claims before any external use.

## Development notes

- Use Python 3.11 or later.
- Keep modules small and typed.
- Add tests with every guardrail or report-generation change.
- Do not add speculative integrations. Use explicit TODO comments where a real external system is not yet wired.
