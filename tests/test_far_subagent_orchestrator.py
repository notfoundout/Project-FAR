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
        findings=findings,
        recommendation=recommendation,
        resolutions=resolutions,
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


def _recommendation(task):
    return (
        Recommendation.ACCEPT
        if task.role is AgentRole.QUALITY_GATE
        else Recommendation.NONE
    )


def test_default_plan_runs_in_dependency_waves_and_keeps_clean_room_blind():
    seen = {}
    order = []

    def runner(*, task, context, sandbox_id, context_digest):
        seen[task.task_id] = context
        order.append(task.task_id)
        findings = (
            (_claim(Disposition.SUPPORTS, evidence_class=EvidenceClass.P),)
            if task.role is AgentRole.EVIDENCE
            else (_claim(),)
        )
        return _report(
            task,
            sandbox_id,
            context_digest,
            findings=findings,
            recommendation=_recommendation(task),
        )

    result = SubagentCoordinator(
        default_far_subagent_plan(objective="Evaluate C1"),
        runner,
        base_context={
            "research_question": "Does C1 survive?",
            "frozen_inputs": {"packet": "sha256:abc"},
        },
    ).run(parallel=False)

    assert result.promotion_allowed is True
    assert order[0] == "claim-registry"
    assert order[-1] == "quality-gate"
    clean = seen["clean-room"]
    assert set(clean) == {"research_question", "frozen_inputs", "_dependencies"}
    assert clean["_dependencies"]["claim-registry"] == {
        "task_id": "claim-registry",
        "claims": [{"claim_id": "C1", "claim": "Atomic target claim"}],
    }
    assert "disposition" not in repr(clean["_dependencies"]["claim-registry"])
    assert "recommendation" not in repr(clean["_dependencies"]["claim-registry"])
    sandboxes = [report.sandbox_id for report in result.reports]
    assert len(sandboxes) == len(set(sandboxes))


def test_clean_room_rejects_conclusion_bearing_context():
    with pytest.raises(ValueError, match="forbidden context"):
        SubagentTask(
            "audit",
            AgentRole.CLEAN_ROOM,
            "blind audit",
            context_keys=("prior_far_verdict",),
            clean_room=True,
            dependency_view=DependencyView.CLAIMS_ONLY,
        )


def test_clean_room_requires_claims_only_dependency_view():
    with pytest.raises(ValueError, match="claims-only"):
        SubagentTask(
            "audit",
            AgentRole.CLEAN_ROOM,
            "blind audit",
            clean_room=True,
            dependency_view=DependencyView.FULL,
        )


def test_specialist_tasks_are_read_only():
    with pytest.raises(ValueError, match="read-only"):
        SubagentTask(
            "writer",
            AgentRole.EVIDENCE,
            "write repo",
            read_only=False,
        )


