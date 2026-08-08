#!/usr/bin/env python3
"""Fail-closed semantic verifier for the design-only FAR SWE-agent v3 package."""
from __future__ import annotations

import re
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
    "theory_version_frozen",
    "far_capsule_built_and_hash_frozen",
    "placebo_built_and_matching_verified",
    "confirmatory_task_population_frozen",
    "task_identity_information_barriers_verified",
    "model_endpoint_and_version_frozen",
    "prompts_and_agent_configuration_frozen",
    "environment_images_and_dependencies_frozen",
    "budgets_and_stopping_rules_frozen",
    "counterbalancing_and_randomization_seed_frozen",
    "grader_and_scoring_contract_frozen",
    "evidence_store_and_restoration_test_passed",
    "independent_preexecution_review_clean",
    "branch_or_tag_protection_and_exact_head_checks_enabled",
    "manual_pilot_launch_authorization_recorded",
}
GATES = PILOT_GATES | {"sacrificial_pilot_completed_and_excluded"} - {
    "manual_pilot_launch_authorization_recorded"
} | {"manual_launch_authorization_recorded"}
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
    raw = integrity._read_regular(MANIFEST)
    manifest = integrity._decode_json(raw, str(MANIFEST))
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
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("stage"), data.get("execution_authorized")) != (
        "1.0", "FAR-SWE-V3-001", "Research", "design_only", False
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
    if not isinstance(assignment, dict) or assignment.get("paired_design") is not True or assignment.get("every_task_in_every_arm") is not True:
        raise DesignError("paired all-arm assignment required")
    if assignment.get("order") != "counterbalanced_within_task" or assignment.get("carryover_control") != "fresh_workspace_and_fresh_model_context_for_every_run":
        raise DesignError("counterbalancing/carryover contract drifted")
    population = data.get("task_population")
    if not isinstance(population, dict) or population.get("status") != "unfrozen":
        raise DesignError("task population must remain unfrozen")
    if population.get("minimum_task_count", 0) < 24 or population.get("minimum_repository_count", 0) < 5:
        raise DesignError("minimum task population weakened")
    controls = data.get("execution_controls")
    if not isinstance(controls, dict) or len(controls) != 9 or any(v is not True for v in controls.values()):
        raise DesignError("all nine cross-arm controls required")
    outcomes = data.get("outcomes", {}).get("primary")
    if outcomes != {
        "id": "task_resolution", "source": "sealed_external_grader",
        "values": ["resolved", "unresolved", "invalid"], "invalid_is_not_resolved": True,
    }:
        raise DesignError("primary outcome contract drifted")
    analysis = data.get("analysis")
    if not isinstance(analysis, dict) or analysis.get("primary_estimand") != "mean_task_level_resolution_probability_far_minus_placebo":
        raise DesignError("primary estimand drifted")
    if analysis.get("bootstrap_resamples") != 100000 or analysis.get("bootstrap_seed_status") != "unfrozen_and_independently_committed_before_execution":
        raise DesignError("bootstrap seed must be independently committed before execution")
    invalid = analysis.get("invalid_run_and_cell_policy")
    if not isinstance(invalid, dict):
        raise DesignError("invalid/missingness policy missing")
    if invalid.get("replacement_attempts_per_infrastructure_invalid_slot") != 1:
        raise DesignError("replacement count drifted")
    if invalid.get("cell_valid_only_if_every_frozen_repetition_is_valid") is not True or invalid.get("retained_invalid_repetition_makes_entire_task_arm_cell_missing") is not True:
        raise DesignError("retained invalid repetition must poison the cell")
    if invalid.get("primary_missingness_rule") != "if any FAR or placebo task-arm cell is missing, final confirmatory classification is inconclusive_due_to_missingness":
        raise DesignError("primary missingness rule drifted")
    if invalid.get("sensitivity_results_are_confirmatory") is not False:
        raise DesignError("sensitivity results cannot be confirmatory")
    if analysis.get("decision_precedence") != [
        "inconclusive_due_to_missingness", "bounded_harm", "bounded_positive",
        "no_practical_advantage", "inconclusive",
    ]:
        raise DesignError("decision precedence drifted")
    categories = analysis.get("decision_categories", {})
    if "upper bound < 0" not in categories.get("bounded_harm", "") or "0 <= 95% paired-task bootstrap upper bound < 0.10" not in categories.get("no_practical_advantage", ""):
        raise DesignError("decision-category non-overlap drifted")
    interval = analysis.get("bootstrap_interval_spec")
    if not isinstance(interval, dict) or interval.get("method") != "percentile_equal_tailed" or interval.get("resample_count") != 100000:
        raise DesignError("bootstrap interval contract drifted")
    task_order = interval.get("task_order", {})
    if task_order.get("contract") != "task-manifest-contract-v1.0.json":
        raise DesignError("bootstrap task-order authority drifted")
    if task_order.get("source") != "exact frozen ordered task manifest committed and integrity-rooted before any sacrificial pilot or confirmatory execution":
        raise DesignError("bootstrap task-manifest timing drifted")
    if task_order.get("sequence_rule") != "manifest JSON array order is authoritative; runtime sorting and locale collation are prohibited":
        raise DesignError("bootstrap task sequence drifted")
    rng = interval.get("rng_procedure", {})
    if rng.get("id") != "sha256_rejection_stream_v1" or rng.get("digest") != "SHA-256":
        raise DesignError("bootstrap RNG drifted")
    if rng.get("resample_index_origin") != 0 or rng.get("draw_index_origin") != 0 or rng.get("rejection_counter_origin") != 0:
        raise DesignError("bootstrap RNG origins drifted")
    if analysis.get("equivalence_or_noninferiority_claim_permitted") is not False or analysis.get("population_generalization_permitted") is not False:
        raise DesignError("prohibited inference was enabled")
    blinding = data.get("blinding")
    if not isinstance(blinding, dict) or len(blinding) != 4 or any(v is not True for v in blinding.values()):
        raise DesignError("complete blinding contract required")
    if data.get("pilot") != {
        "required": True,
        "status": "not_authorized",
        "purpose": "harness, evidence retention, randomization, restoration, and grader-interface validation only",
        "minimum_sacrificial_tasks": 3,
        "pilot_tasks_excluded_from_confirmatory_evidence": True,
        "model_calls_currently_prohibited": True,
    }:
        raise DesignError("sacrificial pilot contract drifted")


def verify_task_manifest_contract() -> None:
    _require_exact_artifact("task-manifest-contract-v1.0.json")
    data = integrity._load_json(HERE / "task-manifest-contract-v1.0.json")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("manifest_status"), data.get("execution_authorized")) != (
        "1.3", "FAR-SWE-V3-001", "Research", "uninstantiated", False
    ):
        raise DesignError("task manifest identity/boundary drifted")
    freeze = data.get("freeze_timing", "")
    if "before any sacrificial pilot or confirmatory execution" not in freeze or "freezing after any agent run is prohibited" not in freeze:
        raise DesignError("task manifest prospective freeze timing drifted")
    shape = _require_keys(data.get("document_shape"), {"media_type", "top_level_type", "canonical_serialization"}, "task manifest document shape")
    if shape.get("media_type") != "application/json" or shape.get("top_level_type") != "array" or "duplicate keys prohibited" not in shape.get("canonical_serialization", ""):
        raise DesignError("task manifest serialization contract drifted")
    record = _require_keys(
        data.get("record_schema"),
        {"required_keys_exactly", "blind_task_id", "repository_blind_id", "task_bundle_root_sha256"},
        "task manifest record schema",
    )
    if record.get("required_keys_exactly") != ["blind_task_id", "repository_blind_id", "task_bundle_root_sha256"]:
        raise DesignError("task record field set drifted")
    blind = _require_keys(record.get("blind_task_id"), {"pattern", "encoding", "unicode_permitted", "unique"}, "blind task id")
    if blind.get("pattern") != "^TASK-[0-9]{6}$" or blind.get("unicode_permitted") is not False or blind.get("unique") is not True:
        raise DesignError("blind task identity contract drifted")
    repository_blind = _require_keys(record.get("repository_blind_id"), {"pattern", "encoding", "unicode_permitted", "canonical_mapping"}, "repository blind id")
    if repository_blind.get("pattern") != "^REPO-[0-9]{4}$" or repository_blind.get("unicode_permitted") is not False:
        raise DesignError("repository blind-id syntax drifted")
    mapping = repository_blind.get("canonical_mapping", "")
    if "equal authoritative repository identities must use the same blind ID" not in mapping or "distinct authoritative repository identities must use distinct blind IDs" not in mapping:
        raise DesignError("repository blind-ID mapping drifted")
    root_field = _require_keys(record.get("task_bundle_root_sha256"), {"pattern", "construction", "unique"}, "task bundle root field")
    if root_field.get("pattern") != "^[0-9a-f]{64}$" or root_field.get("unique") is not True or "task_bundle_root_contract" not in root_field.get("construction", ""):
        raise DesignError("task-bundle root identity/uniqueness drifted")
    root = _require_keys(
        data.get("task_bundle_root_contract"),
        {"algorithm_id", "hash", "descriptor_media_type", "descriptor_canonicalization", "descriptor_required_keys_exactly", "descriptor_values", "required_root_members", "archive_or_filesystem_metadata_in_root", "path_order_or_archive_format_in_root", "recomputation_rule"},
        "task bundle root contract",
    )
    if root.get("algorithm_id") != "far-swe-v3-task-bundle-root-v2" or root.get("hash") != "SHA-256":
        raise DesignError("task-bundle root algorithm drifted")
    if root.get("descriptor_canonicalization") != "RFC 8785 JSON Canonicalization Scheme (JCS); UTF-8 bytes; no BOM; no insignificant whitespace":
        raise DesignError("task-bundle descriptor canonicalization drifted")
    descriptor_keys = ["algorithm_id", "repository_provider", "repository_provider_id", "canonical_repository_url", "repository_commit_sha", "task_payload_sha256", "task_payload_bytes"]
    if root.get("descriptor_required_keys_exactly") != descriptor_keys:
        raise DesignError("task-bundle descriptor shape drifted")
    values = _require_keys(root.get("descriptor_values"), set(descriptor_keys), "task-bundle descriptor values")
    if values.get("algorithm_id") != "far-swe-v3-task-bundle-root-v2":
        raise DesignError("task-bundle descriptor algorithm drifted")
    if "exact JSON string github.com" not in values.get("repository_provider", "") or "no other provider" not in values.get("repository_provider", ""):
        raise DesignError("GitHub-only repository provider drifted")
    provider_id = values.get("repository_provider_id", "")
    if "positive JSON integer" not in provider_id or "GitHub REST repository id" not in provider_id or "strings" not in provider_id:
        raise DesignError("GitHub repository-provider ID type drifted")
    canonical_url = values.get("canonical_repository_url", "")
    if "https://github.com/{full_name}" not in canonical_url or "audit metadata" not in canonical_url or "never the repository-count identity" not in canonical_url:
        raise DesignError("canonical repository URL role drifted")
    if "lowercase 40-character Git commit SHA" not in values.get("repository_commit_sha", ""):
        raise DesignError("repository commit identity drifted")
    if "lowercase SHA-256" not in values.get("task_payload_sha256", "") or "nonnegative integer byte count" not in values.get("task_payload_bytes", ""):
        raise DesignError("task payload identity drifted")
    if root.get("required_root_members") != [
        "authoritative repository provider", "provider-stable repository identity", "canonical repository URL",
        "exact repository commit", "exact task/issue payload digest", "exact task/issue payload byte count",
    ]:
        raise DesignError("task-bundle required root members drifted")
    if root.get("archive_or_filesystem_metadata_in_root") is not False or root.get("path_order_or_archive_format_in_root") is not False:
        raise DesignError("task-bundle root must be archive/filesystem-order independent")
    identity = _require_keys(
        data.get("repository_identity_contract"),
        {"supported_provider", "authoritative_identity", "github_identity_rule", "canonical_url_rule", "equal_authoritative_identities_same_blind_id", "distinct_authoritative_identities_distinct_blind_ids", "minimum_repository_count_basis", "per_repository_cap_basis", "validation_timing"},
        "repository identity contract",
    )
    if identity.get("supported_provider") != "github.com only":
        raise DesignError("repository provider scope drifted")
    if "positive JSON integer" not in identity.get("authoritative_identity", "") or "api.github.com REST repository id" not in identity.get("authoritative_identity", ""):
        raise DesignError("authoritative repository identity drifted")
    if identity.get("equal_authoritative_identities_same_blind_id") is not True or identity.get("distinct_authoritative_identities_distinct_blind_ids") is not True:
        raise DesignError("repository identity/blind-ID bijection drifted")
    if "(repository_provider, repository_provider_id)" not in identity.get("minimum_repository_count_basis", "") or "(repository_provider, repository_provider_id)" not in identity.get("per_repository_cap_basis", ""):
        raise DesignError("repository count/cap identity basis drifted")
    order = data.get("order_contract")
    if not isinstance(order, dict) or order.get("authoritative_sequence") != "top-level JSON array order" or order.get("runtime_sorting_permitted") is not False or order.get("locale_collation_permitted") is not False:
        raise DesignError("task-order contract drifted")
    validations = data.get("preexecution_validation")
    required = {
        "record keys match the exact schema",
        "blind task identifiers are unique",
        "task bundle roots are unique so one authoritative task identity cannot occupy multiple manifest records or bootstrap units",
        "all identifiers match their ASCII fixed-width patterns",
        "all task bundle roots are lowercase 64-character SHA-256 hex",
        "every task bundle root is independently recomputed from the canonical task-bundle descriptor",
        "every repository_provider is exactly github.com and every repository_provider_id is a positive JSON integer independently resolved from api.github.com before counting or blind-ID assignment",
        "every canonical repository URL is derived from the authoritative GitHub repository id and returned full_name before counting or blind-ID assignment",
        "equal authoritative repository identities use the same repository blind ID and distinct authoritative repository identities use distinct blind IDs",
        "minimum repository count and per-repository cap are computed from authoritative provider-stable repository identities rather than URL spellings or blind-ID label count",
        "the exact task manifest artifact bytes and Git blob identity are committed before any sacrificial pilot or confirmatory execution",
    }
    if not isinstance(validations, list) or set(validations) != required:
        raise DesignError("task-manifest preexecution validation drifted")


