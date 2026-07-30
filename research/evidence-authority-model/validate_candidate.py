#!/usr/bin/env python3
"""Reproducible validator for FAR-EVIDENCE-AUTHORITY-MODEL-001.

The validator executes against the preregistered frozen Git commit, not the
mutable working tree, for every proof-discovery input. Candidate artifacts are
read from the current research branch. No canonical governance is installed.
"""

from __future__ import annotations

import argparse
import copy
import fnmatch
import hashlib
import json
import pathlib
import re
import subprocess
from collections import defaultdict
from typing import Any, Iterable

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
CAMPAIGN_ROOT = REPO_ROOT / "research/evidence-authority-model"
CANDIDATE_ROOT = CAMPAIGN_ROOT / "candidate"
MODEL_PATH = CANDIDATE_ROOT / "model-v1.0.md"
REGISTRY_PATH = CANDIDATE_ROOT / "registry-v1.0.json"
MANIFEST_PATH = CANDIDATE_ROOT / "proof-artifact-status-manifest-v1.0.json"
SPEC_PATH = CAMPAIGN_ROOT / "execution-spec-v1.0.json"
CANONICAL_IMPLEMENTATION_PATHS = (
    "docs/governance/evidence-authority-model.md",
    "docs/governance/evidence-authority-registry.json",
    "docs/governance/proof-artifact-status-manifest.json",
)
METADATA_ROOT_PREFIXES = (
    "foundations/",
    "theory/",
    "docs/governance/",
    "research/",
    "mechanization/",
)
PATH_EXTENSIONS = (".md", ".json", ".yaml", ".yml", ".lean")
GENERIC_PATH_KEYS = {
    "proof",
    "proof_object",
    "proof_artifact",
    "source_proof",
    "lean_file",
    "proof_registry",
    "entrypoint",
}
PATH_SUFFIXES = ("_proof_artifact", "_proof_registry")
EXPECTED_PATHWAYS = {
    "theorem_metadata",
    "lemma_metadata",
    "proposition_metadata",
    "dependency_registry",
    "verifier_required_objects",
    "structured_metadata",
    "object_valued_paths",
    "terminal_entrypoints",
    "self_registering_records",
}
EXPECTED_SPEC_SHA256 = "5328b419dd8ef86e77852730f3b2d3b6a1b6f6440bea92a55ff537db2f72bc2a"
CHARTER_STATUSES = {"Accepted", "Research", "Provisional", "Archive", "Unknown"}
REQUIRED_MANIFEST_ENTRY_FIELDS = {
    "artifact",
    "artifact_status",
    "authority_bearing",
    "status_decision_record",
    "scope",
    "limitations",
}


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_digest(value: Any) -> str:
    rendered = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(rendered).hexdigest()


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
    )


class FrozenTree:
    """Read-only view of the preregistered frozen commit."""

    def __init__(self, commit: str):
        self.commit = commit
        self._ensure_commit()
        self.tree_sha = run_git("rev-parse", f"{commit}^{{tree}}").stdout.strip()
        listing = run_git("ls-tree", "-r", commit).stdout.splitlines()
        self.blobs: dict[str, str] = {}
        for line in listing:
            match = re.match(r"^\d+\s+blob\s+([0-9a-f]{40})\t(.+)$", line)
            if match:
                self.blobs[match.group(2)] = match.group(1)

    def _ensure_commit(self) -> None:
        present = run_git("cat-file", "-e", f"{self.commit}^{{commit}}", check=False)
        if present.returncode == 0:
            return
        fetched = run_git(
            "fetch",
            "--no-tags",
            "--depth=1",
            "origin",
            self.commit,
            check=False,
        )
        if fetched.returncode != 0:
            raise RuntimeError(
                f"cannot fetch frozen commit {self.commit}: {fetched.stderr.strip()}"
            )
        run_git("cat-file", "-e", f"{self.commit}^{{commit}}")

    def exists(self, path: str) -> bool:
        return path in self.blobs

    def blob_sha(self, path: str) -> str | None:
        return self.blobs.get(path)

    def read_text(self, path: str) -> str:
        if path not in self.blobs:
            raise FileNotFoundError(f"{path} absent from frozen commit {self.commit}")
        return run_git("show", f"{self.commit}:{path}").stdout

    def load_json(self, path: str) -> Any:
        return json.loads(self.read_text(path))

    def load_yaml(self, path: str) -> Any:
        return yaml.safe_load(self.read_text(path))

    def structured_metadata_paths(self) -> list[str]:
        return sorted(
            path
            for path in self.blobs
            if path.endswith((".json", ".yaml", ".yml"))
            and path.startswith(METADATA_ROOT_PREFIXES)
            and "/fixtures/" not in f"/{path}/"
            and "__pycache__" not in path
            and path
            != "research/evidence-authority-model/candidate/proof-artifact-status-manifest-v1.0.json"
        )


