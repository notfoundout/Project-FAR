from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "theory" / "irreducibility" / "upp_irreducibility_maximality_v1.py"
spec = importlib.util.spec_from_file_location("upp_w14", PATH)
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


class TestUPPW14(unittest.TestCase):
    def test_canonical_ledger_proves_relative_result(self):
        ledger = m.canonical_ledger()
        self.assertEqual(m.validate_ledger(ledger), ())
        self.assertEqual(m.irreducibility_verdict(ledger), m.Verdict.PROVED)
        self.assertEqual(m.maximality_verdict(ledger), m.Verdict.PROVED)
        self.assertEqual(m.aggregate_verdict(ledger), m.Verdict.PROVED)

    def test_all_proper_component_subsets_registered(self):
        self.assertEqual(len(m.proper_component_subsets()), 31)
        self.assertNotIn(frozenset(m.COMPONENTS), m.proper_component_subsets())

    def test_valid_reduction_refutes_irreducibility(self):
        ledger = m.canonical_ledger()
        valid = m.ReductionCandidate("valid-reduction", frozenset(), frozenset(m.PRESERVATION_DIMENSIONS), frozenset(m.REDUCTION_REQUIREMENTS), True, True, True)
        mutated = m.SearchLedger(ledger.reduction_candidates + (valid,), ledger.extension_challenges, True, True, True, True)
        self.assertEqual(m.irreducibility_verdict(mutated), m.Verdict.REFUTED)

    def test_unresolved_reduction_keeps_unknown(self):
        ledger = m.canonical_ledger()
        unknown = m.ReductionCandidate("unknown-reduction", frozenset(), frozenset(m.PRESERVATION_DIMENSIONS), frozenset(m.REDUCTION_REQUIREMENTS), True, True, True, unresolved_facts=("equivalence_unresolved",))
        mutated = m.SearchLedger(ledger.reduction_candidates + (unknown,), ledger.extension_challenges, True, True, True, True)
        self.assertEqual(m.irreducibility_verdict(mutated), m.Verdict.UNKNOWN)

    def test_hidden_machinery_reduction_fails(self):
        c = m.ReductionCandidate("hidden", frozenset(), frozenset(m.PRESERVATION_DIMENSIONS), frozenset(m.REDUCTION_REQUIREMENTS) - {"machinery_closed"}, True, True, True)
        self.assertEqual(m.reduction_verdict(c), m.Verdict.REFUTED)

    def test_circular_reduction_fails(self):
        c = m.ReductionCandidate("circular", frozenset(), frozenset(m.PRESERVATION_DIMENSIONS), frozenset(m.REDUCTION_REQUIREMENTS) - {"non_circular"}, True, True, True)
        self.assertEqual(m.reduction_verdict(c), m.Verdict.REFUTED)

    def test_information_loss_fails(self):
        c = m.ReductionCandidate("lossy", frozenset(), frozenset(m.PRESERVATION_DIMENSIONS) - {"information"}, frozenset(m.REDUCTION_REQUIREMENTS), True, True, True)
        self.assertEqual(m.reduction_verdict(c), m.Verdict.REFUTED)

    def test_cost_shift_fails(self):
        c = m.ReductionCandidate("cost-shift", frozenset(), frozenset(m.PRESERVATION_DIMENSIONS), frozenset(m.REDUCTION_REQUIREMENTS), True, True, False)
        self.assertEqual(m.reduction_verdict(c), m.Verdict.REFUTED)

    def test_in_class_nonembedding_refutes_maximality(self):
        ledger = m.canonical_ledger()
        bad = m.ExtensionChallenge("novel", frozenset(m.MAXIMALITY_REQUIREMENTS), True, False, frozenset(m.PRESERVATION_DIMENSIONS))
        mutated = m.SearchLedger(ledger.reduction_candidates, ledger.extension_challenges + (bad,), True, True, True, True)
        self.assertEqual(m.maximality_verdict(mutated), m.Verdict.REFUTED)

    def test_unresolved_extension_keeps_unknown(self):
        ledger = m.canonical_ledger()
        u = m.ExtensionChallenge("unresolved", frozenset(m.MAXIMALITY_REQUIREMENTS), None, None, frozenset(), unresolved_facts=("membership_unresolved",))
        mutated = m.SearchLedger(ledger.reduction_candidates, ledger.extension_challenges + (u,), True, True, True, True)
        self.assertEqual(m.maximality_verdict(mutated), m.Verdict.UNKNOWN)

    def test_out_of_class_challenge_is_not_counterexample(self):
        c = m.ExtensionChallenge("outside", frozenset(m.MAXIMALITY_REQUIREMENTS), False, False, frozenset())
        self.assertEqual(m.challenge_verdict(c), m.Verdict.PROVED)

    def test_duplicate_ids_invalidate_ledger(self):
        ledger = m.canonical_ledger()
        duplicate = ledger.reduction_candidates[0]
        mutated = m.SearchLedger(ledger.reduction_candidates + (duplicate,), ledger.extension_challenges, True, True, False, True)
        self.assertIn("duplicate_reduction_candidate_identity", m.validate_ledger(mutated))

    def test_unfrozen_space_is_unknown(self):
        ledger = m.canonical_ledger()
        mutated = m.SearchLedger(ledger.reduction_candidates, ledger.extension_challenges, False, False, True, True)
        self.assertEqual(m.aggregate_verdict(mutated), m.Verdict.UNKNOWN)


if __name__ == "__main__":
    unittest.main()
