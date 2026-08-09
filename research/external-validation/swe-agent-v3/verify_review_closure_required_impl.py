"""Required implementation for frozen v1.2 plus additive prospective hardening."""
from __future__ import annotations

from pathlib import Path

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


def _sync_integrity_context() -> None:
    """Keep the frozen validator on the caller's active committed-byte source."""
    legacy.integrity.ROOT = integrity.ROOT
    legacy.integrity.HERE = integrity.HERE
    legacy.integrity.MANIFEST = integrity.MANIFEST
    legacy.integrity._committed_blob_bytes = integrity._committed_blob_bytes


def validate(path: Path = AMENDMENT):
    _sync_integrity_context()
    if legacy._blob(path) != EXPECTED_AMENDMENT_BLOB:
        raise DesignError("frozen review-closure amendment bytes drifted")
    if legacy._blob(NARRATIVE) != EXPECTED_NARRATIVE_BLOB:
        raise DesignError("frozen review-closure narrative bytes drifted")
    data = legacy.validate(path)
    effective = data.get("task_manifest_effective_contract")
    if not isinstance(effective, dict):
        raise DesignError("effective task-manifest contract missing")
    strata = effective.get("task_strata")
    if not isinstance(strata, dict) or strata.get("classification_timing") != EXPECTED_TIMING:
        raise DesignError("task-stratum classification timing drifted")
    classification_digest.validate_contract()
    return data