def syntactic_repo_path(value: Any) -> bool:
    """Recognize a registered repository path without requiring existence."""
    if not isinstance(value, str) or not value.endswith(PATH_EXTENSIONS):
        return False
    if value.startswith(("http://", "https://", "/")) or "\n" in value:
        return False
    candidate = pathlib.PurePosixPath(value)
    return value == candidate.as_posix() and ".." not in candidate.parts


def path_values(value: Any, *, object_path: bool = False) -> Iterable[tuple[str, bool]]:
    if syntactic_repo_path(value):
        yield value, object_path
        return
    if isinstance(value, list):
        for child in value:
            yield from path_values(child, object_path=object_path)
        return
    if isinstance(value, dict):
        nested_object = object_path or "path" in value
        if "path" in value:
            yield from path_values(value["path"], object_path=True)
        for key, child in value.items():
            if key != "path":
                yield from path_values(child, object_path=nested_object)


def required_proof_objects(verifier_text: str) -> set[str]:
    match = re.search(
        r"REQUIRED_PROOF_OBJECT_THEOREMS\s*=\s*\{(?P<body>.*?)\n\}",
        verifier_text,
        re.DOTALL,
    )
    if match is None:
        raise ValueError("verifier proof-object requirement set not found")
    theorem_ids = set(re.findall(r'"(T-\d{3})"', match.group("body")))
    return {f"theory/proof-objects/{item}.proof.yaml" for item in theorem_ids}


def add_paths(
    inventory: dict[str, set[str]],
    paths: Iterable[str],
    pathway: str,
    disabled: set[str],
) -> None:
    if pathway in disabled:
        return
    for path in paths:
        if syntactic_repo_path(path):
            inventory[path].add(pathway)


