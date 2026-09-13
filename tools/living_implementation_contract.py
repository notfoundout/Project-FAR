#!/usr/bin/env python3
"""Pure validation contract for separately authorized living-research implementation proposals."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

CHANGE_DISPOSITION = "PROJECT_CHANGE_REQUIRED"
CANDIDATE_PREFIX = "research/living/inbox/candidates"
PROPOSAL_PREFIX = "research/living/inbox/implementation-proposals"
PAYLOAD_PREFIX = "research/living/inbox/implementation-payloads"


class ImplementationContractError(RuntimeError):
    pass


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json_sha(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    return sha256(raw.encode("utf-8"))


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ImplementationContractError(f"expected object: {path}")
    return value


def safe_path(raw: str) -> str:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise ImplementationContractError("unsafe repository path")
    path = PurePosixPath(raw)
    if path.is_absolute() or "." in path.parts or ".." in path.parts:
        raise ImplementationContractError(f"unsafe repository path: {raw}")
    return path.as_posix()


def under(path: str, root: str) -> bool:
    parts = PurePosixPath(path).parts
    root_parts = PurePosixPath(root).parts
    return parts[: len(root_parts)] == root_parts


def validate_target(path: str, policy: dict[str, Any]) -> str:
    path = safe_path(path)
    if path in set(policy["write_exact_paths"]):
        return path
    if not any(under(path, root) for root in policy["write_roots"]):
        raise ImplementationContractError(f"target outside implementation surface: {path}")
    return path
