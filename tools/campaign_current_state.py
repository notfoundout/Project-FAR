#!/usr/bin/env python3
"""Separate what a completed campaign froze from what the repository currently documents.

A completed campaign manifest records the bytes of every artifact **as of execution**. Some of
those artifacts are experimental inputs, outputs, or recorded results, which must never change.
Others are living documentation surfaces — the README, the canonical map, governance registers —
which necessarily change as the repository continues.

Rewriting the manifest when a documentation surface changes makes the two indistinguishable: the
manifest then asserts that post-execution bytes were the executed bytes. Git history is not a
substitute for that distinction, because the manifest is what the checker reads.

This module keeps both facts explicit:

* ``manifest.json`` is historical evidence and is never rewritten;
* a **current-state supplement** records, for each artifact whose bytes have legitimately moved
  since execution, the executed digest, the current digest, and the reason;
* an artifact in the campaign's **protected set** may never appear in the supplement, so an
  experimental input, output, or recorded result cannot be re-pointed at post-execution bytes.

Undeclared drift still fails closed: an artifact that differs from the manifest with no
supplement entry is an error, exactly as before.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REQUIRED_ENTRY_FIELDS = ("path", "executed_sha256", "current_sha256", "class", "reason")


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_supplement(path: Path, prefix: str) -> tuple[dict[str, Mapping[str, Any]], list[str]]:
    """Return (entries by path, errors). A missing supplement is valid and means no drift."""
    if not path.is_file():
        return {}, []
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"{prefix}_SUPPLEMENT_UNREADABLE {exc}"]
    if not isinstance(document, Mapping):
        return {}, [f"{prefix}_SUPPLEMENT_INVALID not an object"]

    entries: dict[str, Mapping[str, Any]] = {}
    errors: list[str] = []
    raw = document.get("entries")
    if not isinstance(raw, list):
        return {}, [f"{prefix}_SUPPLEMENT_INVALID entries must be a list"]
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping) or any(
            not isinstance(item.get(field), str) or not item.get(field)
            for field in REQUIRED_ENTRY_FIELDS
        ):
            errors.append(f"{prefix}_SUPPLEMENT_ENTRY_INVALID index={index}")
            continue
        rel = str(item["path"])
        if rel in entries:
            errors.append(f"{prefix}_SUPPLEMENT_DUPLICATE {rel}")
        entries[rel] = item
    return entries, errors


def artifact_hash_errors(
    root: Path,
    manifest_hashes: Mapping[str, str],
    supplement_path: Path,
    protected_paths: Iterable[str],
    prefix: str,
) -> list[str]:
    """Check current bytes against the executed manifest, allowing declared documentation drift.

    ``manifest_hashes`` maps repository-relative path to the digest recorded at execution.
    ``protected_paths`` are artifacts that may never drift: experimental inputs, outputs, and
    recorded results.
    """
    entries, errors = load_supplement(supplement_path, prefix)
    protected = set(protected_paths)

    unknown = sorted(set(entries) - set(manifest_hashes))
    if unknown:
        errors.append(f"{prefix}_SUPPLEMENT_UNKNOWN_ARTIFACT {unknown}")

    forbidden = sorted(set(entries) & protected)
    if forbidden:
        errors.append(
            f"{prefix}_SUPPLEMENT_FORBIDDEN_FOR_PROTECTED_ARTIFACT {forbidden}: "
            "experimental inputs, outputs and recorded results may not be re-pointed at "
            "post-execution bytes"
        )

    for rel in sorted(manifest_hashes):
        path = root / rel
        if not path.is_file():
            errors.append(f"{prefix}_ARTIFACT_MISSING {rel}")
            continue
        executed = manifest_hashes[rel]
        actual = sha256_of(path)
        if actual == executed:
            if rel in entries:
                errors.append(
                    f"{prefix}_SUPPLEMENT_STALE {rel}: artifact matches the executed manifest, "
                    "so its supplement entry must be removed"
                )
            continue
        entry = entries.get(rel)
        if entry is None:
            errors.append(
                f"{prefix}_ARTIFACT_HASH_MISMATCH {rel}: executed={executed} actual={actual}; "
                "declare the change in the current-state supplement or restore the bytes"
            )
            continue
        if entry["executed_sha256"] != executed:
            errors.append(
                f"{prefix}_SUPPLEMENT_EXECUTED_DIGEST_DRIFT {rel}: "
                f"supplement={entry['executed_sha256']} manifest={executed}"
            )
        if entry["current_sha256"] != actual:
            errors.append(
                f"{prefix}_SUPPLEMENT_CURRENT_DIGEST_DRIFT {rel}: "
                f"supplement={entry['current_sha256']} actual={actual}"
            )
    return sorted(set(errors))


def manifest_hash_map(
    artifacts: Sequence[Mapping[str, Any]], prefix: str
) -> tuple[dict[str, str], list[str]]:
    """Extract path -> executed digest from a campaign manifest artifact list."""
    hashes: dict[str, str] = {}
    errors: list[str] = []
    for index, item in enumerate(artifacts):
        if not isinstance(item, Mapping):
            errors.append(f"{prefix}_ARTIFACT_ENTRY_INVALID index={index}")
            continue
        rel, digest = item.get("path"), item.get("sha256")
        if not isinstance(rel, str) or not isinstance(digest, str):
            errors.append(f"{prefix}_ARTIFACT_ENTRY_INVALID index={index}")
            continue
        if rel in hashes:
            errors.append(f"{prefix}_ARTIFACT_DUPLICATE {rel}")
        hashes[rel] = digest
    return hashes, errors
