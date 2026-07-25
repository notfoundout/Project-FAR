from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_record(base: Any, path: Path) -> dict[str, Any] | None:
    try:
        value = base.read_json(path)
    except (SystemExit, OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _recover_complete(
    core: Any,
    state: dict[str, Any],
    run: dict[str, Any],
    record: dict[str, Any],
    outcome: Any,
) -> None:
    base = core.base
    completed_at = record.get("completed_at")
    trajectory_sha256 = record.get("trajectory_sha256")
    if not isinstance(completed_at, str) or not completed_at:
        raise SystemExit(
            f"Validated completed record lacks completed_at: {run['run_id']}"
        )
    if not isinstance(trajectory_sha256, str) or not trajectory_sha256:
        raise SystemExit(
            f"Validated completed record lacks trajectory_sha256: {run['run_id']}"
        )
    recovery_dir = base.OUTPUT_DIR / "recoveries"
    recovery_path = recovery_dir / f"{run['run_id']}-running-to-complete.json"
    recovery = {
        "schema": "far-swe-agent-state-recovery/1.0",
        "recovered_at": base.utc_now(),
        "run_id": run["run_id"],
        "attempts_preserved": run.get("attempts"),
        "before_state": "running",
        "after_state": "complete",
        "run_record_sha256": base.sha256_file(core._record_path(run)),
        "outcome": outcome.to_dict(),
    }
    base.write_json(recovery_path, recovery)
    state.setdefault("recoveries", []).append(recovery)
    run.update(
        {
            "state": "complete",
            "record": str(core._record_path(run).relative_to(base.OUTPUT_DIR)),
            "completed_at": completed_at,
            "trajectory_sha256": trajectory_sha256,
            "outcome_category": outcome.category,
            "recovery": str(recovery_path.relative_to(base.OUTPUT_DIR)),
        }
    )
    run.pop("correction", None)
    run.pop("corrected_from", None)


def install(core: Any) -> Any:
    original_reconcile = core.reconcile_completed_runs
    original_apply_correction = core._apply_state_correction
    original_persist_outcome = getattr(core, "_persist_outcome", None)

    def apply_state_correction(state, run, outcome, record):
        run.pop("recovery", None)
        return original_apply_correction(state, run, outcome, record)

    core._apply_state_correction = apply_state_correction

    if original_persist_outcome is not None:
        def persist_outcome(state, run, record, outcome):
            base = core.base
            run_dir = base.RUNS_DIR / run["run_id"]
            if outcome.state == "complete":
                completed_at = record.get("completed_at")
                trajectory_sha256 = record.get("trajectory_sha256")
                if not isinstance(completed_at, str) or not completed_at:
                    raise SystemExit(
                        f"Completed outcome lacks completed_at: {run['run_id']}"
                    )
                if not isinstance(trajectory_sha256, str) or not trajectory_sha256:
                    raise SystemExit(
                        f"Completed outcome lacks trajectory_sha256: {run['run_id']}"
                    )

            record["state"] = outcome.state
            record["outcome"] = outcome.to_dict()
            record["artifact_sha256"] = core._current_artifact_hashes(run_dir)
            record_path = run_dir / "run-record.json"
            base.write_json(record_path, record)
            run.update(
                {
                    "state": outcome.state,
                    "record": str(record_path.relative_to(base.OUTPUT_DIR)),
                    "outcome_category": outcome.category,
                }
            )
            run.pop("recovery", None)
            run.pop("correction", None)
            run.pop("corrected_from", None)
            if outcome.state == "complete":
                run["completed_at"] = record["completed_at"]
                run["trajectory_sha256"] = record["trajectory_sha256"]
            else:
                core._clear_completion_metadata(run)
            base.save_state(state)

        core._persist_outcome = persist_outcome

    def reconcile(state: dict[str, Any], task_id: str) -> bool:
        changed = original_reconcile(state, task_id)
        earlier_invalid = False
        active_seen = False
        for run in state["runs"]:
            if run["state"] == "complete":
                continue
            if run["state"] != "running":
                earlier_invalid = True
                continue
            if earlier_invalid or active_seen:
                outcome = core._sequence_violation_outcome(run)
                core._apply_state_correction(state, run, outcome, {})
                changed = True
                continue

            active_seen = True
            record_path = core._record_path(run)
            record = _read_record(core.base, record_path)
            if record is None:
                # No durable final record exists. Leave the run resumable so the
                # core retry path archives the interrupted attempt before retrying.
                earlier_invalid = True
                continue

            candidate = dict(run)
            candidate["record"] = str(record_path.relative_to(core.base.OUTPUT_DIR))
            if isinstance(record.get("trajectory_sha256"), str):
                candidate["trajectory_sha256"] = record["trajectory_sha256"]
            preserved_record, outcome = core._classify_preserved_run(
                candidate, task_id
            )
            if outcome.state == "complete":
                _recover_complete(core, state, run, preserved_record, outcome)
                changed = True
                continue

            core._apply_state_correction(
                state, run, outcome, preserved_record
            )
            changed = True
            earlier_invalid = True

        if changed:
            core.base.save_state(state)
        return changed

    core.reconcile_completed_runs = reconcile
    return core
