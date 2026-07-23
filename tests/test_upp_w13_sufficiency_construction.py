from __future__ import annotations
import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "theory" / "sufficiency" / "upp_sufficiency_construction_v1.py"
spec = importlib.util.spec_from_file_location("upp_sufficiency_construction_v1_test", PATH)
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

class SufficiencyConstructionTests(unittest.TestCase):
    def base(self, **changes):
        p = m.canonical_package()
        data = {field: getattr(p, field) for field in p.__dataclass_fields__}
        data.update(changes)
        return m.RCCDPackage(**data)

    def test_canonical_package_proves(self):
        self.assertEqual(m.assess(m.canonical_package()).verdict, m.Verdict.PROVED)

    def test_each_component_is_required(self):
        for component in m.COMPONENTS:
            with self.subTest(component=component):
                p = self.base(components=frozenset(set(m.COMPONENTS) - {component}))
                self.assertEqual(m.assess(p).verdict, m.Verdict.REFUTED)

    def test_each_interface_is_required(self):
        for interface in m.canonical_package().typed_interfaces:
            with self.subTest(interface=interface):
                p = self.base(typed_interfaces=frozenset(set(m.canonical_package().typed_interfaces) - {interface}))
                self.assertEqual(m.assess(p).verdict, m.Verdict.REFUTED)

    def test_all_boolean_obligations_are_required(self):
        names = [
            "effective_assembly", "closed_machinery", "total_registered_queries",
            "stable_identity", "equivalence_invariant", "round_trip_reconstruction",
            "failure_unknown_separated",
        ]
        for name in names:
            with self.subTest(name=name):
                self.assertEqual(m.assess(self.base(**{name: False})).verdict, m.Verdict.REFUTED)

    def test_each_preservation_dimension_is_required(self):
        for dimension in m.PRESERVATION_DIMENSIONS:
            with self.subTest(dimension=dimension):
                values = dict(m.canonical_package().preservation)
                values[dimension] = False
                self.assertEqual(m.assess(self.base(preservation=values)).verdict, m.Verdict.REFUTED)

    def test_unresolved_preservation_stays_unknown(self):
        values = dict(m.canonical_package().preservation)
        values["semantic"] = None
        assessment = m.assess(self.base(preservation=values))
        self.assertEqual(assessment.verdict, m.Verdict.UNKNOWN)
        self.assertIn("preservation:semantic", assessment.unresolved)

    def test_failure_dominates_unknown(self):
        values = dict(m.canonical_package().preservation)
        values["semantic"] = None
        values["historical"] = False
        self.assertEqual(m.assess(self.base(preservation=values)).verdict, m.Verdict.REFUTED)

    def test_component_order_is_irrelevant(self):
        reversed_components = frozenset(reversed(m.COMPONENTS))
        self.assertEqual(m.assess(self.base(components=reversed_components)).verdict, m.Verdict.PROVED)

    def test_anti_trivialization_registry_is_complete(self):
        self.assertEqual(len(m.ANTI_TRIVIALIZATION_CASES), 12)
        self.assertEqual(len(set(m.ANTI_TRIVIALIZATION_CASES)), 12)

if __name__ == "__main__":
    unittest.main()
