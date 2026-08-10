#!/usr/bin/env python3
"""Fail-closed semantic verifier for the design-only FAR SWE-agent v3 package."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_integrity as integrity
import verify_review_closure as review_closure
import verify_public_narratives as public_narratives

DesignError = integrity.DesignError
ROOT = integrity.ROOT
HERE = integrity.HERE
MANIFEST = integrity.MANIFEST
_committed_blob_bytes = integrity._committed_blob_bytes

STRATA_ORDER = ["bug_fix", "test_failure", "behavioral_regression", "API_or_contract_change", "multi_file_change"]
EXPECTED_TOLERANCE = {
    "applies_to": ["utf8_bytes", "frozen_tokenizer_tokens"],
    "maximum_absolute_relative_difference": {"numerator": 1, "denominator": 100},
    "reference_count": "far_treatment_count",
    "far_count_requirement": "positive integer",
    "placebo_count_requirement": "nonnegative integer",
    "boundary": "inclusive",
    "rounding": "none",
    "floating_point_permitted": False,
    "integer_acceptance_rule": "abs(placebo_count - far_treatment_count) * 100 <= far_treatment_count",
}
EXPECTED_ARMS = [
    {
        "id": "baseline", "required": True,
        "description": "Ordinary frozen agent configuration without an auxiliary capsule.",
        "extra_capsule": None, "tool_permissions": "identical_across_arms", "budget": "identical_across_arms",
    },
    {
        "id": "placebo", "required": True,
        "description": "Inert auxiliary capsule matched to the FAR capsule for exposure and burden but containing no FAR concepts or task-relevant guidance.",
        "extra_capsule": "placebo",
        "matching_requirements": {
            "relative_tolerance": EXPECTED_TOLERANCE,
            "file_count_exact": True, "relative_path_shape_exact": True, "directory_depth_exact": True,
            "read_order_exact": True, "interaction_turns_exact": True, "tool_permissions_exact": True,
        },
        "forbidden_content": [
            "FAR terminology", "task identities", "repository-specific facts", "gold patches", "hidden tests",
            "benchmark outcomes", "software-engineering advice beyond neutral formatting text",
        ],
    },
    {
        "id": "far", "required": True,
        "description": "Frozen treatment capsule exported from one exact Project FAR commit after theory freeze.",
        "extra_capsule": "far", "capsule_contract": "treatment-capsule-contract-v1.0.json",
        "tool_permissions": "identical_across_arms", "budget": "identical_across_arms",
    },
]
EXPECTED_ASSIGNMENT = {
    "primary_unit": "task", "paired_design": True, "every_task_in_every_arm": True,
    "repetitions_per_task_arm_status": "unfrozen", "minimum_repetitions_per_task_arm": 2,
    "order": "counterbalanced_within_task", "randomization_seed_status": "unfrozen_and_sealed_before_execution",
    "carryover_control": "fresh_workspace_and_fresh_model_context_for_every_run",
}
EXPECTED_TASK_POPULATION = {
    "status": "unfrozen", "confirmatory_source": "external_private_or_sealed_holdout",
    "minimum_task_count": 24, "minimum_repository_count": 5, "maximum_fraction_from_one_repository": 0.2,
    "required_strata": STRATA_ORDER,
    "sealed_identity_ledger_contract": "task-manifest-contract-v1.0.json#/sealed_identity_ledger_contract",
    "prohibited_task_repositories": ["notfoundout/Project-FAR", "any fork or mirror containing Project FAR treatment material"],
    "prohibited_tasks": [
        "any historical SWE-agent v2 task", "any task used in the sacrificial harness pilot",
        "any task exposed during capsule construction",
        "any task with gold patch or hidden-test exposure to an operator or treatment author",
    ],
}
EXPECTED_EXECUTION_CONTROLS = {
    "same_model_endpoint_across_arms": True, "model_fallback_prohibited": True,
    "same_system_and_agent_prompts_except_capsule_mount": True, "same_repository_commit_across_arms": True,
    "same_environment_image_across_arms": True, "same_tools_across_arms": True,
    "same_call_token_time_and_cost_budgets_across_arms": True, "fresh_context_per_run": True,
    "parallel_cross_arm_information_sharing_prohibited": True,
}
EXPECTED_OUTCOMES = {
    "primary": {"id": "task_resolution", "source": "sealed_external_grader", "values": ["resolved", "unresolved", "invalid"], "invalid_is_not_resolved": True},
    "secondary": [
        "target_test_status", "regression_test_status", "patch_applies", "budget_exhausted", "wall_clock_seconds",
        "model_calls", "input_tokens", "output_tokens", "provider_cost", "tool_calls", "changed_files",
        "human_adjudication_minutes", "safety_or_authorization_violation",
    ],
}
EXPECTED_DECISION_CATEGORIES = {
    "inconclusive_due_to_missingness": "one or more FAR or placebo task-arm cells remain missing after the single permitted same-slot infrastructure replacement",
    "bounded_harm": "no primary cells are missing and 95% paired-task bootstrap upper bound < 0",
    "bounded_positive": "no primary cells are missing and estimate >= 0.10 and 95% paired-task bootstrap lower bound > 0 and no critical harm triggers under critical-harm-thresholds-v1.0.json",
    "no_practical_advantage": "no primary cells are missing and 0 <= 95% paired-task bootstrap upper bound < 0.10",
    "inconclusive": "no primary cells are missing and none of the preceding categories applies",
}
EXPECTED_INVALID_POLICY = {
    "replacement_attempts_per_infrastructure_invalid_slot": 1,
    "replacement_must_use_same_frozen_task_arm_repetition_and_conditions": True,
    "replacement_must_finish_before_any_outcome_reveal": True,
    "cell_valid_only_if_every_frozen_repetition_is_valid": True,
    "retained_invalid_repetition_makes_entire_task_arm_cell_missing": True,
    "primary_missingness_rule": "if any FAR or placebo task-arm cell is missing, final confirmatory classification is inconclusive_due_to_missingness",
    "required_descriptive_sensitivity": [
        "complete-case paired estimate", "worst-case full-task-set bound with missing FAR=0 and missing placebo=1",
        "best-case full-task-set bound with missing FAR=1 and missing placebo=0",
    ],
    "sensitivity_results_are_confirmatory": False,
}
EXPECTED_INTERVAL = {
    "method": "percentile_equal_tailed", "confidence_level": 0.95,
    "lower_tail_probability": 0.025, "upper_tail_probability": 0.975,
    "resample_count": 100000, "resample_unit": "task", "resample_size": "number_of_complete_primary_tasks",
    "draws_with_replacement": True,
    "task_order": {
        "contract": "task-manifest-contract-v1.0.json",
        "source": "exact frozen ordered task manifest committed and integrity-rooted before any sacrificial pilot or confirmatory execution",
        "sealed_identity_ledger": "the exact sealed identity ledger governed by task-manifest-contract-v1.0.json is committed with the task manifest before execution and binds each blind record to its authoritative GitHub repository/task descriptor",
        "blind_identifier_pattern": "^TASK-[0-9]{6}$",
        "blind_identifier_encoding": "ASCII subset of UTF-8; Unicode and normalization-sensitive identifiers are prohibited",
        "sequence_rule": "manifest JSON array order is authoritative; runtime sorting and locale collation are prohibited",
        "uniqueness_rule": "blind identifiers and task-bundle roots must each be unique",
        "strata_rule": "each record carries a frozen nonempty canonical-order subset of the five preregistered strata and the manifest-wide union must cover all five before execution",
        "complete_case_rule": "remove tasks with missing primary cells while preserving manifest-relative order",
        "bootstrap_vector_rule": "D_i vector indices are exactly the remaining manifest array positions in order",
    },
    "rng_procedure": {
        "id": "sha256_rejection_stream_v1",
        "seed_format": "exactly 64 lowercase hexadecimal characters strictly base16-decoded into 32 bytes; the ASCII hex characters are not hashed",
        "counter_encoding": "decoded_seed_32_bytes || uint64_be(resample_index) || uint64_be(draw_index) || uint32_be(rejection_counter)",
        "digest": "SHA-256", "integer": "first 8 digest bytes interpreted as unsigned big-endian",
        "unbiased_index_rule": "reject x >= 2^64 - (2^64 mod N); otherwise index = x mod N; increment rejection_counter from zero until accepted",
        "resample_index_origin": 0, "draw_index_origin": 0, "rejection_counter_origin": 0,
    },
    "quantile_convention": {
        "id": "hyndman_fan_type_7", "sorted_values": "ascending bootstrap estimates including duplicates",
        "formula": "h=(m-1)*p; q=(1-f)*x[floor(h)] + f*x[ceil(h)], where f=h-floor(h), zero-based indices, and m=100000",
    },
    "classification_uses_bounds": "lower p=0.025 and upper p=0.975 from this exact procedure",
}
EXPECTED_ANALYSIS = {
    "task_level_aggregation": "mean over repetitions within each task and arm",
    "primary_estimand": "mean_task_level_resolution_probability_far_minus_placebo",
    "uncertainty_method": "paired_task_bootstrap", "bootstrap_resamples": 100000,
    "bootstrap_seed_status": "frozen_by_bootstrap-seed-commitment-contract-v1.0.json_before_execution",
    "bootstrap_seed_contract": "bootstrap-seed-commitment-contract-v1.0.json",
    "critical_harm_contract": "critical-harm-thresholds-v1.0.json",
    "decision_categories": EXPECTED_DECISION_CATEGORIES,
    "multiple_comparison_policy": "primary contrast alone is confirmatory; all secondary contrasts and component ablations are exploratory unless separately frozen before exposure",
    "equivalence_or_noninferiority_claim_permitted": False,
    "population_generalization_permitted": False,
    "invalid_run_and_cell_policy": EXPECTED_INVALID_POLICY,
    "decision_precedence": ["inconclusive_due_to_missingness", "bounded_harm", "bounded_positive", "no_practical_advantage", "inconclusive"],
    "bootstrap_interval_spec": EXPECTED_INTERVAL,
}
EXPECTED_BLINDING = {
    "arm_labels_blinded_to_graders": True,
    "task_outcomes_hidden_until_all_required_runs_and_evidence_bundles_are_frozen": True,
    "capsule_authors_prohibited_from_task_identity_access": True,
    "grader_prohibited_from_capsule_identity_access_until_scoring_freeze": True,
}
EXPECTED_PILOT = {
    "required": True, "status": "not_authorized",
    "purpose": "harness, evidence retention, randomization, restoration, and grader-interface validation only",
    "minimum_sacrificial_tasks": 3, "pilot_tasks_excluded_from_confirmatory_evidence": True,
    "model_calls_currently_prohibited": True,
}
EXPECTED_NONCLAIMS = [
    "universal software-engineering improvement", "model-independent improvement", "theory truth",
    "FAR primitive necessity", "FAR minimality", "external replication", "commercial readiness",
    "equivalence of baseline and placebo", "pooling with historical SWE-agent v2",
]
EXPECTED_CAPSULE = {
    "schema_version": "1.0", "program_id": "FAR-SWE-V3-001", "artifact_status": "Research",
    "capsule_status": "uninstantiated", "execution_authorized": False,
    "source": {"repository": "notfoundout/Project-FAR", "commit_sha": None, "tree_sha": None, "theory_version": None, "exporter_blob_sha": None},
    "required_outputs": {
        "capsule_manifest": "canonical JSON with normalized relative paths, byte sizes, SHA-256, Git blob SHA-1 where applicable, and media type",
        "capsule_root_sha256": None, "tokenizer_identity": None, "token_count": None, "utf8_byte_count": None,
        "file_count": None, "maximum_directory_depth": None,
    },
    "allowed_content_classes": [
        "static instructions derived from the frozen FAR version", "static schemas", "static checklists",
        "deterministic local validation tools", "worked examples that are domain-neutral and frozen before task selection",
    ],
    "forbidden_content_classes": [
        "confirmatory task identifiers", "confirmatory repository names", "issue text from confirmatory tasks",
        "gold patches", "hidden tests", "grader outputs", "benchmark outcomes", "task-specific hints",
        "post-selection examples", "internet retrieval instructions", "additional model calls", "provider-specific hidden memory",
        "Project FAR repository navigation unrelated to the exported capsule",
    ],
    "runtime_constraints": {
        "read_only": True, "network_access": False, "writes_outside_run_evidence_directory": False,
        "extra_tool_permissions": False, "extra_context_window": False, "extra_model_calls": False,
        "mutable_remote_dependencies": False,
    },
    "placebo_matching": {
        "required": True, "relative_tolerance": EXPECTED_TOLERANCE,
        "file_count_exact": True, "relative_path_shape_exact": True, "directory_depth_exact": True,
        "read_order_exact": True, "interaction_turns_exact": True, "tool_permissions_exact": True,
    },
    "freeze_sequence": [
        "freeze theory version and source commit", "export candidate FAR capsule deterministically",
        "audit for forbidden task or outcome content", "freeze tokenizer identity and compute exposure metrics",
        "construct inert placebo without confirmatory task access", "verify matching tolerances",
        "commit capsule and placebo manifests before confirmatory task identities are released", "seal exact capsule and placebo bytes",
    ],
    "invalidation_rules": [
        "any source commit or capsule byte change creates a new experiment version",
        "any confirmatory task identity exposure to a capsule author invalidates the affected task",
        "any unmatched tool, budget, context, read-order, or interaction advantage invalidates the causal contrast",
        "any mutable remote dependency invalidates the capsule",
    ],
}
EXPECTED_EVIDENCE_BUNDLE_SECTION = """## Evidence bundle per run

