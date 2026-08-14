"""The reconstructed live state must keep saying what the transcript says.

These tests guard the two failure modes that would silently corrupt the
research record: collapsing the transcript's confidence classes, and letting
the withdrawn DI3 argument creep back into the live queue.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from far_adversarial import calibration, ledger as L  # noqa: E402

import importlib.util  # noqa: E402

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
        text = TRANSCRIPT.read_text(encoding="utf-8")
        self.assertIn("NONCANONICAL", text.upper())


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

    def test_di3_is_withdrawn_and_stays_withdrawn(self):
        di3 = [i for i in self.ledger.issues.values() if i.claim.startswith("DI3:")]
        self.assertEqual(len(di3), 1)
        self.assertEqual(di3[0].state, L.ISSUE_WITHDRAWN)
        with self.assertRaises(L.IssueReopenError):
            self.ledger.apply_action(di3[0].id, actor="claude", action=L.SUSTAIN,
                                     rationale="resurrecting a settled argument")

    def test_di3_records_all_four_turns_it_ran_across(self):
        di3 = [i for i in self.ledger.issues.values() if i.claim.startswith("DI3:")][0]
        for turn in ("25", "28", "31", "32"):
            self.assertIn(turn, di3.provenance)

    def test_s1_is_not_authorized_for_restart(self):
        s1 = self.ledger.targets["PFAR-S1"]
        self.assertFalse(s1.authorized)
        self.assertEqual(s1.status, L.READY_UNDER_INTERNAL_PROTOCOL)

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

    def test_intra_sequent_frontier_conflation_is_conceded(self):
        conceded = [i for i in self.ledger.issues.values()
                    if "intra-sequent" in i.claim and i.state == L.ISSUE_CONCEDED]
        self.assertEqual(len(conceded), 1)

    def test_targets_with_unrecovered_protocol_are_not_authorized(self):
        for tid in ("PFAR-T1-T8", "PFAR-E0", "PFAR-SRB2", "PFAR-RC2"):
            self.assertFalse(self.ledger.targets[tid].authorized, tid)

    def test_the_next_dependency_valid_target_is_the_repository_successor_repair(self):
        # The Presenting FAR queue is source-blocked; the repository's
        # registered successor repair is the only executable next step.
        self.assertEqual(self.ledger.next_target().id, "REPO-UPP-SR-001-W1")

    def test_sr_w2_is_blocked_behind_sr_w1(self):
        with self.assertRaises(PermissionError):
            self.ledger.select_target("REPO-UPP-SR-001-W2")

    def test_build_is_deterministic_in_structure(self):
        other = build_live_state.build()
        self.assertEqual(sorted(self.ledger.targets), sorted(other.targets))
        self.assertEqual(sorted(self.ledger.issues), sorted(other.issues))


class CalibrationTests(unittest.TestCase):
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
