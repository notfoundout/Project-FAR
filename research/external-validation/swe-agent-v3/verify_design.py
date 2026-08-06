#!/usr/bin/env python3
"""Fail-closed verifier for the design-only FAR SWE-agent v3 package."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = HERE / "design-manifest-v1.0.json"

REQUIRED_ARMS = ["baseline", "placebo", "far"]
REQUIRED_GATE_NAMES = {
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
REQUIRED_EVIDENCE_TERMS = {
    "stdout", "stderr", "trajectory", "commands", "tool calls", "model messages",
    "patch", "prediction", "grader logs", "content-root digest"
}
FORBIDDEN_CLAIMS = {
    "universal software-engineering improvement",
    "model-independent improvement",
    "commercial readiness",
}


class DesignError(RuntimeError):
    pass


def _load_json(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        raise DesignError(f"symlink prohibited: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DesignError(f"invalid JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise DesignError(f"JSON object required: {path}")
    return data


def _safe_manifest_path(relative: str) -> Path:
    posix = PurePosixPath(relative)
    if posix.is_absolute() or ".." in posix.parts or "." in posix.parts or "\\" in relative:
        raise DesignError(f"unsafe manifest path: {relative}")
    current = ROOT
    for part in posix.parts:
        current = current / part
        if current.is_symlink():
            raise DesignError(f"symlink prohibited in manifest path: {relative}")
    resolved = current.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise DesignError(f"manifest path escapes repository: {relative}") from exc
    return current


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest() -> None:
    manifest = _load_json(MANIFEST)
    if manifest.get("schema_version") != "1.0":
        raise DesignError("manifest schema_version must be 1.0")
    entries = manifest.get("artifacts")
    if not isinstance(entries, list) or not entries:
        raise DesignError("manifest artifacts must be non-empty list")
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise DesignError("manifest entry must be object")
        relative = entry.get("path")
        expected = entry.get("sha256")
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise DesignError("manifest path and sha256 required")
        if relative in seen:
            raise DesignError(f"duplicate manifest path: {relative}")
        seen.add(relative)
        path = _safe_manifest_path(relative)
        if not path.is_file():
            raise DesignError(f"missing manifested file: {relative}")
        if _sha256(path) != expected:
            raise DesignError(f"digest mismatch: {relative}")
    required = {
        "research/external-validation/swe-agent-v3/README.md",
        "research/external-validation/swe-agent-v3/question-v1.0.md",
        "research/external-validation/swe-agent-v3/preregistration-v1.0.json",
        "research/external-validation/swe-agent-v3/treatment-capsule-contract-v1.0.json",
        "research/external-validation/swe-agent-v3/execution-gate-v1.0.json",
        "research/external-validation/swe-agent-v3/evidence-and-analysis-plan-v1.0.md",
        "research/external-validation/swe-agent-v3/verify_design.py",
    }
    if seen != required:
        raise DesignError(f"manifest artifact set mismatch: {sorted(seen ^ required)}")


def verify_preregistration() -> None:
    data = _load_json(HERE / "preregistration-v1.0.json")
    if data.get("program_id") != "FAR-SWE-V3-001":
        raise DesignError("wrong program_id")
    if data.get("artifact_status") != "Research" or data.get("stage") != "design_only":
        raise DesignError("package must remain Research/design_only")
    if data.get("execution_authorized") is not False:
        raise DesignError("execution must remain unauthorized")
    if data.get("historical_v2_pooling_permitted") is not False:
        raise DesignError("historical v2 pooling must be prohibited")

    arms = data.get("arms")
    if not isinstance(arms, list) or [arm.get("id") for arm in arms] != REQUIRED_ARMS:
        raise DesignError("exact ordered arms baseline, placebo, far required")
    if not all(arm.get("required") is True for arm in arms):
        raise DesignError("all three arms must be required")

    matching = arms[1].get("matching_requirements")
    if not isinstance(matching, dict):
        raise DesignError("placebo matching requirements missing")
    for key in (
        "file_count_exact", "relative_path_shape_exact", "directory_depth_exact",
        "read_order_exact", "interaction_turns_exact", "tool_permissions_exact"
    ):
        if matching.get(key) is not True:
            raise DesignError(f"placebo exact match required: {key}")
    for key in ("utf8_bytes_relative_tolerance", "frozen_tokenizer_tokens_relative_tolerance"):
        value = matching.get(key)
        if not isinstance(value, (int, float)) or value < 0 or value > 0.01:
            raise DesignError(f"placebo tolerance too weak: {key}")

    population = data.get("task_population")
    if not isinstance(population, dict) or population.get("status") != "unfrozen":
        raise DesignError("task population must remain unfrozen")
    if population.get("minimum_task_count", 0) < 24:
        raise DesignError("minimum_task_count must be at least 24")
    if population.get("minimum_repository_count", 0) < 5:
        raise DesignError("minimum_repository_count must be at least 5")
    if population.get("maximum_fraction_from_one_repository", 1) > 0.20:
        raise DesignError("single-repository fraction exceeds 0.20")
    prohibited = " ".join(population.get("prohibited_task_repositories", [])).lower()
    if "project-far" not in prohibited and "project far" not in prohibited:
        raise DesignError("Project FAR must be prohibited as a task repository")

    assignment = data.get("assignment", {})
    if assignment.get("paired_design") is not True or assignment.get("every_task_in_every_arm") is not True:
        raise DesignError("paired all-arm task design required")
    if assignment.get("minimum_repetitions_per_task_arm", 0) < 2:
        raise DesignError("at least two repetitions per task-arm required")
    if assignment.get("carryover_control") != "fresh_workspace_and_fresh_model_context_for_every_run":
        raise DesignError("fresh workspace and model context required")

    controls = data.get("execution_controls", {})
    for key in (
        "same_model_endpoint_across_arms", "model_fallback_prohibited",
        "same_system_and_agent_prompts_except_capsule_mount",
        "same_repository_commit_across_arms", "same_environment_image_across_arms",
        "same_tools_across_arms", "same_call_token_time_and_cost_budgets_across_arms",
        "fresh_context_per_run", "parallel_cross_arm_information_sharing_prohibited"
    ):
        if controls.get(key) is not True:
            raise DesignError(f"execution control must be true: {key}")

    analysis = data.get("analysis", {})
    if analysis.get("primary_estimand") != "mean_task_level_resolution_probability_far_minus_placebo":
        raise DesignError("wrong primary estimand")
    if analysis.get("equivalence_or_noninferiority_claim_permitted") is not False:
        raise DesignError("equivalence/noninferiority claims must be prohibited")
    if analysis.get("population_generalization_permitted") is not False:
        raise DesignError("population generalization must be prohibited")
    if data.get("minimum_practically_important_difference") != 0.10:
        raise DesignError("minimum practically important difference must remain 0.10")

    pilot = data.get("pilot", {})
    if pilot.get("status") != "not_authorized" or pilot.get("model_calls_currently_prohibited") is not True:
        raise DesignError("pilot must remain unauthorized with model calls prohibited")
    if pilot.get("pilot_tasks_excluded_from_confirmatory_evidence") is not True:
        raise DesignError("pilot tasks must be excluded")


def verify_capsule_contract() -> None:
    data = _load_json(HERE / "treatment-capsule-contract-v1.0.json")
    if data.get("capsule_status") != "uninstantiated" or data.get("execution_authorized") is not False:
        raise DesignError("capsule must remain uninstantiated and unauthorized")
    source = data.get("source", {})
    for key in ("commit_sha", "tree_sha", "theory_version", "exporter_blob_sha"):
        if source.get(key) is not None:
            raise DesignError(f"source {key} must be null before theory freeze")
    forbidden = " ".join(data.get("forbidden_content_classes", [])).lower()
    for token in ("task identifiers", "gold patches", "hidden tests", "benchmark outcomes"):
        if token not in forbidden:
            raise DesignError(f"missing forbidden capsule content: {token}")
    runtime = data.get("runtime_constraints", {})
    if runtime.get("network_access") is not False:
        raise DesignError("capsule network access must be false")
    if runtime.get("extra_model_calls") is not False or runtime.get("extra_tool_permissions") is not False:
        raise DesignError("capsule cannot add model calls or tool permissions")


def verify_execution_gate() -> None:
    data = _load_json(HERE / "execution-gate-v1.0.json")
    if data.get("execution_authorized") is not False:
        raise DesignError("execution gate must be false")
    if data.get("model_calls_authorized") is not False or data.get("benchmark_execution_authorized") is not False:
        raise DesignError("model and benchmark execution must be false")
    gates = data.get("gates")
    if not isinstance(gates, dict) or set(gates) != REQUIRED_GATE_NAMES:
        raise DesignError("execution gate set mismatch")
    if any(value is not False for value in gates.values()):
        raise DesignError("all execution gates must remain false in design-only package")
    forbidden = " ".join(data.get("forbidden_current_actions", [])).lower()
    for term in ("model call", "pilot execution", "confirmatory execution", "outcome reveal"):
        if term not in forbidden:
            raise DesignError(f"missing forbidden current action: {term}")


def verify_evidence_plan() -> None:
    text = (HERE / "evidence-and-analysis-plan-v1.0.md").read_text(encoding="utf-8").lower()
    for term in REQUIRED_EVIDENCE_TERMS:
        if term not in text:
            raise DesignError(f"missing evidence term: {term}")
    for term in ("outer process success cannot override", "budget_exhausted", "invalid", "historical swe-agent v2"):
        if term not in text:
            raise DesignError(f"missing evidence boundary: {term}")


def verify_claim_boundary() -> None:
    text = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in (HERE / "README.md", HERE / "question-v1.0.md")
    )
    if "execution authorized: **no**" not in text:
        raise DesignError("README must visibly deny execution authorization")
    if "would not establish" not in text:
        raise DesignError("claim boundary missing")
    for claim in FORBIDDEN_CLAIMS:
        if claim not in text:
            raise DesignError(f"explicit nonclaim missing: {claim}")


def verify() -> None:
    verify_manifest()
    verify_preregistration()
    verify_capsule_contract()
    verify_execution_gate()
    verify_evidence_plan()
    verify_claim_boundary()


if __name__ == "__main__":
    try:
        verify()
    except DesignError as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: FAR-SWE-V3-001 design is internally consistent and execution remains blocked.")
