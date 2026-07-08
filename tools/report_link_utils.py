#!/usr/bin/env python3
"""Helpers for stable relative links in generated Markdown reports."""
from __future__ import annotations

import os
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def repo_path(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else ROOT / p


def repo_label(path: str | Path) -> str:
    p = repo_path(path)
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()


def relative_href(target_path: str | Path, from_file: str | Path) -> str:
    target = repo_path(target_path)
    source = repo_path(from_file)
    rel = Path(os.path.relpath(target, source.parent)).as_posix()
    return quote(rel, safe="/#.-_")


def markdown_link(target_path: str | Path, from_file: str | Path, label: str | None = None) -> str:
    label = label or repo_label(target_path)
    return f"[{label}]({relative_href(target_path, from_file)})"


def markdown_line_link(target_path: str | Path, from_file: str | Path, line: int | None = None, label: str | None = None) -> str:
    if line is None:
        return markdown_link(target_path, from_file, label)
    label = label or f"{repo_label(target_path)}:L{line}"
    return f"[{label}]({relative_href(target_path, from_file)}#L{line})"


def slugify_heading(text: str) -> str:
    slug = text.strip().lower()
    slug = re.sub(r"[`*_~\[\]()]+", "", slug)
    slug = re.sub(r"[^a-z0-9 -]", "", slug)
    return re.sub(r"\s+", "-", slug).strip("-")


def existing_file(path: str | Path) -> bool:
    p = repo_path(path)
    return p.exists() and p.is_file()
