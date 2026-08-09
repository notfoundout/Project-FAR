"""Required implementation for frozen v1.2 plus additive prospective hardening."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import verify_integrity as integrity
import verify_review_closure_v1_2_legacy as legacy
import verify_classification_input_digest_contract as classification_digest

DesignError = legacy.DesignError
AMENDMENT = legacy.AMENDMENT
NARRATIVE = legacy.NARRATIVE
SEED_INPUTS = legacy.SEED_INPUTS
CLASSIFICATION_INPUTS = legacy.CLASSIFICATION_INPUTS
HISTORICAL = legacy.HISTORICAL
TASK_IDENTITY_KEYS = legacy.TASK_IDENTITY_KEYS
TASK_BUNDLE_KEYS = legacy.TASK_BUNDLE_KEYS
REQUIRED_STRATA = legacy.REQUIRED_STRATA
CLASSIFICATION_MAPPING = legacy.CLASSIFICATION_MAPPING
CLASSIFICATION_EVIDENCE_RULE = legacy.CLASSIFICATION_EVIDENCE_RULE
PILOT_PREREQUISITES = legacy.PILOT_PREREQUISITES
CONFIRMATORY_PREREQUISITES = legacy.CONFIRMATORY_PREREQUISITES
_blob = legacy._blob
_current_blob = legacy._current_blob
EXPECTED_TIMING = "computed from the frozen classification inputs and committed before any sacrificial pilot or confirmatory execution"
EXPECTED_AMENDMENT_BLOB = "59c862790fee90beb0b3fba93dfd9b4e51921322"
EXPECTED_NARRATIVE_BLOB = "6089f31d1769349fc1e9f9588ad40dca9e775fef"
EFFECTIVE_RECORD_KEYS = {"blind_task_id", "repository_blind_id", "task_strata", "task_identity_sha256", "task_bundle_root_sha256"}
TASK_IDENTITY_DESCRIPTOR_KEYS = {
    "algorithm_id", "repository_provider", "repository_provider_id", "canonical_repository_url",
    "repository_commit_sha", "task_payload_sha256", "task_payload_bytes",
}
TASK_BUNDLE_DESCRIPTOR_KEYS = {"algorithm_id", "task_identity_sha256", "task_strata", "classification_inputs_sha256"}
EVIDENCE_RECORD_KEYS = {"blind_task_id", "task_identity_descriptor", "classification_descriptor", "task_bundle_descriptor"}
STRATA_BY_INPUT = {
    "source_declares_defect_or_bug": "bug_fix",
    "frozen_entry_test_or_CI_is_failing": "test_failure",
    "source_declares_previously_working_behavior_regressed": "behavioral_regression",
    "source_acceptance_criteria_require_API_or_contract_change": "API_or_contract_change",
    "sealed_reference_patch_touches_multiple_files": "multi_file_change",
}
STRATA_ORDER = ["bug_fix", "test_failure", "behavioral_regression", "API_or_contract_change", "multi_file_change"]
MINIMUM_TASK_COUNT = 24
MINIMUM_REPOSITORY_COUNT = 5
MAX_REPOSITORY_FRACTION_NUMERATOR = 1
MAX_REPOSITORY_FRACTION_DENOMINATOR = 5
BLIND_TASK_RE = re.compile(r"TASK-[0-9]{6}")
BLIND_REPOSITORY_RE = re.compile(r"REPO-[0-9]{4}")


def _sync_integrity_context() -> None:
    """Bind delegated validators to the caller's active repository/fixture root."""
    legacy.integrity.ROOT = integrity.ROOT
    legacy.integrity.HERE = integrity.HERE
    legacy.integrity.MANIFEST = integrity.MANIFEST
    legacy.integrity._committed_blob_bytes = integrity._committed_blob_bytes
    classification_digest.integrity.ROOT = integrity.ROOT
    classification_digest.integrity.HERE = integrity.HERE
    classification_digest.integrity.MANIFEST = integrity.MANIFEST
    classification_digest.integrity._committed_blob_bytes = integrity._committed_blob_bytes


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _load_json_any(path: Path) -> Any:
    return integrity._decode_json(integrity._read_regular(path), str(path))


def _require_sha256(value: Any, label: str) -> str:
    if type(value) is not str or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise DesignError(f"{label} must be lowercase SHA-256 hex")
    return value


