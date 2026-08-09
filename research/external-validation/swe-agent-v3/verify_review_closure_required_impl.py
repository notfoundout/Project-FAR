"""Required implementation for frozen v1.2 plus additive prospective hardening."""
from __future__ import annotations

from pathlib import Path

import verify_review_closure_v1_2_legacy as legacy
import verify_classification_input_digest_contract as classification_digest

DesignError = legacy.DesignError
AMENDMENT = legacy.AMENDMENT
NARRATIVE = legacy.NARRATIVE
SEED_INPUTS = legacy.SEED_INPUTS
CLASSIFICATION_INPUTS = legacy.CLASSIFICATION_INPUTS
# Public frozen-contract constants remain part of the required verifier API.
# Re-export them explicitly so the additive wrapper cannot silently break the
# mutation suite or downstream verification code while semantics stay frozen.
HISTORICAL = legacy.HISTORICAL
TASK_IDENTITY_KEYS = legacy.TASK_IDENTITY_KEYS
TASK_BUNDLE_KEYS = legacy.TASK_BUNDLE_KEYS
REQUIRED_STRATA = legacy.REQUIRED_STRATA
CLASSIFICATION_MAPPING = legacy.CLASSIFICATION_MAPPING
CLASSIFICATION_EVIDENCE_RULE = legacy.CLASSIFICATION_EVIDENCE_RULE
PILOT_PREREQUISITES = legacy.PILOT_PREREQUISITES
CONFIRMATORY_PREREQUISITES = legacy.CONFIRMATORY_PREREQUISITES
EXPECTED_TIMING = "computed from the frozen classification inputs and committed before any sacrificial pilot or confirmatory execution"
EXPECTED_AMENDMENT_BLOB = "59c862790fee90beb0b3fba93dfd9b4e51921322"
EXPECTED_NARRATIVE_BLOB = "6089f31d1769349fc1e9f9588ad40dca9e775fef"


def validate(path: Path = AMENDMENT):
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
