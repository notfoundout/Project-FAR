#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common_health import ROOT

CERTIFICATION_ARTIFACTS = [
    "docs/governance/repository-certification-standard.md",
    "docs/audits/repository-certification-inventory-audit.md",
    "docs/audits/semantic-certification-report.md",
    "docs/glossary/canonical-vocabulary-index.md",
    "docs/audits/repository-architecture-certification-report.md",
    "docs/audits/documentation-standardization-report.md",
    "docs/certification/README.md",
    "docs/architecture/repository-domain-registry.md",
    "docs/audits/repository-compliance-enforcement-report.md",
]

NAVIGATION_FILES = [
    "README.md",
    "docs/README.md",
    "docs/CANONICAL_MAP.md",
    "docs/certification/README.md",
]

DOMAIN_ROOTS = [
    ".github",
    "archive",
    "assets",
    "conformance",
    "docs",
    "examples",
    "foundations",
    "frameworks",
    "jsonschema",
    "mechanization",
    "methodology",
    "papers",
    "reports",
    "research",
    "schemas",
    "tests",
    "theory",
    "tools",
]

DOCUMENTATION_CHILD_ROOTS = [
    "docs/architecture",
    "docs/audits",
    "docs/certification",
    "docs/doctrine",
    "docs/glossary",
    "docs/governance",
    "docs/maintenance",
    "docs/mechanization",
    "docs/methodology",
    "docs/milestones",
    "docs/planning",
    "docs/principles",
    "docs/releases",
    "docs/reports",
    "docs/roadmap",
]

STANDARD_SECTIONS = [
    "## Purpose",
    "## Why?",
    "## Scope",
    "## Role in Project FAR",
    "## Dependencies",
    "## Dependents",
    "## Design Rationale",
]

errors: list[str] = []


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def exists(relative: str) -> bool:
    return (ROOT / relative).exists()


for artifact in CERTIFICATION_ARTIFACTS:
    if not exists(artifact):
        errors.append(f"missing certification artifact: {artifact}")

for nav in NAVIGATION_FILES:
    if not exists(nav):
        errors.append(f"missing navigation file: {nav}")
        continue
    text = read(nav)
    for artifact in CERTIFICATION_ARTIFACTS:
        if nav == artifact:
            continue
        if artifact not in text and artifact.replace("docs/", "") not in text:
            errors.append(f"{nav}: missing navigation reference to {artifact}")

for root in DOMAIN_ROOTS + DOCUMENTATION_CHILD_ROOTS:
    if not exists(root):
        errors.append(f"registered domain root missing: {root}")

for artifact in [
    "docs/audits/documentation-standardization-report.md",
    "docs/certification/README.md",
    "docs/architecture/repository-domain-registry.md",
    "docs/audits/repository-compliance-enforcement-report.md",
]:
    if not exists(artifact):
        continue
    text = read(artifact)
    for section in STANDARD_SECTIONS:
        if section not in text:
            errors.append(f"{artifact}: missing standard section {section}")

registry = read("docs/architecture/repository-domain-registry.md") if exists("docs/architecture/repository-domain-registry.md") else ""
for root in DOMAIN_ROOTS:
    if f"`{root}/`" not in registry and f"`{root}`" not in registry:
        errors.append(f"docs/architecture/repository-domain-registry.md: missing registered root {root}")

index = read("docs/certification/README.md") if exists("docs/certification/README.md") else ""
for artifact in CERTIFICATION_ARTIFACTS:
    name = Path(artifact).name
    if name not in index:
        errors.append(f"docs/certification/README.md: missing indexed artifact {artifact}")

if errors:
    print("Certification compliance check failed:")
    for error in errors:
        print(f"FAIL {error}")
    raise SystemExit(1)

print("Certification compliance OK")
