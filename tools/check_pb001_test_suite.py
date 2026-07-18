#!/usr/bin/env python3
"""Validate the frozen PB-001 preservation-basis test suite."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/evaluation/pb001-test-suite-registry.json"
SPEC = ROOT / "docs/research/pb001-preservation-basis-test-suite-v1.0.md"

EXPECTED_AXES = [f"P{i}" for i in range(1, 9)]
EXPECTED_PAIRS = [f"PA-{i:02d}" for i in range(1, 9)]
EXPECTED_DOMAINS = [f"D{i}" for i in range(1, 17)]
EXPECTED_FAMILIES = {
    "paired_axis_discrimination",
    "axis_ablation",
    "domain_coverage",
    "IRD_countermodel_coverage",
    "hidden_recovery_audit",
    "adversarial_addition_search",
}
EXPECTED_COUNTERMODELS = {
    "arbitrary_labeled_transition",
    "output_equivalent_lookup",
    "post_hoc_narrative",
    "hidden_operator",
    "pure_optimizer",
    "trivial_universal_encoding",
    "distributed_reasoning",
    "self_revision",
    "continuous_embodied_control",
    "conflicting_normative_reasons",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"PBTS-001 validation failed: {message}")


def main() -> None:
    require(REGISTRY.exists(), f"missing {REGISTRY.relative_to(ROOT)}")
    require(SPEC.exists(), f"missing {SPEC.relative_to(ROOT)}")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    text = SPEC.read_text(encoding="utf-8")

    require(data.get("suite_id") == "PBTS-001", "suite_id must be PBTS-001")
    require(data.get("suite_version") == "1.0", "suite_version must be 1.0")
    require(data.get("status") == "frozen_prospective", "suite must remain prospectively frozen")
    require(data.get("basis_id") == "PB-001", "suite must target PB-001")
    require(data.get("candidate_dependencies") == [], "candidate dependency set must remain empty")
    require(data.get("execution_status") == "not_executed", "freeze PR must not claim execution")
    require(data.get("results") == [], "freeze PR must contain no results")

    pairs = data.get("primary_pairs", [])
    require([p.get("id") for p in pairs] == EXPECTED_PAIRS, "primary pair IDs changed")
    require([p.get("target_axis") for p in pairs] == EXPECTED_AXES, "each P1-P8 axis must have exactly one primary pair")

    require(set(data.get("required_test_families", [])) == EXPECTED_FAMILIES, "required test families changed")
    coverage = data.get("domain_coverage", {})
    require(coverage.get("target_classes") == EXPECTED_DOMAINS, "D1-D16 coverage must be complete")
    require(coverage.get("minimum_cases_per_class", 0) >= 2, "each domain requires at least two cases")
    require(set(data.get("mandatory_countermodels", [])) == EXPECTED_COUNTERMODELS, "mandatory countermodel set changed")

    gate = data.get("advance_gate", {})
    require(gate and all(value is False for value in gate.values()), "all advance gates must remain false before execution")

    required_sections = [
        "## Family A — Paired-axis discrimination",
        "## Family B — Axis ablations",
        "## Family C — Domain coverage",
        "## Family D — IRD-001 countermodel coverage",
        "## Family E — Hidden-recovery audit",
        "## Family F — Adversarial addition search",
        "## Decision rules",
        "## Allowed outcomes",
        "## Nonclaims",
    ]
    for section in required_sections:
        require(section in text, f"missing section: {section}")

    for pair_id in EXPECTED_PAIRS:
        require(pair_id in text, f"missing primary pair {pair_id}")

    forbidden_claims = [
        "PB-001 is sufficient.",
        "PB-001 is necessary.",
        "PB-001 is independent.",
        "PB-001 is minimal.",
        "FARA satisfies PB-001.",
    ]
    for claim in forbidden_claims:
        require(claim not in text, f"unsupported affirmative claim: {claim}")

    print("PBTS-001 test-suite validation: PASS")


if __name__ == "__main__":
    main()
