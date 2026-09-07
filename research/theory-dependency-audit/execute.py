#!/usr/bin/env python3
"""Execute FAR-THEORY-DEPENDENCY-AUDIT-001 with an authenticated archive fallback.

The original executor is preserved byte-for-byte as ``execute_core_v1.py``. This wrapper
prefers the original historical-Git lookup and falls back only when that lookup is unavailable.
Fallback bytes are vendored from the exact historical Git blobs and are revalidated against
the preregistered ``source_locks`` before use.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_CORE_PATH = Path(__file__).with_name("execute_core_v1.py")
_CORE_SPEC = importlib.util.spec_from_file_location(
    "far_theory_dependency_audit_core_v1", _CORE_PATH
)
if _CORE_SPEC is None or _CORE_SPEC.loader is None:
    raise RuntimeError(f"unable to load preserved audit core: {_CORE_PATH}")
_core = importlib.util.module_from_spec(_CORE_SPEC)
_CORE_SPEC.loader.exec_module(_core)

_FROZEN_ROOT = Path("research/theory-dependency-audit/frozen-source-v1.0")
_original_read_base_blob = _core.read_base_blob


def read_base_blob(root: Path, base_commit: str, relative: str) -> bytes:
    """Read the historical blob, falling back to its vendored exact bytes.

    Git history remains preferred. The fallback is accepted only for a path recorded in the
    frozen execution specification and only when its recomputed Git blob SHA equals the
    preregistered source-lock SHA.
    """
    try:
        return _original_read_base_blob(root, base_commit, relative)
    except (ValueError, FileNotFoundError) as git_error:
        spec_path = root / _core.SPEC_PATH.relative_to(_core.ROOT)
        if not spec_path.is_file():
            raise ValueError(
                f"frozen base unavailable and execution specification missing: {relative}"
            ) from git_error
        spec = _core.load_json(spec_path)
        if spec.get("base_commit") != base_commit:
            raise ValueError(
                f"vendored fallback base-commit mismatch: expected {spec.get('base_commit')}, "
                f"requested {base_commit}"
            ) from git_error
        expected_sha = spec.get("source_locks", {}).get(relative)
        if expected_sha is None:
            raise ValueError(
                f"vendored fallback path is not source-locked: {relative}"
            ) from git_error

        frozen_path = root / _FROZEN_ROOT / relative
        if not frozen_path.is_file():
            raise ValueError(
                f"vendored frozen source missing: {relative}"
            ) from git_error
        data = frozen_path.read_bytes()
        actual_sha = _core.git_blob_sha(data)
        if actual_sha != expected_sha:
            raise ValueError(
                "vendored frozen source identity mismatch: "
                f"{relative}: expected {expected_sha}, got {actual_sha}"
            ) from git_error
        return data


# The preserved core resolves ``read_base_blob`` dynamically from its module globals, so this
# one assignment upgrades all existing execution paths without changing the historical logic.
_core.read_base_blob = read_base_blob

# Preserve the historical public module surface for existing tests and callers.
for _name in dir(_core):
    if not _name.startswith("__") and _name != "read_base_blob":
        globals()[_name] = getattr(_core, _name)
globals()["read_base_blob"] = read_base_blob


if __name__ == "__main__":
    sys.exit(main())
