from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "releases" / "1.0-interface-registry.json"
NOTES = ROOT / "docs" / "releases" / "1.0.0-draft.md"

REQUIRED_COMMANDS = {
    "far-decision",
    "far-reasoning-regression",
    "far-external-trace",
}

REQUIRED_NOTE_HEADINGS = {
    "## Research and theory",
    "## Repository and governance",
    "## Verification and mechanization",
    "## Decision integrity",
    "## External traces",
    "## External validation",
    "## Corrections and superseded approaches",
    "## What 1.0.0 will claim",
    "## What 1.0.0 will not claim",
    "## Remaining release gates",
}


def collect_strings(value: object) -> set[str]:
    found: set[str] = set()
    if isinstance(value, str):
        found.add(value)
    elif isinstance(value, dict):
        for key, item in value.items():
            found.add(str(key))
            found.update(collect_strings(item))
    elif isinstance(value, list):
        for item in value:
            found.update(collect_strings(item))
    return found


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry_strings = collect_strings(registry)
    missing_commands = sorted(REQUIRED_COMMANDS - registry_strings)
    if missing_commands:
        raise SystemExit(f"interface registry missing commands: {missing_commands}")

    notes = NOTES.read_text(encoding="utf-8")
    missing_headings = sorted(REQUIRED_NOTE_HEADINGS - set(notes.splitlines()))
    if missing_headings:
        raise SystemExit(f"release notes missing headings: {missing_headings}")
    if "Status: unreleased" not in notes:
        raise SystemExit("draft release notes must remain explicitly unreleased")
    if "unrestricted universality" not in notes:
        raise SystemExit("release notes must preserve the universality nonclaim")

    print("Project FAR 1.0 release materials validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