def discover_proof_paths(
    frozen: FrozenTree,
    disabled: set[str] | None = None,
) -> tuple[dict[str, set[str]], set[str], dict[str, str]]:
    """Discover every registered proof path from the immutable frozen tree."""
    disabled = disabled or set()
    inventory: dict[str, set[str]] = defaultdict(set)
    executed: set[str] = set()
    discovery_inputs: dict[str, str] = {}

    def register_input(path: str) -> None:
        blob = frozen.blob_sha(path)
        if blob is None:
            raise FileNotFoundError(path)
        discovery_inputs[path] = blob

    theorem_path = "theory/metadata/theorems.yaml"
    register_input(theorem_path)
    if "theorem_metadata" not in disabled:
        payload = frozen.load_yaml(theorem_path)
        add_paths(
            inventory,
            (item["proof"] for item in payload["theorems"]),
            "theorem_metadata",
            disabled,
        )
        executed.add("theorem_metadata")

    lemma_path = "theory/metadata/lemmas.yaml"
    register_input(lemma_path)
    if "lemma_metadata" not in disabled:
        payload = frozen.load_yaml(lemma_path)
        add_paths(
            inventory,
            (item["source"] for item in payload["lemmas"]),
            "lemma_metadata",
            disabled,
        )
        executed.add("lemma_metadata")

    proposition_path = "theory/metadata/propositions.yaml"
    register_input(proposition_path)
    if "proposition_metadata" not in disabled:
        payload = frozen.load_yaml(proposition_path)
        add_paths(
            inventory,
            (item["source"] for item in payload["propositions"]),
            "proposition_metadata",
            disabled,
        )
        executed.add("proposition_metadata")

    dependency_path = "theory/dependencies/dependency-registry.yaml"
    register_input(dependency_path)
    if "dependency_registry" not in disabled:
        payload = frozen.load_yaml(dependency_path)
        add_paths(
            inventory,
            (
                item["source"]
                for item in payload["dependencies"]
                if item.get("source_type") == "proof_object"
            ),
            "dependency_registry",
            disabled,
        )
        executed.add("dependency_registry")

    verifier_path = "tools/verify_theory.py"
    register_input(verifier_path)
    if "verifier_required_objects" not in disabled:
        add_paths(
            inventory,
            required_proof_objects(frozen.read_text(verifier_path)),
            "verifier_required_objects",
            disabled,
        )
        executed.add("verifier_required_objects")

    structured_found = False
    object_found = False
    entrypoint_found = False
    self_registering_found = False

    for source in frozen.structured_metadata_paths():
        register_input(source)
        try:
            payload = (
                frozen.load_json(source)
                if source.endswith(".json")
                else frozen.load_yaml(source)
            )
        except (json.JSONDecodeError, yaml.YAMLError, UnicodeDecodeError):
            continue

        if isinstance(payload, dict) and isinstance(payload.get("proof_id"), str):
            if "self_registering_records" not in disabled:
                inventory[source].add("self_registering_records")
                self_registering_found = True

        def walk(value: Any, proof_record: bool = False) -> None:
            nonlocal structured_found, object_found, entrypoint_found
            if isinstance(value, dict):
                proof_record = proof_record or isinstance(value.get("proof_id"), str)
                for key, child in value.items():
                    registered = (
                        key in GENERIC_PATH_KEYS
                        or key.endswith(PATH_SUFFIXES)
                        or (key == "source_artifact" and proof_record)
                    )
                    if registered:
                        pathway = (
                            "terminal_entrypoints"
                            if key == "entrypoint"
                            else "structured_metadata"
                        )
                        if pathway not in disabled:
                            for path, object_path in path_values(child):
                                inventory[path].add(pathway)
                                if pathway == "terminal_entrypoints":
                                    entrypoint_found = True
                                else:
                                    structured_found = True
                                if (
                                    object_path
                                    and "object_valued_paths" not in disabled
                                ):
                                    inventory[path].add("object_valued_paths")
                                    object_found = True
                    walk(child, proof_record)
            elif isinstance(value, list):
                for child in value:
                    walk(child, proof_record)

        walk(payload)

    if structured_found:
        executed.add("structured_metadata")
    if object_found:
        executed.add("object_valued_paths")
    if entrypoint_found:
        executed.add("terminal_entrypoints")
    if self_registering_found:
        executed.add("self_registering_records")
    return inventory, executed, discovery_inputs


def owner_matches(path: str, owner_pattern: str) -> bool:
    return any(fnmatch.fnmatchcase(path, part) for part in owner_pattern.split("|"))


def claim_identity(claim: dict[str, Any]) -> tuple[Any, ...]:
    return (
        claim["proposition_id"],
        claim["scope"],
        tuple(sorted(claim["premises"])),
        claim["version"],
    )


def adjudicate_claims(
    claims: list[dict[str, Any]],
    conflict_policy: dict[str, Any],
) -> dict[str, Any]:
    """Adjudicate concrete claims rather than checking policy strings alone."""
    if not claims:
        return {"result": "Unknown", "reason": "no_claims"}
    identities = {claim_identity(claim) for claim in claims}
    if len(identities) != 1:
        return {"result": "Incomparable", "reason": "different_claim_identity"}

    highest = max(int(claim["priority"]) for claim in claims)
    top = [claim for claim in claims if int(claim["priority"]) == highest]
    polarities = {claim["polarity"] for claim in top}
    if len(polarities) > 1:
        if conflict_policy.get(
            "dual_authority_for_proposition_and_negation_prohibited"
        ) and conflict_policy.get("equal_priority_unresolved_result") == "Unknown":
            return {
                "result": "Unknown",
                "reason": "equal_priority_contradiction",
                "artifacts": sorted(claim["artifact"] for claim in top),
            }
        return {
            "result": "DualAuthority",
            "reason": "equal_priority_contradiction_not_fail_closed",
        }

    return {
        "result": next(iter(polarities)),
        "reason": "unique_highest_priority_polarity",
        "artifacts": sorted(claim["artifact"] for claim in top),
    }


