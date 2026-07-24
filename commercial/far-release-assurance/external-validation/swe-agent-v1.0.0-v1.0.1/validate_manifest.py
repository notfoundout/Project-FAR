from __future__ import annotations

import json
from pathlib import Path

MANIFEST = Path(__file__).with_name("manifest.json")

REQUIRED_TOP_LEVEL = {
    "schema",
    "case_id",
    "status",
    "source",
    "comparison_design",
    "frozen_inputs",
    "required_artifacts",
    "primary_questions",
    "decision_policy",
    "forbidden_before_primary_freeze",
    "claim_boundary",
}

REQUIRED_DECISIONS = {"PASS", "BLOCKED", "REVIEW_REQUIRED", "UNKNOWN"}
REQUIRED_BLINDED_FIELDS = {
    "benchmark_resolution_status",
    "test_pass_fail",
    "reward",
    "grader_output",
    "human_success_label",
    "candidate_preference",
}


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
        "same_task",
        "same_model",
        "same_model_parameters",
        "same_agent_configuration",
        "same_environment_image",
        "same_task_seed",
        "isolated_workspaces",
        "outcome_blinded_until_primary_freeze",
    ):
        assert design[field] is True, f"{field} must remain true"
    assert design["minimum_repetitions_per_release"] >= 2

    assert set(payload["decision_policy"]) == REQUIRED_DECISIONS
    assert set(payload["forbidden_before_primary_freeze"]) == REQUIRED_BLINDED_FIELDS

    frozen_inputs = payload["frozen_inputs"]
    if payload["status"] == "execution_inputs_frozen":
        unresolved = [key for key, value in frozen_inputs.items() if value is None]
        assert not unresolved, f"execution freeze contains null fields: {unresolved}"
    else:
        assert payload["status"] == "protocol_frozen_execution_inputs_pending"

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
