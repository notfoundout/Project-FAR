from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from execution_outcome import ExecutionOutcome, classify_execution

_ALLOWED_INVOCATION_SCHEMAS = {
    "far-swe-agent-invocation/1.1",
    "far-swe-agent-invocation/1.2",
    "far-swe-agent-invocation/1.3",
}
_ALLOWED_RECORD_SCHEMAS = {
    "far-swe-agent-run-record/1.0",
    "far-swe-agent-run-record/1.1",
    "far-swe-agent-run-record/1.2",
}


def _terminal(run: dict[str, Any], reason: str, evidence: dict[str, Any]):
    return {}, ExecutionOutcome(
        "terminal_agent_error",
        "failed_terminal",
        False,
        None,
        False,
        False,
        reason,
        {"run_id": run["run_id"], **evidence},
    )


def _read_mapping(base: Any, path: Path, label: str, run: dict[str, Any]):
    try:
        return base.read_json(path), None
    except (SystemExit, OSError, json.JSONDecodeError) as exc:
        return None, _terminal(
            run,
            f"preserved {label} cannot be read",
            {"path": str(path), "error": str(exc)},
        )


def _classify_preserved_run(
    legacy: Any,
    run: dict[str, Any],
    task_id: str,
    *,
    plan_sha256: str | None = None,
    image: str | None = None,
):
    base = legacy.base
    run_dir = base.RUNS_DIR / run["run_id"]
    record_path = run_dir / "run-record.json"
    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"
    swe_output = run_dir / "sweagent-output"
    missing_core = [
        name
        for name, path in {
            "run_record": record_path,
            "stdout": stdout_path,
            "stderr": stderr_path,
        }.items()
        if not path.is_file()
    ]
    if not swe_output.is_dir():
        missing_core.append("sweagent_output")
    if missing_core:
        return _terminal(
            run,
            "preserved completed run is missing core execution evidence",
            {"missing": sorted(missing_core)},
        )

    record, error = _read_mapping(base, record_path, "run record", run)
    if error is not None:
        return error
    returncode = record.get("returncode")
    if not isinstance(returncode, int):
        return _terminal(
            run,
            "preserved run record has no integer return code",
            {"returncode": returncode, "record_path": str(record_path)},
        )
    stdout = stdout_path.read_text(encoding="utf-8", errors="replace")
    stderr = stderr_path.read_text(encoding="utf-8", errors="replace")
    outcome = classify_execution(
        outer_returncode=returncode,
        swe_output=swe_output,
        task_id=task_id,
        stdout=stdout,
        stderr=stderr,
        allow_no_change=False,
    )
    # A disproved completion is corrected from the primary execution evidence.
    # Completion-only provenance is required only when the execution itself
    # validates as complete; otherwise missing trajectory/invocation artifacts
    # must not turn a retryable provider failure into a terminal failure.
    if outcome.state != "complete":
        return record, outcome

    invocation_path = run_dir / "invocation.json"
    instance_path = run_dir / "instance.json"
    expected_trajectory = f"trajectories/{run['trajectory_artifact']}"
    trajectory_path = base.OUTPUT_DIR / expected_trajectory
    missing_completion = []
    if not invocation_path.is_file():
        missing_completion.append("invocation")
    if not instance_path.is_file():
        missing_completion.append("instance")
    if run.get("record") != str(record_path.relative_to(base.OUTPUT_DIR)):
        missing_completion.append("canonical_record_binding")
    if run.get("trajectory") != expected_trajectory:
        missing_completion.append("canonical_trajectory_binding")
    if not trajectory_path.is_file():
        missing_completion.append("trajectory")
    if missing_completion:
        return _terminal(
            run,
            "successful preserved run is missing completion provenance",
            {"missing": sorted(missing_completion)},
        )

    invocation, error = _read_mapping(base, invocation_path, "invocation", run)
    if error is not None:
        return error
    if plan_sha256 is None or image is None:
        try:
            manifest, lock, _task = base.frozen_inputs()
            plan_sha256 = base.validate_plan(manifest, lock)
            image = lock["immutable_image_reference"]
        except (SystemExit, KeyError, TypeError, AttributeError) as exc:
            return _terminal(
                run,
                "current frozen provenance cannot be resolved",
                {"error": str(exc)},
            )
    invalid: list[str] = []
    if invocation.get("schema") not in _ALLOWED_INVOCATION_SCHEMAS:
        invalid.append("invocation_schema")
    if record.get("schema") not in _ALLOWED_RECORD_SCHEMAS:
        invalid.append("run_record_schema")
    common = {
        "run_id": run["run_id"],
        "release": run["release"],
        "commit": run["full_commit"],
        "task_id": task_id,
    }
    for key, expected in common.items():
        if invocation.get(key) != expected:
            invalid.append(f"invocation_{key}")
        if record.get(key) != expected:
            invalid.append(f"run_record_{key}")
    if record.get("repetition") != run["repetition"]:
        invalid.append("run_record_repetition")
    if record.get("state") != "complete":
        invalid.append("run_record_state")
    if invocation.get("benchmark_outcomes_accessible") is not False:
        invalid.append("invocation_outcome_boundary")
    if record.get("benchmark_outcomes_accessed") is not False:
        invalid.append("run_record_outcome_boundary")
    config_hash = base.sha256_file(base.CONFIG_PATH)
    if invocation.get("agent_config_sha256") != config_hash:
        invalid.append("invocation_agent_config")
    for source, label in ((invocation, "invocation"), (record, "run_record")):
        if source.get("execution_plan_sha256") != plan_sha256:
            invalid.append(f"{label}_execution_plan")
        if source.get("image") != image:
            invalid.append(f"{label}_image")
    if record.get("trajectory") != expected_trajectory:
        invalid.append("run_record_trajectory")
    trajectory_hash = base.sha256_file(trajectory_path)
    if run.get("trajectory_sha256") != trajectory_hash:
        invalid.append("state_trajectory_sha256")
    if record.get("trajectory_sha256") != trajectory_hash:
        invalid.append("run_record_trajectory_sha256")
    if record.get("artifact_sha256") != legacy._current_artifact_hashes(run_dir):
        invalid.append("current_artifact_sha256")
    if invalid:
        return _terminal(
            run,
            "preserved completed run failed provenance validation",
            {
                "invalid": sorted(invalid),
                "record_path": str(record_path),
                "invocation_path": str(invocation_path),
            },
        )
    return record, outcome


def install(legacy: Any) -> Any:
    def classify(
        run: dict[str, Any],
        task_id: str,
        *,
        plan_sha256: str | None = None,
        image: str | None = None,
    ):
        return _classify_preserved_run(
            legacy, run, task_id, plan_sha256=plan_sha256, image=image
        )

    legacy._classify_preserved_run = classify
    return legacy
