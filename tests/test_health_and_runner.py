from __future__ import annotations
import json, os, subprocess, sys, tempfile, unittest
from unittest.mock import patch
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import common_health, repo_health_check, run_tests
class HealthAndRunnerTests(unittest.TestCase):
    def test_complete_suite_budget_matches_canonical_profile_and_overrides_remain_effective(self):
        manifest=json.loads((ROOT/'validation/manifest.json').read_text())
        expected=next(c['timeout_seconds'] for c in manifest['checks'] if c['id']=='tests.canonical')
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(repo_health_check.check_timeout('canonical tests',None),expected)
            self.assertEqual(repo_health_check.check_timeout('individual check',None),common_health.DEFAULT_HEALTH_TIMEOUT_SECONDS)
            self.assertEqual(repo_health_check.check_timeout('canonical tests',7),7)
        with patch.dict(os.environ, {'PROJECT_FAR_HEALTH_TIMEOUT':'17'}):
            self.assertEqual(repo_health_check.check_timeout('canonical tests',None),17)
            self.assertEqual(repo_health_check.check_timeout('individual check',None),17)
            self.assertEqual(repo_health_check.check_timeout('canonical tests',7),7)
    def test_run_success(self):
        cp=common_health.run([sys.executable,'-c','print("ok")'],timeout=5); self.assertEqual(cp.returncode,0); self.assertIn('ok',cp.stdout)
    def test_run_nonzero(self):
        cp=common_health.run([sys.executable,'-c','print("bad"); raise SystemExit(7)'],timeout=5); self.assertEqual(cp.returncode,7); self.assertIn('bad',cp.stdout)
    def test_run_timeout_with_partial_output(self):
        cp=common_health.run([sys.executable,'-c','import time; print("before", flush=True); time.sleep(5)'],timeout=1); self.assertEqual(cp.returncode,124); self.assertIn('TIMEOUT after 1 seconds',cp.stdout); self.assertIn('before',cp.stdout)
    def test_missing_command(self):
        with self.assertRaises(FileNotFoundError): common_health.run(['definitely-missing-project-far-command'],timeout=1)
    def test_runner_discovers_nonzero_tests(self):
        self.assertGreater(run_tests.count_tests(run_tests.discover_suite()),0)
    def test_zero_test_detection(self):
        with tempfile.TemporaryDirectory() as td:
            suite=run_tests.discover_suite(Path(td)); self.assertEqual(run_tests.count_tests(suite),0)
    def test_optional_warning_check_simulation(self):
        cp=common_health.run([sys.executable,'-c','raise SystemExit(3)'],timeout=5); self.assertNotEqual(cp.returncode,0)
    def test_required_failing_check_simulation(self):
        cp=common_health.run([sys.executable,'-c','raise SystemExit(2)'],timeout=5); self.assertEqual(cp.returncode,2)
