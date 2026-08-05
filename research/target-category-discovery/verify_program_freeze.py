#!/usr/bin/env python3
"""Verify the exact public-control freeze for TCD-CLEANROOM-001."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

PROGRAM_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROGRAM_DIR.parents[1]
DEFAULT_MANIFEST = PROGRAM_DIR / "freeze-manifest-v1.0.json"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
EXPECTED_PATH_LIST_SHA256 = "6fe690a6dfdb23733d4814e35154fcb72fb28943b30c6d0d73c1916f62e7fb16"


class FreezeError(RuntimeError):
    pass


def _load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FreezeError(f"invalid freeze manifest: {exc}") from exc
    if not isinstance(value, dict):
        raise FreezeError("freeze manifest must be an object")
    return value


def _paths(data: dict) -> list[str]:
    entries = data.get("files")
    if not isinstance(entries, list):
        raise FreezeError("files must be a list")
    paths = [item.get("path") for item in entries if isinstance(item, dict)]
    if len(paths) != len(entries) or any(not isinstance(path, str) for path in paths):
        raise FreezeError("every file entry requires a string path")
    return paths


def _path_list_digest(paths: list[str]) -> str:
    return hashlib.sha256(("\n".join(paths) + "\n").encode()).hexdigest()


def _safe_path(value: str) -> Path:
    if not value or "\\" in value or value.startswith("/"):
        raise FreezeError(f"unsafe governed path: {value!r}")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise FreezeError(f"unsafe governed path: {value!r}")
    path = (REPO_ROOT / value).resolve()
    try:
        path.relative_to(REPO_ROOT.resolve())
    except ValueError as exc:
        raise FreezeError(f"governed path escapes repository: {value!r}") from exc
    return path


_DEFAULT_PATHS = _paths(_load(DEFAULT_MANIFEST))
REQUIRED_GOVERNED_PATHS = frozenset(_DEFAULT_PATHS)


def verify(manifest_path: Path = DEFAULT_MANIFEST) -> dict[str, object]:
    data = _load(manifest_path)
    if data.get("schema_version") != "1.0":
        raise FreezeError("unexpected freeze-manifest schema")
    if data.get("program_id") != "TCD-CLEANROOM-001":
        raise FreezeError("unexpected program ID")
    if data.get("artifact_status") != "Research":
        raise FreezeError("artifact status must be Research")
    if data.get("execution_authorized") is not False:
        raise FreezeError("freeze manifest must keep execution unauthorized")

    entries = data["files"]
    paths = _paths(data)
    if paths != sorted(paths):
        raise FreezeError("freeze-manifest paths must be sorted")
    if len(set(paths)) != len(paths):
        raise FreezeError("duplicate governed path")
    if _path_list_digest(paths) != EXPECTED_PATH_LIST_SHA256:
        raise FreezeError("governed path set mismatch")

    for item in entries:
        value, expected = item["path"], item.get("sha256")
        if not isinstance(expected, str) or not HEX64.fullmatch(expected):
            raise FreezeError(f"invalid SHA-256 for {value}")
        path = _safe_path(value)
        if not path.is_file():
            raise FreezeError(f"governed file missing: {value}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise FreezeError(f"governed file digest mismatch: {value}: {actual} != {expected}")

    return {"status": "PASS", "files_checked": len(entries)}


def main() -> int:
    try:
        result = verify()
    except FreezeError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"PASS: {result['files_checked']} governed public artifacts match the freeze manifest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