def verify_capsule_contract() -> None:
    _require_exact_artifact("treatment-capsule-contract-v1.0.json")
    data = integrity._load_json(HERE / "treatment-capsule-contract-v1.0.json")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("capsule_status"), data.get("execution_authorized")) != (
        "1.0", "FAR-SWE-V3-001", "Research", "uninstantiated", False
    ):
        raise DesignError("capsule identity/boundary drifted")
    if data.get("source") != {"repository": "notfoundout/Project-FAR", "commit_sha": None, "tree_sha": None, "theory_version": None, "exporter_blob_sha": None}:
        raise DesignError("capsule source provenance drifted")
    if data.get("runtime_constraints") != {"read_only": True, "network_access": False, "writes_outside_run_evidence_directory": False, "extra_tool_permissions": False, "extra_context_window": False, "extra_model_calls": False, "mutable_remote_dependencies": False}:
        raise DesignError("capsule runtime constraints drifted")
    if data.get("freeze_sequence") != [
        "freeze theory version and source commit",
        "export candidate FAR capsule deterministically",
        "audit for forbidden task or outcome content",
        "freeze tokenizer identity and compute exposure metrics",
        "construct inert placebo without confirmatory task access",
        "verify matching tolerances",
        "commit capsule and placebo manifests before confirmatory task identities are released",
        "seal exact capsule and placebo bytes",
    ]:
        raise DesignError("capsule freeze sequence drifted")
    if data.get("invalidation_rules") != [
        "any source commit or capsule byte change creates a new experiment version",
        "any confirmatory task identity exposure to a capsule author invalidates the affected task",
        "any unmatched tool, budget, context, read-order, or interaction advantage invalidates the causal contrast",
        "any mutable remote dependency invalidates the capsule",
    ]:
        raise DesignError("capsule invalidation rules drifted")


