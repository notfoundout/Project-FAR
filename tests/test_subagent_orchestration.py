from __future__ import annotations

import dataclasses
import json
import unittest

from tools import subagent_orchestration as sub


def cap(agent_id: str, **overrides) -> sub.RuntimeCapabilities:
    values = {
        "sandbox_id": f"sandbox:{agent_id}",
        "isolation_verified": True,
        "repository_tools_enabled": False,
        "shared_state_with": (),
    }
    values.update(overrides)
    return sub.RuntimeCapabilities(**values)


def completed(task: sub.AgentTask, *findings: sub.Finding) -> sub.AgentReport:
    return sub.AgentReport(
        agent_id=task.agent_id,
        task_id=task.task_id,
        input_sha256=task.input_sha256,
        status=sub.ReportStatus.COMPLETED,
        findings=tuple(findings),
    )


class PlanTests(unittest.TestCase):
    def test_default_plan_is_deterministic_and_coordinator_is_terminal(self):
        left = sub.far_research_plan()
        right = sub.far_research_plan()
        self.assertEqual(left.sha256, right.sha256)
        order = sub.topological_order(left)
        self.assertEqual(order[-1], "coordinator")
        self.assertEqual(set(left.by_id["coordinator"].dependencies), set(order[:-1]))

    def test_cycle_and_incomplete_coordinator_dependency_fail_closed(self):
        specialist = sub.AgentSpec(
            agent_id="a",
            skill_path=".claude/skills/far-formalizer/SKILL.md",
            role="a",
            dependencies=("b",),
        )
        other = sub.AgentSpec(
            agent_id="b",
            skill_path=".claude/skills/far-formalizer/SKILL.md",
            role="b",
            dependencies=("a",),
        )
        coordinator = sub.AgentSpec(
            agent_id="coordinator",
            skill_path=".claude/skills/far-research-orchestrator/SKILL.md",
            role="coordinate",
            kind=sub.AgentKind.COORDINATOR,
            dependencies=("a", "b"),
        )
        with self.assertRaisesRegex(ValueError, "cycle"):
            sub.OrchestrationPlan(
                plan_id="cycle-plan",
                coordinator_id="coordinator",
                agents=(specialist, other, coordinator),
            )

        coordinator_missing = dataclasses.replace(
            coordinator, dependencies=("a",)
        )
        with self.assertRaisesRegex(ValueError, "every specialist"):
            sub.OrchestrationPlan(
                plan_id="missing-dependency",
                coordinator_id="coordinator",
                agents=(
                    dataclasses.replace(specialist, dependencies=()),
                    dataclasses.replace(other, dependencies=()),
                    coordinator_missing,
                ),
            )

    def test_context_is_content_addressed(self):
        artifact = sub.ContextArtifact.from_text("source-1", "exact bytes")
        self.assertEqual(artifact.sha256, sub.sha256_text("exact bytes"))
        with self.assertRaisesRegex(ValueError, "content hash mismatch"):
            sub.ContextArtifact("source-1", "0" * 64, "exact bytes")


