"""The canonical merge test suite must include every security-relevant product regression surface."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "run_tests.py"


class CanonicalTestScopeTests(unittest.TestCase):
    def test_decision_integrity_semantic_tests_are_canonical(self) -> None:
        spec = importlib.util.spec_from_file_location("far_canonical_test_runner", RUNNER)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        relative = {path.relative_to(ROOT).as_posix() for path in module.TEST_ROOTS}
        self.assertIn("tests", relative)
        self.assertIn("commercial/far-decision-integrity/tests", relative)


if __name__ == "__main__":
    unittest.main()
