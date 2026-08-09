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
HISTORICAL = [(HIST_PREREG, "7147f6814f76eb0f73fd0741b17b2501e38e6f57"),(HIST_PLAN, "15b352d54a524d9caf827018b608028c004f8f13")]
SEED_INPUTS = [
    {"path":"research/external-validation/swe-agent-v3/treatment-capsule-contract-v1.0.json","git_blob_sha1":"e011c8f9972a5682e03526f739437f62e973e76d"},
    {"path":"research/external-validation/swe-agent-v3/execution-gate-v1.0.json","git_blob_sha1":"99eabd1fee9a59770a3a61a07c151abcba23683f"},
]
REQUIRED_STRATA = ["bug_fix","test_failure","behavioral_regression","API_or_contract_change","multi_file_change"]
TASK_IDENTITY_KEYS = ["algorithm_id","repository_provider","repository_provider_id","canonical_repository_url","repository_commit_sha","task_payload_sha256","task_payload_bytes"]
TASK_BUNDLE_KEYS = ["algorithm_id","task_identity_sha256","task_strata","classification_inputs_sha256"]
CLASSIFICATION_INPUTS = ["source_declares_defect_or_bug","frozen_entry_test_or_CI_is_failing","source_declares_previously_working_behavior_regressed","source_acceptance_criteria_require_API_or_contract_change","sealed_reference_patch_touches_multiple_files"]
CLASSIFICATION_MAPPING = {
    "bug_fix":"include iff source_declares_defect_or_bug is true",
    "test_failure":"include iff frozen_entry_test_or_CI_is_failing is true",
    "behavioral_regression":"include iff source_declares_previously_working_behavior_regressed is true",
    "API_or_contract_change":"include iff source_acceptance_criteria_require_API_or_contract_change is true",
    "multi_file_change":"include iff sealed_reference_patch_touches_multiple_files is true",
}
CLASSIFICATION_EVIDENCE_RULE = "each classification input is a frozen JSON boolean with a retained source-evidence locator or sealed-reference-patch attestation; absent or unverifiable evidence forces false, except any required-stratum coverage claim relying on unverifiable evidence fails the launch gate"
PILOT_PREREQUISITES = ["review-closure-amendment-v1.2.json is committed, manifest-rooted, and verified","task-manifest v1.5 implementation enforces unique authoritative task_identity_sha256 independently of strata and deterministic multi-label stratum classification before any manifest is instantiated","critical_harm_threshold_contract including exact repetition-slot event, denominator, pairing, replacement, and retained-evidence rules is frozen and verified"]
CONFIRMATORY_PREREQUISITES = ["all pilot prerequisites remain satisfied","the frozen confirmatory task manifest proves unique authoritative task identities and coverage of every required task stratum under the deterministic classifier","the frozen harm-evidence schema retains every required comparison-index, slot, numerator, denominator, rational-difference, zero-tolerance, and trigger record before execution"]


def _load(path: Path) -> dict[str, Any]:
    value = integrity._decode_json(integrity._read_regular(path), str(path))
    if not isinstance(value, dict): raise DesignError(f"JSON object required: {path}")
    return value

def _blob(path: Path) -> str: return integrity._git_blob_sha1(integrity._read_regular(path))
def _current_blob(path: Path) -> str:
    relative = path.relative_to(REPO_ROOT).as_posix(); return integrity._git_blob_sha1(integrity._committed_blob_bytes(relative))

def validate_historical_authority(data):
    root=data.get("historical_authority_root")
    if not isinstance(root,dict) or root.get("base_design_head")!="83c951aca9be6a09a4517044ae531a3ed1bcc9a9": raise DesignError("historical authority head drifted")
    if "shallow checkouts require no historical Git object or ancestry relation" not in root.get("snapshot_rule",""): raise DesignError("historical snapshot consumption rule drifted")
    expected=[{"path":"research/external-validation/swe-agent-v3/historical-base-83c951/preregistration-v1.0.json","git_blob_sha1":HISTORICAL[0][1]},{"path":"research/external-validation/swe-agent-v3/historical-base-83c951/evidence-and-analysis-plan-v1.0.md","git_blob_sha1":HISTORICAL[1][1]}]
    if root.get("artifacts")!=expected: raise DesignError("historical authority registry drifted")
    for path,expected_blob in HISTORICAL:
        if _blob(path)!=expected_blob or _current_blob(path)!=expected_blob: raise DesignError(f"historical snapshot drifted: {path.name}")
    if _load(HIST_PREREG).get("execution_authorized") is not False: raise DesignError("historical base execution boundary drifted")

