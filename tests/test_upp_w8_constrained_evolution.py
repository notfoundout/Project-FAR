from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "theory/necessity/upp_w8_constrained_evolution_v1.py"
spec = importlib.util.spec_from_file_location("upp_w8_model", MODEL_PATH)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

Truth = mod.Truth
Verdict = mod.Verdict
EvolutionTransition = mod.EvolutionTransition
EvolutionAssessment = mod.EvolutionAssessment
assess = mod.assess_constrained_evolution
construct = mod.construct_admissibility_relation
witness = mod.theorem_witness_exists


def transition(name: str, admissible: Truth, **changes):
    data = dict(
        transition_id=name,
        before_commitments=("p",),
        after_commitments=(name,),
        history_prefix=("h0",),
        admissible=admissible,
        governing_constraints=("consistency",),
        reason_recoverable=Truth.YES,
        equivalence_stable=Truth.YES,
        machinery_charged=Truth.YES,
    )
    data.update(changes)
    return EvolutionTransition(**data)


def base(**changes):
    data = dict(
        target_class_member=Truth.YES,
        representation_admissible=Truth.YES,
        machinery_closed=Truth.YES,
        fully_faithful=Truth.YES,
        equivalence_preserved=Truth.YES,
        transitions=(transition("allow", Truth.YES), transition("deny", Truth.NO)),
        registered_query_total=Truth.YES,
        failure_unknown_separated=Truth.YES,
    )
    data.update(changes)
    return EvolutionAssessment(**data)


class ConstrainedEvolutionTests(unittest.TestCase):
    def test_positive_witness(self):
        assessment = base()
        self.assertEqual(assess(assessment), Verdict.PROVED)
        self.assertTrue(witness(assessment))

    def test_unknown_premise_remains_unknown(self):
        self.assertEqual(assess(base(fully_faithful=Truth.UNKNOWN)), Verdict.UNKNOWN)

    def test_failed_premise_refutes_relative_application(self):
        self.assertEqual(assess(base(machinery_closed=Truth.NO)), Verdict.REFUTED)

    def test_no_commitment_change_is_not_a_witness(self):
        static = transition("static", Truth.YES, after_commitments=("p",))
        self.assertEqual(assess(base(transitions=(static,))), Verdict.UNKNOWN)

    def test_always_true_relation_is_trivialized(self):
        self.assertEqual(
            assess(base(transitions=(transition("a", Truth.YES), transition("b", Truth.YES)))),
            Verdict.REFUTED,
        )

    def test_always_false_relation_is_trivialized(self):
        self.assertEqual(
            assess(base(transitions=(transition("a", Truth.NO), transition("b", Truth.NO)))),
            Verdict.REFUTED,
        )

    def test_unknown_admissibility_is_not_failure(self):
        self.assertEqual(
            assess(base(transitions=(transition("a", Truth.YES), transition("b", Truth.UNKNOWN)))),
            Verdict.UNKNOWN,
        )

    def test_hidden_policy_machinery_refutes(self):
        hidden = transition("deny", Truth.NO, machinery_charged=Truth.NO)
        self.assertEqual(assess(base(transitions=(transition("allow", Truth.YES), hidden))), Verdict.REFUTED)

    def test_unrecoverable_reason_refutes(self):
        bad = transition("deny", Truth.NO, reason_recoverable=Truth.NO)
        self.assertEqual(assess(base(transitions=(transition("allow", Truth.YES), bad))), Verdict.REFUTED)

    def test_representation_dependent_verdict_refutes(self):
        bad = transition("deny", Truth.NO, equivalence_stable=Truth.NO)
        self.assertEqual(assess(base(transitions=(transition("allow", Truth.YES), bad))), Verdict.REFUTED)

    def test_history_erasure_refutes(self):
        bad = transition("deny", Truth.NO, history_prefix=())
        self.assertEqual(assess(base(transitions=(transition("allow", Truth.YES), bad))), Verdict.REFUTED)

    def test_missing_constraint_refutes(self):
        bad = transition("deny", Truth.NO, governing_constraints=())
        self.assertEqual(assess(base(transitions=(transition("allow", Truth.YES), bad))), Verdict.REFUTED)

    def test_inconsistent_duplicate_relation_rejected(self):
        a = transition("a", Truth.YES)
        b = transition("b", Truth.NO, before_commitments=a.before_commitments, after_commitments=a.after_commitments, history_prefix=a.history_prefix)
        with self.assertRaises(ValueError):
            construct((a, b))

    def test_failure_unknown_collapse_refutes(self):
        self.assertEqual(assess(base(failure_unknown_separated=Truth.NO)), Verdict.REFUTED)


if __name__ == "__main__":
    unittest.main()
