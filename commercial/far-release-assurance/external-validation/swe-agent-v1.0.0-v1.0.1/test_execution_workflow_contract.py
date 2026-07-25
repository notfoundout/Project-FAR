from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
WORKFLOW = ROOT / ".github/workflows/far-swe-agent-execution.yml"


class ExecutionWorkflowContractTests(unittest.TestCase):
    def test_restore_step_invokes_case_local_planner(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        match = re.search(
            r"- name: Restore latest validated execution state\n(?P<body>.*?)(?=\n\s*- name: Resolve next frozen SWE-agent release)",
            text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match, "restore step is missing")
        body = match.group("body")
        self.assertIn('python "$CASE_DIR/run_comparison.py" plan', body)
        self.assertNotRegex(body, r"(?m)^\s*python run_comparison\.py plan\s*$")

    def test_contract_runs_before_any_model_execution(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        validation = text.index("- name: Validate manifest and regression tests")
        execution = text.index("- name: Execute exactly one next frozen run")
        self.assertLess(validation, execution)
        self.assertIn("test_execution_workflow_contract.py", text[validation:execution])


if __name__ == "__main__":
    unittest.main()
