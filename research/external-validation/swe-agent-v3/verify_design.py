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
    "theory_version_frozen", "far_capsule_built_and_hash_frozen",
    "placebo_built_and_matching_verified", "confirmatory_task_population_frozen",
    "task_identity_information_barriers_verified", "model_endpoint_and_version_frozen",
    "prompts_and_agent_configuration_frozen", "environment_images_and_dependencies_frozen",
    "budgets_and_stopping_rules_frozen", "counterbalancing_and_randomization_seed_frozen",
    "grader_and_scoring_contract_frozen", "evidence_store_and_restoration_test_passed",
    "independent_preexecution_review_clean", "branch_or_tag_protection_and_exact_head_checks_enabled",
    "manual_pilot_launch_authorization_recorded",
}
GATES = {
    "theory_version_frozen", "far_capsule_built_and_hash_frozen",
    "placebo_built_and_matching_verified", "confirmatory_task_population_frozen",
    "task_identity_information_barriers_verified", "model_endpoint_and_version_frozen",
    "prompts_and_agent_configuration_frozen", "environment_images_and_dependencies_frozen",
    "budgets_and_stopping_rules_frozen", "counterbalancing_and_randomization_seed_frozen",
    "grader_and_scoring_contract_frozen", "evidence_store_and_restoration_test_passed",
    "sacrificial_pilot_completed_and_excluded", "independent_preexecution_review_clean",
    "branch_or_tag_protection_and_exact_head_checks_enabled", "manual_launch_authorization_recorded",
}
EXPECTED_PILOT_GATE_RULE = (
    "sacrificial pilot execution is authorized only when every pilot gate is true, "
    "the exact design manifest verifies, and a separate prospective pilot launch "
    "record names the frozen commit; sacrificial_pilot_completed_and_excluded is "
    "not a pilot prerequisite"
)
EXPECTED_GATE_RULE = (
    "confirmatory execution is authorized only when every gate is true, the exact "
    "design manifest verifies, and a separate prospective confirmatory launch record "
    "names the frozen commit"
)


def _manifest_entries() -> dict[str, dict[str, Any]]:
    manifest = integrity._decode_json(integrity._read_regular(MANIFEST), str(MANIFEST))
    if not isinstance(manifest, dict) or not isinstance(manifest.get("artifacts"), list):
        raise DesignError("verified design manifest required")
    out: dict[str, dict[str, Any]] = {}
    for entry in manifest["artifacts"]:
        if not isinstance(entry, dict) or type(entry.get("path")) is not str:
            raise DesignError("invalid governed-artifact manifest entry")
        out[entry["path"]] = entry
    return out


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


