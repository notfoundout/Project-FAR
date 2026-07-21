from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from s_core_w3_reference import construct_witness, semantic_agreement, validate_package, verify_witness, W3Error
from s_core_w4_negative_controls import CONTROL_IDS, CONTROL_SPEC, apply_control, evaluate_control, run_suite, suite_passes

FIXTURE = ROOT / "theory/evaluation/s-core-w3-reference-fixtures.json"


def load_source() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["source"]


class W4NegativeControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = load_source()
        self.package = construct_witness(self.source)

    def test_baseline_is_accepted(self) -> None:
        self.assertTrue(verify_witness(self.source, self.package))

    def test_all_ten_controls_are_present(self) -> None:
        self.assertEqual(CONTROL_IDS, tuple(f"NC-{index:02d}" for index in range(1, 11)))
        self.assertEqual(set(CONTROL_IDS), set(CONTROL_SPEC))

    def test_full_suite_rejects_every_control(self) -> None:
        results = run_suite(self.source)
        self.assertEqual(len(results), 10)
        self.assertTrue(all(item["status"] == "rejected_expected_reason" for item in results))
        self.assertTrue(suite_passes(self.source))

    def test_control_diagnostics_are_frozen(self) -> None:
        for control_id in CONTROL_IDS:
            result = evaluate_control(control_id, self.source, self.package)
            self.assertEqual(result["diagnostic"], CONTROL_SPEC[control_id]["diagnostic"])
            self.assertEqual(result["violated_clauses"], CONTROL_SPEC[control_id]["violated_clauses"])

    def test_nc01_lookup_table_loses_process(self) -> None:
        mutated = apply_control("NC-01", self.source, self.package)
        self.assertTrue(mutated["A"]["Sigma"])
        self.assertEqual(mutated["A"]["Theta"], [])
        self.assertEqual(mutated["A"]["H"]["events"], [])
        self.assertFalse(verify_witness(self.source, mutated))

    def test_nc02_dependency_collapse_merges_roles(self) -> None:
        mutated = apply_control("NC-02", self.source, self.package)
        support = mutated["W"]["E"]["occ:p4:support"]
        defeat = mutated["W"]["E"]["occ:p4:defeat"]
        roles = {occurrence: role for occurrence, role in mutated["A"]["R"]["occurrence_role"]}
        self.assertEqual(roles[support], roles[defeat])
        self.assertFalse(verify_witness(self.source, mutated))

    def test_nc03_history_erasure_retains_states(self) -> None:
        mutated = apply_control("NC-03", self.source, self.package)
        self.assertEqual(mutated["A"]["Sigma"], self.package["A"]["Sigma"])
        self.assertEqual(mutated["A"]["H"]["revisions"], [])
        self.assertEqual(mutated["A"]["H"]["modifications"], [])
        self.assertFalse(verify_witness(self.source, mutated))

    def test_nc04_hidden_rule_override_is_rejected_by_ledger(self) -> None:
        mutated = apply_control("NC-04", self.source, self.package)
        self.assertIn("undeclared_rule_override", mutated["control_environment"])
        with self.assertRaises(W3Error):
            validate_package(mutated)

    def test_nc05_label_only_semantics_fails_semantic_agreement(self) -> None:
        mutated = apply_control("NC-05", self.source, self.package)
        self.assertFalse(semantic_agreement(self.source, mutated))
        self.assertFalse(verify_witness(self.source, mutated))

    def test_nc06_unrestricted_interpreter_is_rejected(self) -> None:
        mutated = apply_control("NC-06", self.source, self.package)
        self.assertEqual(mutated["W"]["kappa"]["external_dependencies"], ["unrestricted-general-interpreter"])
        with self.assertRaises(W3Error):
            validate_package(mutated)

    def test_nc07_hidden_auxiliary_state_does_not_rescue_witness(self) -> None:
        mutated = apply_control("NC-07", self.source, self.package)
        self.assertTrue(mutated["hidden_auxiliary_state"]["removed_occurrence_role"])
        self.assertFalse(verify_witness(self.source, mutated))

    def test_nc08_provenance_deletion_is_rejected(self) -> None:
        mutated = apply_control("NC-08", self.source, self.package)
        self.assertEqual(mutated["A"]["Prov"], [])
        self.assertEqual(mutated["A"]["H"]["provenance"], [])
        self.assertFalse(verify_witness(self.source, mutated))

    def test_nc09_output_equivalent_process_substitution_is_rejected(self) -> None:
        mutated = apply_control("NC-09", self.source, self.package)
        self.assertEqual(
            [(item["from"], item["to"]) for item in mutated["A"]["Theta"]],
            [(item["from"], item["to"]) for item in self.package["A"]["Theta"]],
        )
        self.assertTrue(mutated["process_substitution"]["same_transition_endpoints"])
        self.assertFalse(verify_witness(self.source, mutated))

    def test_nc10_smuggled_interpretation_is_counted_and_rejected(self) -> None:
        mutated = apply_control("NC-10", self.source, self.package)
        self.assertEqual(mutated["A"]["I"], [])
        self.assertTrue(mutated["W"]["M"]["smuggled_interpretation"])
        self.assertFalse(verify_witness(self.source, mutated))

    def test_controls_do_not_mutate_baseline(self) -> None:
        original = copy.deepcopy(self.package)
        for control_id in CONTROL_IDS:
            apply_control(control_id, self.source, self.package)
        self.assertEqual(self.package, original)


if __name__ == "__main__":
    unittest.main()