def verify_execution_gate() -> None:
    _require_exact_artifact("execution-gate-v1.0.json")
    data = integrity._load_json(HERE / "execution-gate-v1.0.json")
    _require_keys(data, {"schema_version", "program_id", "artifact_status", "execution_authorized", "model_calls_authorized", "benchmark_execution_authorized", "pilot_execution_authorized", "confirmatory_execution_authorized", "pilot_gate_rule", "gate_rule", "pilot_gates", "gates", "current_blockers", "forbidden_current_actions"}, "execution gate")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status")) != ("1.2", "FAR-SWE-V3-001", "Research"):
        raise DesignError("execution-gate identity drifted")
    if any(data.get(k) is not False for k in ("execution_authorized", "model_calls_authorized", "benchmark_execution_authorized", "pilot_execution_authorized", "confirmatory_execution_authorized")):
        raise DesignError("execution and model calls must remain blocked")
    if data.get("pilot_gate_rule") != EXPECTED_PILOT_GATE_RULE or data.get("gate_rule") != EXPECTED_GATE_RULE:
        raise DesignError("launch gate rule drifted")
    pilot_gates = data.get("pilot_gates")
    if not isinstance(pilot_gates, dict) or set(pilot_gates) != PILOT_GATES or any(v is not False for v in pilot_gates.values()):
        raise DesignError("all pre-pilot gates must remain false")
    gates = data.get("gates")
    if not isinstance(gates, dict) or set(gates) != GATES or any(v is not False for v in gates.values()):
        raise DesignError("all confirmatory gates must remain false")
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
    if "independently committed before any pilot or confirmatory execution" not in evidence:
        raise DesignError("bootstrap seed prospective commitment narrative drifted")
    if "authoritative repository provider identity, canonical repository URL, and exact commit" not in evidence:
        raise DesignError("repository identity evidence requirement drifted")
    if "Execution authorized: **No**" not in readme or "would not establish" not in question:
        raise DesignError("visible execution or claim boundary missing")
    if "A sacrificial pilot may only be separately authorized after every pre-pilot gate" not in readme:
        raise DesignError("README pilot authorization boundary drifted")
    if "confirmatory execution additionally requires the completed-and-excluded pilot gate" not in readme:
        raise DesignError("README confirmatory authorization boundary drifted")
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
