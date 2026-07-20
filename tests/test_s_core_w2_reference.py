from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from tools.s_core_w2_reference import (
    SCHEMA, W2Error, check_dynamics, check_history, check_w2, construct_target,
    live_target_transitions, validate_source,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "theory/evaluation/s-core-w2-reference-fixtures.json"


class SCoreW2ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cls.by_id = {item["id"]: item for item in cls.data["fixtures"]}

    def test_fixture_schema(self) -> None:
        self.assertEqual(self.data["schema_version"], "1.0")
        self.assertEqual(self.data["fixture_set_id"], "SCORE-W2-FIXTURES-001")

    def test_all_fixtures_construct_and_verify(self) -> None:
        for fixture in self.data["fixtures"]:
            target, witness = construct_target(fixture["source"])
            self.assertEqual(target["schema"], SCHEMA)
            self.assertTrue(check_w2(fixture["source"], target, witness), fixture["id"])

    def test_deterministic_transition_reflection_and_superseded_exclusion(self) -> None:
        source = self.by_id["W2-FX-001"]["source"]
        target, witness = construct_target(source)
        live_ids = {item["source_key"] for item in live_target_transitions(target)}
        self.assertEqual(live_ids, {"t0", "t1", "t2"})
        mutated = copy.deepcopy(target)
        mutated["Theta"].append(copy.deepcopy(mutated["Theta"][0]))
        mutated["Theta"][-1]["id"] = "transition:spurious"
        mutated["Theta"][-1]["source_key"] = "spurious"
        self.assertFalse(check_dynamics(source, mutated, witness))

    def test_probabilistic_kernel_weights_are_exact(self) -> None:
        source = self.by_id["W2-FX-002"]["source"]
        target, witness = construct_target(source)
        weights = sorted(item["weight"] for item in live_target_transitions(target))
        self.assertEqual(weights, ["1/3", "2/3"])
        mutated = copy.deepcopy(target)
        next(item for item in mutated["Theta"] if item["source_key"] == "p2")["weight"] = "1/3"
        self.assertFalse(check_dynamics(source, mutated, witness))

    def test_history_order_reflection_rejects_added_or_removed_pair(self) -> None:
        source = self.by_id["W2-FX-001"]["source"]
        target, witness = construct_target(source)
        removed = copy.deepcopy(target)
        removed["H"]["order"].pop()
        self.assertFalse(check_history(source, removed, witness))
        added = copy.deepcopy(target)
        e0 = witness["event_map"]["e0"]
        e3 = witness["event_map"]["e3"]
        added["H"]["order"].append([e3, e0])
        self.assertFalse(check_history(source, added, witness))

    def test_revision_changes_state_snapshot(self) -> None:
        source = self.by_id["W2-FX-001"]["source"]
        target, witness = construct_target(source)
        s1 = witness["state_map"]["s1"]
        mutated = copy.deepcopy(target)
        next(item for item in mutated["Sigma"] if item["id"] == s1)["commitments"]["c1"] = "accepted"
        self.assertFalse(check_dynamics(source, mutated, witness))

    def test_self_modification_is_operational_not_label_only(self) -> None:
        source = self.by_id["W2-FX-001"]["source"]
        target, witness = construct_target(source)
        s2 = witness["state_map"]["s2"]
        mutated = copy.deepcopy(target)
        next(item for item in mutated["Sigma"] if item["id"] == s2)["active_rule_versions"] = [witness["version_map"]["R1@v1"]]
        live_ids = {item["source_key"] for item in live_target_transitions(mutated)}
        self.assertNotIn("t2", live_ids)
        self.assertFalse(check_dynamics(source, mutated, witness))

    def test_rejected_modification_preserves_active_versions(self) -> None:
        source = self.by_id["W2-FX-002"]["source"]
        target, witness = construct_target(source)
        self.assertTrue(check_history(source, target, witness))
        record = target["H"]["modifications"][0]
        self.assertEqual(record["decision"], "rejected")
        self.assertEqual(record["deactivates"], [])
        self.assertEqual(record["activates"], [])

    def test_path_condition_is_retained(self) -> None:
        source = self.by_id["W2-FX-001"]["source"]
        target, witness = construct_target(source)
        self.assertEqual(len(target["H"]["path_conditions"]), 1)
        mutated = copy.deepcopy(target)
        mutated["H"]["path_conditions"] = []
        self.assertFalse(check_history(source, mutated, witness))

    def test_negative_fixtures_are_rejected(self) -> None:
        for negative in self.data["negative_fixtures"]:
            source = copy.deepcopy(self.by_id[negative["base_fixture"]]["source"])
            transition = next(item for item in source["transitions"] if item["id"] == negative["mutation"]["transition"])
            transition[negative["mutation"]["field"]] = negative["mutation"]["value"]
            with self.assertRaisesRegex(W2Error, negative["expected_error"]):
                validate_source(source)

    def test_rule_version_change_cannot_be_erased_from_history(self) -> None:
        source = self.by_id["W2-FX-001"]["source"]
        target, witness = construct_target(source)
        mutated = copy.deepcopy(target)
        mutated["H"]["modifications"][0]["activates"] = []
        self.assertFalse(check_history(source, mutated, witness))


if __name__ == "__main__":
    unittest.main()
