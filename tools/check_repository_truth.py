#!/usr/bin/env python3
"""Fail-closed repository status/version/release authority check."""
from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = ROOT / "governance/repository-truth-authority-v1.json"


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
    if status.get("governing_core") != "PROJECT-FAR-CORE-THEORY-1.0":
        fail("governing core-theory authority drift")
    if status.get("current_program") != "POST-CLOSURE-001":
        fail("current program authority drift")

    readme = read_text("README.md")
    required_phrases = (
        f"## Latest release: {latest_release}",
        f"The latest published GitHub repository release is [{latest_release}]",
        "These are separate version surfaces",
        "`PROJECT-FAR-CORE-THEORY-1.0`",
        "## Post-closure phase",
        "The active program is `POST-CLOSURE-001`.",
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
        "current_program": status["current_program"],
        "current_phase": status["current_phase"],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