def validate_authority(data):
    authority=data.get("authority")
    if not isinstance(authority,dict): raise DesignError("closure authority missing")
    for key,expected in CURRENT_BLOBS.items():
        if authority.get(key)!=expected: raise DesignError(f"closure authority drifted: {key}")
    actual={"current_preregistration_git_blob_sha1":_current_blob(PREREG),"current_task_manifest_contract_git_blob_sha1":_current_blob(TASK),"current_seed_commitment_git_blob_sha1":_current_blob(SEED),"current_evidence_plan_git_blob_sha1":_current_blob(PLAN),"current_execution_gate_git_blob_sha1":_current_blob(GATE)}
    if actual!=CURRENT_BLOBS: raise DesignError("closure authority does not match current committed design artifacts")
    if authority.get("superseded_subjects") != ["bootstrap-seed authority narrative and verifier binding to mutable current-manifest inputs","task-manifest record schema, authoritative task identity, and deterministic required-strata classification","critical-harm threshold, repetition-slot event construction, and launch-gate specification"]: raise DesignError("closure superseded-subject registry drifted")
    if authority.get("outcome_exposure_status")!="none": raise DesignError("closure amendment is not prospective")
    for key in ("model_calls_authorized","pilot_execution_authorized","benchmark_execution_authorized","confirmatory_execution_authorized"):
        if authority.get(key) is not False: raise DesignError(f"closure amendment opened execution boundary: {key}")

def validate_seed(data):
    effective=data.get("bootstrap_seed_effective_contract"); seed_contract=_load(SEED)
    if not isinstance(effective,dict) or effective.get("inputs")!=SEED_INPUTS or seed_contract.get("derivation",{}).get("inputs")!=SEED_INPUTS: raise DesignError("immutable seed inputs drifted")
    seed=effective.get("seed_hex")
    if seed!=seed_contract.get("rng_contract",{}).get("seed_hex"): raise DesignError("seed value drifted")
    payload="FAR-SWE-V3-001/bootstrap-seed/v1\n"+f"treatment_capsule_git_blob_sha1={SEED_INPUTS[0]['git_blob_sha1']}\n"+f"execution_gate_git_blob_sha1={SEED_INPUTS[1]['git_blob_sha1']}\n"
    if seed_contract.get("derivation",{}).get("canonical_payload")!=payload or hashlib.sha256(payload.encode()).hexdigest()!=seed: raise DesignError("seed recomputation failed")
    correction=effective.get("authority_correction","")
    if "later prospective task-freeze correction" not in correction or "No outcome, grade, task identity, or run result contributed" not in correction: raise DesignError("seed authority correction drifted")