def conflict_probe(policy: dict[str, Any]) -> dict[str, Any]:
    common = {
        "proposition_id": "CONFLICT-CONTROL-001",
        "scope": "frozen negative-control scope",
        "premises": ["P-A", "P-B"],
        "version": "1.0",
        "priority": 2,
    }
    claims = [
        {**common, "artifact": "control/affirm.json", "polarity": "Affirmed"},
        {**common, "artifact": "control/deny.json", "polarity": "Denied"},
    ]
    return adjudicate_claims(claims, policy)


def synthetic_activation_manifest(
    inventory: dict[str, set[str]],
) -> dict[str, Any]:
    entries = []
    for index, artifact in enumerate(sorted(inventory)):
        authority_bearing = index == 0
        entries.append(
            {
                "artifact": artifact,
                "artifact_status": "Accepted" if authority_bearing else "Research",
                "authority_bearing": authority_bearing,
                "status_decision_record": f"control/decision-{index:03d}.json",
                "scope": "frozen validation control",
                "limitations": ["synthetic activation probe only"],
            }
        )
    return {
        "status": "Accepted",
        "active": True,
        "acceptance_decision_required_for_activation": True,
        "acceptance_decision_record": "control/manifest-acceptance.json",
        "required_entry_fields": sorted(REQUIRED_MANIFEST_ENTRY_FIELDS),
        "entries": entries,
    }


def validate_manifest_entries(
    manifest: dict[str, Any],
    inventory: dict[str, set[str]],
    status_policy: dict[str, Any],
    *,
    activation: bool,
) -> list[str]:
    errors: list[str] = []
    if not activation:
        if manifest.get("status") != "Research" or manifest.get("active") is not False:
            errors.append("manifest_not_inactive_research")
        if not manifest.get("acceptance_decision_required_for_activation"):
            errors.append("manifest_acceptance_decision_not_required")
        if manifest.get("acceptance_decision_record") is not None:
            errors.append("manifest_claims_unearned_acceptance")
        return errors

    if manifest.get("status") != "Accepted" or manifest.get("active") is not True:
        errors.append("activation_manifest_not_accepted_active")
    if not manifest.get("acceptance_decision_record"):
        errors.append("activation_manifest_missing_acceptance_decision")

    required_status = status_policy.get(
        "required_status_for_authority_bearing_artifact"
    )
    if required_status != "Accepted":
        errors.append("proof_status_policy_not_accepted")
    if not status_policy.get("authority_bearing_designation_required"):
        errors.append("authority_bearing_designation_not_required")
    if not status_policy.get("exactly_one_status_per_registered_artifact"):
        errors.append("exactly_one_status_not_required")
    if not status_policy.get(
        "non_authority_bearing_artifacts_excluded_from_active_proof_authority"
    ):
        errors.append("non_authority_bearing_not_excluded")

    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return errors + ["manifest_entries_not_list"]

    by_artifact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"manifest_entry_not_object:{index}")
            continue
        missing = REQUIRED_MANIFEST_ENTRY_FIELDS - set(entry)
        for field in sorted(missing):
            errors.append(f"manifest_missing_field:{index}:{field}")
        artifact = entry.get("artifact")
        if isinstance(artifact, str):
            by_artifact[artifact].append(entry)
        status = entry.get("artifact_status")
        if status not in CHARTER_STATUSES:
            errors.append(f"manifest_invalid_status:{index}:{status}")
        designation = entry.get("authority_bearing")
        if not isinstance(designation, bool):
            errors.append(f"manifest_invalid_authority_designation:{index}")
        if designation is True and status != required_status:
            errors.append(f"authority_bearing_not_accepted:{index}:{status}")
        if not entry.get("status_decision_record"):
            errors.append(f"manifest_missing_status_decision:{index}")

    expected = set(inventory)
    actual = set(by_artifact)
    for artifact in sorted(expected - actual):
        errors.append(f"manifest_missing_artifact:{artifact}")
    for artifact in sorted(actual - expected):
        errors.append(f"manifest_unregistered_artifact:{artifact}")
    for artifact, artifact_entries in sorted(by_artifact.items()):
        if len(artifact_entries) != 1:
            errors.append(f"manifest_duplicate_artifact:{artifact}:{len(artifact_entries)}")
    return errors


