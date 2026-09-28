"""Generic table-consistency checker: the EFR-001 v2.0 active-comparator report.

Input: a JSON object with two lists of rows, ``representation`` and ``required_behavior``, each
row ``{"case_id": str, "value": <any JSON value>}``. The checker answers one question: does any
pair of cases share a representation value while requiring different behavior?

This file deliberately imports nothing from Project FAR and uses no Project FAR terminology, so
the comparator arm receives the same determinate yes/no answer as the FAR arm without any
FAR-specific framing, contract fields, or verifier vocabulary. It is standard library only.
"""
from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _index(rows: object, label: str) -> dict[str, object]:
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{label} must be a non-empty list")
    table: dict[str, object] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"case_id", "value"} or not isinstance(row["case_id"], str):
            raise ValueError(f"{label} rows must be objects with exactly case_id (string) and value")
        if row["case_id"] in table:
            raise ValueError(f"duplicate case_id in {label}: {row['case_id']}")
        table[row["case_id"]] = row["value"]
    return table


def check(tables: dict) -> dict:
    if not isinstance(tables, dict) or set(tables) != {"representation", "required_behavior"}:
        raise ValueError("input must contain exactly representation and required_behavior")
    representation = _index(tables["representation"], "representation")
    behavior = _index(tables["required_behavior"], "required_behavior")
    if set(representation) != set(behavior):
        raise ValueError("representation and required_behavior must list the same case IDs")
    cases = sorted(representation)
    conflicts = [
        {
            "case_a": left,
            "case_b": right,
            "representation": representation[left],
            "behavior_a": behavior[left],
            "behavior_b": behavior[right],
        }
        for left, right in combinations(cases, 2)
        if _canonical(representation[left]) == _canonical(representation[right])
        and _canonical(behavior[left]) != _canonical(behavior[right])
    ]
    mapping: dict[str, object] = {}
    if not conflicts:
        for case_id in cases:
            mapping.setdefault(_canonical(representation[case_id]), behavior[case_id])
    return {
        "result": "INCONSISTENT" if conflicts else "CONSISTENT",
        "cases_checked": len(cases),
        "distinct_representation_values": len({_canonical(representation[c]) for c in cases}),
        "conflicting_pairs": conflicts,
        "mapping": [{"representation": json.loads(key), "required_behavior": value} for key, value in sorted(mapping.items())],
    }


def render(result: dict) -> str:
    """Frozen plain-text rendering shown in the comparator arm's report box."""
    lines = [
        "Table consistency check",
        f"Cases checked: {result['cases_checked']}",
        f"Distinct representation values: {result['distinct_representation_values']}",
        f"Result: {result['result']}",
    ]
    if result["conflicting_pairs"]:
        lines.append("Pairs with the same representation value and different required behavior:")
        for pair in result["conflicting_pairs"]:
            lines.append(
                f"- {pair['case_a']} and {pair['case_b']}: representation {_canonical(pair['representation'])}; "
                f"required behavior {_canonical(pair['behavior_a'])} vs {_canonical(pair['behavior_b'])}"
            )
    else:
        lines.append("Each representation value corresponds to one required-behavior value:")
        for row in result["mapping"]:
            lines.append(f"- {_canonical(row['representation'])} -> {_canonical(row['required_behavior'])}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) not in (1, 2) or (len(args) == 2 and args[1] != "--json"):
        raise SystemExit("usage: python tools/efr_generic_collision_checker.py TABLES.json [--json]")
    result = check(json.loads(Path(args[0]).read_bytes().decode("utf-8")))
    if len(args) == 2:
        print(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False))
    else:
        sys.stdout.write(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
