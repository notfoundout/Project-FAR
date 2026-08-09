"""Compatibility entrypoint for the single FAR-SWE-V3-001 narrative authority.

All complete public-narrative semantics live in verify_public_narratives.py.
This entrypoint intentionally performs no transformation or second copy of any
narrative oracle, preventing compatibility-layer drift.
"""
from __future__ import annotations

import verify_public_narratives as base

NarrativeError = base.NarrativeError
HERE = base.HERE
EXPECTED = base.EXPECTED


def verify(here=HERE) -> None:
    base.verify(here)


if __name__ == "__main__":
    try:
        verify()
    except NarrativeError as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: current FAR-SWE-V3-001 public narratives use the single canonical oracle.")
