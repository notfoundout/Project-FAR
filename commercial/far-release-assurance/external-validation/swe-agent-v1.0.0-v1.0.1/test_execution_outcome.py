from __future__ import annotations

import json
import tempfile
import unittest
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
            "instances_by_exit_status:\n" + f"  {status}:\n" + f"    - {TASK_ID}\n" + "total_cost: 0\n",
            encoding="utf-8",
        )

    def write_prediction(self, patch: object, no_change: bool = False) -> None:
        payload = {"instance_id": TASK_ID, "model_patch": patch, "no_change": no_change}
        (self.output / f"{TASK_ID}.pred").write_text(json.dumps(payload), encoding="utf-8")

    def classify(self, rc: int = 0, stdout: str = "", stderr: str = "", allow_no_change: bool = False):
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
        outcome = self.classify(stderr="RESOURCE_EXHAUSTED request-per-minute request-per-day input-token-per-day")
        self.assertEqual(outcome.category, "provider_quota_exhaustion")
        self.assertEqual(outcome.state, "failed_retryable")
        self.assertTrue(outcome.retryable)
        self.assertFalse(outcome.patch_present)

    def test_outer_zero_internal_exit_error_without_provider_signal_is_terminal(self) -> None:
        self.write_status("exit_error")
        self.write_prediction("")
        outcome = self.classify()
        self.assertEqual(outcome.category, "terminal_agent_error")
        self.assertEqual(outcome.state, "failed_terminal")

    def test_success_requires_non_empty_patch(self) -> None:
        self.write_status("submitted")
        self.write_prediction("non-empty patch")
        outcome = self.classify()
        self.assertEqual(outcome.category, "success_with_patch")
        self.assertEqual(outcome.state, "complete")

    def test_success_status_with_empty_patch_is_rejected(self) -> None:
        self.write_status("submitted")
        self.write_prediction("")
        self.assertEqual(self.classify().state, "failed_terminal")

    def test_no_change_requires_explicit_protocol_permission(self) -> None:
        self.write_status("submitted")
        self.write_prediction("", no_change=True)
        self.assertEqual(self.classify(allow_no_change=False).state, "failed_terminal")
        self.assertEqual(self.classify(allow_no_change=True).category, "valid_no_change")

    def test_missing_target_instance_is_terminal(self) -> None:
        (self.output / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status:\n  submitted:\n    - another-task\n",
            encoding="utf-8",
        )
        self.write_prediction("non-empty patch")
        outcome = self.classify()
        self.assertEqual(outcome.state, "failed_terminal")
        self.assertIn("exactly one", outcome.reason)


if __name__ == "__main__":
    unittest.main()
