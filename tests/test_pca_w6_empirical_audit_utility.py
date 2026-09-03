from __future__ import annotations

import importlib.util
import inspect
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/check_pca_w6_empirical_audit_utility.py"
SPEC = importlib.util.spec_from_file_location("pca_w6_audit_utility", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
W6 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(W6)


class PCAW6AuditUtilityTests(unittest.TestCase):
    def test_recorded_result_recomputes_exactly(self) -> None:
        recorded = json.loads(W6.RESULT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(recorded, W6.compute_results())

    def test_primary_registered_endpoint(self) -> None:
        result = W6.compute_results()
        self.assertEqual(result["primary"]["schema_only_baseline"]["sensitivity"], "0/6")
        self.assertEqual(result["primary"]["schema_only_baseline"]["specificity"], "6/6")
        self.assertEqual(result["primary"]["far_semantic_audit"]["sensitivity"], "6/6")
        self.assertEqual(result["primary"]["far_semantic_audit"]["specificity"], "6/6")
        self.assertEqual(result["primary"]["audit_oracle_agreement"], "12/12")
        self.assertEqual(result["primary"]["registered_all_items_claim"], "PROVED")

    def test_registered_mutation_is_schema_valid_but_semantically_detected(self) -> None:
        path = ROOT / "research/results/pca-w4-domain-contracts/formal-logic-repaired.json"
        clean = json.loads(path.read_text(encoding="utf-8"))
        mutant = W6.inject_registered_collision(clean)
        self.assertFalse(W6.oracle_has_material_collision(clean))
        self.assertTrue(W6.oracle_has_material_collision(mutant))
        self.assertTrue(W6._schema_valid(mutant))
        audit = W6.validate_contract(mutant)
        self.assertFalse(audit.success)
        self.assertIn("FACTORIZATION_FAILURE", {diagnostic.code for diagnostic in audit.diagnostics})
        self.assertNotIn("FREEZE_HASH_MISMATCH", {diagnostic.code for diagnostic in audit.diagnostics})

    def test_secondary_native_lossy_controls(self) -> None:
        result = W6.compute_results()
        self.assertEqual(result["secondary"]["native_lossy_controls_detected"], "6/6")
        self.assertEqual(result["secondary"]["registered_control_claim"], "PROVED")

    def test_oracle_is_independent_of_far_verifier_and_report(self) -> None:
        source = inspect.getsource(W6.oracle_has_material_collision)
        self.assertNotIn("validate_contract", source)
        self.assertNotIn("report", source)
        self.assertNotIn("evidence", source)

    def test_scope_boundaries_are_machine_recorded(self) -> None:
        result = W6.compute_results()
        self.assertFalse(result["analysis_policy"]["population_inference"])
        self.assertFalse(result["independence"]["external_investigator"])
        self.assertFalse(result["independence"]["human_participants"])
        self.assertFalse(result["independence"]["human_disagreement_tested"])
        self.assertEqual(result["terminal"]["bounded_material_loss_detection"], "PROVED")
        self.assertEqual(result["terminal"]["human_disagreement_reduction"], "UNDERDETERMINED")
        self.assertEqual(result["terminal"]["external_real_world_utility"], "OPEN")
        self.assertEqual(result["terminal"]["core_theory_impact"], "NONE")


if __name__ == "__main__":
    unittest.main()