Every attempted run must retain immutable, hash-addressed copies of:

- task identity under sealed mapping, including the frozen task-manifest strata classification;
- frozen task-manifest Git blob identity and frozen sealed identity-ledger Git blob identity;
- retained task-population repository-prohibition audit report root;
- authoritative repository provider identity, canonical repository URL, exact commit, GitHub fork-source repository ID or null, and treatment-material audit result as reconstructed from the sealed identity ledger by the independent identity auditor;
- environment image digest and dependency lock;
- model provider, endpoint, model version, parameters, and provider request identifier;
- all system, agent, task, capsule, and tool instructions;
- capsule or placebo manifest and mount path;
- randomization position and repetition;
- stdout, stderr, ordered trajectory, commands, tool calls, model messages, timestamps, token usage, budget state, and cost;
- workspace status before and after the run;
- patch, prediction, changed-file inventory, internal exit status, outer exit status, and terminal reason;
- target, neighboring, regression, and hidden-grader results;
- grader version, grader logs, adjudication record, and final outcome;
- the critical-harm evaluation inputs and exact results required by `critical-harm-thresholds-v1.0.json`;
- bundle manifest and content-root digest.

Outer process success cannot override an inner execution failure. `budget_exhausted` is distinct from `resolved`. Missing required evidence makes the run `invalid`, never `resolved`.

