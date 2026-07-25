from __future__ import annotations

import hashlib
import json
import tempfile
import types
import unittest
from pathlib import Path

from execution_outcome import ExecutionOutcome
from validated_execution_recovery import install

TASK_ID = "task"


def success() -> ExecutionOutcome:
    return ExecutionOutcome(
        "success_with_patch",
        "complete",
        False,
        "submitted",
        True,
        False,
        "success_with_patch",
        {},
    )


class RecoverySequenceTests(unittest.TestCase):
    def test_second_running_slot_is_sequence_violation_after_first_recovers(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = types.SimpleNamespace()
            base.OUTPUT_DIR = root / "execution-output"
            base.RUNS_DIR = base.OUTPUT_DIR / "runs"
            base.utc_now = lambda: "recovered-now"
            base.sha256_file = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()

            def write_json(path, value):
                path = Path(path)
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")

            def read_json(path):
                value = json.loads(Path(path).read_text(encoding="utf-8"))
                if not isinstance(value, dict):
                    raise SystemExit("Expected JSON object")
                return value

            base.write_json = write_json
            base.read_json = read_json
            base.save_state = lambda state: None

            core = types.SimpleNamespace()
            core.base = base
            core.reconcile_completed_runs = lambda state, task_id: False
            core._record_path = lambda run: base.RUNS_DIR / run["run_id"] / "run-record.json"
            core._sequence_violation_outcome = lambda run: ExecutionOutcome(
                "protocol_sequence_violation",
                "failed_terminal",
                False,
                None,
                False,
                False,
                "sequence violation",
                {"run_id": run["run_id"]},
            )

            def apply_correction(state, run, result, record):
                run["state"] = result.state
                run["outcome_category"] = result.category

            core._apply_state_correction = apply_correction

            def running(run_id):
                return {
                    "run_id": run_id,
                    "state": "running",
                    "attempts": 1,
                    "record": None,
                    "trajectory_artifact": f"{run_id}.traj",
                    "trajectory": f"trajectories/{run_id}.traj",
                }

            first = running("v1.0.0-r1")
            second = running("v1.0.0-r2")
            second["recovery"] = "recoveries/stale.json"
            records = {}
            for run in (first, second):
                record = {
                    "completed_at": f"{run['run_id']}-completed",
                    "trajectory_sha256": f"{run['run_id']}-trajectory-hash",
                }
                records[run["run_id"]] = record
                base.write_json(core._record_path(run), record)

            def classify(candidate, task_id):
                return records[candidate["run_id"]], success()

            core._classify_preserved_run = classify
            install(core)
            state = {"runs": [first, second]}

            changed = core.reconcile_completed_runs(state, TASK_ID)

            self.assertTrue(changed)
            self.assertEqual(first["state"], "complete")
            self.assertEqual(second["state"], "failed_terminal")
            self.assertEqual(
                second["outcome_category"], "protocol_sequence_violation"
            )
            self.assertEqual(len(state["recoveries"]), 1)
            self.assertNotIn("recovery", second)

    def test_persisted_new_attempt_clears_stale_recovery_pointer(self) -> None:
        core = types.SimpleNamespace()
        core.reconcile_completed_runs = lambda state, task_id: False
        core._apply_state_correction = lambda state, run, result, record: None

        def persist(state, run, record, result):
            run["persisted"] = True

        core._persist_outcome = persist
        install(core)
        run = {"recovery": "recoveries/stale.json"}

        core._persist_outcome({}, run, {}, success())

        self.assertNotIn("recovery", run)
        self.assertTrue(run["persisted"])


if __name__ == "__main__":
    unittest.main()
