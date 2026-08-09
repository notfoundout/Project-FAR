"""Shallow-checkout-safe semantic verifier for FAR-SWE-V3-001 amendment v1.1.

This adapter preserves the complete v1.1 semantic validator while replacing its
historical Git-object lookups with immutable historical snapshot bytes rooted in
the caller's active verification tree. It does not authorize execution.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import verify_amendment_v1_1 as legacy

HERE = Path(__file__).resolve().parent
HIST = HERE / "historical-base-83c951"
SNAPSHOTS = {
    legacy.PREREG_REL: ("preregistration-v1.0.json", legacy.PREREG_BLOB),
    legacy.PLAN_REL: ("evidence-and-analysis-plan-v1.0.md", legacy.PLAN_BLOB),
}

AmendmentError = legacy.AmendmentError
probability = legacy.probability
type7 = legacy.type7
classify = legacy.classify


def _regular_bytes(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise AmendmentError(f"regular rooted historical snapshot required: {path}")
    return path.read_bytes()


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _snapshot(relative: str, historical_root: Path | None = None) -> tuple[bytes, str]:
    try:
        filename, expected = SNAPSHOTS[relative]
    except KeyError as exc:
        raise AmendmentError(f"unregistered historical snapshot: {relative}") from exc
    root = historical_root or HIST
    path = root / filename
    data = _regular_bytes(path)
    actual = _git_blob_sha1(data)
    if actual != expected:
        raise AmendmentError(f"rooted historical snapshot identity drifted: {relative}")
    return data, actual


def validate(
    amend: Path = legacy.AMEND,
    readme: Path = legacy.README,
    gate: Path = legacy.GATE,
    historical_root: Path | None = None,
) -> dict[str, Any]:
    """Run the full legacy semantic validator against caller-bound snapshot bytes."""
    original_id = legacy.historical_blob_id
    original_bytes = legacy.historical_blob_bytes

    def rooted_id(head: str, relative: str) -> str:
        if head != legacy.BASE_HEAD:
            raise AmendmentError("historical authority head drifted")
        return _snapshot(relative, historical_root)[1]

    def rooted_bytes(head: str, relative: str) -> bytes:
        if head != legacy.BASE_HEAD:
            raise AmendmentError("historical authority head drifted")
        return _snapshot(relative, historical_root)[0]

    legacy.historical_blob_id = rooted_id
    legacy.historical_blob_bytes = rooted_bytes
    try:
        return legacy.validate(amend=amend, readme=readme, gate=gate)
    finally:
        legacy.historical_blob_id = original_id
        legacy.historical_blob_bytes = original_bytes


if __name__ == "__main__":
    try:
        validate()
    except AmendmentError as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: amendment v1.1 semantics validated from rooted historical snapshots; execution blocked.")
