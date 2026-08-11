#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CURRENT_FILES = {
    "agents": ROOT / "AGENTS.md",
    "readme": ROOT / "README.md",
    "status": ROOT / "docs/project-status.md",
    "map": ROOT / "docs/CANONICAL_MAP.md",
    "roadmap": ROOT / "docs/ROADMAP.md",
    "generated": ROOT / "docs/reports/project-status-generated.md",
    "next_actions": ROOT / "docs/planning/next-actions.md",
}
PROGRAM = ROOT / "docs/governance/post-terminal-public-evaluation-program-v1.0.md"


def newest_release_tag(root: Path = ROOT) -> str | None:
    versions: list[tuple[tuple[int, int, int], str]] = []
    for path in (root / "docs/releases").glob("project-far-v*.md"):
        match = re.fullmatch(r"project-far-v(\d+)\.(\d+)\.(\d+)\.md", path.name)
        if match:
            version = tuple(int(part) for part in match.groups())
            versions.append((version, "v" + ".".join(match.groups())))
    if not versions:
        return None
    return max(versions, key=lambda item: item[0])[1]


def program_identity(program_text: str) -> tuple[str | None, str | None]:
    program = re.search(r"^Program:\s*`([^`]+)`", program_text, re.M)
    next_workstream = re.search(r"^- `([^`]+)`:[^\n]*— next\.$", program_text, re.M)
    return (program.group(1) if program else None, next_workstream.group(1) if next_workstream else None)


def validate_texts(
    texts: dict[str, str],
    expected_release: str,
    program_id: str,
    next_workstream: str,
) -> list[str]:
    errors: list[str] = []

    def require(surface: str, needle: str, reason: str) -> None:
        if needle not in texts.get(surface, ""):
            errors.append(f"{surface}: {reason}: missing {needle!r}")

    require("readme", f"## Latest release: {expected_release}", "README release summary drifted")
    require("readme", "## Post-terminal phase", "README no longer identifies the post-terminal phase")
    require("readme", "`POST-TUE-UPP-001` is complete", "README terminal-program state drifted")

    require("status", f"Current published repository release: [`{expected_release}`]", "canonical status release drifted")
    require("status", f"Current program: `{program_id}`", "canonical status program drifted")
    require("status", f"`{next_workstream}` | Next", "canonical status next-workstream drifted")

    release_doc = f"releases/project-far-{expected_release}.md"
    require("map", f"Current Project FAR release: [`{release_doc}`]({release_doc})", "canonical map current-release navigation drifted")
    require("map", "Post-Terminal Public Evaluation Program", "canonical map lacks current evaluation authority")

    require("roadmap", f"Current published repository release: [`{expected_release}`]", "roadmap release drifted")
    require("roadmap", f"Current program: [`{program_id}`]", "roadmap program drifted")
    require("roadmap", f"`{next_workstream}` — next", "roadmap next-workstream drifted")

    require("generated", "# Historical Bounded-Program Status (Generated)", "generated bounded report can masquerade as current status")
    require("generated", "not a current project-status authority", "generated bounded report lacks an authority boundary")
    if "## Current Research Mode" in texts.get("generated", ""):
        errors.append("generated: historical report still declares a Current Research Mode")

    require("next_actions", f"Program: `{program_id}`.", "next-actions program drifted")
    require("next_actions", f"Canonical next workstream: `{next_workstream}`.", "next-actions workstream drifted")
    if "W5 remains blocked" in texts.get("next_actions", ""):
        errors.append("next_actions: obsolete W5-blocked planning survived into the current task queue")

    require("agents", "If purported current-authority surfaces conflict", "agent routing does not fail closed on authority conflicts")
    require("agents", "project memory", "agent routing does not subordinate memory to repository authority")
    require("agents", "repository presence as evidence that an artifact exists, not that its contents are Accepted", "agent routing conflates repository presence with epistemic authority")

    stale_current_phrases = {
        "status": [
            "v0.4.0 is the current release baseline",
            "Theory/dependency freeze before experiment preregistration",
        ],
        "roadmap": [
            "v0.4.0 is the current release baseline",
            "## Current Research Reset",
            "W5 remains blocked",
        ],
        "map": [
            "Current Project FAR release: [`releases/project-far-v0.4.0.md`]",
        ],
    }
    for surface, phrases in stale_current_phrases.items():
        text = texts.get(surface, "")
        for phrase in phrases:
            if phrase in text:
                errors.append(f"{surface}: stale current-state assertion survived: {phrase!r}")

    return errors


def validate_repository(root: Path = ROOT) -> list[str]:
    expected_release = newest_release_tag(root)
    if expected_release is None:
        return ["release: no docs/releases/project-far-vX.Y.Z.md authority found"]

    program_path = root / PROGRAM.relative_to(ROOT)
    if not program_path.exists():
        return [f"program: missing {program_path.relative_to(root)}"]
    program_id, next_workstream = program_identity(program_path.read_text(encoding="utf-8"))
    if program_id is None:
        return ["program: could not parse current program identity"]
    if next_workstream is None:
        return ["program: could not parse registered next workstream"]

    texts: dict[str, str] = {}
    for key, canonical_path in CURRENT_FILES.items():
        path = root / canonical_path.relative_to(ROOT)
        if not path.exists():
            texts[key] = ""
        else:
            texts[key] = path.read_text(encoding="utf-8", errors="replace")

    return validate_texts(texts, expected_release, program_id, next_workstream)


def main() -> int:
    errors = validate_repository()
    for error in errors:
        print("FAIL", error)
    if errors:
        raise SystemExit(1)
    print("Current-state consistency OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
