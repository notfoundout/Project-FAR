"""Regression tests for accepted reasoning-system boundary classifications."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from evaluate_reasoning_systems import classify_fixture  # noqa: E402


EXPECTED_BOUNDARIES = {
    "inconsistent-calculus": ("PS-011", "extends FAR"),
    "opaque-oracle-reasoning": ("PS-013", "outside FAR scope"),
    "paradox": ("PS-010", "extends FAR"),
}


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

    def test_evidence_registry_matches_fixture_classifications(self) -> None:
        registry = yaml.safe_load(
            (ROOT / "theory" / "evaluation" / "evidence-registry.yaml").read_text(
                encoding="utf-8"
            )
        )
        entries = {entry["id"]: entry for entry in registry["entries"]}

        for fixture, (entry_id, expected) in EXPECTED_BOUNDARIES.items():
            with self.subTest(fixture=fixture):
                result = classify_fixture(
                    ROOT / "examples" / "far" / "reasoning-systems" / f"{fixture}.far.yaml"
                )
                self.assertEqual(entries[entry_id]["classification"], expected)
                self.assertEqual(entries[entry_id]["classification"], result.classification)

    def test_primitive_sufficiency_report_has_no_stale_candidates(self) -> None:
        report = (
            ROOT / "docs" / "reports" / "primitive-sufficiency-report.md"
        ).read_text(encoding="utf-8")
        self.assertIn("- Candidate counterexamples: 0", report)
        self.assertIn("## Candidate Counterexamples\n\nNone.", report)
        self.assertNotIn("- PS-010:", report.split("## Candidate Counterexamples", 1)[1].split("## Reconciled Boundary Cases", 1)[0])
        self.assertNotIn("- PS-011:", report.split("## Candidate Counterexamples", 1)[1].split("## Reconciled Boundary Cases", 1)[0])
        self.assertNotIn("- PS-013:", report.split("## Candidate Counterexamples", 1)[1].split("## Reconciled Boundary Cases", 1)[0])


if __name__ == "__main__":
    unittest.main()
