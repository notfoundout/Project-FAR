"""Prospective additive classification-input digest authority for FAR-SWE-V3-001."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import verify_integrity as integrity

DesignError = integrity.DesignError
HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "classification-input-digest-contract-v1.0.json"

CLASSIFICATION_INPUTS = [
    "source_declares_defect_or_bug",
    "frozen_entry_test_or_CI_is_failing",
    "source_declares_previously_working_behavior_regressed",
    "source_acceptance_criteria_require_API_or_contract_change",
    "sealed_reference_patch_touches_multiple_files",
]
EXPECTED_TIMING = (
    "computed from the frozen classification inputs and committed before any sacrificial pilot or confirmatory execution"
)
EXPECTED_DESCRIPTOR_KEYS = [
    "algorithm_id",
    "task_identity_sha256",
    "classification_inputs",
    "evidence_bindings",
]
EXPECTED_BINDING_KINDS = [
    "source_evidence_locator",
    "sealed_reference_patch_attestation",
    "unverifiable",
]


def _load(path: Path = CONTRACT) -> dict[str, Any]:
    value = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(value, dict):
        raise DesignError("classification-input digest contract must be object")
    return value


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def validate_contract(path: Path = CONTRACT) -> dict[str, Any]:
    data = _load(path)
    if set(data) != {"schema_version","program_id","artifact_status","contract_status","authority","digest_contract","frozen_v1_2_interpretation","preexecution_requirements","nonclaims"}:
        raise DesignError("classification-input digest contract top-level shape drifted")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("contract_status")) != ("1.0","FAR-SWE-V3-001","Research","prospective_pre_execution_additive_hardening"):
        raise DesignError("classification-input digest contract identity/status drifted")
    authority = data.get("authority")
    if not isinstance(authority, dict) or authority.get("frozen_review_closure_amendment_git_blob_sha1") != "59c862790fee90beb0b3fba93dfd9b4e51921322" or authority.get("supersedes_or_rewrites_frozen_v1_2_bytes") is not False or authority.get("outcome_exposure_status") != "none" or authority.get("accepted_theory_change") is not False:
        raise DesignError("classification-input digest authority drifted")
    for key in ("model_calls_authorized","pilot_execution_authorized","benchmark_execution_authorized","confirmatory_execution_authorized"):
        if authority.get(key) is not False:
            raise DesignError(f"classification-input digest contract opened execution boundary: {key}")
    digest = data.get("digest_contract")
    if not isinstance(digest, dict) or digest.get("algorithm_id") != "far-swe-v3-classification-input-digest-v2" or digest.get("descriptor_required_keys_exactly") != EXPECTED_DESCRIPTOR_KEYS or digest.get("classification_input_keys_exactly") != CLASSIFICATION_INPUTS or digest.get("classification_input_value_type") != "exact JSON boolean; numeric 0/1 is prohibited" or digest.get("evidence_binding_keys_exactly_match_classification_inputs") is not True:
        raise DesignError("classification-input digest semantics drifted")
    if digest.get("task_identity_sha256") != {"type":"lowercase 64-character SHA-256 hex JSON string","binding_rule":"must exactly equal the task manifest record task_identity_sha256 for the same record","cross_task_transplantation_permitted":False}:
        raise DesignError("classification-input task-identity binding drifted")
    if digest.get("evidence_binding_schema") != {"required_keys_exactly":["kind","locator"],"kind_allowed_values_exactly":EXPECTED_BINDING_KINDS,"locator_rule":"nonempty UTF-8 JSON string for source_evidence_locator or sealed_reference_patch_attestation; exact JSON null for unverifiable"}:
        raise DesignError("classification-input evidence-binding schema drifted")
    if digest.get("unverifiable_binding_rule") != "an unverifiable binding forces its paired classification input to false and cannot support required-stratum coverage" or digest.get("serialization") != "RFC 8785 JCS UTF-8 bytes of exactly the descriptor defined above" or digest.get("digest") != "lowercase SHA-256 hex" or digest.get("timing") != "descriptor bytes and classification_inputs_sha256 are committed before any sacrificial pilot or confirmatory execution and before outcome reveal":
        raise DesignError("classification-input digest rule drifted")
    if digest.get("recomputation_rule") != "preexecution validation independently recomputes classification_inputs_sha256 from the exact descriptor, verifies task_identity_sha256 equality to the enclosing manifest record, and rejects any mismatch":
        raise DesignError("classification-input digest recomputation rule drifted")
    interpretation = data.get("frozen_v1_2_interpretation")
    if not isinstance(interpretation, dict) or interpretation.get("classification_timing_exactly") != EXPECTED_TIMING:
        raise DesignError("frozen v1.2 classification-input interpretation drifted")
    return data


def validate_descriptor(enclosing_task_identity_sha256: str, descriptor: dict[str, Any], expected_digest: str) -> str:
    validate_contract()
    if type(enclosing_task_identity_sha256) is not str or re.fullmatch(r"[0-9a-f]{64}", enclosing_task_identity_sha256) is None:
        raise DesignError("enclosing task identity must be lowercase SHA-256 hex")
    if not isinstance(descriptor, dict) or list(descriptor.keys()) != EXPECTED_DESCRIPTOR_KEYS:
        raise DesignError("classification-input descriptor shape/order drifted")
    if descriptor.get("algorithm_id") != "far-swe-v3-classification-input-digest-v2" or descriptor.get("task_identity_sha256") != enclosing_task_identity_sha256:
        raise DesignError("classification-input descriptor transplanted across task identity")
    inputs = descriptor.get("classification_inputs")
    if not isinstance(inputs, dict) or list(inputs.keys()) != CLASSIFICATION_INPUTS or any(type(inputs[k]) is not bool for k in CLASSIFICATION_INPUTS):
        raise DesignError("classification inputs must be exact JSON booleans with exact keys")
    bindings = descriptor.get("evidence_bindings")
    if not isinstance(bindings, dict) or list(bindings.keys()) != CLASSIFICATION_INPUTS:
        raise DesignError("classification-input evidence-binding key set/order drifted")
    for key in CLASSIFICATION_INPUTS:
        item = bindings.get(key)
        if not isinstance(item, dict) or list(item.keys()) != ["kind","locator"]:
            raise DesignError(f"classification-input evidence binding shape drifted: {key}")
        kind, locator = item.get("kind"), item.get("locator")
        if kind not in EXPECTED_BINDING_KINDS:
            raise DesignError(f"classification-input evidence binding kind drifted: {key}")
        if kind == "unverifiable":
            if locator is not None or inputs[key] is not False:
                raise DesignError(f"unverifiable classification input must be false with null locator: {key}")
        elif type(locator) is not str or not locator:
            raise DesignError(f"verified classification input requires nonempty evidence locator: {key}")
    if type(expected_digest) is not str or re.fullmatch(r"[0-9a-f]{64}", expected_digest) is None:
        raise DesignError("classification_inputs_sha256 encoding drifted")
    actual = hashlib.sha256(_canonical_json(descriptor)).hexdigest()
    if actual != expected_digest:
        raise DesignError("classification_inputs_sha256 recomputation mismatch")
    return actual


if __name__ == "__main__":
    try:
        validate_contract()
    except DesignError as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: prospective classification-input digest authority is exact, task-bound, and execution remains blocked.")
