from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001'


class CRE002EXT001REP001TeamRegistryTests(unittest.TestCase):
    def test_registry_checker(self):
        result = subprocess.run(
            [sys.executable, 'tools/check_cre002_ext001_rep001_team_registry.py'],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('TEAM REGISTRY CHECK PASSED', result.stdout)

    def test_registration_is_open_but_execution_is_locked(self):
        manifest = json.loads((PKG / 'package-manifest.json').read_text())
        control = json.loads((PKG / 'execution-lock.json').read_text())
        registry = json.loads((PKG / 'team-registry.json').read_text())
        self.assertEqual(manifest['status'], 'team-registration-open')
        self.assertTrue(manifest['team_registration_authorized'])
        self.assertTrue(control['team_registration_authorized'])
        self.assertFalse(control['execution_authorized'])
        self.assertFalse(control['compiler_implementation_authorized'])
        self.assertFalse(registry['minimum_requirements_met'])
        self.assertFalse(registry['execution_unlock_eligible'])
        self.assertEqual(registry['teams'], [])

    def test_no_fake_team_is_registered(self):
        registry = json.loads((PKG / 'team-registry.json').read_text())
        self.assertEqual(registry['eligibility_summary']['eligible_implementation_teams'], 0)
        self.assertEqual(registry['eligibility_summary']['eligible_verifier_teams'], 0)
        self.assertEqual(registry['eligibility_summary']['covered_vocabularies'], [])


if __name__ == '__main__':
    unittest.main()
