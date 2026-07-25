from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from execution_outcome import read_prediction

TASK_ID = "target-task"


class PredictionFileScanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.output = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, name: str, instance_id: str, patch: str) -> None:
        (self.output / name).write_text(
            json.dumps(
                {"instance_id": instance_id, "model_patch": patch}
            ),
            encoding="utf-8",
        )

    def test_noncanonical_target_prediction_is_detected(self) -> None:
        self.write(f"{TASK_ID}.pred", TASK_ID, "patch-a")
        self.write("other.pred", TASK_ID, "patch-b")

        with self.assertRaisesRegex(
            ValueError, "multiple .pred files identify the target instance"
        ):
            read_prediction(self.output, TASK_ID)

    def test_duplicate_target_prediction_is_rejected_even_when_consistent(self) -> None:
        self.write(f"{TASK_ID}.pred", TASK_ID, "same-patch")
        self.write("duplicate.pred", TASK_ID, "same-patch")

        with self.assertRaisesRegex(
            ValueError, "multiple .pred files identify the target instance"
        ):
            read_prediction(self.output, TASK_ID)

    def test_unrelated_prediction_is_ignored(self) -> None:
        self.write(f"{TASK_ID}.pred", TASK_ID, "target-patch")
        self.write("other.pred", "other-task", "other-patch")

        patch, no_change, evidence = read_prediction(self.output, TASK_ID)

        self.assertEqual(patch, "target-patch")
        self.assertFalse(no_change)
        self.assertNotIn("other.pred", evidence)

    def test_malformed_noncanonical_target_prediction_is_rejected(self) -> None:
        self.write(f"{TASK_ID}.pred", TASK_ID, "target-patch")
        (self.output / "other.pred").write_text(
            json.dumps({"instance_id": TASK_ID, "unexpected": "value"}),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "missing model_patch"):
            read_prediction(self.output, TASK_ID)


if __name__ == "__main__":
    unittest.main()
