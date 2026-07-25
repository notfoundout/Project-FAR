from __future__ import annotations

import unittest
from pathlib import Path

CASE_DIR = Path(__file__).parent


class ValidatedExecutionSmokeContractTests(unittest.TestCase):
    def test_rehearsal_uses_validated_controller(self) -> None:
        text = (CASE_DIR / "rehearse_execute_boundary.py").read_text(encoding="utf-8")
        self.assertIn("import execute_controller as base", text)
        self.assertIn("import validated_execute_controller as controller", text)
        self.assertIn("controller.execute_one", text)
        self.assertIn("EXPECTED_CONTROLLER_RETURN = 75", text)
        self.assertIn("provider_quota_exhaustion", text)
        self.assertNotIn("import execute_controller as controller", text)


if __name__ == "__main__":
    unittest.main()
