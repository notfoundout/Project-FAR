#!/usr/bin/env python3
"""Verify the public TCD-CLEANROOM-001 covering-array design."""
from __future__ import annotations

import csv
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

DIMENSIONS: dict[str, tuple[str, ...]] = {
    "Output type": (
        "Factual or analytic conclusion",
        "Classification",
        "Recommendation",
        "Plan",
        "Authorization or decision",
    ),
    "Governing relation": (
        "Explicit rule or deduction",
        "Evidential or probabilistic assessment",
        "Causal or counterfactual assessment",
        "Optimization or multi-criteria choice",
        "Sequential or interactive procedure",
    ),
    "Temporal structure": (
        "Static snapshot",
        "Ordered sequence",
        "Path-sensitive history",
    ),
    "Information condition": (
        "Materially complete information",
        "Explicit uncertainty",
        "Missing information",
        "Conflicting information",
    ),
    "Primary review objective": (
        "Support or correctness",
        "Reproducibility",
        "Authorization or compliance",
        "Sensitivity or robustness",
        "Provenance or accountability",
        "Comparison with an alternative",
    ),
    "Artifact medium": (
        "Narrative",
        "Table or form",
        "Graph or diagram",
        "Executable rule, query, or program",
        "Event log or timeline",
        "Hybrid",
    ),
    "Domain source": (
        "Naturally occurring public case",
        "De-identified operational case",
        "Neutral synthetic case",
    ),
}

EXPECTED_HEADERS = (
    "Row",
    "Blind Case ID",
    "Allocation",
    *DIMENSIONS.keys(),
)

FORBIDDEN_HEADERS = {
    "case id",
    "domain",
    "source",
    "source title",
    "source organization",
    "source url",
    "synthetic rule seed",
    "packet hash",
}

TARGET_PATTERN = re.compile(r"(?:^|[^A-Z])(RCCD|FARA|FARO|PROJECT FAR|FAR-)", re.IGNORECASE)
BLIND_ID_PATTERN = re.compile(r"CR-\d{3}\Z")


class VerificationError(RuntimeError):
    """Raised when the public sampling design violates a frozen control."""


def _load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise VerificationError("CSV has no header")
        rows = list(reader)
        return list(reader.fieldnames), rows


def _pairs(values_a: Iterable[str], values_b: Iterable[str]) -> set[tuple[str, str]]:
    return set(itertools.product(values_a, values_b))


def verify(path: Path = DEFAULT_CSV) -> dict[str, object]:
    headers, rows = _load_rows(path)

    if tuple(headers) != EXPECTED_HEADERS:
        raise VerificationError(
            f"unexpected headers: expected {EXPECTED_HEADERS!r}, got {tuple(headers)!r}"
        )

    lowered_headers = {header.strip().lower() for header in headers}
    leaked_headers = lowered_headers & FORBIDDEN_HEADERS
    if leaked_headers:
        raise VerificationError(f"restricted headers present: {sorted(leaked_headers)}")

    if len(rows) != 36:
        raise VerificationError(f"expected 36 rows, found {len(rows)}")

    expected_rows = list(range(1, 37))
    actual_rows: list[int] = []
    blind_ids: list[str] = []
    for row in rows:
        try:
            actual_rows.append(int(row["Row"]))
        except ValueError as exc:
            raise VerificationError(f"non-integer row value: {row['Row']!r}") from exc
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
        for dimension_b in dimension_names[index + 1 :]:
            required = _pairs(DIMENSIONS[dimension_a], DIMENSIONS[dimension_b])
            counts = Counter((row[dimension_a], row[dimension_b]) for row in rows)
            covered = set(counts)
            missing = required - covered
            if missing:
                raise VerificationError(
                    f"missing pairs for {dimension_a} × {dimension_b}: {sorted(missing)}"
                )
            required_total += len(required)
            covered_total += len(required & covered)
            pair_report.append(
                {
                    "dimension_a": dimension_a,
                    "dimension_b": dimension_b,
                    "required": len(required),
                    "covered": len(required & covered),
                    "minimum_cell_count": min(counts[pair] for pair in required),
                    "maximum_cell_count": max(counts[pair] for pair in required),
                }
            )

    if required_total != 434 or covered_total != 434:
        raise VerificationError(
            f"expected 434/434 pairwise coverage, got {covered_total}/{required_total}"
        )

    objective_medium_counts = Counter(
        (row["Primary review objective"], row["Artifact medium"]) for row in rows
    )
    required_objective_medium = _pairs(
        DIMENSIONS["Primary review objective"], DIMENSIONS["Artifact medium"]
    )
    if set(objective_medium_counts) != required_objective_medium:
        raise VerificationError("objective × medium grid is incomplete")
    if set(objective_medium_counts.values()) != {1}:
        raise VerificationError("objective × medium cells must each occur exactly once")

    source_allocation = Counter(
        (row["Domain source"], row["Allocation"]) for row in rows
    )
    expected_validation_sources = Counter(
        {
            "Naturally occurring public case": 6,
            "De-identified operational case": 6,
        }
    )
    validation_sources = Counter(
        row["Domain source"]
        for row in rows
        if row["Allocation"] == "Validation—sealed"
    )
    if validation_sources != expected_validation_sources:
        raise VerificationError(
            "validation source split mismatch: expected "
            f"{expected_validation_sources}, got {validation_sources}"
        )
    if source_allocation[("Neutral synthetic case", "Validation—sealed")] != 0:
        raise VerificationError("synthetic validation rows were not preregistered")
    if source_allocation[("Neutral synthetic case", "Development")] != 12:
        raise VerificationError("expected all 12 synthetic rows in development")

    _verify_report(pair_report)

    return {
        "status": "PASS",
        "rows": len(rows),
        "development": allocation_counts["Development"],
        "validation": allocation_counts["Validation—sealed"],
        "required_pairs": required_total,
        "covered_pairs": covered_total,
        "source_allocation": {
            f"{source} | {allocation}": count
            for (source, allocation), count in sorted(source_allocation.items())
        },
    }


def _verify_report(computed: list[dict[str, object]]) -> None:
    headers, rows = _load_rows(REPORT_PATH)
    expected_headers = [
        "Dimension A",
        "Dimension B",
        "Required pairs",
        "Covered pairs",
        "Coverage %",
        "Minimum cell count",
        "Maximum cell count",
        "Missing pairs",
    ]
    if headers != expected_headers:
        raise VerificationError("pairwise report headers changed")
    if len(rows) != 21:
        raise VerificationError(f"expected 21 pair-report rows, found {len(rows)}")
    expected_by_pair = {
        (entry["dimension_a"], entry["dimension_b"]): entry for entry in computed
    }
    for row in rows:
        key = (row["Dimension A"], row["Dimension B"])
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
            if int(row[field]) != expected:
                raise VerificationError(
                    f"report mismatch for {key} / {field}: {row[field]} != {expected}"
                )
        if float(row["Coverage %"]) != 100.0 or row["Missing pairs"].strip():
            raise VerificationError(f"report does not show complete coverage for {key}")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    path = Path(argv[0]).resolve() if argv else DEFAULT_CSV
    try:
        result = verify(path)
    except (OSError, VerificationError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(
        "PASS: {rows} rows; {development} development; {validation} validation; "
        "{covered_pairs}/{required_pairs} pairwise level pairs covered.".format(**result)
    )
    if "--json" in argv:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
