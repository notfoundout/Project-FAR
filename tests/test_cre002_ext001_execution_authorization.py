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

    def test_unlock_audit_remains_administrative_only_after_execution(self):
        manifest = self.load('package-manifest.json')
        lock = self.load('execution-lock.json')
        audit = self.load('execution-unlock-audit.json')

        self.assertIn(manifest['status'], {'execution-authorized', 'execution-complete'})
        self.assertTrue(manifest['execution_permitted'])
        self.assertTrue(manifest['compiler_implementation_permitted'])
        self.assertEqual(lock['authorization_status'], 'authorized')
        self.assertTrue(lock['execution_permitted'])
        self.assertTrue(lock['compiler_implementation_permitted'])
        self.assertTrue(audit['immutable_package_lock_verified'])
        self.assertFalse(audit['scientific_results_created_by_unlock'])
        self.assertTrue(all(value is False for value in audit['pre_unlock_checks'].values()))

        if manifest['status'] == 'execution-complete':
            self.assertTrue(manifest['official_results_present'])
            self.assertTrue(lock['official_results_present'])
            self.assertTrue((PKG / manifest['official_result']).is_file())
        else:
            self.assertFalse(manifest['official_results_present'])
            self.assertFalse(lock['official_results_present'])

    def test_scientific_checksum_lock_still_passes(self):
        cp = subprocess.run(
            [sys.executable, 'tools/check_cre002_ext001_checksums.py'],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)

    def test_preregistration_checker_accepts_current_phase(self):
        cp = subprocess.run(
            [sys.executable, 'tools/check_cre002_ext001_preregistration.py'],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)


if __name__ == '__main__':
    unittest.main()
