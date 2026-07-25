from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

import execute_controller as base
from execution_outcome import ExecutionOutcome, classify_execution

FAILED_TERMINAL = "failed_terminal"
base.ALLOWED_STATES.add(FAILED_TERMINAL)

_ATTEMPT_ARTIFACT_NAMES = (
    "instance.json",
    "invocation.json",
    "stdout.log",
    "stderr.log",
    "run-record.json",
    "run-record-correction.json",
    "sweagent-output",
)
_CURRENT_HASH_EXCLUSIONS = {"run-record.json", "run-record-correction.json"}


def _record_path(run: dict[str, Any]) -> Path:
    return base.RUNS_DIR / run["run_id"] / "run-record.json"


def _current_artifact_hashes(run_dir: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(item for item in run_dir.rglob("*") if item.is_file()):
        relative = path.relative_to(run_dir)
        if relative.parts[0] == "attempts" or relative.name in _CURRENT_HASH_EXCLUSIONS:
            continue
        if path.is_symlink():
            raise SystemExit(f"Current attempt contains a symlink: {relative}")
        hashes[str(relative)] = base.sha256_file(path)
    return hashes


def _clear_completion_metadata(run: dict[str, Any]) -> None:
    run.pop("completed_at", None)
    run.pop("trajectory_sha256", None)


def _persist_outcome(
    state: dict[str, Any],
    run: dict[str, Any],
    record: dict[str, Any],
    outcome: ExecutionOutcome,
) -> None:
    run_dir = base.RUNS_DIR / run["run_id"]
    record["state"] = outcome.state
    record["outcome"] = outcome.to_dict()
    record["artifact_sha256"] = _current_artifact_hashes(run_dir)
    base.write_json(run_dir / "run-record.json", record)
    run.update(
        {
            "state": outcome.state,
            "record": str(
                (run_dir / "run-record.json").relative_to(base.OUTPUT_DIR)
            ),
            "outcome_category": outcome.category,
        }
    )
    run.pop("correction", None)
    run.pop("corrected_from", None)
    if outcome.state == "complete":
        run["completed_at"] = record["completed_at"]
    else:
        _clear_completion_metadata(run)
    base.save_state(state)


def _incomplete_preserved_evidence(
    run: dict[str, Any], reason: str, evidence: dict[str, Any]
) -> tuple[dict[str, Any], ExecutionOutcome]:
    return {}, ExecutionOutcome(
        "terminal_agent_error",
        FAILED_TERMINAL,
        False,
        None,
        False,
        False,
        reason,
        {"run_id": run["run_id"], **evidence},
    )


def _classify_preserved_run(
    run: dict[str, Any], task_id: str
) -> tuple[dict[str, Any], ExecutionOutcome]:
    run_dir = base.RUNS_DIR / run["run_id"]
    record_path = run_dir / "run-record.json"
    required = {
        "run_record": record_path,
        "stdout": run_dir / "stdout.log",
        "stderr": run_dir / "stderr.log",
    }
    missing = [name for name, path in required.items() if not path.is_file()]
    swe_output = run_dir / "sweagent-output"
    if not swe_output.is_dir():
        missing.append("sweagent_output")
    if missing:
        return _incomplete_preserved_evidence(
            run,
            "preserved completed run is missing required execution evidence",
            {"missing": sorted(missing)},
        )

    try:
        record = base.read_json(record_path)
    except (SystemExit, OSError, json.JSONDecodeError) as exc:
        return _incomplete_preserved_evidence(
            run,
            "preserved run record cannot be read",
            {"error": str(exc), "record_path": str(record_path)},
        )
    returncode = record.get("returncode")
    if not isinstance(returncode, int):
        return _incomplete_preserved_evidence(
            run,
            "preserved run record has no integer return code",
            {"record_path": str(record_path), "returncode": returncode},
        )

    stdout = required["stdout"].read_text(encoding="utf-8", errors="replace")
    stderr = required["stderr"].read_text(encoding="utf-8", errors="replace")
    outcome = classify_execution(
        outer_returncode=returncode,
        swe_output=swe_output,
        task_id=task_id,
        stdout=stdout,
        stderr=stderr,
        allow_no_change=False,
    )
    return record, outcome


def _sequence_violation_outcome(run: dict[str, Any]) -> ExecutionOutcome:
    return ExecutionOutcome(
        "protocol_sequence_violation",
        FAILED_TERMINAL,
        False,
        None,
        False,
        False,
        "run was completed after an earlier frozen slot became invalid",
        {"run_id": run["run_id"], "slot": run["slot"]},
    )


def _apply_state_correction(
    state: dict[str, Any],
    run: dict[str, Any],
    outcome: ExecutionOutcome,
    record: dict[str, Any],
) -> dict[str, Any]:
    run_dir = base.RUNS_DIR / run["run_id"]
    record_path = run_dir / "run-record.json"
    correction_path = run_dir / "run-record-correction.json"
    before_state = run.get("state")
    correction = {
        "schema": "far-swe-agent-state-correction/1.1",
        "corrected_at": base.utc_now(),
        "run_id": run["run_id"],
        "attempts_preserved": run.get("attempts"),
        "before_state": before_state,
        "after_state": outcome.state,
        "before_run_record_sha256": (
            base.sha256_file(record_path) if record_path.is_file() else None
        ),
        "raw_artifact_sha256": base.collect_hashes(run_dir),
        "previous_record_state": record.get("state") if record else None,
        "outcome": outcome.to_dict(),
    }
    base.write_json(correction_path, correction)
    state.setdefault("corrections", []).append(correction)
    run["state"] = outcome.state
    run["outcome_category"] = outcome.category
    run["corrected_from"] = before_state
    run["correction"] = str(correction_path.relative_to(base.OUTPUT_DIR))
    _clear_completion_metadata(run)
    return correction


def reconcile_completed_runs(state: dict[str, Any], task_id: str) -> bool:
    changed = False
    earlier_invalid = False
    for run in state["runs"]:
        if run["state"] != "complete":
            earlier_invalid = True
            continue
        if earlier_invalid:
            record = base.read_json(_record_path(run)) if _record_path(run).is_file() else {}
            outcome = _sequence_violation_outcome(run)
        else:
            record, outcome = _classify_preserved_run(run, task_id)
        if outcome.state == "complete":
            continue
        _apply_state_correction(state, run, outcome, record)
        changed = True
        earlier_invalid = True
    if changed:
        base.save_state(state)
    return changed


def _terminal_runs(state: dict[str, Any]) -> list[dict[str, Any]]:
    return [run for run in state["runs"] if run["state"] == FAILED_TERMINAL]


def _ensure_progressable(state: dict[str, Any]) -> None:
    terminal = _terminal_runs(state)
    if terminal:
        details = ", ".join(
            f"{run['run_id']} ({run.get('outcome_category', 'unknown')})"
            for run in terminal
        )
        raise SystemExit(
            "Frozen execution matrix is blocked by terminal failure: " + details
        )


def _load_validated_state() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], str, dict[str, Any]
]:
    manifest, lock, task = base.frozen_inputs()
    plan_sha256 = base.validate_plan(manifest, lock)
    state = base.load_state(manifest, lock, plan_sha256)
    reconcile_completed_runs(state, task["instance_id"])
    _ensure_progressable(state)
    return manifest, lock, task, plan_sha256, state


