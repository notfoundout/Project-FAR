from __future__ import annotations

import pytest

from tools.far_subagent_orchestrator import (
    AgentRole,
    AgentStatus,
    ClaimFinding,
    ConflictResolution,
    DependencyView,
    Disposition,
    EvidenceClass,
    Recommendation,
    SubagentCoordinator,
    SubagentReport,
    SubagentTask,
    default_far_subagent_plan,
)


def _report(
    task,
    sandbox_id,
    context_digest,
    *,
    findings=(),
    recommendation=Recommendation.NONE,
    resolutions=(),
):
    return SubagentReport(
        task_id=task.task_id,
        role=task.role,
        status=AgentStatus.COMPLETED,
        summary=f"{task.task_id} complete",
        sandbox_id=sandbox_id,
        context_digest=context_digest,
        findings=tuple(findings),
        recommendation=recommendation,
        resolutions=tuple(resolutions),
    )


def _claim(
    disposition=Disposition.UNCERTAIN,
    *,
    evidence_class=EvidenceClass.A,
):
    provenance = (
        ("source:1",)
        if evidence_class in {EvidenceClass.P, EvidenceClass.C}
        else ()
    )
    return ClaimFinding(
        claim_id="C1",
        claim="Atomic target claim",
        evidence_class=evidence_class,
        disposition=disposition,
        rationale="bounded rationale",
        provenance=provenance,
    )


def test_default_plan_runs_in_dependency_waves_and_keeps_clean_room_blind():
    seen = {}
    order = []

    def runner(*, task, context, sandbox_id, context_digest):
        seen[task.task_id] = context
        order.append(task.task_id)
        if task.role is AgentRole.CLAIM_REGISTRY:
            findings = (_claim(),)
        elif task.role is AgentRole.EVIDENCE:
            findings = (
                _claim(Disposition.SUPPORTS, evidence_class=EvidenceClass.P),
            )
        else:
            findings = (_claim(),)
        return _report(task, sandbox_id, context_digest, findings=findings)

    context = {
        "research_question": "Does C1 survive?",
        "frozen_inputs": {"packet": "sha256:abc"},
    }
    tasks = default_far_subagent_plan(objective="Evaluate C1")
    result = SubagentCoordinator(tasks, runner, base_context=context).run(
        parallel=False
    )

    assert result.promotion_allowed is True
    assert order[0] == "claim-registry"
    assert order[-1] == "quality-gate"

    clean = seen["clean-room"]
    assert set(clean) == {
        "research_question",
        "frozen_inputs",
        "_dependencies",
    }
    projected = clean["_dependencies"]["claim-registry"]
    assert projected == {
        "task_id": "claim-registry",
        "claims": [{"claim_id": "C1", "claim": "Atomic target claim"}],
    }
    assert "disposition" not in repr(projected)
    assert "recommendation" not in repr(projected)

    sandbox_ids = [report.sandbox_id for report in result.reports]
    assert len(sandbox_ids) == len(set(sandbox_ids))


def test_clean_room_rejects_conclusion_bearing_context_and_full_dependency_view():
    with pytest.raises(ValueError, match="forbidden context"):
        SubagentTask(
            task_id="audit",
            role=AgentRole.CLEAN_ROOM,
            objective="blind audit",
            context_keys=("prior_far_verdict",),
            clean_room=True,
            dependency_view=DependencyView.CLAIMS_ONLY,
        )

    with pytest.raises(ValueError, match="claims-only"):
        SubagentTask(
            task_id="audit",
            role=AgentRole.CLEAN_ROOM,
            objective="blind audit",
            clean_room=True,
            dependency_view=DependencyView.FULL,
        )


def test_specialist_tasks_cannot_request_repository_mutation():
    with pytest.raises(ValueError, match="read-only"):
        SubagentTask(
            task_id="writer",
            role=AgentRole.EVIDENCE,
            objective="write repo",
            read_only=False,
        )


