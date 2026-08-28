from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools import adversarial_research_harness as harness
from tools import branch_pr_triage as triage
from tools import exact_contract_playground as playground
from tools import far_research_registry as registry
from tools import research_campaign as campaign

ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def test_all_schemas_semantics_graph_and_generated_views_validate(self):
        data = {path: registry.load(path) for path in registry.DATA_SCHEMAS}
        self.assertEqual(registry.validate_schemas(data), [])
        self.assertEqual(registry.semantic_errors(data), [])
        graph = registry.build_graph(data)
        self.assertEqual(registry.graph_errors(graph), [])
        expected = registry.expected_outputs(data)
        for path, content in expected.items():
            self.assertEqual((ROOT / path).read_text(encoding="utf-8"), content)

    def test_w1_seal_requires_all_promoted_paths_and_exact_hashes(self):
        promotion = registry.load("theory/evaluation/pca-w1-independent-review-promotion-v1.0.json")
        self.assertEqual(registry.w1_seal_errors(promotion), [])
        missing = copy.deepcopy(promotion)
        missing["verified_artifacts"].pop()
        self.assertTrue(any("coverage drift" in error for error in registry.w1_seal_errors(missing)))
        tampered = copy.deepcopy(promotion)
        tampered["verified_artifacts"][0]["sha256"] = "0" * 64
        self.assertTrue(any("missing or changed" in error for error in registry.w1_seal_errors(tampered)))

    def test_duplicate_registry_identity_is_rejected(self):
        data = {path: registry.load(path) for path in registry.DATA_SCHEMAS}
        duplicate = copy.deepcopy(data)
        opportunities = duplicate["research/registry/opportunities-v1.0.json"]["opportunities"]
        opportunities.append(copy.deepcopy(opportunities[0]))
        self.assertTrue(any("duplicate opportunity" in error for error in registry.semantic_errors(duplicate)))


class CampaignFirewallTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.capsule = campaign.load_capsule()

    def test_capsule_hashes_and_stages_validate(self):
        self.assertEqual(campaign.validate_capsule(self.capsule), [])

    def test_capsule_protocol_hash_is_enforced(self):
        tampered = copy.deepcopy(self.capsule)
        tampered["protocol"]["sha256"] = "0" * 64
        self.assertTrue(any("protocol hash mismatch" in error for error in campaign.validate_capsule(tampered)))

    def test_pre_unblinding_denylist_blocks_correction_audit(self):
        with self.assertRaises(campaign.CampaignError):
            campaign.validate_stage_paths(
                self.capsule,
                "A",
                ["docs/audits/project-far-core-theory-v1.1-correction-audit.md"],
            )

    def test_path_traversal_and_outside_allowlist_fail_closed(self):
        for path in ("../AGENTS.md", "/etc/passwd", "README.md"):
            with self.subTest(path=path), self.assertRaises(campaign.CampaignError):
                campaign.validate_stage_paths(self.capsule, "A", [path])

    def test_allowed_evidence_is_read_only_after_full_path_validation(self):
        result = campaign.build_prompt_evidence(
            ROOT,
            self.capsule,
            "A",
            ["theory/theorems/Project-FAR-Theory-Closure-v1.1.md"],
        )
        self.assertEqual(list(result), ["theory/theorems/Project-FAR-Theory-Closure-v1.1.md"])


class AdversarialHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.capsule = campaign.load_capsule()

    @staticmethod
    def lane(provider_id, reasoner, *, isolated=True, sandbox=None):
        return harness.ReasonerLane(
            provider_id=provider_id,
            model_identity=f"test-model:{provider_id}",
            sandbox_id=sandbox or f"sandbox:{provider_id}",
            reasoner=reasoner,
            isolation_verified=isolated,
            prior_exposure="test fixture",
        )

    def test_blind_pass_retains_success_failure_and_stable_issue(self):
        def good(prompt: str, invocation_id: str) -> str:
            self.assertIn("blind-first-pass", prompt)
            return "ISSUE: explicit falsifier needed"

        def failing(_prompt: str, _invocation_id: str) -> str:
            raise RuntimeError("provider unavailable")

        frozen = harness.run_blind_first_pass(
            campaign_id="TEST-CAMPAIGN",
            problem="Try to refute the exact claim.",
            root=ROOT,
            capsule=self.capsule,
            stage_id="A",
            evidence_paths=["theory/theorems/Project-FAR-Theory-Closure-v1.1.md"],
            reasoners={
                "provider-b": self.lane("provider-b", failing),
                "provider-a": self.lane("provider-a", good),
            },
        )
        self.assertEqual([item.status for item in frozen.invocations], ["completed", "failed"])
        self.assertEqual(len(frozen.issues), 1)
        self.assertTrue(frozen.freeze_sha256)

    def test_replay_rejects_changed_prompt_and_adjudication_rejects_unknown_issue(self):
        frozen = harness.run_blind_first_pass(
            campaign_id="TEST-REPLAY",
            problem="frozen problem",
            root=ROOT,
            capsule=self.capsule,
            stage_id="A",
            evidence_paths=["theory/theorems/Project-FAR-Theory-Closure-v1.1.md"],
            reasoners={"provider-a": self.lane("provider-a", lambda _prompt, _id: "ISSUE: one")},
        )
        record = frozen.invocations[0]
        with self.assertRaisesRegex(ValueError, "prompt hash mismatch"):
            harness.replay_selected(
                campaign_id="TEST-REPLAY",
                records=frozen.invocations,
                selected_invocation_ids=[record.invocation_id],
                reasoners={"provider-a": self.lane("provider-a", lambda _prompt, _id: "same")},
                prompts_by_invocation={record.invocation_id: "changed"},
            )
        with self.assertRaisesRegex(ValueError, "unknown issues"):
            harness.adjudication_record(
                campaign_id="TEST-REPLAY",
                frozen=frozen,
                dispositions={"ISSUE-NOT-PRESENT": "rejected"},
                adjudicator="test",
            )

    def test_outbound_redaction_and_isolation_fail_before_provider_call(self):
        captured = []

        def capture(prompt: str, _invocation_id: str) -> str:
            captured.append(prompt)
            return "ISSUE: redaction checked"

        frozen = harness.run_blind_first_pass(
            campaign_id="TEST-REDACTION",
            problem="token=github_pat_abcdefghijklmnopqrstuvwxyz0123456789",
            root=ROOT,
            capsule=self.capsule,
            stage_id="A",
            evidence_paths=["theory/theorems/Project-FAR-Theory-Closure-v1.1.md"],
            reasoners={"provider-a": self.lane("provider-a", capture)},
        )
        self.assertEqual(frozen.invocations[0].status, "completed")
        self.assertIn("[REDACTED]", captured[0])
        self.assertNotIn("github_pat_", captured[0])

        called = False

        def must_not_run(_prompt: str, _invocation_id: str) -> str:
            nonlocal called
            called = True
            return "unexpected"

        with self.assertRaisesRegex(ValueError, "isolation was not verified"):
            harness.run_blind_first_pass(
                campaign_id="TEST-ISOLATION",
                problem="frozen",
                root=ROOT,
                capsule=self.capsule,
                stage_id="A",
                evidence_paths=["theory/theorems/Project-FAR-Theory-Closure-v1.1.md"],
                reasoners={"provider-a": self.lane("provider-a", must_not_run, isolated=False)},
            )
        self.assertFalse(called)

    def test_cross_challenge_redacts_frozen_issues_and_adjudication_is_total(self):
        leaked = "github_pat_abcdefghijklmnopqrstuvwxyz0123456789"
        frozen = harness.run_blind_first_pass(
            campaign_id="TEST-CROSS-REDACTION",
            problem="frozen",
            root=ROOT,
            capsule=self.capsule,
            stage_id="A",
            evidence_paths=["theory/theorems/Project-FAR-Theory-Closure-v1.1.md"],
            reasoners={"provider-a": self.lane(
                "provider-a",
                lambda _prompt, _id: f"ISSUE: token={leaked}\nISSUE: second unresolved issue",
            )},
        )
        captured = []

        def challenge(prompt: str, _invocation_id: str) -> str:
            captured.append(prompt)
            return "no additional issue"

        challenged = harness.run_controlled_cross_challenge(
            campaign_id="TEST-CROSS-REDACTION",
            frozen=frozen,
            challengers={"provider-b": self.lane("provider-b", challenge)},
        )
        self.assertEqual(challenged.invocations[0].status, "completed")
        self.assertIn("[REDACTED]", captured[0])
        self.assertNotIn("github_pat_", captured[0])
        with self.assertRaisesRegex(ValueError, "omits frozen issues"):
            harness.adjudication_record(
                campaign_id="TEST-CROSS-REDACTION",
                frozen=frozen,
                dispositions={frozen.issues[0].issue_id: "accepted"},
                adjudicator="test",
            )

    def test_recorded_replay_preserves_exact_failure(self):
        def failing(_prompt: str, _invocation_id: str) -> str:
            raise RuntimeError("rate limited")

        frozen = harness.run_blind_first_pass(
            campaign_id="TEST-FAILURE-REPLAY",
            problem="frozen",
            root=ROOT,
            capsule=self.capsule,
            stage_id="A",
            evidence_paths=["theory/theorems/Project-FAR-Theory-Closure-v1.1.md"],
            reasoners={"provider-a": self.lane("provider-a", failing)},
        )
        record = frozen.invocations[0]
        # The recorded request is reconstructed from the invocation solely for this fixture.
        evidence = campaign.build_prompt_evidence(
            ROOT, self.capsule, "A", ["theory/theorems/Project-FAR-Theory-Closure-v1.1.md"]
        )
        outbound = {path: harness.redact_outbound(value) for path, value in evidence.items()}
        prompt = campaign.canonical_json({
            "phase": "blind-first-pass", "problem": "frozen", "evidence": outbound,
            "rules": ["extract falsifiable issues", "do not infer proof from agreement"],
        })
        replayed = harness.replay_recorded(
            records=frozen.invocations,
            selected_invocation_ids=[record.invocation_id],
            prompts_by_invocation={record.invocation_id: prompt},
        )
        self.assertEqual(replayed[0].status, "failed")
        self.assertEqual(replayed[0].error, record.error)
        self.assertEqual(replayed[0].replay_of, record.invocation_id)