def _next_archive_dir(run_dir: Path, previous_attempt: int) -> Path:
    root = run_dir / "attempts"
    base_name = f"attempt-{previous_attempt:03d}"
    candidate = root / base_name
    if not candidate.exists():
        return candidate
    index = 1
    while True:
        candidate = root / f"{base_name}-recovery-{index:02d}"
        if not candidate.exists():
            return candidate
        index += 1


def _archive_previous_attempt(
    run: dict[str, Any], run_dir: Path
) -> str | None:
    existing = [run_dir / name for name in _ATTEMPT_ARTIFACT_NAMES if (run_dir / name).exists()]
    trajectory = base.TRAJECTORY_DIR / run["trajectory_artifact"]
    if trajectory.exists():
        existing.append(trajectory)
    if not existing:
        return None

    previous_attempt = int(run.get("attempts", 0))
    if previous_attempt < 1:
        raise SystemExit(
            f"Run {run['run_id']} has execution artifacts but no recorded attempt"
        )
    archive_dir = _next_archive_dir(run_dir, previous_attempt)
    unsafe = [path for path in existing if path.is_symlink()]
    if unsafe:
        raise SystemExit(
            "Refusing to archive symlinked attempt evidence: "
            + ", ".join(str(path) for path in unsafe)
        )
    archive_dir.mkdir(parents=True, exist_ok=False)
    moved: list[tuple[Path, Path]] = []
    try:
        for path in existing:
            if path == trajectory:
                destination = archive_dir / "trajectory" / path.name
            else:
                destination = archive_dir / path.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(destination))
            moved.append((path, destination))
    except BaseException:
        for source, destination in reversed(moved):
            source.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(destination), str(source))
        shutil.rmtree(archive_dir, ignore_errors=True)
        attempts_root = run_dir / "attempts"
        if attempts_root.is_dir() and not any(attempts_root.iterdir()):
            attempts_root.rmdir()
        raise
    return str(archive_dir.relative_to(base.OUTPUT_DIR))


