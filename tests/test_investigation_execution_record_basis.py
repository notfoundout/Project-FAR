#!/usr/bin/env python3
"""Regression coverage for basis-only substantive evidence-closure records."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.check_investigation_execution import _validate_recorded_list


class EvidenceClosureRecordBasisTests(unittest.TestCase):
    def test_explicit_basis_allows_empty_evidence_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            errors: list[str] = []
            _validate_recorded_list(
                closure={
                    "strongest_support": [
                        {
                            "id": "SUP-1",
                            "statement": "The support record is justified directly by the stated basis.",
                            "basis": "No separate repository artifact is required for this bounded record.",
                            "evidence": [],
                        }
                    ]
                },
                field="strongest_support",
                investigation="VI-RECORD-BASIS",
                root=Path(tmp),
                errors=errors,
            )
            self.assertEqual(errors, [])

    def test_empty_evidence_without_basis_still_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            errors: list[str] = []
            _validate_recorded_list(
                closure={
                    "strongest_support": [
                        {
                            "id": "SUP-1",
                            "statement": "A record without either permitted support route.",
                            "evidence": [],
                        }
                    ]
                },
                field="strongest_support",
                investigation="VI-RECORD-BASIS",
                root=Path(tmp),
                errors=errors,
            )
            self.assertIn(
                "VI-RECORD-BASIS: evidence_closure.strongest_support[1] requires a non-empty basis or evidence",
                errors,
            )


if __name__ == "__main__":
    unittest.main()
