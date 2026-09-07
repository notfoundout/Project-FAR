import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MEMORY_PATH = ROOT / "research/registry/project-memory-v1.0.json"


class ProjectMemoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memory = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))

    def test_memory_is_explicitly_non_authoritative(self):
        self.assertEqual(
            "navigation_and_planning_only_not_theory_or_evidence_authority",
            self.memory["authority"],
        )
        self.assertIn("override", self.memory["canonical_resolution_rule"].lower())
        self.assertIn("theory authority", self.memory["nonclaims"])

    def test_epistemic_calibration_preserves_required_boundaries(self):
        calibration = self.memory["epistemic_calibration"]
        self.assertEqual("unresolved", calibration["integrated_methodology_novelty"])
        self.assertEqual("unestablished", calibration["external_real_world_utility"])
        self.assertEqual("unestablished", calibration["commercial_value"])
        self.assertEqual(
            "I1_claimed_isolation_only_not_I2_or_I3",
            calibration["w1_independence"],
        )
        self.assertEqual(
            "bounded_internal_controlled_artifact_semantic_detection_conformance",
            calibration["w6_evidence_class"],
        )

    def test_efr_registration_is_preserved(self):
        efr = self.memory["external_program"]
        self.assertEqual("EXTERNAL-FALSIFICATION-AND-REPLICATION-001", efr["program_id"])
        self.assertEqual("PREREGISTERED_NOT_EXECUTED", efr["status"])
        self.assertTrue(efr["not_w7"])
        self.assertTrue(efr["registration_must_not_be_rewritten_by_this_memory"])
        self.assertTrue(
            efr["all_registered_components_still_required_for_aggregate_external_effectiveness_label"]
        )

    def test_supporting_artifacts_exist(self):
        for relative in self.memory["supporting_artifacts"]:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_claim_guardrails_reject_novelty_and_product_overclaim(self):
        guardrails = " ".join(self.memory["claim_language_guardrails"]).lower()
        self.assertIn("do not describe project far as newly discovered foundational mathematics", guardrails)
        self.assertIn("do not infer novelty", guardrails)
        self.assertIn("commercial value", guardrails)


if __name__ == "__main__":
    unittest.main()
