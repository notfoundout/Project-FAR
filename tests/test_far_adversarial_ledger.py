"""Ledger invariants for the adversarial relay.

These are the epistemic guarantees the manual Claude<->GPT process relied on a
human to remember. Automating the relay only helps if they are enforced.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from far_adversarial import ledger as L  # noqa: E402


def _target(**overrides):
    base = dict(
        id="T-1",
        original_formulation="original",
        current_formulation="current",
        frozen_scope="scope",
        provenance="test",
    )
    base.update(overrides)
    return L.Target(**base)


class IssueIdentityTests(unittest.TestCase):
    def test_issue_ids_are_stable_across_runs(self):
        first = L.issue_id("T-1", "The inference is invalid.")
        second = L.issue_id("T-1", "The inference is invalid.")
        self.assertEqual(first, second)

    def test_issue_ids_ignore_whitespace_and_case_only(self):
        self.assertEqual(
            L.issue_id("T-1", "The  inference IS invalid."),
            L.issue_id("T-1", "the inference is invalid"),
        )

    def test_different_wording_gets_a_different_id(self):
        # Semantic duplicates are never merged by similarity; reconciliation
        # must be an explicit recorded action.
        self.assertNotEqual(
            L.issue_id("T-1", "The inference is invalid."),
            L.issue_id("T-1", "The step does not follow."),
        )

    def test_same_claim_against_a_different_target_is_a_different_issue(self):
        self.assertNotEqual(
            L.issue_id("T-1", "The inference is invalid."),
            L.issue_id("T-2", "The inference is invalid."),
        )


class DefeatedIssueTests(unittest.TestCase):
    def setUp(self):
        self.ledger = L.Ledger()
        self.ledger.add_target(_target())

    def _issue(self, claim="Objection A."):
        return self.ledger.register_issue(
            target_id="T-1", claim=claim, raised_by="gpt", provenance="first-pass"
        )

    def test_withdrawn_issue_cannot_return_to_open(self):
        issue = self._issue()
        self.ledger.apply_action(issue.id, actor="gpt", action=L.WITHDRAW,
                                 rationale="no longer maintained")
        with self.assertRaises(L.IssueReopenError):
            self.ledger.apply_action(issue.id, actor="gpt", action=L.SUSTAIN,
                                     rationale="on second thought")

    def test_conceded_issue_cannot_be_resustained(self):
        issue = self._issue()
        self.ledger.apply_action(issue.id, actor="claude", action=L.CONCEDE,
                                 rationale="defeated")
        with self.assertRaises(L.IssueReopenError):
            self.ledger.apply_action(issue.id, actor="gpt", action=L.COUNTEREXAMPLE,
                                     rationale="recycling the same attack")

    def test_re_registering_a_withdrawn_claim_does_not_reopen_it(self):
        issue = self._issue()
        self.ledger.apply_action(issue.id, actor="gpt", action=L.WITHDRAW, rationale="x")
        again = self.ledger.register_issue(
            target_id="T-1", claim="Objection A.", raised_by="gpt", provenance="round-3"
        )
        self.assertEqual(again.id, issue.id)
        self.assertEqual(again.state, L.ISSUE_WITHDRAWN)

    def test_defeated_issue_remains_in_history(self):
        issue = self._issue()
        self.ledger.apply_action(issue.id, actor="gpt", action=L.WITHDRAW, rationale="x")
        self.assertIn(issue.id, self.ledger.issues)
        self.assertEqual([e.action for e in issue.history], ["RAISE", L.WITHDRAW])

    def test_later_withdrawal_supersedes_an_earlier_sustain(self):
        issue = self._issue()
        self.ledger.apply_action(issue.id, actor="gpt", action=L.SUSTAIN, rationale="stands")
        self.assertTrue(issue.is_live())
        self.ledger.apply_action(issue.id, actor="gpt", action=L.WITHDRAW, rationale="conceded")
        self.assertFalse(issue.is_live())
        self.assertTrue(issue.is_defeated())

    def test_revision_creates_a_successor_issue_with_its_own_identity(self):
        issue = self._issue()
        self.ledger.apply_action(issue.id, actor="gpt", action=L.REVISE,
                                 rationale="narrowed", revised_claim="Objection A, narrowed.")
        self.assertIsNotNone(issue.superseded_by)
        self.assertNotEqual(issue.superseded_by, issue.id)
        self.assertEqual(self.ledger.issues[issue.superseded_by].state, L.ISSUE_OPEN)


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.ledger = L.Ledger()
        self.ledger.add_target(_target())

    def test_agreement_does_not_imply_ready(self):
        issue = self.ledger.register_issue(
            target_id="T-1", claim="Scope drift in step 4.", raised_by="gpt",
            provenance="first-pass",
        )
        # Both lanes record agreement, but the objection still stands.
        self.ledger.apply_action(
            issue.id, actor="gpt", action=L.SUSTAIN, rationale="stands",
            agreement={"claude": "agree", "gpt": "agree", "both_say_ready": True},
        )
        self.assertEqual(self.ledger.evaluate_target("T-1"), L.NEAR_READY)
        self.assertNotEqual(
            self.ledger.evaluate_target("T-1"), L.READY_UNDER_INTERNAL_PROTOCOL
        )

    def test_ready_requires_an_actually_adjudicated_objection(self):
        # A target nobody ever attacked is untested, not ready.
        self.assertEqual(self.ledger.evaluate_target("T-1"), L.OPEN)

    def test_ready_when_every_registered_objection_is_defeated(self):
        issue = self.ledger.register_issue(
            target_id="T-1", claim="Hidden assumption.", raised_by="gpt",
            provenance="first-pass",
        )
        self.ledger.apply_action(issue.id, actor="gpt", action=L.WITHDRAW, rationale="x")
        self.assertEqual(
            self.ledger.evaluate_target("T-1"), L.READY_UNDER_INTERNAL_PROTOCOL
        )

    def test_source_request_blocks_readiness(self):
        issue = self.ledger.register_issue(
            target_id="T-1", claim="Needs the frozen corpus.", raised_by="claude",
            provenance="first-pass",
        )
        self.ledger.apply_action(issue.id, actor="claude", action=L.REQUEST_SOURCE,
                                 rationale="artifact absent")
        self.assertEqual(self.ledger.evaluate_target("T-1"), L.SOURCE_REQUIRED)

    def test_governance_block_outranks_source_request(self):
        first = self.ledger.register_issue(target_id="T-1", claim="Needs a source.",
                                           raised_by="claude", provenance="p")
        second = self.ledger.register_issue(target_id="T-1", claim="Needs a decision.",
                                            raised_by="gpt", provenance="p")
        self.ledger.apply_action(first.id, actor="claude", action=L.REQUEST_SOURCE,
                                 rationale="x")
        self.ledger.apply_action(second.id, actor="gpt", action=L.GOVERNANCE_BLOCK,
                                 rationale="y")
        self.assertEqual(
            self.ledger.evaluate_target("T-1"), L.GOVERNANCE_DECISION_REQUIRED
        )

    def test_formal_obligation_blocks_readiness(self):
        issue = self.ledger.register_issue(target_id="T-1", claim="Needs a proof.",
                                           raised_by="gpt", provenance="p")
        self.ledger.apply_action(issue.id, actor="claude",
                                 action=L.FORMAL_CHECK_REQUIRED_ACTION, rationale="x")
        self.assertEqual(self.ledger.evaluate_target("T-1"), L.FORMAL_CHECK_REQUIRED)

    def test_missing_evidence_prevents_ready(self):
        target = self.ledger.targets["T-1"]
        target.missing_evidence.append("frozen statement NOT_RECOVERED")
        issue = self.ledger.register_issue(target_id="T-1", claim="Objection.",
                                           raised_by="gpt", provenance="p")
        self.ledger.apply_action(issue.id, actor="gpt", action=L.WITHDRAW, rationale="x")
        self.assertEqual(self.ledger.evaluate_target("T-1"), L.SOURCE_REQUIRED)

    def test_ready_is_not_acceptance(self):
        # The disposition vocabulary must not contain a canonical status.
        self.assertNotIn("ACCEPTED", L.TARGET_STATUSES)
        self.assertNotIn("PROMOTED", L.TARGET_STATUSES)


class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.ledger = L.Ledger()
        self.ledger.add_target(_target(id="A", authorized=True))
        self.ledger.add_target(_target(id="B", authorized=True, depends_on=["A"]))
        self.ledger.add_target(_target(id="C", authorized=False))

    def test_next_target_respects_dependency_order(self):
        self.assertEqual(self.ledger.next_target().id, "A")

    def test_next_target_advances_after_a_terminal_disposition(self):
        self.ledger.set_target_status("A", L.READY_UNDER_INTERNAL_PROTOCOL)
        self.assertEqual(self.ledger.next_target().id, "B")

    def test_unauthorized_target_is_never_selected(self):
        self.ledger.set_target_status("A", L.REFUTED)
        self.ledger.set_target_status("B", L.REFUTED)
        self.assertIsNone(self.ledger.next_target())

    def test_explicit_selection_of_an_unauthorized_target_is_blocked(self):
        with self.assertRaises(PermissionError):
            self.ledger.select_target("C")

    def test_explicit_selection_with_unmet_dependencies_is_blocked(self):
        with self.assertRaises(PermissionError):
            self.ledger.select_target("B")


class PersistenceTests(unittest.TestCase):
    def test_unresolved_issues_survive_a_reload(self):
        # A reload is what a compacted context looks like from disk.
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            original = L.Ledger(path)
            original.add_target(_target(authorized=True))
            live = original.register_issue(target_id="T-1", claim="Still standing.",
                                           raised_by="gpt", provenance="p")
            dead = original.register_issue(target_id="T-1", claim="Given up.",
                                           raised_by="gpt", provenance="p")
            original.apply_action(dead.id, actor="gpt", action=L.WITHDRAW, rationale="x")
            original.save()

            reloaded = L.Ledger.load(path)
            self.assertEqual(original.digest(), reloaded.digest())
            self.assertEqual([i.id for i in reloaded.live_issues_for("T-1")], [live.id])
            self.assertTrue(reloaded.issues[dead.id].is_defeated())
            # And it is still un-reopenable after the round trip.
            with self.assertRaises(L.IssueReopenError):
                reloaded.apply_action(dead.id, actor="gpt", action=L.SUSTAIN, rationale="x")

    def test_history_survives_a_reload(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            original = L.Ledger(path)
            original.add_target(_target())
            issue = original.register_issue(target_id="T-1", claim="c", raised_by="gpt",
                                            provenance="p")
            original.apply_action(issue.id, actor="claude", action=L.CONCEDE, rationale="r")
            original.save()
            reloaded = L.Ledger.load(path)
            self.assertEqual([e.action for e in reloaded.issues[issue.id].history],
                             ["RAISE", L.CONCEDE])


class ProvenanceTests(unittest.TestCase):
    def test_target_without_provenance_is_refused(self):
        led = L.Ledger()
        with self.assertRaises(ValueError):
            led.add_target(L.Target(id="X", original_formulation="o",
                                    current_formulation="c", frozen_scope="s",
                                    provenance=""))

    def test_unknown_confidence_class_is_refused(self):
        led = L.Ledger()
        with self.assertRaises(ValueError):
            led.add_target(_target(confidence_class="PROBABLY_FINE"))

    def test_confidence_classes_are_not_collapsed(self):
        self.assertEqual(len(L.CONFIDENCE_CLASSES), 3)
        self.assertIn(L.EXACT_TRANSCRIPT_EVIDENCE, L.CONFIDENCE_CLASSES)
        self.assertIn(L.RECONSTRUCTED_RESEARCH_STATE, L.CONFIDENCE_CLASSES)
        self.assertIn(L.MISSING_TRANSCRIPT_EVIDENCE, L.CONFIDENCE_CLASSES)


if __name__ == "__main__":
    unittest.main()
