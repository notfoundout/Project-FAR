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
  experimental input, output, or recorded result cannot be re-pointed at post-execution bytes;
* every protected path must name a real artifact in the executed manifest, so a misspelling cannot
  silently disable protection;
* an executed input whose live path was later repaired may be preserved as a **frozen copy**: the
  copy must be byte-identical to the executed manifest digest, the campaign recomputes from it,
  and only then may the live path drift under a supplement declaration.

Undeclared drift still fails closed: an artifact that differs from the manifest with no
supplement entry is an error, exactly as before.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REQUIRED_ENTRY_FIELDS = ("path", "executed_sha256", "current_sha256", "class", "reason")


@dataclass(frozen=True, slots=True)
class ArtifactFinding:
    """One provenance finding, before it is rendered into a campaign's error vocabulary.

    Campaigns differ in how they report errors: `PCA-W5`/`PCA-W6` emit prefixed strings while
    `PCA-W4` emits structured `{code, message}` records. The comparison itself is identical, so
    it is performed once here and each campaign renders these findings in its own vocabulary.
    """

    kind: str
    path: str
    detail: str


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


def compare_campaign_artifacts(
    root: Path,
    manifest_hashes: Mapping[str, str],
    supplement_path: Path,
    protected_paths: Iterable[str],
    frozen_copies: Mapping[str, str] | None = None,
) -> list[ArtifactFinding]:
    """Compare current bytes against the executed manifest, allowing declared drift.

    ``manifest_hashes`` maps repository-relative path to the digest recorded at execution.
    ``protected_paths`` are artifacts that may never drift: experimental inputs, outputs, and
    recorded results. Every protected path must be present in ``manifest_hashes``; otherwise the
    protection configuration itself is invalid and the comparison fails closed.

    ``frozen_copies`` maps an executed manifest path to a preserved copy of its executed bytes.
    The copy must exist and match the executed digest exactly; the live path is then compared
    like any unprotected artifact. A path may not be both protected and frozen-copied.

    Returns findings in a campaign-neutral form; callers render them in their own vocabulary.
    """
    entries, load_errors = load_supplement(supplement_path, "")
    frozen_copies = dict(frozen_copies or {})
    findings: list[ArtifactFinding] = []
    for error in load_errors:
        # load_supplement is called with an empty prefix, so each error reads
        # "_CODE detail"; split the code from its detail so rendering does not repeat it.
        kind, _, detail = error.lstrip("_").partition(" ")
        findings.append(ArtifactFinding(kind, "", detail))
    protected = set(protected_paths)
    manifest_paths = set(manifest_hashes)

    for live, copy in sorted(frozen_copies.items()):
        if live not in manifest_paths:
            findings.append(ArtifactFinding("FROZEN_COPY_NOT_IN_MANIFEST", live, f"{live}: frozen copies must preserve an executed manifest artifact"))
            continue
        if live in protected:
            findings.append(ArtifactFinding("FROZEN_COPY_OF_PROTECTED_PATH", live, f"{live}: a path is either protected in place or preserved as a frozen copy, not both"))
        copy_path = root / copy
        if not copy_path.is_file():
            findings.append(ArtifactFinding("FROZEN_COPY_MISSING", copy, f"{copy}: preserved executed bytes of {live} are missing"))
        elif sha256_of(copy_path) != manifest_hashes[live]:
            findings.append(ArtifactFinding("FROZEN_COPY_MISMATCH", copy, f"{copy}: executed={manifest_hashes[live]} actual={sha256_of(copy_path)}"))

    orphaned_protected = sorted(protected - manifest_paths)
    if orphaned_protected:
        findings.append(
            ArtifactFinding(
                "PROTECTED_ARTIFACT_NOT_IN_MANIFEST",
                "",
                f"{orphaned_protected}: protected paths must name artifacts in the "
                "executed manifest",
            )
        )

    unknown = sorted(set(entries) - manifest_paths)
    if unknown:
        findings.append(ArtifactFinding("SUPPLEMENT_UNKNOWN_ARTIFACT", "", f"{unknown}"))

    forbidden = sorted(set(entries) & protected)
    if forbidden:
        findings.append(
            ArtifactFinding(
                "SUPPLEMENT_FORBIDDEN_FOR_PROTECTED_ARTIFACT",
                "",
                f"{forbidden}: experimental inputs, outputs and recorded results may not be "
                "re-pointed at post-execution bytes",
            )
        )

    for rel in sorted(manifest_hashes):
        path = root / rel
        if not path.is_file():
            findings.append(ArtifactFinding("ARTIFACT_MISSING", rel, rel))
            continue
        executed = manifest_hashes[rel]
        actual = sha256_of(path)
        if actual == executed:
            if rel in entries:
                findings.append(
                    ArtifactFinding(
                        "SUPPLEMENT_STALE",
                        rel,
                        f"{rel}: artifact matches the executed manifest, so its supplement "
                        "entry must be removed",
                    )
                )
            continue
        entry = entries.get(rel)
        if entry is None:
            findings.append(
                ArtifactFinding(
                    "ARTIFACT_HASH_MISMATCH",
                    rel,
                    f"{rel}: executed={executed} actual={actual}; declare the change in the "
                    "current-state supplement or restore the bytes",
                )
            )
            continue
        if entry["executed_sha256"] != executed:
            findings.append(
                ArtifactFinding(
                    "SUPPLEMENT_EXECUTED_DIGEST_DRIFT",
                    rel,
                    f"{rel}: supplement={entry['executed_sha256']} manifest={executed}",
                )
            )
        if entry["current_sha256"] != actual:
            findings.append(
                ArtifactFinding(
                    "SUPPLEMENT_CURRENT_DIGEST_DRIFT",
                    rel,
                    f"{rel}: supplement={entry['current_sha256']} actual={actual}",
                )
            )
    return findings


def artifact_hash_errors(
    root: Path,
    manifest_hashes: Mapping[str, str],
    supplement_path: Path,
    protected_paths: Iterable[str],
    prefix: str,
    frozen_copies: Mapping[str, str] | None = None,
) -> list[str]:
    """Render :func:`compare_campaign_artifacts` findings as prefixed campaign error strings."""
    return sorted(
        {
            f"{prefix}_{finding.kind} {finding.detail}"
            for finding in compare_campaign_artifacts(
                root, manifest_hashes, supplement_path, protected_paths, frozen_copies
            )
        }
    )


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
