from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

CASE_DIR = Path(__file__).parent
MANIFEST = CASE_DIR / "manifest.json"
CONFIG = CASE_DIR / "agent-config.yaml"

REQUIRED_TOP_LEVEL = {
    "schema", "case_id", "status", "source", "comparison_design", "frozen_inputs",
    "execution_environment", "execution_requirements", "required_artifacts",
    "primary_questions", "decision_policy", "forbidden_before_primary_freeze",
    "claim_boundary",
}
REQUIRED_DECISIONS = {"PASS", "BLOCKED", "REVIEW_REQUIRED", "UNKNOWN"}
REQUIRED_BLINDED_FIELDS = {
    "benchmark_resolution_status", "test_pass_fail", "reward", "grader_output",
    "human_success_label", "candidate_preference",
}
DECLARATION_PATH = ("forbidden_before_primary_freeze",)
EXPECTED_RUNS = {
    ("v1.0.0", "8ed382c", 1, "baseline-run-1.traj"),
    ("v1.0.0", "8ed382c", 2, "baseline-run-2.traj"),
    ("v1.0.1", "6aff215", 1, "candidate-run-1.traj"),
    ("v1.0.1", "6aff215", 2, "candidate-run-2.traj"),
}
HARNESS_COMMIT = "f7bbbb2ccdf479001d6467c9e34af59e44a840f9"
REQUIRED_ENVIRONMENT_ARTIFACTS = {
    "task-record.public.json", "test-spec.json", "Dockerfile.base", "Dockerfile.env",
    "Dockerfile.instance", "setup-env.sh", "install-repo.sh", "environment-lock.json",
    "environment-lock.sha256",
}
FORBIDDEN_ENVIRONMENT_ARTIFACTS = {"task-record.json", "setup-repo.sh", "eval.sh"}


