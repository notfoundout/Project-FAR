import fnmatch
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "docs/governance/evidence-authority-model.md"
REGISTRY_PATH = ROOT / "docs/governance/evidence-authority-registry.json"
PROOF_STATUS_MANIFEST_PATH = ROOT / "docs/governance/proof-artifact-status-manifest.json"
DEPENDENCY_REGISTRY_PATH = ROOT / "theory/dependencies/dependency-registry.yaml"
THEOREM_METADATA_PATH = ROOT / "theory/metadata/theorems.yaml"
PROOF_METADATA_ROOTS = (
    ROOT / "foundations",
    ROOT / "theory",
    ROOT / "docs/governance",
    ROOT / "research",
    ROOT / "mechanization",
)


def iter_registered_proof_paths(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if isinstance(child, str) and (
                key == "proof_object" or key.endswith("_proof_artifact")
            ):
                yield child
            yield from iter_registered_proof_paths(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_registered_proof_paths(child)


def iter_dependency_yaml_proof_paths(text):
    current_source = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("- id:"):
            current_source = None
            continue
        source_match = re.fullmatch(r"source:\s*(\S+)", line)
        if source_match:
            current_source = source_match.group(1)
            continue
        type_match = re.fullmatch(r"source_type:\s*(\S+)", line)
        if type_match and type_match.group(1) == "proof_object":
            if current_source is None:
                raise AssertionError("proof_object source_type without source")
            yield current_source


def iter_theorem_yaml_proof_paths(text):
    for raw_line in text.splitlines():
        match = re.fullmatch(r"\s*proof:\s*(\S+)\s*", raw_line)
        if match:
            yield match.group(1)


def matches_owner_pattern(path, owner_pattern):
    return any(
        fnmatch.fnmatchcase(path, pattern)
        for pattern in owner_pattern.split("|")
    )


def iter_valid_json_payloads():
    for metadata_root in PROOF_METADATA_ROOTS:
        if not metadata_root.exists():
            continue
        for json_path in metadata_root.rglob("*.json"):
            if json_path == PROOF_STATUS_MANIFEST_PATH:
                continue
            try:
                yield json_path, json.loads(json_path.read_text())
            except json.JSONDecodeError:
                # Some repository fixtures intentionally use malformed JSON to
                # test validators. They are not admissible proof metadata.
                continue


def registered_proof_paths():
    paths = set()
    for _, payload in iter_valid_json_payloads():
        paths.update(iter_registered_proof_paths(payload))
    paths.update(
        iter_dependency_yaml_proof_paths(DEPENDENCY_REGISTRY_PATH.read_text())
    )
    paths.update(iter_theorem_yaml_proof_paths(THEOREM_METADATA_PATH.read_text()))
    return paths


class EvidenceAuthorityModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = MODEL_PATH.read_text()
        cls.registry = json.loads(REGISTRY_PATH.read_text())
        cls.proof_manifest = json.loads(PROOF_STATUS_MANIFEST_PATH.read_text())

    def test_model_and_registry_remain_inactive_research_candidates(self):
        taxonomy = set(self.registry["artifact_status_taxonomy"])
        self.assertIn("Status: **Research**", self.model)
        self.assertIn("Candidacy: **Inactive candidate**", self.model)
        self.assertIn("Promotion completed: **No**", self.model)
        self.assertEqual("Research", self.registry["status"])
        self.assertIn(self.registry["status"], taxonomy)
        self.assertEqual("inactive_candidate", self.registry["candidacy"])
        self.assertFalse(self.registry["promotion_completed"])
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

    def test_authority_contract_registers_itself_without_self_acceptance(self):
        model_domain = self.registry["domains"]["authority_model_specification"]
        registry_domain = self.registry["domains"]["authority_registry_specification"]
        self.assertEqual(
            "docs/governance/evidence-authority-model.md", model_domain["owner"]
        )
        self.assertEqual(
            "docs/governance/evidence-authority-registry.json",
            registry_domain["owner"],
        )
        for domain in (model_domain, registry_domain):
            self.assertEqual("canonical_specification", domain["authority_class"])
            self.assertEqual("Research", domain["current_status"])
            self.assertEqual("Accepted", domain["required_status_for_activation"])
            self.assertIn("self-acceptance", domain["may_not_establish"])
        self.assertIn(
            "authority model and authority registry separately transitioned to Accepted by independent governance",
            self.registry["activation_requirements"],
        )

    def test_status_taxonomy_matches_charter(self):
        expected = {"Accepted", "Research", "Provisional", "Archive", "Unknown"}
        self.assertEqual(expected, set(self.registry["artifact_status_taxonomy"]))
        self.assertIn(self.registry["status"], expected)
        permitted = self.registry["permitted_statuses_by_class"]
        for authority_class, statuses in permitted.items():
            self.assertTrue(statuses, authority_class)
            self.assertTrue(set(statuses) <= expected, authority_class)
            self.assertNotIn("Promoted", statuses)
            self.assertNotIn("Superseded", statuses)
        self.assertEqual(["Archive"], permitted["historical_record"])

    def test_all_authority_classes_have_domains_and_permitted_statuses(self):
        permitted = set(self.registry["permitted_statuses_by_class"])
        declared = {
            domain["authority_class"]
            for domain in self.registry["domains"].values()
        }
        self.assertEqual(declared, permitted)

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

    def test_proof_records_cover_every_registered_proof_artifact(self):
        proofs = self.registry["domains"]["proof_records"]
        status = self.registry["domains"]["theorem_and_proof_status"]
        self.assertEqual("proof_record", proofs["authority_class"])
        self.assertEqual("status_register", status["authority_class"])
        self.assertNotEqual(proofs["authority_class"], status["authority_class"])

        paths = registered_proof_paths()
        self.assertTrue(paths, "no registered proof artifacts discovered")
        self.assertIn(
            "mechanization/lean/FARCanonicalCountermodel.lean",
            paths,
        )
        self.assertIn("theory/proof-objects/T-001.proof.yaml", paths)
        self.assertIn("theory/proof-objects/T-005.proof.yaml", paths)
        self.assertIn("theory/proofs/T-001-primitive-minimality.md", paths)
        self.assertIn("theory/proofs/T-015-explicit-reasoning-meta-theorem.md", paths)
        for proof_path in sorted(paths):
            self.assertTrue((ROOT / proof_path).is_file(), proof_path)
            self.assertTrue(
                matches_owner_pattern(proof_path, proofs["owner_pattern"]),
                proof_path,
            )

    def test_proof_status_manifest_has_registered_owner_and_is_inactive(self):
        manifest_domain = self.registry["domains"]["proof_artifact_status_manifest"]
        self.assertEqual(
            "docs/governance/proof-artifact-status-manifest.json",
            manifest_domain["owner"],
        )
        self.assertEqual("status_register", manifest_domain["authority_class"])
        self.assertEqual("Research", manifest_domain["current_status"])
        self.assertEqual("Accepted", manifest_domain["required_status_for_activation"])
        self.assertFalse(self.proof_manifest["active"])
        self.assertEqual("Research", self.proof_manifest["status"])
        self.assertEqual([], self.proof_manifest["entries"])
        self.assertIn("self-acceptance", manifest_domain["may_not_establish"])

    def test_proof_status_policy_preserves_non_authoritative_artifacts(self):
        proofs = self.registry["domains"]["proof_records"]
        policy = proofs["status_policy"]
        taxonomy = set(self.registry["artifact_status_taxonomy"])
        requirements = set(self.registry["activation_requirements"])

        self.assertTrue(policy["manifest_required_for_activation"])
        self.assertTrue(policy["exactly_one_status_per_registered_artifact"])
        self.assertTrue(policy["authority_bearing_designation_required"])
        self.assertTrue(policy["validate_status_against_artifact_status_taxonomy"])
        self.assertTrue(
            policy["non_authority_bearing_artifacts_may_retain_nonaccepted_charter_statuses"]
        )
        self.assertTrue(
            policy["non_authority_bearing_artifacts_excluded_from_active_proof_authority"]
        )
        self.assertEqual("Unknown", policy["missing_or_undeclared_status"])
        self.assertEqual(
            "Accepted", policy["required_status_for_authority_bearing_artifact"]
        )
        self.assertIn(policy["missing_or_undeclared_status"], taxonomy)
        self.assertIn(
            policy["required_status_for_authority_bearing_artifact"], taxonomy
        )
        self.assertIn(
            "every proof artifact designated authority-bearing has status Accepted",
            requirements,
        )
        self.assertIn(
            "every proof artifact not designated authority-bearing is excluded from active proof authority",
            requirements,
        )
        self.assertIn(
            "registered proof implies authority-bearing proof",
            self.registry["forbidden_inferences"],
        )
        self.assertIn(
            "Only proof artifacts designated authority-bearing must have status `Accepted`",
            self.model,
        )

    def test_definition_scopes_and_status_transition_are_explicit(self):
        terminology = self.registry["domains"]["canonical_terminology"]
        definitions = self.registry["domains"]["detailed_definitions"]
        self.assertEqual(
            "docs/glossary/canonical-terminology.md", terminology["owner"]
        )
        self.assertEqual(
            "theory/definitions/definitions.md", definitions["owner"]
        )
        self.assertEqual("Unknown", definitions["current_status"])
        self.assertEqual("Accepted", definitions["required_status_for_activation"])
        self.assertIn(
            "owner status transitions completed",
            self.registry["promotion_requirements"],
        )
        self.assertIn(
            "detailed formal definitions", terminology["may_not_establish"]
        )
        self.assertIn("canonical naming overrides", definitions["may_not_establish"])

    def test_historical_records_have_archive_owner_and_no_active_authority(self):
        historical = self.registry["domains"]["historical_records"]
        self.assertEqual("archive/**", historical["owner_pattern"])
        self.assertEqual("historical_record", historical["authority_class"])
        self.assertIn("active canonical authority", historical["may_not_establish"])

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
            "authority model status transition completed",
            "authority registry status transition completed",
            "owner status transitions completed",
            "proof artifact status manifest completed and Accepted",
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
            "lifecycle promotion implies artifact status Promoted",
            "proof owner pattern implies Accepted proof status",
            "registered proof implies authority-bearing proof",
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
