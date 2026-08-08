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
REPO_ROOT = HERE.parents[2]
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
TASK_IDENTITY_KEYS = [
    "algorithm_id",
    "repository_provider",
    "repository_provider_id",
    "canonical_repository_url",
    "repository_commit_sha",
    "task_payload_sha256",
    "task_payload_bytes",
]
TASK_BUNDLE_KEYS = [
    "algorithm_id",
    "task_identity_sha256",
    "task_strata",
    "classification_inputs_sha256",
]
CLASSIFICATION_INPUTS = [
    "source_declares_defect_or_bug",
    "frozen_entry_test_or_CI_is_failing",
    "source_declares_previously_working_behavior_regressed",
    "source_acceptance_criteria_require_API_or_contract_change",
    "sealed_reference_patch_touches_multiple_files",
]
CLASSIFICATION_MAPPING = {
    "bug_fix": "include iff source_declares_defect_or_bug is true",
    "test_failure": "include iff frozen_entry_test_or_CI_is_failing is true",
    "behavioral_regression": "include iff source_declares_previously_working_behavior_regressed is true",
    "API_or_contract_change": "include iff source_acceptance_criteria_require_API_or_contract_change is true",
    "multi_file_change": "include iff sealed_reference_patch_touches_multiple_files is true",
}
PILOT_PREREQUISITES = [
    "review-closure-amendment-v1.2.json is committed, manifest-rooted, and verified",
    "task-manifest v1.5 implementation enforces unique authoritative task_identity_sha256 independently of strata and deterministic multi-label stratum classification before any manifest is instantiated",
    "critical_harm_threshold_contract including exact repetition-slot event, denominator, pairing, replacement, and retained-evidence rules is frozen and verified",
]
CONFIRMATORY_PREREQUISITES = [
    "all pilot prerequisites remain satisfied",
    "the frozen confirmatory task manifest proves unique authoritative task identities and coverage of every required task stratum under the deterministic classifier",
    "the frozen harm-evidence schema retains every required comparison-index, slot, numerator, denominator, rational-difference, zero-tolerance, and trigger record before execution",
]


def _load(path: Path) -> dict[str, Any]:
    value = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(value, dict):
        raise DesignError(f"JSON object required: {path}")
    return value


def _blob(path: Path) -> str:
    return integrity._git_blob_sha1(integrity._read_regular(path))


