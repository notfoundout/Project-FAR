from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "research/target-category-discovery/verify_sampling_design.py"
CSV_PATH = ROOT / "research/target-category-discovery/covering-array-v1.0.csv"
REPORT_PATH = ROOT / "research/target-category-discovery/pairwise-coverage-report-v1.0.csv"

spec = importlib.util.spec_from_file_location("verify_sampling_design", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class TargetCategorySamplingDesignTests(unittest.TestCase):
    def test_frozen_public_design_passes(self) -> None:
        result = module.verify(CSV_PATH)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["covered_pairs"], 434)
        self.assertEqual(result["required_pairs"], 434)

    def test_semantically_identical_byte_change_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "array.csv"
            path.write_bytes(CSV_PATH.read_bytes() + b"\n")
            with self.assertRaisesRegex(module.VerificationError, "byte identity mismatch"):
                module.verify(path)

    def test_report_byte_change_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.csv"
            report.write_bytes(REPORT_PATH.read_bytes() + b"\n")
            with self.assertRaisesRegex(module.VerificationError, "report byte identity mismatch"):
                module.verify(CSV_PATH, report_path=report)

    def _mutate_rows(self, mutator, expected: str) -> None:
        fields, rows = read_csv(CSV_PATH)
        mutator(fields, rows)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mutated.csv"
            write_csv(path, fields, rows)
            with self.assertRaisesRegex(module.VerificationError, expected):
                module.verify(path, enforce_frozen_digest=False)

    def test_header_change_is_rejected(self) -> None:
        def mutate(fields, rows):
            fields[-1] = "Source"
            for row in rows:
                row["Source"] = row.pop("Domain source")
        self._mutate_rows(mutate, "unexpected headers")

    def test_row_count_is_rejected(self) -> None:
        self._mutate_rows(lambda fields, rows: rows.pop(), "expected 36 rows")

    def test_noninteger_row_is_rejected(self) -> None:
        self._mutate_rows(lambda fields, rows: rows[0].__setitem__("Row", "one"), "non-integer")

    def test_invalid_blind_identifier_is_rejected(self) -> None:
        self._mutate_rows(lambda fields, rows: rows[0].__setitem__("Blind Case ID", "CASE-001"), "invalid blind")

    def test_target_bearing_token_is_rejected(self) -> None:
        self._mutate_rows(
            lambda fields, rows: rows[0].__setitem__("Output type", "Project FAR conclusion"),
            "target-bearing",
        )

    def test_row_order_is_rejected(self) -> None:
        def mutate(fields, rows):
            rows[0], rows[1] = rows[1], rows[0]
        self._mutate_rows(mutate, "row numbers")

    def test_duplicate_blind_identifier_is_rejected(self) -> None:
        self._mutate_rows(
            lambda fields, rows: rows[1].__setitem__("Blind Case ID", rows[0]["Blind Case ID"]),
            "not unique",
        )

    def test_blind_id_order_mapping_is_rejected(self) -> None:
        def mutate(fields, rows):
            rows[0]["Blind Case ID"], rows[1]["Blind Case ID"] = (
                rows[1]["Blind Case ID"], rows[0]["Blind Case ID"]
            )
        self._mutate_rows(mutate, "do not match row ordering")

    def test_allocation_count_is_rejected(self) -> None:
        self._mutate_rows(
            lambda fields, rows: rows[1].__setitem__("Allocation", "Validation—sealed"),
            "allocation mismatch",
        )

    def test_dimension_level_set_is_rejected(self) -> None:
        self._mutate_rows(
            lambda fields, rows: rows[0].__setitem__("Output type", "Unsupported output"),
            "level mismatch",
        )

    def test_missing_pair_is_rejected(self) -> None:
        def mutate(fields, rows):
            # Preserve every level but remove the unique objective/medium pair from CR-001.
            rows[0]["Artifact medium"] = "Table or form"
        self._mutate_rows(mutate, "missing pairs")

    def test_validation_source_class_split_is_rejected(self) -> None:
        def mutate(fields, rows):
            by_id = {row["Blind Case ID"]: row for row in rows}
            by_id["CR-024"]["Domain source"] = "De-identified operational case"
            by_id["CR-020"]["Domain source"] = "Naturally occurring public case"
        self._mutate_rows(mutate, "validation source split mismatch")

    def test_synthetic_validation_is_rejected(self) -> None:
        def mutate(fields, rows):
            by_id = {row["Blind Case ID"]: row for row in rows}
            # Keep allocation totals but exchange labels between a synthetic development
            # row and a public validation row. Semantic checks must reject the result.
            by_id["CR-002"]["Allocation"] = "Validation—sealed"
            by_id["CR-001"]["Allocation"] = "Development"
        self._mutate_rows(mutate, "validation source split mismatch|synthetic validation")

    def _mutate_report(self, mutator, expected: str) -> None:
        fields, rows = read_csv(REPORT_PATH)
        mutator(fields, rows)
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.csv"
            write_csv(report, fields, rows)
            with self.assertRaisesRegex(module.VerificationError, expected):
                module.verify(
                    CSV_PATH,
                    report_path=report,
                    enforce_frozen_digest=False,
                )

    def test_report_header_is_rejected(self) -> None:
        def mutate(fields, rows):
            fields[-1] = "Missing"
            for row in rows:
                row["Missing"] = row.pop("Missing pairs")
        self._mutate_report(mutate, "headers changed")

    def test_report_row_count_is_rejected(self) -> None:
        self._mutate_report(lambda fields, rows: rows.pop(), "expected 21")

    def test_duplicate_report_pair_is_rejected(self) -> None:
        def mutate(fields, rows):
            rows[1]["Dimension A"] = rows[0]["Dimension A"]
            rows[1]["Dimension B"] = rows[0]["Dimension B"]
        self._mutate_report(mutate, "duplicate report pair")

    def test_report_numeric_mismatch_is_rejected(self) -> None:
        self._mutate_report(
            lambda fields, rows: rows[0].__setitem__("Covered pairs", "24"),
            "report mismatch",
        )

    def test_report_incomplete_coverage_is_rejected(self) -> None:
        self._mutate_report(
            lambda fields, rows: rows[0].__setitem__("Coverage %", "99.0"),
            "does not show complete coverage",
        )


if __name__ == "__main__":
    unittest.main()
