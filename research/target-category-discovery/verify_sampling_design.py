#!/usr/bin/env python3
"""Verify the exact and semantic TCD-CLEANROOM-001 public sampling design."""
from __future__ import annotations

import csv
import hashlib
import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent
DEFAULT_CSV = ROOT / "covering-array-v1.0.csv"
REPORT_PATH = ROOT / "pairwise-coverage-report-v1.0.csv"
CANONICAL_CSV_SHA256 = "fa5d2cff7fdd05418deb1006ff431a284fef2dadf74f15abaea1da5d67d38822"
CANONICAL_REPORT_SHA256 = "eab73927c36dc82c1e142f183fe0d579304d139af4aef80d37c43f831441bc1c"

DIMENSIONS: dict[str, tuple[str, ...]] = {
    "Output type": (
        "Factual or analytic conclusion", "Classification", "Recommendation",
        "Plan", "Authorization or decision",
    ),
    "Governing relation": (
        "Explicit rule or deduction", "Evidential or probabilistic assessment",
        "Causal or counterfactual assessment", "Optimization or multi-criteria choice",
        "Sequential or interactive procedure",
    ),
    "Temporal structure": ("Static snapshot", "Ordered sequence", "Path-sensitive history"),
    "Information condition": (
        "Materially complete information", "Explicit uncertainty",
        "Missing information", "Conflicting information",
    ),
    "Primary review objective": (
        "Support or correctness", "Reproducibility", "Authorization or compliance",
        "Sensitivity or robustness", "Provenance or accountability",
        "Comparison with an alternative",
    ),
    "Artifact medium": (
        "Narrative", "Table or form", "Graph or diagram",
        "Executable rule, query, or program", "Event log or timeline", "Hybrid",
    ),
    "Domain source": (
        "Naturally occurring public case", "De-identified operational case",
        "Neutral synthetic case",
    ),
}

EXPECTED_HEADERS = ("Row", "Blind Case ID", "Allocation", *DIMENSIONS.keys())
TARGET_PATTERN = re.compile(r"(?:^|[^A-Z])(RCCD|FARA|FARO|PROJECT FAR|FAR-)", re.IGNORECASE)
BLIND_ID_PATTERN = re.compile(r"CR-\d{3}\Z")


class VerificationError(RuntimeError):
    """Raised when the public sampling design violates a frozen control."""


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise VerificationError("CSV has no header")
        return list(reader.fieldnames), list(reader)


def _pairs(values_a: Iterable[str], values_b: Iterable[str]) -> set[tuple[str, str]]:
    return set(itertools.product(values_a, values_b))


