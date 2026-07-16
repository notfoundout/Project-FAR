from __future__ import annotations
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CRE002PreregistrationTest(unittest.TestCase):
    def test_preregistration_package_is_locked_and_complete(self) -> None:
        result = subprocess.run(
            [sys.executable, "tools/check_cre002_preregistration.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CRE-002 PREREGISTRATION CHECK PASSED", result.stdout)


if __name__ == "__main__":
    unittest.main()
