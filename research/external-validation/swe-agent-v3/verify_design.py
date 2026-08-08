#!/usr/bin/env python3
"""Fail-closed semantic verifier for the design-only FAR SWE-agent v3 package."""
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

PILOT_GATES = {
    "theory_version_frozen", "far_capsule_built_and_hash_frozen", "placebo_built_and_matching_verified",
    "confirmatory_task_population_frozen", "task_identity_information_barriers_verified",
    "model_endpoint_and_version_frozen", "prompts_and_agent_configuration_frozen",
    "environment_images_and_dependencies_frozen", "budgets_and_stopping_rules_frozen",
    "counterbalancing_and_randomization_seed_frozen", "grader_and_scoring_contract_frozen",
    "evidence_store_and_restoration_test_passed", "independent_preexecution_review_clean",
    "branch_or_tag_protection_and_exact_head_checks_enabled", "manual_pilot_launch_authorization_recorded",
}
GATES = {
    "theory_version_frozen", "far_capsule_built_and_hash_frozen", "placebo_built_and_matching_verified",
    "confirmatory_task_population_frozen", "task_identity_information_barriers_verified",
    "model_endpoint_and_version_frozen", "prompts_and_agent_configuration_frozen",
    "environment_images_and_dependencies_frozen", "budgets_and_stopping_rules_frozen",
    "counterbalancing_and_randomization_seed_frozen", "grader_and_scoring_contract_frozen",
    "evidence_store_and_restoration_test_passed", "sacrificial_pilot_completed_and_excluded",
    "independent_preexecution_review_clean", "branch_or_tag_protection_and_exact_head_checks_enabled",
    "manual_launch_authorization_recorded",
}
EXPECTED_PILOT_GATE_RULE = "sacrificial pilot execution is authorized only when every pilot gate is true, the exact design manifest verifies, and a separate prospective pilot launch record names the frozen commit; sacrificial_pilot_completed_and_excluded is not a pilot prerequisite"
EXPECTED_GATE_RULE = "confirmatory execution is authorized only when every gate is true, the exact design manifest verifies, and a separate prospective confirmatory launch record names the frozen commit"
EXPECTED_TOLERANCE = {
    "applies_to": ["utf8_bytes", "frozen_tokenizer_tokens"],
    "maximum_absolute_relative_difference": {"numerator": 1, "denominator": 100},
    "reference_count": "far_treatment_count", "far_count_requirement": "positive integer",
    "placebo_count_requirement": "nonnegative integer", "boundary": "inclusive", "rounding": "none",
    "floating_point_permitted": False,
    "integer_acceptance_rule": "abs(placebo_count - far_treatment_count) * 100 <= far_treatment_count",
}


def _manifest_entries() -> dict[str, dict[str, Any]]:
    data = integrity._decode_json(integrity._read_regular(MANIFEST), str(MANIFEST))
    if not isinstance(data, dict) or not isinstance(data.get("artifacts"), list):
        raise DesignError("verified design manifest required")
    return {e["path"]: e for e in data["artifacts"] if isinstance(e, dict) and isinstance(e.get("path"), str)}


def _require_exact_artifact(name: str) -> bytes:
    relative = f"research/external-validation/swe-agent-v3/{name}"
    entry = _manifest_entries().get(relative)
    if not isinstance(entry, dict):
        raise DesignError(f"governed artifact missing from manifest: {name}")
    committed = _committed_blob_bytes(relative)
    if len(committed) != entry.get("bytes") or _git_blob_sha1(committed) != entry.get("git_blob_sha1"):
        raise DesignError(f"manifest/current-commit mismatch: {name}")
    if integrity._read_regular(HERE / name) != committed:
        raise DesignError(f"worktree differs from committed artifact: {name}")
    return committed


