import fnmatch
import hashlib
import json
import pathlib
import re
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL = ROOT / "docs/governance/evidence-authority-model.md"
REGISTRY = ROOT / "docs/governance/evidence-authority-registry.json"
MANIFEST = ROOT / "docs/governance/proof-artifact-status-manifest.json"
CAMPAIGN = ROOT / "research/evidence-authority-model"
SPEC = CAMPAIGN / "execution-spec-v1.0.json"
THEOREMS = ROOT / "theory/metadata/theorems.yaml"
LEMMAS = ROOT / "theory/metadata/lemmas.yaml"
DEPENDENCIES = ROOT / "theory/dependencies/dependency-registry.yaml"
VERIFIER = ROOT / "tools/verify_theory.py"
METADATA_ROOTS = tuple(ROOT / path for path in (
    "foundations", "theory", "docs/governance", "research", "mechanization"
))
GENERIC_PATH_KEYS = {
    "proof_object", "proof_artifact", "source_proof", "lean_file", "proof_registry"
}
PATH_SUFFIXES = ("_proof_artifact", "_proof_registry")
PROOF_EXTENSIONS = (".md", ".json", ".yaml", ".yml", ".lean")
SPEC_SHA256 = "5328b419dd8ef86e77852730f3b2d3b6a1b6f6440bea92a55ff537db2f72bc2a"


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def rel(path):
    return path.relative_to(ROOT).as_posix()


def git_blob_sha(path):
    body = path.read_bytes()
    return hashlib.sha1(f"blob {len(body)}\0".encode() + body).hexdigest()


def existing_artifact(value):
    return (
        isinstance(value, str)
        and " " not in value
        and not value.startswith(("http://", "https://"))
        and value.endswith(PROOF_EXTENSIONS)
        and (ROOT / value).is_file()
    )


def path_values(value):
    if existing_artifact(value):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from path_values(item)


def proof_paths_from_payload(value, source=None):
    if isinstance(value, dict):
        if source is not None and isinstance(value.get("proof_id"), str):
            yield rel(source)
        for key, child in value.items():
            is_path_key = (
                key == "proof"
                or key in GENERIC_PATH_KEYS
                or key.endswith(PATH_SUFFIXES)
                or (key == "source_artifact" and isinstance(value.get("proof_id"), str))
            )
            if is_path_key:
                yield from path_values(child)
            yield from proof_paths_from_payload(child, source)
    elif isinstance(value, list):
        for item in value:
            yield from proof_paths_from_payload(item, source)


def structured_metadata():
    for base in METADATA_ROOTS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path == MANIFEST or "fixtures" in path.parts:
                continue
            try:
                if path.suffix == ".json":
                    yield path, json.loads(path.read_text(encoding="utf-8"))
                elif path.suffix in {".yaml", ".yml"}:
                    yield path, load_yaml(path)
            except (json.JSONDecodeError, yaml.YAMLError, UnicodeDecodeError):
                continue