def validate_candidate(
    frozen: FrozenTree,
    *,
    registry: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
    model_text: str | None = None,
    disabled_pathways: set[str] | None = None,
    injected_paths: set[str] | None = None,
    activation_manifest: dict[str, Any] | None = None,
    enforce_research_only_placement: bool = True,
) -> dict[str, Any]:
    registry = copy.deepcopy(registry if registry is not None else load_json(REGISTRY_PATH))
    manifest = copy.deepcopy(manifest if manifest is not None else load_json(MANIFEST_PATH))
    model_text = model_text if model_text is not None else MODEL_PATH.read_text(encoding="utf-8")
    disabled_pathways = disabled_pathways or set()
    injected_paths = injected_paths or set()
    errors: list[str] = []

    if registry.get("status") != "Research" or registry.get("active") is not False:
        errors.append("candidate_not_inactive_research")
    if not registry.get("canonical_repository_implementation_deferred"):
        errors.append("repository_implementation_not_deferred")
    if enforce_research_only_placement:
        for path in CANONICAL_IMPLEMENTATION_PATHS:
            if (REPO_ROOT / path).exists():
                errors.append(f"premature_canonical_implementation:{path}")

    required_domains = set(registry.get("required_governing_domains", []))
    actual_domains = set(registry.get("domains", {}))
    for name in sorted(required_domains - actual_domains):
        errors.append(f"missing_governing_domain:{name}")

    for name, domain in registry.get("domains", {}).items():
        if not domain.get("authority_class"):
            errors.append(f"missing_authority_class:{name}")
        if not domain.get("proposition_scope"):
            errors.append(f"missing_proposition_scope:{name}")
        for key in ("owner", "candidate_artifact"):
            path = domain.get(key)
            if path and not (REPO_ROOT / path).is_file():
                errors.append(f"missing_domain_artifact:{name}:{path}")

    bootstrap = registry.get("bootstrap", {})
    if bootstrap.get("status") != "Unknown" or bootstrap.get("selected_owner") is not None:
        errors.append("bootstrap_not_unknown")

    conflict_result = conflict_probe(registry.get("conflict_policy", {}))
    if conflict_result.get("result") != "Unknown":
        errors.append(f"conflict_probe_not_unknown:{conflict_result.get('result')}")

    errors.extend(
        validate_manifest_entries(
            manifest,
            {},
            registry.get("domains", {})
            .get("proof_records", {})
            .get("status_policy", {}),
            activation=False,
        )
    )

    lower_model = model_text.lower()
    if "neither authorizes nor prohibits experiments" not in lower_model:
        errors.append("experiment_nonauthority_missing")
    if "research candidate authorizes experiment execution" in lower_model:
        errors.append("candidate_authorizes_experiment")
    if "research candidate prohibits experiment execution" in lower_model:
        errors.append("candidate_prohibits_experiment")

    inventory, executed, discovery_inputs = discover_proof_paths(
        frozen, disabled_pathways
    )
    for path in injected_paths:
        inventory[path].add("injected_negative_control")
    for pathway in sorted(EXPECTED_PATHWAYS - executed):
        errors.append(f"missing_discovery_pathway:{pathway}")

    proof_domain = registry.get("domains", {}).get("proof_records", {})
    owner_pattern = proof_domain.get("owner_pattern", "")
    for path in sorted(inventory):
        if not frozen.exists(path):
            errors.append(f"missing_proof_target:{path}")
        if not owner_matches(path, owner_pattern):
            errors.append(f"uncovered_proof_target:{path}")

    activation_manifest = (
        copy.deepcopy(activation_manifest)
        if activation_manifest is not None
        else synthetic_activation_manifest(inventory)
    )
    activation_errors = validate_manifest_entries(
        activation_manifest,
        inventory,
        proof_domain.get("status_policy", {}),
        activation=True,
    )
    errors.extend(activation_errors)

    return {
        "valid": not errors,
        "errors": errors,
        "proof_path_count": len(inventory),
        "executed_pathways": sorted(executed),
        "frozen_base_commit": frozen.commit,
        "frozen_tree_sha": frozen.tree_sha,
        "discovery_input_count": len(discovery_inputs),
        "discovery_input_digest": canonical_digest(discovery_inputs),
        "discovery_input_blobs": dict(sorted(discovery_inputs.items())),
        "proof_inventory": {
            path: sorted(pathways) for path, pathways in sorted(inventory.items())
        },
        "conflict_probe": conflict_result,
        "activation_manifest_probe": {
            "entry_count": len(activation_manifest.get("entries", [])),
            "valid": not activation_errors,
            "errors": activation_errors,
        },
    }


