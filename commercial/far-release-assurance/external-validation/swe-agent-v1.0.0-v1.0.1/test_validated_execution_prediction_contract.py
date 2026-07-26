from __future__ import annotations

import hashlib
import json
import tempfile
import types
import unittest
from pathlib import Path

import execution_outcome as base
from validated_execution_prediction_contract import classify_execution, read_prediction
from validated_execution_reclassification import install as install_reclassification

TASK_ID = "scikit-learn__scikit-learn-14125"


class ValidatedPredictionContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.output = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_status(self, status: str) -> None:
        (self.output / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status:\n"
            f"  {status}:\n"
            f"    - {TASK_ID}\n"
            "total_cost: 0\n",
            encoding="utf-8",
        )

    def write_native_prediction_pair(
        self, per_instance_patch: str | None, aggregate_patch: str | None
    ) -> None:
        nested = self.output / TASK_ID
        nested.mkdir()
        (nested / f"{TASK_ID}.pred").write_text(
            json.dumps(
                {
                    "model_name_or_path": "sweagent-output",
                    "instance_id": TASK_ID,
                    "model_patch": per_instance_patch,
                }
            ),
            encoding="utf-8",
        )
        (self.output / "preds.json").write_text(
            json.dumps(
                {
                    TASK_ID: {
                        "model_name_or_path": "sweagent-output",
                        "instance_id": TASK_ID,
                        "model_patch": aggregate_patch,
                    }
                }
            ),
            encoding="utf-8",
        )

    def test_native_null_and_empty_prediction_pair_is_equivalent(self) -> None:
        self.write_native_prediction_pair(None, "")
        patch, no_change, evidence = read_prediction(self.output, TASK_ID)
        self.assertIsNone(patch)
        self.assertFalse(no_change)
        self.assertIn(f"{TASK_ID}.pred", evidence)
        self.assertIn("preds.json", evidence)

    def test_native_matching_patch_pair_is_equivalent(self) -> None:
        self.write_native_prediction_pair("patch-a", "patch-a")
        patch, no_change, _evidence = read_prediction(self.output, TASK_ID)
        self.assertEqual(patch, "patch-a")
        self.assertFalse(no_change)

    def test_native_conflicting_pair_is_rejected(self) -> None:
        self.write_native_prediction_pair("patch-a", "patch-b")
        with self.assertRaisesRegex(ValueError, "conflicting prediction evidence"):
            read_prediction(self.output, TASK_ID)

    def test_quota_artifact_with_native_prediction_pair_is_retryable(self) -> None:
        self.write_status("exit_error")
        self.write_native_prediction_pair(None, "")
        outcome = classify_execution(
            outer_returncode=0,
            swe_output=self.output,
            task_id=TASK_ID,
            stdout="litellm.RateLimitError HTTP 429 RESOURCE_EXHAUSTED quota exceeded",
            stderr="",
        )
        self.assertEqual(outcome.category, "provider_quota_exhaustion")
        self.assertEqual(outcome.state, "failed_retryable")
        self.assertTrue(outcome.retryable)


class EvidenceReclassificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.output = self.root / "execution-output"
        self.runs = self.output / "runs"
        self.run_dir = self.runs / "v1.0.0-r1"
        self.run_dir.mkdir(parents=True)
        self.record_path = self.run_dir / "run-record.json"
        self.record = {
            "state": "complete",
            "completed_at": "2026-07-25T19:16:34+00:00",
            "trajectory_sha256": "trajectory-hash",
        }
        self.record_path.write_text(json.dumps(self.record), encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_terminal_misclassification_is_corrected_without_overwrite(self) -> None:
        saved: list[dict] = []

        def write_json(path: Path, value: object) -> None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")

        def sha256_file(path: Path) -> str:
            return hashlib.sha256(path.read_bytes()).hexdigest()

        base_namespace = types.SimpleNamespace(
            OUTPUT_DIR=self.output,
            RUNS_DIR=self.runs,
            utc_now=lambda: "2026-07-26T02:00:00+00:00",
            write_json=write_json,
            sha256_file=sha256_file,
            collect_hashes=lambda path: {
                str(item.relative_to(path)): sha256_file(item)
                for item in path.rglob("*")
                if item.is_file()
            },
            save_state=lambda state: saved.append(json.loads(json.dumps(state))),
        )
        outcome = base.ExecutionOutcome(
            "provider_quota_exhaustion",
            "failed_retryable",
            True,
            "exit_error",
            False,
            False,
            "provider quota exhaustion detected",
            {"outer_returncode": 0},
        )
        core = types.SimpleNamespace(
            base=base_namespace,
            reconcile_completed_runs=lambda state, task_id: False,
            _record_path=lambda run: self.record_path,
            _classify_preserved_run=lambda run, task_id: (self.record, outcome),
            _clear_completion_metadata=lambda run: (
                run.pop("completed_at", None), run.pop("trajectory_sha256", None)
            ),
        )
        install_reclassification(core)
        state = {
            "runs": [
                {
                    "run_id": "v1.0.0-r1",
                    "state": "failed_terminal",
                    "attempts": 1,
                    "outcome_category": "terminal_agent_error",
                    "correction": "runs/v1.0.0-r1/run-record-correction.json",
                },
                {"run_id": "v1.0.0-r2", "state": "pending", "attempts": 0},
            ],
            "corrections": [],
        }

        self.assertTrue(core.reconcile_completed_runs(state, TASK_ID))
        run = state["runs"][0]
        self.assertEqual(run["state"], "failed_retryable")
        self.assertEqual(run["outcome_category"], "provider_quota_exhaustion")
        self.assertEqual(run["corrected_from"], "failed_terminal")
        self.assertNotEqual(
            run["correction"], "runs/v1.0.0-r1/run-record-correction.json"
        )
        self.assertTrue((self.output / run["correction"]).is_file())
        self.assertEqual(len(state["corrections"]), 1)
        self.assertEqual(
            state["corrections"][0]["previous_correction"],
            "runs/v1.0.0-r1/run-record-correction.json",
        )
        self.assertEqual(len(saved), 1)

        self.assertFalse(core.reconcile_completed_runs(state, TASK_ID))
        self.assertEqual(len(state["corrections"]), 1)
        self.assertEqual(len(saved), 1)


if __name__ == "__main__":
    unittest.main()
