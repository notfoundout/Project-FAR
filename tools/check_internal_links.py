#!/usr/bin/env python3
"""Check internal Markdown and YAML repository links."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SUFFIXES = {".md", ".yaml", ".yml"}
SKIP_DIRS = {".git", ".github"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
HTML_LINK = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")
YAML_PATH = re.compile(r"(?:^|\s)([A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+)")


def is_external(link: str) -> bool:
    parsed = urlparse(link)
    return parsed.scheme in {"http", "https", "mailto", "tel"} or link.startswith("#")


def clean_link(link: str) -> str:
    link = link.strip()
    if link.startswith("<") and link.endswith(">"):
        link = link[1:-1]
    return link.split("#", 1)[0].split("?", 1)[0]


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUFFIXES:
            continue
        if set(path.relative_to(ROOT).parts) & SKIP_DIRS:
            continue
        files.append(path)
    return sorted(files)


def extract_links(path: Path, line: str) -> list[str]:
    links: list[str] = []
    for pattern in (MARKDOWN_LINK, HTML_LINK):
        links.extend(match.group(1) for match in pattern.finditer(line))
    if path.suffix.lower() in {".yaml", ".yml"}:
        links.extend(match.group(1).rstrip(",.;)]}") for match in YAML_PATH.finditer(line))
    return links


def check() -> list[str]:
    broken: list[str] = []
    for path in iter_files():
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_no, line in enumerate(lines, start=1):
            for raw in extract_links(path, line):
                link = clean_link(raw)
                if not link or is_external(link):
                    continue
                target = ROOT / link.lstrip("/") if link.startswith("/") else (path.parent / unquote(link)).resolve()
                try:
                    rel_target = target.relative_to(ROOT)
                except ValueError:
                    continue
                if not target.exists():
                    broken.append(f"{path.relative_to(ROOT)}:{line_no}: {raw} -> {rel_target}")
    return broken


def main() -> int:
    broken = check()
    if broken:
        print("INTERNAL LINK CHECK FAILED")
        for item in broken:
            print(f"- {item}")
        return 1
    print("INTERNAL LINK CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