def verify(
    path: Path = DEFAULT_CSV,
    *,
    report_path: Path = REPORT_PATH,
    enforce_frozen_digest: bool = True,
) -> dict[str, object]:
    if enforce_frozen_digest:
        if sha256_path(path) != CANONICAL_CSV_SHA256:
            raise VerificationError("covering array byte identity mismatch")
        if sha256_path(report_path) != CANONICAL_REPORT_SHA256:
            raise VerificationError("pairwise report byte identity mismatch")

    headers, rows = _load_rows(path)
    if tuple(headers) != EXPECTED_HEADERS:
        raise VerificationError(
            f"unexpected headers: expected {EXPECTED_HEADERS!r}, got {tuple(headers)!r}"
        )
    if len(rows) != 36:
        raise VerificationError(f"expected 36 rows, found {len(rows)}")

    expected_rows = list(range(1, 37))
    actual_rows: list[int] = []
    blind_ids: list[str] = []
    for row in rows:
        try:
            actual_rows.append(int(row["Row"]))
        except (TypeError, ValueError) as exc:
            raise VerificationError(f"non-integer row value: {row.get('Row')!r}") from exc
        blind_id = row["Blind Case ID"]
        blind_ids.append(blind_id)
        if not BLIND_ID_PATTERN.fullmatch(blind_id):
            raise VerificationError(f"invalid blind case ID: {blind_id!r}")
        for key, value in row.items():
            if TARGET_PATTERN.search(value or ""):
                raise VerificationError(
                    f"target-bearing token in public CSV at {blind_id} / {key}: {value!r}"
                )

    if actual_rows != expected_rows:
        raise VerificationError("row numbers must be exactly 1 through 36 in order")
    if len(set(blind_ids)) != 36:
        raise VerificationError("blind case IDs are not unique")
    if blind_ids != [f"CR-{number:03d}" for number in expected_rows]:
        raise VerificationError("blind case IDs do not match row ordering")

    allocation_counts = Counter(row["Allocation"] for row in rows)
    expected_allocations = Counter({"Development": 24, "Validation—sealed": 12})
    if allocation_counts != expected_allocations:
        raise VerificationError(
            f"allocation mismatch: expected {expected_allocations}, got {allocation_counts}"
        )

    for dimension, expected_levels in DIMENSIONS.items():
        found_levels = {row[dimension] for row in rows}
        expected = set(expected_levels)
        if found_levels != expected:
            raise VerificationError(
                f"level mismatch for {dimension}: missing={sorted(expected-found_levels)}, "
                f"unexpected={sorted(found_levels-expected)}"
            )

    required_total = 0
    covered_total = 0
    pair_report: list[dict[str, object]] = []
    dimension_names = list(DIMENSIONS)
    for index, dimension_a in enumerate(dimension_names):
        for dimension_b in dimension_names[index + 1:]:
            required = _pairs(DIMENSIONS[dimension_a], DIMENSIONS[dimension_b])
            counts = Counter((row[dimension_a], row[dimension_b]) for row in rows)
            missing = required - set(counts)
            if missing:
                raise VerificationError(
                    f"missing pairs for {dimension_a} × {dimension_b}: {sorted(missing)}"
                )
            required_total += len(required)
            covered_total += len(required)
            pair_report.append({
                "dimension_a": dimension_a,
                "dimension_b": dimension_b,
                "required": len(required),
                "covered": len(required),
                "minimum_cell_count": min(counts[pair] for pair in required),
                "maximum_cell_count": max(counts[pair] for pair in required),
            })

    if required_total != 434 or covered_total != 434:
        raise VerificationError(
            f"expected 434/434 pairwise coverage, got {covered_total}/{required_total}"
        )

    source_allocation = Counter((row["Domain source"], row["Allocation"]) for row in rows)
    validation_sources = Counter(
        row["Domain source"] for row in rows if row["Allocation"] == "Validation—sealed"
    )
    expected_validation_sources = Counter({
        "Naturally occurring public case": 6,
        "De-identified operational case": 6,
    })
    if validation_sources != expected_validation_sources:
        raise VerificationError(
            "validation source split mismatch: expected "
            f"{expected_validation_sources}, got {validation_sources}"
        )
    if source_allocation[("Neutral synthetic case", "Validation—sealed")] != 0:
        raise VerificationError("synthetic validation rows were not preregistered")
    if source_allocation[("Neutral synthetic case", "Development")] != 12:
        raise VerificationError("expected all 12 synthetic rows in development")

    _verify_report(pair_report, report_path)
    return {
        "status": "PASS",
        "rows": len(rows),
        "development": allocation_counts["Development"],
        "validation": allocation_counts["Validation—sealed"],
        "required_pairs": required_total,
        "covered_pairs": covered_total,
        "csv_sha256": sha256_path(path),
        "report_sha256": sha256_path(report_path),
    }


def _verify_report(computed: list[dict[str, object]], report_path: Path) -> None:
    headers, rows = _load_rows(report_path)
    expected_headers = [
        "Dimension A", "Dimension B", "Required pairs", "Covered pairs",
        "Coverage %", "Minimum cell count", "Maximum cell count", "Missing pairs",
    ]
    if headers != expected_headers:
        raise VerificationError("pairwise report headers changed")
    if len(rows) != 21:
        raise VerificationError(f"expected 21 pair-report rows, found {len(rows)}")
    expected_by_pair = {
        (entry["dimension_a"], entry["dimension_b"]): entry for entry in computed
    }
    seen: set[tuple[str, str]] = set()
    for row in rows:
        key = (row["Dimension A"], row["Dimension B"])
        if key in seen:
            raise VerificationError(f"duplicate report pair: {key}")
        seen.add(key)
        entry = expected_by_pair.get(key)
        if entry is None:
            raise VerificationError(f"unexpected report pair: {key}")
        checks = {
            "Required pairs": int(entry["required"]),
            "Covered pairs": int(entry["covered"]),
            "Minimum cell count": int(entry["minimum_cell_count"]),
            "Maximum cell count": int(entry["maximum_cell_count"]),
        }
        for field, expected in checks.items():
            try:
                actual = int(row[field])
            except ValueError as exc:
                raise VerificationError(f"non-integer report value for {key} / {field}") from exc
            if actual != expected:
                raise VerificationError(
                    f"report mismatch for {key} / {field}: {actual} != {expected}"
                )
        try:
            coverage = float(row["Coverage %"])
        except ValueError as exc:
            raise VerificationError(f"non-numeric coverage for {key}") from exc
        if coverage != 100.0 or row["Missing pairs"].strip():
            raise VerificationError(f"report does not show complete coverage for {key}")
    if seen != set(expected_by_pair):
        raise VerificationError("pairwise report pair set is incomplete")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    json_mode = "--json" in argv
    positional = [arg for arg in argv if not arg.startswith("--")]
    path = Path(positional[0]).resolve() if positional else DEFAULT_CSV
    try:
        result = verify(path)
    except (OSError, VerificationError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(
        "PASS: {rows} rows; {development} development; {validation} validation; "
        "{covered_pairs}/{required_pairs} pairwise level pairs covered.".format(**result)
    )
    if json_mode:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