def execute_negative_controls(frozen: FrozenTree) -> list[dict[str, Any]]:
    base_registry = load_json(REGISTRY_PATH)
    base_manifest = load_json(MANIFEST_PATH)
    base_model = MODEL_PATH.read_text(encoding="utf-8")
    base_inventory, _, _ = discover_proof_paths(frozen)
    controls: list[dict[str, Any]] = []

    def record(control_id: str, result: dict[str, Any], expected_prefix: str) -> None:
        observed = [
            error for error in result["errors"] if error.startswith(expected_prefix)
        ]
        controls.append(
            {
                "control_id": control_id,
                "expected_failure": expected_prefix,
                "observed_failures": observed,
                "detected": bool(observed) and not result["valid"],
            }
        )

    for domain_name in base_registry["required_governing_domains"]:
        mutated = copy.deepcopy(base_registry)
        mutated["domains"].pop(domain_name, None)
        record(
            f"remove_governing_domain:{domain_name}",
            validate_candidate(
                frozen,
                registry=mutated,
                enforce_research_only_placement=False,
            ),
            f"missing_governing_domain:{domain_name}",
        )

    for pathway in sorted(EXPECTED_PATHWAYS):
        record(
            f"disable_discovery_pathway:{pathway}",
            validate_candidate(
                frozen,
                disabled_pathways={pathway},
                enforce_research_only_placement=False,
            ),
            f"missing_discovery_pathway:{pathway}",
        )

    mutated = copy.deepcopy(base_registry)
    mutated["domains"]["proof_records"]["owner_pattern"] = "research/nowhere/**"
    record(
        "remove_proof_owner_coverage",
        validate_candidate(
            frozen,
            registry=mutated,
            enforce_research_only_placement=False,
        ),
        "uncovered_proof_target:",
    )

    mutated = copy.deepcopy(base_registry)
    mutated["conflict_policy"]["equal_priority_unresolved_result"] = "Accepted"
    record(
        "inject_equal_priority_contradiction_with_nonfailclosed_policy",
        validate_candidate(
            frozen,
            registry=mutated,
            enforce_research_only_placement=False,
        ),
        "conflict_probe_not_unknown:",
    )

    mutated = copy.deepcopy(base_registry)
    mutated["conflict_policy"][
        "dual_authority_for_proposition_and_negation_prohibited"
    ] = False
    record(
        "inject_equal_priority_contradiction_with_dual_authority",
        validate_candidate(
            frozen,
            registry=mutated,
            enforce_research_only_placement=False,
        ),
        "conflict_probe_not_unknown:",
    )

    mutated_manifest = copy.deepcopy(base_manifest)
    mutated_manifest["acceptance_decision_required_for_activation"] = False
    record(
        "remove_manifest_acceptance_gate",
        validate_candidate(
            frozen,
            manifest=mutated_manifest,
            enforce_research_only_placement=False,
        ),
        "manifest_acceptance_decision_not_required",
    )

    valid_activation = synthetic_activation_manifest(base_inventory)
    weakened = copy.deepcopy(valid_activation)
    weakened["entries"][0]["artifact_status"] = "Research"
    record(
        "grant_authority_to_unaccepted_proof",
        validate_candidate(
            frozen,
            activation_manifest=weakened,
            enforce_research_only_placement=False,
        ),
        "authority_bearing_not_accepted:",
    )

    weakened = copy.deepcopy(valid_activation)
    weakened["entries"][0].pop("authority_bearing")
    record(
        "omit_authority_bearing_designation",
        validate_candidate(
            frozen,
            activation_manifest=weakened,
            enforce_research_only_placement=False,
        ),
        "manifest_missing_field:",
    )

    mutated = copy.deepcopy(base_registry)
    mutated["domains"]["proof_records"]["status_policy"][
        "required_status_for_authority_bearing_artifact"
    ] = "Research"
    record(
        "weaken_authority_bearing_status_policy",
        validate_candidate(
            frozen,
            registry=mutated,
            enforce_research_only_placement=False,
        ),
        "proof_status_policy_not_accepted",
    )

    record(
        "inject_missing_registered_target",
        validate_candidate(
            frozen,
            injected_paths={"theory/proofs/DOES-NOT-EXIST.md"},
            enforce_research_only_placement=False,
        ),
        "missing_proof_target:theory/proofs/DOES-NOT-EXIST.md",
    )

    record(
        "inject_experiment_authority",
        validate_candidate(
            frozen,
            model_text=base_model
            + "\nThis Research candidate authorizes experiment execution.\n",
            enforce_research_only_placement=False,
        ),
        "candidate_authorizes_experiment",
    )

    return controls


