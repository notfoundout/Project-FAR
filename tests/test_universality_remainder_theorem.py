from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.check_universality_remainder_theorem import validate_registry


REGISTRY_PATH = Path("theory/evaluation/universality-remainder-theorem-v1.0.json")


class UniversalityRemainderTheoremTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_frozen_registry_passes(self) -> None:
        self.assertEqual(validate_registry(self.registry), [])

    def test_missing_obligation_fails(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["obligations"] = mutated["obligations"][:-1]
        self.assertIn("obligation set changed", validate_registry(mutated))

    def test_unknown_cannot_be_prejudged(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["obligations"][0]["initial_status"] = "satisfied"
        self.assertIn("G1 must begin unresolved", validate_registry(mutated))

    def test_predecessor_history_is_immutable(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["frozen_predecessors"]["terminal_adjudication"] = 295
        self.assertIn("frozen predecessor map changed", validate_registry(mutated))

    def test_finite_search_nonclaim_is_required(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["global_nonclaims"].remove("open_world_maximality_from_finite_search")
        self.assertIn("required global nonclaims missing", validate_registry(mutated))

    def test_successor_order_is_frozen(self) -> None:
        mutated = copy.deepcopy(self.registry)
        mutated["successor_order"] = ["G2", "G1", "G3_and_terminal_adjudication"]
        self.assertIn("successor order changed", validate_registry(mutated))


if __name__ == "__main__":
    unittest.main()