def test_unresolved_cross_agent_conflict_fails_closed():
    tasks = (
        SubagentTask("evidence", AgentRole.EVIDENCE, "support"),
        SubagentTask("counter", AgentRole.COUNTEREXAMPLE, "attack"),
        SubagentTask(
            "quality",
            AgentRole.QUALITY_GATE,
            "gate",
            dependencies=("evidence", "counter"),
        ),
    )

    def runner(*, task, context, sandbox_id, context_digest):
        if task.task_id == "evidence":
            findings = (
                _claim(Disposition.SUPPORTS, evidence_class=EvidenceClass.P),
            )
        elif task.task_id == "counter":
            findings = (
                _claim(Disposition.CONTRADICTS, evidence_class=EvidenceClass.C),
            )
        else:
            findings = ()
        return _report(task, sandbox_id, context_digest, findings=findings)

    result = SubagentCoordinator(tasks, runner).run(parallel=True)

    assert result.promotion_allowed is False
    assert len(result.conflicts) == 1
    assert result.conflicts[0].resolved is False
    assert "C1: unresolved cross-agent conflict" in result.gate_issues


def test_decisive_explicit_resolution_clears_conflict():
    tasks = (
        SubagentTask("evidence", AgentRole.EVIDENCE, "support"),
        SubagentTask("counter", AgentRole.COUNTEREXAMPLE, "attack"),
        SubagentTask(
            "contradiction",
            AgentRole.CONTRADICTION,
            "adjudicate",
            dependencies=("evidence", "counter"),
        ),
        SubagentTask(
            "quality",
            AgentRole.QUALITY_GATE,
            "gate",
            dependencies=("contradiction",),
        ),
    )

    def runner(*, task, context, sandbox_id, context_digest):
        findings = ()
        resolutions = ()
        if task.task_id == "evidence":
            findings = (
                _claim(Disposition.SUPPORTS, evidence_class=EvidenceClass.P),
            )
        elif task.task_id == "counter":
            findings = (
                _claim(Disposition.CONTRADICTS, evidence_class=EvidenceClass.C),
            )
        elif task.task_id == "contradiction":
            resolutions = (
                ConflictResolution(
                    claim_id="C1",
                    disposition=Disposition.SUPPORTS,
                    rationale="primary source controls within this scope",
                    provenance=("source:1",),
                ),
            )
        return _report(
            task,
            sandbox_id,
            context_digest,
            findings=findings,
            resolutions=resolutions,
        )

    result = SubagentCoordinator(tasks, runner).run()

    assert result.promotion_allowed is True
    assert result.conflicts[0].resolved is True
    assert result.conflicts[0].resolver_task_id == "contradiction"


def test_uncertain_resolution_preserves_conflict_and_blocks_promotion():
    tasks = (
        SubagentTask("evidence", AgentRole.EVIDENCE, "support"),
        SubagentTask("counter", AgentRole.COUNTEREXAMPLE, "attack"),
        SubagentTask(
            "contradiction",
            AgentRole.CONTRADICTION,
            "adjudicate",
            dependencies=("evidence", "counter"),
        ),
        SubagentTask(
            "quality",
            AgentRole.QUALITY_GATE,
            "gate",
            dependencies=("contradiction",),
        ),
    )

    def runner(*, task, context, sandbox_id, context_digest):
        findings = ()
        resolutions = ()
        if task.task_id == "evidence":
            findings = (
                _claim(Disposition.SUPPORTS, evidence_class=EvidenceClass.P),
            )
        elif task.task_id == "counter":
            findings = (
                _claim(Disposition.CONTRADICTS, evidence_class=EvidenceClass.C),
            )
        elif task.task_id == "contradiction":
            resolutions = (
                ConflictResolution(
                    claim_id="C1",
                    disposition=Disposition.UNCERTAIN,
                    rationale="evidence does not resolve the collision",
                ),
            )
        return _report(
            task,
            sandbox_id,
            context_digest,
            findings=findings,
            resolutions=resolutions,
        )

    result = SubagentCoordinator(tasks, runner).run()

    assert result.promotion_allowed is False
    assert result.conflicts[0].resolved is False


