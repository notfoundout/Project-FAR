from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_latest(root: Path) -> dict[str, Any]:
    path = root / ".far" / "runs" / "latest.json"
    if not path.is_file():
        raise FileNotFoundError("no validation run found; run `far validate` first")
    return json.loads(path.read_text(encoding="utf-8"))


def format_diagnosis(payload: dict[str, Any], failure_code: str | None = None) -> str:
    results = payload.get("results", [])
    failures = [
        result
        for result in results
        if result.get("status") in {"validation_failure", "infrastructure_error", "timed_out"}
    ]
    if failure_code:
        failures = [item for item in failures if item.get("failure_code") == failure_code]
    if not failures:
        return "No matching root failures were recorded."
    lines = [
        f"Validation run: {payload.get('run_id', 'unknown')}",
        f"Commit: {payload.get('commit_sha', 'unknown')}",
        f"Profile: {payload.get('profile', 'unknown')}",
        "",
    ]
    for index, item in enumerate(failures, start=1):
        lines.extend(
            [
                f"{index}. {item.get('failure_code') or 'FAR-VAL-UNKNOWN-001'} — {item.get('title')}",
                f"   Check: {item.get('check_id')}",
                f"   Status: {item.get('status')}",
                f"   Root cause: {item.get('summary') or 'not provided'}",
            ]
        )
        command = item.get("command") or []
        if command:
            lines.append(f"   Reproduce: {' '.join(command)}")
        changed = item.get("changed_files") or []
        if changed:
            lines.append(f"   Generated drift: {', '.join(changed[:20])}")
        stderr = (item.get("stderr") or "").strip().splitlines()
        if stderr:
            lines.append("   Failure tail:")
            lines.extend(f"     {line}" for line in stderr[-12:])
        lines.append("")
    return "\n".join(lines).rstrip()