"""
EXPECTED_PRE_SUBMISSION_SECTION = """## Pre-submission behavior contract

The agent must retain:

1. a reproduction attempt or explicit `reproduction_unavailable`;
2. a causal hypothesis;
3. at least one observation that discriminates that hypothesis from an alternative;
4. execution of the identified target test before submission, or explicit `target_test_unavailable`;
5. execution of the frozen neighboring-test set after a target pass;
6. a patch that modifies an intended repository path, unless the run terminates with an explicit no-patch failure.

These controls affect all arms equally and are part of the frozen agent configuration, not part of the FAR capsule.

"""


def _manifest_entries() -> dict[str, dict[str, Any]]:
    data = integrity._decode_json(integrity._read_regular(MANIFEST), str(MANIFEST))
    if not isinstance(data, dict) or not isinstance(data.get("artifacts"), list):
        raise DesignError("verified design manifest required")
    return {e["path"]: e for e in data["artifacts"] if isinstance(e, dict) and isinstance(e.get("path"), str)}


def _require_exact_artifact(name: str) -> bytes:
    relative = f"research/external-validation/swe-agent-v3/{name}"
    entry = _manifest_entries().get(relative)
    if not isinstance(entry, dict) or set(entry) != {"path"}:
        raise DesignError(f"governed artifact missing from manifest: {name}")
    committed = _committed_blob_bytes(relative)
    if integrity._read_regular(HERE / name) != committed:
        raise DesignError(f"worktree differs from committed artifact: {name}")
    return committed


def verify_preregistration() -> None:
    _require_exact_artifact("preregistration-v1.0.json")
    data = integrity._load_json(HERE / "preregistration-v1.0.json")
    expected_keys = {
        "schema_version", "program_id", "artifact_status", "stage", "execution_authorized",
        "historical_v2_pooling_permitted", "question", "primary_contrast", "secondary_contrasts",
        "minimum_practically_important_difference", "arms", "assignment", "task_population",
        "execution_controls", "outcomes", "analysis", "blinding", "pilot", "nonclaims",
    }
    if set(data) != expected_keys:
        raise DesignError("preregistration top-level shape drifted")
    if (data["schema_version"], data["program_id"], data["artifact_status"], data["stage"]) != ("1.2", "FAR-SWE-V3-001", "Research", "design_only"):
        raise DesignError("preregistration identity drifted")
    if type(data["execution_authorized"]) is not bool or data["execution_authorized"] is not False:
        raise DesignError("preregistration execution boundary drifted")
    if type(data["historical_v2_pooling_permitted"]) is not bool or data["historical_v2_pooling_permitted"] is not False:
        raise DesignError("historical v2 pooling enabled or type drifted")
    integrity._require_type_exact(data["question"], "Under identical execution conditions, does a frozen Project FAR capsule improve software-engineering task resolution relative to an inert structure-matched placebo?", "registered question")
    integrity._require_type_exact(data["primary_contrast"], "far_minus_placebo", "primary contrast")
    integrity._require_type_exact(data["secondary_contrasts"], ["far_minus_baseline", "placebo_minus_baseline"], "secondary contrasts")
    integrity._require_type_exact(data["minimum_practically_important_difference"], 0.1, "minimum practical difference")
    integrity._require_type_exact(data["arms"], EXPECTED_ARMS, "three-arm treatment contract")
    integrity._require_type_exact(data["assignment"], EXPECTED_ASSIGNMENT, "assignment contract")
    integrity._require_type_exact(data["task_population"], EXPECTED_TASK_POPULATION, "task population contract")
    integrity._require_type_exact(data["execution_controls"], EXPECTED_EXECUTION_CONTROLS, "cross-arm execution controls")
    integrity._require_type_exact(data["outcomes"], EXPECTED_OUTCOMES, "outcome contract")
    integrity._require_type_exact(data["analysis"], EXPECTED_ANALYSIS, "analysis contract")
    integrity._require_type_exact(data["blinding"], EXPECTED_BLINDING, "blinding contract")
    integrity._require_type_exact(data["pilot"], EXPECTED_PILOT, "sacrificial pilot contract")
    integrity._require_type_exact(data["nonclaims"], EXPECTED_NONCLAIMS, "preregistration nonclaims")


def verify_task_manifest_contract() -> None:
    _require_exact_artifact("task-manifest-contract-v1.0.json")
    review_closure.verify_task_identity_contract(HERE / "task-manifest-contract-v1.0.json")


def verify_seed_contract() -> None:
    _require_exact_artifact("bootstrap-seed-commitment-contract-v1.0.json")
    review_closure.verify_seed_contract(HERE / "bootstrap-seed-commitment-contract-v1.0.json")


def verify_critical_harm_contract() -> None:
    _require_exact_artifact("critical-harm-thresholds-v1.0.json")
    review_closure.verify_critical_harm_contract(HERE / "critical-harm-thresholds-v1.0.json")


def verify_capsule_contract() -> None:
    _require_exact_artifact("treatment-capsule-contract-v1.0.json")
    data = integrity._load_json(HERE / "treatment-capsule-contract-v1.0.json")
    integrity._require_type_exact(data, EXPECTED_CAPSULE, "complete treatment capsule contract")


def verify_execution_gate() -> None:
    _require_exact_artifact("execution-gate-v1.0.json")
    review_closure.verify_gate_closed(HERE / "execution-gate-v1.0.json")


def _exact_section(text: str, start_heading: str, next_heading: str, expected: str, label: str) -> None:
    start_marker = start_heading + "\n"
    next_marker = next_heading + "\n"
    if text.count(start_marker) != 1 or text.count(next_marker) != 1:
        raise DesignError(f"{label} headings must occur exactly once")
    start = text.index(start_marker)
    end = text.index(next_marker, start + len(start_marker))
    if text[start:end] != expected:
        raise DesignError(f"{label} exact contract drifted")


def verify_text_boundaries() -> None:
    evidence = _require_exact_artifact("evidence-and-analysis-plan-v1.0.md").decode("utf-8")
    readme = _require_exact_artifact("README.md").decode("utf-8")
    question = _require_exact_artifact("question-v1.0.md").decode("utf-8")
    _exact_section(
        evidence,
        "## Evidence bundle per run",
        "## Pre-submission behavior contract",
        EXPECTED_EVIDENCE_BUNDLE_SECTION,
        "retained evidence bundle",
    )
    _exact_section(
        evidence,
        "## Pre-submission behavior contract",
        "## Placebo exposure matching",
        EXPECTED_PRE_SUBMISSION_SECTION,
        "pre-submission behavior",
    )
    required_evidence = (
        "`D_i = p_i(far) - p_i(placebo)`",
        "frozen sealed identity-ledger Git blob identity",
        "The ledger remains sealed from the executing agent and capsule authors.",
        "is not derived from the current capsule, execution gate, task manifest, sealed identity ledger, or any other mutable launch artifact",
        "`critical-harm-thresholds-v1.0.json` is the sole threshold authority",
        "There is no causal-attribution override, operator waiver, or post-hoc exclusion.",
        "greater than or equal to `1/10`",
        "slot numerator, slot denominator, reduced rational incidence rate",
        "cannot retroactively govern existing runs",
        "`launch_record_required_bindings`",
        "A true gate without the complete launch record cannot authorize execution.",
    )
    for phrase in required_evidence:
        if phrase not in evidence:
            raise DesignError(f"evidence/analysis boundary missing: {phrase}")
    forbidden_evidence = ("`D_i = p_i(far) - p_i(baseline)`", "materially higher regression", "materially higher invalid")
    for phrase in forbidden_evidence:
        if phrase in evidence:
            raise DesignError(f"forbidden evidence/analysis wording survived: {phrase}")
    required_readme = (
        "Execution authorized: **No**",
        "bootstrap seed is already prospectively frozen",
        "historical-authority-v1.0.json",
        "critical_harm_thresholds_frozen_and_verified",
        "sealed identity ledger governed by `task-manifest-contract-v1.0.json`",
        "`launch_record_required_bindings`",
        "The reviewed Git commit/tree is the immutable current-byte authority.",
    )
    for phrase in required_readme:
        if phrase not in readme:
            raise DesignError(f"README boundary missing: {phrase}")
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
    verify_seed_contract()
    verify_critical_harm_contract()
    verify_capsule_contract()
    verify_execution_gate()
    verify_text_boundaries()
    try:
        public_narratives.verify(HERE)
    except public_narratives.NarrativeError as exc:
        raise DesignError(f"complete public narrative contract drifted: {exc}") from exc


if __name__ == "__main__":
    try:
        verify()
    except DesignError as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: FAR-SWE-V3-001 semantics verify and execution remains blocked.")