def execute_one(agent_repo: Path) -> int:
    manifest, lock, task = base.frozen_inputs()
    plan_sha256 = base.validate_plan(manifest, lock)
    base.verify_local_image(lock)
    state = base.load_state(manifest, lock, plan_sha256)
    reconcile_completed_runs(state, task["instance_id"])
    _ensure_progressable(state)
    run = base.next_pending(state)
    if run is None:
        print("All four frozen runs are complete.")
        return 0

    secret = os.environ.get("GEMINI_API_KEY", "")
    if not secret:
        raise SystemExit("GEMINI_API_KEY is required; no model call was started")
    base.verify_agent_checkout(agent_repo, run["full_commit"])

    run_dir = base.RUNS_DIR / run["run_id"]
    run_dir.mkdir(parents=True, exist_ok=True)
    archived = _archive_previous_attempt(run, run_dir)
    swe_output = run_dir / "sweagent-output"
    base.TRAJECTORY_DIR.mkdir(parents=True, exist_ok=True)
    instance_path = run_dir / "instance.json"
    base.build_instance_file(task, lock, instance_path)
    executable = shutil.which("sweagent")
    if executable is None:
        raise SystemExit("Installed SWE-agent console entry point is missing")
    command = base.build_cli_command(executable, agent_repo, instance_path, swe_output)
    parsed_config = base.verify_cli_contract(
        command, agent_repo, instance_path, swe_output
    )

    attempt = int(run.get("attempts", 0)) + 1
    invocation = {
        "schema": "far-swe-agent-invocation/1.3",
        "run_id": run["run_id"],
        "release": run["release"],
        "commit": run["full_commit"],
        "attempt": attempt,
        "task_id": task["instance_id"],
        "image": lock["immutable_image_reference"],
        "agent_config_sha256": base.sha256_file(base.CONFIG_PATH),
        "execution_plan_sha256": plan_sha256,
        "command": command,
        "parsed_contract": parsed_config,
        "environment_variables_present": {"GEMINI_API_KEY": True},
        "benchmark_outcomes_accessible": False,
        "started_at": base.utc_now(),
    }
    base.write_json(run_dir / "invocation.json", invocation)
    run["attempts"] = attempt
    run["state"] = "running"
    run["started_at"] = invocation["started_at"]
    run["record"] = None
    run.pop("outcome_category", None)
    run.pop("correction", None)
    run.pop("corrected_from", None)
    _clear_completion_metadata(run)
    if archived is not None:
        run["previous_attempt_archive"] = archived
    base.save_state(state)

    run_env = os.environ.copy()
    for name in ("GITHUB_TOKEN", "GH_TOKEN"):
        run_env.pop(name, None)
    started = time.monotonic()
    result = subprocess.run(
        command,
        cwd=agent_repo,
        text=True,
        capture_output=True,
        env=run_env,
    )
    duration = time.monotonic() - started
    stdout = base.redact(result.stdout, secret)
    stderr = base.redact(result.stderr, secret)
    (run_dir / "stdout.log").write_text(
        stdout, encoding="utf-8", errors="replace"
    )
    (run_dir / "stderr.log").write_text(
        stderr, encoding="utf-8", errors="replace"
    )

    record: dict[str, Any] = {
        "schema": "far-swe-agent-run-record/1.2",
        "run_id": run["run_id"],
        "release": run["release"],
        "commit": run["full_commit"],
        "repetition": run["repetition"],
        "attempt": attempt,
        "task_id": task["instance_id"],
        "image": lock["immutable_image_reference"],
        "execution_plan_sha256": plan_sha256,
        "returncode": result.returncode,
        "duration_seconds": round(duration, 3),
        "completed_at": base.utc_now(),
        "benchmark_outcomes_accessed": False,
    }
    outcome = classify_execution(
        outer_returncode=result.returncode,
        swe_output=swe_output,
        task_id=task["instance_id"],
        stdout=stdout,
        stderr=stderr,
        allow_no_change=False,
    )

    if outcome.state != "complete":
        _persist_outcome(state, run, record, outcome)
        if outcome.category == "provider_quota_exhaustion":
            print(
                "Provider quota exhaustion recorded as failed_retryable; "
                "the same frozen run remains next."
            )
            return 75
        print(
            "Run rejected by internal-result validation: "
            f"{outcome.category}: {outcome.reason}"
        )
        return 75 if outcome.retryable else 1

    source = base.locate_trajectory(swe_output, task["instance_id"])
    target = base.TRAJECTORY_DIR / run["trajectory_artifact"]
    shutil.copy2(source, target)
    record.update(
        {
            "trajectory": str(target.relative_to(base.OUTPUT_DIR)),
            "trajectory_sha256": base.sha256_file(target),
        }
    )
    _persist_outcome(state, run, record, outcome)
    run["trajectory_sha256"] = record["trajectory_sha256"]
    base.save_state(state)
    print(
        f"Completed frozen run {run['run_id']} only after internal success "
        "and prediction validation."
    )
    return 0


