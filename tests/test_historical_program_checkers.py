"""Runs historical checkers that nothing else invokes.

tools/check_post_terminal_public_evaluation.py runs tests/test_post_terminal_public_evaluation.py
itself, so the call lives here rather than in that module (which would recurse).
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class HistoricalProgramCheckerTest(unittest.TestCase):
    def test_superseded_post_terminal_program_checker_passes(self):
        completed = subprocess.run(
            [sys.executable, "tools/check_post_terminal_public_evaluation.py"],
            cwd=ROOT, capture_output=True, text=True, timeout=300,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