def validate_task_strata(data):
    effective=data.get("task_manifest_effective_contract")
    if not isinstance(effective,dict) or effective.get("effective_schema_version")!="1.5": raise DesignError("effective task-manifest schema drifted")
    if effective.get("required_record_keys_exactly") != ["blind_task_id","repository_blind_id","task_strata","task_identity_sha256","task_bundle_root_sha256"]: raise DesignError("effective task record shape drifted")
    identity=effective.get("task_identity_contract")
    if not isinstance(identity,dict) or identity.get("algorithm_id")!="far-swe-v3-authoritative-task-identity-v1" or identity.get("descriptor_required_keys_exactly")!=TASK_IDENTITY_KEYS or identity.get("serialization")!="RFC 8785 JCS UTF-8 bytes" or identity.get("digest")!="lowercase SHA-256 hex" or identity.get("strata_excluded_from_identity") is not True: raise DesignError("task identity contract drifted")
    if "must be unique across the frozen manifest" not in identity.get("uniqueness_rule","") or "regardless of strata" not in identity.get("uniqueness_rule",""): raise DesignError("task uniqueness rule drifted")
    strata=effective.get("task_strata")
    if not isinstance(strata,dict) or strata.get("type")!="nonempty JSON array of strings" or strata.get("allowed_values_exactly")!=REQUIRED_STRATA or strata.get("canonical_order")!=REQUIRED_STRATA or strata.get("operator_override_after_freeze_permitted") is not False or strata.get("classification_inputs_required")!=CLASSIFICATION_INPUTS or strata.get("deterministic_mapping")!=CLASSIFICATION_MAPPING or strata.get("evidence_rule")!=CLASSIFICATION_EVIDENCE_RULE: raise DesignError("task strata contract drifted")
    if strata.get("multi_label_rule")!="retain every label whose deterministic predicate is true, exactly once, in canonical_order; no primary-label choice or precedence is permitted": raise DesignError("task stratum multi-label rule drifted")
    if _load(PREREG).get("task_population",{}).get("required_strata")!=REQUIRED_STRATA: raise DesignError("amended stratum values do not match preregistration")
    root=effective.get("task_bundle_root_extension")
    if not isinstance(root,dict) or root.get("algorithm_id")!="far-swe-v3-task-bundle-root-v4" or root.get("descriptor_required_keys_exactly")!=TASK_BUNDLE_KEYS or root.get("task_identity_sha256_is_root_member") is not True or root.get("task_strata_are_root_members") is not True or root.get("classification_inputs_sha256_is_root_member") is not True: raise DesignError("task bundle root extension drifted")
    expected=["every manifest record has exactly the five required keys","task_identity_sha256 is recomputed from the authoritative repository/commit/payload descriptor and is unique across the frozen manifest independently of task_strata","task_strata is nonempty, duplicate-free, contains only allowed labels, and is in canonical order","task_strata exactly equals the deterministic mapping from the frozen classification inputs","every preregistered required stratum appears in at least one frozen confirmatory task","task_identity_sha256, task_strata, classification inputs, and task-bundle roots are committed before any sacrificial pilot or confirmatory execution"]
    if effective.get("preexecution_validation_extension")!=expected: raise DesignError("task preexecution validation contract drifted")

def validate_critical_harm(data):
    harm=data.get("critical_harm_threshold_contract")
    if not isinstance(harm,dict) or harm.get("freeze_status")!="frozen_pre_execution": raise DesignError("critical-harm threshold contract is not frozen")
    if harm.get("comparison_index")!="identical frozen task x repetition-slot indexes for FAR and placebo": raise DesignError("harm comparison index drifted")
    if harm.get("zero_tolerance_rule")!="one or more verified occurrences triggers critical_harm": raise DesignError("zero-tolerance trigger drifted")
    rate=harm.get("rate_harms")
    if not isinstance(rate,dict) or set(rate)!={"regression_introduction","invalid_run_rate"}: raise DesignError("rate-harm contract shape drifted")
    for item in rate.values():
        if item.get("threshold")!={"numerator":1,"denominator":10} or "frozen repetition slot" not in item.get("unit","") or "greater than or equal to 1/10" not in item.get("trigger_rule",""): raise DesignError("rate-harm threshold drifted")
    gate=data.get("execution_gate_extension")
    if not isinstance(gate,dict) or gate.get("pilot_prerequisites")!=PILOT_PREREQUISITES or gate.get("confirmatory_prerequisites")!=CONFIRMATORY_PREREQUISITES or gate.get("all_gates_required") is not True or gate.get("current_execution_authorized") is not False: raise DesignError("closure execution-gate boundary drifted")

def validate_narrative_and_nonclaims(data):
    required={"This amendment does not establish that FAR improves software engineering.","This amendment does not authorize model calls, pilot execution, benchmark execution, confirmatory execution, grading, or outcome reveal.","This amendment does not change accepted Project FAR theory or release any theory or empirical claim.","The historical snapshot artifacts are immutable authority copies, not newly generated evidence."}
    if not isinstance(data.get("nonclaims"),list) or set(data["nonclaims"])!=required: raise DesignError("closure nonclaims drifted")

def validate(path: Path=AMENDMENT):
    data=_load(path)
    if (data.get("schema_version"),data.get("program_id"),data.get("artifact_status"),data.get("amendment_status")) != ("1.2","FAR-SWE-V3-001","Research","prospective_pre_execution_correction"): raise DesignError("closure amendment identity drifted")
    validate_authority(data); validate_historical_authority(data); validate_seed(data); validate_task_strata(data); validate_critical_harm(data); validate_narrative_and_nonclaims(data); return data

if __name__ == "__main__":
    try: validate()
    except DesignError as exc: raise SystemExit(f"FAIL: {exc}")
    print("PASS: review-closure amendment v1.2 is prospective, rooted, deterministic, and execution remains blocked.")