def _all_true_bools(value: Any, keys: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != keys:
        raise DesignError(f"exact key set required: {label}")
    if any(type(v) is not bool or v is not True for v in value.values()):
        raise DesignError(f"all values must be boolean true: {label}")


def verify_preregistration() -> None:
    _require_exact_artifact("preregistration-v1.0.json")
    data = integrity._load_json(HERE / "preregistration-v1.0.json")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("stage"), data.get("execution_authorized")) != ("1.0", "FAR-SWE-V3-001", "Research", "design_only", False):
        raise DesignError("preregistration identity/execution boundary drifted")
    if data.get("historical_v2_pooling_permitted") is not False or data.get("primary_contrast") != "far_minus_placebo" or data.get("secondary_contrasts") != ["far_minus_baseline", "placebo_minus_baseline"]:
        raise DesignError("contrast/history contract drifted")
    arms = data.get("arms")
    if not isinstance(arms, list) or [x.get("id") for x in arms] != ["baseline", "placebo", "far"] or any(x.get("required") is not True for x in arms):
        raise DesignError("mandatory three-arm contract drifted")
    if arms[0].get("extra_capsule") is not None or arms[1].get("extra_capsule") != "placebo" or arms[2].get("extra_capsule") != "far" or arms[2].get("capsule_contract") != "treatment-capsule-contract-v1.0.json":
        raise DesignError("arm mapping drifted")
    if arms[1].get("matching_requirements", {}).get("relative_tolerance") != EXPECTED_TOLERANCE:
        raise DesignError("placebo tolerance drifted")
    assignment = data.get("assignment", {})
    if assignment.get("paired_design") is not True or assignment.get("every_task_in_every_arm") is not True or assignment.get("order") != "counterbalanced_within_task" or assignment.get("carryover_control") != "fresh_workspace_and_fresh_model_context_for_every_run":
        raise DesignError("assignment/carryover contract drifted")
    population = data.get("task_population", {})
    if population.get("status") != "unfrozen" or population.get("minimum_task_count", 0) < 24 or population.get("minimum_repository_count", 0) < 5:
        raise DesignError("task population weakened")
    control_keys = {
        "same_model_endpoint_across_arms", "model_fallback_prohibited",
        "same_system_and_agent_prompts_except_capsule_mount", "same_repository_commit_across_arms",
        "same_environment_image_across_arms", "same_tools_across_arms",
        "same_call_token_time_and_cost_budgets_across_arms", "fresh_context_per_run",
        "parallel_cross_arm_information_sharing_prohibited",
    }
    _all_true_bools(data.get("execution_controls"), control_keys, "execution controls")
    if data.get("outcomes", {}).get("primary") != {"id": "task_resolution", "source": "sealed_external_grader", "values": ["resolved", "unresolved", "invalid"], "invalid_is_not_resolved": True}:
        raise DesignError("primary outcome drifted")
    analysis = data.get("analysis", {})
    if analysis.get("primary_estimand") != "mean_task_level_resolution_probability_far_minus_placebo" or analysis.get("uncertainty_method") != "paired_task_bootstrap" or analysis.get("bootstrap_resamples") != 100000 or analysis.get("bootstrap_seed_status") != "unfrozen_and_independently_committed_before_execution":
        raise DesignError("primary/bootstrap analysis drifted")
    invalid = analysis.get("invalid_run_and_cell_policy", {})
    if invalid.get("replacement_attempts_per_infrastructure_invalid_slot") != 1 or invalid.get("cell_valid_only_if_every_frozen_repetition_is_valid") is not True or invalid.get("retained_invalid_repetition_makes_entire_task_arm_cell_missing") is not True or invalid.get("primary_missingness_rule") != "if any FAR or placebo task-arm cell is missing, final confirmatory classification is inconclusive_due_to_missingness" or invalid.get("sensitivity_results_are_confirmatory") is not False:
        raise DesignError("invalid-run/missingness policy drifted")
    if analysis.get("decision_precedence") != ["inconclusive_due_to_missingness", "bounded_harm", "bounded_positive", "no_practical_advantage", "inconclusive"]:
        raise DesignError("decision precedence drifted")
    categories = analysis.get("decision_categories", {})
    if "upper bound < 0" not in categories.get("bounded_harm", "") or "0 <= 95% paired-task bootstrap upper bound < 0.10" not in categories.get("no_practical_advantage", ""):
        raise DesignError("decision category boundary drifted")
    interval = analysis.get("bootstrap_interval_spec", {})
    order = interval.get("task_order", {})
    if interval.get("method") != "percentile_equal_tailed" or interval.get("resample_count") != 100000 or order.get("source") != "exact frozen ordered task manifest committed and integrity-rooted before any sacrificial pilot or confirmatory execution" or order.get("sequence_rule") != "manifest JSON array order is authoritative; runtime sorting and locale collation are prohibited":
        raise DesignError("bootstrap interval/order drifted")
    if analysis.get("equivalence_or_noninferiority_claim_permitted") is not False or analysis.get("population_generalization_permitted") is not False:
        raise DesignError("prohibited inference enabled")
    _all_true_bools(data.get("blinding"), {"arm_labels_blinded_to_graders", "task_outcomes_hidden_until_all_required_runs_and_evidence_bundles_are_frozen", "capsule_authors_prohibited_from_task_identity_access", "grader_prohibited_from_capsule_identity_access_until_scoring_freeze"}, "blinding")
    if data.get("pilot") != {"required": True, "status": "not_authorized", "purpose": "harness, evidence retention, randomization, restoration, and grader-interface validation only", "minimum_sacrificial_tasks": 3, "pilot_tasks_excluded_from_confirmatory_evidence": True, "model_calls_currently_prohibited": True}:
        raise DesignError("pilot contract drifted")


def verify_task_manifest_contract() -> None:
    _require_exact_artifact("task-manifest-contract-v1.0.json")
    import verify_review_closure as review_closure
    review_closure.verify_task_identity_contract(HERE / "task-manifest-contract-v1.0.json")


