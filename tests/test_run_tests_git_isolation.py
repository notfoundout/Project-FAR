"""The canonical runner isolates tests from the host's git configuration.

A developer or CI host may configure commit signing, a signing helper, hooks or other global git
settings. Tests that commit to temporary repositories must behave identically everywhere, so the
runner points git at an empty global configuration and ignores the system one.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMIT_IN_TEMPORARY_REPOSITORY = (
    "import importlib.util, subprocess, sys, tempfile\n"
    "spec = importlib.util.spec_from_file_location('far_run_tests', sys.argv[1])\n"
    "runner = importlib.util.module_from_spec(spec)\n"
    "LOAD_RUNNER\n"
    "repo = tempfile.mkdtemp()\n"
    "git = lambda *a: subprocess.run(['git', '-C', repo, *a], check=True, capture_output=True)\n"
    "git('init', '-q')\n"
    "git('-c', 'user.name=t', '-c', 'user.email=t@example.invalid', 'commit', '--allow-empty', '-qm', 'x')\n"
)


class RunnerGitIsolationTests(unittest.TestCase):
    def _commit(self, *, load_runner: bool) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            # A hostile host configuration: every commit must be signed by a program that does not exist.
            (home / ".gitconfig").write_text(
                "[commit]\n\tgpgsign = true\n[gpg]\n\tprogram = /nonexistent/far-hostile-signer\n", encoding="utf-8"
            )
            script = COMMIT_IN_TEMPORARY_REPOSITORY.replace(
                "LOAD_RUNNER", "spec.loader.exec_module(runner)" if load_runner else "pass"
            )
            env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(home)}
            return subprocess.run(
                [sys.executable, "-c", script, str(ROOT / "tools" / "run_tests.py")],
                env=env, capture_output=True, text=True, check=False,
            )

    def test_host_git_configuration_does_not_reach_tests(self) -> None:
        completed = self._commit(load_runner=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_control_the_same_commit_fails_without_isolation(self) -> None:
        self.assertNotEqual(self._commit(load_runner=False).returncode, 0)


if __name__ == "__main__":
    unittest.main()
