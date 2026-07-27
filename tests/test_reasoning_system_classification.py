"""Regression tests for accepted reasoning-system boundary classifications."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from evaluate_reasoning_systems import classify_fixture  # noqa: E402


class ReasoningSystemClassificationTests(unittest.TestCase):
    def assert_fixture_classification(self, fixture: str, expected: str) -> None:
        result = classify_fixture(
            ROOT / "examples" / "far" / "reasoning-systems" / f"{fixture}.far.yaml"
        )
        self.assertEqual(result.classification, expected)
        self.assertTrue(result.primitive_mapping_complete)

    def test_inconsistent_calculus_is_a_conservative_extension(self) -> None:
        self.assert_fixture_classification("inconsistent-calculus", "extends FAR")

    def test_opaque_oracle_is_outside_far_scope(self) -> None:
        self.assert_fixture_classification("opaque-oracle-reasoning", "outside FAR scope")

    def test_paradox_is_a_conservative_extension(self) -> None:
        self.assert_fixture_classification("paradox", "extends FAR")


if __name__ == "__main__":
    unittest.main()