class OrchestrationTests(unittest.TestCase):
    @staticmethod
    def simple_plan(*, sequencing_only=False) -> sub.OrchestrationPlan:
        a = sub.AgentSpec(
            agent_id="a",
            skill_path=".claude/skills/far-discovery-engine/SKILL.md",
            role="a",
        )
        b = sub.AgentSpec(
            agent_id="b",
            skill_path=".claude/skills/far-formalizer/SKILL.md",
            role="b",
            dependencies=("a",),
            receives_dependency_reports=not sequencing_only,
        )
        coordinator = sub.AgentSpec(
            agent_id="coordinator",
            skill_path=".claude/skills/far-research-orchestrator/SKILL.md",
            role="coordinator",
            kind=sub.AgentKind.COORDINATOR,
            dependencies=("a", "b"),
        )
        return sub.OrchestrationPlan(
            plan_id="simple-plan",
            coordinator_id="coordinator",
            agents=(a, b, coordinator),
        )

    def test_explicit_dependency_visibility_and_only_coordinator_integrates(self):
        plan = self.simple_plan()
        seen = {}

        def callback(agent, task):
            seen[agent.agent_id] = tuple(
                report.agent_id for report in task.dependency_reports
            )
            return completed(task)

        runtime = sub.CallableRuntime(
            {name: callback for name in plan.by_id},
            {name: cap(name) for name in plan.by_id},
        )
        result = sub.orchestrate(
            plan=plan,
            objective="test objective",
            context=(sub.ContextArtifact.from_text("input", "frozen"),),
            runtime=runtime,
        )
        self.assertEqual(result.status, sub.RunStatus.COMPLETED)
        self.assertEqual(seen["a"], ())
        self.assertEqual(seen["b"], ("a",))
        self.assertEqual(seen["coordinator"], ("a", "b"))
        self.assertEqual(result.coordinator_report.agent_id, "coordinator")

    def test_sequencing_dependency_can_hide_upstream_report(self):
        plan = self.simple_plan(sequencing_only=True)
        seen_b = []

        def callback(agent, task):
            if agent.agent_id == "b":
                seen_b.extend(task.dependency_reports)
            return completed(task)

        runtime = sub.CallableRuntime(
            {name: callback for name in plan.by_id},
            {name: cap(name) for name in plan.by_id},
        )
        result = sub.orchestrate(
            plan=plan,
            objective="blind-after-sequence",
            context=(),
            runtime=runtime,
        )
        self.assertEqual(result.status, sub.RunStatus.COMPLETED)
        self.assertEqual(seen_b, [])

    def test_support_contradiction_blocks_coordinator_even_under_majority(self):
        agents = []
        for name in ("a", "b", "c", "d"):
            agents.append(
                sub.AgentSpec(
                    agent_id=name,
                    skill_path=".claude/skills/far-theory-auditor/SKILL.md",
                    role=name,
                )
            )
        coordinator = sub.AgentSpec(
            agent_id="coordinator",
            skill_path=".claude/skills/far-research-orchestrator/SKILL.md",
            role="coordinate",
            kind=sub.AgentKind.COORDINATOR,
            dependencies=tuple(item.agent_id for item in agents),
        )
        plan = sub.OrchestrationPlan(
            plan_id="conflict-plan",
            coordinator_id="coordinator",
            agents=tuple(agents) + (coordinator,),
        )
        coordinator_called = False

        def callback(agent, task):
            nonlocal coordinator_called
            if agent.agent_id == "coordinator":
                coordinator_called = True
                return completed(task)
            disposition = (
                sub.FindingDisposition.CONTRADICTS
                if agent.agent_id == "d"
                else sub.FindingDisposition.SUPPORTS
            )
            finding = sub.Finding(
                finding_id=f"F-{agent.agent_id}",
                claim_id="CLAIM-1",
                disposition=disposition,
                statement=f"{agent.agent_id} result",
            )
            return completed(task, finding)

        runtime = sub.CallableRuntime(
            {name: callback for name in plan.by_id},
            {name: cap(name) for name in plan.by_id},
        )
        result = sub.orchestrate(
            plan=plan,
            objective="conflict",
            context=(),
            runtime=runtime,
        )
        self.assertEqual(result.status, sub.RunStatus.BLOCKED)
        self.assertFalse(coordinator_called)
        self.assertEqual(len(result.conflicts), 1)
        self.assertEqual(
            result.conflicts[0].supporting_findings, ("F-a", "F-b", "F-c")
        )
        self.assertEqual(result.conflicts[0].contradicting_findings, ("F-d",))
        self.assertIn("coordinator", result.blocked_agents)

    def test_runtime_failure_is_durable_and_blocks_dependents(self):
        plan = self.simple_plan()
        calls = []

        def callback(agent, task):
            calls.append(agent.agent_id)
            if agent.agent_id == "a":
                raise RuntimeError("provider unavailable")
            return completed(task)

        runtime = sub.CallableRuntime(
            {name: callback for name in plan.by_id},
            {name: cap(name) for name in plan.by_id},
        )
        result = sub.orchestrate(
            plan=plan,
            objective="failure",
            context=(),
            runtime=runtime,
        )
        self.assertEqual(result.status, sub.RunStatus.FAILED)
        self.assertEqual(calls, ["a"])
        self.assertEqual(result.failures[0].agent_id, "a")
        self.assertIn("provider unavailable", result.failures[0].error)
        self.assertEqual(result.blocked_agents, ("b", "coordinator"))
        report = next(item for item in result.reports if item.agent_id == "a")
        self.assertEqual(report.status, sub.ReportStatus.FAILED)

    def test_cross_task_report_substitution_becomes_failure(self):
        plan = self.simple_plan()

        def callback(agent, task):
            if agent.agent_id == "a":
                return sub.AgentReport(
                    agent_id="a",
                    task_id="TASK-wrong",
                    input_sha256=task.input_sha256,
                    status=sub.ReportStatus.COMPLETED,
                )
            return completed(task)

        runtime = sub.CallableRuntime(
            {name: callback for name in plan.by_id},
            {name: cap(name) for name in plan.by_id},
        )
        result = sub.orchestrate(
            plan=plan,
            objective="binding",
            context=(),
            runtime=runtime,
        )
        self.assertEqual(result.status, sub.RunStatus.FAILED)
        self.assertIn("report task mismatch", result.failures[0].error)

    def test_agent_cannot_cite_evidence_it_never_received(self):
        plan = self.simple_plan()

        def callback(agent, task):
            if agent.agent_id == "a":
                finding = sub.Finding(
                    finding_id="F-a",
                    claim_id="CLAIM-1",
                    disposition=sub.FindingDisposition.SUPPORTS,
                    statement="claims hidden support",
                    evidence_refs=("not-visible",),
                )
                return completed(task, finding)
            return completed(task)

        runtime = sub.CallableRuntime(
            {name: callback for name in plan.by_id},
            {name: cap(name) for name in plan.by_id},
        )
        result = sub.orchestrate(
            plan=plan,
            objective="evidence visibility",
            context=(),
            runtime=runtime,
        )
        self.assertEqual(result.status, sub.RunStatus.FAILED)
        self.assertIn("not visible to task", result.failures[0].error)

    def test_cross_agent_duplicate_finding_id_is_rejected(self):
        agents = (
            sub.AgentSpec(
                agent_id="a",
                skill_path=".claude/skills/far-discovery-engine/SKILL.md",
                role="a",
            ),
            sub.AgentSpec(
                agent_id="b",
                skill_path=".claude/skills/far-formalizer/SKILL.md",
                role="b",
            ),
        )
        coordinator = sub.AgentSpec(
            agent_id="coordinator",
            skill_path=".claude/skills/far-research-orchestrator/SKILL.md",
            role="coordinate",
            kind=sub.AgentKind.COORDINATOR,
            dependencies=("a", "b"),
        )
        plan = sub.OrchestrationPlan(
            plan_id="duplicate-finding-plan",
            coordinator_id="coordinator",
            agents=agents + (coordinator,),
        )

        def callback(agent, task):
            if agent.agent_id == "coordinator":
                return completed(task)
            return completed(
                task,
                sub.Finding(
                    finding_id="F-shared",
                    claim_id=f"CLAIM-{agent.agent_id}",
                    disposition=sub.FindingDisposition.UNKNOWN,
                    statement=agent.agent_id,
                ),
            )

        runtime = sub.CallableRuntime(
            {name: callback for name in plan.by_id},
            {name: cap(name) for name in plan.by_id},
        )
        result = sub.orchestrate(
            plan=plan,
            objective="global finding identity",
            context=(),
            runtime=runtime,
        )
        self.assertEqual(result.status, sub.RunStatus.FAILED)
        self.assertEqual(result.failures[0].agent_id, "b")
        self.assertIn("duplicate cross-agent finding_id", result.failures[0].error)

    def test_runtime_capabilities_fail_before_first_invocation(self):
        plan = self.simple_plan()
        called = []

        def callback(agent, task):
            called.append(agent.agent_id)
            return completed(task)

        cases = [
            {
                "a": cap("a", isolation_verified=False),
                "b": cap("b"),
                "coordinator": cap("coordinator"),
            },
            {
                "a": cap("a", sandbox_id="same"),
                "b": cap("b", sandbox_id="same"),
                "coordinator": cap("coordinator"),
            },
            {
                "a": cap("a", shared_state_with=("b",)),
                "b": cap("b"),
                "coordinator": cap("coordinator"),
            },
            {
                "a": cap("a", repository_tools_enabled=True),
                "b": cap("b"),
                "coordinator": cap("coordinator"),
            },
        ]
        for capabilities in cases:
            with self.subTest(capabilities=capabilities), self.assertRaises(ValueError):
                sub.orchestrate(
                    plan=plan,
                    objective="capability check",
                    context=(),
                    runtime=sub.CallableRuntime(
                        {name: callback for name in plan.by_id}, capabilities
                    ),
                )
            self.assertEqual(called, [])

    def test_identical_inputs_produce_identical_run_task_and_result_hashes(self):
        plan = self.simple_plan()

        def callback(agent, task):
            return completed(task)

        def execute():
            runtime = sub.CallableRuntime(
                {name: callback for name in plan.by_id},
                {name: cap(name) for name in plan.by_id},
            )
            return sub.orchestrate(
                plan=plan,
                objective="deterministic",
                context=(sub.ContextArtifact.from_text("x", "y"),),
                runtime=runtime,
            )

        one, two = execute(), execute()
        self.assertEqual(one.run_id, two.run_id)
        self.assertEqual(
            [report.task_id for report in one.reports],
            [report.task_id for report in two.reports],
        )
        self.assertEqual(one.result_sha256, two.result_sha256)


