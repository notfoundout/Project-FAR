from __future__ import annotations

import copy
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

    def test_protocol_base_schema_and_verifier_are_exactly_frozen(self) -> None:
        self.assertEqual(W6.verify_protocol_base_dependencies(), [])

    def test_registered_w4_corpus_projection_is_exactly_protocol_base(self) -> None:
        manifest = json.loads(W6.W4_MANIFEST.read_text(encoding="utf-8"))
        W6.validate_registered_corpus_manifest(manifest)
        broken = copy.deepcopy(manifest)
        broken["records"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "record projection drifted"):
            W6.validate_registered_corpus_manifest(broken)
        broken = copy.deepcopy(manifest)
        broken["protocol_commit"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "metadata drift"):
            W6.validate_registered_corpus_manifest(broken)

    def test_registered_mutation_is_schema_valid_but_semantically_detected_in_every_domain(self) -> None:
        groups = W6._record_groups()
        for domain in W6.EXPECTED_DOMAINS:
            with self.subTest(domain=domain):
                clean = json.loads(groups[domain]["repaired"].read_text(encoding="utf-8"))
                mutant = W6.inject_registered_collision(clean)

                self.assertFalse(W6.oracle_has_material_collision(clean))
                self.assertTrue(W6.oracle_has_material_collision(mutant))
                self.assertTrue(W6._schema_valid(mutant))
                audit = W6.validate_contract(mutant)
                codes = {diagnostic.code for diagnostic in audit.diagnostics}
                self.assertFalse(audit.success)
                self.assertIn("FACTORIZATION_FAILURE", codes)
                self.assertNotIn("FREEZE_HASH_MISMATCH", codes)

                for key, value in clean.items():
                    if key not in {"contract", "freeze"}:
                        self.assertEqual(mutant[key], value)
                for key, value in clean["contract"].items():
                    if key != "representation":
                        self.assertEqual(mutant["contract"][key], value)
                for key, value in clean["freeze"].items():
                    if key != "contract_sha256":
                        self.assertEqual(mutant["freeze"][key], value)

    def test_oracle_fails_closed_on_ambiguous_duplicate_case_ids(self) -> None:
        groups = W6._record_groups()
        document = json.loads(groups["formal-logic"]["repaired"].read_text(encoding="utf-8"))
        document["contract"]["source_domain"]["cases"][1]["id"] = document["contract"]["source_domain"]["cases"][0]["id"]
        with self.assertRaisesRegex(ValueError, "duplicate case ids"):
            W6.oracle_has_material_collision(document)

    def test_secondary_native_lossy_controls(self) -> None:
        result = W6.compute_results()
        self.assertEqual(result["secondary"]["native_lossy_controls_detected"], "6/6")
        self.assertEqual(result["secondary"]["registered_control_claim"], "PROVED")

    def test_oracle_is_independent_of_far_verifier_and_report(self) -> None:
        source = inspect.getsource(W6.oracle_has_material_collision)
        self.assertNotIn("validate_contract", source)
        self.assertNotIn("report", source)
        self.assertNotIn("evidence", source)

    def test_manifest_is_exact_hash_bound_and_fail_closed(self) -> None:
        manifest = json.loads(W6.MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(W6.manifest_errors(manifest), [])
        self.assertEqual(W6.verify_manifest(), [])

        missing = copy.deepcopy(manifest)
        missing["artifacts"] = missing["artifacts"][:-1]
        errors = W6.manifest_errors(missing)
        self.assertTrue(any("artifact set/order mismatch" in error for error in errors))

        extra = copy.deepcopy(manifest)
        extra["artifacts"].append({"path": "README.md", "sha256": "0" * 64})
        errors = W6.manifest_errors(extra)
        self.assertTrue(any("artifact set/order mismatch" in error for error in errors))

        wrong_hash = copy.deepcopy(manifest)
        wrong_hash["artifacts"][0]["sha256"] = "0" * 64
        errors = W6.manifest_errors(wrong_hash)
        self.assertTrue(any("hash mismatch" in error for error in errors))

        malformed = copy.deepcopy(manifest)
        malformed["artifacts"][0]["unexpected"] = True
        errors = W6.manifest_errors(malformed)
        self.assertTrue(any("must contain only path and sha256" in error for error in errors))

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
