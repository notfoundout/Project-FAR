import fnmatch
import hashlib
import json
import pathlib
import re
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "docs/governance/evidence-authority-model.md"
REGISTRY_PATH = ROOT / "docs/governance/evidence-authority-registry.json"
PROOF_STATUS_MANIFEST_PATH = ROOT / "docs/governance/proof-artifact-status-manifest.json"
QUESTION_PATH = ROOT / "research/evidence-authority-model/question-v1.0.md"
EXECUTION_SPEC_PATH = ROOT / "research/evidence-authority-model/execution-spec-v1.0.json"
EXECUTION_PATH = ROOT / "research/evidence-authority-model/execution-v1.0.json"
OBSERVATION_PATH = ROOT / "research/evidence-authority-model/observation-v1.0.json"
RESULT_PATH = ROOT / "research/evidence-authority-model/result-v1.0.json"
REPLICATION_PATH = ROOT / "research/evidence-authority-model/replication-v1.0.json"
REPORT_PATH = ROOT / "research/evidence-authority-model/report-v1.0.md"
DEPENDENCY_REGISTRY_PATH = ROOT / "theory/dependencies/dependency-registry.yaml"
THEOREM_METADATA_PATH = ROOT / "theory/metadata/theorems.yaml"
LEMMA_METADATA_PATH = ROOT / "theory/metadata/lemmas.yaml"
VERIFY_THEORY_PATH = ROOT / "tools/verify_theory.py"
PROOF_METADATA_ROOTS = (
    ROOT / "foundations",
    ROOT / "theory",
    ROOT / "docs/governance",
    ROOT / "research",
    ROOT / "mechanization",
)
PATH_KEYS = {
    "proof",
    "proof_object",
    "proof_artifact",
    "source_proof",
    "lean_file",
    "proof_registry",
}
PATH_KEY_SUFFIXES = ("_proof_artifact", "_proof_registry")
PROOF_EXTENSIONS = (".md", ".json", ".yaml", ".yml", ".lean")
EXPECTED_SPEC_SHA256 = "5328b419dd8ef86e77852730f3b2d3b6a1b6f6440bea92a55ff537db2f72bc2a"


def relative(path):
    return path.relative_to(ROOT).as_posix()


def git_blob_sha(path):
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode()
    return hashlib.sha1(header + content).hexdigest()


