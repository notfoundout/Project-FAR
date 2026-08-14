"""The reconstructed live state must keep saying what the transcript says.

These tests guard the failure modes that would silently corrupt the research
record: collapsing the transcript's confidence classes, letting the withdrawn
DI3 argument creep back into the live queue, presenting a transcribed
disposition as a derived one, and weakening a calibration case after it missed.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from far_adversarial import calibration, ledger as L  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "build_live_state", ROOT / "tools" / "build_presenting_far_live_state.py"
)
build_live_state = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = build_live_state
_spec.loader.exec_module(build_live_state)

TRANSCRIPT = ROOT / ".far" / "inbox" / "presenting-project-far.md"


class TranscriptConfidenceTests(unittest.TestCase):
    @unittest.skipUnless(TRANSCRIPT.exists(), "transcript reconstruction not present")
    def test_transcript_declares_all_three_confidence_labels(self):
        text = TRANSCRIPT.read_text(encoding="utf-8")
        for label in ("VERBATIM-RECOVERED", "RECONSTRUCTED-HIGH", "GAP"):
            self.assertIn(label, text)

    @unittest.skipUnless(TRANSCRIPT.exists(), "transcript reconstruction not present")
    def test_truncation_marker_is_preserved(self):
        # The Turn 33 source cuts off mid-sentence. Completing it would be
        # fabrication, so the marker must survive verbatim.
        text = TRANSCRIPT.read_text(encoding="utf-8")
        self.assertIn("RECOVERED SOURCE TRUNCATES HERE", text)

    @unittest.skipUnless(TRANSCRIPT.exists(), "transcript reconstruction not present")
    def test_transcript_is_marked_noncanonical(self):
        self.assertIn("NONCANONICAL", TRANSCRIPT.read_text(encoding="utf-8").upper())


class LiveStateTests(unittest.TestCase):
    def setUp(self):
        self.ledger = build_live_state.build()

    def test_every_target_carries_provenance_and_a_confidence_class(self):
        for target in self.ledger.targets.values():
            self.assertTrue(target.provenance, target.id)
            self.assertIn(target.confidence_class, L.CONFIDENCE_CLASSES, target.id)

    def test_every_issue_carries_provenance_and_a_confidence_class(self):
        for issue in self.ledger.issues.values():
            self.assertTrue(issue.provenance, issue.id)
            self.assertIn(issue.confidence_class, L.CONFIDENCE_CLASSES, issue.id)

    def test_every_obligation_carries_provenance(self):
        for obligation in self.ledger.obligations.values():
            self.assertTrue(obligation.provenance, obligation.id)

    def test_di3_is_withdrawn_and_stays_withdrawn(self):
        di3 = [i for i in self.ledger.issues.values() if i.claim.startswith("DI3:")]
        self.assertEqual(len(di3), 1)
        self.assertEqual(di3[0].state, L.ISSUE_WITHDRAWN)
        with self.assertRaises(L.IssueReopenError):
            self.ledger.apply_action(di3[0].id, actor="claude", action=L.SUSTAIN,
                                     rationale="resurrecting a settled argument")

    def test_di3_was_defeated_by_its_owner_not_by_the_other_lane(self):
        # GPT rebutted; only Claude, who raised it, could end it.
        di3 = [i for i in self.ledger.issues.values() if i.claim.startswith("DI3:")][0]
        self.assertEqual(di3.raised_by, "claude")
        actions = {(e.actor, e.action) for e in di3.history}
        self.assertIn(("gpt", L.REBUT), actions)
        self.assertIn(("claude", L.WITHDRAW), actions)
        self.assertNotIn("gpt", {e.actor for e in di3.history
                                 if e.to_state in L.DEFEATED_ISSUE_STATES})

    def test_di3_records_all_four_turns_it_ran_across(self):
        di3 = [i for i in self.ledger.issues.values() if i.claim.startswith("DI3:")][0]
        for turn in ("25", "28", "31", "32"):
            self.assertIn(turn, di3.provenance)

    def test_s1_is_not_authorized_for_restart(self):
        s1 = self.ledger.targets["PFAR-S1"]
        self.assertFalse(s1.authorized)
        self.assertEqual(s1.status, L.READY_UNDER_INTERNAL_PROTOCOL)

    def test_s1_ready_is_recorded_not_derived(self):
        # This executor could not have derived READY: the frozen protocol that
        # produced it is unrecovered.
        s1 = self.ledger.targets["PFAR-S1"]
        self.assertEqual(s1.status_basis, L.STATUS_RECORDED)
        self.assertIn("RECORDED", " ".join(s1.notes))

    def test_s1_ready_is_recorded_as_non_acceptance(self):
        self.assertIn("not Acceptance",
                      " ".join(self.ledger.targets["PFAR-S1"].notes))
        self.assertIn("not Project FAR Acceptance", self.ledger.meta["not_acceptance"])

    def test_s1_missing_evidence_is_recorded_rather_than_invented(self):
        s1 = self.ledger.targets["PFAR-S1"]
        joined = " ".join(s1.missing_evidence)
        for identifier in ("CDE-v1", "FDI1-FDI5", "SR-B2"):
            self.assertIn(identifier, joined)
        self.assertIn("NOT_RECOVERED", s1.original_formulation)

    def test_s1_source_obligations_are_registered_and_unresolved(self):
        blocking = self.ledger.blocking_obligations_for("PFAR-S1")
        self.assertGreaterEqual(len(blocking), 3)
        self.assertTrue(all(o.kind == L.OBLIGATION_SOURCE for o in blocking))

    def test_turn_33_corrections_are_preserved_verbatim_on_the_target(self):
        # The intra-sequent/frontier concession and the DF-02b weakening were
        # corrections to Claude's defeated argument, not standing objections to
        # S1, so they live as recorded supporting material.
        s1 = self.ledger.targets["PFAR-S1"]
        supporting = " ".join(s1.supporting_arguments)
        self.assertIn("intra-sequent", supporting)
        self.assertIn("frontier representation are distinct analytical levels", supporting)
        self.assertIn("No eligible source encountered so far has been certified",
                      supporting)
        self.assertTrue(any("conflated" in c for c in s1.concessions))

    def test_rc1_objections_stand_against_it(self):
        # Claude was challenged and conceded, so the objections are upheld and
        # RC1 is refuted rather than quietly resolved.
        upheld = [i for i in self.ledger.issues_for("PFAR-RC1") if i.is_upheld()]
        self.assertEqual(len(upheld), 6)
        self.assertEqual(self.ledger.evaluate_target("PFAR-RC1"), L.REFUTED)
        self.assertEqual(self.ledger.targets["PFAR-RC1"].status, L.REFUTED)

    def test_rc2_repairs_remain_live(self):
        self.assertEqual(len(self.ledger.live_issues_for("PFAR-RC2")), 5)

    def test_targets_with_unrecovered_protocol_are_not_authorized(self):
        for tid in ("PFAR-T1-T8", "PFAR-E0", "PFAR-SRB2", "PFAR-RC2"):
            self.assertFalse(self.ledger.targets[tid].authorized, tid)

    def test_the_next_dependency_valid_target_is_the_repository_successor_repair(self):
        # The Presenting FAR queue is source-blocked; the repository's
        # registered successor repair is the next executable path.
        self.assertEqual(self.ledger.next_target().id, "REPO-UPP-SR-001-W1")

    def test_sr_w1_carries_its_registered_formal_obligation(self):
        blocking = self.ledger.blocking_obligations_for("REPO-UPP-SR-001-W1")
        self.assertEqual(len(blocking), 1)
        self.assertEqual(blocking[0].kind, L.OBLIGATION_FORMAL)

    def test_sr_w2_requires_sr_w1_to_be_established_not_merely_terminal(self):
        dependency = self.ledger.targets["REPO-UPP-SR-001-W2"].depends_on[0]
        self.assertEqual(dependency.requires, [L.READY_UNDER_INTERNAL_PROTOCOL])
        self.assertFalse(dependency.accept_recorded)
        with self.assertRaises(PermissionError):
            self.ledger.select_target("REPO-UPP-SR-001-W2")

    def test_a_refuted_sr_w1_does_not_unlock_sr_w2(self):
        self.ledger.set_target_status("REPO-UPP-SR-001-W1", L.REFUTED)
        self.assertFalse(self.ledger.dependencies_satisfied("REPO-UPP-SR-001-W2"))

    def test_sr_w1_is_described_as_the_next_executable_path_not_a_proven_critical_path(self):
        notes = " ".join(self.ledger.targets["REPO-UPP-SR-001-W1"].notes)
        self.assertIn("next fully specified, authorized executable research path", notes)
        self.assertIn("Not a proven global critical path", notes)

    def test_declared_frozen_evidence_paths_are_repository_relative(self):
        for target in self.ledger.targets.values():
            for path in target.frozen_evidence_paths:
                self.assertFalse(path.startswith("/"), path)
                self.assertNotIn("..", path)

    def test_build_is_deterministic(self):
        other = build_live_state.build()
        self.assertEqual(self.ledger.digest(), other.digest())


class CalibrationImmutabilityTests(unittest.TestCase):
    """Regression for audit finding 12: v1 and its MISS must not be softened."""

    # Pinned at the value the graded sandboxed run was scored against. Any edit
    # to a case's stimulus, markers, or failure markers changes this and fails.
    FROZEN_PREREGISTRATION_DIGEST = (
        "6e03129580bbd98bd5010819da3c5405a4e7e91c56f059b2af6066e833651374"
    )

    def test_the_preregistration_digest_is_unchanged(self):
        self.assertEqual(
            calibration.preregistration_digest(list(calibration.CASES)),
            self.FROZEN_PREREGISTRATION_DIGEST,
        )

    def test_the_missed_marker_group_still_exists(self):
        # Group 1 is the intra-sequent/frontier level distinction: the group
        # the sandboxed run missed. Deleting or loosening it would convert a
        # recorded miss into a pass without rerunning anything.
        self.assertEqual(len(calibration.DI3_CASE.required_markers), 3)
        group = calibration.DI3_CASE.required_markers[1]
        self.assertTrue(any("intra" in marker for marker in group))
        self.assertTrue(any("frontier" in marker for marker in group))

    def test_the_recorded_report_still_records_a_miss(self):
        import json

        report_path = (ROOT / ".far" / "research" / "presenting-far"
                       / "calibration-report.json")
        if not report_path.exists():
            self.skipTest("calibration report not present")
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(report["preregistration_digest"],
                         self.FROZEN_PREREGISTRATION_DIGEST)
        result = report["results"][0]
        self.assertFalse(result["passed"])
        self.assertEqual(result["missed_groups"], [1])


class CalibrationCaseTests(unittest.TestCase):
    def test_stimulus_never_contains_the_known_answer(self):
        for case in calibration.CASES.values():
            self.assertNotIn(case.known_answer, case.stimulus)
            self.assertNotIn("Turn 33", case.stimulus)
            self.assertNotIn("withdraw", case.stimulus.lower())

    def test_preregistration_digest_is_stable(self):
        ids = list(calibration.CASES)
        self.assertEqual(calibration.preregistration_digest(ids),
                         calibration.preregistration_digest(ids))

    def test_a_response_reproducing_the_historical_correction_passes(self):
        response = (
            "The argument is invalid. It conflates the absence of a canonical "
            "deterministic search strategy with the absence of a completely "
            "determined transition relation; a highly nondeterministic relation is "
            "still completely determined. It also treats intra-sequent collection "
            "(lists/sets/multisets) as if it were the frontier level, but these are "
            "distinct levels. The surviving negative claim is only that no eligible "
            "source has been certified to determine the frozen frontier-level "
            "search structure."
        )
        self.assertTrue(calibration.grade(calibration.DI3_CASE, response).passed)

    def test_a_response_repeating_the_defeated_position_is_a_miss(self):
        response = (
            "The argument is valid and S1 must stay OPEN, because LK proof search "
            "genuinely has no canonical strategy."
        )
        result = calibration.grade(calibration.DI3_CASE, response)
        self.assertFalse(result.passed)
        self.assertTrue(result.fired_failure_markers)

    def test_a_half_correct_response_is_a_miss(self):
        # Getting the determinism point but missing the level distinction is
        # recorded as a miss, not rounded up to a pass.
        response = (
            "The argument is invalid: a nondeterministic transition relation is "
            "still a completely determined transition relation."
        )
        result = calibration.grade(calibration.DI3_CASE, response)
        self.assertFalse(result.passed)
        self.assertIn(1, result.missed_groups)


if __name__ == "__main__":
    unittest.main()