class PlaygroundAndTriageTests(unittest.TestCase):
    def test_playground_constructs_decoder_or_collision(self):
        sufficient = playground.analyze(json.loads(
            (ROOT / "examples/exact-contract-playground/sufficient.json").read_text(encoding="utf-8")
        ))
        insufficient = playground.analyze(json.loads(
            (ROOT / "examples/exact-contract-playground/insufficient.json").read_text(encoding="utf-8")
        ))
        self.assertTrue(sufficient["sufficient"])
        self.assertIsNotNone(sufficient["decoder"])
        self.assertFalse(insufficient["sufficient"])
        self.assertIsNotNone(insufficient["collision_witness"])

    def test_playground_rejects_incomplete_behavior(self):
        with self.assertRaises(playground.PlaygroundError):
            playground.analyze({"schema_version": "far-exact-playground/1.0", "cases": ["x"], "tests": ["t"], "behavior": {}, "representation": {"x": 0}})

    def test_triage_never_authorizes_deletion_and_preserves_unique_evidence(self):
        snapshot = {
            "schema_version": "far-branch-pr-snapshot/1.0",
            "repository": "test/repo",
            "base_commit": "abc",
            "inventory_summary": {
                "observed_branch_count": 2,
                "fully_classified_count": 1,
                "unclassified_retained_count": 1,
            },
            "branches": [{
                "name": "old-research", "head": "def", "unique_commit_count": 2,
                "unique_paths": ["evidence.json"], "frozen_evidence": False,
                "open_pr": False, "merged_pr": False, "closed_pr": True,
                "superseded_by": "successor-pr",
            }],
        }
        report = triage.classify_snapshot(snapshot)
        self.assertEqual(report["branches"][0]["category"], "unique unmerged evidence")
        self.assertFalse(report["branches"][0]["deletion_authorized"])
        self.assertFalse(report["destructive_actions_performed"])
        self.assertEqual(report["inventory_summary"]["unclassified_retained_count"], 1)


if __name__ == "__main__":
    unittest.main()
