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


class ActionOwnershipTests(unittest.TestCase):
    """Regression for audit finding 3: action legality must be actor-sensitive."""

    def setUp(self):
        self.ledger = L.Ledger()
        self.ledger.add_target(_target())
        self.issue = self.ledger.register_issue(
            target_id="T-1", claim="Objection A.", raised_by="gpt", provenance="p"
        )

    def test_challenged_party_may_not_withdraw_someone_elses_objection(self):
        with self.assertRaises(L.IllegalActionError):
            self.ledger.apply_action(self.issue.id, actor="claude", action=L.WITHDRAW,
                                     rationale="not mine to drop")

    def test_challenged_party_may_not_sustain_someone_elses_objection(self):
        with self.assertRaises(L.IllegalActionError):
            self.ledger.apply_action(self.issue.id, actor="claude", action=L.SUSTAIN,
                                     rationale="not mine to sustain")

    def test_challenged_party_may_not_revise_someone_elses_objection(self):
        with self.assertRaises(L.IllegalActionError):
            self.ledger.apply_action(self.issue.id, actor="claude", action=L.REVISE,
                                     rationale="rewriting your objection",
                                     revised_claim="narrower")

    def test_owner_may_not_rebut_its_own_objection(self):
        with self.assertRaises(L.IllegalActionError):
            self.ledger.apply_action(self.issue.id, actor="gpt", action=L.REBUT,
                                     rationale="arguing with myself")

    def test_owner_may_not_concede_its_own_objection(self):
        # Giving up your own objection is WITHDRAW, which is a different record.
        with self.assertRaises(L.IllegalActionError):
            self.ledger.apply_action(self.issue.id, actor="gpt", action=L.CONCEDE,
                                     rationale="wrong verb")

    def test_owner_may_withdraw(self):
        self.ledger.apply_action(self.issue.id, actor="gpt", action=L.WITHDRAW,
                                 rationale="defeated")
        self.assertEqual(self.issue.state, L.ISSUE_WITHDRAWN)

    def test_challenged_party_may_rebut_and_concede(self):
        self.ledger.apply_action(self.issue.id, actor="claude", action=L.REBUT,
                                 rationale="answered")
        self.assertEqual(self.issue.state, L.ISSUE_REBUTTED)
        self.ledger.apply_action(self.issue.id, actor="gpt", action=L.SUSTAIN,
                                 rationale="unanswered")
        self.assertEqual(self.issue.state, L.ISSUE_SUSTAINED)

    def test_both_sides_may_raise_blocking_actions(self):
        for actor, action in (("claude", L.REQUEST_SOURCE), ("gpt", L.GOVERNANCE_BLOCK)):
            ledger = L.Ledger()
            ledger.add_target(_target())
            issue = ledger.register_issue(target_id="T-1", claim="c", raised_by="gpt",
                                          provenance="p")
            ledger.apply_action(issue.id, actor=actor, action=action, rationale="r")
            self.assertTrue(issue.is_blocking())

    def test_every_action_is_permitted_to_exactly_one_or_both_roles(self):
        # Exhaustive: no action may be unreachable by both roles.
        for action in L.ISSUE_ACTIONS:
            self.assertTrue(
                action in L.OWNER_ACTIONS or action in L.CHALLENGED_ACTIONS, action
            )

    def test_no_action_lets_a_challenged_lane_defeat_an_objection(self):
        # Regression for audit finding 2. This is the core property: nothing a
        # challenged lane can say ends an objection it does not own.
        ledger = L.Ledger()
        ledger.add_target(_target())
        for action in sorted(L.CHALLENGED_ACTIONS):
            issue = ledger.register_issue(
                target_id="T-1", claim=f"Objection via {action}.", raised_by="gpt",
                provenance="p",
            )
            ledger.apply_action(issue.id, actor="claude", action=action, rationale="r")
            self.assertNotIn(issue.state, L.DEFEATED_ISSUE_STATES, action)

    def test_reject_is_not_an_available_action(self):
        # REJECT used to move an objection straight into a defeated state.
        self.assertNotIn("REJECT", L.ISSUE_ACTIONS)


