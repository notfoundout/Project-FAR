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
