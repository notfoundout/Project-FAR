from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import execute_controller as base
from execution_outcome import ExecutionOutcome, classify_execution


ACTIVE_STATES = {"pending", "running", "quota_paused", "failed_retryable"}


@dataclass(frozen=True)
class ReconciliationResult:
    changed: bool
    run_id: str | None
    before_state: str | None
    after_state: str | None
    outcome: ExecutionOutcome | None


def _classify_preserved_run(run: dict[str, Any], task_id: str) -> ExecutionOutcome:
    run_dir = base.RUNS_DIR / run["run_id"]
    record_path = run_dir / "run-record.json"
    if not record_path.is_file():
        raise SystemExit(f"restored state references missing run record: {record_path}")
    record = base.read_json(record_path)
    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"
    if not stdout_path.is_file() or not stderr_path.is_file():
        raise SystemExit(f"restored state is missing preserved logs for {run['run_id']}")
    return classify_execution(
        outer_returncode=int(record.get("returncode", 1)),
        swe_output=run_dir / "sweagent-output",
        task_id=task_id,
        stdout=stdout_path.read_text(encoding="utf-8", errors="replace"),
        stderr=stderr_path.read_text(encoding="utf-8", errors="replace"),
        allow_no_change=False,
    )


def validate_run_order(state: dict[str, Any]) -> None:
    runs = state.get("runs")
    if not isinstance(runs, list) or not runs:
        raise SystemExit("execution state has no frozen runs")

    active_indexes = [index for index, run in enumerate(runs) if run.get("state") in ACTIVE_STATES]
    if len(active_indexes) > 1:
        raise SystemExit(f"execution state has multiple active runs: {active_indexes}")

    first_non_complete = next((index for index, run in enumerate(runs) if run.get("state") != "complete"), len(runs))
    for index in range(first_non_complete + 1, len(runs)):
        if runs[index].get("state") == "complete":
            raise SystemExit("execution state advances past an incomplete earlier frozen run")

    for run in runs:
        attempts = run.get("attempts")
        if not isinstance(attempts, int) or attempts < 0:
            raise SystemExit(f"invalid attempt count for {run.get('run_id')}: {attempts}")
        if run.get("state") not in base.ALLOWED_STATES | {"failed_terminal"}:
            raise SystemExit(f"unknown run state for {run.get('run_id')}: {run.get('state')}")


def reconcile_restored_state() -> ReconciliationResult:
    manifest, lock, task = base.frozen_inputs()
    plan_sha256 = base.validate_plan(manifest, lock)
    state = base.load_state(manifest, lock, plan_sha256)
    validate_run_order(state)

    for run in state["runs"]:
        if run.get("state") != "complete":
            break
        outcome = _classify_preserved_run(run, task["instance_id"])
        if outcome.state == "complete":
            continue

        before_state = run["state"]
        audit = state.setdefault("corrections", [])
        record_path = base.RUNS_DIR / run["run_id"] / "run-record.json"
        audit.append({
            "schema": "far-swe-agent-state-correction/1.1",
            "corrected_at": base.utc_now(),
            "reason": "restored-completion-failed-internal-validation",
            "run_id": run["run_id"],
            "attempts_preserved": run.get("attempts"),
            "before_state": before_state,
            "after_state": outcome.state,
            "before_run_record_sha256": base.sha256_file(record_path),
            "raw_artifact_sha256": base.collect_hashes(base.RUNS_DIR / run["run_id"]),
            "outcome": outcome.to_dict(),
        })
        run["state"] = outcome.state
        run["outcome_category"] = outcome.category
        run["corrected_from"] = before_state
        run.pop("completed_at", None)
        base.save_state(state)
        validate_run_order(state)
        return ReconciliationResult(True, run["run_id"], before_state, outcome.state, outcome)

    return ReconciliationResult(False, None, None, None, None)