def test_i_only_acceptance_is_rejected_by_gate():
    tasks = (
        SubagentTask("analysis", AgentRole.FORMALIZER, "analyze"),
        SubagentTask(
            "quality",
            AgentRole.QUALITY_GATE,
            "gate",
            dependencies=("analysis",),
        ),
    )

    def runner(*, task, context, sandbox_id, context_digest):
        if task.task_id == "analysis":
            findings = (
                _claim(Disposition.SUPPORTS, evidence_class=EvidenceClass.I),
            )
            recommendation = Recommendation.ACCEPT
        else:
            findings = ()
            recommendation = Recommendation.NONE
        return _report(
            task,
            sandbox_id,
            context_digest,
            findings=findings,
            recommendation=recommendation,
        )

    result = SubagentCoordinator(tasks, runner).run()

    assert result.promotion_allowed is False
    assert (
        "analysis: acceptance lacks non-I supporting evidence"
        in result.gate_issues
    )


def test_runner_failure_blocks_dependents_and_quality_gate():
    tasks = (
        SubagentTask("evidence", AgentRole.EVIDENCE, "research"),
        SubagentTask(
            "quality",
            AgentRole.QUALITY_GATE,
            "gate",
            dependencies=("evidence",),
        ),
    )

    def runner(*, task, context, sandbox_id, context_digest):
        if task.task_id == "evidence":
            raise RuntimeError("provider unavailable")
        return _report(task, sandbox_id, context_digest)

    result = SubagentCoordinator(tasks, runner).run(parallel=False)

    assert result.report("evidence").status is AgentStatus.FAILED
    assert result.report("quality").status is AgentStatus.BLOCKED
    assert result.promotion_allowed is False
    assert "evidence: failed" in result.gate_issues
    assert "quality: blocked" in result.gate_issues
    assert "quality-gate: did not complete" in result.gate_issues


def test_wrong_execution_binding_is_rejected():
    task = SubagentTask("evidence", AgentRole.EVIDENCE, "research")

    def runner(*, task, context, sandbox_id, context_digest):
        return SubagentReport(
            task_id=task.task_id,
            role=task.role,
            status=AgentStatus.COMPLETED,
            summary="bad binding",
            sandbox_id="wrong",
            context_digest=context_digest,
        )

    result = SubagentCoordinator(
        (task,),
        runner,
        require_quality_gate=False,
    ).run(parallel=False)

    assert result.report("evidence").status is AgentStatus.FAILED
    assert "sandbox_id mismatch" in result.report("evidence").errors[0]
    assert result.promotion_allowed is False


def test_cycle_and_missing_context_are_rejected_before_execution():
    with pytest.raises(ValueError, match="cycle detected"):
        SubagentCoordinator(
            (
                SubagentTask(
                    "a",
                    AgentRole.DISCOVERY,
                    "a",
                    dependencies=("b",),
                ),
                SubagentTask(
                    "b",
                    AgentRole.EVIDENCE,
                    "b",
                    dependencies=("a",),
                ),
            ),
            lambda **kwargs: None,
            require_quality_gate=False,
        )

    with pytest.raises(ValueError, match="missing base context"):
        SubagentCoordinator(
            (
                SubagentTask(
                    "a",
                    AgentRole.DISCOVERY,
                    "a",
                    context_keys=("missing",),
                ),
            ),
            lambda **kwargs: None,
            base_context={},
            require_quality_gate=False,
        )


def test_parallel_and_sequential_runs_are_structurally_deterministic():
    tasks = (
        SubagentTask("a", AgentRole.DISCOVERY, "a"),
        SubagentTask("b", AgentRole.EVIDENCE, "b"),
        SubagentTask(
            "quality",
            AgentRole.QUALITY_GATE,
            "gate",
            dependencies=("a", "b"),
        ),
    )

    def runner(*, task, context, sandbox_id, context_digest):
        return _report(task, sandbox_id, context_digest)

    sequential = SubagentCoordinator(tasks, runner, run_root="same").run(
        parallel=False
    )
    parallel = SubagentCoordinator(tasks, runner, run_root="same").run(
        parallel=True
    )

    assert [r.task_id for r in sequential.reports] == [
        r.task_id for r in parallel.reports
    ]
    assert [r.sandbox_id for r in sequential.reports] == [
        r.sandbox_id for r in parallel.reports
    ]
    assert [r.context_digest for r in sequential.reports] == [
        r.context_digest for r in parallel.reports
    ]
    assert sequential.gate_issues == parallel.gate_issues == ()