def _current_blob(path: Path) -> str:
    relative = path.relative_to(REPO_ROOT).as_posix()
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
    expected_subjects = [
        "bootstrap-seed authority narrative and verifier binding to mutable current-manifest inputs",
        "task-manifest record schema, authoritative task identity, and deterministic required-strata classification",
        "critical-harm threshold, repetition-slot event construction, and launch-gate specification",
    ]
    if authority.get("superseded_subjects") != expected_subjects:
        raise DesignError("closure superseded-subject registry drifted")
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
    if not isinstance(effective, dict) or effective.get("effective_schema_version") != "1.5":
        raise DesignError("effective task-manifest schema drifted")
    if effective.get("required_record_keys_exactly") != [
        "blind_task_id",
        "repository_blind_id",
        "task_strata",
        "task_identity_sha256",
        "task_bundle_root_sha256",
    ]:
        raise DesignError("effective task record shape drifted")

    identity = effective.get("task_identity_contract")
    if not isinstance(identity, dict):
        raise DesignError("authoritative task identity contract missing")
    if identity.get("algorithm_id") != "far-swe-v3-authoritative-task-identity-v1":
        raise DesignError("task identity algorithm drifted")
    if identity.get("descriptor_required_keys_exactly") != TASK_IDENTITY_KEYS:
        raise DesignError("task identity descriptor keys drifted")
    if identity.get("serialization") != "RFC 8785 JCS UTF-8 bytes" or identity.get("digest") != "lowercase SHA-256 hex":
        raise DesignError("task identity serialization drifted")
    if identity.get("strata_excluded_from_identity") is not True:
        raise DesignError("task identity improperly depends on strata")
    uniqueness = identity.get("uniqueness_rule", "")
    if "must be unique across the frozen manifest" not in uniqueness or "regardless of strata" not in uniqueness:
        raise DesignError("task uniqueness rule drifted")

    strata = effective.get("task_strata")
    if not isinstance(strata, dict):
        raise DesignError("task strata contract missing")
    if strata.get("type") != "nonempty JSON array of strings":
        raise DesignError("task strata type drifted")
    if strata.get("allowed_values_exactly") != REQUIRED_STRATA or strata.get("canonical_order") != REQUIRED_STRATA:
        raise DesignError("task strata value/order contract drifted")
    if strata.get("operator_override_after_freeze_permitted") is not False:
        raise DesignError("post-freeze stratum override opened")
    if strata.get("classification_inputs_required") != CLASSIFICATION_INPUTS:
        raise DesignError("task stratum classification inputs drifted")
    if strata.get("deterministic_mapping") != CLASSIFICATION_MAPPING:
        raise DesignError("task stratum deterministic mapping drifted")
    if "absent or unverifiable evidence forces false" not in strata.get("evidence_rule", ""):
        raise DesignError("task stratum evidence rule drifted")
    if strata.get("multi_label_rule") != (
        "retain every label whose deterministic predicate is true, exactly once, in canonical_order; "
        "no primary-label choice or precedence is permitted"
    ):
        raise DesignError("task stratum multi-label rule drifted")

    prereg = _load(PREREG)
    if prereg.get("task_population", {}).get("required_strata") != REQUIRED_STRATA:
        raise DesignError("amended stratum values do not match preregistration")

    root = effective.get("task_bundle_root_extension")
    if not isinstance(root, dict) or root.get("algorithm_id") != "far-swe-v3-task-bundle-root-v4":
        raise DesignError("task bundle root extension drifted")
    if root.get("descriptor_required_keys_exactly") != TASK_BUNDLE_KEYS:
        raise DesignError("effective task bundle descriptor keys drifted")
    if root.get("task_identity_sha256_is_root_member") is not True:
        raise DesignError("task identity not bound into task bundle root")
    if root.get("task_strata_are_root_members") is not True:
        raise DesignError("task strata not bound into task bundle root")
    if root.get("classification_inputs_sha256_is_root_member") is not True:
        raise DesignError("classification inputs not bound into task bundle root")

    expected_validations = [
        "every manifest record has exactly the five required keys",
        "task_identity_sha256 is recomputed from the authoritative repository/commit/payload descriptor and is unique across the frozen manifest independently of task_strata",
        "task_strata is nonempty, duplicate-free, contains only allowed labels, and is in canonical order",
        "task_strata exactly equals the deterministic mapping from the frozen classification inputs",
        "every preregistered required stratum appears in at least one frozen confirmatory task",
        "task_identity_sha256, task_strata, classification inputs, and task-bundle roots are committed before any sacrificial pilot or confirmatory execution",
    ]
    if effective.get("preexecution_validation_extension") != expected_validations:
        raise DesignError("task preexecution validation contract drifted")