def validate(path: Path | None = None):
    _sync_integrity_context()
    path = path or (integrity.HERE / "review-closure-amendment-v1.2.json")
    narrative = integrity.HERE / "AMENDMENT-v1.2.md"
    if legacy._blob(path) != EXPECTED_AMENDMENT_BLOB:
        raise DesignError("frozen review-closure amendment bytes drifted")
    if legacy._blob(narrative) != EXPECTED_NARRATIVE_BLOB:
        raise DesignError("frozen review-closure narrative bytes drifted")
    prior_narrative = legacy.NARRATIVE
    prior_amendment = legacy.AMENDMENT
    legacy.NARRATIVE = narrative
    legacy.AMENDMENT = path
    try:
        data = legacy.validate(path)
    finally:
        legacy.NARRATIVE = prior_narrative
        legacy.AMENDMENT = prior_amendment
    effective = data.get("task_manifest_effective_contract")
    if not isinstance(effective, dict):
        raise DesignError("effective task-manifest contract missing")
    strata = effective.get("task_strata")
    if not isinstance(strata, dict) or strata.get("classification_timing") != EXPECTED_TIMING:
        raise DesignError("task-stratum classification timing drifted")
    classification_digest.validate_contract(integrity.HERE / "classification-input-digest-contract-v1.0.json")
    return data


def _validate_population_contract(
    manifest: list[Any],
    repository_counts: dict[tuple[str, int], int],
    identity_to_blind: dict[tuple[str, int], str],
    blind_to_identity: dict[str, tuple[str, int]],
) -> None:
    task_count = len(manifest)
    if task_count < MINIMUM_TASK_COUNT:
        raise DesignError(f"frozen task population has {task_count} tasks; minimum is {MINIMUM_TASK_COUNT}")
    if len(repository_counts) < MINIMUM_REPOSITORY_COUNT:
        raise DesignError(
            f"frozen task population has {len(repository_counts)} authoritative repositories; "
            f"minimum is {MINIMUM_REPOSITORY_COUNT}"
        )
    if len(identity_to_blind) != len(repository_counts) or len(blind_to_identity) != len(repository_counts):
        raise DesignError("repository authoritative-identity/blind-ID mapping is not one-to-one")
    for identity, count in repository_counts.items():
        if count * MAX_REPOSITORY_FRACTION_DENOMINATOR > task_count * MAX_REPOSITORY_FRACTION_NUMERATOR:
            raise DesignError(
                "per-repository task cap exceeded for authoritative repository "
                f"{identity}: {count}/{task_count} > 1/5"
            )


