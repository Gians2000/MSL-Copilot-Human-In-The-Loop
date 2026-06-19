# AGENTS.md

This repository contains **MSL Agent**, an evidence-first Medical Science Liaison Intelligence Assistant for
oncology, initially focused on NSCLC.

The agent is a human-in-the-loop copilot for internal medical/scientific intelligence. It must not be treated as
an autonomous medical decision system, a promotional content generator, or a replacement for Medical, Legal,
Regulatory, Compliance, or Market Access review.

## Mandatory Clinical Rules

- Do not invent clinical data, trials, endpoints, hazard ratios, ORR, PFS, OS, safety signals, guideline
  statements, regulatory decisions, or reimbursement conclusions.
- Every clinical claim must be connected to a verifiable source: PMID, DOI, NCT number, ClinicalTrials.gov URL,
  guideline, peer-reviewed publication, or regulatory document.
- If a source is not available, write `evidenza non identificata` instead of inferring or filling the gap.
- Always separate:
  - observed data,
  - interpretation,
  - strategic hypothesis,
  - MSL implication.
- Do not provide individual treatment recommendations.
- Do not use promotional language.
- Do not make comparative superiority claims unless the source is a valid head-to-head comparison or the claim is
  explicitly marked as indirect, hypothesis-generating, and requiring human review.
- Do not present off-label use as a recommendation. Off-label or jurisdiction-dependent statements must be flagged
  for human review.
- Every output must include an `Evidence Ledger` section with source, date, supported claim, and confidence level.
- Every output must include `Limitations and Assumptions`.

## Coding Style

- Use Python 3.11+.
- Prefer typed, small modules with explicit return types.
- Use Pydantic models for structured pipeline outputs and validation-sensitive domain models.
- Keep functions deterministic where possible.
- Avoid speculative integrations. If a real connector is not implemented, add a concise TODO that names the missing
  approved integration.
- Keep comments short and useful; avoid restating obvious code.
- Preserve the legacy `src/msl_ai_intelligence` package unless a task explicitly asks to migrate it.
- New PoC capabilities belong under `src/msl_agent`.

## Required Tests

Run before handoff:

```bash
python -m unittest discover -s tests
```

Any change to evidence validation, report generation, or compliance logic must add or update tests. Required
guardrail coverage includes:

- unsupported clinical claim handling,
- missing source handling,
- invalid NCT handling,
- unsupported superiority comparisons,
- off-label flagging,
- required report sections.

## Error Handling

- Fail safely when evidence is missing.
- Degrade output with explicit limitations rather than inventing content.
- Validation functions should return structured issues or raise clear exceptions, depending on mode.
- User-facing errors should identify what is missing and what human review must resolve.

## Source Validation

- A clinical claim is valid only when all referenced `source_ids` exist in the Evidence Ledger.
- Source records should include source type, title, URL or identifier, publication or access date when available,
  supported claim text, and confidence.
- Use `evidenza non identificata` when an expected source is unavailable.
- Do not substitute PubMed, ClinicalTrials.gov, or regulatory facts with model memory.

## Report Generation

Final reports must include:

- Executive summary.
- Clinical context.
- Unmet needs.
- Current evidence landscape.
- Active/recent trials.
- SWOT matching.
- Trial opportunity hypothesis.
- MSL discussion prompts.
- Evidence Ledger.
- Limitations and Assumptions.
- Human Review Checklist.

Reports must label every clinical statement as one of:

- `fact`
- `interpretation`
- `hypothesis`
- `recommendation`

No clinical claim should appear without citation. If a report contains uncited clinical content, it is not ready
for handoff.

## Compliance Review Before Final Output

Before producing a final report or demo artifact:

1. Validate every claim against the Evidence Ledger.
2. Confirm that unsupported claims are blocked or explicitly marked `evidenza non identificata`.
3. Flag off-label, jurisdiction-dependent, or promotional-risk language for human review.
4. Confirm that comparative claims are either head-to-head supported or marked as indirect/hypothesis-generating.
5. Ensure the output includes `Evidence Ledger`, `Limitations and Assumptions`, and `Human Review Checklist`.
6. Mark the artifact as `internal draft - human review required`.

## Human-in-the-Loop Principle

The agent may draft, structure, check, and summarize. Humans approve. Any artifact intended for external use must
be reviewed by Medical and Compliance, and access/value claims must also be reviewed by Market Access/Economics.
