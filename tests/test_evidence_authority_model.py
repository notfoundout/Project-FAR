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

    def test_model_and_registry_remain_inactive_research_candidates(self):
        self.assertIn(
            "Status: **Research candidate; not Accepted or Promoted**",
            self.model,
        )
        self.assertEqual(
            "Research candidate; not Accepted or Promoted",
            self.registry["status"],
        )
        self.assertFalse(self.registry["active"])
        self.assertEqual("Research", self.registry["lifecycle_state"])

    def test_registry_points_to_existing_fixed_owners(self):
        for domain in self.registry["domains"].values():
            owner = domain.get("owner")
            if owner:
                self.assertTrue((ROOT / owner).is_file(), owner)
            proposed_owner = domain.get("proposed_owner")
            if proposed_owner:
                self.assertTrue((ROOT / proposed_owner).is_file(), proposed_owner)

    def test_all_authority_classes_have_permitted_statuses(self):
        allowed = set(self.registry["permitted_statuses_by_class"])
        declared = {
            domain["authority_class"]
            for domain in self.registry["domains"].values()
        }
        self.assertEqual(declared, allowed - {"historical_record"})
        for authority_class, statuses in self.registry[
            "permitted_statuses_by_class"
        ].items():
            self.assertTrue(statuses, authority_class)
            self.assertNotIn("Unknown", statuses)
            self.assertNotIn("Provisional", statuses)

    def test_every_domain_has_scope_and_nonclaim_boundaries(self):
        for name, domain in self.registry["domains"].items():
            self.assertTrue(domain.get("proposition_scope"), name)
            self.assertTrue(domain.get("may_establish"), name)
            self.assertTrue(domain.get("may_not_establish"), name)

    def test_bootstrap_is_external_unknown_and_hash_locked(self):
        bootstrap = self.registry["bootstrap"]
        self.assertEqual("Unknown", bootstrap["status"])
        self.assertIsNone(bootstrap["selected_owner"])
        self.assertTrue(
            bootstrap["selection_must_be_preregistered_and_hash_locked"]
        )
        self.assertIn("predates this model", bootstrap["required_authority"])
        self.assertIn("bootstrap status is `Unknown`", self.model)

    def test_governance_owner_is_candidate_not_active(self):
        governance = self.registry["domains"]["governance_decisions"]
        self.assertEqual("governance_decision", governance["authority_class"])
        self.assertEqual("docs/DECISION_LOG.md", governance["proposed_owner"])
        self.assertEqual(
            "candidate_inactive_until_external_bootstrap",
            governance["owner_state"],
        )
        self.assertIn("self-acceptance", governance["may_not_establish"])
        self.assertIn("self-promotion", governance["may_not_establish"])

    def test_proof_records_have_a_distinct_owner_domain(self):
        proofs = self.registry["domains"]["proof_records"]
        status = self.registry["domains"]["theorem_and_proof_status"]
        self.assertEqual("proof_record", proofs["authority_class"])
        self.assertIn("proof", proofs["owner_pattern"])
        self.assertEqual("status_register", status["authority_class"])
        self.assertNotEqual(proofs["authority_class"], status["authority_class"])

    def test_definition_scopes_are_split_explicitly(self):
        terminology = self.registry["domains"]["canonical_terminology"]
        definitions = self.registry["domains"]["detailed_definitions"]
        self.assertEqual(
            "docs/glossary/canonical-terminology.md", terminology["owner"]
        )
        self.assertEqual(
            "theory/definitions/definitions.md", definitions["owner"]
        )
        self.assertIn(
            "detailed formal definitions", terminology["may_not_establish"]
        )
        self.assertIn("canonical naming overrides", definitions["may_not_establish"])

    def test_research_and_methodology_claim_boundaries(self):
        research = self.registry["domains"]["research_observations"]
        methodology = self.registry["domains"]["methodology"]
        self.assertIn("acceptance", research["may_not_establish"])
        self.assertIn("promotion", research["may_not_establish"])
        self.assertIn(
            "logical derivation from FARA", methodology["may_not_establish"]
        )

    def test_promotion_requires_independent_bootstrap_and_full_lifecycle(self):
        requirements = set(self.registry["promotion_requirements"])
        required = {
            "separate preregistered lifecycle",
            "pre-existing independent bootstrap authority",
            "bootstrap authority hash lock",
            "exact artifact and version",
            "replication record",
            "acceptance record",
            "promotion record",
            "semantic and dependency validation",
        }
        self.assertTrue(required <= requirements)

    def test_forbidden_inferences_block_self_activation_and_experiment_power(self):
        forbidden = set(self.registry["forbidden_inferences"])
        required = {
            "CI success implies truth",
            "artifact self-promotion",
            "candidate owner implies active owner",
            "research candidate implies acceptance",
            "research candidate authorizes experiment execution",
            "research candidate prohibits experiment execution",
        }
        self.assertTrue(required <= forbidden)

    def test_experiment_consequence_is_explicitly_post_promotion(self):
        self.assertIn("## Proposed consequence after promotion", self.model)
        self.assertIn(
            "This Research candidate itself neither authorizes nor prohibits the next experiment",
            self.model,
        )
        self.assertNotIn("## Consequence for the next experiment", self.model)


if __name__ == "__main__":
    unittest.main()