def verify_capsule_contract() -> None:
    _require_exact_artifact("treatment-capsule-contract-v1.0.json")
    data = integrity._load_json(HERE / "treatment-capsule-contract-v1.0.json")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("capsule_status"), data.get("execution_authorized")) != ("1.0", "FAR-SWE-V3-001", "Research", "uninstantiated", False):
        raise DesignError("capsule identity/boundary drifted")
    if data.get("source") != {"repository": "notfoundout/Project-FAR", "commit_sha": None, "tree_sha": None, "theory_version": None, "exporter_blob_sha": None}:
        raise DesignError("capsule source drifted")
    runtime = data.get("runtime_constraints")
    expected_runtime = {"read_only": True, "network_access": False, "writes_outside_run_evidence_directory": False, "extra_tool_permissions": False, "extra_context_window": False, "extra_model_calls": False, "mutable_remote_dependencies": False}
    if not isinstance(runtime, dict) or set(runtime) != set(expected_runtime) or any(type(runtime[k]) is not bool or runtime[k] is not expected_runtime[k] for k in expected_runtime):
        raise DesignError("capsule runtime constraints drifted or changed type")
    if data.get("placebo_matching", {}).get("relative_tolerance") != EXPECTED_TOLERANCE:
        raise DesignError("capsule placebo tolerance drifted")
    if data.get("freeze_sequence") != ["freeze theory version and source commit", "export candidate FAR capsule deterministically", "audit for forbidden task or outcome content", "freeze tokenizer identity and compute exposure metrics", "construct inert placebo without confirmatory task access", "verify matching tolerances", "commit capsule and placebo manifests before confirmatory task identities are released", "seal exact capsule and placebo bytes"]:
        raise DesignError("capsule freeze sequence drifted")
    if data.get("invalidation_rules") != ["any source commit or capsule byte change creates a new experiment version", "any confirmatory task identity exposure to a capsule author invalidates the affected task", "any unmatched tool, budget, context, read-order, or interaction advantage invalidates the causal contrast", "any mutable remote dependency invalidates the capsule"]:
        raise DesignError("capsule invalidation rules drifted")


def verify_execution_gate() -> None:
    _require_exact_artifact("execution-gate-v1.0.json")
    data = integrity._load_json(HERE / "execution-gate-v1.0.json")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status")) != ("1.2", "FAR-SWE-V3-001", "Research"):
        raise DesignError("execution gate identity drifted")
    for key in ("execution_authorized", "model_calls_authorized", "benchmark_execution_authorized", "pilot_execution_authorized", "confirmatory_execution_authorized"):
        if type(data.get(key)) is not bool or data.get(key) is not False:
            raise DesignError("execution/model calls must remain boolean false")
    if data.get("pilot_gate_rule") != EXPECTED_PILOT_GATE_RULE or data.get("gate_rule") != EXPECTED_GATE_RULE:
        raise DesignError("launch rule drifted")
    pilot, gates = data.get("pilot_gates"), data.get("gates")
    if not isinstance(pilot, dict) or set(pilot) != PILOT_GATES or any(type(v) is not bool or v is not False for v in pilot.values()):
        raise DesignError("pre-pilot gate set drifted")
    if not isinstance(gates, dict) or set(gates) != GATES or any(type(v) is not bool or v is not False for v in gates.values()):
        raise DesignError("confirmatory gate set drifted")
    if len(data.get("current_blockers", [])) != 6 or set(data.get("forbidden_current_actions", [])) != {"model access probe", "agent model call", "benchmark task selection with capsule-author access", "pilot execution", "confirmatory execution", "outcome reveal", "claim of FAR improvement"}:
        raise DesignError("execution blockers/forbidden actions drifted")


def verify_text_boundaries() -> None:
    evidence = _require_exact_artifact("evidence-and-analysis-plan-v1.0.md").decode("utf-8")
    readme = _require_exact_artifact("README.md").decode("utf-8")
    question = _require_exact_artifact("question-v1.0.md").decode("utf-8")
    if "`D_i = p_i(far) - p_i(placebo)`" not in evidence or "`D_i = p_i(far) - p_i(baseline)`" in evidence:
        raise DesignError("primary narrative contrast drifted")
    if "independently committed before any pilot or confirmatory execution" not in evidence or "authoritative repository provider identity, canonical repository URL, and exact commit" not in evidence:
        raise DesignError("evidence identity boundary drifted")
    if "Execution authorized: **No**" not in readme or "A sacrificial pilot may only be separately authorized after every pre-pilot gate" not in readme or "confirmatory execution additionally requires the completed-and-excluded pilot gate" not in readme:
        raise DesignError("README execution boundary drifted")
    if "would not establish" not in question:
        raise DesignError("question nonclaim boundary missing")
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
    print("PASS: FAR-SWE-V3-001 semantics verify and execution remains blocked.")
