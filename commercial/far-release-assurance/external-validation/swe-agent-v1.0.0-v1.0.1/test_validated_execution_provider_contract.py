from __future__ import annotations

import hashlib
import json
import tempfile
import types
import unittest
from pathlib import Path

import execution_outcome as base
from validated_execution_prediction_contract import classify_execution as prediction_classifier
from validated_execution_provider_contract import wrap_classifier
from validated_execution_reclassification import install as install_reclassification

TASK_ID = "scikit-learn__scikit-learn-14125"


class ProviderClassificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.output = Path(self.tmp.name)
        (self.output / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status:\n"
            "  exit_error:\n"
            f"    - {TASK_ID}\n"
            "total_cost: 0\n",
            encoding="utf-8",
        )
        target = self.output / TASK_ID
        target.mkdir()
        (target / f"{TASK_ID}.pred").write_text(
            json.dumps({"instance_id": TASK_ID, "model_patch": None}),
            encoding="utf-8",
        )
        (self.output / "preds.json").write_text(
            json.dumps({TASK_ID: {"instance_id": TASK_ID, "model_patch": ""}}),
            encoding="utf-8",
        )
        self.classify = wrap_classifier(prediction_classifier)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def outcome(self, stdout: str, stderr: str = ""):
        return self.classify(
            outer_returncode=0,
            swe_output=self.output,
            task_id=TASK_ID,
            stdout=stdout,
            stderr=stderr,
            allow_no_change=False,
        )

    def test_model_unavailable_to_new_users_is_terminal(self) -> None:
        outcome = self.outcome(
            "DockerDeploymentConfig(startup_timeout=180.0)\n"
            "Client error '404 Not Found' for url "
            "'https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.5-pro:generateContent'\n"
            '"message": "This model models/gemini-2.5-pro is no longer '
            'available to new users.", "status": "NOT_FOUND"'
        )
        self.assertEqual(outcome.category, "provider_model_unavailable")
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertFalse(outcome.retryable)

    def test_benign_startup_timeout_configuration_is_not_retryable(self) -> None:
        outcome = self.outcome(
            "DockerDeploymentConfig(startup_timeout=180.0, pull='missing')"
        )
        self.assertEqual(outcome.category, "terminal_agent_error")
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertFalse(outcome.retryable)

    def test_real_http_503_remains_retryable(self) -> None:
        outcome = self.outcome("litellm API error: HTTP 503 service unavailable")
        self.assertEqual(outcome.category, "retryable_provider_error")
        self.assertEqual(outcome.state, "failed_retryable")
        self.assertTrue(outcome.retryable)

    def test_quota_failure_remains_retryable(self) -> None:
        outcome = self.outcome("HTTP 429 RESOURCE_EXHAUSTED quota exceeded")
        self.assertEqual(outcome.category, "provider_quota_exhaustion")
        self.assertEqual(outcome.state, "failed_retryable")
        self.assertTrue(outcome.retryable)

    def test_validated_success_still_outranks_earlier_provider_text(self) -> None:
        (self.output / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status:\n"
            "  submitted:\n"
            f"    - {TASK_ID}\n",
            encoding="utf-8",
        )
        target = self.output / TASK_ID
        (target / f"{TASK_ID}.pred").write_text(
            json.dumps({"instance_id": TASK_ID, "model_patch": "patch-a"}),
            encoding="utf-8",
        )
        (self.output / "preds.json").write_text(
            json.dumps(
                {TASK_ID: {"instance_id": TASK_ID, "model_patch": "patch-a"}}
            ),
            encoding="utf-8",
        )
        outcome = self.outcome(
            "earlier request: 404 Not Found for "
            "models/gemini-2.5-pro:generateContent"
        )
        self.assertEqual(outcome.category, "success_with_patch")
        self.assertEqual(outcome.state, "complete")


class ProviderReclassificationTests(unittest.TestCase):
    def test_retryable_model_unavailability_is_reclassified_terminal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "execution-output"
            runs = output / "runs"
            run_dir = runs / "v1.0.0-r1"
            run_dir.mkdir(parents=True)
            record_path = run_dir / "run-record.json"
            record = {"state": "failed_retryable"}
            record_path.write_text(json.dumps(record), encoding="utf-8")
            saved: list[dict] = []

            def write_json(path: Path, value: object) -> None:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")

            def sha256_file(path: Path) -> str:
                return hashlib.sha256(path.read_bytes()).hexdigest()

            terminal = base.ExecutionOutcome(
                "provider_model_unavailable",
                "failed_terminal",
                False,
                "exit_error",
                False,
                False,
                "the frozen model endpoint is unavailable to this API project",
                {"provider_classification_signal": "not available to new users"},
            )
            base_namespace = types.SimpleNamespace(
                OUTPUT_DIR=output,
                RUNS_DIR=runs,
                utc_now=lambda: "2026-07-26T04:00:00+00:00",
                write_json=write_json,
                sha256_file=sha256_file,
                collect_hashes=lambda path: {
                    str(item.relative_to(path)): sha256_file(item)
                    for item in path.rglob("*")
                    if item.is_file()
                },
                save_state=lambda state: saved.append(json.loads(json.dumps(state))),
            )
            core = types.SimpleNamespace(
                base=base_namespace,
                reconcile_completed_runs=lambda state, task_id: False,
                _record_path=lambda run: record_path,
                _classify_preserved_run=lambda run, task_id: (record, terminal),
                _clear_completion_metadata=lambda run: (
                    run.pop("completed_at", None),
                    run.pop("trajectory_sha256", None),
                ),
            )
            install_reclassification(core)
            state = {
                "runs": [
                    {
                        "run_id": "v1.0.0-r1",
                        "state": "failed_retryable",
                        "attempts": 3,
                        "outcome_category": "retryable_provider_error",
                    },
                    {"run_id": "v1.0.0-r2", "state": "pending", "attempts": 0},
                ],
                "corrections": [],
            }

            self.assertTrue(core.reconcile_completed_runs(state, TASK_ID))
            run = state["runs"][0]
            self.assertEqual(run["state"], "failed_terminal")
            self.assertEqual(run["outcome_category"], "provider_model_unavailable")
            self.assertEqual(run["corrected_from"], "failed_retryable")
            self.assertEqual(len(state["corrections"]), 1)
            self.assertEqual(len(saved), 1)


if __name__ == "__main__":
    unittest.main()
