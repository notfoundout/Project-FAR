import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "theory/necessity/upp_recoverable_commitment_v1.py"
spec = importlib.util.spec_from_file_location("upp_recoverable_commitment_v1", PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

CommitmentWitness = module.CommitmentWitness
RecoverabilityPremises = module.RecoverabilityPremises
Verdict = module.Verdict
assess = module.assess_recoverable_commitment


def good_witness():
    return CommitmentWitness(
        commitment_ids=frozenset({"c1", "c2"}),
        query_to_commitment={"q1": "c1", "q2": "c2"},
        effective=True,
        total_on_registered_queries=True,
        stable_under_equivalence=True,
        distinguishes_failure_unknown=True,
    )


def premises(**changes):
    values = dict(
        in_target_class=True,
        representation_admissible=True,
        machinery_closed=True,
        full_faithfulness=True,
        commitment_equivalence_respected=True,
        witness=good_witness(),
    )
    values.update(changes)
    return RecoverabilityPremises(**values)


class RecoverableCommitmentTests(unittest.TestCase):
    def test_complete_instance_proved(self):
        self.assertEqual(assess(premises()).verdict, Verdict.PROVED)

    def test_class_failure_refutes(self):
        self.assertEqual(assess(premises(in_target_class=False)).verdict, Verdict.REFUTED)

    def test_admissibility_unknown_remains_unknown(self):
        self.assertEqual(assess(premises(representation_admissible=None)).verdict, Verdict.UNKNOWN)

    def test_hidden_machinery_refutes(self):
        self.assertEqual(assess(premises(machinery_closed=False)).verdict, Verdict.REFUTED)

    def test_faithfulness_unknown_remains_unknown(self):
        self.assertEqual(assess(premises(full_faithfulness=None)).verdict, Verdict.UNKNOWN)

    def test_equivalence_collapse_refutes(self):
        self.assertEqual(assess(premises(commitment_equivalence_respected=False)).verdict, Verdict.REFUTED)

    def test_missing_witness_unknown(self):
        result = assess(premises(witness=None))
        self.assertEqual(result.verdict, Verdict.UNKNOWN)
        self.assertIn("effective_commitment_domain", result.unresolved_obligations)

    def test_non_effective_selector_refutes(self):
        w = good_witness()
        bad = CommitmentWitness(w.commitment_ids, w.query_to_commitment, False, True, True, True)
        self.assertEqual(assess(premises(witness=bad)).verdict, Verdict.REFUTED)

    def test_partial_query_interface_refutes(self):
        w = CommitmentWitness(frozenset({"c1"}), {"q1": "missing"}, True, True, True, True)
        self.assertEqual(assess(premises(witness=w)).verdict, Verdict.REFUTED)

    def test_unstable_identity_refutes(self):
        w = good_witness()
        bad = CommitmentWitness(w.commitment_ids, w.query_to_commitment, True, True, False, True)
        self.assertEqual(assess(premises(witness=bad)).verdict, Verdict.REFUTED)

    def test_failure_unknown_merge_refutes(self):
        w = good_witness()
        bad = CommitmentWitness(w.commitment_ids, w.query_to_commitment, True, True, True, False)
        self.assertEqual(assess(premises(witness=bad)).verdict, Verdict.REFUTED)

    def test_empty_commitment_domain_refutes(self):
        w = CommitmentWitness(frozenset(), {}, True, True, True, True)
        self.assertEqual(assess(premises(witness=w)).verdict, Verdict.REFUTED)

    def test_failure_dominates_unknown(self):
        result = assess(premises(in_target_class=None, machinery_closed=False))
        self.assertEqual(result.verdict, Verdict.REFUTED)


if __name__ == "__main__":
    unittest.main()
