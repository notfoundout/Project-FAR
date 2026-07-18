#!/usr/bin/env python3
"""Validate the frozen architecture-neutral reasoning definition."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/evaluation/independent-reasoning-definition-registry.json"
DOMAIN = ROOT / "theory/evaluation/reasoning-domain-registry.json"
DEFINITION = ROOT / "docs/research/independent-reasoning-definition-v1.0.md"

EXPECTED_COMPONENTS = {"T", "X", "H", "O", "K", "Q", "Delta", "Gamma", "support_relation"}
EXPECTED_CONDITIONS = {"R1", "R2", "R3", "R4", "R5", "R6"}
EXPECTED_GRADES = {"E0", "E1", "E2"}
EXPECTED_COUNTERMODELS = {
    "C1_arbitrary_labeled_transition",
    "C2_output_equivalent_lookup",
    "C3_post_hoc_narrative",
    "C4_hidden_operator",
    "C5_pure_optimizer",
    "C6_trivial_universal_encoding",
    "C7_distributed_reasoning",
    "C8_self_revision",
    "C9_continuous_embodied_control",
    "C10_conflicting_normative_reasons",
}
REQUIRED_SECTIONS = [
    "## Mathematical setting",
    "## Core definition",
    "## Definition family by evidential strength",
    "## Boundary classifications",
    "## Domain coverage obligations",
    "## Clause-to-domain justification",
    "## Countermodels and stress tests",
    "## Candidate-neutrality audit",
    "## Failure and revision conditions",
    "## Nonclaims",
    "## Immediate next milestone",
]
FORBIDDEN_DEPENDENCIES = {"frameworks/FARA", "frameworks/FARO", "far-ir"}


def fail(message: str) -> None:
    raise SystemExit(f"independent reasoning definition check failed: {message}")


def main() -> None:
    for path in (REGISTRY, DOMAIN, DEFINITION):
        if not path.is_file():
            fail(f"missing required artifact: {path.relative_to(ROOT)}")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    domain = json.loads(DOMAIN.read_text(encoding="utf-8"))
    text = DEFINITION.read_text(encoding="utf-8")

    if registry.get("definition_id") != "IRD-001":
        fail("definition_id must be IRD-001")
    if registry.get("definition_version") != "1.0":
        fail("definition version must be 1.0")
    if registry.get("status") != "frozen_prospective":
        fail("definition must remain frozen_prospective")
    if registry.get("definition") != "docs/research/independent-reasoning-definition-v1.0.md":
        fail("definition path drift")

    dependencies = set(registry.get("candidate_dependencies", []))
    if dependencies:
        fail("candidate_dependencies must be empty")
    serialized_dependencies = " ".join(registry.get("depends_on", [])).lower()
    if any(item.lower() in serialized_dependencies for item in FORBIDDEN_DEPENDENCIES):
        fail("definition may not depend on FARA, FARO, or FAR-IR")

    if set(registry.get("core_components", [])) != EXPECTED_COMPONENTS:
        fail("core component set changed without a version revision")
    condition_ids = {item.get("id") for item in registry.get("core_conditions", [])}
    if condition_ids != EXPECTED_CONDITIONS:
        fail("R1-R6 condition set changed without a version revision")
    if set(registry.get("evidential_grades", {})) != EXPECTED_GRADES:
        fail("E0-E2 evidential grades are incomplete")
    if set(registry.get("mandatory_countermodels", [])) != EXPECTED_COUNTERMODELS:
        fail("mandatory countermodel set changed")

    domain_ids = {item["id"] for item in domain.get("target_classes", [])}
    if set(registry.get("covered_domain_classes", [])) != domain_ids:
        fail("definition coverage must match all frozen target classes")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            fail(f"missing section: {section}")

    for condition in EXPECTED_CONDITIONS:
        if f"### {condition} —" not in text:
            fail(f"missing formal condition heading: {condition}")

    for grade in EXPECTED_GRADES:
        if f"### {grade} —" not in text:
            fail(f"missing evidential grade heading: {grade}")

    lower = text.lower()
    if "does not depend on `frameworks/fara/`" not in lower:
        fail("candidate-independence declaration missing")
    if "no fara primitive" not in lower and "does not require representation" not in lower:
        fail("FARA-neutrality statement missing")
    if "multiple reasoning classes" not in lower:
        fail("fragmentation outcome must remain allowed")
    if "no finite universal architecture" not in lower:
        fail("impossibility outcome must remain allowed")
    if "invented hidden steps are prohibited" not in lower:
        fail("observability anti-repair rule missing")

    nonclaims = " ".join(registry.get("nonclaims", [])).lower()
    for phrase in ("not established as necessary", "does not establish that one universal", "does not establish that fara represents"):
        if phrase not in nonclaims:
            fail(f"required nonclaim missing: {phrase}")

    next_artifact = registry.get("next_required_artifact", "").lower()
    if "preservation-basis" not in next_artifact:
        fail("next milestone must be the preservation-basis investigation")

    print("independent reasoning definition check: PASS")


if __name__ == "__main__":
    main()
