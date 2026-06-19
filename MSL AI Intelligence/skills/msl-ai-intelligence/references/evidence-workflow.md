# Evidence Workflow

Use this reference when collecting or extracting evidence for a lung cancer intelligence task.

## Source Hierarchy

1. Primary peer-reviewed trial publications and supplements.
2. Regulatory labels and assessment reports from FDA, EMA, AIFA, or other relevant agencies.
3. Major congress abstracts or presentations when they are the newest available evidence.
4. Guideline documents from NCCN, ESMO, ASCO, AIOM, or national bodies.
5. HTA and reimbursement documents, including AIFA where Italy is in scope.
6. RWE studies, registry analyses, claims data, EHR studies, and pragmatic studies.
7. High-quality systematic reviews, ITCs, and network meta-analyses.

## Trial Extraction Fields

Capture:

- Trial name, phase, registration ID, publication year, geography, sponsor.
- Disease, histology, line, prior treatment, biomarker eligibility, key inclusion and exclusion criteria.
- Intervention, comparator, dosing, treatment duration.
- Primary endpoint and key secondary endpoints.
- OS, PFS, ORR, DOR, HR, confidence intervals, p-values where appropriate.
- Subgroups: PD-L1, TMB, EGFR, ALK, ROS1, KRAS G12C, histology, smoking, age, sex, geography, CNS disease.
- Safety: any-grade AE, grade 3 or higher AE, SAE, irAE, discontinuation, death, selected toxicity of interest.
- Data maturity, follow-up, crossover, subsequent therapy, multiplicity, and limitations.

## RWE Extraction Fields

Capture:

- Data source, country, period, sample size, inclusion logic.
- Real-world OS, PFS, TTD, time to next treatment, treatment duration.
- Utilization by line and sequence.
- Biomarker testing rates, NGS completion, turnaround time, tissue failure.
- Adherence, dose intensity, discontinuation reason, safety if available.
- Representativeness and missingness.

## Competitive Extraction Fields

Capture:

- Current standard of care by line and biomarker segment.
- Direct competitors and mechanisms: anti-PD-1, anti-PD-L1, CTLA-4, chemo-IO, anti-VEGF, ADC, bispecific, TKI, KRAS inhibitor, MET, RET, HER2, EGFR, ALK.
- Phase 2 or phase 3 competitors in the same population.
- Differentiating evidence: survival, durability, safety, convenience, route, biomarker, sequencing.
- Guideline placement and level of evidence.

## Access Extraction Fields

Capture:

- Geography and date.
- Label population and reimbursed population.
- HTA value drivers and criticisms.
- Managed entry agreements, registries, restrictions, or monitoring requirements.
- Testing prerequisites and implementation barriers.
- Regional uptake or center-level variation if available.

## Interpretation Rules

- Do not mix medians and hazard ratios as if they answer the same question.
- Treat immature OS cautiously when crossover or subsequent therapy can dilute effects.
- Treat PFS gains without OS or quality-of-life support as strategically meaningful but access-sensitive.
- Mark all cross-trial comparisons as indirect.
- Flag subgroups with small n, wide confidence intervals, post hoc status, or interaction tests not reported.
- Separate clinical evidence from commercial inference.
