"""Regression guards for root-of-trust audit repairs that had no failing test of their own.

See docs/audits/root-of-trust-audit-2026-09.md. Each test fails if its repair is reverted.
"""
from __future__ import annotations

import io
import re
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import run_tests  # noqa: E402

MODULE = '''
def test_passes():
    pass

def test_fails():
    assert False, "module-level failure"

async def test_async():
    assert False

def test_generator():
    assert False
    yield
'''


class ModuleLevelTestFunctionTests(unittest.TestCase):
    def _run(self) -> unittest.TestResult:
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "test_module_functions_probe.py").write_text(MODULE, encoding="utf-8")
            suite = run_tests.discover_suite(Path(directory))
        self.assertEqual(run_tests.count_tests(suite), 4)
        result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
        self.assertEqual(result.testsRun, 4)
        return result

    def test_failing_module_level_function_is_collected_and_fails(self) -> None:
        failed = {test.id().rsplit(".", 1)[-1] for test, _ in self._run().failures}
        self.assertIn("test_fails", failed)

    def test_async_and_generator_functions_fail_instead_of_passing_unexecuted(self) -> None:
        errors = {test.id().rsplit(".", 1)[-1]: text for test, text in self._run().errors}
        self.assertEqual(set(errors), {"test_async", "test_generator"})
        for text in errors.values():
            self.assertIn("async and generator test functions are not supported", text)


class LocalValidationBypassesCacheTests(unittest.TestCase):
    def test_every_make_validate_recipe_passes_no_cache(self) -> None:
        recipes = [line.strip() for line in (ROOT / "Makefile").read_text(encoding="utf-8").splitlines()
                   if "far_validation validate" in line]
        self.assertGreaterEqual(len(recipes), 4)
        self.assertEqual([line for line in recipes if "--no-cache" not in line.split()], [])


class TeePipelinesFailClosedTests(unittest.TestCase):
    def test_every_workflow_step_piping_into_tee_runs_with_pipefail(self) -> None:
        # GitHub's default shell is `bash -e` without pipefail, so `validator | tee log` exits with
        # tee's status. An explicit `shell: bash` adds `-o pipefail`.
        unguarded, seen = [], 0
        for path in sorted((ROOT / ".github" / "workflows").glob("*.y*ml")):
            workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
            workflow_shell = ((workflow.get("defaults") or {}).get("run") or {}).get("shell")
            for job_id, job in (workflow.get("jobs") or {}).items():
                job_shell = ((job.get("defaults") or {}).get("run") or {}).get("shell")
                for step in job.get("steps") or []:
                    script = step.get("run")
                    if not isinstance(script, str) or not re.search(r"(?<!\|)\|\s*tee\b", script):
                        continue
                    seen += 1
                    shell = step.get("shell") or job_shell or workflow_shell
                    if shell != "bash" and "pipefail" not in script:
                        unguarded.append(f"{path.name}:{job_id}:{step.get('name')}")
        self.assertGreater(seen, 0)
        self.assertEqual(unguarded, [])


if __name__ == "__main__":
    unittest.main()
