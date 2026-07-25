from __future__ import annotations

import hashlib
import importlib
import json
import sys
import tempfile
import types
import unittest
from unittest import mock
from datetime import datetime, timezone
from pathlib import Path

from execution_outcome import classify_execution

TASK_ID = "scikit-learn__scikit-learn-14125"


class ExecutionOutcomeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.output = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_status(self, status: str) -> None:
        (self.output / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status:\n"
            + f"  {status}:\n"
            + f"    - {TASK_ID}\n"
            + "total_cost: 0\n",
            encoding="utf-8",
        )

    def write_prediction(
        self,
        patch: object,
        no_change: bool = False,
        *,
        task_id: str = TASK_ID,
        filename: str | None = None,
    ) -> Path:
        payload = {
            "instance_id": task_id,
            "model_patch": patch,
            "no_change": no_change,
        }
        target = self.output / (filename or f"{task_id}.pred")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload), encoding="utf-8")
        return target

    def classify(
        self,
        rc: int = 0,
        stdout: str = "",
        stderr: str = "",
        allow_no_change: bool = False,
    ):
        return classify_execution(
            outer_returncode=rc,
            swe_output=self.output,
            task_id=TASK_ID,
            stdout=stdout,
            stderr=stderr,
            allow_no_change=allow_no_change,
        )

    def test_outer_zero_internal_exit_error_empty_patch_quota_is_retryable(self) -> None:
        self.write_status("exit_error")
        self.write_prediction(None)
        outcome = self.classify(
            stderr=(
                "RESOURCE_EXHAUSTED request-per-minute request-per-day "
                "input-token-per-day"
            )
        )
        self.assertEqual(outcome.category, "provider_quota_exhaustion")
        self.assertEqual(outcome.state, "failed_retryable")
        self.assertTrue(outcome.retryable)
        self.assertFalse(outcome.patch_present)

    def test_quota_without_status_file_remains_retryable(self) -> None:
        outcome = self.classify(
            rc=1, stderr="HTTP 429 RESOURCE_EXHAUSTED request-per-day"
        )
        self.assertEqual(outcome.category, "provider_quota_exhaustion")
        self.assertEqual(outcome.state, "failed_retryable")

    def test_outer_zero_internal_exit_error_without_provider_signal_is_terminal(self) -> None:
        self.write_status("exit_error")
        self.write_prediction("")
        outcome = self.classify()
        self.assertEqual(outcome.category, "terminal_agent_error")
        self.assertEqual(outcome.state, "failed_terminal")

    def test_nonzero_outer_with_internal_agent_error_is_terminal(self) -> None:
        self.write_status("exit_error")
        self.write_prediction("")
        outcome = self.classify(rc=2, stderr="deterministic agent failure")
        self.assertEqual(outcome.category, "terminal_agent_error")
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertFalse(outcome.retryable)

    def test_success_requires_non_empty_patch(self) -> None:
        self.write_status("submitted")
        self.write_prediction("non-empty patch")
        outcome = self.classify()
        self.assertEqual(outcome.category, "success_with_patch")
        self.assertEqual(outcome.state, "complete")

    def test_recovered_provider_error_does_not_override_validated_success(self) -> None:
        self.write_status("submitted")
        self.write_prediction("non-empty patch")
        outcome = self.classify(
            stderr="earlier retry received HTTP 429 and timed out"
        )
        self.assertEqual(outcome.category, "success_with_patch")
        self.assertEqual(outcome.state, "complete")
        self.assertFalse(outcome.retryable)

    def test_success_status_with_empty_patch_is_rejected(self) -> None:
        self.write_status("submitted")
        self.write_prediction("")
        self.assertEqual(self.classify().state, "failed_terminal")

    def test_nonzero_outer_cannot_complete_even_with_success_status_and_patch(self) -> None:
        self.write_status("submitted")
        self.write_prediction("non-empty patch")
        outcome = self.classify(rc=3)
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertEqual(outcome.category, "terminal_agent_error")

    def test_nonzero_outer_with_provider_signal_is_retryable(self) -> None:
        self.write_status("submitted")
        self.write_prediction("non-empty patch")
        outcome = self.classify(rc=1, stderr="HTTP 503 service unavailable")
        self.assertEqual(outcome.state, "failed_retryable")
        self.assertEqual(outcome.category, "retryable_provider_error")

    def test_no_change_requires_explicit_protocol_permission(self) -> None:
        self.write_status("submitted")
        self.write_prediction("", no_change=True)
        self.assertEqual(
            self.classify(allow_no_change=False).state, "failed_terminal"
        )
        self.assertEqual(
            self.classify(allow_no_change=True).category, "valid_no_change"
        )

    def test_missing_target_instance_is_terminal(self) -> None:
        (self.output / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status:\n  submitted:\n    - another-task\n",
            encoding="utf-8",
        )
        self.write_prediction("non-empty patch")
        outcome = self.classify()
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("exactly one", outcome.reason)

    def test_unrelated_prediction_file_is_not_accepted(self) -> None:
        self.write_status("submitted")
        self.write_prediction(
            "patch for another task",
            task_id="another-task",
            filename="another-task.pred",
        )
        outcome = self.classify()
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertFalse(outcome.patch_present)

    def test_missing_prediction_with_provider_marker_is_retryable(self) -> None:
        self.write_status("exit_error")
        outcome = self.classify(stderr="HTTP 429 RESOURCE_EXHAUSTED")
        self.assertEqual(outcome.state, "failed_retryable")
        self.assertEqual(outcome.category, "provider_quota_exhaustion")

    def test_missing_prediction_without_provider_marker_is_terminal(self) -> None:
        self.write_status("exit_error")
        outcome = self.classify(stderr="agent stopped without a prediction")
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("missing prediction evidence", outcome.reason)

    def test_missing_prediction_with_transient_provider_marker_is_retryable(self) -> None:
        self.write_status("exit_error")
        outcome = self.classify(stderr="HTTP 503 service unavailable")
        self.assertEqual(outcome.state, "failed_retryable")
        self.assertEqual(outcome.category, "retryable_provider_error")

    def test_unrelated_prediction_with_provider_marker_is_terminal(self) -> None:
        self.write_status("exit_error")
        self.write_prediction(
            None, task_id="another-task", filename="another-task.pred"
        )
        outcome = self.classify(stderr="HTTP 429 RESOURCE_EXHAUSTED")
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("does not identify target instance", outcome.reason)

    def test_duplicate_status_files_with_provider_marker_are_terminal(self) -> None:
        self.write_status("exit_error")
        nested = self.output / "nested"
        nested.mkdir()
        (nested / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status:\n"
            f"  exit_error: [{TASK_ID}]\n",
            encoding="utf-8",
        )
        outcome = self.classify(stderr="HTTP 503 service unavailable")
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("expected exactly one", outcome.reason)

    def test_malformed_status_with_provider_marker_fails_closed(self) -> None:
        (self.output / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status: [not-a-mapping]\n", encoding="utf-8"
        )
        self.write_prediction(None)
        outcome = self.classify(stderr="HTTP 503 service unavailable")
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("not a mapping", outcome.reason)

    def test_conflicting_duplicate_prediction_evidence_is_terminal(self) -> None:
        self.write_status("submitted")
        self.write_prediction("patch-a")
        nested = self.output / "nested"
        nested.mkdir()
        (nested / "preds.json").write_text(
            json.dumps(
                [
                    {
                        "instance_id": TASK_ID,
                        "model_patch": "patch-b",
                        "no_change": False,
                    }
                ]
            ),
            encoding="utf-8",
        )
        outcome = self.classify()
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("conflicting prediction evidence", outcome.reason)

    def test_consistent_duplicate_prediction_evidence_is_terminal(self) -> None:
        self.write_status("submitted")
        self.write_prediction("patch-a")
        (self.output / "preds.json").write_text(
            json.dumps(
                {
                    TASK_ID: {
                        "model_patch": "patch-a",
                        "no_change": False,
                    }
                }
            ),
            encoding="utf-8",
        )
        outcome = self.classify()
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("duplicate prediction evidence", outcome.reason)

    def test_duplicate_yaml_status_key_is_terminal(self) -> None:
        (self.output / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status:\n"
            f"  submitted: [{TASK_ID}]\n"
            f"  submitted: [{TASK_ID}]\n",
            encoding="utf-8",
        )
        self.write_prediction("patch")
        outcome = self.classify()
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("duplicate key", outcome.reason)

    def test_symlinked_prediction_is_terminal(self) -> None:
        self.write_status("submitted")
        external = self.output.parent / "external.pred"
        external.write_text(
            json.dumps({"instance_id": TASK_ID, "model_patch": "patch"}),
            encoding="utf-8",
        )
        (self.output / f"{TASK_ID}.pred").symlink_to(external)
        outcome = self.classify(stderr="HTTP 429 RESOURCE_EXHAUSTED")
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("not a regular file", outcome.reason)

    def test_symlinked_output_directory_is_terminal(self) -> None:
        external = self.output / "external-output"
        external.mkdir()
        (external / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status:\n"
            f"  submitted: [{TASK_ID}]\n",
            encoding="utf-8",
        )
        (external / f"{TASK_ID}.pred").write_text(
            json.dumps({"instance_id": TASK_ID, "model_patch": "patch"}),
            encoding="utf-8",
        )
        linked = self.output / "linked"
        linked.symlink_to(external, target_is_directory=True)
        outcome = classify_execution(
            outer_returncode=0,
            swe_output=linked,
            task_id=TASK_ID,
            stdout="",
            stderr="",
        )
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("not a local regular directory", outcome.reason)

    def test_malformed_exact_prediction_is_terminal(self) -> None:
        self.write_status("submitted")
        (self.output / f"{TASK_ID}.pred").write_text("not json", encoding="utf-8")
        outcome = self.classify()
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("invalid JSON", outcome.reason)

    def test_non_empty_patch_and_no_change_is_rejected(self) -> None:
        self.write_status("submitted")
        self.write_prediction("patch", no_change=True)
        outcome = self.classify()
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("both a non-empty patch and no-change", outcome.reason)


