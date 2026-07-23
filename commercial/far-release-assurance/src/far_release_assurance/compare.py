"""Deterministic baseline-versus-candidate release comparison."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping

from .closure import assess_closure
from .decision import adjudicate
from .model import (
    EvidenceStatus,
    Finding,
    FindingDisposition,
    ReleaseComparison,
    ReleasePackage,
    Severity,
)


@dataclass(frozen=True, slots=True)
class MachineryDelta:
    added: tuple[str, ...]
    removed: tuple[str, ...]
    changed: tuple[str, ...]
    newly_unresolved: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ComparisonSummary:
    comparison: ReleaseComparison
    machinery: MachineryDelta
    replay_delta: float | None
    output_metric_deltas: Mapping[str, float]
    event_type_deltas: Mapping[str, int]


def _finding(
    rule_id: str,
    rationale: str,
    *,
    severity: Severity,
    disposition: FindingDisposition = FindingDisposition.CONFIRMED,
    blocking: bool = False,
    baseline_refs: tuple[str, ...] = (),
    candidate_refs: tuple[str, ...] = (),
) -> Finding:
    return Finding(
        finding_id=f"compare:{rule_id}:{','.join(candidate_refs or baseline_refs) or 'release'}",
        rule_id=rule_id,
        severity=severity,
        disposition=disposition,
        rationale=rationale,
        baseline_refs=baseline_refs,
        candidate_refs=candidate_refs,
        affected_ids=tuple(sorted(set(baseline_refs + candidate_refs))),
        blocking=blocking,
    )


def _machinery_signature(item) -> tuple[object, ...]:
    return (
        item.kind,
        item.name,
        item.version,
        item.digest,
        tuple(sorted(item.required_dependencies)),
        item.evidence_status,
        item.declared,
        item.effective,
        item.valid,
        item.mutable,
        item.external,
        tuple(sorted(item.attributes.items())),
    )


def _event_counts(package: ReleasePackage) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event in package.events:
        counts[event.event_type] = counts.get(event.event_type, 0) + 1
    return counts


def compare_releases(baseline: ReleasePackage, candidate: ReleasePackage) -> ComparisonSummary:
    baseline_items = {item.machinery_id: item for item in baseline.machinery}
    candidate_items = {item.machinery_id: item for item in candidate.machinery}

    added = tuple(sorted(candidate_items.keys() - baseline_items.keys()))
    removed = tuple(sorted(baseline_items.keys() - candidate_items.keys()))
    changed = tuple(
        sorted(
            machinery_id
            for machinery_id in baseline_items.keys() & candidate_items.keys()
            if _machinery_signature(baseline_items[machinery_id])
            != _machinery_signature(candidate_items[machinery_id])
        )
    )
    newly_unresolved = tuple(
        sorted(
            machinery_id
            for machinery_id, item in candidate_items.items()
            if item.unresolved()
            and (
                machinery_id not in baseline_items
                or not baseline_items[machinery_id].unresolved()
            )
        )
    )

    findings: list[Finding] = []
    for machinery_id in added:
        item = candidate_items[machinery_id]
        if not item.declared:
            findings.append(
                _finding(
                    "undeclared-machinery-added",
                    f"Candidate introduced undeclared machinery {machinery_id}.",
                    severity=Severity.CRITICAL,
                    blocking=True,
                    candidate_refs=(machinery_id,),
                )
            )
        elif item.mutable and item.kind == "policy":
            findings.append(
                _finding(
                    "mutable-policy-added",
                    f"Candidate introduced mutable policy machinery {machinery_id}.",
                    severity=Severity.HIGH,
                    blocking=True,
                    candidate_refs=(machinery_id,),
                )
            )

    for machinery_id in changed:
        before = baseline_items[machinery_id]
        after = candidate_items[machinery_id]
        if after.kind == "policy" and (after.mutable or not after.version):
            findings.append(
                _finding(
                    "policy-version-regression",
                    f"Policy machinery {machinery_id} became mutable or unversioned.",
                    severity=Severity.HIGH,
                    blocking=True,
                    baseline_refs=(machinery_id,),
                    candidate_refs=(machinery_id,),
                )
            )
        if not before.unresolved() and after.unresolved():
            findings.append(
                _finding(
                    "machinery-evidence-regression",
                    f"Machinery {machinery_id} became unresolved in the candidate.",
                    severity=Severity.HIGH,
                    disposition=FindingDisposition.UNKNOWN,
                    candidate_refs=(machinery_id,),
                )
            )
        if before.declared and not after.declared:
            findings.append(
                _finding(
                    "machinery-disclosure-regression",
                    f"Machinery {machinery_id} changed from declared to undeclared.",
                    severity=Severity.CRITICAL,
                    blocking=True,
                    candidate_refs=(machinery_id,),
                )
            )

    if removed:
        findings.append(
            _finding(
                "machinery-removed",
                "Candidate removed previously disclosed machinery; human review is required.",
                severity=Severity.MEDIUM,
                baseline_refs=removed,
            )
        )

    candidate_invalidated = {
        event.subject_id
        for event in candidate.events
        if event.event_type == "support_invalidated"
    }
    candidate_withdrawn = {
        event.subject_id
        for event in candidate.events
        if event.event_type == "commitment_withdrawn"
    }
    for event in candidate.events:
        if event.event_type != "conclusion_derived":
            continue
        invalid_support = tuple(sorted(candidate_invalidated.intersection(event.evidence_refs)))
        if invalid_support and event.subject_id not in candidate_withdrawn:
            findings.append(
                _finding(
                    "invalidated-support-not-propagated",
                    f"Conclusion {event.subject_id} retained invalidated support.",
                    severity=Severity.CRITICAL,
                    blocking=True,
                    candidate_refs=(event.subject_id, *invalid_support),
                )
            )

    identity_changes = sum(event.event_type == "identity_changed" for event in candidate.events)
    identity_revalidations = sum(event.event_type == "identity_revalidated" for event in candidate.events)
    if identity_changes > identity_revalidations:
        findings.append(
            _finding(
                "identity-revalidation-deficit",
                "Candidate contains an identity change without a matching revalidation.",
                severity=Severity.CRITICAL,
                blocking=True,
                candidate_refs=("identity",),
            )
        )

    replay_delta = None
    if baseline.replay_completeness is not None and candidate.replay_completeness is not None:
        replay_delta = candidate.replay_completeness - baseline.replay_completeness
        if replay_delta < 0:
            findings.append(
                _finding(
                    "replay-completeness-regression",
                    f"Replay completeness decreased by {abs(replay_delta):.6f}.",
                    severity=Severity.MEDIUM,
                    candidate_refs=(candidate.release_id,),
                )
            )

    metric_names = sorted(set(baseline.output_metrics) | set(candidate.output_metrics))
    output_metric_deltas = {
        name: candidate.output_metrics.get(name, 0.0) - baseline.output_metrics.get(name, 0.0)
        for name in metric_names
    }

    baseline_counts = _event_counts(baseline)
    candidate_counts = _event_counts(candidate)
    event_type_deltas = {
        name: candidate_counts.get(name, 0) - baseline_counts.get(name, 0)
        for name in sorted(set(baseline_counts) | set(candidate_counts))
        if candidate_counts.get(name, 0) != baseline_counts.get(name, 0)
    }

    baseline_closure = assess_closure(
        baseline.machinery, baseline.decision_roots + baseline.release_roots
    )
    candidate_closure = assess_closure(
        candidate.machinery, candidate.decision_roots + candidate.release_roots
    )
    decision, rationale = adjudicate(tuple(findings), candidate_closure.status)
    comparison = ReleaseComparison(
        baseline_release_id=baseline.release_id,
        candidate_release_id=candidate.release_id,
        baseline_closure=baseline_closure,
        candidate_closure=candidate_closure,
        findings=tuple(sorted(findings, key=lambda finding: finding.finding_id)),
        decision=decision,
        rationale=rationale,
    )
    return ComparisonSummary(
        comparison=comparison,
        machinery=MachineryDelta(added, removed, changed, newly_unresolved),
        replay_delta=replay_delta,
        output_metric_deltas=output_metric_deltas,
        event_type_deltas=event_type_deltas,
    )


def comparison_to_dict(summary: ComparisonSummary) -> dict[str, object]:
    comparison = summary.comparison
    return {
        "schema_version": "far-release-comparison/0.1",
        "baseline_release_id": comparison.baseline_release_id,
        "candidate_release_id": comparison.candidate_release_id,
        "decision": comparison.decision.value,
        "rationale": comparison.rationale,
        "baseline_closure": asdict(comparison.baseline_closure),
        "candidate_closure": asdict(comparison.candidate_closure),
        "machinery": asdict(summary.machinery),
        "replay_delta": summary.replay_delta,
        "output_metric_deltas": dict(sorted(summary.output_metric_deltas.items())),
        "event_type_deltas": dict(sorted(summary.event_type_deltas.items())),
        "findings": [
            {
                **asdict(finding),
                "severity": finding.severity.value,
                "disposition": finding.disposition.value,
            }
            for finding in comparison.findings
        ],
    }
