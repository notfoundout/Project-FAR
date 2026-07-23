import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "theory/representations/upp_representation_universe_v1.py"
SPEC = importlib.util.spec_from_file_location("upp_representation_test", PATH)
MODEL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODEL
SPEC.loader.exec_module(MODEL)


class RepresentationUniverseTests(unittest.TestCase):
    def candidate(self, **changes):
        values = dict(
            identifier="r",
            family=MODEL.EncodingFamily.SYMBOLIC,
            finite_description=True,
            effective_construction=True,
            effective_use=True,
            support_inventory_complete=True,
            declared_support=frozenset({MODEL.SupportKind.DECODER}),
            total_registered_query_interface=True,
            stable_identity_conditions=True,
        )
        values.update(changes)
        return MODEL.RepresentationCandidate(**values)

    def test_complete_candidate_is_admissible(self):
        self.assertEqual(MODEL.classify(self.candidate()), MODEL.Verdict.ADMISSIBLE)

    def test_each_false_criterion_is_inadmissible(self):
        for field in ("finite_description", "effective_construction", "effective_use", "support_inventory_complete", "total_registered_query_interface", "stable_identity_conditions"):
            with self.subTest(field=field):
                self.assertEqual(MODEL.classify(self.candidate(**{field: False})), MODEL.Verdict.INADMISSIBLE)

    def test_each_unresolved_criterion_is_unknown(self):
        for field in ("finite_description", "effective_construction", "effective_use", "support_inventory_complete", "total_registered_query_interface", "stable_identity_conditions"):
            with self.subTest(field=field):
                self.assertEqual(MODEL.classify(self.candidate(**{field: None})), MODEL.Verdict.UNKNOWN)

    def test_oracle_cannot_be_declared_effective(self):
        with self.assertRaises(ValueError):
            MODEL.classify(self.candidate(declared_support=frozenset({MODEL.SupportKind.ORACLE})))

    def test_medium_invariance(self):
        a = self.candidate(identifier="a", family=MODEL.EncodingFamily.SYMBOLIC)
        b = self.candidate(identifier="b", family=MODEL.EncodingFamily.DISTRIBUTED)
        self.assertTrue(MODEL.is_medium_invariant(a, b))

    def test_kernel_language_rejected(self):
        for term in MODEL.FORBIDDEN_KERNEL_TERMS:
            self.assertFalse(MODEL.text_is_kernel_neutral(f"criterion requires {term}"))

    def test_neutral_language_allowed(self):
        self.assertTrue(MODEL.text_is_kernel_neutral("all support procedures are inventoried"))


if __name__ == "__main__":
    unittest.main()
