"""Structured multi-step pipeline for MSL trial opportunity briefs."""

from __future__ import annotations

from pydantic import BaseModel, Field

from msl_agent.evidence import (
    ClaimType,
    ClinicalClaim,
    Confidence,
    EvidenceItem,
    EvidenceLedger,
    GuardrailIssue,
    validate_claims_against_sources,
    validate_nct_identifier,
)


class TrialOpportunityRequest(BaseModel):
    """Input for generating an MSL trial opportunity brief."""

    indication: str
    scenario: str
    audience: str
    data_cutoff: str | None = None
    literature_sources: list[EvidenceItem] = Field(default_factory=list)
    clinical_trial_sources: list[EvidenceItem] = Field(default_factory=list)
    candidate_claims: list[ClinicalClaim] = Field(default_factory=list)
    unmet_need_topics: list[str] = Field(default_factory=list)
    swot_inputs: dict[str, list[str]] = Field(default_factory=dict)
    narrative_inputs: list[str] = Field(default_factory=list)


class InputValidationOutput(BaseModel):
    """Step 1 output: normalized input and validation issues."""

    valid: bool
    issues: list[str] = Field(default_factory=list)
    normalized_input: TrialOpportunityRequest


class LiteratureRetrievalOutput(BaseModel):
    """Step 2 output: retrieved or provided literature sources."""

    sources: list[EvidenceItem] = Field(default_factory=list)
    missing_sources: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ClinicalTrialRetrievalOutput(BaseModel):
    """Step 3 output: retrieved or provided clinical trial sources."""

    trials: list[EvidenceItem] = Field(default_factory=list)
    invalid_nct_ids: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class EvidenceExtractionOutput(BaseModel):
    """Step 4 output: evidence ledger and extraction limitations."""

    ledger: EvidenceLedger
    unsupported_items: list[str] = Field(default_factory=list)


class UnmetNeed(BaseModel):
    """A structured unmet need mapped from evidence or explicitly degraded."""

    topic: str
    supporting_claims: list[str] = Field(default_factory=list)
    status: str = "needs_human_review"


class UnmetNeedMappingOutput(BaseModel):
    """Step 5 output: unmet need map."""

    unmet_needs: list[UnmetNeed] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class SWOTMatchingOutput(BaseModel):
    """Step 6 output: SWOT matching."""

    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    threats: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class NarrativeStrategy(BaseModel):
    """A stakeholder narrative draft grounded in evidence status."""

    audience: str
    narrative: str
    claim_type: ClaimType
    needs_human_review: bool


class NarrativeStrategyOutput(BaseModel):
    """Step 7 output: narrative strategy draft."""

    narratives: list[NarrativeStrategy] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class ComplianceReviewOutput(BaseModel):
    """Step 8 output: compliance and evidence review."""

    passed: bool
    requires_human_review: bool
    issues: list[GuardrailIssue] = Field(default_factory=list)


class FinalReportOutput(BaseModel):
    """Step 9 output: final Markdown draft plus ledger."""

    markdown: str
    ledger: EvidenceLedger
    limitations: list[str] = Field(default_factory=list)


class TrialOpportunityPipelineOutput(BaseModel):
    """Complete pipeline output with every step retained for auditability."""

    input_validation: InputValidationOutput
    literature_retrieval: LiteratureRetrievalOutput
    clinical_trial_retrieval: ClinicalTrialRetrievalOutput
    evidence_extraction: EvidenceExtractionOutput
    unmet_need_mapping: UnmetNeedMappingOutput
    swot_matching: SWOTMatchingOutput
    narrative_strategy: NarrativeStrategyOutput
    compliance_review: ComplianceReviewOutput
    final_report: FinalReportOutput


def _validate_input(request: TrialOpportunityRequest) -> InputValidationOutput:
    issues: list[str] = []
    for field_name in ("indication", "scenario", "audience"):
        if not getattr(request, field_name).strip():
            issues.append(f"{field_name} is required")
    return InputValidationOutput(valid=not issues, issues=issues, normalized_input=request)


