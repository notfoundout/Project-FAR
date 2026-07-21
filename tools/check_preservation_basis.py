#!/usr/bin/env python3
"""Validate the frozen architecture-neutral preservation basis."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/evaluation/preservation-basis-registry.json"
SPEC = ROOT / "docs/research/preservation-basis-investigation-v1.0.md"

EXPECTED_AXES = {
    "P1": "configuration",
    "P2": "commitment",
    "P3": "stake_and_alternatives",
    "P4": "ground_and_justification",
    "P5": "admissibility_and_dynamics",
    "P6": "consequence",
    "P7": "historical_and_path",
    "P8": "evidential_correspondence",
}
EXPECTED_TESTS = {
    "domain_coverage",
    "paired_independence",
    "axis_ablation",
    "adversarial_addition_search",
}
EXPECTED_SCORES = {"pass", "partial", "fail", "unknown"}
REQUIRED_SECTIONS = [
    "## PB-001 candidate preservation basis",
    "## Treatment of the inherited six dimensions",
    "## Candidate-neutrality audit",
    "## Sufficiency, independence, and minimality test program",
    "## Allowed unfavorable outcomes",
    "## Nonclaims",
]
FORBIDDEN_CLAIMS = [
    "PB-001 is sufficient.",
    "PB-001 is necessary.",
    "PB-001 is independent.",
    "PB-001 is minimal.",
    "FARA satisfies PB-001.",
]


def fail(message: str) -> None:
    raise SystemExit(f"preservation-basis check failed: {message}")


def main() -> None:
    if not REGISTRY.exists() or not SPEC.exists():
        fail("required registry or specification is missing")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    text = SPEC.read_text(encoding="utf-8")

    if data.get("basis_id") != "PB-001" or data.get("basis_version") != "1.0":
        fail("PB-001 identity or version changed")
    if data.get("status") != "frozen_prospective_candidate":
        fail("PB-001 must remain a prospective candidate basis")
    if data.get("candidate_dependencies") != []:
        fail("PB-001 may not depend on a candidate architecture")

    axes = data.get("axes", [])
    actual = {axis.get("id"): axis.get("name") for axis in axes}
    if actual != EXPECTED_AXES:
        fail(f"axis set changed: {actual!r}")
    if any(axis.get("status") != "provisionally_retained" for axis in axes):
        fail("axes may not be upgraded beyond provisional status")

    if set(data.get("score_values", [])) != EXPECTED_SCORES:
        fail("score values must remain Pass/Partial/Fail/Unknown")
    if data.get("unknown_ordering") != "unordered":
        fail("Unknown may not be ordered between Partial and Fail")

    aggregate = data.get("aggregate_criterion", {})
    if aggregate.get("coordinate") is not False:
        fail("information/no-loss aggregate may not be counted as a coordinate")
    if set(aggregate.get("derived_from", [])) != set(EXPECTED_AXES):
        fail("aggregate no-loss judgment must derive from all P1-P8 axes")

    dispositions = data.get("legacy_dimension_dispositions", {})
    if dispositions.get("information") != "reclassified_as_aggregate_criterion":
        fail("legacy information preservation must remain an aggregate criterion")
    if set(data.get("required_test_families", [])) != EXPECTED_TESTS:
        fail("required preservation-basis test families changed")

    allowed = set(data.get("allowed_outcomes", []))
    for required in {
        "axis_redundancy",
        "basis_incomplete",
        "no_finite_basis",
        "IRD_revision_required",
        "insufficient_evidence",
    }:
        if required not in allowed:
            fail(f"unfavorable or unresolved outcome missing: {required}")

    nonclaims = " ".join(data.get("nonclaims", []))
    for term in [
        "not established as sufficient",
        "not established as necessary",
        "not established as independent",
        "not established as minimal",
        "does not establish FARA",
    ]:
        if term not in nonclaims:
            fail(f"required nonclaim missing: {term}")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            fail(f"required section missing: {section}")
    for axis_id in EXPECTED_AXES:
        if f"### {axis_id} —" not in text:
            fail(f"axis section missing: {axis_id}")
    for forbidden in FORBIDDEN_CLAIMS:
        if forbidden in text:
            fail(f"unsupported affirmative claim present: {forbidden}")

    lower = text.lower()
    aggregate_statements = (
        "reclassified as an aggregate adequacy criterion, not a coordinate",
        "information preservation is an aggregate no-loss criterion rather than an independent dimension",
    )
    if not all(statement in lower for statement in aggregate_statements):
        fail("aggregate treatment of information preservation is not explicit")
    if "FARA primitives" not in text or "not derivation inputs" not in text:
        fail("candidate-neutral derivation boundary is not explicit")

    print("preservation-basis check: PASS")


if __name__ == "__main__":
    main()
