"""Prospective review-closure verifier for FAR-SWE-V3-001 amendment v1.2."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_integrity as integrity

DesignError = integrity.DesignError
HERE = Path(__file__).resolve().parent
AMENDMENT = HERE / "review-closure-amendment-v1.2.json"
NARRATIVE = HERE / "AMENDMENT-v1.2.md"
SEED = HERE / "bootstrap-seed-commitment-contract-v1.0.json"
PREREG = HERE / "preregistration-v1.0.json"
TASK = HERE / "task-manifest-contract-v1.0.json"
PLAN = HERE / "evidence-and-analysis-plan-v1.0.md"
GATE = HERE / "execution-gate-v1.0.json"
HIST_PREREG = HERE / "historical-base-83c951/preregistration-v1.0.json"
HIST_PLAN = HERE / "historical-base-83c951/evidence-and-analysis-plan-v1.0.md"

CURRENT_BLOBS = {
    "current_preregistration_git_blob_sha1": "b6664cf59ca7a2033c99f512e2b233601ad53d94",
    "current_task_manifest_contract_git_blob_sha1": "b160b713d3b1290f9580f96e1d9f88392a3275be",
    "current_seed_commitment_git_blob_sha1": "e5a9b94a0ccbce383cfbc7237d98e400af9d853d",
    "current_evidence_plan_git_blob_sha1": "04baff3069bc81f5a23fc2b92c5c04fec855b2c4",
    "current_execution_gate_git_blob_sha1": "99eabd1fee9a59770a3a61a07c151abcba23683f",
}
HISTORICAL = [
    (HIST_PREREG, "7147f6814f76eb0f73fd0741b17b2501e38e6f57"),
    (HIST_PLAN, "15b352d54a524d9caf827018b608028c004f8f13"),
]
SEED_INPUTS = [
    {
        "path": "research/external-validation/swe-agent-v3/treatment-capsule-contract-v1.0.json",
        "git_blob_sha1": "e011c8f9972a5682e03526f739437f62e973e76d",
    },
    {
        "path": "research/external-validation/swe-agent-v3/execution-gate-v1.0.json",
        "git_blob_sha1": "99eabd1fee9a59770a3a61a07c151abcba23683f",
    },
]
REQUIRED_STRATA = [
    "bug_fix",
    "test_failure",
    "behavioral_regression",
    "API_or_contract_change",
    "multi_file_change",
]


def _load(path: Path) -> dict[str, Any]:
    value = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(value, dict):
        raise DesignError(f"JSON object required: {path}")
    return value


def _blob(path: Path) -> str:
    return integrity._git_blob_sha1(integrity._read_regular(path))


def _current_blob(path: Path) -> str:
    relative = path.relative_to(integrity.ROOT).as_posix()
    return integrity._git_blob_sha1(integrity._committed_blob_bytes(relative))


def validate_historical_authority(data: dict[str, Any]) -> None:
    root = data.get("historical_authority_root")
    if not isinstance(root, dict) or root.get("base_design_head") != "83c951aca9be6a09a4517044ae531a3ed1bcc9a9":
        raise DesignError("historical authority head drifted")
    if "shallow checkouts require no historical Git object or ancestry relation" not in root.get("snapshot_rule", ""):
        raise DesignError("historical snapshot consumption rule drifted")
    expected = [
        {
            "path": "research/external-validation/swe-agent-v3/historical-base-83c951/preregistration-v1.0.json",
            "git_blob_sha1": HISTORICAL[0][1],
        },
        {
            "path": "research/external-validation/swe-agent-v3/historical-base-83c951/evidence-and-analysis-plan-v1.0.md",
            "git_blob_sha1": HISTORICAL[1][1],
        },
    ]
    if root.get("artifacts") != expected:
        raise DesignError("historical authority registry drifted")
    for path, expected_blob in HISTORICAL:
        if _blob(path) != expected_blob or _current_blob(path) != expected_blob:
            raise DesignError(f"historical snapshot drifted: {path.name}")
    hist_prereg = _load(HIST_PREREG)
    if hist_prereg.get("execution_authorized") is not False:
        raise DesignError("historical base execution boundary drifted")


def validate_authority(data: dict[str, Any]) -> None:
    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise DesignError("closure authority missing")
    for key, expected in CURRENT_BLOBS.items():
        if authority.get(key) != expected:
            raise DesignError(f"closure authority drifted: {key}")
    actual = {
        "current_preregistration_git_blob_sha1": _current_blob(PREREG),
        "current_task_manifest_contract_git_blob_sha1": _current_blob(TASK),
        "current_seed_commitment_git_blob_sha1": _current_blob(SEED),
        "current_evidence_plan_git_blob_sha1": _current_blob(PLAN),
        "current_execution_gate_git_blob_sha1": _current_blob(GATE),
    }
    if actual != CURRENT_BLOBS:
        raise DesignError("closure authority does not match current committed design artifacts")
    if authority.get("outcome_exposure_status") != "none":
        raise DesignError("closure amendment is not prospective")
    for key in (
        "model_calls_authorized",
        "pilot_execution_authorized",
        "benchmark_execution_authorized",
        "confirmatory_execution_authorized",
    ):
        if authority.get(key) is not False:
            raise DesignError(f"closure amendment opened execution boundary: {key}")


def validate_seed(data: dict[str, Any]) -> None:
    effective = data.get("bootstrap_seed_effective_contract")
    seed_contract = _load(SEED)
    if not isinstance(effective, dict) or effective.get("inputs") != SEED_INPUTS:
        raise DesignError("immutable seed inputs drifted")
    if seed_contract.get("derivation", {}).get("inputs") != SEED_INPUTS:
        raise DesignError("base seed contract input identities drifted")
    seed = effective.get("seed_hex")
    if seed != seed_contract.get("rng_contract", {}).get("seed_hex"):
        raise DesignError("seed value drifted")
    payload = (
        "FAR-SWE-V3-001/bootstrap-seed/v1\n"
        f"treatment_capsule_git_blob_sha1={SEED_INPUTS[0]['git_blob_sha1']}\n"
        f"execution_gate_git_blob_sha1={SEED_INPUTS[1]['git_blob_sha1']}\n"
    )
    if seed_contract.get("derivation", {}).get("canonical_payload") != payload:
        raise DesignError("seed canonical payload drifted")
    if hashlib.sha256(payload.encode("utf-8")).hexdigest() != seed:
        raise DesignError("seed recomputation failed")
    correction = effective.get("authority_correction", "")
    if "later prospective task-freeze correction" not in correction or "No outcome, grade, task identity, or run result contributed" not in correction:
        raise DesignError("seed authority correction drifted")


def validate_task_strata(data: dict[str, Any]) -> None:
    effective = data.get("task_manifest_effective_contract")
    if not isinstance(effective, dict) or effective.get("effective_schema_version") != "1.4":
        raise DesignError("effective task-manifest schema drifted")
    if effective.get("required_record_keys_exactly") != [
        "blind_task_id", "repository_blind_id", "task_stratum", "task_bundle_root_sha256"
    ]:
        raise DesignError("effective task record shape drifted")
    stratum = effective.get("task_stratum")
    if not isinstance(stratum, dict) or stratum.get("allowed_values_exactly") != REQUIRED_STRATA or stratum.get("operator_override_after_freeze_permitted") is not False:
        raise DesignError("task stratum contract drifted")
    prereg = _load(PREREG)
    if prereg.get("task_population", {}).get("required_strata") != REQUIRED_STRATA:
        raise DesignError("amended stratum values do not match preregistration")
    root = effective.get("task_bundle_root_extension")
    if not isinstance(root, dict) or root.get("algorithm_id") != "far-swe-v3-task-bundle-root-v3" or root.get("task_stratum_is_root_member") is not True:
        raise DesignError("stratum root-binding drifted")
    keys = root.get("descriptor_required_keys_exactly")
    if not isinstance(keys, list) or "task_stratum" not in keys or len(keys) != 8:
        raise DesignError("stratum descriptor shape drifted")
    validations = effective.get("preexecution_validation_extension")
    required = {
        "every manifest record has exactly one allowed task_stratum value",
        "every preregistered required stratum appears in at least one frozen confirmatory task",
        "task_stratum is included in the canonical task-bundle descriptor and therefore in task_bundle_root_sha256",
        "stratum labels and task-bundle roots are committed before any sacrificial pilot or confirmatory execution",
    }
    if not isinstance(validations, list) or set(validations) != required:
        raise DesignError("stratum preexecution validation drifted")


def validate_critical_harm(data: dict[str, Any]) -> None:
    harm = data.get("critical_harm_threshold_contract")
    if not isinstance(harm, dict) or harm.get("freeze_status") != "frozen_pre_execution":
        raise DesignError("critical-harm threshold contract is not frozen")
    zero = harm.get("zero_tolerance_harms")
    if zero != [
        "authorization or information-barrier violation",
        "hidden task leakage",
        "unmatched tool, context, or budget access",
        "evidence loss preventing independent verification",
    ]:
        raise DesignError("zero-tolerance harm contract drifted")
    rate = harm.get("rate_harms")
    if not isinstance(rate, dict) or set(rate) != {"regression_introduction", "invalid_run_rate"}:
        raise DesignError("rate-harm contract shape drifted")
    for label, contract in rate.items():
        if not isinstance(contract, dict) or contract.get("contrast") != "FAR rate minus placebo rate":
            raise DesignError(f"harm contrast drifted: {label}")
        if contract.get("threshold") != {"numerator": 1, "denominator": 10}:
            raise DesignError(f"harm threshold drifted: {label}")
        if "greater than or equal to 1/10" not in contract.get("trigger_rule", ""):
            raise DesignError(f"harm trigger drifted: {label}")
    if "triggers critical_harm" not in harm.get("missing_harm_evidence_rule", ""):
        raise DesignError("missing harm evidence fail-closed rule drifted")
    if harm.get("classification_effect") != "critical_harm vetoes bounded_positive and cannot be overridden by efficacy estimates":
        raise DesignError("critical-harm classification effect drifted")
    retained = harm.get("retained_evidence")
    if not isinstance(retained, list) or len(retained) != 5:
        raise DesignError("critical-harm evidence retention drifted")
    gate = data.get("execution_gate_extension")
    if not isinstance(gate, dict) or gate.get("all_gates_required") is not True or gate.get("current_execution_authorized") is not False:
        raise DesignError("closure execution-gate extension drifted")
    if len(gate.get("pilot_prerequisites", [])) != 3 or len(gate.get("confirmatory_prerequisites", [])) != 3:
        raise DesignError("closure gate prerequisites drifted")


def validate_narrative_and_nonclaims(data: dict[str, Any]) -> None:
    nonclaims = data.get("nonclaims")
    required = {
        "This amendment does not establish that FAR improves software engineering.",
        "This amendment does not authorize model calls, pilot execution, benchmark execution, confirmatory execution, grading, or outcome reveal.",
        "This amendment does not change accepted Project FAR theory or release any theory or empirical claim.",
        "The historical snapshot artifacts are immutable authority copies, not newly generated evidence.",
    }
    if not isinstance(nonclaims, list) or set(nonclaims) != required:
        raise DesignError("closure nonclaims drifted")
    narrative = integrity._read_regular(NARRATIVE).decode("utf-8")
    for phrase in (
        "Execution authorized: **No**",
        "No historical Git object, full clone, merge-base relation, or network fetch is required.",
        "must contain exactly four keys",
        "critical_harm` is triggered when either exact rate difference is at least `1/10`",
        "Current execution remains blocked.",
    ):
        if phrase not in narrative:
            raise DesignError("closure narrative boundary drifted")


def validate(path: Path = AMENDMENT) -> dict[str, Any]:
    data = _load(path)
    if (
        data.get("schema_version"),
        data.get("program_id"),
        data.get("artifact_status"),
        data.get("amendment_status"),
    ) != ("1.2", "FAR-SWE-V3-001", "Research", "prospective_pre_execution_correction"):
        raise DesignError("closure amendment identity drifted")
    validate_authority(data)
    validate_historical_authority(data)
    validate_seed(data)
    validate_task_strata(data)
    validate_critical_harm(data)
    validate_narrative_and_nonclaims(data)
    return data


if __name__ == "__main__":
    try:
        validate()
    except DesignError as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: review-closure amendment v1.2 is prospective, rooted, deterministic, and execution remains blocked.")
