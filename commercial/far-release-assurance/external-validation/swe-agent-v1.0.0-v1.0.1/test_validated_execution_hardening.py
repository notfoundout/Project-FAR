from __future__ import annotations

import hashlib
import importlib
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path

TASK_ID = "scikit-learn__scikit-learn-14125"


def _base(root: Path) -> types.ModuleType:
    base = types.ModuleType("execute_controller")
    base.ALLOWED_STATES = {"pending", "running", "failed_retryable", "complete"}
    base.OUTPUT_DIR = root / "execution-output"
    base.RUNS_DIR = base.OUTPUT_DIR / "runs"
    base.TRAJECTORY_DIR = base.OUTPUT_DIR / "trajectories"
    base.CONFIG_PATH = root / "agent-config.yaml"
    base.CONFIG_PATH.write_text("config\n", encoding="utf-8")
    base.sha256_file = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    base.write_json = lambda p, v: (
        Path(p).parent.mkdir(parents=True, exist_ok=True),
        Path(p).write_text(json.dumps(v, sort_keys=True) + "\n", encoding="utf-8"),
    )[-1]

    def read_json(path):
        value = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise SystemExit("Expected JSON object")
        return value

    base.read_json = read_json
    base.frozen_inputs = lambda: (
        {"case_id": "case"},
        {"immutable_image_reference": "image@sha256:" + "a" * 64},
        {"instance_id": TASK_ID},
    )
    base.validate_plan = lambda manifest, lock: "plan-sha"
    base.collect_hashes = lambda p: {}
    base.save_state = lambda state: None
    base.utc_now = lambda: "now"
    return base


class HardeningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.saved = {name: sys.modules.get(name) for name in (
            "execute_controller",
            "validated_execute_controller",
            "validated_execute_controller_legacy",
        )}
        self.base = _base(self.root)
        sys.modules["execute_controller"] = self.base
        for name in ("validated_execute_controller", "validated_execute_controller_legacy"):
            sys.modules.pop(name, None)
        self.controller = importlib.import_module("validated_execute_controller")

    def tearDown(self) -> None:
        for name, value in self.saved.items():
            if value is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = value
        self.tmp.cleanup()

    def make_case(self, status: str, patch: object, stderr: str = ""):
        item = {
            "run_id": "v1.0.0-r1",
            "release": "v1.0.0",
            "full_commit": "commit",
            "repetition": 1,
            "trajectory_artifact": "run.traj",
            "trajectory": "trajectories/run.traj",
            "record": "runs/v1.0.0-r1/run-record.json",
            "state": "complete",
        }
        run_dir = self.base.RUNS_DIR / item["run_id"]
        output = run_dir / "sweagent-output"
        output.mkdir(parents=True)
        (output / "run_batch_exit_statuses.yaml").write_text(
            f"instances_by_exit_status:\n  {status}:\n    - {TASK_ID}\n",
            encoding="utf-8",
        )
        (output / f"{TASK_ID}.pred").write_text(
            json.dumps({"instance_id": TASK_ID, "model_patch": patch}),
            encoding="utf-8",
        )
        (run_dir / "stdout.log").write_text("", encoding="utf-8")
        (run_dir / "stderr.log").write_text(stderr, encoding="utf-8")
        self.base.write_json(run_dir / "run-record.json", {
            "schema": "far-swe-agent-run-record/1.2",
            "run_id": item["run_id"], "release": item["release"],
            "commit": item["full_commit"], "repetition": 1,
            "task_id": TASK_ID, "state": "complete", "returncode": 0,
            "benchmark_outcomes_accessed": False,
        })
        return item, self.controller._classify_preserved_run(item, TASK_ID)

    def test_retryable_failure_does_not_require_completion_artifacts(self) -> None:
        _item, (_record, outcome) = self.make_case(
            "exit_error", None, "HTTP 429 RESOURCE_EXHAUSTED request-per-day"
        )
        self.assertEqual(outcome.state, "failed_retryable")
        self.assertEqual(outcome.category, "provider_quota_exhaustion")

    def test_success_without_trajectory_is_terminal(self) -> None:
        _item, (_record, outcome) = self.make_case("submitted", "patch")
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("completion provenance", outcome.reason)


if __name__ == "__main__":
    unittest.main()