def _retrieve_literature(request: TrialOpportunityRequest) -> LiteratureRetrievalOutput:
    notes = [
        "Using provided literature sources only.",
        "TODO: connect approved PubMed/DOI retrieval before production use.",
    ]
    missing = [] if request.literature_sources else ["literature_sources"]
    return LiteratureRetrievalOutput(
        sources=request.literature_sources,
        missing_sources=missing,
        notes=notes,
    )


def _retrieve_trials(request: TrialOpportunityRequest) -> ClinicalTrialRetrievalOutput:
    known_nct_ids = {
        identifier
        for source in request.clinical_trial_sources
        for identifier in source.identifiers
        if identifier.startswith("NCT")
    }
    invalid: list[str] = []
    for source in request.clinical_trial_sources:
        for identifier in source.identifiers:
            if identifier.startswith("NCT"):
                result = validate_nct_identifier(identifier, known_nct_ids=known_nct_ids)
                if not result.permitted:
                    invalid.append(identifier)

    notes = [
        "Using provided clinical trial sources only.",
        "TODO: connect approved ClinicalTrials.gov retrieval before production use.",
    ]
    return ClinicalTrialRetrievalOutput(
        trials=request.clinical_trial_sources,
        invalid_nct_ids=invalid,
        notes=notes,
    )


def _extract_evidence(
    request: TrialOpportunityRequest,
    literature: LiteratureRetrievalOutput,
    trials: ClinicalTrialRetrievalOutput,
) -> EvidenceExtractionOutput:
    sources = [*literature.sources, *trials.trials]
    claims = list(request.candidate_claims)
    unsupported: list[str] = []

    if not claims:
        unsupported.append("No candidate clinical claims supplied; output degraded to evidence gap.")
        claims.append(
            ClinicalClaim(
                claim_text="evidenza non identificata per clinical claims in the requested scenario",
                source_ids=[],
                claim_type=ClaimType.FACT,
                confidence=Confidence.INSUFFICIENT,
                evidence_level="evidenza non identificata",
                needs_human_review=True,
            )
        )

    ledger = EvidenceLedger(
        sources=sources,
        claims=claims,
        data_cutoff=request.data_cutoff,
        limitations=[*literature.missing_sources, *unsupported],
    )
    validation = validate_claims_against_sources(ledger, strict=False)
    unsupported.extend(issue.issue for issue in validation.issues)
    ledger.limitations.extend(issue.issue for issue in validation.issues)
    return EvidenceExtractionOutput(ledger=ledger, unsupported_items=unsupported)


def _map_unmet_needs(
    request: TrialOpportunityRequest,
    evidence: EvidenceExtractionOutput,
) -> UnmetNeedMappingOutput:
    if not request.unmet_need_topics:
        return UnmetNeedMappingOutput(
            unmet_needs=[
                UnmetNeed(
                    topic="evidenza non identificata",
                    supporting_claims=[],
                    status="insufficient_evidence",
                )
            ],
            limitations=["No unmet_need_topics supplied; unmet need map requires human input."],
        )

    claim_texts = [claim.claim_text for claim in evidence.ledger.claims if claim.source_ids]
    return UnmetNeedMappingOutput(
        unmet_needs=[
            UnmetNeed(topic=topic, supporting_claims=claim_texts, status="draft_human_review_required")
            for topic in request.unmet_need_topics
        ],
        limitations=[] if claim_texts else ["Unmet needs have no source-linked claims."],
    )


def _match_swot(request: TrialOpportunityRequest) -> SWOTMatchingOutput:
    swot = request.swot_inputs
    limitations: list[str] = []
    if not swot:
        limitations.append("No SWOT inputs supplied; SWOT matching degraded to empty draft.")

    return SWOTMatchingOutput(
        strengths=swot.get("strengths", []),
        weaknesses=swot.get("weaknesses", []),
        opportunities=swot.get("opportunities", []),
        threats=swot.get("threats", []),
        limitations=limitations,
    )


