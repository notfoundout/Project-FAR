"""Blindness, execution/epistemic separation, evidence preservation, continuation.

No test in this file performs a paid API call: every provider is scripted.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from far_adversarial import ledger as L, protocol  # noqa: E402
from far_adversarial.evidence import EvidenceStore, replay_key  # noqa: E402
from far_adversarial.orchestrator import (  # noqa: E402
    EXECUTION_STOP,
    NO_ELIGIBLE_TARGET,
    Orchestrator,
    ROUND_LIMIT,
    TARGET_TERMINAL,
)
from far_adversarial.providers import (  # noqa: E402
    INVALID_PROVIDER_OUTPUT,
    RATE_LIMIT,
    ReplayProvider,
    ScriptedProvider,
)
from far_adversarial.safety import sha256_hex  # noqa: E402

CLAUDE_SIGNATURE = "CLAUDE-LANE-PRIVATE-MARKER-8f21"
GPT_SIGNATURE = "GPT-LANE-PRIVATE-MARKER-3c07"


def first_pass(objections, marker="", sources=(), formals=()):
    return json.dumps(
        {
            "assessment": f"analysis {marker}",
            "objections": [
                {"claim": claim, "kind": "other", "rationale": "because"}
                for claim in objections
            ],
            "source_requests": list(sources),
            "formal_obligations": list(formals),
        }
    )


def audit(responses):
    return json.dumps({"responses": responses})


def act(issue_id, action, revised=None):
    return {"issue_id": issue_id, "action": action, "rationale": "r",
            "revised_claim": revised}


def make_target(**overrides):
    base = dict(
        id="T-1",
        original_formulation="original",
        current_formulation="current formulation",
        frozen_scope="scope",
        provenance="test",
        authorized=True,
    )
    base.update(overrides)
    return L.Target(**base)


class Harness:
    def __init__(self, tmp, claude_responses, gpt_responses, targets=None, max_rounds=4):
        self.ledger = L.Ledger(Path(tmp) / "state.json")
        for target in targets or [make_target()]:
            self.ledger.add_target(target)
        self.store = EvidenceStore(Path(tmp) / "evidence")
        self.claude = ScriptedProvider(claude_responses, name="claude", model="claude-test")
        self.gpt = ScriptedProvider(gpt_responses, name="gpt", model="gpt-test")
        self.orchestrator = Orchestrator(
            ledger=self.ledger, store=self.store, claude=self.claude, gpt=self.gpt,
            evidence_loader=lambda t: {"frozen.md": "frozen evidence body"},
            source_freeze="git:cafebabe:d00d", max_rounds_per_target=max_rounds,
            parallel=False,
        )


class BlindnessTests(unittest.TestCase):
    def test_neither_first_pass_prompt_contains_the_other_lanes_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[first_pass(["Claude objection."], CLAUDE_SIGNATURE)],
                gpt_responses=[first_pass(["GPT objection."], GPT_SIGNATURE)],
            )
            harness.orchestrator.blind_first_passes(harness.ledger.targets["T-1"])
            claude_prompt = harness.orchestrator.lane_prompts["claude"][0]
            gpt_prompt = harness.orchestrator.lane_prompts["gpt"][0]
            self.assertNotIn(GPT_SIGNATURE, claude_prompt)
            self.assertNotIn(CLAUDE_SIGNATURE, gpt_prompt)
            self.assertNotIn("GPT objection", claude_prompt)
            self.assertNotIn("Claude objection", gpt_prompt)

    def test_first_pass_prompt_has_no_parameter_for_other_lane_findings(self):
        import inspect

        params = set(inspect.signature(protocol.first_pass_prompt).parameters)
        self.assertEqual(params, {"role", "target", "evidence", "source_freeze"})

    def test_both_lanes_receive_identical_frozen_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(tmp, [first_pass([])], [first_pass([])])
            harness.orchestrator.blind_first_passes(harness.ledger.targets["T-1"])
            claude_prompt = harness.orchestrator.lane_prompts["claude"][0]
            gpt_prompt = harness.orchestrator.lane_prompts["gpt"][0]
            marker = "## Eligible frozen evidence"
            self.assertEqual(claude_prompt.split(marker)[1], gpt_prompt.split(marker)[1])
            self.assertNotEqual(claude_prompt, gpt_prompt)  # roles differ

    def test_lane_prompts_differ_only_in_the_role_preamble(self):
        """Regression for audit finding 8: substantive evidence must be equal."""
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(tmp, [first_pass([])], [first_pass([])])
            harness.orchestrator.blind_first_passes(harness.ledger.targets["T-1"])
            claude_prompt = harness.orchestrator.lane_prompts["claude"][0]
            gpt_prompt = harness.orchestrator.lane_prompts["gpt"][0]
            claude_body = claude_prompt[len(protocol.CLAUDE_ROLE):]
            gpt_body = gpt_prompt[len(protocol.GPT_ROLE):]
            self.assertEqual(claude_body, gpt_body)

    def test_raw_output_is_preserved_before_any_cross_exchange(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(tmp, [first_pass(["Claude objection."])],
                              [first_pass(["GPT objection."])])
            harness.orchestrator.blind_first_passes(harness.ledger.targets["T-1"])
            recorded = harness.store.all_invocations()
            self.assertEqual(len(recorded), 2)
            self.assertEqual({inv.lane for inv in recorded}, {"claude", "gpt"})
            self.assertEqual(harness.ledger.issues, {})  # nothing extracted yet


class CrossAuditTests(unittest.TestCase):
    def test_rebuttal_round_sends_each_lane_only_the_other_lanes_objections(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(tmp,
                              [first_pass(["Claude objection."]), audit([])],
                              [first_pass(["GPT objection."]), audit([])])
            target = harness.ledger.targets["T-1"]
            passes = harness.orchestrator.blind_first_passes(target)
            ids = harness.orchestrator.extract_issues(target, passes)
            harness.orchestrator.rebuttal_round(target, ids)
            claude_audit = harness.orchestrator.lane_prompts["claude"][1]
            gpt_audit = harness.orchestrator.lane_prompts["gpt"][1]
            self.assertIn("GPT objection.", claude_audit)
            self.assertNotIn("Claude objection.", claude_audit)
            self.assertIn("Claude objection.", gpt_audit)
            self.assertNotIn("GPT objection.", gpt_audit)

    def test_challenged_prompt_offers_no_terminating_action(self):
        """Regression for audit finding 3: the contract matches actual standing."""
        self.assertIn("REBUT", protocol.CHALLENGED_CONTRACT)
        self.assertNotIn("WITHDRAW", protocol.CHALLENGED_CONTRACT)
        self.assertIn("WITHDRAW", protocol.OWNER_CONTRACT)

    def test_challenged_schema_excludes_owner_only_actions(self):
        schema = protocol.cross_audit_schema(sorted(L.CHALLENGED_ACTIONS))
        allowed = schema["properties"]["responses"]["items"]["properties"]["action"]["enum"]
        self.assertNotIn("WITHDRAW", allowed)
        self.assertNotIn("SUSTAIN", allowed)
        self.assertIn("REBUT", allowed)

    def test_a_rebuttal_leaves_the_objection_live(self):
        gpt_issue = L.issue_id("T-1", "GPT objection.")
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[first_pass([]), audit([act(gpt_issue, "REBUT")])],
                gpt_responses=[first_pass(["GPT objection."]), audit([])],
                max_rounds=1,
            )
            harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertEqual(harness.ledger.issues[gpt_issue].state, L.ISSUE_REBUTTED)
            self.assertTrue(harness.ledger.issues[gpt_issue].is_live())

    def test_owner_review_can_withdraw_after_a_rebuttal(self):
        gpt_issue = L.issue_id("T-1", "GPT objection.")
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[first_pass([]), audit([act(gpt_issue, "REBUT")])],
                gpt_responses=[first_pass(["GPT objection."]),
                               audit([act(gpt_issue, "WITHDRAW")])],
                max_rounds=1,
            )
            report = harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertEqual(harness.ledger.issues[gpt_issue].state, L.ISSUE_WITHDRAWN)
            self.assertEqual(report.stop_reason, TARGET_TERMINAL)
            self.assertEqual(harness.ledger.targets["T-1"].status,
                             L.READY_UNDER_INTERNAL_PROTOCOL)

    def test_settled_issues_are_not_resent(self):
        gpt_issue = L.issue_id("T-1", "GPT objection.")
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[first_pass([]), audit([act(gpt_issue, "CONCEDE")]),
                                  audit([]), audit([])],
                gpt_responses=[first_pass(["GPT objection."]), audit([]), audit([])],
                max_rounds=1,
            )
            target = harness.ledger.targets["T-1"]
            harness.orchestrator.run_target(target)
            before = len(harness.orchestrator.lane_prompts["claude"])
            harness.orchestrator.rebuttal_round(target, [gpt_issue])
            for prompt in harness.orchestrator.lane_prompts["claude"][before:]:
                self.assertNotIn(gpt_issue, prompt)

    def test_response_naming_an_unregistered_issue_is_rejected(self):
        parsed = protocol.parse_cross_audit(
            audit([act("ISS-DEADBEEF00", "REBUT")]),
            known_issue_ids={"ISS-000000000000"},
            permitted_actions=set(L.CHALLENGED_ACTIONS),
        )
        self.assertIsNone(parsed)

    def test_action_outside_the_actors_standing_is_rejected_at_the_parser(self):
        parsed = protocol.parse_cross_audit(
            audit([act("ISS-1", "WITHDRAW")]),
            known_issue_ids={"ISS-1"},
            permitted_actions=set(L.CHALLENGED_ACTIONS),
        )
        self.assertIsNone(parsed)

    def test_unknown_action_is_rejected(self):
        parsed = protocol.parse_cross_audit(
            audit([act("ISS-1", "APPROVE")]), known_issue_ids={"ISS-1"},
            permitted_actions=set(L.ISSUE_ACTIONS),
        )
        self.assertIsNone(parsed)


class ObligationExtractionTests(unittest.TestCase):
    """Regression for audit finding 4: requests become blocking ledger objects."""

    def test_first_pass_source_requests_block_closure(self):
        gpt_issue = L.issue_id("T-1", "GPT objection.")
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[first_pass([], sources=["the frozen corpus E0"]),
                                  audit([act(gpt_issue, "REBUT")])],
                gpt_responses=[first_pass(["GPT objection."]),
                               audit([act(gpt_issue, "WITHDRAW")])],
                max_rounds=1,
            )
            harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertEqual(harness.ledger.targets["T-1"].status, L.SOURCE_REQUIRED)
            self.assertEqual(len(harness.ledger.blocking_obligations_for("T-1")), 1)

    def test_first_pass_formal_obligations_block_closure(self):
        gpt_issue = L.issue_id("T-1", "GPT objection.")
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[first_pass([], formals=["discharge the lemma"]),
                                  audit([act(gpt_issue, "REBUT")])],
                gpt_responses=[first_pass(["GPT objection."]),
                               audit([act(gpt_issue, "WITHDRAW")])],
                max_rounds=1,
            )
            harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertEqual(harness.ledger.targets["T-1"].status,
                             L.FORMAL_CHECK_REQUIRED)

    def test_source_requests_do_not_pollute_declared_evidence_paths(self):
        # The declared path list is an input contract, not a scratch pad.
        with tempfile.TemporaryDirectory() as tmp:
            target = make_target(frozen_evidence_paths=["docs/a.md"])
            harness = Harness(tmp, [first_pass([], sources=["../../etc/passwd"])],
                              [first_pass([])], targets=[target])
            t = harness.ledger.targets["T-1"]
            passes = harness.orchestrator.blind_first_passes(t)
            harness.orchestrator.extract_issues(t, passes)
            self.assertEqual(t.frozen_evidence_paths, ["docs/a.md"])


class MalformedOutputTests(unittest.TestCase):
    def test_non_json_first_pass_is_an_execution_failure_not_a_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(tmp, ["I would rather write prose than JSON."],
                              [first_pass([])])
            report = harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertEqual(report.stop_reason, EXECUTION_STOP)
            self.assertIn(INVALID_PROVIDER_OUTPUT, report.execution_failures)
            self.assertFalse(report.is_epistemic_stop)
            self.assertEqual(harness.ledger.targets["T-1"].status, L.OPEN)

    def test_json_wrapped_in_a_code_fence_still_parses(self):
        parsed = protocol.parse_first_pass("here you go:\n```json\n"
                                           + first_pass(["a"]) + "\n```")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["objections"][0]["claim"], "a")

    def test_json_with_surrounding_prose_still_parses(self):
        self.assertIsNotNone(
            protocol.parse_first_pass("Preamble. " + first_pass(["a"]) + " Trailing.")
        )

    def test_objection_without_a_claim_is_rejected(self):
        raw = json.dumps({"assessment": "x", "objections": [{"kind": "other"}]})
        self.assertIsNone(protocol.parse_first_pass(raw))

    def test_empty_response_is_rejected(self):
        self.assertIsNone(protocol.parse_first_pass(""))


class ExecutionVersusEpistemicTests(unittest.TestCase):
    """Regression for audit finding 1: a ceiling is never a research outcome."""

    def _stalemate(self, tmp, max_rounds):
        gpt_issue = L.issue_id("T-1", "GPT objection.")
        claude_issue = L.issue_id("T-1", "Claude objection.")
        return Harness(
            tmp,
            claude_responses=[first_pass(["Claude objection."])]
            + [audit([act(gpt_issue, "REBUT")]), audit([act(claude_issue, "SUSTAIN")])] * 6,
            gpt_responses=[first_pass(["GPT objection."])]
            + [audit([act(claude_issue, "REBUT")]), audit([act(gpt_issue, "SUSTAIN")])] * 6,
            max_rounds=max_rounds,
        )

    def test_round_ceiling_does_not_write_a_terminal_disposition(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = self._stalemate(tmp, max_rounds=2)
            report = harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertEqual(report.stop_reason, ROUND_LIMIT)
            status = harness.ledger.targets["T-1"].status
            self.assertNotIn(status, L.TERMINAL_TARGET_STATUSES)
            self.assertNotEqual(status, L.UNDERDETERMINED)

    def test_round_ceiling_is_not_an_epistemic_stop(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = self._stalemate(tmp, max_rounds=2)
            report = harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertFalse(report.is_epistemic_stop)
            self.assertTrue(report.is_execution_stop)
            self.assertTrue(report.resumable)
            self.assertEqual(report.targets_closed, [])

    def test_round_ceiling_preserves_every_live_issue(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = self._stalemate(tmp, max_rounds=2)
            harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            live = harness.ledger.live_issues_for("T-1")
            self.assertEqual(len(live), 2)

    def test_round_ceiling_does_not_satisfy_a_downstream_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = self._stalemate(tmp, max_rounds=2)
            harness.ledger.add_target(make_target(
                id="T-2", depends_on=[L.Dependency(target_id="T-1")]))
            harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertFalse(harness.ledger.dependencies_satisfied("T-2"))
            with self.assertRaises(PermissionError):
                harness.ledger.select_target("T-2")

    def test_a_ceilinged_target_is_resumable(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = self._stalemate(tmp, max_rounds=2)
            harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            # Still the next eligible target: nothing was closed.
            self.assertEqual(harness.ledger.next_target().id, "T-1")

    def test_rate_limit_is_not_a_theoretical_stalemate(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(tmp, [RATE_LIMIT], [first_pass([])])
            report = harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertEqual(report.stop_reason, EXECUTION_STOP)
            self.assertIn(RATE_LIMIT, report.execution_failures)
            self.assertFalse(report.is_epistemic_stop)
            self.assertTrue(report.resumable)
            self.assertNotIn(harness.ledger.targets["T-1"].status,
                             L.TERMINAL_TARGET_STATUSES)

    def test_execution_failure_codes_are_disjoint_from_target_dispositions(self):
        from far_adversarial.providers import EXECUTION_FAILURES

        self.assertEqual(EXECUTION_FAILURES & L.TARGET_STATUSES, frozenset())

    def test_execution_stop_reasons_are_disjoint_from_epistemic_stop_reasons(self):
        from far_adversarial.orchestrator import EPISTEMIC_STOPS, EXECUTION_STOPS

        self.assertEqual(EPISTEMIC_STOPS & EXECUTION_STOPS, frozenset())


class EvidenceAndReplayTests(unittest.TestCase):
    def test_every_invocation_records_the_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(tmp, [first_pass([])], [first_pass([])])
            harness.orchestrator.blind_first_passes(harness.ledger.targets["T-1"])
            inv = harness.store.all_invocations()[0]
            for field in ("provider", "model", "config", "prompt_hash", "source_freeze",
                          "raw_response", "raw_response_hash", "normalized_response",
                          "normalized_response_hash", "usage", "started_at",
                          "finished_at", "schema_version", "resolved_model"):
                self.assertTrue(hasattr(inv, field), field)
            self.assertEqual(inv.raw_response_hash, sha256_hex(inv.raw_response))

    def test_resolved_model_identity_is_recorded_not_the_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(tmp, [first_pass([])], [first_pass([])])
            harness.orchestrator.blind_first_passes(harness.ledger.targets["T-1"])
            self.assertEqual(harness.orchestrator.resolved_models["gpt"], "gpt-test")

    def test_replay_reproduces_a_recorded_response_without_a_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EvidenceStore(Path(tmp) / "evidence")
            store.record(provider="gpt", model="gpt-test", config={},
                         prompt_text="the prompt", source_freeze="cafebabe",
                         raw_response="the recorded answer", normalized_response=None)
            replay = ReplayProvider(store, "gpt", "gpt-test", "cafebabe")
            self.assertEqual(replay.complete("the prompt").raw, "the recorded answer")

    def test_replay_of_an_unrecorded_prompt_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EvidenceStore(Path(tmp) / "evidence")
            replay = ReplayProvider(store, "gpt", "gpt-test", "cafebabe")
            self.assertFalse(replay.complete("never asked").ok)

    def test_replay_key_changes_when_the_frozen_source_changes(self):
        self.assertNotEqual(replay_key("gpt", "gpt-test", "abc", "freeze-1"),
                            replay_key("gpt", "gpt-test", "abc", "freeze-2"))

    def test_replay_key_changes_when_the_model_changes(self):
        self.assertNotEqual(replay_key("gpt", "gpt-4", "abc", "f"),
                            replay_key("gpt", "gpt-5", "abc", "f"))

    def test_tampered_raw_evidence_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EvidenceStore(Path(tmp) / "evidence")
            inv = store.record(provider="gpt", model="m", config={}, prompt_text="p",
                               source_freeze="f", raw_response="original",
                               normalized_response=None)
            (store.raw_dir / f"{inv.invocation_id}.txt").write_text("tampered",
                                                                    encoding="utf-8")
            self.assertTrue(store.verify_integrity())

    def test_tampered_normalized_response_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EvidenceStore(Path(tmp) / "evidence")
            store.record(provider="gpt", model="m", config={}, prompt_text="p",
                         source_freeze="f", raw_response="raw",
                         normalized_response={"objections": []})
            lines = store.index_path.read_text(encoding="utf-8").splitlines()
            record = json.loads(lines[0])
            record["normalized_response"] = {"objections": ["fabricated"]}
            store.index_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
            problems = store.verify_integrity()
            self.assertTrue(any("normalized" in p for p in problems))

    def test_secrets_never_reach_stored_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EvidenceStore(Path(tmp) / "evidence")
            inv = store.record(
                provider="gpt", model="m", config={},
                prompt_text="key sk-abcdefghijklmnopqrstuvwx", source_freeze="f",
                raw_response="echoing sk-abcdefghijklmnopqrstuvwx back",
                normalized_response=None,
            )
            self.assertNotIn("abcdefghijklmnopqrstuvwx", inv.prompt_text)
            self.assertNotIn("abcdefghijklmnopqrstuvwx", inv.raw_response)
            self.assertNotIn("abcdefghijklmnopqrstuvwx",
                             (store.raw_dir / f"{inv.invocation_id}.txt").read_text())


class ContinuationTests(unittest.TestCase):
    def _closing_scripts(self, target_id):
        issue = L.issue_id(target_id, f"{target_id} objection.")
        return (
            [first_pass([]), audit([act(issue, "REBUT")])],
            [first_pass([f"{target_id} objection."]), audit([act(issue, "WITHDRAW")])],
        )

    def test_next_target_loads_automatically_after_closure(self):
        with tempfile.TemporaryDirectory() as tmp:
            claude_a, gpt_a = self._closing_scripts("A")
            claude_b, gpt_b = self._closing_scripts("B")
            harness = Harness(
                tmp, claude_a + claude_b, gpt_a + gpt_b,
                targets=[make_target(id="A"),
                         make_target(id="B", depends_on=[L.Dependency(target_id="A")])],
                max_rounds=1,
            )
            reports = harness.orchestrator.run(max_targets=4)
            closed = [t for report in reports for t in report.targets_closed]
            self.assertEqual(closed, ["A", "B"])
            self.assertEqual(reports[-1].stop_reason, NO_ELIGIBLE_TARGET)
            self.assertTrue(reports[-1].is_epistemic_stop)

    def test_run_stops_on_execution_failure_without_closing_a_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(tmp, [RATE_LIMIT], [first_pass([])],
                              targets=[make_target(id="A"), make_target(id="B")])
            reports = harness.orchestrator.run(max_targets=4)
            self.assertEqual(reports[-1].stop_reason, EXECUTION_STOP)
            self.assertEqual(reports[-1].targets_closed, [])
            self.assertEqual(harness.ledger.targets["B"].status, L.OPEN)

    def test_run_stops_at_a_round_ceiling_without_advancing(self):
        with tempfile.TemporaryDirectory() as tmp:
            issue_a = L.issue_id("A", "A objection.")
            harness = Harness(
                tmp,
                claude_responses=[first_pass([])] + [audit([act(issue_a, "REBUT")]),
                                                     audit([])] * 4,
                gpt_responses=[first_pass(["A objection."])]
                + [audit([]), audit([act(issue_a, "SUSTAIN")])] * 4,
                targets=[make_target(id="A"), make_target(id="B")],
                max_rounds=2,
            )
            reports = harness.orchestrator.run(max_targets=4)
            self.assertEqual(reports[-1].stop_reason, ROUND_LIMIT)
            self.assertEqual(harness.ledger.targets["B"].status, L.OPEN)

    def test_ledger_is_persisted_between_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            claude_a, gpt_a = self._closing_scripts("A")
            harness = Harness(tmp, claude_a, gpt_a, targets=[make_target(id="A")],
                              max_rounds=1)
            harness.orchestrator.run(max_targets=1)
            reloaded = L.Ledger.load(harness.ledger.path)
            self.assertEqual(reloaded.targets["A"].status,
                             L.READY_UNDER_INTERNAL_PROTOCOL)


if __name__ == "__main__":
    unittest.main()