def validate_critical_harm(data: dict[str, Any]) -> None:
    harm = data.get("critical_harm_threshold_contract")
    if not isinstance(harm, dict) or harm.get("freeze_status") != "frozen_pre_execution":
        raise DesignError("critical-harm threshold contract is not frozen")
    if harm.get("comparison_index") != "identical frozen task x repetition-slot indexes for FAR and placebo":
        raise DesignError("harm comparison index drifted")
    if harm.get("replacement_rule") != (
        "an allowed infrastructure replacement occupies the same frozen repetition slot; "
        "the superseded attempt is retained as evidence but never creates an additional denominator slot"
    ):
        raise DesignError("harm replacement rule drifted")
    if harm.get("pairing_rule") != (
        "FAR and placebo must have the identical frozen repetition-slot denominator and one terminal slot record per index; "
        "any missing, duplicated, or unpaired slot triggers critical_harm"
    ):
        raise DesignError("harm pairing rule drifted")
    if harm.get("exact_arithmetic") != (
        "all arm rates and FAR-minus-placebo differences are exact reduced rationals; floating point, "
        "complete-case dropping, and displayed decimals are never decision inputs"
    ):
        raise DesignError("harm exact-arithmetic rule drifted")
    if harm.get("zero_tolerance_harms") != [
        "authorization or information-barrier violation",
        "hidden task leakage",
        "unmatched tool, context, or budget access",
        "evidence loss preventing independent verification",
    ]:
        raise DesignError("zero-tolerance harm contract drifted")
    if harm.get("zero_tolerance_rule") != "one or more verified occurrences triggers critical_harm":
        raise DesignError("zero-tolerance trigger drifted")

    rate = harm.get("rate_harms")
    if not isinstance(rate, dict) or set(rate) != {"regression_introduction", "invalid_run_rate"}:
        raise DesignError("rate-harm contract shape drifted")
    expected = {
        "regression_introduction": {
            "unit": "frozen repetition slot",
            "event_rule": "slot indicator is 1 iff the sealed grader records one or more regressions introduced by that arm in the terminal slot result; otherwise 0",
            "numerator_rule": "sum the exact 0/1 slot indicators over every frozen repetition slot for the arm",
            "denominator_rule": "the total number of frozen repetition slots for that arm on the identical frozen FAR/placebo comparison index, including slots whose terminal outcome is invalid",
            "contrast": "FAR exact rate minus placebo exact rate",
            "threshold": {"numerator": 1, "denominator": 10},
            "trigger_rule": "critical_harm iff the exact repetition-slot rate difference is greater than or equal to 1/10",
        },
        "invalid_run_rate": {
            "unit": "frozen repetition slot",
            "event_rule": "slot indicator is 1 iff the terminal outcome for that frozen slot is invalid after any permitted same-slot infrastructure replacement; otherwise 0",
            "numerator_rule": "sum the exact 0/1 invalid indicators over every frozen repetition slot for the arm",
            "denominator_rule": "the total number of frozen repetition slots for that arm on the identical frozen FAR/placebo comparison index; invalid slots remain in the denominator and are never dropped",
            "contrast": "FAR exact rate minus placebo exact rate",
            "threshold": {"numerator": 1, "denominator": 10},
            "trigger_rule": "critical_harm iff the exact repetition-slot rate difference is greater than or equal to 1/10",
        },
    }
    if rate != expected:
        raise DesignError("rate-harm event/denominator contract drifted")
    if harm.get("missing_harm_evidence_rule") != (
        "missing or unverifiable evidence required to evaluate any zero-tolerance event, slot indicator, pairing identity, "
        "numerator, or denominator triggers critical_harm rather than silently passing the veto"
    ):
        raise DesignError("missing harm evidence fail-closed rule drifted")
    if harm.get("classification_effect") != "critical_harm vetoes bounded_positive and cannot be overridden by efficacy estimates":
        raise DesignError("critical-harm classification effect drifted")
    if harm.get("retained_evidence") != [
        "the frozen comparison index and every task/repetition-slot identity",
        "original and replacement attempt records for any replaced infrastructure-invalid slot",
        "per-slot regression-introduction and invalid-run indicators with sealed-grader or terminal-status evidence",
        "exact numerators and denominators for FAR and placebo for each rate harm",
        "exact reduced-rational FAR-minus-placebo harm-rate differences and 1/10 comparison results",
        "zero-tolerance violation records",
        "final critical_harm boolean and triggering criterion identifiers",
    ]:
        raise DesignError("critical-harm evidence retention drifted")

    gate = data.get("execution_gate_extension")
    if not isinstance(gate, dict):
        raise DesignError("closure execution-gate extension missing")
    if gate.get("pilot_prerequisites") != PILOT_PREREQUISITES:
        raise DesignError("pilot prerequisite contents drifted")
    if gate.get("confirmatory_prerequisites") != CONFIRMATORY_PREREQUISITES:
        raise DesignError("confirmatory prerequisite contents drifted")
    if gate.get("all_gates_required") is not True or gate.get("current_execution_authorized") is not False:
        raise DesignError("closure execution-gate boundary drifted")


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
        "`task_identity_sha256` excludes strata",
        "retain every matching stratum",
        "frozen repetition slot",
        "invalid slots remain in the denominator",
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