def make_base(root: Path) -> types.ModuleType:
    base = types.ModuleType("execute_controller")
    base.ALLOWED_STATES = {"pending", "running", "failed_retryable", "complete"}
    base.OUTPUT_DIR = root / "execution-output"
    base.RUNS_DIR = base.OUTPUT_DIR / "runs"
    base.TRAJECTORY_DIR = base.OUTPUT_DIR / "trajectories"
    base.CONFIG_PATH = root / "agent-config.yaml"
    base.CONFIG_PATH.write_text("config\n", encoding="utf-8")
    base.saved_states = []

    def sha256_file(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def write_json(path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    def read_json(path: Path):
        if not path.is_file():
            raise SystemExit(f"Missing required file: {path}")
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise SystemExit(f"Expected JSON object: {path}")
        return value

    def collect_hashes(path: Path):
        return {
            str(item.relative_to(path)): sha256_file(item)
            for item in sorted(
                candidate for candidate in path.rglob("*") if candidate.is_file()
            )
        }

    def save_state(state):
        base.saved_states.append(json.loads(json.dumps(state)))

    base.sha256_file = sha256_file
    base.write_json = write_json
    base.read_json = read_json
    base.collect_hashes = collect_hashes
    base.save_state = save_state
    base.utc_now = lambda: datetime.now(timezone.utc).isoformat()
    return base


class ValidatedControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.original_base = sys.modules.get("execute_controller")
        self.original_validated = sys.modules.get("validated_execute_controller")
        self.base = make_base(self.root)
        sys.modules["execute_controller"] = self.base
        sys.modules.pop("validated_execute_controller", None)
        self.controller = importlib.import_module("validated_execute_controller")

    def tearDown(self) -> None:
        if self.original_validated is None:
            sys.modules.pop("validated_execute_controller", None)
        else:
            sys.modules["validated_execute_controller"] = self.original_validated
        if self.original_base is None:
            sys.modules.pop("execute_controller", None)
        else:
            sys.modules["execute_controller"] = self.original_base
        self.tmp.cleanup()

    def make_run(self, run_id: str, slot: int, state: str = "complete") -> dict:
        return {
            "run_id": run_id,
            "slot": slot,
            "state": state,
            "attempts": 1,
            "trajectory_artifact": f"{run_id}.traj",
            "completed_at": "old",
            "trajectory_sha256": "old-hash",
        }

    def write_evidence(
        self,
        run: dict,
        *,
        internal_status: str,
        patch: object,
        stderr: str = "",
        returncode: int = 0,
    ) -> None:
        run_dir = self.base.RUNS_DIR / run["run_id"]
        output = run_dir / "sweagent-output"
        output.mkdir(parents=True)
        (output / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status:\n"
            + f"  {internal_status}:\n"
            + f"    - {TASK_ID}\n",
            encoding="utf-8",
        )
        (output / f"{TASK_ID}.pred").write_text(
            json.dumps({"instance_id": TASK_ID, "model_patch": patch}),
            encoding="utf-8",
        )
        (run_dir / "stdout.log").write_text("", encoding="utf-8")
        (run_dir / "stderr.log").write_text(stderr, encoding="utf-8")
        self.base.write_json(
            run_dir / "run-record.json",
            {"state": "complete", "returncode": returncode},
        )

    def test_reconcile_reclassifies_legacy_false_completion(self) -> None:
        first = self.make_run("v1.0.0-r1", 1)
        second = self.make_run("v1.0.0-r2", 2, "pending")
        self.write_evidence(
            first,
            internal_status="exit_error",
            patch=None,
            stderr="RESOURCE_EXHAUSTED HTTP 429 request-per-day",
        )
        state = {"runs": [first, second]}

        changed = self.controller.reconcile_completed_runs(state, TASK_ID)

        self.assertTrue(changed)
        self.assertEqual(first["state"], "failed_retryable")
        self.assertEqual(first["outcome_category"], "provider_quota_exhaustion")
        self.assertNotIn("completed_at", first)
        self.assertNotIn("trajectory_sha256", first)
        self.assertEqual(second["state"], "pending")
        correction = (
            self.base.RUNS_DIR / first["run_id"] / "run-record-correction.json"
        )
        self.assertTrue(correction.is_file())
        self.assertEqual(len(state["corrections"]), 1)
        self.assertEqual(len(self.base.saved_states), 1)

    def test_reconcile_invalidates_later_completion_after_bad_earlier_slot(self) -> None:
        first = self.make_run("v1.0.0-r1", 1)
        second = self.make_run("v1.0.0-r2", 2)
        self.write_evidence(first, internal_status="exit_error", patch="")
        self.write_evidence(second, internal_status="submitted", patch="valid")
        state = {"runs": [first, second]}

        self.controller.reconcile_completed_runs(state, TASK_ID)

        self.assertEqual(first["state"], "failed_terminal")
        self.assertEqual(second["state"], "failed_terminal")
        self.assertEqual(
            second["outcome_category"], "protocol_sequence_violation"
        )

    def test_terminal_failure_blocks_matrix_progression(self) -> None:
        state = {"runs": [self.make_run("v1.0.0-r1", 1, "failed_terminal")]}
        state["runs"][0]["outcome_category"] = "terminal_agent_error"
        with self.assertRaisesRegex(SystemExit, "blocked by terminal failure"):
            self.controller._ensure_progressable(state)

    def test_archive_preserves_previous_attempt_and_stale_trajectory(self) -> None:
        run = self.make_run("v1.0.0-r1", 1, "failed_retryable")
        run_dir = self.base.RUNS_DIR / run["run_id"]
        run_dir.mkdir(parents=True)
        for name in ("instance.json", "stdout.log", "run-record.json"):
            (run_dir / name).write_text(name, encoding="utf-8")
        (run_dir / "sweagent-output").mkdir()
        (run_dir / "sweagent-output" / "partial").write_text(
            "partial", encoding="utf-8"
        )
        self.base.TRAJECTORY_DIR.mkdir(parents=True)
        trajectory = self.base.TRAJECTORY_DIR / run["trajectory_artifact"]
        trajectory.write_text("stale", encoding="utf-8")

        archived = self.controller._archive_previous_attempt(run, run_dir)

        archive = self.base.OUTPUT_DIR / archived
        self.assertTrue((archive / "instance.json").is_file())
        self.assertTrue((archive / "sweagent-output" / "partial").is_file())
        self.assertTrue((archive / "trajectory" / trajectory.name).is_file())
        self.assertFalse(trajectory.exists())
        self.assertFalse((run_dir / "run-record.json").exists())

    def test_current_hashes_exclude_records_and_archived_attempts(self) -> None:
        run_dir = self.base.RUNS_DIR / "run"
        (run_dir / "attempts" / "attempt-001").mkdir(parents=True)
        (run_dir / "attempts" / "attempt-001" / "old.log").write_text(
            "old", encoding="utf-8"
        )
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "stdout.log").write_text("current", encoding="utf-8")
        (run_dir / "run-record.json").write_text("record", encoding="utf-8")
        (run_dir / "run-record-correction.json").write_text(
            "correction", encoding="utf-8"
        )

        hashes = self.controller._current_artifact_hashes(run_dir)

        self.assertEqual(set(hashes), {"stdout.log"})

    def test_current_hashes_reject_symlinked_external_evidence(self) -> None:
        run_dir = self.base.RUNS_DIR / "run"
        run_dir.mkdir(parents=True)
        external = self.root / "external.log"
        external.write_text("external", encoding="utf-8")
        (run_dir / "stdout.log").symlink_to(external)
        with self.assertRaisesRegex(SystemExit, "contains a symlink"):
            self.controller._current_artifact_hashes(run_dir)

    def test_interrupted_archive_rolls_back_all_moved_evidence(self) -> None:
        run = self.make_run("v1.0.0-r1", 1, "failed_retryable")
        run_dir = self.base.RUNS_DIR / run["run_id"]
        run_dir.mkdir(parents=True)
        first = run_dir / "instance.json"
        second = run_dir / "stdout.log"
        first.write_text("instance", encoding="utf-8")
        second.write_text("stdout", encoding="utf-8")
        real_move = self.controller.shutil.move
        calls = 0

        def interrupted(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated interruption")
            return real_move(source, destination)

        with mock.patch.object(self.controller.shutil, "move", side_effect=interrupted):
            with self.assertRaisesRegex(OSError, "simulated interruption"):
                self.controller._archive_previous_attempt(run, run_dir)
        self.assertEqual(first.read_text(encoding="utf-8"), "instance")
        self.assertEqual(second.read_text(encoding="utf-8"), "stdout")
        self.assertFalse((run_dir / "attempts").exists())


if __name__ == "__main__":
    unittest.main()