def _forbidden_paths(value: Any, path: tuple[str, ...] = ()) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = path + (str(key),)
            if key in REQUIRED_BLINDED_FIELDS and path != DECLARATION_PATH:
                found.append(".".join(child_path))
            found.extend(_forbidden_paths(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_forbidden_paths(child, path + (str(index),)))
    return found


def _valid_sha256(value: object, *, prefixed: bool = False) -> bool:
    if not isinstance(value, str):
        return False
    if prefixed:
        return len(value) == 71 and value.startswith("sha256:") and all(c in "0123456789abcdef" for c in value[7:])
    return len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def validate(payload: dict) -> None:
    missing = REQUIRED_TOP_LEVEL - payload.keys()
    assert not missing, f"missing top-level fields: {sorted(missing)}"
    assert payload["schema"] == "far-external-release-comparison/0.3"
    assert payload["source"] == {
        "repository": "https://github.com/SWE-agent/SWE-agent",
        "baseline_ref": "v1.0.0",
        "baseline_commit": "8ed382c",
        "candidate_ref": "v1.0.1",
        "candidate_commit": "6aff215",
        "release_notes_source": "official_github_releases",
    }

    design = payload["comparison_design"]
    for field in (
        "same_task", "same_model", "same_model_parameters", "same_agent_configuration",
        "same_environment_image", "same_task_seed", "isolated_workspaces",
        "outcome_blinded_until_primary_freeze",
    ):
        assert design[field] is True, f"{field} must remain true"
    assert design["minimum_repetitions_per_release"] == 2

    assert set(payload["decision_policy"]) == REQUIRED_DECISIONS
    assert set(payload["forbidden_before_primary_freeze"]) == REQUIRED_BLINDED_FIELDS
    leaked_paths = _forbidden_paths(payload)
    assert not leaked_paths, f"pre-freeze outcome leakage: {sorted(leaked_paths)}"

    frozen = payload["frozen_inputs"]
    assert frozen["task_id"] == "scikit-learn__scikit-learn-14125"
    assert frozen["swebench_repository"] == "https://github.com/SWE-bench/SWE-bench"
    assert frozen["swebench_harness_commit"] == HARNESS_COMMIT
    assert frozen["swebench_dataset"] == "princeton-nlp/SWE-bench"
    assert frozen["swebench_split"] == "test"
    assert frozen["environment_construction"] == "official_swebench_local_build_namespace_none"
    assert frozen["environment_lock_path"] == "environment-freeze/environment-lock.json"
    assert frozen["model"] == "gemini/gemini-2.5-pro"
    assert frozen["provider_model"] == "gemini-2.5-pro"
    assert frozen["model_parameters"] == {
        "temperature": 0.0,
        "top_p": 1.0,
        "per_instance_cost_limit_usd": 0.0,
        "total_cost_limit_usd": 0.0,
        "per_instance_call_limit": 30,
        "minimum_delay_seconds": 15.0,
        "retry_min_wait_seconds": 30,
        "retry_max_wait_seconds": 600,
    }
    constraints = frozen["free_tier_constraints"]
    assert constraints["billing_required"] is False
    assert constraints["quota_not_guaranteed"] is True
    assert constraints["provider_may_use_inputs_and_outputs_to_improve_products"] is True
    assert frozen["task_seed"] == 14125
    assert len(frozen["model_selection_sources"]) >= 3
    actual_config_hash = hashlib.sha256(CONFIG.read_bytes()).hexdigest()
    assert actual_config_hash == frozen["agent_config_sha256"], "agent config hash mismatch"

    status = payload["status"]
    if status == "execution_inputs_frozen":
        assert _valid_sha256(frozen["environment_lock_sha256"])
        assert _valid_sha256(frozen["local_image_id"], prefixed=True)
        assert _valid_sha256(frozen["registry_digest"], prefixed=True)
        expected_ref = "ghcr.io/notfoundout/project-far-swebench-scikit-learn-14125@" + frozen["registry_digest"]
        assert frozen["immutable_image_reference"] == expected_ref
    else:
        assert status == "execution_inputs_selected_local_environment_build_pending"
        assert frozen["environment_lock_sha256"] is None
        assert frozen["local_image_id"] is None
        assert "immutable_image_reference" not in frozen
        assert "registry_digest" not in frozen

    assert "environment_image_reference" not in frozen
    assert "environment_image_digest" not in frozen

    environment = payload["execution_environment"]
    assert environment["provider"] == "github_actions"
    assert environment["runner"] == "ubuntu-24.04"
    assert environment["credential_secret"] == "GEMINI_API_KEY"
    assert environment["manual_dispatch_only"] is True

    requirements = payload["execution_requirements"]
    assert requirements["required_secret"] == "GEMINI_API_KEY"
    assert requirements["maximum_total_model_cost_usd"] == 0.0
    assert requirements["build_and_freeze_local_environment_before_first_model_call"] is True
    assert requirements["remote_image_resolution_forbidden"] is True
    assert requirements["sequential_runs_required"] is True
    assert requirements["resume_after_rate_limit"] is True
    runs = requirements["runs"]
    assert len(runs) == 4
    assert {
        (r["release"], r["commit"], r["repetition"], r["trajectory_artifact"])
        for r in runs
    } == EXPECTED_RUNS

    artifacts = set(payload["required_artifacts"])
    assert REQUIRED_ENVIRONMENT_ARTIFACTS <= artifacts, (
        "missing required environment artifacts: "
        f"{sorted(REQUIRED_ENVIRONMENT_ARTIFACTS - artifacts)}"
    )
    assert not (FORBIDDEN_ENVIRONMENT_ARTIFACTS & artifacts), (
        "outcome-bearing or obsolete environment artifacts declared: "
        f"{sorted(FORBIDDEN_ENVIRONMENT_ARTIFACTS & artifacts)}"
    )
    assert {
        "baseline-run-1.traj", "baseline-run-2.traj", "candidate-run-1.traj",
        "candidate-run-2.traj", "primary_freeze_manifest", "post_freeze_outcome_reveal",
        "bundle_sha256_manifest",
    } <= artifacts

    forbidden_text = json.dumps(payload).lower()
    assert "hidden chain of thought" not in forbidden_text
    assert "guaranteed safety" not in forbidden_text
    assert "regulatory certification" not in forbidden_text


def main() -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate(payload)
    print(f"validated {payload['case_id']} ({payload['status']})")


if __name__ == "__main__":
    main()
