#!/usr/bin/env python3
"""Fail-closed verifier for the design-only FAR SWE-agent v3 package."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_integrity as integrity

DesignError = integrity.DesignError
ROOT = integrity.ROOT
HERE = integrity.HERE
MANIFEST = integrity.MANIFEST
_committed_blob_bytes = integrity._committed_blob_bytes
_git_blob_sha1 = integrity._git_blob_sha1

ARTIFACT_BLOBS = {
    "README.md": "4685f7a42beaab65eb6a96bb9a3ec72f2313744e",
    "question-v1.0.md": "b61da8b21953b835d341331e360405d6783d4cf4",
    "preregistration-v1.0.json": "7147f6814f76eb0f73fd0741b17b2501e38e6f57",
    "task-manifest-contract-v1.0.json": "1cb4f312ae907b9a93afbe5c85ebcca93bbbd3e9",
    "treatment-capsule-contract-v1.0.json": "e011c8f9972a5682e03526f739437f62e973e76d",
    "execution-gate-v1.0.json": "055cdd17581074e2325d570db8df9266e88556e2",
    "evidence-and-analysis-plan-v1.0.md": "15b352d54a524d9caf827018b608028c004f8f13",
}
PILOT_DIGEST = "847385a29ce4b02d7ece9817dfc4c7772a0583c6b4e0f663248bf3bb02bda478"
FREEZE_SEQUENCE_DIGEST = "198b19ca3ef97f55480077559b47197668ab842474f252f0d7b1faa876186449"
INVALIDATION_RULES_DIGEST = "63b9a2c5989ce78e065133dd0920b67115e1cae9c5cd3d4cc5efa30c96536670"
EXPECTED_GATE_RULE = (
    "execution is authorized only when every gate is true, the exact design "
    "manifest verifies, and a separate launch record names the frozen commit"
)
GATES = {
    "theory_version_frozen", "far_capsule_built_and_hash_frozen",
    "placebo_built_and_matching_verified", "confirmatory_task_population_frozen",
    "task_identity_information_barriers_verified", "model_endpoint_and_version_frozen",
    "prompts_and_agent_configuration_frozen", "environment_images_and_dependencies_frozen",
    "budgets_and_stopping_rules_frozen", "counterbalancing_and_randomization_seed_frozen",
    "grader_and_scoring_contract_frozen", "evidence_store_and_restoration_test_passed",
    "sacrificial_pilot_completed_and_excluded", "independent_preexecution_review_clean",
    "branch_or_tag_protection_and_exact_head_checks_enabled",
    "manual_launch_authorization_recorded",
}


def _require_exact_artifact(name: str) -> bytes:
    raw = integrity._read_regular(HERE / name)
    if integrity._git_blob_sha1(raw) != ARTIFACT_BLOBS[name]:
        raise DesignError(f"complete governed artifact drifted: {name}")
    return raw


def _require_keys(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise DesignError(f"exact key set required: {label}")
    return value


def verify_preregistration() -> None:
    _require_exact_artifact("preregistration-v1.0.json")
    data = integrity._load_json(HERE / "preregistration-v1.0.json")
    if (data.get("program_id"), data.get("stage"), data.get("execution_authorized")) != (
        "FAR-SWE-V3-001", "design_only", False
    ):
        raise DesignError("preregistration identity or execution boundary drifted")
    if data.get("primary_contrast") != "far_minus_placebo":
        raise DesignError("primary contrast must remain FAR minus placebo")
    if data.get("secondary_contrasts") != ["far_minus_baseline", "placebo_minus_baseline"]:
        raise DesignError("secondary contrasts drifted")
    if data.get("historical_v2_pooling_permitted") is not False:
        raise DesignError("historical v2 pooling must remain prohibited")
    arms = data.get("arms")
    if not isinstance(arms, list) or [x.get("id") for x in arms] != ["baseline", "placebo", "far"]:
        raise DesignError("exact three-arm order required")
    if any(x.get("required") is not True for x in arms):
        raise DesignError("all three arms must remain mandatory")
    if arms[0].get("extra_capsule") is not None or arms[1].get("extra_capsule") != "placebo":
        raise DesignError("baseline/placebo treatment mapping drifted")
    if arms[2].get("extra_capsule") != "far" or arms[2].get("capsule_contract") != "treatment-capsule-contract-v1.0.json":
        raise DesignError("FAR treatment mapping drifted")
    assignment = data.get("assignment")
    if not isinstance(assignment, dict) or assignment.get("paired_design") is not True:
        raise DesignError("paired assignment required")
    if assignment.get("order") != "counterbalanced_within_task":
        raise DesignError("counterbalancing contract drifted")
    population = data.get("task_population")
    if not isinstance(population, dict) or population.get("status") != "unfrozen":
        raise DesignError("task population must remain unfrozen")
    if population.get("minimum_task_count", 0) < 24 or population.get("minimum_repository_count", 0) < 5:
        raise DesignError("minimum task population weakened")
    controls = data.get("execution_controls")
    if not isinstance(controls, dict) or len(controls) != 9 or any(v is not True for v in controls.values()):
        raise DesignError("all nine cross-arm controls required")
    outcomes = data.get("outcomes", {}).get("primary")
    if outcomes != {"id": "task_resolution", "source": "sealed_external_grader", "values": ["resolved", "unresolved", "invalid"], "invalid_is_not_resolved": True}:
        raise DesignError("primary outcome contract drifted")
    analysis = data.get("analysis")
    if not isinstance(analysis, dict) or analysis.get("primary_estimand") != "mean_task_level_resolution_probability_far_minus_placebo":
        raise DesignError("primary estimand drifted")
    if analysis.get("bootstrap_resamples") != 100000 or analysis.get("bootstrap_seed_status") != "unfrozen_and_committed_before_outcome_reveal":
        raise DesignError("bootstrap contract drifted")
    if analysis.get("equivalence_or_noninferiority_claim_permitted") is not False or analysis.get("population_generalization_permitted") is not False:
        raise DesignError("prohibited inference was enabled")
    blinding = data.get("blinding")
    if not isinstance(blinding, dict) or len(blinding) != 4 or any(v is not True for v in blinding.values()):
        raise DesignError("complete blinding contract required")
    integrity._require_digest(data.get("pilot"), PILOT_DIGEST, "sacrificial pilot")


def verify_task_manifest_contract() -> None:
    _require_exact_artifact("task-manifest-contract-v1.0.json")
    data = integrity._load_json(HERE / "task-manifest-contract-v1.0.json")
    if data.get("manifest_status") != "uninstantiated" or data.get("execution_authorized") is not False:
        raise DesignError("task manifest boundary drifted")
    freeze_timing = data.get("freeze_timing")
    if not isinstance(freeze_timing, str) or "before any sacrificial pilot or confirmatory execution" not in freeze_timing or "freezing after any agent run is prohibited" not in freeze_timing:
        raise DesignError("task manifest prospective freeze timing drifted")
    record = _require_keys(
        data.get("record_schema"),
        {"required_keys_exactly", "blind_task_id", "repository_blind_id", "task_bundle_root_sha256"},
        "task manifest record schema",
    )
    root_field = _require_keys(record.get("task_bundle_root_sha256"), {"pattern", "construction"}, "task bundle root field")
    if root_field.get("pattern") != "^[0-9a-f]{64}$" or "task_bundle_root_contract" not in root_field.get("construction", ""):
        raise DesignError("task bundle root field drifted")
    root = _require_keys(
        data.get("task_bundle_root_contract"),
        {
            "algorithm_id", "hash", "descriptor_media_type", "descriptor_canonicalization",
            "descriptor_required_keys_exactly", "descriptor_values", "required_root_members",
            "archive_or_filesystem_metadata_in_root", "path_order_or_archive_format_in_root",
            "recomputation_rule",
        },
        "task bundle root contract",
    )
    if root.get("algorithm_id") != "far-swe-v3-task-bundle-root-v1" or root.get("hash") != "SHA-256":
        raise DesignError("task bundle root algorithm drifted")
    if root.get("descriptor_canonicalization") != "RFC 8785 JSON Canonicalization Scheme (JCS); UTF-8 bytes; no BOM; no insignificant whitespace":
        raise DesignError("task bundle descriptor canonicalization drifted")
    required_descriptor_keys = [
        "algorithm_id", "repository_url", "repository_commit_sha",
        "task_payload_sha256", "task_payload_bytes",
    ]
    if root.get("descriptor_required_keys_exactly") != required_descriptor_keys:
        raise DesignError("task bundle descriptor shape drifted")
    values = _require_keys(root.get("descriptor_values"), set(required_descriptor_keys), "task bundle descriptor values")
    if values.get("algorithm_id") != "far-swe-v3-task-bundle-root-v1":
        raise DesignError("task bundle descriptor algorithm identity drifted")
    if root.get("required_root_members") != [
        "repository URL", "exact repository commit", "exact task/issue payload digest", "exact task/issue payload byte count"
    ]:
        raise DesignError("task bundle required root members drifted")
    if root.get("archive_or_filesystem_metadata_in_root") is not False or root.get("path_order_or_archive_format_in_root") is not False:
        raise DesignError("task bundle root must be independent of archive/path metadata")
    order = data.get("order_contract")
    if not isinstance(order, dict) or order.get("authoritative_sequence") != "top-level JSON array order" or order.get("runtime_sorting_permitted") is not False:
        raise DesignError("task-order contract drifted")
    validations = data.get("preexecution_validation")
    if not isinstance(validations, list) or "every task bundle root is independently recomputed from the canonical task-bundle descriptor" not in validations or "the exact task manifest artifact bytes and Git blob identity are committed before any sacrificial pilot or confirmatory execution" not in validations:
        raise DesignError("task manifest preexecution validation drifted")


def verify_capsule_contract() -> None:
    _require_exact_artifact("treatment-capsule-contract-v1.0.json")
    data = integrity._load_json(HERE / "treatment-capsule-contract-v1.0.json")
    if data.get("capsule_status") != "uninstantiated" or data.get("execution_authorized") is not False:
        raise DesignError("capsule boundary drifted")
    if data.get("source") != {"repository": "notfoundout/Project-FAR", "commit_sha": None, "tree_sha": None, "theory_version": None, "exporter_blob_sha": None}:
        raise DesignError("capsule source provenance drifted")
    if data.get("runtime_constraints") != {"read_only": True, "network_access": False, "writes_outside_run_evidence_directory": False, "extra_tool_permissions": False, "extra_context_window": False, "extra_model_calls": False, "mutable_remote_dependencies": False}:
        raise DesignError("capsule runtime constraints drifted")
    integrity._require_digest(data.get("freeze_sequence"), FREEZE_SEQUENCE_DIGEST, "capsule freeze sequence")
    integrity._require_digest(data.get("invalidation_rules"), INVALIDATION_RULES_DIGEST, "capsule invalidation rules")


def verify_execution_gate() -> None:
    _require_exact_artifact("execution-gate-v1.0.json")
    data = integrity._load_json(HERE / "execution-gate-v1.0.json")
    _require_keys(data, {"schema_version", "program_id", "artifact_status", "execution_authorized", "model_calls_authorized", "benchmark_execution_authorized", "gate_rule", "gates", "current_blockers", "forbidden_current_actions"}, "execution gate")
    if any(data.get(k) is not False for k in ("execution_authorized", "model_calls_authorized", "benchmark_execution_authorized")):
        raise DesignError("execution and model calls must remain blocked")
    if data.get("gate_rule") != EXPECTED_GATE_RULE:
        raise DesignError("all-gates launch rule drifted")
    gates = data.get("gates")
    if not isinstance(gates, dict) or set(gates) != GATES or any(v is not False for v in gates.values()):
        raise DesignError("all sixteen gates must remain false")
    if len(data.get("current_blockers", [])) != 6:
        raise DesignError("complete current-blocker list required")
    if set(data.get("forbidden_current_actions", [])) != {"model access probe", "agent model call", "benchmark task selection with capsule-author access", "pilot execution", "confirmatory execution", "outcome reveal", "claim of FAR improvement"}:
        raise DesignError("forbidden-current-action contract drifted")


def verify_text_boundaries() -> None:
    evidence = _require_exact_artifact("evidence-and-analysis-plan-v1.0.md").decode("utf-8")
    readme = _require_exact_artifact("README.md").decode("utf-8")
    question = _require_exact_artifact("question-v1.0.md").decode("utf-8")
    if "`D_i = p_i(far) - p_i(placebo)`" not in evidence or "`D_i = p_i(far) - p_i(baseline)`" in evidence:
        raise DesignError("primary analysis narrative must remain FAR minus placebo")
    if "Execution authorized: **No**" not in readme or "would not establish" not in question:
        raise DesignError("visible execution or claim boundary missing")
    for phrase in ("universal software-engineering improvement", "model-independent improvement", "commercial readiness"):
        if phrase not in question:
            raise DesignError(f"public nonclaim missing: {phrase}")


def verify() -> None:
    integrity.ROOT, integrity.HERE, integrity.MANIFEST = ROOT, HERE, MANIFEST
    integrity._committed_blob_bytes = _committed_blob_bytes
    integrity.verify_manifest()
    integrity.verify_byte_policy()
    verify_preregistration()
    verify_task_manifest_contract()
    verify_capsule_contract()
    verify_execution_gate()
    verify_text_boundaries()


if __name__ == "__main__":
    try:
        verify()
    except DesignError as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: FAR-SWE-V3-001 is exact-locked and execution remains blocked.")
