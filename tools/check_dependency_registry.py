#!/usr/bin/env python3
"""Validate Project FAR dependency registry records."""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "theory/dependencies/dependency-schema.yaml"
REGISTRY = ROOT / "theory/dependencies/dependency-registry.yaml"
REQUIRED = [
    "id", "source", "source_type", "target", "target_type", "relationship",
    "confidence", "status", "evidence", "notes",
]
PATH_PREFIXES = (
    "README.md", "Makefile", ".github/", "docs/", "theory/", "tools/",
    "examples/", "tests/", "reports/", "foundations/", "frameworks/", "papers/",
    "mechanization/", "archive/", "research/", "methodology/",
)


def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise ValueError(f"missing required file: {path.relative_to(ROOT)}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path.relative_to(ROOT)}")
    return data


def allowed(schema: dict, field: str) -> set[str]:
    values = schema.get("record", {}).get("fields", {}).get(field, {}).get("allowed_values")
    if not isinstance(values, list):
        raise ValueError(f"schema missing allowed values for {field}")
    return {str(v) for v in values}


def looks_like_repo_path(value: str) -> bool:
    return value.startswith(PATH_PREFIXES)


def validate() -> list[str]:
    errors: list[str] = []
    try:
        schema = load_yaml(SCHEMA)
        registry = load_yaml(REGISTRY)
    except ValueError as exc:
        return [str(exc)]

    schema_required = schema.get("record", {}).get("required_fields")
    if schema_required != REQUIRED:
        errors.append("schema required_fields does not match dependency validator requirements")

    type_values = allowed(schema, "source_type")
    target_type_values = allowed(schema, "target_type")
    relationship_values = allowed(schema, "relationship")
    status_values = allowed(schema, "status")
    confidence_values = allowed(schema, "confidence")

    dependencies = registry.get("dependencies")
    if not isinstance(dependencies, list):
        errors.append("registry dependencies must be a list")
        return errors

    seen: set[str] = set()
    for index, dep in enumerate(dependencies, start=1):
        label = dep.get("id", f"record #{index}") if isinstance(dep, dict) else f"record #{index}"
        if not isinstance(dep, dict):
            errors.append(f"{label}: dependency record must be a mapping")
            continue
        for field in REQUIRED:
            if field not in dep or dep[field] in (None, ""):
                errors.append(f"{label}: missing required field {field}")
        dep_id = str(dep.get("id", ""))
        if dep_id in seen:
            errors.append(f"{label}: duplicate id {dep_id}")
        seen.add(dep_id)
        if dep.get("source_type") not in type_values:
            errors.append(f"{label}: invalid source_type {dep.get('source_type')}")
        if dep.get("target_type") not in target_type_values:
            errors.append(f"{label}: invalid target_type {dep.get('target_type')}")
        if dep.get("relationship") not in relationship_values:
            errors.append(f"{label}: invalid relationship {dep.get('relationship')}")
        if dep.get("status") not in status_values:
            errors.append(f"{label}: invalid status {dep.get('status')}")
        if dep.get("confidence") not in confidence_values:
            errors.append(f"{label}: invalid confidence {dep.get('confidence')}")
        source = str(dep.get("source", ""))
        target = str(dep.get("target", ""))
        for role, value in (("source", source), ("target", target)):
            if looks_like_repo_path(value) and not (ROOT / value).exists():
                errors.append(f"{label}: {role} path does not exist: {value}")
        if source == target and "self" not in str(dep.get("notes", "")).lower():
            errors.append(f"{label}: self-dependency requires explicit self-dependency notes")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("DEPENDENCY REGISTRY CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    count = len(load_yaml(REGISTRY).get("dependencies", []))
    print("DEPENDENCY REGISTRY CHECK PASSED")
    print(f"records: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
