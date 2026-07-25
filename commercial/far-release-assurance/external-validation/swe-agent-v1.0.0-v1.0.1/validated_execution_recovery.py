from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from execution_outcome import ExecutionOutcome


def _read_record(base: Any, path: Path) -> dict[str, Any] | None:
    try:
        value = base.read_json(path)
    except (SystemExit, OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _next_recovery_path(base: Any, run: dict[str, Any]) -> Path:
    recovery_dir = base.OUTPUT_DIR / "recoveries"
    attempt = int(run.get("attempts", 0))
    stem = f"{run['run_id']}-attempt-{attempt:03d}-running-to-complete"
    candidate = recovery_dir / f"{stem}.json"
    if not candidate.exists():
        return candidate
    index = 1
    while True:
        candidate = recovery_dir / f"{stem}-recovery-{index:02d}.json"
        if not candidate.exists():
            return candidate
        index += 1


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
    recovery_path = _next_recovery_path(base, run)
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


def _load_reconcilable_state(
    base: Any,
    manifest: dict[str, Any],
    lock: dict[str, Any],
    plan_sha256: str,
) -> dict[str, Any]:
    if not base.STATE_PATH.is_file():
        return base.initial_state(manifest, lock, plan_sha256)
    state = base.read_json(base.STATE_PATH)
    if (
        state.get("schema") != base.STATE_SCHEMA
        or state.get("case_id") != manifest.get("case_id")
    ):
        raise SystemExit("Execution state schema or case mismatch")
    if state.get("manifest_sha256") != base.sha256_file(base.MANIFEST_PATH):
        raise SystemExit("Execution state was created for a different manifest")
    if state.get("environment_lock_sha256") != base.sha256_file(base.LOCK_PATH):
        raise SystemExit(
            "Execution state was created for a different environment lock"
        )
    if state.get("execution_plan_sha256") != plan_sha256:
        raise SystemExit("Execution state was created for a different execution plan")
    if state.get("immutable_image_reference") != lock.get(
        "immutable_image_reference"
    ):
        raise SystemExit("Execution state image mismatch")

    expected = base.expected_runs(manifest)
    actual = state.get("runs")
    if not isinstance(actual, list) or len(actual) != len(expected):
        raise SystemExit("Execution state run matrix mismatch")
    for frozen, recorded in zip(expected, actual, strict=True):
        for key in (
            "slot",
            "run_id",
            "release",
            "commit",
            "full_commit",
            "repetition",
            "trajectory_artifact",
        ):
            if recorded.get(key) != frozen.get(key):
                raise SystemExit(
                    f"Execution state drift at run {frozen['run_id']}: {key}"
                )
        if recorded.get("state") not in base.ALLOWED_STATES:
            raise SystemExit(
                f"Invalid execution state for {frozen['run_id']}: "
                f"{recorded.get('state')!r}"
            )
    return state


def install(core: Any) -> Any:
    original_reconcile = core.reconcile_completed_runs
    core.base.load_state = lambda manifest, lock, plan_sha256: (
        _load_reconcilable_state(core.base, manifest, lock, plan_sha256)
    )
    original_apply_correction = core._apply_state_correction
    original_persist_outcome = getattr(core, "_persist_outcome", None)

    def sequence_violation_outcome(run):
        return ExecutionOutcome(
            "protocol_sequence_violation",
            "failed_terminal",
            False,
            None,
            False,
            False,
            "run contains execution state after an earlier frozen slot became incomplete",
            {
                "run_id": run["run_id"],
                "slot": run.get("slot"),
                "state": run.get("state"),
                "attempts": run.get("attempts"),
            },
        )

    core._sequence_violation_outcome = sequence_violation_outcome

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
        frontier_seen = False
        for run in state["runs"]:
            if not frontier_seen:
                if run["state"] == "complete":
                    continue
                frontier_seen = True
                if run["state"] != "running":
                    continue

                record_path = core._record_path(run)
                record = _read_record(core.base, record_path)
                if record is None:
                    # No durable final record exists. Leave the run resumable so
                    # the core retry path archives it before retrying.
                    continue

                candidate = dict(run)
                candidate["record"] = str(
                    record_path.relative_to(core.base.OUTPUT_DIR)
                )
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
                continue

            untouched_pending = (
                run["state"] == "pending"
                and int(run.get("attempts", 0)) == 0
            )
            already_sequence_blocked = (
                run["state"] == "failed_terminal"
                and run.get("outcome_category") == "protocol_sequence_violation"
            )
            if untouched_pending or already_sequence_blocked:
                continue

            outcome = core._sequence_violation_outcome(run)
            core._apply_state_correction(state, run, outcome, {})
            changed = True

        if changed:
            core.base.save_state(state)
        return changed

    core.reconcile_completed_runs = reconcile
    return core
