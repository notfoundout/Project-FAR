import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "theory/equivalence/upp_representation_equivalence_v1.py"
SPEC = importlib.util.spec_from_file_location("upp_representation_equivalence_v1", MODULE_PATH)
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)

ClosedPackage = mod.ClosedPackage
Correspondence = mod.Correspondence
Dimension = mod.Dimension
Evidence = mod.Evidence
Verdict = mod.Verdict
assess_equivalence = mod.assess_equivalence


def package(pid="L", prefix=""):
    return ClosedPackage(
        package_id=pid,
        facts=frozenset({prefix + "p", prefix + "q"}),
        transitions=frozenset({(prefix + "s0", prefix + "advance", prefix + "s1")}),
        dependencies=frozenset({(prefix + "q", prefix + "because", prefix + "p")}),
        histories=frozenset({(prefix + "s0", prefix + "s1")}),
        query_answers={prefix + "ask": prefix + "q"},
        error_answers={prefix + "bad": "Unknown"},
        identity_classes=frozenset({frozenset({prefix + "s0"}), frozenset({prefix + "s1"})}),
        machinery=frozenset({prefix + "decoder", prefix + "scheduler"}),
    )


def correspondence(source="L", target="R", sp="", tp="", total=True, effective=True):
    return Correspondence(
        source_package=source,
        target_package=target,
        fact_map={sp + "p": tp + "p", sp + "q": tp + "q"},
        state_map={sp + "s0": tp + "s0", sp + "s1": tp + "s1"},
        relation_map={sp + "advance": tp + "advance", sp + "because": tp + "because"},
        query_map={sp + "ask": tp + "ask", sp + "bad": tp + "bad"},
        machinery_map={sp + "decoder": tp + "decoder", sp + "scheduler": tp + "scheduler"},
        total_claimed=total,
        effective_claimed=effective,
    )


