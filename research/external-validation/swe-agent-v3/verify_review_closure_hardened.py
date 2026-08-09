"""Required additive hardening for FAR-SWE-V3-001 review-closure amendment v1.2."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import verify_integrity as integrity
import verify_review_closure_v1_2 as base
import verify_classification_input_digest_contract as classification_digest

DesignError = integrity.DesignError
AMENDMENT = base.AMENDMENT
EXPECTED_TIMING = (
    "computed from the frozen classification inputs and committed before any sacrificial pilot or confirmatory execution"
)
EXPECTED_AMENDMENT_BLOB = "59c862790fee90beb0b3fba93dfd9b4e51921322"
EXPECTED_NARRATIVE_BLOB = "6089f31d1769349fc1e9f9588ad40dca9e775fef"


def validate(path: Path | None = None) -> dict[str, Any]:
    """Validate hardening against the caller's active repository/fixture root."""
    path = path or (integrity.HERE / "review-closure-amendment-v1.2.json")
    narrative = integrity.HERE / "AMENDMENT-v1.2.md"
    classification_contract = integrity.HERE / "classification-input-digest-contract-v1.0.json"
    if integrity._git_blob_sha1(integrity._read_regular(path)) != EXPECTED_AMENDMENT_BLOB:
        raise DesignError("frozen review-closure amendment bytes drifted")
    if integrity._git_blob_sha1(integrity._read_regular(narrative)) != EXPECTED_NARRATIVE_BLOB:
        raise DesignError("frozen review-closure narrative bytes drifted")
    data = base.validate(path)
    effective = data.get("task_manifest_effective_contract")
    if not isinstance(effective, dict):
        raise DesignError("effective task-manifest contract missing")
    strata = effective.get("task_strata")
    if not isinstance(strata, dict) or strata.get("classification_timing") != EXPECTED_TIMING:
        raise DesignError("task-stratum classification timing drifted")
    classification_digest.validate_contract(classification_contract)
    return data


if __name__ == "__main__":
    try:
        validate()
    except DesignError as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: frozen v1.2 and additive task-bound classification-input hardening verify; execution remains blocked.")
