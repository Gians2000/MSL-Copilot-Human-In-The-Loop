# Compliance Guardrails

MSL Agent is an internal medical/scientific copilot. It must not be used as an autonomous medical decision
system or promotional content generator.

## Required guardrails

- Do not invent clinical data, trials, endpoints, hazard ratios, response rates, survival metrics, safety signals,
  or guideline statements.
- Link every clinical claim to a verifiable source.
- Separate observed evidence, interpretation, hypothesis, and MSL implication.
- Avoid individual treatment recommendations.
- Avoid promotional language.
- Avoid unsupported comparative superiority claims.
- Flag off-label or jurisdiction-dependent statements for human review.
- Include Evidence Ledger, Limitations and Assumptions, and Human Review Checklist in final reports.

## Human review gates

Before external use, draft outputs require:

- Medical review for clinical accuracy and balance.
- Compliance review for non-promotional language and off-label risk.
- Market Access/Economics review for payer or value claims.

## TODO

- Define company-specific MLR workflow owners and approval states.
- Add jurisdiction-specific label and reimbursement validation once approved source systems are available.
