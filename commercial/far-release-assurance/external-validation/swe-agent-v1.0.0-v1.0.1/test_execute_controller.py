from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import execute_controller as controller


class ExecuteControllerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.case = self.root / "case"
        self.case.mkdir()
        self.output = self.case / "execution-output"
        self.environment = self.case / "environment-freeze"
        self.environment.mkdir()
        self.config = self.case / "agent-config.yaml"
        self.config.write_text("agent:\n  model:\n    name: gemini/gemini-2.5-pro\n", encoding="utf-8")
        self.task = {
            "instance_id": "scikit-learn__scikit-learn-14125",
            "repo": "scikit-learn/scikit-learn",
            "base_commit": "c0c53137cec61a4d6cd72d8a43bbe0321476e440",
            "problem_statement": "Public problem only",
            "outcome_fields_included": False,
            "redacted_fields": ["patch", "test_patch", "FAIL_TO_PASS", "PASS_TO_PASS"],
        }
        controller.write_json(self.environment / "task-record.public.json", self.task)
        self.lock = {
            "task_id": self.task["instance_id"],
            "swebench_harness_commit": "f7bbbb2ccdf479001d6467c9e34af59e44a840f9",
            "immutable_image_reference": "ghcr.io/notfoundout/image@sha256:" + "b" * 64,
            "registry_repository": "ghcr.io/notfoundout/image",
            "registry_digest": "sha256:" + "b" * 64,
            "file_sha256": {
                "task-record.public.json": controller.sha256_file(self.environment / "task-record.public.json")
            },
            "outcome_data_exported": False,
            "model_call_started": False,
        }
        controller.write_json(self.environment / "environment-lock.json", self.lock)
        self.runs = [
            {"release": "v1.0.0", "commit": "8ed382c", "repetition": 1, "trajectory_artifact": "baseline-run-1.traj"},
            {"release": "v1.0.0", "commit": "8ed382c", "repetition": 2, "trajectory_artifact": "baseline-run-2.traj"},
            {"release": "v1.0.1", "commit": "6aff215", "repetition": 1, "trajectory_artifact": "candidate-run-1.traj"},
            {"release": "v1.0.1", "commit": "6aff215", "repetition": 2, "trajectory_artifact": "candidate-run-2.traj"},
        ]
        self.manifest = {
            "case_id": "swe-agent-v1.0.0-v1.0.1",
            "status": "execution_inputs_frozen",
            "frozen_inputs": {
                "task_id": self.task["instance_id"],
                "model": "gemini/gemini-2.5-pro",
                "environment_lock_sha256": controller.sha256_file(self.environment / "environment-lock.json"),
                "agent_config_sha256": controller.sha256_file(self.config),
            },
            "execution_requirements": {"runs": self.runs},
        }
        controller.write_json(self.case / "manifest.json", self.manifest)
        self.plan_path = self.output / "execution-plan.json"
        self.state_path = self.output / "execution-state.json"
        self.paths = patch.multiple(
            controller,
            CASE_DIR=self.case,
            MANIFEST_PATH=self.case / "manifest.json",
            LOCK_PATH=self.environment / "environment-lock.json",
            TASK_PATH=self.environment / "task-record.public.json",
            CONFIG_PATH=self.config,
            OUTPUT_DIR=self.output,
            PLAN_PATH=self.plan_path,
            STATE_PATH=self.state_path,
            TRAJECTORY_DIR=self.output / "trajectories",
            RUNS_DIR=self.output / "runs",
        )
        self.paths.start()
        self.write_valid_plan()
        self.plan_hash = controller.sha256_file(self.plan_path)

    def tearDown(self) -> None:
        self.paths.stop()
        self.tmp.cleanup()

    def write_valid_plan(self) -> None:
        plan_runs = []
        for item in self.runs:
            plan_runs.append({
                **item,
                "workspace": f"workspaces/{item['release']}-run-{item['repetition']}",
                "trajectory": f"trajectories/{item['trajectory_artifact']}",
                "outcomes_accessible": False,
                "state": "pending",
            })
        controller.write_json(self.plan_path, {
            "schema": "far-external-execution-plan/0.4",
            "case_id": self.manifest["case_id"],
            "manifest_sha256": controller.sha256_file(self.case / "manifest.json"),
            "agent_config_sha256": controller.sha256_file(self.config),
            "environment_lock_sha256": controller.sha256_file(self.environment / "environment-lock.json"),
            "immutable_image_reference": self.lock["immutable_image_reference"],
            "registry_digest": self.lock["registry_digest"],
            "task_id": self.task["instance_id"],
            "model": self.manifest["frozen_inputs"]["model"],
            "maximum_model_cost_usd": 0.0,
            "sequential_only": True,
            "runs": plan_runs,
        })

    def test_frozen_inputs_are_bound(self) -> None:
        manifest, lock, task = controller.frozen_inputs()
        self.assertEqual(manifest["case_id"], self.manifest["case_id"])
        self.assertEqual(lock["immutable_image_reference"], self.lock["immutable_image_reference"])
        self.assertFalse(task["outcome_fields_included"])

    def test_valid_plan_is_bound(self) -> None:
        self.assertEqual(controller.validate_plan(self.manifest, self.lock), self.plan_hash)

    def test_plan_drift_is_fatal(self) -> None:
        plan = json.loads(self.plan_path.read_text())
        plan["runs"][0]["commit"] = "deadbee"
        controller.write_json(self.plan_path, plan)
        with self.assertRaisesRegex(SystemExit, "plan run drift"):
            controller.validate_plan(self.manifest, self.lock)

    def test_lock_hash_drift_is_fatal(self) -> None:
        changed = json.loads((self.case / "manifest.json").read_text())
        changed["frozen_inputs"]["environment_lock_sha256"] = "0" * 64
        controller.write_json(self.case / "manifest.json", changed)
        with self.assertRaisesRegex(SystemExit, "lock hash mismatch"):
            controller.frozen_inputs()

    def test_public_task_hash_drift_is_fatal(self) -> None:
        (self.environment / "task-record.public.json").write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "task-record hash mismatch"):
            controller.frozen_inputs()

    def test_run_order_is_frozen_and_sequential(self) -> None:
        state = controller.initial_state(self.manifest, self.lock, self.plan_hash)
        self.assertEqual(controller.next_pending(state)["run_id"], "v1.0.0-r1")
        state["runs"][0]["state"] = "complete"
        self.assertEqual(controller.next_pending(state)["run_id"], "v1.0.0-r2")
        state["runs"][1]["state"] = "complete"
        self.assertEqual(controller.next_pending(state)["run_id"], "v1.0.1-r1")

    def test_running_state_retries_same_slot(self) -> None:
        state = controller.initial_state(self.manifest, self.lock, self.plan_hash)
        state["runs"][0]["state"] = "running"
        self.assertEqual(controller.next_pending(state)["run_id"], "v1.0.0-r1")

    def test_resume_rejects_manifest_drift(self) -> None:
        state = controller.initial_state(self.manifest, self.lock, self.plan_hash)
        controller.save_state(state)
        changed = json.loads((self.case / "manifest.json").read_text())
        changed["case_id"] = "changed"
        controller.write_json(self.case / "manifest.json", changed)
        with self.assertRaisesRegex(SystemExit, "schema or case mismatch"):
            controller.load_state(changed, self.lock, self.plan_hash)

    def test_resume_rejects_plan_drift(self) -> None:
        state = controller.initial_state(self.manifest, self.lock, self.plan_hash)
        controller.save_state(state)
        with self.assertRaisesRegex(SystemExit, "different execution plan"):
            controller.load_state(self.manifest, self.lock, "0" * 64)

    def test_quota_failure_classification(self) -> None:
        self.assertEqual(controller.classify_failure("", "HTTP 429 RESOURCE_EXHAUSTED"), "quota_paused")
        self.assertEqual(controller.classify_failure("bad config", ""), "failed_retryable")

    def test_instance_file_contains_no_gold_outcomes(self) -> None:
        target = self.root / "instance.json"
        controller.build_instance_file(self.task, self.lock, target)
        raw = target.read_text(encoding="utf-8")
        payload = json.loads(raw)
        self.assertEqual(payload[0]["image_name"], self.lock["immutable_image_reference"])
        self.assertEqual(payload[0]["repo_name"], "testbed")
        for forbidden in ("patch", "test_patch", "FAIL_TO_PASS", "PASS_TO_PASS"):
            self.assertNotIn(forbidden, raw)
        self.assertFalse(payload[0]["extra_fields"]["outcome_data_accessible"])

    def test_state_rejects_run_matrix_mutation(self) -> None:
        state = controller.initial_state(self.manifest, self.lock, self.plan_hash)
        state["runs"][0]["commit"] = "deadbee"
        controller.save_state(state)
        with self.assertRaisesRegex(SystemExit, "Execution state drift"):
            controller.load_state(self.manifest, self.lock, self.plan_hash)

    def test_state_rejects_completed_run_after_incomplete_run(self) -> None:
        state = controller.initial_state(self.manifest, self.lock, self.plan_hash)
        state["runs"][1]["state"] = "complete"
        controller.save_state(state)
        with self.assertRaisesRegex(SystemExit, "sequential ordering"):
            controller.load_state(self.manifest, self.lock, self.plan_hash)

    def test_secret_redaction(self) -> None:
        self.assertEqual(controller.redact("before secret after", "secret"), "before [REDACTED] after")


if __name__ == "__main__":
    unittest.main()
