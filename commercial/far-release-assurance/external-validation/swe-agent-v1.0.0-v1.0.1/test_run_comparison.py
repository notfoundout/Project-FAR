from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_comparison

TASK_ID = "scikit-learn__scikit-learn-14125"
HARNESS = "f7bbbb2ccdf479001d6467c9e34af59e44a840f9"
LOCAL_ID = "sha256:" + "a" * 64
DIGEST = "sha256:" + "b" * 64
REFERENCE = "ghcr.io/notfoundout/project-far-swebench-scikit-learn-14125@" + DIGEST


def make_lock(*, outcome_exported: bool = False, model_started: bool = False) -> dict:
    return {
        "task_id": TASK_ID,
        "swebench_harness_commit": HARNESS,
        "local_image_id": LOCAL_ID,
        "immutable_image_reference": REFERENCE,
        "registry_digest": DIGEST,
        "cross_runner_portable": True,
        "outcome_data_exported": outcome_exported,
        "model_call_started": model_started,
    }


def make_manifest(path: Path, lock: dict) -> dict:
    return {
        "status": "execution_inputs_frozen",
        "frozen_inputs": {
            "environment_lock_path": path.name,
            "environment_lock_sha256": run_comparison.sha256_file(path),
            "local_image_id": lock["local_image_id"],
            "immutable_image_reference": lock["immutable_image_reference"],
            "registry_digest": lock["registry_digest"],
            "task_id": lock["task_id"],
            "swebench_harness_commit": lock["swebench_harness_commit"],
        },
    }


class EnvironmentLockTests(unittest.TestCase):
    def test_pending_status_blocks_execution(self) -> None:
        manifest = {"status": "execution_inputs_selected_local_environment_build_pending", "frozen_inputs": {}}
        with self.assertRaises(SystemExit):
            run_comparison.load_environment_lock(manifest)

    def test_lock_hash_portability_and_boundaries_are_verified(self) -> None:
        lock = make_lock()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lock_path = root / "environment-lock.json"
            lock_path.write_text(json.dumps(lock), encoding="utf-8")
            with patch.object(run_comparison, "CASE_DIR", root):
                self.assertEqual(run_comparison.load_environment_lock(make_manifest(lock_path, lock)), lock)

    def test_outcome_export_in_lock_is_fatal(self) -> None:
        lock = make_lock(outcome_exported=True)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "environment-lock.json"
            path.write_text(json.dumps(lock), encoding="utf-8")
            with patch.object(run_comparison, "CASE_DIR", root), self.assertRaises(SystemExit):
                run_comparison.load_environment_lock(make_manifest(path, lock))

    def test_model_call_in_lock_is_fatal(self) -> None:
        lock = make_lock(model_started=True)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "environment-lock.json"
            path.write_text(json.dumps(lock), encoding="utf-8")
            with patch.object(run_comparison, "CASE_DIR", root), self.assertRaises(SystemExit):
                run_comparison.load_environment_lock(make_manifest(path, lock))

    def test_nonportable_lock_is_fatal(self) -> None:
        lock = make_lock()
        lock["cross_runner_portable"] = False
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "environment-lock.json"
            path.write_text(json.dumps(lock), encoding="utf-8")
            with patch.object(run_comparison, "CASE_DIR", root), self.assertRaises(SystemExit):
                run_comparison.load_environment_lock(make_manifest(path, lock))


if __name__ == "__main__":
    unittest.main()
