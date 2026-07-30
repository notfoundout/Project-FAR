import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "research/evidence-authority-model/validate_candidate.py"

spec = importlib.util.spec_from_file_location("evidence_authority_validator", VALIDATOR)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class EvidenceAuthorityPrimaryExecutionTests(unittest.TestCase):
    def test_revised_candidate_and_provenance_mutations(self):
        result = validator.run_full_validation(enforce_research_only_placement=True)
        validation = result["positive_validation"]
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
            "unequal_priority_probe": validation["unequal_priority_probe"],
            "conflict_probe": validation["conflict_probe"],
            "activation_manifest_probe": validation["activation_manifest_probe"],
        }
        print("BEGIN_EVIDENCE_AUTHORITY_PRIMARY_V2")
        print(json.dumps(summary, sort_keys=True))
        print("END_EVIDENCE_AUTHORITY_PRIMARY_V2")
        self.assertEqual("pass", result["overall"], result["errors"])
        self.assertEqual([], result["errors"])
        self.assertTrue(result["all_negative_controls_detected"])
        self.assertEqual(40, result["negative_control_count"])
        self.assertEqual(52, validation["proof_path_count"])
        self.assertEqual(372, validation["discovery_input_count"])
        self.assertEqual("Affirmed", validation["unequal_priority_probe"]["result"])
        self.assertEqual(1, validation["unequal_priority_probe"]["selected_numeric_priority"])
        self.assertEqual("Unknown", validation["conflict_probe"]["result"])
        self.assertTrue(validation["activation_manifest_probe"]["valid"])
        self.assertEqual(52, validation["activation_manifest_probe"]["entry_count"])
        self.assertRegex(result["evidence_digest"], r"^[0-9a-f]{64}$")
        required_controls = {
            "omit_manifest_decision_decision_date",
            "omit_manifest_decision_supporting_evidence",
            "omit_manifest_decision_scope",
            "omit_manifest_decision_limitations",
            "omit_artifact_status_decision_decision_date",
            "omit_artifact_status_decision_supporting_evidence",
            "omit_artifact_status_decision_scope",
            "omit_artifact_status_decision_limitations",
        }
        self.assertTrue(required_controls <= set(summary["control_ids"]))


if __name__ == "__main__":
    unittest.main()
