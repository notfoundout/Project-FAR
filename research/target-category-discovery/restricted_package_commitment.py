#!/usr/bin/env python3
"""Build deterministic restricted-package commitments without exposing file contents."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import unicodedata
from pathlib import Path, PurePosixPath


class CommitmentError(RuntimeError):
    pass


def _hash(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def normalize_relative_path(path: str) -> str:
    value = unicodedata.normalize("NFC", path)
    if not value or "\\" in value or value.startswith("/"):
        raise CommitmentError(f"unsafe path: {path!r}")
    raw_parts = value.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        raise CommitmentError(f"unsafe path: {path!r}")
    pure = PurePosixPath(value)
    return pure.as_posix()


def collect_entries(directory: Path) -> list[dict[str, object]]:
    directory = directory.resolve()
    if not directory.is_dir():
        raise CommitmentError("package root is not a directory")
    entries: list[dict[str, object]] = []
    normalized_seen: set[str] = set()
    inode_seen: set[tuple[int, int]] = set()
    for current, dirnames, filenames in os.walk(directory, followlinks=False):
        current_path = Path(current)
        for dirname in list(dirnames):
            candidate = current_path / dirname
            if candidate.is_symlink():
                raise CommitmentError(f"symlink directory rejected: {candidate}")
        for filename in filenames:
            path = current_path / filename
            if path.is_symlink() or not path.is_file():
                raise CommitmentError(f"non-regular file rejected: {path}")
            stat = path.stat()
            inode_key = (int(stat.st_dev), int(stat.st_ino))
            if stat.st_ino and inode_key in inode_seen:
                raise CommitmentError(f"hard-link alias rejected: {path}")
            if stat.st_ino:
                inode_seen.add(inode_key)
            rel = normalize_relative_path(path.relative_to(directory).as_posix())
            if rel in normalized_seen:
                raise CommitmentError(f"normalized path collision: {rel}")
            normalized_seen.add(rel)
            data = path.read_bytes()
            entries.append({
                "path": rel,
                "size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            })
    entries.sort(key=lambda item: str(item["path"]).encode("utf-8"))
    return entries


def canonical_manifest_bytes(entries: list[dict[str, object]]) -> bytes:
    payload = {"schema_version": "1.0", "files": entries}
    return (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        .encode("utf-8") + b"\n"
    )


def merkle_root(entries: list[dict[str, object]]) -> str:
    if not entries:
        return hashlib.sha256(b"empty\0").hexdigest()
    level = []
    for entry in entries:
        leaf = (
            b"leaf\0"
            + str(entry["path"]).encode("utf-8")
            + b"\0"
            + str(entry["size"]).encode("ascii")
            + b"\0"
            + str(entry["sha256"]).encode("ascii")
        )
        level.append(_hash(leaf))
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [
            _hash(b"node\0" + level[index] + level[index + 1])
            for index in range(0, len(level), 2)
        ]
    return level[0].hex()


def build_commitment(directory: Path, package_version: str, declaration_id: str, reveal_condition: str) -> dict[str, object]:
    if not package_version or not declaration_id or not reveal_condition:
        raise CommitmentError("version, declaration ID, and reveal condition are required")
    entries = collect_entries(directory)
    manifest_bytes = canonical_manifest_bytes(entries)
    return {
        "schema_version": "1.0",
        "package_version": package_version,
        "file_count": len(entries),
        "canonical_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "merkle_root": merkle_root(entries),
        "custodian_declaration_id": declaration_id,
        "reveal_condition": reveal_condition,
    }


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 4:
        print(
            "usage: restricted_package_commitment.py DIRECTORY VERSION DECLARATION_ID REVEAL_CONDITION",
            file=sys.stderr,
        )
        return 2
    try:
        result = build_commitment(Path(argv[0]), argv[1], argv[2], argv[3])
    except (OSError, CommitmentError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
