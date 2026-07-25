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


def _record_path(run: dict[str, Any]) -> Path:
    return base.RUNS_DIR / run["run_id"] / "run-record.json"


def _persist_outcome(
    state: dict[str, Any],
    run: dict[str, Any],
    record: dict[str, Any],
    outcome: ExecutionOutcome,
) -> None:
    run_dir = base.RUNS_DIR / run["run_id"]
    record["state"] = outcome.state
    record["outcome"] = outcome.to_dict()
    record["artifact_sha256"] = base.collect_hashes(run_dir)
    base.write_json(run_dir / "run-record.json", record)
    run.update({
        "state": outcome.state,
        "record": str((run_dir / "run-record.json").relative_to(base.OUTPUT_DIR)),
        "outcome_category": outcome.category,
    })
    if outcome.state == "complete":
        run["completed_at"] = record["completed_at"]
    base.save_state(state)


def execute_one(agent_repo: Path) -> int:
    manifest, lock, task = base.frozen_inputs()
    plan_sha256 = base.validate_plan(manifest, lock)
    base.verify_local_image(lock)
    state = base.load_state(manifest, lock, plan_sha256)
    run = base.next_pending(state)
    if run is None:
        print("All four frozen runs are complete.")
        return 0

    secret = os.environ.get("GEMINI_API_KEY", "")
    if not secret:
        raise SystemExit("GEMINI_API_KEY is required; no model call was started")
    base.verify_agent_checkout(agent_repo, run["full_commit"])

    run_dir = base.RUNS_DIR / run["run_id"]
    swe_output = run_dir / "sweagent-output"
    run_dir.mkdir(parents=True, exist_ok=True)
    base.TRAJECTORY_DIR.mkdir(parents=True, exist_ok=True)
    instance_path = run_dir / "instance.json"
    base.build_instance_file(task, lock, instance_path)
    executable = shutil.which("sweagent")
    if executable is None:
        raise SystemExit("Installed SWE-agent console entry point is missing")
    command = base.build_cli_command(executable, agent_repo, instance_path, swe_output)
    parsed_config = base.verify_cli_contract(command, agent_repo, instance_path, swe_output)

    invocation = {
        "schema": "far-swe-agent-invocation/1.2",
        "run_id": run["run_id"],
        "release": run["release"],
        "commit": run["full_commit"],
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
    run["attempts"] += 1
    run["state"] = "running"
    run["started_at"] = invocation["started_at"]
    base.save_state(state)

    run_env = os.environ.copy()
    for name in ("GITHUB_TOKEN", "GH_TOKEN"):
        run_env.pop(name, None)
    started = time.monotonic()
    result = subprocess.run(command, cwd=agent_repo, text=True, capture_output=True, env=run_env)
    duration = time.monotonic() - started
    stdout = base.redact(result.stdout, secret)
    stderr = base.redact(result.stderr, secret)
    (run_dir / "stdout.log").write_text(stdout, encoding="utf-8", errors="replace")
    (run_dir / "stderr.log").write_text(stderr, encoding="utf-8", errors="replace")

    record: dict[str, Any] = {
        "schema": "far-swe-agent-run-record/1.1",
        "run_id": run["run_id"],
        "release": run["release"],
        "commit": run["full_commit"],
        "repetition": run["repetition"],
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
            print("Provider quota exhaustion recorded as failed_retryable; the same frozen run remains next.")
            return 75
        print(f"Run rejected by internal-result validation: {outcome.category}: {outcome.reason}")
        return 75 if outcome.retryable else 1

    source = base.locate_trajectory(swe_output, task["instance_id"])
    target = base.TRAJECTORY_DIR / run["trajectory_artifact"]
    shutil.copy2(source, target)
    record.update({
        "trajectory": str(target.relative_to(base.OUTPUT_DIR)),
        "trajectory_sha256": base.sha256_file(target),
    })
    _persist_outcome(state, run, record, outcome)
    run["trajectory_sha256"] = record["trajectory_sha256"]
    base.save_state(state)
    print(f"Completed frozen run {run['run_id']} only after internal success and prediction validation.")
    return 0


def repair_run(run_id: str) -> dict[str, Any]:
    manifest, lock, task = base.frozen_inputs()
    plan_sha256 = base.validate_plan(manifest, lock)
    state = base.load_state(manifest, lock, plan_sha256)
    matches = [item for item in state["runs"] if item["run_id"] == run_id]
    if len(matches) != 1:
        raise SystemExit(f"Unknown run_id: {run_id}")
    run = matches[0]
    run_dir = base.RUNS_DIR / run_id
    record_path = run_dir / "run-record.json"
    record = base.read_json(record_path)
    stdout = (run_dir / "stdout.log").read_text(encoding="utf-8", errors="replace")
    stderr = (run_dir / "stderr.log").read_text(encoding="utf-8", errors="replace")
    swe_output = run_dir / "sweagent-output"
    outcome = classify_execution(
        outer_returncode=int(record.get("returncode", 1)),
        swe_output=swe_output,
        task_id=task["instance_id"],
        stdout=stdout,
        stderr=stderr,
        allow_no_change=False,
    )
    if outcome.state == "complete":
        raise SystemExit("Repair refused: preserved evidence validates the existing completion")

    before_state = run.get("state")
    before_record_sha256 = base.sha256_file(record_path)
    audit = state.setdefault("corrections", [])
    audit.append({
        "schema": "far-swe-agent-state-correction/1.0",
        "corrected_at": base.utc_now(),
        "run_id": run_id,
        "attempts_preserved": run.get("attempts"),
        "before_state": before_state,
        "after_state": outcome.state,
        "before_run_record_sha256": before_record_sha256,
        "raw_artifact_sha256": base.collect_hashes(run_dir),
        "outcome": outcome.to_dict(),
    })
    run["state"] = outcome.state
    run["outcome_category"] = outcome.category
    run["corrected_from"] = before_state
    run.pop("completed_at", None)
    base.save_state(state)
    return audit[-1]


def status() -> dict[str, Any]:
    return base.status()


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