def _require_keys(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise DesignError(f"exact key set required: {label}")
    return value


def verify_preregistration() -> None:
    _require_exact_artifact("preregistration-v1.0.json")
    data = integrity._load_json(HERE / "preregistration-v1.0.json")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("stage"), data.get("execution_authorized")) != ("1.0", "FAR-SWE-V3-001", "Research", "design_only", False):
        raise DesignError("preregistration identity or execution boundary drifted")
    if data.get("primary_contrast") != "far_minus_placebo" or data.get("secondary_contrasts") != ["far_minus_baseline", "placebo_minus_baseline"]:
        raise DesignError("contrast contract drifted")
    if data.get("historical_v2_pooling_permitted") is not False:
        raise DesignError("historical v2 pooling must remain prohibited")
    arms = data.get("arms")
    if not isinstance(arms, list) or [x.get("id") for x in arms] != ["baseline", "placebo", "far"] or any(x.get("required") is not True for x in arms):
        raise DesignError("exact mandatory three-arm order required")
    if arms[0].get("extra_capsule") is not None or arms[1].get("extra_capsule") != "placebo" or arms[2].get("extra_capsule") != "far" or arms[2].get("capsule_contract") != "treatment-capsule-contract-v1.0.json":
        raise DesignError("arm treatment mapping drifted")
    tolerance = arms[1].get("matching_requirements", {}).get("relative_tolerance")
    expected_tolerance = {
        "applies_to": ["utf8_bytes", "frozen_tokenizer_tokens"],
        "maximum_absolute_relative_difference": {"numerator": 1, "denominator": 100},
        "reference_count": "far_treatment_count", "far_count_requirement": "positive integer",
        "placebo_count_requirement": "nonnegative integer", "boundary": "inclusive", "rounding": "none",
        "floating_point_permitted": False,
        "integer_acceptance_rule": "abs(placebo_count - far_treatment_count) * 100 <= far_treatment_count",
    }
    if tolerance != expected_tolerance:
        raise DesignError("placebo tolerance contract drifted")
    assignment = data.get("assignment", {})
    if assignment.get("paired_design") is not True or assignment.get("every_task_in_every_arm") is not True or assignment.get("order") != "counterbalanced_within_task" or assignment.get("carryover_control") != "fresh_workspace_and_fresh_model_context_for_every_run":
        raise DesignError("paired assignment/carryover contract drifted")
    population = data.get("task_population", {})
    if population.get("status") != "unfrozen" or population.get("minimum_task_count", 0) < 24 or population.get("minimum_repository_count", 0) < 5:
        raise DesignError("task population contract weakened")
    controls = data.get("execution_controls")
    if not isinstance(controls, dict) or set(controls) != {
        "same_model_endpoint_across_arms", "model_fallback_prohibited",
        "same_system_and_agent_prompts_except_capsule_mount", "same_repository_commit_across_arms",
        "same_environment_image_across_arms", "same_tools_across_arms",
        "same_call_token_time_and_cost_budgets_across_arms", "fresh_context_per_run",
        "parallel_cross_arm_information_sharing_prohibited",
    } or any(v is not True for v in controls.values()):
        raise DesignError("all nine exact cross-arm controls required")
    if data.get("outcomes", {}).get("primary") != {"id": "task_resolution", "source": "sealed_external_grader", "values": ["resolved", "unresolved", "invalid"], "invalid_is_not_resolved": True}:
        raise DesignError("primary outcome contract drifted")
    analysis = data.get("analysis", {})
    if analysis.get("primary_estimand") != "mean_task_level_resolution_probability_far_minus_placebo" or analysis.get("uncertainty_method") != "paired_task_bootstrap" or analysis.get("bootstrap_resamples") != 100000 or analysis.get("bootstrap_seed_status") != "unfrozen_and_independently_committed_before_execution":
        raise DesignError("primary analysis/bootstrap contract drifted")
    invalid = analysis.get("invalid_run_and_cell_policy", {})
    if invalid.get("replacement_attempts_per_infrastructure_invalid_slot") != 1 or invalid.get("cell_valid_only_if_every_frozen_repetition_is_valid") is not True or invalid.get("retained_invalid_repetition_makes_entire_task_arm_cell_missing") is not True or invalid.get("primary_missingness_rule") != "if any FAR or placebo task-arm cell is missing, final confirmatory classification is inconclusive_due_to_missingness" or invalid.get("sensitivity_results_are_confirmatory") is not False:
        raise DesignError("invalid-run/missingness contract drifted")
    if analysis.get("decision_precedence") != ["inconclusive_due_to_missingness", "bounded_harm", "bounded_positive", "no_practical_advantage", "inconclusive"]:
        raise DesignError("decision precedence drifted")
    categories = analysis.get("decision_categories", {})
    if "upper bound < 0" not in categories.get("bounded_harm", "") or "0 <= 95% paired-task bootstrap upper bound < 0.10" not in categories.get("no_practical_advantage", ""):
        raise DesignError("decision categories overlap or drifted")
    interval = analysis.get("bootstrap_interval_spec", {})
    task_order = interval.get("task_order", {})
    if interval.get("method") != "percentile_equal_tailed" or interval.get("resample_count") != 100000 or task_order.get("contract") != "task-manifest-contract-v1.0.json" or task_order.get("source") != "exact frozen ordered task manifest committed and integrity-rooted before any sacrificial pilot or confirmatory execution" or task_order.get("sequence_rule") != "manifest JSON array order is authoritative; runtime sorting and locale collation are prohibited":
        raise DesignError("bootstrap interval/task-order contract drifted")
    rng = interval.get("rng_procedure", {})
    if rng.get("id") != "sha256_rejection_stream_v1" or rng.get("digest") != "SHA-256" or [rng.get("resample_index_origin"), rng.get("draw_index_origin"), rng.get("rejection_counter_origin")] != [0, 0, 0]:
        raise DesignError("bootstrap RNG contract drifted")
    if analysis.get("equivalence_or_noninferiority_claim_permitted") is not False or analysis.get("population_generalization_permitted") is not False:
        raise DesignError("prohibited inference enabled")
    blinding = data.get("blinding")
    if not isinstance(blinding, dict) or len(blinding) != 4 or any(v is not True for v in blinding.values()):
        raise DesignError("complete blinding contract required")
    if data.get("pilot") != {"required": True, "status": "not_authorized", "purpose": "harness, evidence retention, randomization, restoration, and grader-interface validation only", "minimum_sacrificial_tasks": 3, "pilot_tasks_excluded_from_confirmatory_evidence": True, "model_calls_currently_prohibited": True}:
        raise DesignError("sacrificial pilot contract drifted")


