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

    def test_model_and_registry_remain_research_candidates(self):
        self.assertIn(
            "Status: **Research candidate; not Accepted or Promoted**",
            self.model,
        )
        self.assertEqual(
            "Research candidate; not Accepted or Promoted",
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

    def test_governance_decision_authority_is_registered(self):
        governance = self.registry["domains"]["governance_decisions"]
        self.assertEqual("governance_decision", governance["authority_class"])
        self.assertEqual("docs/DECISION_LOG.md", governance["owner"])
        self.assertIn("acceptance", governance["may_establish"])
        self.assertIn("promotion", governance["may_establish"])

    def test_governance_decisions_cannot_prove_truth_or_self_promote(self):
        governance = self.registry["domains"]["governance_decisions"]
        forbidden = set(governance["may_not_establish"])
        self.assertIn("theorem truth", forbidden)
        self.assertIn("empirical truth", forbidden)
        self.assertIn("self-acceptance", forbidden)
        self.assertIn("self-promotion", forbidden)

    def test_promotion_gate_requires_full_lifecycle(self):
        requirements = set(self.registry["promotion_requirements"])
        expected = {
            "separate preregistered lifecycle",
            "independent governance decision",
            "exact artifact and version",
            "promoted propositions and scope",
            "required proof or evidence",
            "replication record",
            "acceptance record",
            "promotion record",
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
        self.assertIn("research candidate implies acceptance", forbidden)

    def test_model_preserves_unresolved_dependency_status(self):
        self.assertIn(
            "does not settle those dependencies or activate the gate by itself",
            self.model,
        )
        self.assertIn(
            "No experiment may resume",
            self.model,
        )


if __name__ == "__main__":
    unittest.main()
