# Data Sources

Use the source hierarchy below when implementing future connectors or evidence ingestion.

## Clinical Trials

- ClinicalTrials.gov and EU Clinical Trials Register for protocol and status.
- Primary publications and supplements for efficacy, subgroup, and safety data.
- Congress abstracts for recent updates that are not yet fully published.

## Guidelines

- NCCN, ESMO, ASCO, AIOM, and national guidelines relevant to the target geography.
- Capture version, date, recommendation class, level of evidence, and population.

## Regulatory And Access

- FDA labels and multidisciplinary reviews.
- EMA EPARs and product information.
- AIFA reimbursement and registry documents for Italy.
- HTA reports and managed entry agreement context when available.

## RWE

- Registry studies, EHR studies, claims analyses, pragmatic cohorts, and institutional datasets.
- Extract data period, country, sample size, selection logic, endpoint definitions, and missingness.

## Competitive Intelligence

- Approved mechanisms and phase 2 or phase 3 assets in the same segment.
- Record mechanism, population, endpoint, readout timing, sponsor, and strategic implication.

## Data Quality Rules

- Preserve source URLs and retrieval dates.
- Store evidence level and caveat with every claim.
- Avoid unsupported cross-trial superiority language.
- Mark hypotheses separately from established findings.