def _draft_narratives(
    request: TrialOpportunityRequest,
    unmet_needs: UnmetNeedMappingOutput,
) -> NarrativeStrategyOutput:
    if request.narrative_inputs:
        return NarrativeStrategyOutput(
            narratives=[
                NarrativeStrategy(
                    audience=request.audience,
                    narrative=narrative,
                    claim_type=ClaimType.HYPOTHESIS,
                    needs_human_review=True,
                )
                for narrative in request.narrative_inputs
            ]
        )

    topics = ", ".join(need.topic for need in unmet_needs.unmet_needs)
    return NarrativeStrategyOutput(
        narratives=[
            NarrativeStrategy(
                audience=request.audience,
                narrative=f"Draft narrative requires human review; mapped topics: {topics}",
                claim_type=ClaimType.HYPOTHESIS,
                needs_human_review=True,
            )
        ],
        limitations=["No narrative_inputs supplied; narrative is a degraded draft."],
    )


def _review_compliance(evidence: EvidenceExtractionOutput) -> ComplianceReviewOutput:
    validation = validate_claims_against_sources(evidence.ledger, strict=False)
    issues = [GuardrailIssue(message=issue.issue, severity=issue.severity) for issue in validation.issues]
    requires_human_review = bool(issues) or any(claim.needs_human_review for claim in evidence.ledger.claims)
    return ComplianceReviewOutput(
        passed=not issues,
        requires_human_review=requires_human_review,
        issues=issues,
    )


def _render_minimal_report(
    request: TrialOpportunityRequest,
    evidence: EvidenceExtractionOutput,
    unmet_needs: UnmetNeedMappingOutput,
    swot: SWOTMatchingOutput,
    narratives: NarrativeStrategyOutput,
    compliance: ComplianceReviewOutput,
) -> FinalReportOutput:
    from msl_agent.reports import render_nsclc_trial_opportunity_brief

    limitations = [
        *evidence.ledger.limitations,
        *unmet_needs.limitations,
        *swot.limitations,
        *narratives.limitations,
    ]
    markdown = render_nsclc_trial_opportunity_brief(
        request=request,
        ledger=evidence.ledger,
        unmet_needs=unmet_needs.unmet_needs,
        swot=swot,
        narratives=narratives.narratives,
        limitations=limitations,
        compliance=compliance,
    )
    return FinalReportOutput(markdown=markdown, ledger=evidence.ledger, limitations=limitations)


def run_trial_opportunity_pipeline(request: TrialOpportunityRequest) -> TrialOpportunityPipelineOutput:
    """Run the full MSL trial opportunity pipeline."""

    input_validation = _validate_input(request)
    literature = _retrieve_literature(input_validation.normalized_input)
    trials = _retrieve_trials(input_validation.normalized_input)
    evidence = _extract_evidence(input_validation.normalized_input, literature, trials)
    unmet_needs = _map_unmet_needs(input_validation.normalized_input, evidence)
    swot = _match_swot(input_validation.normalized_input)
    narratives = _draft_narratives(input_validation.normalized_input, unmet_needs)
    compliance = _review_compliance(evidence)
    final_report = _render_minimal_report(
        input_validation.normalized_input,
        evidence,
        unmet_needs,
        swot,
        narratives,
        compliance,
    )
    return TrialOpportunityPipelineOutput(
        input_validation=input_validation,
        literature_retrieval=literature,
        clinical_trial_retrieval=trials,
        evidence_extraction=evidence,
        unmet_need_mapping=unmet_needs,
        swot_matching=swot,
        narrative_strategy=narratives,
        compliance_review=compliance,
        final_report=final_report,
    )
