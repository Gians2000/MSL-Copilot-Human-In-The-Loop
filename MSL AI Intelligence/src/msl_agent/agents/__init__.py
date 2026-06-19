"""Agentic workflow components for MSL brief generation."""

from .pipeline import (
    ClinicalTrialRetrievalOutput,
    ComplianceReviewOutput,
    EvidenceExtractionOutput,
    FinalReportOutput,
    InputValidationOutput,
    LiteratureRetrievalOutput,
    NarrativeStrategy,
    NarrativeStrategyOutput,
    SWOTMatchingOutput,
    TrialOpportunityPipelineOutput,
    TrialOpportunityRequest,
    UnmetNeed,
    UnmetNeedMappingOutput,
    run_trial_opportunity_pipeline,
)

__all__ = [
    "ClinicalTrialRetrievalOutput",
    "ComplianceReviewOutput",
    "EvidenceExtractionOutput",
    "FinalReportOutput",
    "InputValidationOutput",
    "LiteratureRetrievalOutput",
    "NarrativeStrategy",
    "NarrativeStrategyOutput",
    "SWOTMatchingOutput",
    "TrialOpportunityPipelineOutput",
    "TrialOpportunityRequest",
    "UnmetNeed",
    "UnmetNeedMappingOutput",
    "run_trial_opportunity_pipeline",
]
