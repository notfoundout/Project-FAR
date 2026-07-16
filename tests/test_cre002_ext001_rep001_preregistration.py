from __future__ import annotations
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CRE002EXT001REP001PreregistrationTests(unittest.TestCase):
    def test_preregistration_checker(self):
        result = subprocess.run(
            [sys.executable, 'tools/check_cre002_ext001_rep001_preregistration.py'],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('PREREGISTRATION CHECK PASSED', result.stdout)

    def test_parent_result_is_not_copied_into_replication_package(self):
        package = ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001'
        self.assertFalse((package / 'generated').exists())
        self.assertFalse((package / 'results').exists())
        self.assertFalse((package / 'submissions').exists())


if __name__ == '__main__':
    unittest.main()