def repair_run(run_id: str) -> dict[str, Any]:
    manifest, lock, task = base.frozen_inputs()
    plan_sha256 = base.validate_plan(manifest, lock)
    state = base.load_state(manifest, lock, plan_sha256)
    matches = [item for item in state["runs"] if item["run_id"] == run_id]
    if len(matches) != 1:
        raise SystemExit(f"Unknown run_id: {run_id}")
    run = matches[0]
    if run["state"] != "complete":
        raise SystemExit(
            f"Repair refused: run is not marked complete ({run['state']})"
        )
    record, outcome = _classify_preserved_run(run, task["instance_id"])
    if outcome.state == "complete":
        raise SystemExit(
            "Repair refused: preserved evidence validates the existing completion"
        )
    correction = _apply_state_correction(state, run, outcome, record)
    base.save_state(state)
    return correction


def status() -> dict[str, Any]:
    _, _, _, _, state = _load_validated_state()
    return state


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("--agent-repo", type=Path)
    execute_parser = sub.add_parser("execute-next")
    execute_parser.add_argument("--agent-repo", type=Path, required=True)
    repair_parser = sub.add_parser("repair-run")
    repair_parser.add_argument("--run-id", required=True)
    sub.add_parser("status")
    args = parser.parse_args()
    if args.command == "validate":
        base.validate_only(args.agent_repo)
    elif args.command == "status":
        print(json.dumps(status(), indent=2, sort_keys=True))
    elif args.command == "repair-run":
        print(json.dumps(repair_run(args.run_id), indent=2, sort_keys=True))
    else:
        raise SystemExit(execute_one(args.agent_repo.resolve()))


if __name__ == "__main__":
    main()
