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
    "README.md": "e8ecc4a9c337e57a108b96de16772dcf10081ff2",
    "question-v1.0.md": "b61da8b21953b835d341331e360405d6783d4cf4",
    "preregistration-v1.0.json": "c6c9b5399ef2699ddcd2652dbb2acdd8e820bee1",
    "task-manifest-contract-v1.0.json": "02f12f061a0dcfa61212b27c40ce9a12bdb2c9a0",
    "treatment-capsule-contract-v1.0.json": "e011c8f9972a5682e03526f739437f62e973e76d",
    "execution-gate-v1.0.json": "99eabd1fee9a59770a3a61a07c151abcba23683f",
    "evidence-and-analysis-plan-v1.0.md": "04baff3069bc81f5a23fc2b92c5c04fec855b2c4",
}
PILOT_DIGEST = "847385a29ce4b02d7ece9817dfc4c7772a0583c6b4e0f663248bf3bb02bda478"
FREEZE_SEQUENCE_DIGEST = "198b19ca3ef97f55480077559b47197668ab842474f252f0d7b1faa876186449"
INVALIDATION_RULES_DIGEST = "63b9a2c5989ce78e065133dd0920b67115e1cae9c5cd3d4cc5efa30c96536670"

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
GATES = {
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
    "sacrificial_pilot_completed_and_excluded",
    "independent_preexecution_review_clean",
    "branch_or_tag_protection_and_exact_head_checks_enabled",
    "manual_launch_authorization_recorded",
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
    if analysis.get("bootstrap_resamples") != 100000 or analysis.get("bootstrap_seed_status") != "unfrozen_and_independently_committed_before_execution":
        raise DesignError("bootstrap seed must be independently committed before execution")
    if analysis.get("equivalence_or_noninferiority_claim_permitted") is not False or analysis.get("population_generalization_permitted") is not False:
        raise DesignError("prohibited inference was enabled")
    blinding = data.get("blinding")
    if not isinstance(blinding, dict) or len(blinding) != 4 or any(v is not True for v in blinding.values()):
        raise DesignError("complete blinding contract required")
    integrity._require_digest(data.get("pilot"), PILOT_DIGEST, "sacrificial pilot")


def verify_task_manifest_contract() -> None:
    _require_exact_artifact("task-manifest-contract-v1.0.json")
    data = integrity._load_json(HERE / "task-manifest-contract-v1.0.json")
    if data.get("schema_version") != "1.2":
        raise DesignError("task manifest contract version drifted")
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
    repository_blind = _require_keys(
        record.get("repository_blind_id"),
        {"pattern", "encoding", "unicode_permitted", "canonical_mapping"},
        "repository blind id",
    )
    if repository_blind.get("pattern") != "^REPO-[0-9]{4}$" or repository_blind.get("unicode_permitted") is not False:
        raise DesignError("repository blind-id syntax drifted")
    mapping = repository_blind.get("canonical_mapping", "")
    if "equal authoritative repository identities must use the same blind ID" not in mapping or "distinct authoritative repository identities must use distinct blind IDs" not in mapping:
        raise DesignError("repository blind IDs are not bound one-to-one to authoritative repository identities")
    root_field = _require_keys(
        record.get("task_bundle_root_sha256"), {"pattern", "construction"}, "task bundle root field"
    )
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
    if root.get("algorithm_id") != "far-swe-v3-task-bundle-root-v2" or root.get("hash") != "SHA-256":
        raise DesignError("task bundle root algorithm drifted")
    if root.get("descriptor_canonicalization") != "RFC 8785 JSON Canonicalization Scheme (JCS); UTF-8 bytes; no BOM; no insignificant whitespace":
        raise DesignError("task bundle descriptor canonicalization drifted")
    required_descriptor_keys = [
        "algorithm_id", "repository_provider", "repository_provider_id",
        "canonical_repository_url", "repository_commit_sha",
        "task_payload_sha256", "task_payload_bytes",
    ]
    if root.get("descriptor_required_keys_exactly") != required_descriptor_keys:
        raise DesignError("task bundle descriptor shape drifted")
    values = _require_keys(root.get("descriptor_values"), set(required_descriptor_keys), "task bundle descriptor values")
    if values.get("algorithm_id") != "far-swe-v3-task-bundle-root-v2":
        raise DesignError("task bundle descriptor algorithm identity drifted")
    if "github requires the decimal GitHub REST repository id" not in values.get("repository_provider_id", ""):
        raise DesignError("provider-stable repository identity rule drifted")
    canonical_rule = values.get("canonical_repository_url", "")
    for required in ("default port 443 omitted", "query, fragment, userinfo", "URL spelling is never the repository-count identity"):
        if required not in canonical_rule:
            raise DesignError("canonical repository URL audit rule drifted")
    if root.get("required_root_members") != [
        "authoritative repository provider", "provider-stable repository identity",
        "canonical repository URL", "exact repository commit",
        "exact task/issue payload digest", "exact task/issue payload byte count",
    ]:
        raise DesignError("task bundle required root members drifted")
    if root.get("archive_or_filesystem_metadata_in_root") is not False or root.get("path_order_or_archive_format_in_root") is not False:
        raise DesignError("task bundle root must be independent of archive/path metadata")
    identity = _require_keys(
        data.get("repository_identity_contract"),
        {
            "authoritative_identity", "github_identity_rule", "canonical_url_rule",
            "equal_authoritative_identities_same_blind_id",
            "distinct_authoritative_identities_distinct_blind_ids",
            "minimum_repository_count_basis", "per_repository_cap_basis",
            "validation_timing",
        },
        "repository identity contract",
    )
    if identity.get("equal_authoritative_identities_same_blind_id") is not True or identity.get("distinct_authoritative_identities_distinct_blind_ids") is not True:
        raise DesignError("repository blind-ID mapping must be bijective over authoritative identities")
    github_rule = identity.get("github_identity_rule", "")
    for required in ("decimal REST repository id", "path case", "default HTTPS port spelling", "renames"):
        if required not in github_rule:
            raise DesignError("GitHub repository alias resistance drifted")
    if "(repository_provider, repository_provider_id)" not in identity.get("minimum_repository_count_basis", "") or "(repository_provider, repository_provider_id)" not in identity.get("per_repository_cap_basis", ""):
        raise DesignError("repository count and cap must use provider-stable identity")
    order = data.get("order_contract")
    if not isinstance(order, dict) or order.get("authoritative_sequence") != "top-level JSON array order" or order.get("runtime_sorting_permitted") is not False:
        raise DesignError("task-order contract drifted")
    validations = data.get("preexecution_validation")
    required_validations = {
        "every task bundle root is independently recomputed from the canonical task-bundle descriptor",
        "every canonical repository URL is resolved to one authoritative provider-stable repository identity before counting or blind-ID assignment",
        "equal authoritative repository identities use the same repository blind ID and distinct authoritative repository identities use distinct blind IDs",
        "minimum repository count and per-repository cap are computed from authoritative provider-stable repository identities rather than URL spellings or blind-ID label count",
        "the exact task manifest artifact bytes and Git blob identity are committed before any sacrificial pilot or confirmatory execution",
    }
    if not isinstance(validations, list) or not required_validations.issubset(set(validations)):
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
    _require_keys(
        data,
        {
            "schema_version", "program_id", "artifact_status", "execution_authorized",
            "model_calls_authorized", "benchmark_execution_authorized",
            "pilot_execution_authorized", "confirmatory_execution_authorized",
            "pilot_gate_rule", "gate_rule", "pilot_gates", "gates",
            "current_blockers", "forbidden_current_actions",
        },
        "execution gate",
    )
    if data.get("schema_version") != "1.2":
        raise DesignError("execution-gate version drifted")
    if any(data.get(k) is not False for k in (
        "execution_authorized", "model_calls_authorized", "benchmark_execution_authorized",
        "pilot_execution_authorized", "confirmatory_execution_authorized",
    )):
        raise DesignError("execution and model calls must remain blocked")
    if data.get("pilot_gate_rule") != EXPECTED_PILOT_GATE_RULE:
        raise DesignError("pilot launch rule drifted")
    if data.get("gate_rule") != EXPECTED_GATE_RULE:
        raise DesignError("confirmatory all-gates launch rule drifted")
    pilot_gates = data.get("pilot_gates")
    if not isinstance(pilot_gates, dict) or set(pilot_gates) != PILOT_GATES or any(v is not False for v in pilot_gates.values()):
        raise DesignError("all pre-pilot gates must remain false")
    gates = data.get("gates")
    if not isinstance(gates, dict) or set(gates) != GATES or any(v is not False for v in gates.values()):
        raise DesignError("all confirmatory gates must remain false")
    if "sacrificial_pilot_completed_and_excluded" in pilot_gates:
        raise DesignError("completed pilot cannot be a pilot prerequisite")
    if "sacrificial_pilot_completed_and_excluded" not in gates:
        raise DesignError("confirmatory execution must require completed excluded pilot")
    if len(data.get("current_blockers", [])) != 6:
        raise DesignError("complete current-blocker list required")
    if set(data.get("forbidden_current_actions", [])) != {
        "model access probe", "agent model call",
        "benchmark task selection with capsule-author access", "pilot execution",
        "confirmatory execution", "outcome reveal", "claim of FAR improvement",
    }:
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