def load_yaml(path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def is_existing_repo_artifact(value):
    if not isinstance(value, str):
        return False
    if value.startswith(("http://", "https://")) or " " in value:
        return False
    if not value.endswith(PROOF_EXTENSIONS):
        return False
    candidate = ROOT / value
    return candidate.is_file()


def iter_path_values(value):
    if isinstance(value, str):
        if is_existing_repo_artifact(value):
            yield value
    elif isinstance(value, list):
        for child in value:
            yield from iter_path_values(child)


def iter_registered_proof_paths(value, source_path=None):
    if isinstance(value, dict):
        if source_path is not None and isinstance(value.get("proof_id"), str):
            yield relative(source_path)
        for key, child in value.items():
            key_is_path = key in PATH_KEYS or key.endswith(PATH_KEY_SUFFIXES)
            if key == "source_artifact" and isinstance(value.get("proof_id"), str):
                key_is_path = True
            if key_is_path:
                yield from iter_path_values(child)
            yield from iter_registered_proof_paths(child, source_path)
    elif isinstance(value, list):
        for child in value:
            yield from iter_registered_proof_paths(child, source_path)


def iter_structured_metadata():
    for metadata_root in PROOF_METADATA_ROOTS:
        if not metadata_root.exists():
            continue
        for path in metadata_root.rglob("*"):
            if not path.is_file() or path == PROOF_STATUS_MANIFEST_PATH:
                continue
            if "fixtures" in path.parts or "__pycache__" in path.parts:
                continue
            try:
                if path.suffix == ".json":
                    yield path, json.loads(path.read_text(encoding="utf-8"))
                elif path.suffix in {".yaml", ".yml"}:
                    yield path, load_yaml(path)
            except (json.JSONDecodeError, yaml.YAMLError, UnicodeDecodeError):
                # Malformed validation fixtures are not admissible metadata.
                continue


def verifier_required_proof_objects():
    text = VERIFY_THEORY_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"REQUIRED_PROOF_OBJECT_THEOREMS\s*=\s*\{(?P<body>.*?)\n\}",
        text,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("verify_theory.py proof-object requirement set not found")
    theorem_ids = set(re.findall(r'"(T-\d{3})"', match.group("body")))
    return {f"theory/proof-objects/{theorem_id}.proof.yaml" for theorem_id in theorem_ids}


def theorem_proof_paths():
    data = load_yaml(THEOREM_METADATA_PATH)
    return {item["proof"] for item in data["theorems"]}


def lemma_proof_paths():
    data = load_yaml(LEMMA_METADATA_PATH)
    return {item["source"] for item in data["lemmas"]}


def dependency_proof_paths():
    data = load_yaml(DEPENDENCY_REGISTRY_PATH)
    return {
        item["source"]
        for item in data["dependencies"]
        if item.get("source_type") == "proof_object"
    }


def registered_proof_paths():
    paths = set()
    paths.update(theorem_proof_paths())
    paths.update(lemma_proof_paths())
    paths.update(dependency_proof_paths())
    paths.update(verifier_required_proof_objects())
    for source_path, payload in iter_structured_metadata():
        paths.update(iter_registered_proof_paths(payload, source_path))
    return paths


def matches_owner_pattern(path, owner_pattern):
    return any(
        fnmatch.fnmatchcase(path, pattern)
        for pattern in owner_pattern.split("|")
    )


class EvidenceAuthorityModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = MODEL_PATH.read_text(encoding="utf-8")
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        cls.proof_manifest = json.loads(
            PROOF_STATUS_MANIFEST_PATH.read_text(encoding="utf-8")
        )
        cls.execution_spec = json.loads(EXECUTION_SPEC_PATH.read_text(encoding="utf-8"))
        cls.execution = json.loads(EXECUTION_PATH.read_text(encoding="utf-8"))
        cls.observation = json.loads(OBSERVATION_PATH.read_text(encoding="utf-8"))
        cls.result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
        cls.replication = json.loads(REPLICATION_PATH.read_text(encoding="utf-8"))

    def test_campaign_is_preregistered_and_source_locked(self):
        self.assertTrue(QUESTION_PATH.is_file())
        self.assertTrue(EXECUTION_SPEC_PATH.is_file())
        self.assertEqual(
            EXPECTED_SPEC_SHA256,
            hashlib.sha256(EXECUTION_SPEC_PATH.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            "FAR-EVIDENCE-AUTHORITY-MODEL-001",
            self.execution_spec["investigation_id"],
        )
        self.assertEqual(
            "791906aa7f483c7906650bd0a55c8ba1505e2e62",
            self.execution_spec["preregistration_commit"],
        )
        for source, expected_blob in self.execution_spec["frozen_sources"].items():
            source_path = ROOT / source
            self.assertTrue(source_path.is_file(), source)
            self.assertEqual(expected_blob, git_blob_sha(source_path), source)

    def test_campaign_lifecycle_remains_research_and_non_promotional(self):
        for payload in (
            self.execution_spec,
            self.execution,
            self.observation,
            self.result,
            self.replication,
        ):
            self.assertEqual("Research", payload["status"])
            self.assertEqual(
                "FAR-EVIDENCE-AUTHORITY-MODEL-001",
                payload["investigation_id"],
            )
        self.assertEqual("bounded_candidate_supported", self.result["discovery"])
        self.assertEqual("prohibited", self.result["lifecycle"]["acceptance"])
        self.assertEqual("prohibited", self.result["lifecycle"]["promotion"])
        self.assertFalse(self.replication["external_independence"])
        self.assertEqual("pending", self.replication["external_replication"])
        self.assertTrue(REPORT_PATH.is_file())
        report = REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("Status: **Research**", report)
        self.assertIn("External replication: **pending**", report)
        self.assertIn("Acceptance: **prohibited**", report)
        self.assertIn("Promotion: **prohibited**", report)

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
        self.assertTrue(self.registry["research_provenance"]["pre_preregistration_drafts_withdrawn"])

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

    def test_governing_charter_and_assurance_taxonomy_are_registered_blockers(self):
        charter = self.registry["domains"]["research_execution_charter"]
        taxonomy = self.registry["domains"]["proof_assurance_taxonomy"]
        self.assertEqual(
            "docs/governance/research-execution-charter.md", charter["owner"]
        )
        self.assertEqual("Provisional", charter["current_status"])
        self.assertEqual("methodological_specification", charter["authority_class"])
        self.assertEqual("Accepted", charter["required_status_for_activation"])
        self.assertEqual("docs/proof-assurance-taxonomy.md", taxonomy["owner"])
        self.assertEqual("Unknown", taxonomy["current_status"])
        self.assertEqual("canonical_specification", taxonomy["authority_class"])
        self.assertEqual("Accepted", taxonomy["required_status_for_activation"])
        requirements = set(self.registry["activation_requirements"])
        self.assertIn(
            "research execution charter transitioned to Accepted or replaced by an independently Accepted successor",
            requirements,
        )
        self.assertIn(
            "proof assurance taxonomy transitioned to Accepted or replaced by an independently Accepted successor",
            requirements,
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
        self.assertGreaterEqual(len(paths), 45)
        required = {
            "mechanization/lean/FARCanonicalCountermodel.lean",
            "mechanization/lean/SCoreW5.lean",
            "theory/proof-objects/T-001.proof.yaml",
            "theory/proof-objects/T-005.proof.yaml",
            "theory/proof-objects/T-006.proof.yaml",
            "theory/proof-objects/T-015.proof.yaml",
            "theory/proofs/T-001-primitive-minimality.md",
            "theory/proofs/T-015-explicit-reasoning-meta-theorem.md",
            "theory/lemmas/core-lemmas.md",
            "theory/evaluation/s-core-w5-theorem-assembly-proof.json",
        }
        self.assertTrue(required <= paths, sorted(required - paths))
        for proof_path in sorted(paths):
            self.assertTrue((ROOT / proof_path).is_file(), proof_path)
            self.assertTrue(
                matches_owner_pattern(proof_path, proofs["owner_pattern"]),
                proof_path,
            )

    def test_proof_discovery_contract_names_every_current_pathway(self):
        contract = self.registry["domains"]["proof_records"]["discovery_contract"]
        self.assertEqual(
            "theory/metadata/lemmas.yaml", contract["lemma_metadata"]
        )
        self.assertEqual("tools/verify_theory.py", contract["required_proof_object_source"])
        self.assertTrue(PATH_KEYS <= set(contract["path_keys"]))
        self.assertEqual(set(PATH_KEY_SUFFIXES), set(contract["path_key_suffixes"]))
        self.assertIn("proof_id", contract["self_registering_record_keys"])

    def test_proof_status_manifest_has_registered_owner_and_own_provenance_gate(self):
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
        self.assertTrue(
            self.proof_manifest["acceptance_decision_required_for_activation"]
        )
        self.assertIsNone(self.proof_manifest["acceptance_decision_record"])
        self.assertEqual([], self.proof_manifest["entries"])
        self.assertIn("self-acceptance", manifest_domain["may_not_establish"])
        self.assertIn(
            "manifest-level acceptance_decision_record is present and valid",
            self.proof_manifest["activation_conditions"],
        )

    def test_proof_status_policy_preserves_non_authoritative_artifacts(self):
        proofs = self.registry["domains"]["proof_records"]
        policy = proofs["status_policy"]
        taxonomy = set(self.registry["artifact_status_taxonomy"])
        requirements = set(self.registry["activation_requirements"])

        self.assertTrue(policy["manifest_required_for_activation"])
        self.assertTrue(policy["manifest_acceptance_decision_required"])
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

    def test_equal_priority_conflicts_fail_closed(self):
        policy = self.registry["conflict_policy"]
        self.assertTrue(policy["unique_scoped_owner_or_authorized_version_required"])
        self.assertEqual("Unknown", policy["equal_priority_unresolved_result"])
        self.assertEqual("Unknown", policy["higher_priority_unresolved_result"])
        self.assertTrue(policy["recency_is_not_a_tiebreaker"])
        self.assertTrue(policy["dual_authority_for_proposition_and_negation_prohibited"])
        self.assertIn(
            "If two equal-priority artifacts contradict one another",
            self.model,
        )
        self.assertIn(
            "equal-priority contradiction permits dual authority",
            self.registry["forbidden_inferences"],
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
        self.assertIn("research charter status", methodology["may_not_establish"])

    def test_promotion_requires_independent_bootstrap_and_full_lifecycle(self):
        requirements = set(self.registry["promotion_requirements"])
        required = {
            "separate preregistered lifecycle",
            "pre-existing independent bootstrap authority",
            "bootstrap authority hash lock",
            "exact artifact and version",
            "external replication record",
            "acceptance record",
            "promotion record",
            "authority model status transition completed",
            "authority registry status transition completed",
            "research execution charter status transition or Accepted successor completed",
            "proof assurance taxonomy status transition or Accepted successor completed",
            "owner status transitions completed",
            "proof artifact status manifest completed and Accepted",
            "proof artifact status manifest acceptance decision linked",
            "equal-priority conflict inventory resolved or classified Unknown",
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
            "status register defines assurance taxonomy without a separately registered taxonomy",
            "recency resolves equal-priority contradiction",
            "equal-priority contradiction permits dual authority",
            "provisional research charter silently governs an activated authority model",
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