class EvidenceSettlementTests(unittest.TestCase):
    def setUp(self):
        self.ledger = L.Ledger()
        self.ledger.add_target(_target())
        self.issue = self.ledger.register_issue(
            target_id="T-1", claim="Objection A.", raised_by="gpt", provenance="p"
        )

    def test_a_lane_may_not_settle_an_issue(self):
        for actor in ("claude", "gpt"):
            with self.assertRaises(L.IllegalActionError):
                self.ledger.settle_issue(self.issue.id, actor=actor, outcome="DEFEATED",
                                         rationale="r", evidence_ref="ref")

    def test_deterministic_evidence_may_defeat_an_issue(self):
        self.ledger.settle_issue(self.issue.id, actor="deterministic",
                                 outcome="DEFEATED", rationale="checker output",
                                 evidence_ref="tools/check_x.py run 42")
        self.assertEqual(self.issue.state, L.ISSUE_SETTLED_DEFEATED)

    def test_settlement_requires_an_evidence_reference(self):
        with self.assertRaises(ValueError):
            self.ledger.settle_issue(self.issue.id, actor="formal", outcome="UPHELD",
                                     rationale="r", evidence_ref="")

    def test_settled_issue_cannot_be_settled_again(self):
        self.ledger.settle_issue(self.issue.id, actor="source", outcome="UPHELD",
                                 rationale="r", evidence_ref="doc#L1")
        with self.assertRaises(L.IssueReopenError):
            self.ledger.settle_issue(self.issue.id, actor="source", outcome="DEFEATED",
                                     rationale="r", evidence_ref="doc#L2")


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

    def test_conceded_issue_cannot_be_reworked(self):
        issue = self._issue()
        self.ledger.apply_action(issue.id, actor="claude", action=L.CONCEDE,
                                 rationale="the objection is right")
        with self.assertRaises(L.IssueReopenError):
            self.ledger.apply_action(issue.id, actor="claude", action=L.REBUT,
                                     rationale="actually no")

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
        self.ledger.apply_action(issue.id, actor="claude", action=L.REBUT, rationale="a")
        self.ledger.apply_action(issue.id, actor="gpt", action=L.SUSTAIN, rationale="stands")
        self.assertTrue(issue.is_live())
        self.ledger.apply_action(issue.id, actor="gpt", action=L.WITHDRAW, rationale="ok")
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

    def _defeat(self, claim="Hidden assumption."):
        issue = self.ledger.register_issue(target_id="T-1", claim=claim,
                                           raised_by="gpt", provenance="p")
        self.ledger.apply_action(issue.id, actor="claude", action=L.REBUT, rationale="a")
        self.ledger.apply_action(issue.id, actor="gpt", action=L.WITHDRAW, rationale="ok")
        return issue

    def test_agreement_does_not_imply_ready(self):
        issue = self.ledger.register_issue(
            target_id="T-1", claim="Scope drift in step 4.", raised_by="gpt",
            provenance="first-pass",
        )
        self.ledger.apply_action(issue.id, actor="claude", action=L.REBUT, rationale="a")
        self.ledger.apply_action(
            issue.id, actor="gpt", action=L.SUSTAIN, rationale="stands",
            agreement={"claude": "agree", "gpt": "agree", "both_say_ready": True},
        )
        self.assertEqual(self.ledger.evaluate_target("T-1"), L.NEAR_READY)

    def test_ready_requires_an_actually_adjudicated_objection(self):
        self.assertEqual(self.ledger.evaluate_target("T-1"), L.OPEN)

    def test_ready_when_every_registered_objection_is_defeated(self):
        self._defeat()
        self.assertEqual(
            self.ledger.evaluate_target("T-1"), L.READY_UNDER_INTERNAL_PROTOCOL
        )

    def test_conceded_objection_refutes_the_target(self):
        issue = self.ledger.register_issue(target_id="T-1", claim="Fatal.",
                                           raised_by="gpt", provenance="p")
        self.ledger.apply_action(issue.id, actor="claude", action=L.CONCEDE,
                                 rationale="it is right")
        self.assertEqual(self.ledger.evaluate_target("T-1"), L.REFUTED)

    def test_unresolved_source_obligation_blocks_ready(self):
        """Regression for audit finding 4."""
        self._defeat()
        self.ledger.register_obligation(
            target_id="T-1", kind=L.OBLIGATION_SOURCE,
            statement="the frozen corpus E0", raised_by="claude", provenance="first-pass",
        )
        self.assertEqual(self.ledger.evaluate_target("T-1"), L.SOURCE_REQUIRED)

    def test_unresolved_formal_obligation_blocks_ready(self):
        """Regression for audit finding 4."""
        self._defeat()
        self.ledger.register_obligation(
            target_id="T-1", kind=L.OBLIGATION_FORMAL,
            statement="discharge the determinacy lemma", raised_by="gpt",
            provenance="first-pass",
        )
        self.assertEqual(self.ledger.evaluate_target("T-1"), L.FORMAL_CHECK_REQUIRED)

    def test_discharged_obligation_stops_blocking(self):
        self._defeat()
        obligation = self.ledger.register_obligation(
            target_id="T-1", kind=L.OBLIGATION_FORMAL, statement="lemma",
            raised_by="gpt", provenance="first-pass",
        )
        self.ledger.resolve_obligation(
            obligation.id, actor="formal", state=L.OBLIGATION_DISCHARGED,
            resolution_provenance="mechanization/proof.lean#L40",
        )
        self.assertEqual(
            self.ledger.evaluate_target("T-1"), L.READY_UNDER_INTERNAL_PROTOCOL
        )

    def test_a_lane_cannot_discharge_its_own_obligation(self):
        obligation = self.ledger.register_obligation(
            target_id="T-1", kind=L.OBLIGATION_FORMAL, statement="lemma",
            raised_by="gpt", provenance="p",
        )
        with self.assertRaises(L.IllegalActionError):
            self.ledger.resolve_obligation(
                obligation.id, actor="gpt", state=L.OBLIGATION_DISCHARGED,
                resolution_provenance="I say so",
            )

    def test_obligation_resolution_requires_provenance(self):
        obligation = self.ledger.register_obligation(
            target_id="T-1", kind=L.OBLIGATION_SOURCE, statement="artifact",
            raised_by="gpt", provenance="p",
        )
        with self.assertRaises(ValueError):
            self.ledger.resolve_obligation(
                obligation.id, actor="source", state=L.OBLIGATION_DISCHARGED,
                resolution_provenance="",
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

    def test_missing_evidence_prevents_ready(self):
        self.ledger.targets["T-1"].missing_evidence.append("frozen statement NOT_RECOVERED")
        self._defeat()
        self.assertEqual(self.ledger.evaluate_target("T-1"), L.SOURCE_REQUIRED)

    def test_ready_is_not_acceptance(self):
        self.assertNotIn("ACCEPTED", L.TARGET_STATUSES)
        self.assertNotIn("PROMOTED", L.TARGET_STATUSES)


class DependencyPredicateTests(unittest.TestCase):
    """Regression for audit finding 5: terminal is not the same as established."""

    def _pair(self, requires=None, predecessor_status=L.OPEN,
              basis=L.STATUS_DERIVED, accept_recorded=False):
        ledger = L.Ledger()
        ledger.add_target(_target(id="A", authorized=True, status=predecessor_status,
                                  status_basis=basis))
        dependency = L.Dependency(target_id="A", accept_recorded=accept_recorded)
        if requires is not None:
            dependency.requires = requires
        ledger.add_target(_target(id="B", authorized=True, depends_on=[dependency]))
        return ledger

    def test_established_predecessor_unlocks_the_dependant(self):
        ledger = self._pair(predecessor_status=L.READY_UNDER_INTERNAL_PROTOCOL)
        self.assertTrue(ledger.dependencies_satisfied("B"))

    def test_refuted_predecessor_does_not_unlock(self):
        ledger = self._pair(predecessor_status=L.REFUTED)
        self.assertFalse(ledger.dependencies_satisfied("B"))
        with self.assertRaises(PermissionError):
            ledger.select_target("B")

    def test_source_required_predecessor_does_not_unlock(self):
        ledger = self._pair(predecessor_status=L.SOURCE_REQUIRED)
        self.assertFalse(ledger.dependencies_satisfied("B"))

    def test_governance_blocked_predecessor_does_not_unlock(self):
        ledger = self._pair(predecessor_status=L.GOVERNANCE_DECISION_REQUIRED)
        self.assertFalse(ledger.dependencies_satisfied("B"))

    def test_underdetermined_predecessor_does_not_unlock(self):
        ledger = self._pair(predecessor_status=L.UNDERDETERMINED)
        self.assertFalse(ledger.dependencies_satisfied("B"))

    def test_formal_check_required_predecessor_does_not_unlock(self):
        ledger = self._pair(predecessor_status=L.FORMAL_CHECK_REQUIRED)
        self.assertFalse(ledger.dependencies_satisfied("B"))

    def test_blocked_predecessor_does_not_unlock(self):
        ledger = self._pair(predecessor_status=L.BLOCKED)
        self.assertFalse(ledger.dependencies_satisfied("B"))

    def test_every_terminal_status_other_than_established_is_refused_by_default(self):
        for status in sorted(L.TERMINAL_TARGET_STATUSES - L.ESTABLISHED_TARGET_STATUSES):
            ledger = self._pair(predecessor_status=status)
            self.assertFalse(ledger.dependencies_satisfied("B"), status)

    def test_an_edge_may_explicitly_accept_a_refutation(self):
        # A redirect edge is legitimate, but it has to be written down.
        ledger = self._pair(requires=[L.REFUTED], predecessor_status=L.REFUTED)
        self.assertTrue(ledger.dependencies_satisfied("B"))

    def test_recorded_disposition_does_not_unlock_by_default(self):
        ledger = self._pair(predecessor_status=L.READY_UNDER_INTERNAL_PROTOCOL,
                            basis=L.STATUS_RECORDED)
        self.assertFalse(ledger.dependencies_satisfied("B"))

    def test_recorded_disposition_unlocks_only_when_the_edge_says_so(self):
        ledger = self._pair(predecessor_status=L.READY_UNDER_INTERNAL_PROTOCOL,
                            basis=L.STATUS_RECORDED, accept_recorded=True)
        self.assertTrue(ledger.dependencies_satisfied("B"))

    def test_unknown_required_disposition_is_refused_at_registration(self):
        ledger = L.Ledger()
        with self.assertRaises(ValueError):
            ledger.add_target(_target(id="B", depends_on=[
                L.Dependency(target_id="A", requires=["ROUND_LIMIT"])
            ]))

    def test_missing_predecessor_does_not_unlock(self):
        ledger = L.Ledger()
        ledger.add_target(_target(id="B", authorized=True,
                                  depends_on=[L.Dependency(target_id="ABSENT")]))
        self.assertFalse(ledger.dependencies_satisfied("B"))


class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.ledger = L.Ledger()
        self.ledger.add_target(_target(id="A", authorized=True))
        self.ledger.add_target(_target(id="B", authorized=True,
                                       depends_on=[L.Dependency(target_id="A")]))
        self.ledger.add_target(_target(id="C", authorized=False))

    def test_next_target_respects_dependency_order(self):
        self.assertEqual(self.ledger.next_target().id, "A")

    def test_next_target_advances_after_an_established_disposition(self):
        self.ledger.set_target_status("A", L.READY_UNDER_INTERNAL_PROTOCOL)
        self.assertEqual(self.ledger.next_target().id, "B")

    def test_next_target_does_not_advance_after_a_refutation(self):
        self.ledger.set_target_status("A", L.REFUTED)
        self.assertIsNone(self.ledger.next_target())

    def test_unauthorized_target_is_never_selected(self):
        self.ledger.set_target_status("A", L.REFUTED)
        self.assertIsNone(self.ledger.next_target())

    def test_explicit_selection_of_an_unauthorized_target_is_blocked(self):
        with self.assertRaises(PermissionError):
            self.ledger.select_target("C")

    def test_explicit_selection_with_unmet_dependencies_is_blocked(self):
        with self.assertRaises(PermissionError):
            self.ledger.select_target("B")


class CandidateRepairTests(unittest.TestCase):
    """Regression for audit finding 10: repairs produce successors, not edits."""

    def setUp(self):
        self.ledger = L.Ledger()
        self.ledger.add_target(_target(id="T-1", authorized=True,
                                       frozen_evidence_paths=["docs/a.md"]))
        self.issue = self.ledger.register_issue(target_id="T-1", claim="Too strong.",
                                                raised_by="gpt", provenance="p")

    def _candidate(self):
        return self.ledger.propose_candidate(
            predecessor_target_id="T-1",
            proposed_formulation="current, restricted to finite cases",
            changed_propositions=["P3 now carries a finiteness antecedent"],
            justification="P3 fails on the infinite corner",
            provenance="cross-audit",
            issues_addressed=[self.issue.id],
        )

    def test_candidate_does_not_mutate_the_frozen_target(self):
        before = self.ledger.targets["T-1"].current_formulation
        self._candidate()
        self.assertEqual(self.ledger.targets["T-1"].current_formulation, before)

    def test_materialising_a_candidate_creates_a_distinct_successor_target(self):
        candidate = self._candidate()
        successor = self.ledger.materialize_successor(candidate.id)
        self.assertNotEqual(successor.id, "T-1")
        self.assertEqual(successor.current_formulation, candidate.proposed_formulation)
        self.assertEqual(self.ledger.targets["T-1"].current_formulation, "current")

    def test_successor_requires_fresh_blind_passes(self):
        successor = self.ledger.materialize_successor(self._candidate().id)
        self.assertTrue(successor.requires_fresh_blind_pass)
        self.assertEqual(successor.status, L.OPEN)
        self.assertEqual(self.ledger.issues_for(successor.id), [])

    def test_successor_records_its_predecessor_and_candidate(self):
        candidate = self._candidate()
        successor = self.ledger.materialize_successor(candidate.id)
        self.assertIn(candidate.id, successor.provenance)
        self.assertIn("T-1", successor.provenance)
        self.assertEqual(candidate.successor_target_id, successor.id)

    def test_candidate_records_what_changed_and_why(self):
        candidate = self._candidate()
        self.assertTrue(candidate.changed_propositions)
        self.assertTrue(candidate.justification)
        self.assertEqual(candidate.issues_addressed, [self.issue.id])
        self.assertEqual(candidate.regression_status, "NOT_RUN")
        self.assertEqual(candidate.formal_status, "NOT_RUN")

    def test_candidate_identity_is_content_addressed(self):
        self.assertEqual(self._candidate().id, self._candidate().id)


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
            original.register_obligation(target_id="T-1", kind=L.OBLIGATION_SOURCE,
                                         statement="artifact", raised_by="gpt",
                                         provenance="p")
            original.save()

            reloaded = L.Ledger.load(path)
            self.assertEqual(original.digest(), reloaded.digest())
            self.assertEqual([i.id for i in reloaded.live_issues_for("T-1")], [live.id])
            self.assertTrue(reloaded.issues[dead.id].is_defeated())
            self.assertEqual(len(reloaded.blocking_obligations_for("T-1")), 1)
            with self.assertRaises(L.IssueReopenError):
                reloaded.apply_action(dead.id, actor="gpt", action=L.SUSTAIN, rationale="x")

    def test_typed_dependencies_survive_a_reload(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            original = L.Ledger(path)
            original.add_target(_target(id="A", status=L.REFUTED))
            original.add_target(_target(id="B", authorized=True, depends_on=[
                L.Dependency(target_id="A", requires=[L.READY_UNDER_INTERNAL_PROTOCOL])
            ]))
            original.save()
            reloaded = L.Ledger.load(path)
            self.assertFalse(reloaded.dependencies_satisfied("B"))
            self.assertEqual(reloaded.targets["B"].depends_on[0].target_id, "A")

    def test_a_foreign_schema_is_refused_rather_than_guessed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            path.write_text('{"meta": {"schema": "far-adversarial-ledger/1"}}',
                            encoding="utf-8")
            with self.assertRaises(ValueError):
                L.Ledger.load(path)

    def test_digest_ignores_wall_clock_but_not_semantics(self):
        # Replay reconstructs on a different day; timestamps cannot count.
        first = L.Ledger()
        first.add_target(_target())
        first.register_issue(target_id="T-1", claim="c", raised_by="gpt", provenance="p")
        second = L.Ledger()
        second.add_target(_target())
        second.register_issue(target_id="T-1", claim="c", raised_by="gpt", provenance="p")
        self.assertEqual(first.digest(), second.digest())
        second.register_issue(target_id="T-1", claim="d", raised_by="gpt", provenance="p")
        self.assertNotEqual(first.digest(), second.digest())


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

    def test_unknown_status_basis_is_refused(self):
        led = L.Ledger()
        with self.assertRaises(ValueError):
            led.add_target(_target(status_basis="VIBES"))

    def test_confidence_classes_are_not_collapsed(self):
        self.assertEqual(len(L.CONFIDENCE_CLASSES), 3)
        self.assertIn(L.EXACT_TRANSCRIPT_EVIDENCE, L.CONFIDENCE_CLASSES)
        self.assertIn(L.RECONSTRUCTED_RESEARCH_STATE, L.CONFIDENCE_CLASSES)
        self.assertIn(L.MISSING_TRANSCRIPT_EVIDENCE, L.CONFIDENCE_CLASSES)


if __name__ == "__main__":
    unittest.main()
