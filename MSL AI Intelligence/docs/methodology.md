# Methodology

MSL Agent follows an evidence-first workflow for internal medical/scientific intelligence.

## Workflow

1. Validate the user input and intended audience.
2. Retrieve or load verifiable public-source evidence.
3. Extract clinical claims and source metadata.
4. Classify each claim as fact, interpretation, hypothesis, or recommendation.
5. Map unmet needs and evidence gaps.
6. Draft trial opportunity hypotheses and MSL discussion prompts.
7. Run compliance guardrails.
8. Generate a Markdown report with an Evidence Ledger and limitations.
9. Require human review before use outside the draft context.

## Evidence handling

Clinical claims must link to sources such as PMID, DOI, NCT number, ClinicalTrials.gov URL, guideline, or
regulatory document. If no source is available, the system must state `evidenza non identificata` instead of
filling the gap by inference.

## Confidence

Confidence is assigned at claim level:

- `high`: directly supported by a high-quality source.
- `moderate`: supported but with limitations, such as indirect evidence or immature endpoint.
- `low`: exploratory, early, or context-dependent.
- `insufficient`: evidence missing or not adequate for the claim.

## Current limitations

- The PoC uses curated or mock-verifiable data unless a real connector is implemented.
- It does not access proprietary systems.
- It does not perform medical decision-making.
- It requires human review for clinical and compliance-sensitive outputs.
