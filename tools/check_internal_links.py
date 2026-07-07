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
MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_LINK = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']")
YAML_KEY_VALUE = re.compile(r"^\s*-?\s*([A-Za-z0-9_.-]+)\s*:\s*(.+?)\s*$")
PATH_WITH_EXTENSION = re.compile(r"(?<![A-Za-z0-9_./-])([A-Za-z0-9_./-]+\.(?:md|png|svg|pdf|tex|jpg|jpeg|gif))(?![A-Za-z0-9_./-])")


def is_external(link: str) -> bool:
    parsed = urlparse(link)
    return parsed.scheme in {"http", "https", "mailto", "tel"} or link.startswith("#")


def clean_link(link: str) -> str:
    link = link.strip().strip('"\'')
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


def extract_yaml_links(line: str) -> list[str]:
    match = YAML_KEY_VALUE.match(line)
    if not match:
        return []
    key, value = match.groups()
    value = value.split(" #", 1)[0].strip().rstrip(",")
    if not value or value in {"[]", "{}"}:
        return []
    links: list[str] = []
    links.extend(match.group(1) for match in PATH_WITH_EXTENSION.finditer(value))
    # Preserve order while avoiding duplicate reports from key/value matches.
    return list(dict.fromkeys(links))


def extract_links(path: Path, line: str) -> list[str]:
    links: list[str] = []
    for pattern in (MARKDOWN_IMAGE, MARKDOWN_LINK, HTML_LINK):
        links.extend(match.group(1) for match in pattern.finditer(line))
    if path.suffix.lower() in {".yaml", ".yml"}:
        links.extend(extract_yaml_links(line))
    return links


def resolve_target(path: Path, link: str) -> Path:
    decoded = unquote(link)
    if decoded.startswith("/"):
        return ROOT / decoded.lstrip("/")
    relative_target = (path.parent / decoded).resolve()
    if relative_target.exists():
        return relative_target
    root_target = (ROOT / decoded).resolve()
    if root_target.exists():
        return root_target
    return relative_target


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
                target = resolve_target(path, link)
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
        print(f"Broken links: {len(broken)}")
        return 1
    print("INTERNAL LINK CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
