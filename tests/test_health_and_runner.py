from __future__ import annotations
import subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import common_health, run_tests
class HealthAndRunnerTests(unittest.TestCase):
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