class EquivalenceTests(unittest.TestCase):
    def full_evidence(self):
        return Evidence(frozenset(Dimension))

    def assess(self, left=None, right=None, lr=None, rl=None, evidence=None):
        left = left or package("L")
        right = right or package("R", "x_")
        lr = lr or correspondence("L", "R", "", "x_")
        rl = rl or correspondence("R", "L", "x_", "")
        evidence = evidence or self.full_evidence()
        return assess_equivalence(left, right, lr, rl, evidence)

    def test_explicit_renaming_is_equivalent(self):
        result = self.assess()
        self.assertEqual(result.verdict, Verdict.EQUIVALENT)
        self.assertFalse(result.failures)
        self.assertFalse(result.unresolved)

    def test_one_way_map_is_unknown_not_equivalent(self):
        result = self.assess(lr=correspondence("L", "R", "", "x_", total=False))
        self.assertEqual(result.verdict, Verdict.UNKNOWN)
        self.assertIn("totality_not_established", result.unresolved)

    def test_ineffective_map_is_unknown(self):
        result = self.assess(rl=correspondence("R", "L", "x_", "", effective=False))
        self.assertEqual(result.verdict, Verdict.UNKNOWN)

    def test_dependency_difference_defeats_behavioral_equivalence(self):
        right = package("R", "x_")
        right = ClosedPackage(
            right.package_id, right.facts, right.transitions,
            frozenset({("x_q", "x_because", "x_q")}),
            right.histories, right.query_answers, right.error_answers,
            right.identity_classes, right.machinery,
        )
        result = self.assess(right=right)
        self.assertEqual(result.verdict, Verdict.NON_EQUIVALENT)
        self.assertIn("dependency_preservation_failure", result.failures)

    def test_history_difference_defeats_current_state_match(self):
        right = package("R", "x_")
        right = ClosedPackage(
            right.package_id, right.facts, right.transitions, right.dependencies,
            frozenset({("x_s1",)}), right.query_answers, right.error_answers,
            right.identity_classes, right.machinery,
        )
        result = self.assess(right=right)
        self.assertEqual(result.verdict, Verdict.NON_EQUIVALENT)
        self.assertIn("history_preservation_failure", result.failures)

    def test_error_unknown_cannot_be_collapsed(self):
        right = package("R", "x_")
        right = ClosedPackage(
            right.package_id, right.facts, right.transitions, right.dependencies,
            right.histories, right.query_answers, {"x_bad": "Fail"},
            right.identity_classes, right.machinery,
        )
        result = self.assess(right=right)
        self.assertEqual(result.verdict, Verdict.NON_EQUIVALENT)
        self.assertIn("error_unknown_preservation_failure", result.failures)

    def test_identity_collapse_is_rejected(self):
        right = package("R", "x_")
        right = ClosedPackage(
            right.package_id, right.facts, right.transitions, right.dependencies,
            right.histories, right.query_answers, right.error_answers,
            frozenset({frozenset({"x_s0", "x_s1"})}), right.machinery,
        )
        result = self.assess(right=right)
        self.assertEqual(result.verdict, Verdict.NON_EQUIVALENT)
        self.assertIn("identity_preservation_failure", result.failures)

    def test_hidden_machinery_difference_is_rejected(self):
        right = package("R", "x_")
        right = ClosedPackage(
            right.package_id, right.facts, right.transitions, right.dependencies,
            right.histories, right.query_answers, right.error_answers,
            right.identity_classes, frozenset({"x_decoder", "x_scheduler", "x_oracle"}),
        )
        result = self.assess(right=right)
        self.assertEqual(result.verdict, Verdict.NON_EQUIVALENT)
        self.assertIn("machinery_preservation_failure", result.failures)

    def test_noninjective_fact_map_is_rejected(self):
        lr = correspondence("L", "R", "", "x_")
        lr = Correspondence(
            lr.source_package, lr.target_package,
            {"p": "x_p", "q": "x_p"}, lr.state_map, lr.relation_map,
            lr.query_map, lr.machinery_map, True, True,
        )
        result = self.assess(lr=lr)
        self.assertEqual(result.verdict, Verdict.NON_EQUIVALENT)
        self.assertIn("fact_map_noninjective", result.failures)

    def test_round_trip_failure_is_rejected(self):
        rl = correspondence("R", "L", "x_", "")
        rl = Correspondence(
            rl.source_package, rl.target_package,
            {"x_p": "q", "x_q": "p"}, rl.state_map, rl.relation_map,
            rl.query_map, rl.machinery_map, True, True,
        )
        result = self.assess(rl=rl)
        self.assertEqual(result.verdict, Verdict.NON_EQUIVALENT)
        self.assertIn("fact_round_trip_failure", result.failures)

    def test_unresolved_dimension_yields_unknown(self):
        checked = frozenset(d for d in Dimension if d is not Dimension.HISTORY)
        result = self.assess(evidence=Evidence(checked, frozenset({Dimension.HISTORY})))
        self.assertEqual(result.verdict, Verdict.UNKNOWN)
        self.assertTrue(any(x.startswith("unresolved_dimensions:") for x in result.unresolved))

    def test_unaddressed_dimension_yields_unknown(self):
        checked = frozenset(d for d in Dimension if d is not Dimension.SEMANTICS)
        result = self.assess(evidence=Evidence(checked))
        self.assertEqual(result.verdict, Verdict.UNKNOWN)
        self.assertTrue(any(x.startswith("unaddressed_dimensions:") for x in result.unresolved))

    def test_endpoint_mismatch_is_rejected(self):
        lr = correspondence("WRONG", "R", "", "x_")
        result = self.assess(lr=lr)
        self.assertEqual(result.verdict, Verdict.NON_EQUIVALENT)
        self.assertIn("left_to_right_endpoint_mismatch", result.failures)

    def test_invalid_empty_package_is_rejected(self):
        left = package("", "")
        result = self.assess(left=left)
        self.assertEqual(result.verdict, Verdict.NON_EQUIVALENT)
        self.assertIn("package_id_empty", result.failures)


if __name__ == "__main__":
    unittest.main()