def verify_task_manifest_contract() -> None:
    _require_exact_artifact("task-manifest-contract-v1.0.json")
    data = integrity._load_json(HERE / "task-manifest-contract-v1.0.json")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("manifest_status"), data.get("execution_authorized")) != ("1.3", "FAR-SWE-V3-001", "Research", "uninstantiated", False):
        raise DesignError("task manifest identity/boundary drifted")
    freeze = data.get("freeze_timing", "")
    if "before any sacrificial pilot or confirmatory execution" not in freeze or "freezing after any agent run is prohibited" not in freeze:
        raise DesignError("task manifest freeze timing drifted")
    record = _require_keys(data.get("record_schema"), {"required_keys_exactly", "blind_task_id", "repository_blind_id", "task_bundle_root_sha256"}, "task record schema")
    if record.get("required_keys_exactly") != ["blind_task_id", "repository_blind_id", "task_bundle_root_sha256"]:
        raise DesignError("task record key set drifted")
    blind = _require_keys(record.get("blind_task_id"), {"pattern", "encoding", "unicode_permitted", "unique"}, "blind task id")
    if blind.get("pattern") != "^TASK-[0-9]{6}$" or blind.get("unicode_permitted") is not False or blind.get("unique") is not True:
        raise DesignError("blind task identity drifted")
    repo_blind = _require_keys(record.get("repository_blind_id"), {"pattern", "encoding", "unicode_permitted", "canonical_mapping"}, "repository blind id")
    if repo_blind.get("pattern") != "^REPO-[0-9]{4}$" or repo_blind.get("unicode_permitted") is not False or "one-to-one" not in repo_blind.get("canonical_mapping", ""):
        raise DesignError("repository blind identity drifted")
    task_root = _require_keys(record.get("task_bundle_root_sha256"), {"pattern", "construction", "unique"}, "task bundle root")
    if task_root.get("pattern") != "^[0-9a-f]{64}$" or task_root.get("unique") is not True or "task_bundle_root_contract" not in task_root.get("construction", ""):
        raise DesignError("task root identity/uniqueness drifted")
    root = data.get("task_bundle_root_contract", {})
    descriptor_keys = ["algorithm_id", "repository_provider", "repository_provider_id", "canonical_repository_url", "repository_commit_sha", "task_payload_sha256", "task_payload_bytes"]
    if root.get("algorithm_id") != "far-swe-v3-task-bundle-root-v2" or root.get("hash") != "SHA-256" or root.get("descriptor_canonicalization") != "RFC 8785 JSON Canonicalization Scheme (JCS); UTF-8 bytes; no BOM; no insignificant whitespace" or root.get("descriptor_required_keys_exactly") != descriptor_keys:
        raise DesignError("task-bundle root/descriptor contract drifted")
    values = root.get("descriptor_values", {})
    if set(values) != set(descriptor_keys) or "exact JSON string github.com" not in values.get("repository_provider", "") or "positive JSON integer" not in values.get("repository_provider_id", "") or "GitHub REST repository id" not in values.get("repository_provider_id", "") or "audit metadata" not in values.get("canonical_repository_url", "") or "never the repository-count identity" not in values.get("canonical_repository_url", "") or "lowercase 40-character Git commit SHA" not in values.get("repository_commit_sha", ""):
        raise DesignError("task-bundle repository identity contract drifted")
    if root.get("archive_or_filesystem_metadata_in_root") is not False or root.get("path_order_or_archive_format_in_root") is not False:
        raise DesignError("task root must be archive/path-order independent")
    identity = data.get("repository_identity_contract", {})
    if identity.get("supported_provider") != "github.com only" or "positive JSON integer" not in identity.get("authoritative_identity", "") or identity.get("equal_authoritative_identities_same_blind_id") is not True or identity.get("distinct_authoritative_identities_distinct_blind_ids") is not True:
        raise DesignError("authoritative repository identity drifted")
    for key in ("minimum_repository_count_basis", "per_repository_cap_basis"):
        if "(repository_provider, repository_provider_id)" not in identity.get(key, ""):
            raise DesignError("repository count/cap identity basis drifted")
    order = data.get("order_contract", {})
    if order.get("authoritative_sequence") != "top-level JSON array order" or order.get("runtime_sorting_permitted") is not False or order.get("locale_collation_permitted") is not False:
        raise DesignError("task order contract drifted")
    validations = data.get("preexecution_validation")
    required = {
        "record keys match the exact schema", "blind task identifiers are unique",
        "task bundle roots are unique so one authoritative task identity cannot occupy multiple manifest records or bootstrap units",
        "all identifiers match their ASCII fixed-width patterns", "all task bundle roots are lowercase 64-character SHA-256 hex",
        "every task bundle root is independently recomputed from the canonical task-bundle descriptor",
        "every repository_provider is exactly github.com and every repository_provider_id is a positive JSON integer independently resolved from api.github.com before counting or blind-ID assignment",
        "every canonical repository URL is derived from the authoritative GitHub repository id and returned full_name before counting or blind-ID assignment",
        "equal authoritative repository identities use the same repository blind ID and distinct authoritative repository identities use distinct blind IDs",
        "minimum repository count and per-repository cap are computed from authoritative provider-stable repository identities rather than URL spellings or blind-ID label count",
        "the exact task manifest artifact bytes and Git blob identity are committed before any sacrificial pilot or confirmatory execution",
    }
    if not isinstance(validations, list) or set(validations) != required:
        raise DesignError("task preexecution validation drifted")


