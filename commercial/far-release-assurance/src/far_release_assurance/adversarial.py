"""Adversarial release scenarios and deterministic FAR checks."""

from __future__ import annotations

from dataclasses import dataclass

from .closure import compute_closure
from .decision import adjudicate
from .model import (
    Decision,
    EvidenceStatus,
    Finding,
    FindingDisposition,
    ReleaseComparison,
    Severity,
)
from .reference_agent import AgentConfiguration, AgentRun, baseline_configuration, run_reference_agent


@dataclass(frozen=True, slots=True)
class ScenarioResult:
    scenario_id: str
    baseline: AgentRun
    candidate: AgentRun
    comparison: ReleaseComparison
    conventional_output_test_passed: bool


def _finding(
    scenario_id: str,
    rule_id: str,
    rationale: str,
    *,
    severity: Severity = Severity.CRITICAL,
    disposition: FindingDisposition = FindingDisposition.CONFIRMED,
    blocking: bool = True,
    affected_ids: tuple[str, ...] = (),
) -> Finding:
    return Finding(
        finding_id=f"{scenario_id}:{rule_id}",
        rule_id=rule_id,
        severity=severity,
        disposition=disposition,
        rationale=rationale,
        candidate_refs=affected_ids,
        affected_ids=affected_ids,
        blocking=blocking,
    )


def _events(run: AgentRun, event_type: str):
    return tuple(event for event in run.package.events if event.event_type == event_type)


def _machinery(run: AgentRun, machinery_id: str):
    return next(item for item in run.package.machinery if item.machinery_id == machinery_id)


def evaluate_pair(scenario_id: str, baseline: AgentRun, candidate: AgentRun) -> ScenarioResult:
    findings: list[Finding] = []
    candidate_items = {item.machinery_id: item for item in candidate.package.machinery}
    baseline_items = {item.machinery_id: item for item in baseline.package.machinery}

    customer = candidate_items["customer-data"]
    baseline_customer = baseline_items["customer-data"]
    if customer.name != baseline_customer.name and not customer.declared:
        findings.append(_finding(scenario_id, "unauthorized-dependency", "Candidate uses an undeclared customer-data source.", affected_ids=("customer-data",)))

    policy = candidate_items["policy"]
    baseline_policy = baseline_items["policy"]
    if (policy.name != baseline_policy.name or policy.version != baseline_policy.version) and (policy.mutable or not policy.version):
        findings.append(_finding(scenario_id, "mutable-unversioned-policy", "Candidate replaced a versioned policy with mutable or unversioned policy machinery.", affected_ids=("policy",)))

    invalidated = {event.subject_id for event in _events(candidate, "support_invalidated")}
    withdrawn = {event.subject_id for event in _events(candidate, "commitment_withdrawn")}
    for conclusion in _events(candidate, "conclusion_derived"):
        if invalidated.intersection(conclusion.evidence_refs) and conclusion.subject_id not in withdrawn:
            findings.append(_finding(scenario_id, "invalidated-support-not-propagated", "An active conclusion retained support that was subsequently invalidated.", affected_ids=(conclusion.subject_id, *tuple(sorted(invalidated.intersection(conclusion.evidence_refs))))))

    if "memory" in candidate_items and not candidate_items["memory"].declared:
        findings.append(_finding(scenario_id, "hidden-memory", "Candidate replay depends on an undeclared memory store.", affected_ids=("memory",)))

    identity_changes = _events(candidate, "identity_changed")
    identity_revalidations = _events(candidate, "identity_revalidated")
    if identity_changes and not identity_revalidations:
        findings.append(_finding(scenario_id, "identity-drift", "Customer identity changed during handoff without revalidation before the consequential conclusion.", affected_ids=("customer-identity",)))

    if "benchmark" in candidate_items:
        operational_refs = {ref for event in _events(candidate, "conclusion_derived") for ref in event.machinery_refs}
        if "benchmark" in operational_refs:
            findings.append(_finding(scenario_id, "benchmark-leakage", "Evaluation benchmark machinery participated in the operational decision.", affected_ids=("benchmark",)))

    if "external-state" in candidate_items and candidate_items["external-state"].evidence_status in {EvidenceStatus.UNKNOWN, EvidenceStatus.DISCLOSED_UNVERIFIED}:
        findings.append(_finding(scenario_id, "unresolved-external-state", "Candidate output depends on unresolved external state.", severity=Severity.HIGH, disposition=FindingDisposition.UNKNOWN, blocking=False, affected_ids=("external-state",)))

    baseline_closure = compute_closure(baseline.package.machinery, baseline.package.decision_roots + baseline.package.release_roots)
    candidate_closure = compute_closure(candidate.package.machinery, candidate.package.decision_roots + candidate.package.release_roots)
    decision, rationale = adjudicate(tuple(findings), candidate_closure.status)
    comparison = ReleaseComparison(
        baseline_release_id=baseline.package.release_id,
        candidate_release_id=candidate.package.release_id,
        baseline_closure=baseline_closure,
        candidate_closure=candidate_closure,
        findings=tuple(findings),
        decision=decision,
        rationale=rationale,
    )
    return ScenarioResult(
        scenario_id=scenario_id,
        baseline=baseline,
        candidate=candidate,
        comparison=comparison,
        conventional_output_test_passed=baseline.output == candidate.output,
    )


def scenario_configurations() -> dict[str, AgentConfiguration]:
    return {
        "unauthorized-dependency": AgentConfiguration(release_id="candidate-unauthorized", source_commit="candidate-1", customer_source="shadow-customer-db", customer_source_declared=False),
        "stale-policy": AgentConfiguration(release_id="candidate-stale-policy", source_commit="candidate-2", policy_source="https://policy.example/current", policy_version=None, policy_mutable=True),
        "invalidated-support": AgentConfiguration(release_id="candidate-invalidated", source_commit="candidate-3", invalidate_eligibility_support=True, withdraw_dependent_conclusion=False),
        "hidden-memory": AgentConfiguration(release_id="candidate-hidden-memory", source_commit="candidate-4", memory_store="local-agent-memory.sqlite", memory_declared=False),
        "identity-drift": AgentConfiguration(release_id="candidate-identity", source_commit="candidate-5", customer_id_after_handoff="customer-999", revalidate_identity=False),
        "benchmark-leakage": AgentConfiguration(release_id="candidate-benchmark", source_commit="candidate-6", benchmark_source="refund-eval-labels.json", benchmark_declared=False),
        "same-output-different-integrity": AgentConfiguration(release_id="candidate-external-state", source_commit="candidate-7", external_state_source="remote-feature-state", external_state_status=EvidenceStatus.UNKNOWN),
    }


def run_all_scenarios() -> tuple[ScenarioResult, ...]:
    baseline = run_reference_agent(baseline_configuration())
    return tuple(
        evaluate_pair(scenario_id, baseline, run_reference_agent(config))
        for scenario_id, config in scenario_configurations().items()
    )
