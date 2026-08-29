#!/usr/bin/env python3
"""Noncanonical finite exact-contract demonstrator for FAR-CORE-001/002."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping


class PlaygroundError(ValueError):
    pass


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _validate(spec: Mapping[str, Any]) -> tuple[list[str], list[str], dict[str, Any], dict[str, Any]]:
    if spec.get("schema_version") != "far-exact-playground/1.0":
        raise PlaygroundError("unsupported or missing schema_version")
    cases = spec.get("cases")
    tests = spec.get("tests")
    behavior = spec.get("behavior")
    representation = spec.get("representation")
    if not isinstance(cases, list) or not cases or not all(isinstance(x, str) and x for x in cases):
        raise PlaygroundError("cases must be a non-empty list of non-empty strings")
    if len(cases) != len(set(cases)):
        raise PlaygroundError("cases must be unique")
    if not isinstance(tests, list) or not tests or not all(isinstance(x, str) and x for x in tests):
        raise PlaygroundError("tests must be a non-empty list of non-empty strings")
    if len(tests) != len(set(tests)):
        raise PlaygroundError("tests must be unique")
    if not isinstance(behavior, dict) or set(behavior) != set(cases):
        raise PlaygroundError("behavior keys must equal the case set")
    for case in cases:
        if not isinstance(behavior[case], dict) or set(behavior[case]) != set(tests):
            raise PlaygroundError(f"behavior[{case!r}] keys must equal the test set")
    if not isinstance(representation, dict) or set(representation) != set(cases):
        raise PlaygroundError("representation keys must equal the case set")
    return cases, tests, behavior, representation


def analyze(spec: Mapping[str, Any]) -> dict[str, Any]:
    cases, tests, behavior, representation = _validate(spec)
    rep_groups: dict[str, list[str]] = defaultdict(list)
    behavior_groups: dict[str, list[str]] = defaultdict(list)
    rep_values: dict[str, Any] = {}
    behavior_values: dict[str, Any] = {}
    for case in cases:
        rep_key = canonical(representation[case])
        behavior_key = canonical(behavior[case])
        rep_groups[rep_key].append(case)
        behavior_groups[behavior_key].append(case)
        rep_values[rep_key] = representation[case]
        behavior_values[behavior_key] = behavior[case]

    collisions: list[dict[str, Any]] = []
    decoder: list[dict[str, Any]] = []
    for rep_key in sorted(rep_groups):
        group = sorted(rep_groups[rep_key])
        seen_behaviors = sorted({canonical(behavior[case]) for case in group})
        if len(seen_behaviors) == 1:
            decoder.append({"representation_value": rep_values[rep_key], "behavior": behavior_values[seen_behaviors[0]]})
        else:
            for index, left in enumerate(group):
                for right in group[index + 1 :]:
                    if behavior[left] != behavior[right]:
                        collisions.append({"left": left, "right": right, "representation_value": rep_values[rep_key], "left_behavior": behavior[left], "right_behavior": behavior[right]})

    quotient = [
        {"class_id": f"Q-{index:03d}", "cases": sorted(behavior_groups[key]), "behavior": behavior_values[key]}
        for index, key in enumerate(sorted(behavior_groups), 1)
    ]
    case_to_class = {case: item["class_id"] for item in quotient for case in item["cases"]}
    sufficient = not collisions
    rep_class_count = len(rep_groups)
    quotient_count = len(quotient)
    comparison = "equivalent_to_observational_quotient" if sufficient and rep_class_count == quotient_count else ("strictly_more_informative_than_observational_quotient" if sufficient else "insufficient_not_comparable_as_sufficient_representation")
    return {
        "schema_version": "far-exact-playground-result/1.0",
        "authority": "experimental_noncanonical_finite_exact_demonstrator",
        "case_count": len(cases),
        "test_count": len(tests),
        "sufficient": sufficient,
        "decoder": decoder if sufficient else None,
        "collision_witness": collisions[0] if collisions else None,
        "all_collisions": collisions,
        "observational_equivalence_classes": quotient,
        "quotient_map": {case: case_to_class[case] for case in sorted(cases)},
        "represented_value_count": rep_class_count,
        "quotient_class_count": quotient_count,
        "comparison": comparison,
        "nonclaims": ["not the production FAR engine", "not the W3 contract language", "finite execution is not a universal proof"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        result = analyze(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, PlaygroundError) as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result["sufficient"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
