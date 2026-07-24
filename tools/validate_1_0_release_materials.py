from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "releases" / "1.0-interface-registry.json"
READINESS = ROOT / "docs" / "releases" / "1.0-readiness.json"
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

    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    if readiness.get("previous_public_version") != "0.4.0":
        raise SystemExit("release baseline must be 0.4.0")
    if "0.4.0" not in readiness.get("baseline_correction", ""):
        raise SystemExit("readiness metadata must preserve the baseline correction")

    notes = NOTES.read_text(encoding="utf-8")
    missing_headings = sorted(REQUIRED_NOTE_HEADINGS - set(notes.splitlines()))
    if missing_headings:
        raise SystemExit(f"release notes missing headings: {missing_headings}")
    if "Status: unreleased" not in notes:
        raise SystemExit("draft release notes must remain explicitly unreleased")
    if "from 0.4.0" not in notes:
        raise SystemExit("release notes must cover 0.4.0 to 1.0.0")
    if "the public baseline for these cumulative notes is `0.4.0`, not `0.3.1`" not in notes:
        raise SystemExit("release notes must record the corrected baseline")
    if "unrestricted universality" not in notes:
        raise SystemExit("release notes must preserve the universality nonclaim")

    print("Project FAR 1.0 release materials validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
