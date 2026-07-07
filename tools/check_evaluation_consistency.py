#!/usr/bin/env python3
"""Validate Project FAR evaluation/reporting registries without touching theory artifacts."""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
PRIMITIVES = {
    "Investigation",
    "Representation",
    "Representational Structure",
    "Interpretation",
    "Reasoning Calculus",
}
EVIDENCE_CLASSIFICATIONS = {
    "fits FAR",
    "extends FAR",
    "candidate counterexample",
    "conservative extension",
}
ANALYSIS_STATUSES = {"not analyzed", "analyzed", "conservative extension", "outside FAR scope"}
REGISTRY_RESOLUTIONS = {"unresolved", "fits FAR", "conservative extension", "outside scope"}
ADVERSARIAL_STATUSES = {
    "resolved by existing primitive",
    "conservative extension",
    "unresolved pressure",
    "candidate primitive failure",
}
REQUIRED_EVIDENCE_FIELDS = {
    "id",
    "system",
    "fixture",
    "classification",
    "analysis_status",
    "registry_resolution",
    "confidence",
    "review_status",
    "notes",
}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def check_unique(items, field, label, errors):
    seen = set()
    for item in items:
        value = item.get(field)
        if value in seen:
            errors.append(f"duplicate {label} {value!r}")
        seen.add(value)


def main() -> int:
    errors: list[str] = []

    evidence_path = ROOT / "theory/evaluation/evidence-registry.yaml"
    evidence = load_yaml(evidence_path) or {}
    entries = evidence.get("entries", [])
    check_unique(entries, "id", "evidence id", errors)
    for entry in entries:
        missing = REQUIRED_EVIDENCE_FIELDS - set(entry)
        if missing:
            errors.append(f"{entry.get('id', '<missing id>')}: missing fields {sorted(missing)}")
        if entry.get("classification") not in EVIDENCE_CLASSIFICATIONS:
            errors.append(f"{entry.get('id')}: unknown classification {entry.get('classification')!r}")
        if entry.get("analysis_status") not in ANALYSIS_STATUSES:
            errors.append(f"{entry.get('id')}: unknown analysis_status {entry.get('analysis_status')!r}")
        if entry.get("registry_resolution") not in REGISTRY_RESOLUTIONS:
            errors.append(f"{entry.get('id')}: unknown registry_resolution {entry.get('registry_resolution')!r}")
        fixture = entry.get("fixture")
        if fixture and not (ROOT / fixture).is_file():
            errors.append(f"{entry.get('id')}: fixture does not exist: {fixture}")

    adv_path = ROOT / "theory/falsification/adversarial-test-suite.yaml"
    adversarial = load_yaml(adv_path) or {}
    tests = adversarial.get("tests", [])
    check_unique(tests, "id", "adversarial id", errors)
    for test in tests:
        if test.get("current_status") not in ADVERSARIAL_STATUSES:
            errors.append(f"{test.get('id')}: unknown current_status {test.get('current_status')!r}")
        if test.get("primitive_under_pressure") not in PRIMITIVES:
            errors.append(f"{test.get('id')}: invalid primitive_under_pressure {test.get('primitive_under_pressure')!r}")

    pressure_path = ROOT / "theory/falsification/primitive-pressure-registry.yaml"
    pressure = load_yaml(pressure_path) or {}
    pressure_entries = pressure.get("primitives", [])
    check_unique(pressure_entries, "primitive", "pressure primitive", errors)
    for entry in pressure_entries:
        if entry.get("primitive") not in PRIMITIVES:
            errors.append(f"invalid pressure-registry primitive {entry.get('primitive')!r}")

    if errors:
        print("Evaluation consistency check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Evaluation consistency check passed: "
        f"{len(entries)} evidence entries, {len(tests)} adversarial tests, "
        f"{len(pressure_entries)} primitive pressure entries."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