def verify_capsule_contract() -> None:
    _require_exact_artifact("treatment-capsule-contract-v1.0.json")
    data = integrity._load_json(HERE / "treatment-capsule-contract-v1.0.json")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("capsule_status"), data.get("execution_authorized")) != ("1.0", "FAR-SWE-V3-001", "Research", "uninstantiated", False):
        raise DesignError("capsule identity/boundary drifted")
    if data.get("source") != {"repository": "notfoundout/Project-FAR", "commit_sha": None, "tree_sha": None, "theory_version": None, "exporter_blob_sha": None}:
        raise DesignError("capsule source provenance drifted")
    if data.get("runtime_constraints") != {"read_only": True, "network_access": False, "writes_outside_run_evidence_directory": False, "extra_tool_permissions": False, "extra_context_window": False, "extra_model_calls": False, "mutable_remote_dependencies": False}:
        raise DesignError("capsule runtime constraints drifted")
    tol = data.get("placebo_matching", {}).get("relative_tolerance")
    if tol != {"applies_to": ["utf8_bytes", "frozen_tokenizer_tokens"], "maximum_absolute_relative_difference": {"numerator": 1, "denominator": 100}, "reference_count": "far_treatment_count", "far_count_requirement": "positive integer", "placebo_count_requirement": "nonnegative integer", "boundary": "inclusive", "rounding": "none", "floating_point_permitted": False, "integer_acceptance_rule": "abs(placebo_count - far_treatment_count) * 100 <= far_treatment_count"}:
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
    if any(data.get(k) is not False for k in ("execution_authorized", "model_calls_authorized", "benchmark_execution_authorized", "pilot_execution_authorized", "confirmatory_execution_authorized")):
        raise DesignError("execution/model calls must remain blocked")
    if data.get("pilot_gate_rule") != EXPECTED_PILOT_GATE_RULE or data.get("gate_rule") != EXPECTED_GATE_RULE:
        raise DesignError("launch rule drifted")
    pilot = data.get("pilot_gates")
    gates = data.get("gates")
    if not isinstance(pilot, dict) or set(pilot) != PILOT_GATES or any(v is not False for v in pilot.values()):
        raise DesignError("pre-pilot gate set drifted")
    if not isinstance(gates, dict) or set(gates) != GATES or any(v is not False for v in gates.values()):
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
        raise DesignError("prospective evidence identity boundary drifted")
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
