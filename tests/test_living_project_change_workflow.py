from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/living-project-change-gate.yml"


class LivingProjectChangeWorkflowTests(unittest.TestCase):
    def test_python_tools_are_invoked_as_modules(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("python -m tools.check_living_project_change_obligations", text)
        self.assertIn("python -m tools.living_implementation_contract", text)
        self.assertNotIn("python tools/check_living_project_change_obligations.py", text)
        self.assertNotIn("python tools/living_implementation_contract.py", text)


if __name__ == "__main__":
    unittest.main()
