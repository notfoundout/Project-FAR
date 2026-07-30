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
    def test_frozen_candidate_and_mutation_campaign(self):
        result = validator.run_full_validation(enforce_research_only_placement=True)
        print("BEGIN_EVIDENCE_AUTHORITY_PRIMARY")
        print(json.dumps(result, indent=2, sort_keys=True))
        print("END_EVIDENCE_AUTHORITY_PRIMARY")
        self.assertEqual("pass", result["overall"], result["errors"])
        self.assertTrue(result["all_negative_controls_detected"])
        self.assertGreaterEqual(result["negative_control_count"], 24)
        validation = result["positive_validation"]
        self.assertEqual(
            "787d8776f0aab7c78cea9d536762c323b62d8c37",
            validation["frozen_base_commit"],
        )
        self.assertGreaterEqual(validation["proof_path_count"], 52)
        inventory = validation["proof_inventory"]
        expected = {
            "theory/theorems/propositions.md",
            "theory/evaluation/fara-canonical-kernel-proof-v1.0.json",
            "mechanization/lean/UPPSemanticKernel.lean",
            "theory/proof-objects/T-015.proof.yaml",
        }
        self.assertTrue(expected <= set(inventory), sorted(expected - set(inventory)))
        self.assertEqual("Unknown", validation["conflict_probe"]["result"])
        self.assertTrue(validation["activation_manifest_probe"]["valid"])
        self.assertRegex(result["evidence_digest"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
