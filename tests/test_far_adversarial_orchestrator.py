"""Blindness, evidence preservation, replay, and continuation.

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
    TARGET_TERMINAL,
    replay_run,
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


def first_pass(objections, marker=""):
    return json.dumps(
        {
            "assessment": f"analysis {marker}",
            "objections": [
                {"claim": claim, "kind": "other", "rationale": "because"}
                for claim in objections
            ],
            "source_requests": [],
            "formal_obligations": [],
        }
    )


def audit(responses):
    return json.dumps({"responses": responses})


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
    def __init__(self, tmp, claude_responses, gpt_responses, targets=None,
                 max_rounds=4):
        self.ledger = L.Ledger(Path(tmp) / "state.json")
        for target in targets or [make_target()]:
            self.ledger.add_target(target)
        self.store = EvidenceStore(Path(tmp) / "evidence")
        self.claude = ScriptedProvider(claude_responses, name="claude", model="claude-test")
        self.gpt = ScriptedProvider(gpt_responses, name="gpt", model="gpt-test")
        self.orchestrator = Orchestrator(
            ledger=self.ledger,
            store=self.store,
            claude=self.claude,
            gpt=self.gpt,
            evidence_loader=lambda t: {"frozen.md": "frozen evidence body"},
            source_freeze="cafebabe",
            max_rounds_per_target=max_rounds,
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
            harness = Harness(
                tmp,
                claude_responses=[first_pass([])],
                gpt_responses=[first_pass([])],
            )
            harness.orchestrator.blind_first_passes(harness.ledger.targets["T-1"])
            claude_prompt = harness.orchestrator.lane_prompts["claude"][0]
            gpt_prompt = harness.orchestrator.lane_prompts["gpt"][0]
            marker = "## Eligible frozen evidence"
            self.assertEqual(claude_prompt.split(marker)[1], gpt_prompt.split(marker)[1])
            self.assertNotEqual(claude_prompt, gpt_prompt)  # roles differ

    def test_raw_output_is_preserved_before_any_cross_exchange(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[first_pass(["Claude objection."])],
                gpt_responses=[first_pass(["GPT objection."])],
            )
            harness.orchestrator.blind_first_passes(harness.ledger.targets["T-1"])
            recorded = harness.store.all_invocations()
            self.assertEqual(len(recorded), 2)
            self.assertEqual({inv.lane for inv in recorded}, {"claude", "gpt"})
            self.assertEqual(harness.ledger.issues, {})  # nothing extracted yet


class CrossAuditTests(unittest.TestCase):
    def test_each_lane_answers_only_the_other_lanes_objections(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[first_pass(["Claude objection."]), audit([])],
                gpt_responses=[first_pass(["GPT objection."]), audit([])],
            )
            target = harness.ledger.targets["T-1"]
            passes = harness.orchestrator.blind_first_passes(target)
            ids = harness.orchestrator.extract_issues(target, passes)
            harness.orchestrator.cross_audit(target, ids)
            claude_audit = harness.orchestrator.lane_prompts["claude"][1]
            gpt_audit = harness.orchestrator.lane_prompts["gpt"][1]
            self.assertIn("GPT objection.", claude_audit)
            self.assertNotIn("Claude objection.", claude_audit)
            self.assertIn("Claude objection.", gpt_audit)
            self.assertNotIn("GPT objection.", gpt_audit)

    def test_settled_issues_are_not_resent(self):
        gpt_issue = L.issue_id("T-1", "GPT objection.")
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[
                    first_pass([]),
                    audit([{"issue_id": gpt_issue, "action": "CONCEDE",
                            "rationale": "defeated", "revised_claim": None}]),
                    audit([]),
                ],
                gpt_responses=[first_pass(["GPT objection."]), audit([]), audit([])],
            )
            target = harness.ledger.targets["T-1"]
            passes = harness.orchestrator.blind_first_passes(target)
            ids = harness.orchestrator.extract_issues(target, passes)
            harness.orchestrator.cross_audit(target, ids)
            before = len(harness.orchestrator.lane_prompts["claude"])
            harness.orchestrator.cross_audit(target, ids)
            after_prompts = harness.orchestrator.lane_prompts["claude"][before:]
            for prompt in after_prompts:
                self.assertNotIn(gpt_issue, prompt)

    def test_response_naming_an_unregistered_issue_is_rejected(self):
        parsed = protocol.parse_cross_audit(
            audit([{"issue_id": "ISS-DEADBEEF00", "action": "SUSTAIN",
                    "rationale": "r", "revised_claim": None}]),
            known_issue_ids={"ISS-000000000000"},
        )
        self.assertIsNone(parsed)

    def test_unknown_action_is_rejected(self):
        parsed = protocol.parse_cross_audit(
            audit([{"issue_id": "ISS-1", "action": "APPROVE", "rationale": "r"}]),
            known_issue_ids={"ISS-1"},
        )
        self.assertIsNone(parsed)


class MalformedOutputTests(unittest.TestCase):
    def test_non_json_first_pass_is_an_execution_failure_not_a_finding(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=["I would rather write prose than JSON."],
                gpt_responses=[first_pass([])],
            )
            report = harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertEqual(report.stop_reason, EXECUTION_STOP)
            self.assertIn(INVALID_PROVIDER_OUTPUT, report.execution_failures)
            self.assertFalse(report.is_epistemic_stop)
            self.assertEqual(harness.ledger.targets["T-1"].status, L.OPEN)

    def test_json_wrapped_in_a_code_fence_still_parses(self):
        parsed = protocol.parse_first_pass("here you go:\n```json\n" + first_pass(["a"]) + "\n```")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["objections"][0]["claim"], "a")

    def test_json_with_surrounding_prose_still_parses(self):
        parsed = protocol.parse_first_pass("Preamble. " + first_pass(["a"]) + " Trailing.")
        self.assertIsNotNone(parsed)

    def test_objection_without_a_claim_is_rejected(self):
        raw = json.dumps({"assessment": "x", "objections": [{"kind": "other"}]})
        self.assertIsNone(protocol.parse_first_pass(raw))

    def test_empty_response_is_rejected(self):
        self.assertIsNone(protocol.parse_first_pass(""))


class ResourceStopTests(unittest.TestCase):
    def test_rate_limit_is_not_a_theoretical_stalemate(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[RATE_LIMIT],
                gpt_responses=[first_pass([])],
            )
            report = harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertEqual(report.stop_reason, EXECUTION_STOP)
            self.assertIn(RATE_LIMIT, report.execution_failures)
            self.assertFalse(report.is_epistemic_stop)
            self.assertNotIn(harness.ledger.targets["T-1"].status,
                             L.TERMINAL_TARGET_STATUSES)

    def test_execution_failure_codes_are_disjoint_from_target_dispositions(self):
        from far_adversarial.providers import EXECUTION_FAILURES

        self.assertEqual(EXECUTION_FAILURES & L.TARGET_STATUSES, frozenset())

    def test_round_ceiling_yields_underdetermined_not_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[first_pass(["Claude objection."])] + [audit([])] * 6,
                gpt_responses=[first_pass(["GPT objection."])] + [audit([])] * 6,
                max_rounds=2,
            )
            report = harness.orchestrator.run_target(harness.ledger.targets["T-1"])
            self.assertEqual(harness.ledger.targets["T-1"].status, L.UNDERDETERMINED)
            self.assertNotEqual(harness.ledger.targets["T-1"].status,
                                L.READY_UNDER_INTERNAL_PROTOCOL)
            self.assertEqual(report.stop_reason, TARGET_TERMINAL)


class EvidenceAndReplayTests(unittest.TestCase):
    def test_every_invocation_records_the_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(tmp, [first_pass([])], [first_pass([])])
            harness.orchestrator.blind_first_passes(harness.ledger.targets["T-1"])
            inv = harness.store.all_invocations()[0]
            for field in ("provider", "model", "config", "prompt_hash", "source_freeze",
                          "raw_response", "raw_response_hash", "normalized_response",
                          "normalized_response_hash", "usage", "started_at",
                          "finished_at", "schema_version"):
                self.assertTrue(hasattr(inv, field), field)
            self.assertEqual(inv.raw_response_hash, sha256_hex(inv.raw_response))

    def test_replay_reproduces_a_recorded_response_without_a_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EvidenceStore(Path(tmp) / "evidence")
            store.record(
                provider="gpt", model="gpt-test", config={}, prompt_text="the prompt",
                source_freeze="cafebabe", raw_response="the recorded answer",
                normalized_response=None,
            )
            replay = ReplayProvider(store, "gpt", "gpt-test", "cafebabe")
            self.assertEqual(replay.complete("the prompt").raw, "the recorded answer")

    def test_replay_of_an_unrecorded_prompt_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EvidenceStore(Path(tmp) / "evidence")
            replay = ReplayProvider(store, "gpt", "gpt-test", "cafebabe")
            result = replay.complete("never asked")
            self.assertFalse(result.ok)

    def test_replay_key_changes_when_the_frozen_source_changes(self):
        # Source drift must not silently reuse an answer from another freeze.
        self.assertNotEqual(
            replay_key("gpt", "gpt-test", "abc", "freeze-1"),
            replay_key("gpt", "gpt-test", "abc", "freeze-2"),
        )

    def test_replay_key_changes_when_the_model_changes(self):
        self.assertNotEqual(
            replay_key("gpt", "gpt-4", "abc", "f"),
            replay_key("gpt", "gpt-5", "abc", "f"),
        )

    def test_tampered_raw_evidence_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EvidenceStore(Path(tmp) / "evidence")
            inv = store.record(provider="gpt", model="m", config={}, prompt_text="p",
                               source_freeze="f", raw_response="original",
                               normalized_response=None)
            (store.raw_dir / f"{inv.invocation_id}.txt").write_text("tampered",
                                                                    encoding="utf-8")
            problems = store.verify_integrity()
            self.assertTrue(problems)
            self.assertFalse(replay_run(store)["replayable"])

    def test_secrets_never_reach_stored_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = EvidenceStore(Path(tmp) / "evidence")
            inv = store.record(
                provider="gpt", model="m", config={},
                prompt_text="key sk-abcdefghijklmnopqrstuvwx",
                source_freeze="f",
                raw_response="echoing sk-abcdefghijklmnopqrstuvwx back",
                normalized_response=None,
            )
            self.assertNotIn("abcdefghijklmnopqrstuvwx", inv.prompt_text)
            self.assertNotIn("abcdefghijklmnopqrstuvwx", inv.raw_response)
            self.assertNotIn("abcdefghijklmnopqrstuvwx",
                             (store.raw_dir / f"{inv.invocation_id}.txt").read_text())


class ContinuationTests(unittest.TestCase):
    def test_next_target_loads_automatically_after_closure(self):
        with tempfile.TemporaryDirectory() as tmp:
            targets = [
                make_target(id="A"),
                make_target(id="B", depends_on=["A"]),
            ]
            harness = Harness(
                tmp,
                claude_responses=[first_pass([]), first_pass([])],
                gpt_responses=[
                    first_pass(["A objection."]),
                    first_pass(["B objection."]),
                ],
                targets=targets,
            )
            # Claude concedes each objection in the cross-audit round.
            harness.claude._responses = [
                first_pass([]),
                audit([{"issue_id": L.issue_id("A", "A objection."), "action": "CONCEDE",
                        "rationale": "defeated", "revised_claim": None}]),
                first_pass([]),
                audit([{"issue_id": L.issue_id("B", "B objection."), "action": "CONCEDE",
                        "rationale": "defeated", "revised_claim": None}]),
            ]
            # GPT raises the only objection on each target, so it is never
            # asked to answer one: it is invoked once per target.
            harness.gpt._responses = [
                first_pass(["A objection."]),
                first_pass(["B objection."]),
            ]
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

    def test_ledger_is_persisted_between_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = Harness(
                tmp,
                claude_responses=[
                    first_pass([]),
                    audit([{"issue_id": L.issue_id("A", "A objection."),
                            "action": "CONCEDE", "rationale": "d", "revised_claim": None}]),
                ],
                gpt_responses=[first_pass(["A objection."]), audit([])],
                targets=[make_target(id="A")],
            )
            harness.orchestrator.run(max_targets=1)
            reloaded = L.Ledger.load(harness.ledger.path)
            self.assertEqual(reloaded.targets["A"].status,
                             L.READY_UNDER_INTERNAL_PROTOCOL)


if __name__ == "__main__":
    unittest.main()
