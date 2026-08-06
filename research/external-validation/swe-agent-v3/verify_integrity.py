"""Strict JSON and committed-byte integrity checks for FAR-SWE-V3-001."""
from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = HERE / "design-manifest-v1.0.json"
MANIFEST_RELATIVE = "research/external-validation/swe-agent-v3/design-manifest-v1.0.json"


class DesignError(RuntimeError):
    pass


def _bad_constant(token: str) -> Any:
    raise DesignError(f"non-finite JSON constant prohibited: {token}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DesignError(f"duplicate JSON key prohibited: {key}")
        out[key] = value
    return out


def _decode_json(data: bytes, label: str) -> Any:
    if data.startswith(b"\xef\xbb\xbf"):
        raise DesignError(f"UTF-8 BOM prohibited: {label}")
    try:
        return json.loads(
            data.decode("utf-8"),
            parse_constant=_bad_constant,
            object_pairs_hook=_unique_object,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DesignError(f"invalid strict JSON {label}: {exc}") from exc


def _read_regular(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise DesignError(f"regular file required: {path}")
    return path.read_bytes()


def _committed_blob_bytes(relative: str) -> bytes:
    try:
        return subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "blob", f"HEAD:{relative}"],
            check=True,
            capture_output=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise DesignError(f"cannot read committed Git blob: {relative}") from exc


def _load_json(path: Path) -> dict[str, Any]:
    value = _decode_json(_read_regular(path), str(path))
    if not isinstance(value, dict):
        raise DesignError(f"JSON object required: {path}")
    return value


def _canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _require_digest(value: Any, expected: str, label: str) -> None:
    if _canonical_digest(value) != expected:
        raise DesignError(f"exact contract mismatch: {label}")


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def _safe_path(relative: str) -> Path:
    p = PurePosixPath(relative)
    if (
        p.is_absolute()
        or not p.parts
        or any(x in {"", ".", ".."} for x in p.parts)
        or "\\" in relative
    ):
        raise DesignError(f"unsafe manifest path: {relative}")
    current = ROOT
    for part in p.parts:
        current /= part
        if current.is_symlink():
            raise DesignError(f"symlink prohibited: {relative}")
    try:
        current.resolve().relative_to(ROOT.resolve())
    except ValueError as exc:
        raise DesignError(f"manifest path escapes repository: {relative}") from exc
    return current


def _integer(value: Any, label: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise DesignError(f"{label} must be integer >= {minimum}")
    return value


def _number(value: Any, label: str) -> float:
    if type(value) not in (int, float) or not math.isfinite(value):
        raise DesignError(f"{label} must be finite JSON number")
    return float(value)


def _strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or any(type(x) is not str for x in value):
        raise DesignError(f"{label} must be string list")
    return value


REQUIRED_ARTIFACTS = {
    "research/external-validation/swe-agent-v3/.gitattributes",
    "research/external-validation/swe-agent-v3/README.md",
    "research/external-validation/swe-agent-v3/question-v1.0.md",
    "research/external-validation/swe-agent-v3/preregistration-v1.0.json",
    "research/external-validation/swe-agent-v3/task-manifest-contract-v1.0.json",
    "research/external-validation/swe-agent-v3/treatment-capsule-contract-v1.0.json",
    "research/external-validation/swe-agent-v3/execution-gate-v1.0.json",
    "research/external-validation/swe-agent-v3/evidence-and-analysis-plan-v1.0.md",
    "research/external-validation/swe-agent-v3/verify_integrity.py",
    "research/external-validation/swe-agent-v3/verify_design.py",
}


def verify_manifest() -> None:
    worktree = _read_regular(MANIFEST)
    if worktree != _committed_blob_bytes(MANIFEST_RELATIVE):
        raise DesignError("design manifest differs from committed HEAD blob")
    manifest = _decode_json(worktree, MANIFEST_RELATIVE)
    if not isinstance(manifest, dict) or manifest.get("schema_version") != "1.0":
        raise DesignError("manifest schema_version must be 1.0")
    entries = manifest.get("artifacts")
    if not isinstance(entries, list) or not entries:
        raise DesignError("manifest artifacts must be non-empty list")
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {
            "path",
            "git_blob_sha1",
            "bytes",
        }:
            raise DesignError(
                "manifest entries require exactly path, git_blob_sha1, bytes"
            )
        relative = entry["path"]
        blob = entry["git_blob_sha1"]
        size = entry["bytes"]
        if type(relative) is not str or relative in seen:
            raise DesignError(f"invalid or duplicate manifest path: {relative}")
        if type(blob) is not str or re.fullmatch(r"[0-9a-f]{40}", blob) is None:
            raise DesignError(f"invalid Git blob id: {relative}")
        _integer(size, f"manifest bytes for {relative}")
        seen.add(relative)
        committed = _committed_blob_bytes(relative)
        if len(committed) != size or _git_blob_sha1(committed) != blob:
            raise DesignError(f"committed blob identity mismatch: {relative}")
        if _read_regular(_safe_path(relative)) != committed:
            raise DesignError(f"worktree differs from committed blob: {relative}")
    if seen != REQUIRED_ARTIFACTS:
        raise DesignError(
            f"manifest artifact set mismatch: {sorted(seen ^ REQUIRED_ARTIFACTS)}"
        )


def verify_byte_policy() -> None:
    expected = (
        b"# Preserve exact governed bytes regardless of core.autocrlf or platform defaults.\n"
        b"* -text\n"
    )
    if _read_regular(HERE / ".gitattributes") != expected:
        raise DesignError("package byte-preservation policy mismatch")
