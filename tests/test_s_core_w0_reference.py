from __future__ import annotations

import json
from pathlib import Path
import unittest

from tools.s_core_w0_reference import AXES, FiniteSourceContract, transport_set

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "theory/evaluation/s-core-w0-reference-fixtures.json"


class SCoreW0ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cls.by_id = {item["id"]: item for item in cls.data["fixtures"]}

    def test_fixture_schema_and_axis_set(self) -> None:
        self.assertEqual(self.data["schema_version"], "1.0")
        self.assertEqual(self.data["fixture_set_id"], "SCORE-W0-FIXTURES-001")
        self.assertEqual(AXES, ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8I"))

    def test_closure_is_complete_and_cycles_terminate(self) -> None:
        fixture = self.by_id["W0-FX-001"]
        contract = FiniteSourceContract.from_dict(fixture["contract"])
        self.assertEqual(contract.closure(), frozenset(fixture["expected_closure"]))
        self.assertEqual(contract.applicable_axes(), tuple(fixture["expected_applicable_axes"]))
        self.assertIn("h0", contract.reference_map()["p0"])
        self.assertIn("p0", contract.reference_map()["h0"])

    def test_sparse_axes_are_decidably_inapplicable(self) -> None:
        fixture = self.by_id["W0-FX-002"]
        contract = FiniteSourceContract.from_dict(fixture["contract"])
        self.assertEqual(contract.closure(), frozenset(fixture["expected_closure"]))
        self.assertEqual(contract.applicable_axes(), tuple(fixture["expected_applicable_axes"]))
        self.assertEqual(contract.reduct_nodes("P7"), frozenset())
        self.assertEqual(contract.reduct_nodes("P8I"), frozenset())

    def test_canonical_code_is_invariant_under_sort_preserving_renaming(self) -> None:
        for fixture in self.data["fixtures"]:
            contract = FiniteSourceContract.from_dict(fixture["contract"])
            renamed = contract.renamed(fixture["renaming"])
            self.assertEqual(contract.canonical_code(), renamed.canonical_code(), fixture["id"])

    def test_reduct_extraction_commutes_with_renaming(self) -> None:
        for fixture in self.data["fixtures"]:
            contract = FiniteSourceContract.from_dict(fixture["contract"])
            mapping = fixture["renaming"]
            renamed = contract.renamed(mapping)
            for axis in AXES:
                self.assertEqual(
                    transport_set(contract.reduct_nodes(axis), mapping),
                    renamed.reduct_nodes(axis),
                    f"{fixture['id']} {axis}",
                )

    def test_axis_reducts_are_closed_under_references(self) -> None:
        for fixture in self.data["fixtures"]:
            contract = FiniteSourceContract.from_dict(fixture["contract"])
            references = contract.reference_map()
            for axis in AXES:
                reduct = contract.reduct_nodes(axis)
                for node in reduct:
                    self.assertTrue(set(references.get(node, ())) <= set(reduct))

    def test_undeclared_reference_is_rejected(self) -> None:
        fixture = next(item for item in self.data["negative_fixtures"] if item["id"] == "W0-NF-001")
        with self.assertRaisesRegex(ValueError, fixture["expected_error"]):
            FiniteSourceContract.from_dict(fixture["contract"])

    def test_sort_changing_renaming_is_rejected(self) -> None:
        fixture = next(item for item in self.data["negative_fixtures"] if item["id"] == "W0-NF-002")
        base = FiniteSourceContract.from_dict(self.by_id[fixture["base_fixture"]]["contract"])
        with self.assertRaisesRegex(ValueError, fixture["expected_error"]):
            base.renamed(fixture["renaming"])


if __name__ == "__main__":
    unittest.main()