def _conflict_tasks():
    return (
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


def _conflict_runner(resolution):
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
        elif task.task_id == "contradiction" and resolution is not None:
            resolutions = (resolution,)
        return _report(
            task,
            sandbox_id,
            context_digest,
            findings=findings,
            recommendation=_recommendation(task),
            resolutions=resolutions,
        )

    return runner


def test_unresolved_cross_agent_conflict_fails_closed():
    result = SubagentCoordinator(
        _conflict_tasks(),
        _conflict_runner(None),
    ).run()
    assert result.promotion_allowed is False
    assert result.conflicts[0].resolved is False
    assert "C1: unresolved cross-agent conflict" in result.gate_issues


def test_decisive_explicit_resolution_clears_conflict():
    result = SubagentCoordinator(
        _conflict_tasks(),
        _conflict_runner(
            ConflictResolution(
                "C1",
                Disposition.SUPPORTS,
                "primary source controls within this scope",
                ("source:1",),
            )
        ),
    ).run()
    assert result.promotion_allowed is True
    assert result.conflicts[0].resolved is True
    assert result.conflicts[0].resolver_task_id == "contradiction"


def test_uncertain_resolution_preserves_conflict():
    result = SubagentCoordinator(
        _conflict_tasks(),
        _conflict_runner(
            ConflictResolution(
                "C1",
                Disposition.UNCERTAIN,
                "evidence does not resolve the collision",
            )
        ),
    ).run()
    assert result.promotion_allowed is False
    assert result.conflicts[0].resolved is False


def test_i_only_acceptance_is_rejected():
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
        findings = (
            (_claim(Disposition.SUPPORTS, evidence_class=EvidenceClass.I),)
            if task.task_id == "analysis"
            else ()
        )
        return _report(
            task,
            sandbox_id,
            context_digest,
            findings=findings,
            recommendation=_recommendation(task),
        )

    result = SubagentCoordinator(tasks, runner).run()
    assert result.promotion_allowed is False
    assert "quality-gate: acceptance lacks non-I supporting evidence" in result.gate_issues


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
    assert "quality-gate: did not complete" in result.gate_issues


def test_wrong_execution_binding_is_rejected():
    task = SubagentTask("evidence", AgentRole.EVIDENCE, "research")

    def runner(*, task, context, sandbox_id, context_digest):
        return SubagentReport(
            task.task_id,
            task.role,
            AgentStatus.COMPLETED,
            "bad binding",
            "wrong",
            context_digest,
        )

    result = SubagentCoordinator(
        (task,),
        runner,
        require_quality_gate=False,
    ).run(parallel=False)
    assert result.report("evidence").status is AgentStatus.FAILED
    assert "sandbox_id mismatch" in result.report("evidence").errors[0]


def test_cycle_and_missing_context_are_rejected_before_execution():
    with pytest.raises(ValueError, match="cycle detected"):
        SubagentCoordinator(
            (
                SubagentTask("a", AgentRole.DISCOVERY, "a", dependencies=("b",)),
                SubagentTask("b", AgentRole.EVIDENCE, "b", dependencies=("a",)),
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

    sequential = SubagentCoordinator(tasks, runner, run_root="same").run(parallel=False)
    parallel = SubagentCoordinator(tasks, runner, run_root="same").run(parallel=True)
    assert [r.task_id for r in sequential.reports] == [r.task_id for r in parallel.reports]
    assert [r.sandbox_id for r in sequential.reports] == [r.sandbox_id for r in parallel.reports]
    assert [r.context_digest for r in sequential.reports] == [r.context_digest for r in parallel.reports]
    assert sequential.gate_issues == parallel.gate_issues == ()
    assert sequential.promotion_allowed is parallel.promotion_allowed is False


def test_quality_gate_must_affirmatively_accept_before_promotion():
    task = SubagentTask("quality", AgentRole.QUALITY_GATE, "gate")
    result = SubagentCoordinator(
        (task,),
        lambda *, task, context, sandbox_id, context_digest: _report(
            task, sandbox_id, context_digest
        ),
    ).run(parallel=False)
    assert result.gate_issues == ()
    assert result.promotion_allowed is False


def test_non_contradiction_task_cannot_emit_resolution():
    task = SubagentTask("evidence", AgentRole.EVIDENCE, "research")

    def runner(*, task, context, sandbox_id, context_digest):
        return _report(
            task,
            sandbox_id,
            context_digest,
            resolutions=(
                ConflictResolution(
                    "C1",
                    Disposition.SUPPORTS,
                    "attempted self-adjudication",
                    ("source:1",),
                ),
            ),
        )

    result = SubagentCoordinator(
        (task,),
        runner,
        require_quality_gate=False,
    ).run(parallel=False)
    assert result.report("evidence").status is AgentStatus.FAILED
    assert "only contradiction tasks may emit conflict resolutions" in (
        result.report("evidence").errors[0]
    )


def test_decisive_resolution_requires_provenance():
    with pytest.raises(ValueError, match="decisive conflict resolutions require provenance"):
        ConflictResolution(
            "C1",
            Disposition.SUPPORTS,
            "unsupported adjudication",
        )


def test_primary_and_computational_findings_require_nonempty_provenance():
    with pytest.raises(ValueError, match="P/C findings require non-empty provenance"):
        ClaimFinding(
            "C1",
            "Atomic target claim",
            EvidenceClass.P,
            Disposition.SUPPORTS,
            "missing source",
            ("",),
        )
