from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from tools import check_repository_truth as truth

ROOT = Path(__file__).resolve().parents[1]


class RepositoryTruthTests(unittest.TestCase):
    def test_checker_passes_current_repository(self) -> None:
        completed = subprocess.run(
            [sys.executable, "tools/check_repository_truth.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["successful"])
        self.assertEqual(payload["package_version"], "0.6.0")
        self.assertEqual(payload["latest_release"], "v1.0.0")
        self.assertEqual(payload["governing_core"], "PROJECT-FAR-CORE-THEORY-1.0")
        self.assertEqual(payload["current_program"], "POST-CLOSURE-001")
        self.assertEqual(payload["current_phase"], "post-closure assurance and application")

    def test_version_drift_fails_closed(self) -> None:
        original = truth.read_text

        def mutated(path: str) -> str:
            text = original(path)
            if path.endswith("__init__.py"):
                return text.replace('__version__ = "0.6.0"', '__version__ = "9.9.9"')
            return text

        with mock.patch.object(truth, "read_text", side_effect=mutated):
            with self.assertRaises(SystemExit) as caught:
                truth.main()
        self.assertIn("package version drift", str(caught.exception))

    def test_historical_dashboard_cannot_be_current(self) -> None:
        original = truth.read_text

        def mutated(path: str) -> str:
            text = original(path)
            if path == "README.md":
                return text + "\nCurrent project phase: W3.5\n"
            return text

        with mock.patch.object(truth, "read_text", side_effect=mutated):
            with self.assertRaises(SystemExit) as caught:
                truth.main()
        self.assertIn("historical W3.5 dashboard", str(caught.exception))

    def test_release_badge_tag_pin_fails_closed(self) -> None:
        original = truth.read_text

        def mutated(path: str) -> str:
            text = original(path)
            if path == "README.md":
                return text.replace(
                    "](https://github.com/notfoundout/Project-FAR/releases/latest)\n",
                    "](https://github.com/notfoundout/Project-FAR/releases/tag/v1.0.0)\n",
                    1,
                )
            return text

        with mock.patch.object(truth, "read_text", side_effect=mutated):
            with self.assertRaises(SystemExit) as caught:
                truth.main()
        self.assertIn("latest-release route", str(caught.exception))

    def test_release_badge_version_drift_fails_closed(self) -> None:
        original = truth.read_text

        def mutated(path: str) -> str:
            text = original(path)
            if path == "README.md":
                return text.replace("Release v1.0.0", "Release v0.4.0", 1)
            return text

        with mock.patch.object(truth, "read_text", side_effect=mutated):
            with self.assertRaises(SystemExit) as caught:
                truth.main()
        self.assertIn("release badge drift", str(caught.exception))

    def test_release_record_drift_fails_closed(self) -> None:
        original = truth.read_text

        def mutated(path: str) -> str:
            text = original(path)
            if path == "docs/releases/project-far-v1.0.0.md":
                return text.replace("v1.0.0", "v0.4.0")
            return text

        with mock.patch.object(truth, "read_text", side_effect=mutated):
            with self.assertRaises(SystemExit) as caught:
                truth.main()
        self.assertIn("release record", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
