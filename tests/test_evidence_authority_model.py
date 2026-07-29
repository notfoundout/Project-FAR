import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "docs/governance/evidence-authority-model.md"
REGISTRY_PATH = ROOT / "docs/governance/evidence-authority-registry.json"


class EvidenceAuthorityModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = MODEL_PATH.read_text()
        cls.registry = json.loads(REGISTRY_PATH.read_text())

    def test_model_and_registry_are_accepted_governance_artifacts(self):
        self.assertIn("Status: **Accepted governance specification**", self.model)
        self.assertEqual(
            "Accepted governance registry",
            self.registry["status"],
        )

    def test_registry_points_to_existing_canonical_owners(self):
        for domain in self.registry["domains"].values():
            owner = domain.get("owner")
            if owner:
                self.assertTrue((ROOT / owner).is_file(), owner)

    def test_authority_classes_are_closed(self):
        allowed = {
            "governance_decision",
            "canonical_specification",
            "proof_record",
            "status_register",
            "research_record",
            "methodological_specification",
            "index",
            "historical_record",
        }
        declared = {
            domain["authority_class"]
            for domain in self.registry["domains"].values()
        }
        self.assertTrue(declared <= allowed)

    def test_every_domain_has_nonclaim_boundaries(self):
        for name, domain in self.registry["domains"].items():
            self.assertTrue(domain.get("may_establish"), name)
            self.assertTrue(domain.get("may_not_establish"), name)

    def test_indexes_cannot_claim_truth_or_acceptance(self):
        index = self.registry["domains"]["repository_navigation"]
        forbidden = set(index["may_not_establish"])
        self.assertIn("claim truth", forbidden)
        self.assertIn("proof", forbidden)
        self.assertIn("acceptance", forbidden)

    def test_research_cannot_promote_itself(self):
        research = self.registry["domains"]["research_observations"]
        forbidden = set(research["may_not_establish"])
        self.assertIn("canonical theory", forbidden)
        self.assertIn("acceptance", forbidden)
        self.assertIn("promotion", forbidden)

    def test_methodology_cannot_claim_logical_derivation(self):
        methodology = self.registry["domains"]["methodology"]
        self.assertIn(
            "logical derivation from FARA",
            methodology["may_not_establish"],
        )

    def test_promotion_gate_is_complete(self):
        requirements = set(self.registry["promotion_requirements"])
        expected = {
            "separate governance decision",
            "exact artifact and version",
            "promoted propositions and scope",
            "required proof or evidence",
            "limitations and counterexamples",
            "status-register update",
            "canonical-map update",
            "semantic and dependency validation",
        }
        self.assertEqual(expected, requirements)

    def test_forbidden_inferences_include_ci_and_self_promotion(self):
        forbidden = set(self.registry["forbidden_inferences"])
        self.assertIn("CI success implies truth", forbidden)
        self.assertIn("artifact self-promotion", forbidden)
        self.assertIn("formal notation implies proof", forbidden)

    def test_model_preserves_unresolved_dependency_status(self):
        self.assertIn(
            "does not settle those dependencies",
            self.model,
        )
        self.assertIn(
            "No experiment may resume",
            self.model,
        )


if __name__ == "__main__":
    unittest.main()
