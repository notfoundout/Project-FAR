#!/usr/bin/env python3
"""Print compact root-cause diagnostics from the latest unified validation run."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / ".far" / "runs" / "latest.json"


def main() -> int:
    if not LATEST.is_file():
        print("No unified validation run record exists.")
        return 1
    payload = json.loads(LATEST.read_text(encoding="utf-8"))
    failures = [
        item
        for item in payload.get("results", [])
        if item.get("status") in {"validation_failure", "infrastructure_error", "timed_out"}
    ]
    if not failures:
        print("No root failures recorded.")
        return 0
    print("PROJECT FAR UNIFIED VALIDATION ROOT FAILURES")
    for item in failures:
        print()
        print(f"{item.get('failure_code') or 'FAR-VAL-UNKNOWN-001'} — {item.get('title')}")
        print(f"check: {item.get('check_id')}")
        print(f"summary: {item.get('summary')}")
        command = item.get("command") or []
        if command:
            print("reproduce: " + " ".join(command))
        changed = item.get("changed_files") or []
        if changed:
            print("changed files:")
            for path in changed[:30]:
                print(f"  {path}")
        stderr = (item.get("stderr") or "").splitlines()
        stdout = (item.get("stdout") or "").splitlines()
        if stderr:
            print("stderr tail:")
            for line in stderr[-40:]:
                print(f"  {line}")
        if stdout:
            print("stdout tail:")
            for line in stdout[-25:]:
                print(f"  {line}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
