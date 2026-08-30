#!/usr/bin/env python3
"""Fail-closed repository status/version/release authority check."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = ROOT / "governance/repository-truth-authority-v1.json"
EXPECTED_CORE = "PROJECT-FAR-CORE-THEORY-1.1"
HISTORICAL_CORE = "PROJECT-FAR-CORE-THEORY-1.0"
HISTORICAL_CORE_PATH = "theory/theorems/Project-FAR-Theory-Closure-v1.0.md"
EXPECTED_V1_SHA256 = "b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5"
EXPECTED_EXPORT_VERSION = "1.2.0"


def fail(message: str) -> None:
    raise SystemExit(f"repository-truth: {message}")


def read_text(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        fail(f"missing required file: {path}")
    return target.read_text(encoding="utf-8")


def extract(pattern: str, text: str, source: str) -> str:
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        fail(f"unable to resolve version declaration in {source}")
    return match.group(1)


def main() -> int:
    authority = json.loads(AUTHORITY.read_text(encoding="utf-8"))
    if authority.get("schema") != "project-far/repository-truth-authority/1.0":
        fail("unsupported or missing authority schema")

    pyproject = tomllib.loads(read_text("pyproject.toml"))
    package_version = str(pyproject["project"]["version"])
    init_version = extract(
        r'^__version__\s*=\s*["\']([^"\']+)["\']',
        read_text("mechanization/far_mechanization/__init__.py"),
        "mechanization/far_mechanization/__init__.py",
    )
    cli_version = extract(
        r'^CLI_VERSION\s*=\s*["\']([^"\']+)["\']',
        read_text("mechanization/far_mechanization/cli.py"),
        "mechanization/far_mechanization/cli.py",
    )
    versions = {
        "pyproject.toml": package_version,
        "mechanization/far_mechanization/__init__.py": init_version,
        "mechanization/far_mechanization/cli.py": cli_version,
    }
    if len(set(versions.values())) != 1:
        fail("package version drift: " + json.dumps(versions, sort_keys=True))

    release = authority.get("release_surface", {})
    latest_release = release.get("latest_release")
    if not isinstance(latest_release, str) or not re.fullmatch(r"v\d+\.\d+\.\d+", latest_release):
        fail("release authority latest_release is missing or malformed")

    status = authority.get("project_status", {})
    if status.get("current_phase") != "post-closure assurance and application":
        fail("project-status phase authority drift")
    if status.get("governing_core") != EXPECTED_CORE:
        fail("governing core-theory authority drift")
    if status.get("governing_core_source") != "theory/theorems/Project-FAR-Theory-Closure-v1.1.md":
        fail("governing core-theory source drift")
    if status.get("historical_core") != HISTORICAL_CORE:
        fail("historical core-theory identity drift")
    if status.get("historical_core_sha256") != EXPECTED_V1_SHA256:
        fail("historical core-theory hash authority drift")
    if status.get("current_program") != "POST-CLOSURE-001":
        fail("current program authority drift")
    if status.get("completed_assurance_workstream") != "PCA-W2-PROOF-ASSISTANT-FORMALIZATION":
        fail("completed W2 assurance authority drift")
    if status.get("completed_contract_schema_workstream") != "PCA-W3-CONTRACT-SCHEMA":
        fail("completed W3 contract-schema authority drift")
    if status.get("active_workstream") != "PCA-W4-DOMAIN-CONTRACTS":
        fail("active workstream authority drift")
    if status.get("independent_review_status") != "complete_confirmed_14_proved_exact_scopes_novelty_not_established":
        fail("independent-review authority drift")
    if status.get("formalization_status") != "14_formalized_0_partial_obstruction_0_contradiction":
        fail("formalization authority drift")
    if status.get("contract_schema_status") != "far-ir_2.0_versioned_successor_complete_finite_explicit_semantic_checks_v1_unchanged":
        fail("W3 contract-schema status authority drift")

    historical_bytes = (ROOT / HISTORICAL_CORE_PATH).read_bytes()
    if hashlib.sha256(historical_bytes).hexdigest() != EXPECTED_V1_SHA256:
        fail("historical v1.0 core bytes changed")

    export_authority = authority.get("specification_export", {})
    if export_authority.get("export_version") != EXPECTED_EXPORT_VERSION:
        fail("specification export authority version drift")
    if export_authority.get("governing_core") != EXPECTED_CORE:
        fail("specification export governing-core drift")
    if export_authority.get("historical_core_status") != "historical":
        fail("specification export historical-core status drift")

    manifest = json.loads(read_text("exports/far-spec-v1/manifest.json"))
    if manifest.get("export_version") != EXPECTED_EXPORT_VERSION:
        fail("specification export manifest version drift")
    if manifest.get("core_theory_id") != EXPECTED_CORE:
        fail("specification export manifest core-theory drift")
    entries = {row.get("path"): row for row in manifest.get("artifacts", [])}
    historical_entry = entries.get("theorems/Project-FAR-Theory-Closure-v1.0.md", {})
    if historical_entry.get("status") != "historical" or historical_entry.get("sha256") != EXPECTED_V1_SHA256:
        fail("specification export does not preserve v1.0 as historical")
    current_entry = entries.get("theorems/Project-FAR-Theory-Closure-v1.1.md", {})
    if current_entry.get("status") != "canonical":
        fail("specification export does not mark v1.1 theorem canonical")
    ledger_entry = entries.get("theorems/project-far-core-theory-v1.1.json", {})
    if ledger_entry.get("status") != "canonical":
        fail("specification export does not mark v1.1 ledger canonical")

    readme = read_text("README.md")
    required_phrases = (
        f"## Latest release: {latest_release}",
        f"The latest published GitHub repository release is [{latest_release}]",
        "These are separate version surfaces",
        f"`{EXPECTED_CORE}`",
        "Historical v1.0",
        "## Post-closure phase",
        "The active program is `POST-CLOSURE-001`.",
        "`PCA-W3-CONTRACT-SCHEMA`: complete.",
        "`PCA-W4-DOMAIN-CONTRACTS`: **next**.",
        "Core theory reopens only for a reproducible contradiction",
        "Historical bounded-program status",
    )
    for phrase in required_phrases:
        if phrase not in readme:
            fail(f"README missing required authority phrase: {phrase}")

    if "Current project phase: W3.5" in readme:
        fail("historical W3.5 dashboard is still presented as the current project phase")

    badge_pattern = re.compile(
        r'^\[!\[Release ([^\]]+)\]\([^\n]+\)\]\(([^\n]+)\)$', re.MULTILINE
    )
    badge = badge_pattern.search(readme)
    if not badge:
        fail("README release badge is missing or malformed")
    if badge.group(1) != latest_release:
        fail(f"README release badge drift: {badge.group(1)} != {latest_release}")
    if badge.group(2) != "https://github.com/notfoundout/Project-FAR/releases/latest":
        fail("README release badge must target the GitHub latest-release route")

    release_record = str(release.get("release_record", ""))
    record = read_text(release_record)
    if f"# Project FAR {latest_release}" not in record:
        fail("release record does not match latest release authority")
    if f"/releases/tag/{latest_release}" not in record:
        fail("release record does not link to the authoritative GitHub release")

    report = {
        "schema": authority["schema"],
        "successful": True,
        "package_version": package_version,
        "latest_release": latest_release,
        "status_authority": status["authority"],
        "governing_core": status["governing_core"],
        "historical_core": status["historical_core"],
        "historical_core_sha256": status["historical_core_sha256"],
        "specification_export_version": export_authority["export_version"],
        "current_program": status["current_program"],
        "active_workstream": status["active_workstream"],
        "completed_contract_schema_workstream": status["completed_contract_schema_workstream"],
        "contract_schema_status": status["contract_schema_status"],
        "independent_review_status": status["independent_review_status"],
        "formalization_status": status["formalization_status"],
        "current_phase": status["current_phase"],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
