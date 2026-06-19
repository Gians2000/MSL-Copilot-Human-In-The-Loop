# Pre-refine vs Post-refine Comparison

Data: 19 giugno 2026  
Use case: NSCLC EGFR-mutato, unmet needs, terapie innovative, trial promettenti, R&D/Economics/KOL strategy.

## Files compared

### Pre-refine outputs

- `outputs/NSCLC_EGFR_RnD_Report_2026-06-19.md`
- `outputs/NSCLC_EGFR_Economics_Report_2026-06-19.md`
- `outputs/NSCLC_EGFR_KOL_Trial_Narratives_2026-06-19.md`

### Post-refine outputs

- `outputs/post_refine_NSCLC_EGFR_Trial_Opportunity_Brief_2026-06-19.md`
- `outputs/post_refine_NSCLC_EGFR_Evidence_Ledger_2026-06-19.json`

## High-level comparison

| Dimension | Pre-refine | Post-refine |
|---|---|---|
| Output breadth | Broad: R&D, Economics, KOL engagement, trial narratives in three long reports | Narrower: one structured NSCLC Trial Opportunity Brief plus JSON ledger |
| Strategic richness | High; strong for executive storytelling and advisory-board thinking | Moderate; intentionally constrained by evidence ledger and required sections |
| Evidence traceability | Sources listed, but not every claim is machine-linked to source IDs | Claim-level source IDs, confidence, evidence level, and human-review flag |
| Hallucination control | Mostly prompt/instruction based | Enforced by Pydantic models, validation tests, and ledger checks |
| Human-in-the-loop | Described conceptually | Embedded in report status, claim flags, limitations, and checklist |
| Compliance posture | Good draft, but review burden remains manual | Stronger PoC posture: unsupported claims degrade to `evidenza non identificata` |
| GitHub/product readiness | Report artifact only | Package, tests, CLI, docs, demo, ledger JSON, CI-ready structure |

## What improved after refine

- Every clinical claim in the post-refine brief is classified as `fact`, `hypothesis`, or `recommendation`.
- Every claim has source IDs or would be degraded by the pipeline.
- The Evidence Ledger is exported as machine-readable JSON.
- Unsupported or strategic content is marked for human review.
- The report includes mandatory `Evidence Ledger`, `Limitations and Assumptions`, and `Human Review Checklist`.
- The pipeline retains structured outputs for each step: input validation, retrieval, extraction, unmet need mapping, SWOT, narrative, compliance, final report.

## What became less strong after refine

- The post-refine brief is less expansive and less polished as an executive narrative.
- Department-specific depth for R&D and Economics is lower than in the pre-refine reports.
- The current PoC uses provided/curated public sources; it does not yet perform live PubMed, ClinicalTrials.gov, regulatory, or internal Chiesi retrieval.
- KOL strategy is represented as prompts and hypotheses rather than a full engagement plan.

## Practical interpretation

The pre-refine output is better as a high-context strategic draft.  
The post-refine output is better as a defendable PoC artifact.

For a Chiesi executive demo, the strongest story is to show both:

1. The pre-refine reports demonstrate the value potential and richness of MSL intelligence generation.
2. The post-refine pipeline demonstrates governance: evidence ledger, auditability, guardrails, human review, and reproducibility.

## Recommended demo sequence

1. Show the pre-refine R&D/Economics/KOL outputs as the "value vision".
2. Show the post-refine brief as the controlled PoC version.
3. Open the JSON Evidence Ledger to prove claim traceability.
4. Run the unit tests to show guardrails are executable, not just policy text.
5. Position the next phase as connector integration and reviewer workflow, not more prompting.
