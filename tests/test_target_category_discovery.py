from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "research/target-category-discovery/verify_sampling_design.py"
CSV_PATH = ROOT / "research/target-category-discovery/covering-array-v1.0.csv"

spec = importlib.util.spec_from_file_location("verify_sampling_design", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TargetCategorySamplingDesignTests(unittest.TestCase):
    def test_frozen_public_design_passes(self) -> None:
        result = module.verify(CSV_PATH)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["covered_pairs"], 434)
        self.assertEqual(result["required_pairs"], 434)

    def test_duplicate_blind_identifier_is_rejected(self) -> None:
        with CSV_PATH.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            fieldnames = list(reader.fieldnames or [])
        rows[1]["Blind Case ID"] = rows[0]["Blind Case ID"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mutated.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaises(module.VerificationError):
                module.verify(path)

    def test_target_bearing_identifier_is_rejected(self) -> None:
        with CSV_PATH.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            fieldnames = list(reader.fieldnames or [])
        rows[0]["Blind Case ID"] = "FAR-001"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mutated.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaises(module.VerificationError):
                module.verify(path)

    def test_validation_source_class_split_is_rejected(self) -> None:
        with CSV_PATH.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            fieldnames = list(reader.fieldnames or [])

        rows_by_id = {row["Blind Case ID"]: row for row in rows}
        rows_by_id["CR-024"]["Domain source"] = "De-identified operational case"
        rows_by_id["CR-020"]["Domain source"] = "Naturally occurring public case"

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mutated.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(
                module.VerificationError,
                "validation source split mismatch",
            ):
                module.verify(path)


if __name__ == "__main__":
    unittest.main()
