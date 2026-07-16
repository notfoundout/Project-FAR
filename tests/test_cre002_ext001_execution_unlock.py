from pathlib import Path
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001'


class TestCre002Ext001ExecutionUnlock(unittest.TestCase):
    def test_checksum_lock_still_passes(self):
        cp = subprocess.run(
            [sys.executable, 'tools/check_cre002_ext001_checksums.py'],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)

    def test_authorization_is_administrative_and_results_absent(self):
        manifest = json.loads((PKG / 'package-manifest.json').read_text())
        lock = json.loads((PKG / 'execution-lock.json').read_text())
        audit = json.loads((PKG / 'execution-unlock-audit.json').read_text())
        self.assertTrue(manifest['execution_permitted'])
        self.assertTrue(manifest['compiler_implementation_permitted'])
        self.assertTrue(lock['execution_permitted'])
        self.assertTrue(lock['compiler_implementation_permitted'])
        self.assertFalse(manifest['official_results_present'])
        self.assertFalse(lock['official_results_present'])
        self.assertFalse(audit['official_results_present'])
        self.assertFalse(audit['immutable_scientific_files_modified'])
        self.assertEqual(audit['authorization_type'], 'separate-reviewed-pull-request')
        self.assertEqual(audit['preserved_prior_result'], 'CRE-002-COMPARISON-1.0')

    def test_preregistration_checker_accepts_reviewed_unlock_state(self):
        cp = subprocess.run(
            [sys.executable, 'tools/check_cre002_ext001_preregistration.py'],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)


if __name__ == '__main__':
    unittest.main()
