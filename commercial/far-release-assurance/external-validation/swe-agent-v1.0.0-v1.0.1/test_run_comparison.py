from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_comparison


class EnvironmentLockTests(unittest.TestCase):
    def test_pending_status_blocks_execution(self) -> None:
        manifest = {
            "status": "execution_inputs_selected_local_environment_build_pending",
            "frozen_inputs": {},
        }
        with self.assertRaises(SystemExit):
            run_comparison.load_environment_lock(manifest)

    def test_lock_hash_and_boundaries_are_verified(self) -> None:
        lock = {
            "task_id": "scikit-learn__scikit-learn-14125",
            "swebench_harness_commit": "f7bbbb2ccdf479001d6467c9e34af59e44a840f9",
            "local_image_id": "sha256:" + "a" * 64,
            "outcome_data_exported": False,
            "model_call_started": False,
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lock_path = root / "environment-lock.json"
            lock_path.write_text(json.dumps(lock), encoding="utf-8")
            manifest = {
                "status": "execution_inputs_frozen",
                "frozen_inputs": {
                    "environment_lock_path": "environment-lock.json",
                    "environment_lock_sha256": run_comparison.sha256_file(lock_path),
                    "local_image_id": lock["local_image_id"],
                    "task_id": lock["task_id"],
                    "swebench_harness_commit": lock["swebench_harness_commit"],
                },
            }
            with patch.object(run_comparison, "CASE_DIR", root):
                self.assertEqual(run_comparison.load_environment_lock(manifest), lock)

    def test_outcome_export_in_lock_is_fatal(self) -> None:
        lock = {
            "task_id": "scikit-learn__scikit-learn-14125",
            "swebench_harness_commit": "f7bbbb2ccdf479001d6467c9e34af59e44a840f9",
            "local_image_id": "sha256:" + "a" * 64,
            "outcome_data_exported": True,
            "model_call_started": False,
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "environment-lock.json"
            path.write_text(json.dumps(lock), encoding="utf-8")
            manifest = {
                "status": "execution_inputs_frozen",
                "frozen_inputs": {
                    "environment_lock_path": path.name,
                    "environment_lock_sha256": run_comparison.sha256_file(path),
                    "local_image_id": lock["local_image_id"],
                    "task_id": lock["task_id"],
                    "swebench_harness_commit": lock["swebench_harness_commit"],
                },
            }
            with patch.object(run_comparison, "CASE_DIR", root), self.assertRaises(SystemExit):
                run_comparison.load_environment_lock(manifest)

    def test_model_call_in_lock_is_fatal(self) -> None:
        lock = {
            "task_id": "scikit-learn__scikit-learn-14125",
            "swebench_harness_commit": "f7bbbb2ccdf479001d6467c9e34af59e44a840f9",
            "local_image_id": "sha256:" + "a" * 64,
            "outcome_data_exported": False,
            "model_call_started": True,
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "environment-lock.json"
            path.write_text(json.dumps(lock), encoding="utf-8")
            manifest = {
                "status": "execution_inputs_frozen",
                "frozen_inputs": {
                    "environment_lock_path": path.name,
                    "environment_lock_sha256": run_comparison.sha256_file(path),
                    "local_image_id": lock["local_image_id"],
                    "task_id": lock["task_id"],
                    "swebench_harness_commit": lock["swebench_harness_commit"],
                },
            }
            with patch.object(run_comparison, "CASE_DIR", root), self.assertRaises(SystemExit):
                run_comparison.load_environment_lock(manifest)


if __name__ == "__main__":
    unittest.main()
