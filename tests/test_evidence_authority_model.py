import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "research/evidence-authority-model/validate_candidate.py"
SENTINEL = "theory/evaluation/fara-operator-w2-proof-v1.0.json"

spec = importlib.util.spec_from_file_location("evidence_authority_validator", VALIDATOR)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class EvidenceAuthorityPrimaryExecutionTests(unittest.TestCase):
    def test_canonical_id_proof_schema_campaign(self):
        result = validator.run_full_validation(enforce_research_only_placement=True)
        validation = result["positive_validation"]
        synthetic = validator.v1.synthetic_activation_manifest(validation["proof_inventory"])
        summary = {
            "overall": result["overall"],
            "errors": result["errors"],
            "evidence_digest": result["evidence_digest"],
            "negative_control_count": result["negative_control_count"],
            "all_negative_controls_detected": result["all_negative_controls_detected"],
            "control_ids": [item["control_id"] for item in result["negative_controls"]],
            "proof_path_count": validation["proof_path_count"],
            "frozen_base_commit": validation["frozen_base_commit"],
            "frozen_tree_sha": validation["frozen_tree_sha"],
            "discovery_input_count": validation["discovery_input_count"],
            "discovery_input_digest": validation["discovery_input_digest"],
            "canonical_id_sentinel_pathways": validation["proof_inventory"].get(SENTINEL),
            "unequal_priority_probe": validation["unequal_priority_probe"],
            "conflict_probe": validation["conflict_probe"],
            "activation_manifest_probe": validation["activation_manifest_probe"],
            "synthetic_decision_record_count": len(synthetic["decision_records"]),
        }
        print("BEGIN_EVIDENCE_AUTHORITY_PRIMARY_V3")
        print(json.dumps(summary, sort_keys=True))
        print("END_EVIDENCE_AUTHORITY_PRIMARY_V3")
        self.assertEqual("pass", result["overall"], result["errors"])
        self.assertEqual([], result["errors"])
        self.assertTrue(result["all_negative_controls_detected"])
        self.assertEqual(41, result["negative_control_count"])
        self.assertEqual(53, validation["proof_path_count"])
        self.assertEqual(372, validation["discovery_input_count"])
        self.assertIn(SENTINEL, validation["proof_inventory"])
        self.assertIn("self_registering_records", validation["proof_inventory"][SENTINEL])
        self.assertEqual("Affirmed", validation["unequal_priority_probe"]["result"])
        self.assertEqual(1, validation["unequal_priority_probe"]["selected_numeric_priority"])
        self.assertEqual("Unknown", validation["conflict_probe"]["result"])
        self.assertTrue(validation["activation_manifest_probe"]["valid"])
        self.assertEqual(53, validation["activation_manifest_probe"]["entry_count"])
        self.assertEqual(54, len(synthetic["decision_records"]))
        self.assertIn(
            "disable_canonical_id_proof_record_schema",
            summary["control_ids"],
        )
        self.assertRegex(result["evidence_digest"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