def required_proof_objects():
    match = re.search(
        r"REQUIRED_PROOF_OBJECT_THEOREMS\s*=\s*\{(?P<body>.*?)\n\}",
        VERIFIER.read_text(encoding="utf-8"),
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("verifier proof-object set not found")
    ids = set(re.findall(r'"(T-\d{3})"', match.group("body")))
    return {f"theory/proof-objects/{item}.proof.yaml" for item in ids}


def registered_proof_paths():
    paths = {item["proof"] for item in load_yaml(THEOREMS)["theorems"]}
    paths.update(item["source"] for item in load_yaml(LEMMAS)["lemmas"])
    paths.update(
        item["source"]
        for item in load_yaml(DEPENDENCIES)["dependencies"]
        if item.get("source_type") == "proof_object"
    )
    paths.update(required_proof_objects())
    for source, payload in structured_metadata():
        paths.update(proof_paths_from_payload(payload, source))
    return paths


def matches(path, pattern):
    return any(fnmatch.fnmatchcase(path, part) for part in pattern.split("|"))


class EvidenceAuthorityModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = MODEL.read_text(encoding="utf-8")
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.spec = json.loads(SPEC.read_text(encoding="utf-8"))
        cls.execution = json.loads((CAMPAIGN / "execution-v1.0.json").read_text())
        cls.observation = json.loads((CAMPAIGN / "observation-v1.0.json").read_text())
        cls.result = json.loads((CAMPAIGN / "result-v1.0.json").read_text())
        cls.replication = json.loads((CAMPAIGN / "replication-v1.0.json").read_text())

    def test_preregistered_campaign_and_source_locks(self):
        self.assertTrue((CAMPAIGN / "question-v1.0.md").is_file())
        self.assertEqual(SPEC_SHA256, hashlib.sha256(SPEC.read_bytes()).hexdigest())
        self.assertEqual("791906aa7f483c7906650bd0a55c8ba1505e2e62", self.spec["preregistration_commit"])
        for path, expected in self.spec["frozen_sources"].items():
            source = ROOT / path
            self.assertTrue(source.is_file(), path)
            self.assertEqual(expected, git_blob_sha(source), path)

    def test_campaign_remains_research_with_external_replication_pending(self):
        for payload in (self.spec, self.execution, self.observation, self.result, self.replication):
            self.assertEqual("Research", payload["status"])
            self.assertEqual("FAR-EVIDENCE-AUTHORITY-MODEL-001", payload["investigation_id"])
        self.assertEqual("bounded_candidate_supported", self.result["discovery"])
        self.assertEqual("prohibited", self.result["lifecycle"]["acceptance"])
        self.assertEqual("prohibited", self.result["lifecycle"]["promotion"])
        self.assertFalse(self.replication["external_independence"])
        self.assertEqual("pending", self.replication["external_replication"])
        report = (CAMPAIGN / "report-v1.0.md").read_text()
        for marker in ("Status: **Research**", "External replication: **pending**", "Acceptance: **prohibited**", "Promotion: **prohibited**"):
            self.assertIn(marker, report)

    def test_candidate_is_inactive_and_pre_preregistration_drafts_withdrawn(self):
        self.assertIn("Status: **Research**", self.model)
        self.assertIn("Candidacy: **Inactive candidate**", self.model)
        self.assertIn("Promotion completed: **No**", self.model)
        self.assertEqual("Research", self.registry["status"])
        self.assertFalse(self.registry["active"])
        self.assertFalse(self.registry["promotion_completed"])
        self.assertTrue(self.registry["research_provenance"]["pre_preregistration_drafts_withdrawn"])

    def test_fixed_owners_exist_and_all_classes_are_closed(self):
        declared = set()
        for name, domain in self.registry["domains"].items():
            declared.add(domain["authority_class"])
            self.assertTrue(domain.get("proposition_scope"), name)
            self.assertTrue(domain.get("may_establish"), name)
            self.assertTrue(domain.get("may_not_establish"), name)
            for key in ("owner", "proposed_owner"):
                if domain.get(key):
                    self.assertTrue((ROOT / domain[key]).is_file(), domain[key])
        self.assertEqual(declared, set(self.registry["permitted_statuses_by_class"]))

    def test_charter_taxonomy_and_lifecycle_stages_are_separate(self):
        expected = {"Accepted", "Research", "Provisional", "Archive", "Unknown"}
        self.assertEqual(expected, set(self.registry["artifact_status_taxonomy"]))
        for authority_class, statuses in self.registry["permitted_statuses_by_class"].items():
            self.assertTrue(statuses, authority_class)
            self.assertTrue(set(statuses) <= expected, authority_class)
            self.assertNotIn("Promoted", statuses)
            self.assertNotIn("Superseded", statuses)

    def test_external_bootstrap_and_self_ownership_are_fail_closed(self):
        bootstrap = self.registry["bootstrap"]
        self.assertEqual("Unknown", bootstrap["status"])
        self.assertIsNone(bootstrap["selected_owner"])
        self.assertTrue(bootstrap["selection_must_be_preregistered_and_hash_locked"])
        for key in ("authority_model_specification", "authority_registry_specification"):
            domain = self.registry["domains"][key]
            self.assertEqual("Research", domain["current_status"])
            self.assertEqual("Accepted", domain["required_status_for_activation"])
            self.assertIn("self-acceptance", domain["may_not_establish"])

    def test_governing_charter_and_assurance_taxonomy_are_registered_blockers(self):
        charter = self.registry["domains"]["research_execution_charter"]
        assurance = self.registry["domains"]["proof_assurance_taxonomy"]
        self.assertEqual("docs/governance/research-execution-charter.md", charter["owner"])
        self.assertEqual("Provisional", charter["current_status"])
        self.assertEqual("Accepted", charter["required_status_for_activation"])
        self.assertEqual("docs/proof-assurance-taxonomy.md", assurance["owner"])
        self.assertEqual("Unknown", assurance["current_status"])
        self.assertEqual("Accepted", assurance["required_status_for_activation"])
        requirements = set(self.registry["activation_requirements"])
        self.assertIn("research execution charter transitioned to Accepted or replaced by an independently Accepted successor", requirements)
        self.assertIn("proof assurance taxonomy transitioned to Accepted or replaced by an independently Accepted successor", requirements)

    def test_every_registered_proof_path_exists_and_has_a_proposed_owner(self):
        paths = registered_proof_paths()
        self.assertGreaterEqual(len(paths), 45)
        required = {
            "mechanization/lean/FARCanonicalCountermodel.lean",
            "mechanization/lean/SCoreW5.lean",
            "theory/lemmas/core-lemmas.md",
            "theory/proof-objects/T-001.proof.yaml",
            "theory/proof-objects/T-006.proof.yaml",
            "theory/proof-objects/T-015.proof.yaml",
            "theory/proofs/T-001-primitive-minimality.md",
            "theory/proofs/T-015-explicit-reasoning-meta-theorem.md",
            "theory/evaluation/s-core-w5-theorem-assembly-proof.json",
        }
        self.assertTrue(required <= paths, sorted(required - paths))
        pattern = self.registry["domains"]["proof_records"]["owner_pattern"]
        for path in sorted(paths):
            self.assertTrue((ROOT / path).is_file(), path)
            self.assertTrue(matches(path, pattern), path)

    def test_discovery_contract_names_all_generic_metadata_pathways(self):
        contract = self.registry["domains"]["proof_records"]["discovery_contract"]
        self.assertEqual("theory/metadata/theorems.yaml", contract["theorem_metadata"])
        self.assertEqual("theory/metadata/lemmas.yaml", contract["lemma_metadata"])
        self.assertEqual("tools/verify_theory.py", contract["required_proof_object_source"])
        self.assertTrue(GENERIC_PATH_KEYS <= set(contract["path_keys"]))
        self.assertEqual(set(PATH_SUFFIXES), set(contract["path_key_suffixes"]))
        self.assertIn("proof_id", contract["self_registering_record_keys"])

    def test_manifest_has_its_own_acceptance_provenance_gate(self):
        domain = self.registry["domains"]["proof_artifact_status_manifest"]
        self.assertEqual("docs/governance/proof-artifact-status-manifest.json", domain["owner"])
        self.assertEqual("Research", domain["current_status"])
        self.assertEqual("Accepted", domain["required_status_for_activation"])
        self.assertFalse(self.manifest["active"])
        self.assertTrue(self.manifest["acceptance_decision_required_for_activation"])
        self.assertIsNone(self.manifest["acceptance_decision_record"])
        self.assertEqual([], self.manifest["entries"])
        self.assertIn("manifest-level acceptance_decision_record is present and valid", self.manifest["activation_conditions"])

    def test_proof_status_and_authority_bearing_are_separate(self):
        policy = self.registry["domains"]["proof_records"]["status_policy"]
        self.assertTrue(policy["manifest_acceptance_decision_required"])
        self.assertTrue(policy["exactly_one_status_per_registered_artifact"])
        self.assertTrue(policy["authority_bearing_designation_required"])
        self.assertEqual("Accepted", policy["required_status_for_authority_bearing_artifact"])
        self.assertTrue(policy["non_authority_bearing_artifacts_may_retain_nonaccepted_charter_statuses"])
        self.assertTrue(policy["non_authority_bearing_artifacts_excluded_from_active_proof_authority"])
        self.assertIn("registered proof implies authority-bearing proof", self.registry["forbidden_inferences"])
        self.assertIn("Only proof artifacts designated authority-bearing must have status `Accepted`", self.model)

    def test_equal_priority_conflicts_yield_unknown(self):
        policy = self.registry["conflict_policy"]
        self.assertTrue(policy["unique_scoped_owner_or_authorized_version_required"])
        self.assertEqual("Unknown", policy["equal_priority_unresolved_result"])
        self.assertTrue(policy["recency_is_not_a_tiebreaker"])
        self.assertTrue(policy["dual_authority_for_proposition_and_negation_prohibited"])
        self.assertIn("If two equal-priority artifacts contradict one another", self.model)
        self.assertIn("equal-priority contradiction permits dual authority", self.registry["forbidden_inferences"])

    def test_definition_historical_research_and_methodology_boundaries(self):
        definitions = self.registry["domains"]["detailed_definitions"]
        self.assertEqual("Unknown", definitions["current_status"])
        self.assertEqual("Accepted", definitions["required_status_for_activation"])
        self.assertEqual("archive/**", self.registry["domains"]["historical_records"]["owner_pattern"])
        self.assertIn("acceptance", self.registry["domains"]["research_observations"]["may_not_establish"])
        self.assertIn("logical derivation from FARA", self.registry["domains"]["methodology"]["may_not_establish"])

    def test_promotion_gate_is_complete_and_experiment_power_is_absent(self):
        requirements = set(self.registry["promotion_requirements"])
        required = {
            "separate preregistered lifecycle",
            "pre-existing independent bootstrap authority",
            "external replication record",
            "acceptance record",
            "promotion record",
            "research execution charter status transition or Accepted successor completed",
            "proof assurance taxonomy status transition or Accepted successor completed",
            "proof artifact status manifest acceptance decision linked",
            "equal-priority conflict inventory resolved or classified Unknown",
            "semantic and dependency validation",
        }
        self.assertTrue(required <= requirements)
        forbidden = set(self.registry["forbidden_inferences"])
        self.assertIn("research candidate authorizes experiment execution", forbidden)
        self.assertIn("research candidate prohibits experiment execution", forbidden)
        self.assertIn("## Proposed consequence after promotion", self.model)
        self.assertIn("This Research candidate itself neither authorizes nor prohibits the next experiment", self.model)


if __name__ == "__main__":
    unittest.main()