def validate_instantiated_task_manifest(task_manifest_path: Path, evidence_registry_path: Path) -> None:
    """Required preexecution recomputation for every effective v1.5 task record.

    This does not instantiate or authorize a manifest. It validates already-frozen
    prospective bytes, their retained classification evidence, and the complete
    preregistered population constraints before launch.
    """
    validate()
    manifest = _load_json_any(task_manifest_path)
    evidence = _load_json_any(evidence_registry_path)
    if not isinstance(manifest, list) or not manifest:
        raise DesignError("instantiated task manifest must be a nonempty JSON array")
    if not isinstance(evidence, list) or len(evidence) != len(manifest):
        raise DesignError("classification evidence registry must align one-to-one with task manifest records")

    blind_task_ids: set[str] = set()
    task_ids: set[str] = set()
    bundle_roots: set[str] = set()
    observed_strata: set[str] = set()
    repository_counts: dict[tuple[str, int], int] = {}
    identity_to_blind: dict[tuple[str, int], str] = {}
    blind_to_identity: dict[str, tuple[str, int]] = {}
    identity_to_url: dict[tuple[str, int], str] = {}
    evidence_root = evidence_registry_path.parent

    for index, (record, proof) in enumerate(zip(manifest, evidence, strict=True)):
        label = f"task record {index}"
        if not isinstance(record, dict) or set(record) != EFFECTIVE_RECORD_KEYS:
            raise DesignError(f"{label} effective v1.5 shape drifted")
        if not isinstance(proof, dict) or set(proof) != EVIDENCE_RECORD_KEYS:
            raise DesignError(f"{label} classification-evidence shape drifted")

        blind_task_id = record.get("blind_task_id")
        repository_blind_id = record.get("repository_blind_id")
        if type(blind_task_id) is not str or BLIND_TASK_RE.fullmatch(blind_task_id) is None:
            raise DesignError(f"{label} blind task ID encoding drifted")
        if blind_task_id in blind_task_ids:
            raise DesignError("duplicate blind task ID in frozen manifest")
        blind_task_ids.add(blind_task_id)
        if type(repository_blind_id) is not str or BLIND_REPOSITORY_RE.fullmatch(repository_blind_id) is None:
            raise DesignError(f"{label} repository blind ID encoding drifted")
        if proof.get("blind_task_id") != blind_task_id:
            raise DesignError(f"{label} evidence registry blind-task binding drifted")

        task_identity = _require_sha256(record.get("task_identity_sha256"), f"{label} task identity")
        if task_identity in task_ids:
            raise DesignError("duplicate authoritative task identity in frozen manifest")
        task_ids.add(task_identity)

        identity_descriptor = proof.get("task_identity_descriptor")
        if not isinstance(identity_descriptor, dict) or set(identity_descriptor) != TASK_IDENTITY_DESCRIPTOR_KEYS:
            raise DesignError(f"{label} task-identity descriptor shape drifted")
        if identity_descriptor.get("algorithm_id") != "far-swe-v3-authoritative-task-identity-v1":
            raise DesignError(f"{label} task-identity algorithm drifted")
        provider = identity_descriptor.get("repository_provider")
        provider_id = identity_descriptor.get("repository_provider_id")
        if provider != "github.com" or type(provider_id) is not int or provider_id <= 0:
            raise DesignError(f"{label} authoritative repository identity drifted")
        canonical_url = identity_descriptor.get("canonical_repository_url")
        if type(canonical_url) is not str or re.fullmatch(r"https://github\.com/[^/]+/[^/]+", canonical_url) is None:
            raise DesignError(f"{label} canonical repository URL drifted")
        if canonical_url == "https://github.com/notfoundout/Project-FAR":
            raise DesignError("Project FAR repository is prohibited from the confirmatory task population")
        if type(identity_descriptor.get("repository_commit_sha")) is not str or re.fullmatch(r"[0-9a-f]{40}", identity_descriptor["repository_commit_sha"]) is None:
            raise DesignError(f"{label} repository commit identity drifted")
        _require_sha256(identity_descriptor.get("task_payload_sha256"), f"{label} task payload")
        if type(identity_descriptor.get("task_payload_bytes")) is not int or identity_descriptor["task_payload_bytes"] < 0:
            raise DesignError(f"{label} task payload byte count drifted")
        if _sha256(identity_descriptor) != task_identity:
            raise DesignError(f"{label} task_identity_sha256 recomputation mismatch")

        repository_identity = (provider, provider_id)
        prior_blind = identity_to_blind.setdefault(repository_identity, repository_blind_id)
        if prior_blind != repository_blind_id:
            raise DesignError("equal authoritative repository identities must use the same repository blind ID")
        prior_identity = blind_to_identity.setdefault(repository_blind_id, repository_identity)
        if prior_identity != repository_identity:
            raise DesignError("distinct authoritative repository identities must use distinct repository blind IDs")
        prior_url = identity_to_url.setdefault(repository_identity, canonical_url)
        if prior_url != canonical_url:
            raise DesignError("equal authoritative repository identities have inconsistent canonical repository URLs")
        repository_counts[repository_identity] = repository_counts.get(repository_identity, 0) + 1

        bundle_descriptor = proof.get("task_bundle_descriptor")
        if not isinstance(bundle_descriptor, dict) or set(bundle_descriptor) != TASK_BUNDLE_DESCRIPTOR_KEYS:
            raise DesignError(f"{label} task-bundle descriptor shape drifted")
        if bundle_descriptor.get("algorithm_id") != "far-swe-v3-task-bundle-root-v4" or bundle_descriptor.get("task_identity_sha256") != task_identity:
            raise DesignError(f"{label} task-bundle identity binding drifted")

        classification_descriptor = proof.get("classification_descriptor")
        classification_digest_value = _require_sha256(bundle_descriptor.get("classification_inputs_sha256"), f"{label} classification inputs")
        classification_digest.validate_descriptor(
            task_identity,
            classification_descriptor,
            classification_digest_value,
            evidence_root=evidence_root,
        )
        inputs = classification_descriptor["classification_inputs"]
        expected_strata = [STRATA_BY_INPUT[key] for key in classification_digest.CLASSIFICATION_INPUTS if inputs[key]]
        if not expected_strata:
            raise DesignError(f"{label} task strata cannot be empty")
        if record.get("task_strata") != expected_strata or bundle_descriptor.get("task_strata") != expected_strata:
            raise DesignError(f"{label} deterministic task-strata mapping drifted")
        observed_strata.update(expected_strata)

        bundle_root = _require_sha256(record.get("task_bundle_root_sha256"), f"{label} task bundle root")
        if bundle_root in bundle_roots:
            raise DesignError("duplicate task-bundle root in frozen manifest")
        bundle_roots.add(bundle_root)
        if _sha256(bundle_descriptor) != bundle_root:
            raise DesignError(f"{label} task_bundle_root_sha256 recomputation mismatch")

    _validate_population_contract(manifest, repository_counts, identity_to_blind, blind_to_identity)
    if observed_strata != set(STRATA_ORDER):
        missing = [item for item in STRATA_ORDER if item not in observed_strata]
        raise DesignError("required task-strata coverage missing: " + ", ".join(missing))


def launch_authorization_open(gate_path: Path | None = None) -> bool:
    """Return whether the governed gate claims any pilot/confirmatory launch authorization."""
    gate_path = gate_path or (integrity.HERE / "execution-gate-v1.0.json")
    data = _load_json_any(gate_path)
    if not isinstance(data, dict):
        raise DesignError("execution gate must be a JSON object")
    return any(data.get(key) is True for key in ("pilot_execution_authorized", "confirmatory_execution_authorized"))
