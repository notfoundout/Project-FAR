from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001'


class TestCre002Ext001ExecutionAuthorization(unittest.TestCase):
    def load(self, name: str) -> dict:
        return json.loads((PKG / name).read_text())

    def test_authorization_is_administrative_only(self):
        manifest = self.load('package-manifest.json')
        lock = self.load('execution-lock.json')
        audit = self.load('execution-unlock-audit.json')

        self.assertEqual(manifest['status'], 'execution-authorized')
        self.assertTrue(manifest['execution_permitted'])
        self.assertTrue(manifest['compiler_implementation_permitted'])
        self.assertFalse(manifest['official_results_present'])
        self.assertEqual(lock['authorization_status'], 'authorized')
        self.assertTrue(lock['execution_permitted'])
        self.assertTrue(lock['compiler_implementation_permitted'])
        self.assertFalse(lock['official_results_present'])
        self.assertTrue(audit['immutable_package_lock_verified'])
        self.assertFalse(audit['scientific_results_created_by_unlock'])
        self.assertTrue(all(value is False for value in audit['pre_unlock_checks'].values()))

    def test_scientific_checksum_lock_still_passes(self):
        cp = subprocess.run(
            [sys.executable, 'tools/check_cre002_ext001_checksums.py'],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)

    def test_preregistration_checker_accepts_reviewed_unlock(self):
        cp = subprocess.run(
            [sys.executable, 'tools/check_cre002_ext001_preregistration.py'],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)


if __name__ == '__main__':
    unittest.main()
