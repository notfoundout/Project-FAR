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


def outcome(state: str, category: str, retryable: bool = False) -> ExecutionOutcome:
    return ExecutionOutcome(
        category,
        state,
        retryable,
        "submitted" if state == "complete" else "exit_error",
        state == "complete",
        False,
        category,
        {},
    )


class RecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        base = types.SimpleNamespace()
        base.OUTPUT_DIR = root / "execution-output"
        base.RUNS_DIR = base.OUTPUT_DIR / "runs"
        base.saved = []
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
        base.save_state = lambda state: base.saved.append(json.loads(json.dumps(state)))

        core = types.SimpleNamespace()
        core.base = base
        core.reconcile_completed_runs = lambda state, task_id: False
        core._record_path = lambda run: base.RUNS_DIR / run["run_id"] / "run-record.json"
        core._sequence_violation_outcome = lambda run: outcome(
            "failed_terminal", "protocol_sequence_violation"
        )

        def apply_correction(state, run, result, record):
            run["state"] = result.state
            run["outcome_category"] = result.category
            state.setdefault("corrections", []).append(
                {"run_id": run["run_id"], "category": result.category}
            )

        core._apply_state_correction = apply_correction
        self.base = base
        self.core = core

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def running(self) -> dict:
        return {
            "run_id": "v1.0.0-r1",
            "state": "running",
            "attempts": 1,
            "record": None,
            "trajectory_artifact": "run.traj",
            "trajectory": "trajectories/run.traj",
        }

    def test_running_without_final_record_remains_resumable(self) -> None:
        run = self.running()
        self.core._classify_preserved_run = lambda candidate, task_id: self.fail(
            "classifier must not run without a durable record"
        )
        install(self.core)

        changed = self.core.reconcile_completed_runs({"runs": [run]}, TASK_ID)

        self.assertFalse(changed)
        self.assertEqual(run["state"], "running")
        self.assertEqual(self.base.saved, [])

    def test_valid_final_record_recovers_running_state_to_complete(self) -> None:
        run = self.running()
        record_path = self.core._record_path(run)
        record = {
            "completed_at": "completed-before-interruption",
            "trajectory_sha256": "trajectory-hash",
        }
        self.base.write_json(record_path, record)

        def classify(candidate, task_id):
            self.assertEqual(
                candidate["record"],
                "runs/v1.0.0-r1/run-record.json",
            )
            self.assertEqual(candidate["trajectory_sha256"], "trajectory-hash")
            return record, outcome("complete", "success_with_patch")

        self.core._classify_preserved_run = classify
        install(self.core)
        state = {"runs": [run]}

        changed = self.core.reconcile_completed_runs(state, TASK_ID)

        self.assertTrue(changed)
        self.assertEqual(run["state"], "complete")
        self.assertEqual(run["completed_at"], "completed-before-interruption")
        self.assertEqual(run["trajectory_sha256"], "trajectory-hash")
        self.assertEqual(run["outcome_category"], "success_with_patch")
        recovery_path = self.base.OUTPUT_DIR / run["recovery"]
        self.assertTrue(recovery_path.is_file())
        self.assertEqual(state["recoveries"][0]["before_state"], "running")
        self.assertEqual(len(self.base.saved), 1)

    def test_final_failure_is_reclassified_before_retry(self) -> None:
        run = self.running()
        record_path = self.core._record_path(run)
        record = {"returncode": 86}
        self.base.write_json(record_path, record)
        self.core._classify_preserved_run = lambda candidate, task_id: (
            record,
            outcome("failed_retryable", "provider_quota_exhaustion", True),
        )
        install(self.core)
        state = {"runs": [run]}

        changed = self.core.reconcile_completed_runs(state, TASK_ID)

        self.assertTrue(changed)
        self.assertEqual(run["state"], "failed_retryable")
        self.assertEqual(run["outcome_category"], "provider_quota_exhaustion")
        self.assertEqual(state["corrections"][0]["run_id"], run["run_id"])

    def test_running_after_earlier_failure_is_sequence_violation(self) -> None:
        first = {"run_id": "v1.0.0-r1", "state": "failed_retryable"}
        second = self.running()
        second["run_id"] = "v1.0.0-r2"
        self.core._classify_preserved_run = lambda candidate, task_id: self.fail(
            "out-of-sequence run must not be classified as valid"
        )
        install(self.core)
        state = {"runs": [first, second]}

        changed = self.core.reconcile_completed_runs(state, TASK_ID)

        self.assertTrue(changed)
        self.assertEqual(second["state"], "failed_terminal")
        self.assertEqual(second["outcome_category"], "protocol_sequence_violation")


if __name__ == "__main__":
    unittest.main()