def verify_frozen_sources(
    frozen: FrozenTree,
    spec: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    observed_sha = hashlib.sha256(SPEC_PATH.read_bytes()).hexdigest()
    if observed_sha != EXPECTED_SPEC_SHA256:
        errors.append("execution_spec_hash_mismatch")
    if spec.get("frozen_base_commit") != frozen.commit:
        errors.append("frozen_base_commit_mismatch")
    for source, expected_blob in spec["frozen_sources"].items():
        observed = frozen.blob_sha(source)
        if observed is None:
            errors.append(f"missing_frozen_source:{source}")
        elif observed != expected_blob:
            errors.append(f"frozen_source_hash_mismatch:{source}")
    return errors


def run_full_validation(
    *,
    enforce_research_only_placement: bool = True,
) -> dict[str, Any]:
    spec = load_json(SPEC_PATH)
    frozen = FrozenTree(spec["frozen_base_commit"])
    positive = validate_candidate(
        frozen,
        enforce_research_only_placement=enforce_research_only_placement,
    )
    source_errors = verify_frozen_sources(frozen, spec)
    controls = execute_negative_controls(frozen)
    undetected = [item["control_id"] for item in controls if not item["detected"]]
    overall_errors = list(positive["errors"]) + source_errors
    overall_errors.extend(
        f"undetected_negative_control:{item}" for item in undetected
    )
    core = {
        "schema_version": "1.1",
        "status": "Research",
        "investigation_id": "FAR-EVIDENCE-AUTHORITY-MODEL-001",
        "overall": "pass" if not overall_errors else "fail",
        "errors": overall_errors,
        "positive_validation": positive,
        "negative_controls": controls,
        "negative_control_count": len(controls),
        "all_negative_controls_detected": not undetected,
        "canonical_repository_implementation_deferred": enforce_research_only_placement,
        "nonclaims": [
            "validation does not establish truth",
            "validation does not Accept or Promote the candidate",
            "validation does not authorize Repository Change",
            "validation does not authorize or prohibit experiments",
        ],
    }
    core["evidence_digest"] = canonical_digest(core)
    return core


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument(
        "--allow-canonical-staging",
        action="store_true",
        help="Skip the final research-only placement check for diagnostic staging.",
    )
    args = parser.parse_args()
    result = run_full_validation(
        enforce_research_only_placement=not args.allow_canonical_staging
    )
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["overall"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
