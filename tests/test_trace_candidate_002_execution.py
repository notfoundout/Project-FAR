from __future__ import annotations

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNNER = ROOT / "research" / "external-validation" / "trace-candidate-002" / "execute_staged.py"
WORKFLOW = ROOT / ".github" / "workflows" / "trace-candidate-002-execution.yml"


class TestTraceCandidate002Execution(unittest.TestCase):
    def test_pre_outcome_reader_excludes_outcome_columns(self):
        text = RUNNER.read_text(encoding="utf-8")
        pre = text.split("def acquire_pre_outcome", 1)[1].split("def execute_pre_outcome", 1)[0]
        self.assertIn('["filename", "trajectory", "submission"]', pre)
        self.assertNotIn('"resolved"', pre)
        self.assertNotIn('"exit_status"', pre)

    def test_reveal_requires_primary_freeze(self):
        text = RUNNER.read_text(encoding="utf-8")
        reveal = text.split("def reveal_outcome", 1)[1]
        self.assertIn("primary result must be frozen before outcome reveal", reveal)
        self.assertIn('"blind_order_preserved"', reveal)

    def test_workflow_runs_pre_outcome_twice_before_reveal(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        first = text.index("--stage pre-outcome")
        second = text.index("--stage pre-outcome", first + 1)
        reveal = text.index("--stage reveal")
        self.assertLess(first, second)
        self.assertLess(second, reveal)
        self.assertIn("diff -ru", text)


if __name__ == "__main__":
    unittest.main()
