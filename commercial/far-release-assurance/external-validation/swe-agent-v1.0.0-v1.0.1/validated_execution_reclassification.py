from __future__ import annotations

from pathlib import Path
from typing import Any

_RECLASSIFIABLE_STATES = {"failed_retryable", "failed_terminal"}


def _next_correction_path(base: Any, run: dict[str, Any]) -> Path:
    correction_dir = base.OUTPUT_DIR / "corrections"
    attempt = int(run.get("attempts", 0))
    stem = f"{run['run_id']}-attempt-{attempt:03d}-evidence-reclassification"
    candidate = correction_dir / f"{stem}.json"
    if not candidate.exists():
        return candidate
    index = 1
    while True:
        candidate = correction_dir / f"{stem}-{index:02d}.json"
        if not candidate.exists():
            return candidate
        index += 1


def install(core: Any) -> Any:
    """Re-evaluate the first failed slot when classifier semantics improve.

    Preserved execution evidence is immutable, but the validator itself can be
    corrected. This wrapper permits an auditable state transition between
    failed states (or back to a fully provenance-validated completion) without
    deleting or overwriting the earlier correction record.
    """
    original_reconcile = core.reconcile_completed_runs

    def reconcile(state: dict[str, Any], task_id: str) -> bool:
        changed = original_reconcile(state, task_id)
        run = next((item for item in state["runs"] if item["state"] != "complete"), None)
        if run is None or run.get("state") not in _RECLASSIFIABLE_STATES:
            return changed

        record_path = core._record_path(run)
        if not record_path.is_file():
            return changed

        record, outcome = core._classify_preserved_run(run, task_id)
        if outcome.state not in _RECLASSIFIABLE_STATES | {"complete"}:
            return changed
        if (
            outcome.state == run.get("state")
            and outcome.category == run.get("outcome_category")
        ):
            return changed

        base = core.base
        before_state = run.get("state")
        correction_path = _next_correction_path(base, run)
        correction = {
            "schema": "far-swe-agent-evidence-reclassification/1.0",
            "corrected_at": base.utc_now(),
            "run_id": run["run_id"],
            "attempts_preserved": run.get("attempts"),
            "before_state": before_state,
            "after_state": outcome.state,
            "before_outcome_category": run.get("outcome_category"),
            "after_outcome_category": outcome.category,
            "previous_correction": run.get("correction"),
            "run_record_sha256": base.sha256_file(record_path),
            "raw_artifact_sha256": base.collect_hashes(base.RUNS_DIR / run["run_id"]),
            "outcome": outcome.to_dict(),
        }
        base.write_json(correction_path, correction)
        state.setdefault("corrections", []).append(correction)

        run.update(
            {
                "state": outcome.state,
                "record": str(record_path.relative_to(base.OUTPUT_DIR)),
                "outcome_category": outcome.category,
                "corrected_from": before_state,
                "correction": str(correction_path.relative_to(base.OUTPUT_DIR)),
            }
        )
        run.pop("recovery", None)
        if outcome.state == "complete":
            completed_at = record.get("completed_at")
            trajectory_sha256 = record.get("trajectory_sha256")
            if not isinstance(completed_at, str) or not completed_at:
                raise SystemExit(
                    f"Reclassified completion lacks completed_at: {run['run_id']}"
                )
            if not isinstance(trajectory_sha256, str) or not trajectory_sha256:
                raise SystemExit(
                    f"Reclassified completion lacks trajectory_sha256: {run['run_id']}"
                )
            run["completed_at"] = completed_at
            run["trajectory_sha256"] = trajectory_sha256
        else:
            core._clear_completion_metadata(run)

        base.save_state(state)
        return True

    core.reconcile_completed_runs = reconcile
    return core
