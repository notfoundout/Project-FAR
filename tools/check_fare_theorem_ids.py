#!/usr/bin/env python3
"""Check active FARE mathematics theorem identifiers for uniqueness."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROOFS_ROOT = ROOT / "frameworks" / "FARE" / "mathematics" / "proofs"
IDENTIFIER_HEADING = re.compile(r"^##\s+Identifier\s*$")
THEOREM_ID = re.compile(r"^MT-\d{3}$")


def active_markdown_files(proofs_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(proofs_root.rglob("*.md")):
        relative = path.relative_to(proofs_root)
        if "archive" in relative.parts:
            continue
        files.append(path)
    return files


def identifiers_in(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    found: list[str] = []
    for index, line in enumerate(lines):
        if not IDENTIFIER_HEADING.fullmatch(line.strip()):
            continue
        for candidate in lines[index + 1 :]:
            value = candidate.strip()
            if not value:
                continue
            if value == "---" or value.startswith("#"):
                break
            if THEOREM_ID.fullmatch(value):
                found.append(value)
            break
    return found


def duplicate_active_ids(
    proofs_root: Path = DEFAULT_PROOFS_ROOT,
) -> dict[str, list[Path]]:
    by_id: dict[str, list[Path]] = defaultdict(list)
    if not proofs_root.exists():
        return {}
    for path in active_markdown_files(proofs_root):
        for identifier in identifiers_in(path):
            by_id[identifier].append(path)
    return {
        identifier: paths
        for identifier, paths in sorted(by_id.items())
        if len(paths) > 1
    }


def validate(proofs_root: Path = DEFAULT_PROOFS_ROOT) -> list[str]:
    issues: list[str] = []
    for identifier, paths in duplicate_active_ids(proofs_root).items():
        rendered = ", ".join(
            str(path.relative_to(proofs_root)).replace("\\", "/")
            for path in paths
        )
        issues.append(f"duplicate active FARE theorem id {identifier}: {rendered}")
    return issues


def main() -> int:
    issues = validate()
    for issue in issues:
        print(f"FAIL {issue}")
    if issues:
        return 1
    print("Active FARE theorem identifiers are unique")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
