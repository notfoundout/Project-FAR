#!/usr/bin/env python3
"""Fail-closed verifier for the design-only FAR SWE-agent v3 package."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_integrity as integrity

DesignError = integrity.DesignError
ROOT = integrity.ROOT
HERE = integrity.HERE
MANIFEST = integrity.MANIFEST
_committed_blob_bytes = integrity._committed_blob_bytes
_git_blob_sha1 = integrity._git_blob_sha1

CONTRACT_DIGESTS = {
    "arms": "69842f18cf5309d92bb5fba51a394d77b1ef221264a6881f56fd7d56ef62e095",
    "arm_matching": "386f364130f3cff43092e1eef9c3e45fbf9291e4d3cf10f90878670925f14459",
    "task_population": "a06b42a8b462051535547dc5435864fdb78aa4ab77b73469a01e752c5eac2bad",
    "assignment": "bcb47dde562693980e012d8a2840e28015d6c2d24347138707bc25bf2fa4aceb",
    "execution_controls": "98c69c448baae529a4314b570e92d503df65bf0f581f1241c046c309426aa503",
    "outcomes": "425fbc3a58632b77b5ccfeec264a4d4756f6809d2b3e58cf300c045a26c57f2b",
    "blinding": "0a49cf62f75063a91f88a2d732ba1a12b57fa0a7f2c1961d55232cb005340182",
    "allowed_content": "4d6c91f92ef7c78b9a73a479a45403757b954499b1b212f2bbcdaffba8426824",
    "runtime": "ebea8e1896276afdcdbc3f058f1f52994be991d77c031d821b7b28e5b29d13d6",
    "source": "b6914e456e26124212e124e10d2eda7abefd520a8953f6d5445ec2a2f3238a14",
    "required_outputs": "af9cf47a1dc29cbfb5d91a17ecc685534378f79340355f746497d4e417e2d252",
    "forbidden_content": "add8736a01f34595b59bc4eaf069ca84f38a1c77de7433839dec4f4cd7a35a5b",
    "placebo_matching": "7502f557f9dac08df1afe5d13993785276f5b26b0d33dce49db9fc577f5f0d3d",
    "invalid_policy": "911e4ae6c40c019e204e67bbc5d4ceadb393a10eedb193fcd3df0ada625a550c",
    "decision_categories": "38d6859deb3966d2e887733c959ed8e5ca55db898864a4f7385ba2797f4561d8",
    "decision_precedence": "0d82a12d4a5a7d482c6c8a3800877de00b2aee45735ed6962174b9a90b7afc72",
    "bootstrap": "cb128bfd172c463dc1d4d109ccbc58e1146da0ff5236d690bb30f53079b1e695",
    "task_contract": "9e1a81d50a8513f110da1a749c42709d28356e07d512fea1dc106aba814b4bf2",
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


def verify_preregistration() -> None:
    data = integrity._load_json(HERE / "preregistration-v1.0.json")
    identity = (
        data.get("program_id"),
        data.get("artifact_status"),
        data.get("stage"),
    )
    if identity != ("FAR-SWE-V3-001", "Research", "design_only"):
        raise DesignError("wrong preregistration identity or status")
    if data.get("execution_authorized") is not False:
        raise DesignError("execution must remain prohibited")
    if data.get("historical_v2_pooling_permitted") is not False:
        raise DesignError("historical v2 pooling must remain prohibited")

    arms = data.get("arms")
    if not isinstance(arms, list):
        raise DesignError("arms must be a list")
    integrity._require_digest(
        arms,
        CONTRACT_DIGESTS["arms"],
        "preregistered arm treatment semantics",
    )
    ids = [arm.get("id") for arm in arms if isinstance(arm, dict)]
    if ids != ["baseline", "placebo", "far"]:
        raise DesignError("exact ordered arms baseline, placebo, far required")
    if any(arm.get("required") is not True for arm in arms):
        raise DesignError("all arms must be required")
    integrity._require_digest(
        arms[1].get("matching_requirements"),
        CONTRACT_DIGESTS["arm_matching"],
        "preregistration placebo matching",
    )

    population = data.get("task_population")
    integrity._require_digest(
        population,
        CONTRACT_DIGESTS["task_population"],
        "complete confirmatory task-population contract",
    )
    if not isinstance(population, dict) or population.get("status") != "unfrozen":
        raise DesignError("task population must remain unfrozen")
    if integrity._integer(
        population.get("minimum_task_count"), "minimum_task_count"
    ) < 24:
        raise DesignError("minimum_task_count must be at least 24")
    if integrity._integer(
        population.get("minimum_repository_count"), "minimum_repository_count"
    ) < 5:
        raise DesignError("minimum_repository_count must be at least 5")
    if integrity._number(
        population.get("maximum_fraction_from_one_repository"),
        "maximum_fraction_from_one_repository",
    ) > 0.2:
        raise DesignError("single-repository fraction exceeds 0.20")
    prohibited = " ".join(
        integrity._strings(
            population.get("prohibited_task_repositories"),
            "prohibited repositories",
        )
    ).lower()
    if "project-far" not in prohibited:
        raise DesignError("Project FAR task repository prohibition missing")

    assignment = data.get("assignment")
    integrity._require_digest(
        assignment,
        CONTRACT_DIGESTS["assignment"],
        "complete counterbalancing and assignment contract",
    )
    if not isinstance(assignment, dict):
        raise DesignError("assignment object required")
    if assignment.get("paired_design") is not True:
        raise DesignError("paired design required")
    if assignment.get("every_task_in_every_arm") is not True:
        raise DesignError("every task must appear in every arm")
    if integrity._integer(
        assignment.get("minimum_repetitions_per_task_arm"),
        "minimum repetitions",
    ) < 2:
        raise DesignError("at least two repetitions required")
    if (
        assignment.get("carryover_control")
        != "fresh_workspace_and_fresh_model_context_for_every_run"
    ):
        raise DesignError("fresh workspace and context required")

    integrity._require_digest(
        data.get("execution_controls"),
        CONTRACT_DIGESTS["execution_controls"],
        "execution controls",
    )
    integrity._require_digest(
        data.get("outcomes"),
        CONTRACT_DIGESTS["outcomes"],
        "primary and secondary outcome contract",
    )

    analysis = data.get("analysis")
    if not isinstance(analysis, dict):
        raise DesignError("analysis object required")
    exact = {
        "primary_estimand": "mean_task_level_resolution_probability_far_minus_placebo",
        "task_level_aggregation": "mean over repetitions within each task and arm",
        "uncertainty_method": "paired_task_bootstrap",
        "bootstrap_seed_status": "unfrozen_and_committed_before_outcome_reveal",
    }
    if any(analysis.get(key) != value for key, value in exact.items()):
        raise DesignError("analysis identity mismatch")
    if integrity._integer(
        analysis.get("bootstrap_resamples"), "bootstrap_resamples"
    ) != 100000:
        raise DesignError("bootstrap resample count mismatch")
    if integrity._number(
        data.get("minimum_practically_important_difference"),
        "minimum practical difference",
    ) != 0.1:
        raise DesignError("minimum practical difference must be 0.10")
    if analysis.get("equivalence_or_noninferiority_claim_permitted") is not False:
        raise DesignError("equivalence claims prohibited")
    if analysis.get("population_generalization_permitted") is not False:
        raise DesignError("population generalization prohibited")
    for key, digest_name in (
        ("invalid_run_and_cell_policy", "invalid_policy"),
        ("decision_categories", "decision_categories"),
        ("decision_precedence", "decision_precedence"),
        ("bootstrap_interval_spec", "bootstrap"),
    ):
        integrity._require_digest(
            analysis.get(key),
            CONTRACT_DIGESTS[digest_name],
            key,
        )

    integrity._require_digest(
        data.get("blinding"),
        CONTRACT_DIGESTS["blinding"],
        "preregistration blinding contract",
    )

    pilot = data.get("pilot")
    if not isinstance(pilot, dict):
        raise DesignError("pilot object required")
    if pilot.get("status") != "not_authorized":
        raise DesignError("pilot must remain unauthorized")
    if pilot.get("model_calls_currently_prohibited") is not True:
        raise DesignError("pilot model calls must remain prohibited")
    if pilot.get("pilot_tasks_excluded_from_confirmatory_evidence") is not True:
        raise DesignError("pilot tasks must remain excluded")


def verify_task_manifest_contract() -> None:
    integrity._require_digest(
        integrity._load_json(HERE / "task-manifest-contract-v1.0.json"),
        CONTRACT_DIGESTS["task_contract"],
        "task-manifest ordering and identifier contract",
    )


def verify_capsule_contract() -> None:
    data = integrity._load_json(HERE / "treatment-capsule-contract-v1.0.json")
    if data.get("capsule_status") != "uninstantiated":
        raise DesignError("capsule must remain uninstantiated")
    if data.get("execution_authorized") is not False:
        raise DesignError("capsule execution must remain unauthorized")
    integrity._require_digest(
        data.get("source"),
        CONTRACT_DIGESTS["source"],
        "capsule source provenance",
    )
    integrity._require_digest(
        data.get("required_outputs"),
        CONTRACT_DIGESTS["required_outputs"],
        "capsule identity outputs",
    )
    integrity._require_digest(
        data.get("allowed_content_classes"),
        CONTRACT_DIGESTS["allowed_content"],
        "complete capsule allowed-content boundary",
    )
    integrity._require_digest(
        data.get("forbidden_content_classes"),
        CONTRACT_DIGESTS["forbidden_content"],
        "complete capsule forbidden-content boundary",
    )
    forbidden = " ".join(
        integrity._strings(
            data.get("forbidden_content_classes"),
            "forbidden capsule content",
        )
    ).lower()
    required = ("task identifiers", "gold patches", "hidden tests", "benchmark outcomes")
    if any(term not in forbidden for term in required):
        raise DesignError("forbidden capsule content boundary incomplete")
    integrity._require_digest(
        data.get("runtime_constraints"),
        CONTRACT_DIGESTS["runtime"],
        "capsule runtime",
    )
    integrity._require_digest(
        data.get("placebo_matching"),
        CONTRACT_DIGESTS["placebo_matching"],
        "capsule placebo matching",
    )


def verify_execution_gate() -> None:
    data = integrity._load_json(HERE / "execution-gate-v1.0.json")
    authorization_keys = (
        "execution_authorized",
        "model_calls_authorized",
        "benchmark_execution_authorized",
    )
    if any(data.get(key) is not False for key in authorization_keys):
        raise DesignError("execution must remain unauthorized")
    gates = data.get("gates")
    if not isinstance(gates, dict):
        raise DesignError("gate object required")
    if set(gates) != GATES or any(value is not False for value in gates.values()):
        raise DesignError("execution gate set must be exact and all false")
    forbidden = " ".join(
        integrity._strings(
            data.get("forbidden_current_actions"),
            "forbidden actions",
        )
    ).lower()
    required = (
        "model call",
        "pilot execution",
        "confirmatory execution",
        "outcome reveal",
    )
    if any(term not in forbidden for term in required):
        raise DesignError("forbidden current actions incomplete")


def verify_text_boundaries() -> None:
    evidence = integrity._read_regular(
        HERE / "evidence-and-analysis-plan-v1.0.md"
    ).decode("utf-8").lower()
    required_evidence = (
        "model provider, endpoint, model version, parameters, and provider request identifier",
        "stdout",
        "stderr",
        "trajectory",
        "commands",
        "tool calls",
        "model messages",
        "patch",
        "prediction",
        "grader logs",
        "content-root digest",
        "outer process success cannot override",
        "budget_exhausted",
        "invalid",
        "historical swe-agent v2",
        "abs(placebo_count - far_treatment_count) * 100 <= far_treatment_count",
        "runtime sorting",
        "array order is authoritative",
    )
    if any(term not in evidence for term in required_evidence):
        raise DesignError("evidence or analysis boundary missing")

    claims = "\n".join(
        integrity._read_regular(HERE / path).decode("utf-8").lower()
        for path in ("README.md", "question-v1.0.md")
    )
    if "execution authorized: **no**" not in claims:
        raise DesignError("visible execution boundary missing")
    if "would not establish" not in claims:
        raise DesignError("visible claim boundary missing")
    nonclaims = (
        "universal software-engineering improvement",
        "model-independent improvement",
        "commercial readiness",
    )
    if any(term not in claims for term in nonclaims):
        raise DesignError("explicit nonclaim missing")


def verify() -> None:
    integrity.ROOT = ROOT
    integrity.HERE = HERE
    integrity.MANIFEST = MANIFEST
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
    print(
        "PASS: FAR-SWE-V3-001 design is internally consistent "
        "and execution remains blocked."
    )
