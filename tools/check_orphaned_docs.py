#!/usr/bin/env python3
"""Report Markdown documents that are unreachable from repository navigation."""

from __future__ import annotations

import argparse
import re
from collections import deque
from pathlib import Path

from common_health import ROOT, is_ignored_link, markdown_links, rel, strip_anchor

SCAN_ROOTS = ("docs", "theory", "frameworks", "foundations", "methodology", "research", "papers")
ROOT_DOCUMENTS = (
    "README.md",
    "docs/CANONICAL_MAP.md",
    "docs/OVERVIEW.md",
    "docs/project-status.md",
)
INLINE_PATH = re.compile(r"`([^`\n]+\.md(?:#[^`\s]+)?)`")
ORPHAN_OK_MARKER = re.compile(r"(?m)^[ \t]*<!-- orphan-ok -->[ \t]*$")


def referenced_documents(path: Path, text: str, root: Path = ROOT) -> set[Path]:
    """Return existing Markdown targets explicitly referenced by *path*.

    Project indexes historically use both Markdown links and inline-code paths.
    An exact, resolvable inline path is navigation (unlike an incidental filename
    in prose), so both established forms participate in reachability.
    """
    targets = {target for _, target, _, _ in markdown_links(text)}
    targets.update(match.group(1) for match in INLINE_PATH.finditer(text))
    resolved: set[Path] = set()
    for target in targets:
        if is_ignored_link(target):
            continue
        clean = strip_anchor(target)
        if not clean:
            continue
        candidate = (path.parent / clean).resolve()
        if not candidate.exists():
            candidate = (root / clean).resolve()
        if candidate.is_dir():
            candidate /= "README.md"
        if candidate.exists() and candidate.suffix.lower() == ".md":
            resolved.add(candidate)
    return resolved


def find_orphans(root: Path = ROOT) -> list[Path]:
    roots = [root / item for item in ROOT_DOCUMENTS]
    roots += list((root / "frameworks").glob("*/README.md"))
    roots += list((root / "docs" / "releases").glob("*.md"))
    # Audit records are report-class evidence under the repository-domain
    # policy even though their filenames conventionally end in ``-audit``.
    roots += list((root / "docs" / "audits").glob("*.md"))
    roots += list((root / "docs").glob("**/*report*.md"))
    # Research records are intentionally isolated report/evidence artifacts;
    # their authority comes from their registered execution, not navigation.
    roots += list((root / "docs" / "research").glob("*.md"))
    roots += list((root / "research").glob("**/*.md"))
    # A versioned experiment/execution README is the package entry point.
    roots += list((root / "theory" / "evaluation" / "comparative-representation" / "experiments").glob("*/README.md"))
    roots += list((root / "theory" / "independence").glob("**/README.md"))
    roots += list((root / "theory" / "scope").glob("*/README.md"))

    all_docs = {
        path.resolve()
        for scan_root in SCAN_ROOTS
        if (root / scan_root).exists()
        for path in (root / scan_root).rglob("*.md")
        if "archive" not in path.relative_to(root).parts
        and not ORPHAN_OK_MARKER.search(path.read_text(encoding="utf-8", errors="replace"))
    }
    seen: set[Path] = set()
    queue = deque(path.resolve() for path in roots if path.exists())
    while queue:
        path = queue.popleft()
        if path in seen or not path.exists() or path.suffix.lower() != ".md":
            continue
        seen.add(path)
        queue.extend(referenced_documents(path, path.read_text(encoding="utf-8", errors="replace"), root) - seen)
    return sorted(all_docs - seen)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    orphans = find_orphans()
    for path in orphans:
        print(f"WARN orphaned doc: {rel(path)}")
    if args.strict and orphans:
        return 1
    print("Orphaned doc check completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
