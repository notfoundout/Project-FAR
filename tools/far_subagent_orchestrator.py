"""Deterministic, provider-neutral subagent orchestration for Project FAR.

FAR-SUBAGENT-1.0 mechanizes execution boundaries around existing FAR research
skills. It does not amend FAR theory, establish external independence, or turn
model agreement into evidence.
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping, Protocol, Sequence

try:
    from tools.adversarial_research_harness import (
        assert_distinct_lane_sandboxes,
        lane_sandbox_id,
    )
except ModuleNotFoundError as exc:
    # Direct execution sets sys.path[0] to tools/, so "tools." is unavailable.
    if not (exc.name == "tools" or str(exc.name).startswith("tools.")):
        raise
    from adversarial_research_harness import (  # type: ignore[no-redef]
        assert_distinct_lane_sandboxes,
        lane_sandbox_id,
    )


class EvidenceClass(str, Enum):
    P = "P"
    C = "C"
    A = "A"
    I = "I"


class Disposition(str, Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    UNCERTAIN = "uncertain"


class Recommendation(str, Enum):
    NONE = "none"
    ACCEPT = "accept"
    REJECT = "reject"
    UNCERTAIN = "uncertain"


class AgentStatus(str, Enum):
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class DependencyView(str, Enum):
    CLAIMS_ONLY = "claims-only"
    FINDINGS = "findings"
    FULL = "full"


class AgentRole(str, Enum):
    CLAIM_REGISTRY = "claim-registry"
    DISCOVERY = "discovery"
    EVIDENCE = "evidence"
    COUNTEREXAMPLE = "counterexample"
    FORMALIZER = "formalizer"
    CLEAN_ROOM = "clean-room"
    CONTRADICTION = "contradiction"
    QUALITY_GATE = "quality-gate"


ROLE_SKILLS: Mapping[AgentRole, str] = {
    AgentRole.CLAIM_REGISTRY: "far-claim-registry",
    AgentRole.DISCOVERY: "far-discovery-engine",
    AgentRole.EVIDENCE: "far-evidence-ledger",
    AgentRole.COUNTEREXAMPLE: "far-counterexample-hunter",
    AgentRole.FORMALIZER: "far-formalizer",
    AgentRole.CLEAN_ROOM: "far-clean-room-auditor",
    AgentRole.CONTRADICTION: "far-contradiction-detector",
    AgentRole.QUALITY_GATE: "far-research-quality-gate",
}

_CLEAN_ROOM_FORBIDDEN_CONTEXT = frozenset(
    {
        "accepted_answer",
        "preferred_conclusion",
        "prior_far_verdict",
        "prior_target_conclusion",
        "synthesis",
        "target_conclusion",
    }
)


@dataclass(frozen=True)
class ClaimFinding:
    claim_id: str
    claim: str
    evidence_class: EvidenceClass
    disposition: Disposition
    rationale: str
    provenance: tuple[str, ...] = ()
    uncertainty: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "provenance", tuple(self.provenance))
        if not self.claim_id.strip() or not self.claim.strip():
            raise ValueError("claim_id and claim must be non-empty")
        if not self.rationale.strip():
            raise ValueError("rationale must be non-empty")
        if self.evidence_class in {EvidenceClass.P, EvidenceClass.C} and (
            not self.provenance or any(not item.strip() for item in self.provenance)
        ):
            raise ValueError("P/C findings require non-empty provenance")


@dataclass(frozen=True)
class ConflictResolution:
    claim_id: str
    disposition: Disposition
    rationale: str
    provenance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "provenance", tuple(self.provenance))
        if not self.claim_id.strip() or not self.rationale.strip():
            raise ValueError("resolution claim_id and rationale must be non-empty")
        if self.disposition is not Disposition.UNCERTAIN and (
            not self.provenance or any(not item.strip() for item in self.provenance)
        ):
            raise ValueError("decisive conflict resolutions require provenance")


@dataclass(frozen=True)
class SubagentTask:
    task_id: str
    role: AgentRole
    objective: str
    context_keys: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    dependency_view: DependencyView = DependencyView.FULL
    clean_room: bool = False
    done_criteria: tuple[str, ...] = ()
    exclusions: tuple[str, ...] = ()
    read_only: bool = True

    def __post_init__(self) -> None:
        for field in ("context_keys", "dependencies", "done_criteria", "exclusions"):
            object.__setattr__(self, field, tuple(getattr(self, field)))
        if not self.task_id.strip() or not self.objective.strip():
            raise ValueError("task_id and objective must be non-empty")
        if len(set(self.dependencies)) != len(self.dependencies):
            raise ValueError(f"{self.task_id}: duplicate dependencies")
        if self.task_id in self.dependencies:
            raise ValueError(f"{self.task_id}: task cannot depend on itself")
        if len(set(self.context_keys)) != len(self.context_keys):
            raise ValueError(f"{self.task_id}: duplicate context keys")
        if not self.read_only:
            raise ValueError(
                f"{self.task_id}: specialist subagents are read-only; "
                "repository mutation remains coordinator-owned"
            )
        if self.clean_room:
            if self.dependency_view is not DependencyView.CLAIMS_ONLY:
                raise ValueError(
                    f"{self.task_id}: clean-room tasks require claims-only dependency view"
                )
            leaked = _CLEAN_ROOM_FORBIDDEN_CONTEXT.intersection(self.context_keys)
            if leaked:
                raise ValueError(
                    f"{self.task_id}: clean-room task exposes forbidden context {sorted(leaked)}"
                )

    @property
    def skill(self) -> str:
        return ROLE_SKILLS[self.role]


@dataclass(frozen=True)
class SubagentReport:
    task_id: str
    role: AgentRole
    status: AgentStatus
    summary: str
    sandbox_id: str
    context_digest: str
    findings: tuple[ClaimFinding, ...] = ()
    recommendation: Recommendation = Recommendation.NONE
    resolutions: tuple[ConflictResolution, ...] = ()
    errors: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field in ("findings", "resolutions", "errors"):
            object.__setattr__(self, field, tuple(getattr(self, field)))
        if not self.task_id.strip() or not self.sandbox_id.strip() or not self.context_digest.strip():
            raise ValueError("report task_id, sandbox_id, and context_digest must be non-empty")
        if self.status is AgentStatus.COMPLETED and not self.summary.strip():
            raise ValueError("completed reports require a summary")
        if self.status is AgentStatus.FAILED and not self.errors:
            raise ValueError("failed reports require an error")
        claim_ids = [finding.claim_id for finding in self.findings]
        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError(f"{self.task_id}: duplicate finding claim_id values")


class SubagentRunner(Protocol):
    def __call__(
        self,
        *,
        task: SubagentTask,
        context: Mapping[str, Any],
        sandbox_id: str,
        context_digest: str,
    ) -> SubagentReport: ...


@dataclass(frozen=True)
class FindingConflict:
    claim_id: str
    supporting_tasks: tuple[str, ...]
    contradicting_tasks: tuple[str, ...]
    resolution: ConflictResolution | None = None
    resolver_task_id: str | None = None

    @property
    def resolved(self) -> bool:
        return (
            self.resolution is not None
            and self.resolution.disposition is not Disposition.UNCERTAIN
        )


@dataclass(frozen=True)
class OrchestrationResult:
    reports: tuple[SubagentReport, ...]
    conflicts: tuple[FindingConflict, ...]
    gate_issues: tuple[str, ...]
    promotion_allowed: bool

    def report(self, task_id: str) -> SubagentReport:
        for report in self.reports:
            if report.task_id == task_id:
                return report
        raise KeyError(task_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "reports": [_report_to_dict(report) for report in self.reports],
            "conflicts": [
                {
                    "claim_id": conflict.claim_id,
                    "supporting_tasks": list(conflict.supporting_tasks),
                    "contradicting_tasks": list(conflict.contradicting_tasks),
                    "resolved": conflict.resolved,
                    "resolver_task_id": conflict.resolver_task_id,
                    "resolution": (
                        _resolution_to_dict(conflict.resolution)
                        if conflict.resolution is not None
                        else None
                    ),
                }
                for conflict in self.conflicts
            ],
            "gate_issues": list(self.gate_issues),
            "promotion_allowed": self.promotion_allowed,
        }


class SubagentCoordinator:
    def __init__(
        self,
        tasks: Sequence[SubagentTask],
        runner: SubagentRunner,
        *,
        base_context: Mapping[str, Any] | None = None,
        run_root: str = "far-subagents",
        max_workers: int = 4,
        require_quality_gate: bool = True,
    ) -> None:
        if not tasks:
            raise ValueError("at least one subagent task is required")
        if max_workers < 1:
            raise ValueError("max_workers must be >= 1")
        self.tasks = tuple(tasks)
        self.runner = runner
        self.base_context = deepcopy(dict(base_context or {}))
        self.run_root = run_root
        self.max_workers = max_workers
        self.require_quality_gate = require_quality_gate
        _assert_json_compatible(self.base_context, "base_context")
        self._task_by_id = _validate_task_graph(self.tasks, self.base_context)
        assert_distinct_lane_sandboxes(
            [self._sandbox_id(self._task_by_id[task_id]) for task_id in sorted(self._task_by_id)]
        )

    def run(self, *, parallel: bool = True) -> OrchestrationResult:
        pending = set(self._task_by_id)
        reports: dict[str, SubagentReport] = {}

        while pending:
            ready = [
                self._task_by_id[task_id]
                for task_id in sorted(pending)
                if all(dep in reports for dep in self._task_by_id[task_id].dependencies)
            ]
            if not ready:
                raise RuntimeError("subagent DAG made no progress")

            runnable: list[SubagentTask] = []
            for task in ready:
                bad_dependencies = [
                    dep
                    for dep in task.dependencies
                    if reports[dep].status is not AgentStatus.COMPLETED
                ]
                if bad_dependencies:
                    reports[task.task_id] = self._blocked_report(
                        task, bad_dependencies, reports
                    )
                else:
                    runnable.append(task)

            if runnable:
                reports.update(self._run_batch(runnable, reports, parallel=parallel))
            pending.difference_update(task.task_id for task in ready)

        ordered = tuple(reports[task.task_id] for task in self.tasks)
        conflicts = _detect_conflicts(ordered)
        issues = _gate_issues(
            ordered,
            conflicts,
            require_quality_gate=self.require_quality_gate,
        )
        return OrchestrationResult(
            ordered,
            conflicts,
            issues,
            _promotion_allowed(
                ordered,
                issues,
                require_quality_gate=self.require_quality_gate,
            ),
        )

    def _run_batch(
        self,
        tasks: Sequence[SubagentTask],
        reports: Mapping[str, SubagentReport],
        *,
        parallel: bool,
    ) -> dict[str, SubagentReport]:
        if not parallel or len(tasks) == 1:
            return {task.task_id: self._execute_task(task, reports) for task in tasks}

        completed: dict[str, SubagentReport] = {}
        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(tasks))) as pool:
            futures = {
                pool.submit(self._execute_task, task, reports): task.task_id
                for task in tasks
            }
            for future in as_completed(futures):
                task_id = futures[future]
                try:
                    completed[task_id] = future.result()
                except Exception as exc:  # defensive executor boundary
                    completed[task_id] = self._failed_report(
                        self._task_by_id[task_id],
                        context_digest="unavailable",
                        error=f"{type(exc).__name__}: {exc}",
                    )
        return completed

    def _execute_task(
        self,
        task: SubagentTask,
        reports: Mapping[str, SubagentReport],
    ) -> SubagentReport:
        context = self._context_for(task, reports)
        digest = _context_digest(context)
        sandbox_id = self._sandbox_id(task)
        try:
            report = self.runner(
                task=task,
                context=deepcopy(context),
                sandbox_id=sandbox_id,
                context_digest=digest,
            )
            _validate_report_binding(report, task, sandbox_id, digest)
            return report
        except Exception as exc:
            return self._failed_report(
                task,
                context_digest=digest,
                error=f"{type(exc).__name__}: {exc}",
            )

    def _context_for(
        self,
        task: SubagentTask,
        reports: Mapping[str, SubagentReport],
    ) -> dict[str, Any]:
        context = {key: deepcopy(self.base_context[key]) for key in task.context_keys}
        if task.dependencies:
            context["_dependencies"] = {
                dep: _project_dependency(reports[dep], task.dependency_view)
                for dep in task.dependencies
            }
        _assert_json_compatible(context, f"context for {task.task_id}")
        return context

    def _sandbox_id(self, task: SubagentTask) -> str:
        return lane_sandbox_id(f"subagent:{task.task_id}", run_root=self.run_root)

    def _blocked_report(
        self,
        task: SubagentTask,
        bad_dependencies: Sequence[str],
        reports: Mapping[str, SubagentReport],
    ) -> SubagentReport:
        context = self._context_for(task, reports)
        return SubagentReport(
            task.task_id,
            task.role,
            AgentStatus.BLOCKED,
            "",
            self._sandbox_id(task),
            _context_digest(context),
            errors=("dependency failure: " + ", ".join(sorted(bad_dependencies)),),
        )

    def _failed_report(
        self,
        task: SubagentTask,
        *,
        context_digest: str,
        error: str,
    ) -> SubagentReport:
        return SubagentReport(
            task.task_id,
            task.role,
            AgentStatus.FAILED,
            "",
            self._sandbox_id(task),
            context_digest,
            errors=(error,),
        )


def default_far_subagent_plan(
    *,
    objective: str,
    context_keys: Sequence[str] = ("research_question", "frozen_inputs"),
) -> tuple[SubagentTask, ...]:
    if not objective.strip():
        raise ValueError("objective must be non-empty")
    keys = tuple(context_keys)
    leaked = _CLEAN_ROOM_FORBIDDEN_CONTEXT.intersection(keys)
    if leaked:
        raise ValueError(
            "default plan cannot expose conclusion-bearing context to clean-room "
            f"lane: {sorted(leaked)}"
        )

    claim = SubagentTask(
        "claim-registry",
        AgentRole.CLAIM_REGISTRY,
        f"Decompose and register the atomic claims for: {objective}",
        keys,
        done_criteria=(
            "Each material claim has a stable claim_id and exact wording.",
            "Scope and assumptions are explicit.",
        ),
    )

    claims_only = (("claim-registry",), DependencyView.CLAIMS_ONLY)
    discovery = SubagentTask(
        "discovery",
        AgentRole.DISCOVERY,
        "Search broadly for material evidence and competing explanations.",
        keys,
        *claims_only,
        done_criteria=("Material candidate evidence and alternatives are surfaced.",),
    )
    evidence = SubagentTask(
        "evidence",
        AgentRole.EVIDENCE,
        "Build provenance-bearing evidence for and against each atomic claim.",
        keys,
        *claims_only,
        done_criteria=(
            "P/C evidence has source provenance.",
            "Support and counterevidence are separated.",
        ),
    )
    counterexamples = SubagentTask(
        "counterexamples",
        AgentRole.COUNTEREXAMPLE,
        "Actively seek counterexamples and scope-breaking cases.",
        keys,
        *claims_only,
        done_criteria=("Strongest discovered falsifiers are recorded.",),
    )
    formalizer = SubagentTask(
        "formalizer",
        AgentRole.FORMALIZER,
        "Formalize inferential structure and expose hidden assumptions.",
        keys,
        *claims_only,
        done_criteria=(
            "Premises, conclusion, assumptions, and failure conditions are explicit.",
        ),
    )
    clean_room = SubagentTask(
        "clean-room",
        AgentRole.CLEAN_ROOM,
        "Independently evaluate the frozen target claims without prior verdicts.",
        keys,
        *claims_only,
        clean_room=True,
        exclusions=(
            "Prior FAR verdicts",
            "Preferred conclusion",
            "Construction-session synthesis",
        ),
        done_criteria=(
            "The first-pass verdict is recorded before exposure to prior conclusions.",
        ),
    )
    contradictions = SubagentTask(
        "contradictions",
        AgentRole.CONTRADICTION,
        "Compare specialist outputs and adjudicate explicit contradictions.",
        keys,
        ("discovery", "evidence", "counterexamples", "formalizer", "clean-room"),
        DependencyView.FULL,
        done_criteria=(
            "Every support/contradiction collision is preserved or explicitly resolved.",
        ),
    )
    quality_gate = SubagentTask(
        "quality-gate",
        AgentRole.QUALITY_GATE,
        "Apply FAR acceptance and closure gates to the frozen specialist packet.",
        keys,
        (
            "claim-registry",
            "discovery",
            "evidence",
            "counterexamples",
            "formalizer",
            "clean-room",
            "contradictions",
        ),
        DependencyView.FULL,
        done_criteria=(
            "Evidence classes and provenance are valid.",
            "Unresolved contradictions block promotion.",
            "I-class material is not used to validate FAR.",
        ),
    )
    return (
        claim,
        discovery,
        evidence,
        counterexamples,
        formalizer,
        clean_room,
        contradictions,
        quality_gate,
    )


def plan_to_dict(tasks: Sequence[SubagentTask]) -> dict[str, Any]:
    return {
        "protocol": "FAR-SUBAGENT-1.0",
        "coordinator": "far-research-orchestrator",
        "specialists": [
            {
                "task_id": task.task_id,
                "role": task.role.value,
                "skill": task.skill,
                "objective": task.objective,
                "context_keys": list(task.context_keys),
                "dependencies": list(task.dependencies),
                "dependency_view": task.dependency_view.value,
                "clean_room": task.clean_room,
                "read_only": task.read_only,
                "done_criteria": list(task.done_criteria),
                "exclusions": list(task.exclusions),
            }
            for task in tasks
        ],
    }


def _validate_task_graph(
    tasks: Sequence[SubagentTask],
    base_context: Mapping[str, Any],
) -> dict[str, SubagentTask]:
    task_by_id: dict[str, SubagentTask] = {}
    for task in tasks:
        if task.task_id in task_by_id:
            raise ValueError(f"duplicate task_id: {task.task_id}")
        task_by_id[task.task_id] = task

    for task in tasks:
        missing_deps = set(task.dependencies).difference(task_by_id)
        if missing_deps:
            raise ValueError(f"{task.task_id}: unknown dependencies {sorted(missing_deps)}")
        missing_context = set(task.context_keys).difference(base_context)
        if missing_context:
            raise ValueError(f"{task.task_id}: missing base context {sorted(missing_context)}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visited:
            return
        if task_id in visiting:
            raise ValueError(f"cycle detected at task {task_id}")
        visiting.add(task_id)
        for dependency in task_by_id[task_id].dependencies:
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in task_by_id:
        visit(task_id)
    return task_by_id


def _project_dependency(report: SubagentReport, view: DependencyView) -> dict[str, Any]:
    if view is DependencyView.CLAIMS_ONLY:
        return {
            "task_id": report.task_id,
            "claims": [
                {"claim_id": finding.claim_id, "claim": finding.claim}
                for finding in report.findings
            ],
        }
    if view is DependencyView.FINDINGS:
        return {
            "task_id": report.task_id,
            "findings": [_finding_to_dict(finding) for finding in report.findings],
        }
    return _report_to_dict(report)


def _validate_report_binding(
    report: SubagentReport,
    task: SubagentTask,
    sandbox_id: str,
    context_digest: str,
) -> None:
    errors: list[str] = []
    if report.task_id != task.task_id:
        errors.append(f"task_id {report.task_id!r} != {task.task_id!r}")
    if report.role is not task.role:
        errors.append(f"role {report.role.value!r} != {task.role.value!r}")
    if report.sandbox_id != sandbox_id:
        errors.append("sandbox_id mismatch")
    if report.context_digest != context_digest:
        errors.append("context_digest mismatch")
    if report.resolutions and task.role is not AgentRole.CONTRADICTION:
        errors.append("only contradiction tasks may emit conflict resolutions")
    if errors:
        raise ValueError(
            f"{task.task_id}: runner returned report bound to wrong execution: "
            + "; ".join(errors)
        )


def _detect_conflicts(reports: Sequence[SubagentReport]) -> tuple[FindingConflict, ...]:
    by_claim: dict[str, dict[Disposition, set[str]]] = {}
    resolutions: dict[str, list[tuple[str, ConflictResolution]]] = {}

    for report in reports:
        if report.status is not AgentStatus.COMPLETED:
            continue
        for finding in report.findings:
            if finding.disposition not in {Disposition.SUPPORTS, Disposition.CONTRADICTS}:
                continue
            bucket = by_claim.setdefault(
                finding.claim_id,
                {Disposition.SUPPORTS: set(), Disposition.CONTRADICTS: set()},
            )
            bucket[finding.disposition].add(report.task_id)
        for resolution in report.resolutions:
            resolutions.setdefault(resolution.claim_id, []).append(
                (report.task_id, resolution)
            )

    conflicts: list[FindingConflict] = []
    for claim_id in sorted(by_claim):
        support = tuple(sorted(by_claim[claim_id][Disposition.SUPPORTS]))
        contradict = tuple(sorted(by_claim[claim_id][Disposition.CONTRADICTS]))
        if not support or not contradict:
            continue

        candidates = resolutions.get(claim_id, [])
        resolver: str | None = None
        resolution: ConflictResolution | None = None
        if len(candidates) == 1:
            resolver, resolution = candidates[0]
        elif len(candidates) > 1:
            decisive = [
                item for item in candidates
                if item[1].disposition is not Disposition.UNCERTAIN
            ]
            dispositions = {item[1].disposition for item in decisive}
            if len(dispositions) == 1 and decisive:
                resolver, resolution = sorted(decisive, key=lambda item: item[0])[0]

        conflicts.append(
            FindingConflict(claim_id, support, contradict, resolution, resolver)
        )
    return tuple(conflicts)


def _gate_issues(
    reports: Sequence[SubagentReport],
    conflicts: Sequence[FindingConflict],
    *,
    require_quality_gate: bool,
) -> tuple[str, ...]:
    issues: list[str] = []
    for report in reports:
        if report.status is AgentStatus.FAILED:
            issues.append(f"{report.task_id}: failed")
        elif report.status is AgentStatus.BLOCKED:
            issues.append(f"{report.task_id}: blocked")

    for conflict in conflicts:
        if not conflict.resolved:
            issues.append(f"{conflict.claim_id}: unresolved cross-agent conflict")

    if require_quality_gate:
        quality = [report for report in reports if report.role is AgentRole.QUALITY_GATE]
        if not quality:
            issues.append("quality-gate: required task missing")
        elif any(report.status is not AgentStatus.COMPLETED for report in quality):
            issues.append("quality-gate: did not complete")
        elif any(report.recommendation is Recommendation.ACCEPT for report in quality):
            qualifying_support = any(
                finding.disposition is Disposition.SUPPORTS
                and finding.evidence_class is not EvidenceClass.I
                for report in reports
                if report.status is AgentStatus.COMPLETED
                for finding in report.findings
            )
            if not qualifying_support:
                issues.append("quality-gate: acceptance lacks non-I supporting evidence")

    return tuple(dict.fromkeys(issues))


def _promotion_allowed(
    reports: Sequence[SubagentReport],
    issues: Sequence[str],
    *,
    require_quality_gate: bool,
) -> bool:
    if issues:
        return False
    if not require_quality_gate:
        return True
    return any(
        report.role is AgentRole.QUALITY_GATE
        and report.status is AgentStatus.COMPLETED
        and report.recommendation is Recommendation.ACCEPT
        for report in reports
    )


def _context_digest(context: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        context,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _assert_json_compatible(value: Any, label: str) -> None:
    try:
        json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be JSON-compatible: {exc}") from exc


def _finding_to_dict(finding: ClaimFinding) -> dict[str, Any]:
    return {
        "claim_id": finding.claim_id,
        "claim": finding.claim,
        "evidence_class": finding.evidence_class.value,
        "disposition": finding.disposition.value,
        "rationale": finding.rationale,
        "provenance": list(finding.provenance),
        "uncertainty": finding.uncertainty,
    }


def _resolution_to_dict(resolution: ConflictResolution) -> dict[str, Any]:
    return {
        "claim_id": resolution.claim_id,
        "disposition": resolution.disposition.value,
        "rationale": resolution.rationale,
        "provenance": list(resolution.provenance),
    }


def _report_to_dict(report: SubagentReport) -> dict[str, Any]:
    return {
        "task_id": report.task_id,
        "role": report.role.value,
        "status": report.status.value,
        "summary": report.summary,
        "sandbox_id": report.sandbox_id,
        "context_digest": report.context_digest,
        "findings": [_finding_to_dict(finding) for finding in report.findings],
        "recommendation": report.recommendation.value,
        "resolutions": [_resolution_to_dict(item) for item in report.resolutions],
        "errors": list(report.errors),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect the Project FAR subagent plan.")
    parser.add_argument(
        "--objective",
        default="Evaluate a bounded FAR research question.",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            plan_to_dict(default_far_subagent_plan(objective=args.objective)),
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
