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
    "execution_requirements", "required_artifacts", "primary_questions", "decision_policy",
    "forbidden_before_primary_freeze", "claim_boundary",
}
REQUIRED_DECISIONS = {"PASS", "BLOCKED", "REVIEW_REQUIRED", "UNKNOWN"}
REQUIRED_BLINDED_FIELDS = {
    "benchmark_resolution_status", "test_pass_fail", "reward", "grader_output",
    "human_success_label", "candidate_preference",
}
DECLARATION_PATH = ("forbidden_before_primary_freeze",)


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


def validate(payload: dict) -> None:
    missing = REQUIRED_TOP_LEVEL - payload.keys()
    assert not missing, f"missing top-level fields: {sorted(missing)}"

    source = payload["source"]
    assert source["repository"] == "https://github.com/SWE-agent/SWE-agent"
    assert source["baseline_ref"] == "v1.0.0"
    assert source["baseline_commit"] == "8ed382c"
    assert source["candidate_ref"] == "v1.0.1"
    assert source["candidate_commit"] == "6aff215"

    design = payload["comparison_design"]
    for field in (
        "same_task", "same_model", "same_model_parameters", "same_agent_configuration",
        "same_environment_image", "same_task_seed", "isolated_workspaces",
        "outcome_blinded_until_primary_freeze",
    ):
        assert design[field] is True, f"{field} must remain true"
    assert design["minimum_repetitions_per_release"] >= 2

    assert set(payload["decision_policy"]) == REQUIRED_DECISIONS
    assert set(payload["forbidden_before_primary_freeze"]) == REQUIRED_BLINDED_FIELDS
    leaked_paths = _forbidden_paths(payload)
    assert not leaked_paths, f"pre-freeze outcome leakage: {sorted(leaked_paths)}"

    frozen = payload["frozen_inputs"]
    assert frozen["task_id"] == "scikit-learn__scikit-learn-14125"
    assert frozen["model"] == "anthropic/claude-opus-4-5"
    assert frozen["model_parameters"]["temperature"] == 0.0
    assert frozen["model_parameters"]["reasoning_effort"] == "high"
    assert frozen["task_seed"] == 14125
    actual_config_hash = hashlib.sha256(CONFIG.read_bytes()).hexdigest()
    assert actual_config_hash == frozen["agent_config_sha256"], "agent config hash mismatch"

    status = payload["status"]
    if status == "execution_inputs_frozen":
        assert frozen["environment_image_digest"], "frozen execution requires image digest"
    else:
        assert status == "execution_inputs_selected_environment_digest_pending"
        assert frozen["environment_image_digest"] is None

    runs = payload["execution_requirements"]["runs"]
    assert len(runs) == 4
    assert {(run["release"], run["repetition"]) for run in runs} == {
        ("v1.0.0", 1), ("v1.0.0", 2), ("v1.0.1", 1), ("v1.0.1", 2)
    }

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
