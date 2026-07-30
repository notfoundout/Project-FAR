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


class EvidenceAuthorityResearchExecutionTests(unittest.TestCase):
    def test_research_candidate_and_all_preregistered_negative_controls(self):
        result = validator.run_full_validation(enforce_research_only_placement=True)
        print("BEGIN_EVIDENCE_AUTHORITY_VALIDATION")
        print(json.dumps(result, indent=2, sort_keys=True))
        print("END_EVIDENCE_AUTHORITY_VALIDATION")
        self.assertEqual("pass", result["overall"], result["errors"])
        self.assertTrue(result["all_negative_controls_detected"])
        self.assertGreaterEqual(result["negative_control_count"], 20)

        validation = result["positive_validation"]
        self.assertEqual(51, validation["proof_path_count"])
        inventory = validation["proof_inventory"]
        expected = {
            "theory/evaluation/fara-canonical-kernel-proof-v1.0.json",
            "theory/proofs/P-001-first-propositions.md",
            "mechanization/lean/UPPSemanticKernel.lean",
            "mechanization/lean/G2OpenWorldLowerBound.lean",
            "mechanization/lean/G3EpistemicMaximality.lean",
            "theory/proof-objects/T-015.proof.yaml",
        }
        self.assertTrue(expected <= set(inventory), sorted(expected - set(inventory)))
        self.assertIn(
            "object_valued_paths",
            inventory["theory/evaluation/fara-canonical-kernel-proof-v1.0.json"],
        )
        self.assertIn(
            "proposition_metadata",
            inventory["theory/proofs/P-001-first-propositions.md"],
        )
        self.assertIn(
            "terminal_entrypoints",
            inventory["mechanization/lean/UPPSemanticKernel.lean"],
        )


if __name__ == "__main__":
    unittest.main()
