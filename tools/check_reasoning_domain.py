#!/usr/bin/env python3
"""Validate the frozen architecture-neutral reasoning-domain specification."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/evaluation/reasoning-domain-registry.json"
SPEC = ROOT / "docs/research/reasoning-domain-specification-v1.0.md"

EXPECTED_IDS = [f"D{i}" for i in range(1, 17)]
EXPECTED_STRATA = {"O0", "O1", "O2", "O3", "O4"}
FORBIDDEN_ADMISSION_PHRASES = [
    "must instantiate representation",
    "must instantiate structure",
    "must instantiate interpretation",
    "must instantiate investigation",
    "must instantiate calculus",
    "fara is required",
]
REQUIRED_SPEC_SECTIONS = [
    "## Target classes",
    "## Cross-cutting variation requirements",
    "## Boundary and unresolved classes",
    "## Provisional exclusions",
    "## Observability strata",
    "## Domain admission procedure",
    "## Revision and freeze policy",
    "## Candidate-neutrality audit",
    "## Required output of the next milestone",
]


def fail(message: str) -> None:
    raise SystemExit(f"reasoning-domain check failed: {message}")


def main() -> None:
    if not REGISTRY.is_file():
        fail(f"missing registry: {REGISTRY.relative_to(ROOT)}")
    if not SPEC.is_file():
        fail(f"missing specification: {SPEC.relative_to(ROOT)}")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    text = SPEC.read_text(encoding="utf-8")
    lower = text.lower()

    if data.get("schema_version") != "1.0":
        fail("unsupported schema version")
    if data.get("specification_version") != "1.0":
        fail("unexpected specification version")
    if data.get("status") != "frozen_prospective":
        fail("domain specification is not prospectively frozen")
    if data.get("specification") != "docs/research/reasoning-domain-specification-v1.0.md":
        fail("registry points to the wrong specification")

    target_classes = data.get("target_classes")
    if not isinstance(target_classes, list):
        fail("target_classes must be a list")
    ids = [entry.get("id") for entry in target_classes]
    if ids != EXPECTED_IDS:
        fail(f"target class IDs must be exactly {EXPECTED_IDS}")
    if len(set(ids)) != len(ids):
        fail("duplicate target class ID")
    if any(entry.get("status") != "target" for entry in target_classes):
        fail("all registered D1-D16 classes must retain target status")

    strata = data.get("observability_strata", {})
    if set(strata) != EXPECTED_STRATA:
        fail("observability strata must be exactly O0-O4")

    axes = data.get("cross_cutting_axes")
    if not isinstance(axes, list) or len(axes) < 14 or len(set(axes)) != len(axes):
        fail("cross-cutting variation axes are incomplete or duplicated")

    boundaries = data.get("boundary_classes")
    if not isinstance(boundaries, list) or len(boundaries) < 10:
        fail("boundary-class coverage is incomplete")

    for section in REQUIRED_SPEC_SECTIONS:
        if section not in text:
            fail(f"missing required section: {section}")

    for phrase in FORBIDDEN_ADMISSION_PHRASES:
        if phrase in lower:
            fail(f"candidate-native admission requirement detected: {phrase}")

    required_nonclaims = {
        "This registry does not define reasoning mathematically.",
        "This registry does not establish that one universal reasoning class exists.",
        "This registry does not establish FARA universality, necessity, minimality, or superiority.",
    }
    if set(data.get("nonclaims", [])) != required_nonclaims:
        fail("required domain nonclaims changed or are incomplete")

    if "failure to define one common mathematical class is an allowed outcome" not in lower:
        fail("the specification must permit domain fragmentation")
    if "lack of internal-state access does not by itself make a system non-reasoning" not in lower:
        fail("opaque systems are being excluded by observability alone")
    if "fara is not referenced as an admission criterion" not in lower:
        fail("candidate-neutrality audit is incomplete")

    print("reasoning-domain check: PASS")


if __name__ == "__main__":
    main()