class ReasonerLaneAdapterTests(unittest.TestCase):
    def test_adapter_redacts_secrets_and_strictly_parses_report(self):
        captured = []

        def reasoner(prompt, _invocation_id):
            captured.append(prompt)
            task = json.loads(prompt)["task"]
            return json.dumps(
                {
                    "contract": "far-subagent-report/1.0",
                    "agent_id": "a",
                    "task_id": task["task_id"],
                    "input_sha256": task["input_sha256"],
                    "status": "completed",
                    "findings": [],
                    "limitations": [],
                    "error": None,
                }
            )

        a = sub.AgentSpec(
            agent_id="a",
            skill_path=".claude/skills/far-discovery-engine/SKILL.md",
            role="a",
        )
        coordinator = sub.AgentSpec(
            agent_id="coordinator",
            skill_path=".claude/skills/far-research-orchestrator/SKILL.md",
            role="coordinate",
            kind=sub.AgentKind.COORDINATOR,
            dependencies=("a",),
        )
        plan = sub.OrchestrationPlan(
            plan_id="adapter-plan",
            coordinator_id="coordinator",
            agents=(a, coordinator),
        )

        def coordinator_reasoner(prompt, _invocation_id):
            task = json.loads(prompt)["task"]
            return json.dumps(
                {
                    "contract": "far-subagent-report/1.0",
                    "agent_id": "coordinator",
                    "task_id": task["task_id"],
                    "input_sha256": task["input_sha256"],
                    "status": "completed",
                    "findings": [],
                    "limitations": [],
                    "error": None,
                }
            )

        lanes = {
            "a": sub.ReasonerLane(
                provider_id="a",
                model_identity="model:a",
                sandbox_id="sandbox:a",
                reasoner=reasoner,
                isolation_verified=True,
            ),
            "coordinator": sub.ReasonerLane(
                provider_id="coordinator",
                model_identity="model:c",
                sandbox_id="sandbox:c",
                reasoner=coordinator_reasoner,
                isolation_verified=True,
            ),
        }
        result = sub.orchestrate(
            plan=plan,
            objective="token=github_pat_abcdefghijklmnopqrstuvwxyz0123456789",
            context=(),
            runtime=sub.ReasonerLaneRuntime(lanes),
        )
        self.assertEqual(result.status, sub.RunStatus.COMPLETED)
        self.assertIn("[REDACTED]", captured[0])
        self.assertNotIn("github_pat_", captured[0])

    def test_adapter_rejects_lane_provider_identity_mismatch_before_call(self):
        called = False

        def reasoner(_prompt, _invocation_id):
            nonlocal called
            called = True
            return "{}"

        a = sub.AgentSpec(
            agent_id="a",
            skill_path=".claude/skills/far-discovery-engine/SKILL.md",
            role="a",
        )
        coordinator = sub.AgentSpec(
            agent_id="coordinator",
            skill_path=".claude/skills/far-research-orchestrator/SKILL.md",
            role="coordinate",
            kind=sub.AgentKind.COORDINATOR,
            dependencies=("a",),
        )
        plan = sub.OrchestrationPlan(
            plan_id="provider-mismatch-plan",
            coordinator_id="coordinator",
            agents=(a, coordinator),
        )
        lanes = {
            "a": sub.ReasonerLane(
                provider_id="different",
                model_identity="model:a",
                sandbox_id="sandbox:a",
                reasoner=reasoner,
                isolation_verified=True,
            ),
            "coordinator": sub.ReasonerLane(
                provider_id="coordinator",
                model_identity="model:c",
                sandbox_id="sandbox:c",
                reasoner=reasoner,
                isolation_verified=True,
            ),
        }
        with self.assertRaisesRegex(ValueError, "lane/provider identity mismatch"):
            sub.orchestrate(
                plan=plan,
                objective="identity",
                context=(),
                runtime=sub.ReasonerLaneRuntime(lanes),
            )
        self.assertFalse(called)

    def test_parser_rejects_extra_keys_and_unknown_disposition(self):
        base = {
            "contract": "far-subagent-report/1.0",
            "agent_id": "a",
            "task_id": "TASK-1",
            "input_sha256": "0" * 64,
            "status": "completed",
            "findings": [],
            "limitations": [],
            "error": None,
        }
        extra = dict(base)
        extra["surprise"] = True
        with self.assertRaisesRegex(ValueError, "keys mismatch"):
            sub.parse_agent_report(json.dumps(extra))

        bad = dict(base)
        bad["findings"] = [
            {
                "finding_id": "F-1",
                "claim_id": "C-1",
                "disposition": "probably",
                "statement": "x",
                "evidence_refs": [],
            }
        ]
        with self.assertRaisesRegex(ValueError, "invalid disposition"):
            sub.parse_agent_report(json.dumps(bad))


if __name__ == "__main__":
    unittest.main()
