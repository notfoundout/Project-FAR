"""Exact semantic hardening for FAR-SWE-V3-001 review-closure amendment v1.2."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import verify_integrity as integrity
import verify_review_closure_v1_2 as base

DesignError = integrity.DesignError
AMENDMENT = base.AMENDMENT
EXPECTED_TIMING = (
    "computed from the frozen classification inputs and committed before any sacrificial pilot or confirmatory execution"
)
EXPECTED_DIGEST_CONTRACT = {
    "algorithm_id": "far-swe-v3-classification-input-digest-v1",
    "descriptor_required_keys_exactly": ["algorithm_id", "classification_inputs", "evidence_bindings"],
    "classification_input_keys_exactly": base.CLASSIFICATION_INPUTS,
    "classification_input_value_type": "exact JSON boolean; numeric 0/1 is prohibited",
    "evidence_binding_keys_exactly_match_classification_inputs": True,
    "evidence_binding_schema": {
        "required_keys_exactly": ["kind", "locator"],
        "kind_allowed_values_exactly": [
            "source_evidence_locator",
            "sealed_reference_patch_attestation",
            "unverifiable",
        ],
        "locator_rule": (
            "nonempty UTF-8 JSON string for source_evidence_locator or sealed_reference_patch_attestation; "
            "exact JSON null for unverifiable"
        ),
    },
    "unverifiable_binding_rule": (
        "an unverifiable binding forces its classification input to false and cannot support required-stratum coverage"
    ),
    "serialization": "RFC 8785 JCS UTF-8 bytes of exactly the descriptor defined above",
    "digest": "lowercase SHA-256 hex",
    "timing": (
        "descriptor bytes and classification_inputs_sha256 are committed before any sacrificial pilot or confirmatory execution"
    ),
    "recomputation_rule": (
        "preexecution validation independently recomputes classification_inputs_sha256 from the exact descriptor and rejects any mismatch"
    ),
}
EXPECTED_PREEXECUTION = [
    "every manifest record has exactly the five required keys",
    "task_identity_sha256 is recomputed from the authoritative repository/commit/payload descriptor and is unique across the frozen manifest independently of task_strata",
    "classification_inputs_sha256 is independently recomputed from the exact frozen classification-input descriptor including evidence bindings and must match",
    "task_strata is nonempty, duplicate-free, contains only allowed labels, and is in canonical order",
    "task_strata exactly equals the deterministic mapping from the frozen classification inputs",
    "every preregistered required stratum appears in at least one frozen confirmatory task",
    "task_identity_sha256, task_strata, classification inputs, evidence bindings, and task-bundle roots are committed before any sacrificial pilot or confirmatory execution",
]


def _load(path: Path) -> dict[str, Any]:
    value = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(value, dict):
        raise DesignError("review-closure amendment must be object")
    return value


def validate(path: Path = AMENDMENT) -> dict[str, Any]:
    data = base.validate(path)
    effective = data.get("task_manifest_effective_contract")
    if not isinstance(effective, dict):
        raise DesignError("effective task-manifest contract missing")
    strata = effective.get("task_strata")
    if not isinstance(strata, dict) or strata.get("classification_timing") != EXPECTED_TIMING:
        raise DesignError("task-stratum classification timing drifted")
    if effective.get("classification_input_digest_contract") != EXPECTED_DIGEST_CONTRACT:
        raise DesignError("classification-input digest contract drifted")
    if effective.get("preexecution_validation_extension") != EXPECTED_PREEXECUTION:
        raise DesignError("classification-input preexecution validation drifted")
    return data


if __name__ == "__main__":
    try:
        validate()
    except DesignError as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: review-closure v1.2 timing and classification-input digest semantics are exact; execution blocked.")
