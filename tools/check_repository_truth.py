#!/usr/bin/env python3
"""Fail-closed repository status/version authority check."""
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

    readme = read_text("README.md")
    required_phrases = (
        "The deductive UPP queue is closed.",
        "The active phase is independent criticism, countermodel search, proof review, kernel-checked reconstruction, bounded replication, and application-correspondence testing.",
        "Historical bounded-program status",
    )
    for phrase in required_phrases:
        if phrase not in readme:
            fail(f"README missing required status authority phrase: {phrase}")

    if "Current project phase: W3.5" in readme:
        fail("historical W3.5 dashboard is still presented as the current project phase")
    if "/releases/tag/v0.4.0" in readme:
        fail("README release surface pins stale v0.4.0 tag")

    report = {
        "schema": authority["schema"],
        "successful": True,
        "package_version": package_version,
        "status_authority": authority["project_status"]["authority"],
        "current_phase": authority["project_status"]["current_phase"],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
