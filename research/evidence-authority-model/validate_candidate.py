#!/usr/bin/env python3
"""Reproducible validator for FAR-EVIDENCE-AUTHORITY-MODEL-001.

This is a Research execution artifact. It validates the research-only candidate,
executes the preregistered negative controls, and emits machine-readable evidence.
It does not install or activate governance.
"""

from __future__ import annotations

import argparse
import copy
import fnmatch
import hashlib
import json
import pathlib
import re
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
THEOREM_METADATA = REPO_ROOT / "theory/metadata/theorems.yaml"
LEMMA_METADATA = REPO_ROOT / "theory/metadata/lemmas.yaml"
PROPOSITION_METADATA = REPO_ROOT / "theory/metadata/propositions.yaml"
DEPENDENCY_REGISTRY = REPO_ROOT / "theory/dependencies/dependency-registry.yaml"
VERIFIER = REPO_ROOT / "tools/verify_theory.py"
METADATA_ROOTS = tuple(
    REPO_ROOT / path
    for path in ("foundations", "theory", "docs/governance", "research", "mechanization")
)
CANONICAL_IMPLEMENTATION_PATHS = (
    REPO_ROOT / "docs/governance/evidence-authority-model.md",
    REPO_ROOT / "docs/governance/evidence-authority-registry.json",
    REPO_ROOT / "docs/governance/proof-artifact-status-manifest.json",
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


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: pathlib.Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def relative(path: pathlib.Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def git_blob_sha(path: pathlib.Path) -> str:
    body = path.read_bytes()
    return hashlib.sha1(f"blob {len(body)}\0".encode() + body).hexdigest()


def syntactic_repo_path(value: Any) -> bool:
    """Recognize a registered repository path without requiring it to exist."""
    if not isinstance(value, str) or not value.endswith(PATH_EXTENSIONS):
        return False
    if value.startswith(("http://", "https://", "/")) or "\n" in value:
        return False
    candidate = pathlib.PurePosixPath(value)
    return value == candidate.as_posix() and ".." not in candidate.parts


def path_values(value: Any, *, object_path: bool = False) -> Iterable[tuple[str, bool]]:
    """Traverse strings, lists, and object-valued path registrations."""
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


def structured_metadata() -> Iterable[tuple[pathlib.Path, Any]]:
    for root in METADATA_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path == MANIFEST_PATH:
                continue
            if "fixtures" in path.parts or "__pycache__" in path.parts:
                continue
            try:
                if path.suffix == ".json":
                    yield path, load_json(path)
                elif path.suffix in {".yaml", ".yml"}:
                    yield path, load_yaml(path)
            except (json.JSONDecodeError, yaml.YAMLError, UnicodeDecodeError):
                continue


def required_proof_objects() -> set[str]:
    match = re.search(
        r"REQUIRED_PROOF_OBJECT_THEOREMS\s*=\s*\{(?P<body>.*?)\n\}",
        VERIFIER.read_text(encoding="utf-8"),
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


def discover_proof_paths(disabled: set[str] | None = None) -> tuple[dict[str, set[str]], set[str]]:
    disabled = disabled or set()
    inventory: dict[str, set[str]] = defaultdict(set)
    executed: set[str] = set()

    if "theorem_metadata" not in disabled:
        paths = [item["proof"] for item in load_yaml(THEOREM_METADATA)["theorems"]]
        add_paths(inventory, paths, "theorem_metadata", disabled)
        executed.add("theorem_metadata")

    if "lemma_metadata" not in disabled:
        paths = [item["source"] for item in load_yaml(LEMMA_METADATA)["lemmas"]]
        add_paths(inventory, paths, "lemma_metadata", disabled)
        executed.add("lemma_metadata")

    if "proposition_metadata" not in disabled:
        paths = [
            item["source"]
            for item in load_yaml(PROPOSITION_METADATA)["propositions"]
            if str(item.get("status", "")).startswith("Established")
        ]
        add_paths(inventory, paths, "proposition_metadata", disabled)
        executed.add("proposition_metadata")

    if "dependency_registry" not in disabled:
        paths = [
            item["source"]
            for item in load_yaml(DEPENDENCY_REGISTRY)["dependencies"]
            if item.get("source_type") == "proof_object"
        ]
        add_paths(inventory, paths, "dependency_registry", disabled)
        executed.add("dependency_registry")

    if "verifier_required_objects" not in disabled:
        add_paths(
            inventory,
            required_proof_objects(),
            "verifier_required_objects",
            disabled,
        )
        executed.add("verifier_required_objects")

    structured_found = False
    object_found = False
    entrypoint_found = False
    self_registering_found = False
    for source, payload in structured_metadata():
        if isinstance(payload, dict) and isinstance(payload.get("proof_id"), str):
            if "self_registering_records" not in disabled:
                inventory[relative(source)].add("self_registering_records")
                self_registering_found = True

        def walk(value: Any, proof_record: bool = False) -> None:
            nonlocal structured_found, object_found, entrypoint_found
            if isinstance(value, dict):
                proof_record = proof_record or isinstance(value.get("proof_id"), str)
                for key, child in value.items():
                    is_registered = (
                        key in GENERIC_PATH_KEYS
                        or key.endswith(PATH_SUFFIXES)
                        or (key == "source_artifact" and proof_record)
                    )
                    if is_registered:
                        pathway = "terminal_entrypoints" if key == "entrypoint" else "structured_metadata"
                        if pathway not in disabled:
                            for path, object_path in path_values(child):
                                inventory[path].add(pathway)
                                if pathway == "terminal_entrypoints":
                                    entrypoint_found = True
                                else:
                                    structured_found = True
                                if object_path and "object_valued_paths" not in disabled:
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
    return inventory, executed


def owner_matches(path: str, owner_pattern: str) -> bool:
    return any(fnmatch.fnmatchcase(path, part) for part in owner_pattern.split("|"))


def validate_candidate(
    *,
    registry: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
    model_text: str | None = None,
    disabled_pathways: set[str] | None = None,
    injected_paths: set[str] | None = None,
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
            if path.exists():
                errors.append(f"premature_canonical_implementation:{relative(path)}")

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
            if domain.get(key) and not (REPO_ROOT / domain[key]).is_file():
                errors.append(f"missing_domain_artifact:{name}:{domain[key]}")

    bootstrap = registry.get("bootstrap", {})
    if bootstrap.get("status") != "Unknown" or bootstrap.get("selected_owner") is not None:
        errors.append("bootstrap_not_unknown")

    conflict = registry.get("conflict_policy", {})
    if conflict.get("equal_priority_unresolved_result") != "Unknown":
        errors.append("equal_priority_not_unknown")
    if not conflict.get("dual_authority_for_proposition_and_negation_prohibited"):
        errors.append("dual_authority_not_prohibited")
    if not conflict.get("recency_is_not_a_tiebreaker"):
        errors.append("recency_tiebreaker_permitted")

    if manifest.get("status") != "Research" or manifest.get("active") is not False:
        errors.append("manifest_not_inactive_research")
    if not manifest.get("acceptance_decision_required_for_activation"):
        errors.append("manifest_acceptance_decision_not_required")
    if manifest.get("acceptance_decision_record") is not None:
        errors.append("manifest_claims_unearned_acceptance")

    lower_model = model_text.lower()
    if "neither authorizes nor prohibits experiments" not in lower_model:
        errors.append("experiment_nonauthority_missing")
    if "research candidate authorizes experiment execution" in lower_model:
        errors.append("candidate_authorizes_experiment")
    if "research candidate prohibits experiment execution" in lower_model:
        errors.append("candidate_prohibits_experiment")

    inventory, executed = discover_proof_paths(disabled_pathways)
    for path in injected_paths:
        inventory[path].add("injected_negative_control")
    for pathway in sorted(EXPECTED_PATHWAYS - executed):
        errors.append(f"missing_discovery_pathway:{pathway}")

    proof_domain = registry.get("domains", {}).get("proof_records", {})
    owner_pattern = proof_domain.get("owner_pattern", "")
    for path in sorted(inventory):
        if not (REPO_ROOT / path).is_file():
            errors.append(f"missing_proof_target:{path}")
        if not owner_matches(path, owner_pattern):
            errors.append(f"uncovered_proof_target:{path}")

    return {
        "valid": not errors,
        "errors": errors,
        "proof_path_count": len(inventory),
        "executed_pathways": sorted(executed),
        "proof_inventory": {
            path: sorted(pathways) for path, pathways in sorted(inventory.items())
        },
    }


def execute_negative_controls() -> list[dict[str, Any]]:
    base_registry = load_json(REGISTRY_PATH)
    base_manifest = load_json(MANIFEST_PATH)
    base_model = MODEL_PATH.read_text(encoding="utf-8")
    controls: list[dict[str, Any]] = []

    def record(control_id: str, result: dict[str, Any], expected_prefix: str) -> None:
        observed = [error for error in result["errors"] if error.startswith(expected_prefix)]
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
            validate_candidate(registry=mutated, enforce_research_only_placement=False),
            f"missing_governing_domain:{domain_name}",
        )

    for pathway in sorted(EXPECTED_PATHWAYS):
        record(
            f"disable_discovery_pathway:{pathway}",
            validate_candidate(
                disabled_pathways={pathway},
                enforce_research_only_placement=False,
            ),
            f"missing_discovery_pathway:{pathway}",
        )

    mutated = copy.deepcopy(base_registry)
    mutated["domains"]["proof_records"]["owner_pattern"] = "research/nowhere/**"
    record(
        "remove_proof_owner_coverage",
        validate_candidate(registry=mutated, enforce_research_only_placement=False),
        "uncovered_proof_target:",
    )

    mutated = copy.deepcopy(base_registry)
    mutated["conflict_policy"]["equal_priority_unresolved_result"] = "Accepted"
    record(
        "permit_equal_priority_resolution",
        validate_candidate(registry=mutated, enforce_research_only_placement=False),
        "equal_priority_not_unknown",
    )

    mutated = copy.deepcopy(base_registry)
    mutated["conflict_policy"]["dual_authority_for_proposition_and_negation_prohibited"] = False
    record(
        "permit_dual_authority",
        validate_candidate(registry=mutated, enforce_research_only_placement=False),
        "dual_authority_not_prohibited",
    )

    mutated_manifest = copy.deepcopy(base_manifest)
    mutated_manifest["acceptance_decision_required_for_activation"] = False
    record(
        "remove_manifest_acceptance_gate",
        validate_candidate(manifest=mutated_manifest, enforce_research_only_placement=False),
        "manifest_acceptance_decision_not_required",
    )

    record(
        "inject_missing_registered_target",
        validate_candidate(
            injected_paths={"theory/proofs/DOES-NOT-EXIST.md"},
            enforce_research_only_placement=False,
        ),
        "missing_proof_target:theory/proofs/DOES-NOT-EXIST.md",
    )

    record(
        "inject_experiment_authority",
        validate_candidate(
            model_text=base_model + "\nThis Research candidate authorizes experiment execution.\n",
            enforce_research_only_placement=False,
        ),
        "candidate_authorizes_experiment",
    )

    return controls


def verify_frozen_sources() -> list[str]:
    spec = load_json(SPEC_PATH)
    errors: list[str] = []
    observed_sha = hashlib.sha256(SPEC_PATH.read_bytes()).hexdigest()
    if observed_sha != EXPECTED_SPEC_SHA256:
        errors.append("execution_spec_hash_mismatch")
    for source, expected_blob in spec["frozen_sources"].items():
        path = REPO_ROOT / source
        if not path.is_file():
            errors.append(f"missing_frozen_source:{source}")
        elif git_blob_sha(path) != expected_blob:
            errors.append(f"frozen_source_hash_mismatch:{source}")
    return errors


def run_full_validation(*, enforce_research_only_placement: bool = True) -> dict[str, Any]:
    positive = validate_candidate(
        enforce_research_only_placement=enforce_research_only_placement
    )
    source_errors = verify_frozen_sources()
    controls = execute_negative_controls()
    undetected = [item["control_id"] for item in controls if not item["detected"]]
    overall_errors = list(positive["errors"]) + source_errors
    overall_errors.extend(f"undetected_negative_control:{item}" for item in undetected)
    return {
        "schema_version": "1.0",
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument(
        "--allow-canonical-staging",
        action="store_true",
        help="Skip final research-only placement check for diagnostic staging only.",
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
