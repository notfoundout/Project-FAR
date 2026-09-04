#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURRENT_CORE = "PROJECT-FAR-CORE-THEORY-1.1"
HISTORICAL_CORE = "PROJECT-FAR-CORE-THEORY-1.0"

CURRENT_FILES = {
    "agents": ROOT / "AGENTS.md",
    "readme": ROOT / "README.md",
    "status": ROOT / "docs/project-status.md",
    "map": ROOT / "docs/CANONICAL_MAP.md",
    "roadmap": ROOT / "docs/ROADMAP.md",
    "generated": ROOT / "docs/reports/project-status-generated.md",
    "next_actions": ROOT / "docs/planning/next-actions.md",
}
PROGRAM = ROOT / "docs/governance/post-closure-assurance-and-application-program-v1.0.md"


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
    """Return program id and registered next workstream, if one exists.

    A completed POST-CLOSURE-001 program legitimately has no next workstream. The
    absence is distinguished from parse failure by validate_repository(), which
    independently requires the explicit terminal status and no-W7 declaration.
    """
    program = re.search(r"^Program:\s*`([^`]+)`", program_text, re.M)
    next_workstream = re.search(
        r"^- `([^`]+)`:[^\n]*\bnext\b[^\n]*$",
        program_text,
        re.M | re.I,
    )
    return (
        program.group(1) if program else None,
        next_workstream.group(1) if next_workstream else None,
    )


def validate_texts(
    texts: dict[str, str],
    expected_release: str,
    program_id: str,
    next_workstream: str | None,
) -> list[str]:
    errors: list[str] = []

    def require(surface: str, needle: str, reason: str) -> None:
        if needle not in texts.get(surface, ""):
            errors.append(f"{surface}: {reason}: missing {needle!r}")

    require("readme", f"## Latest release: {expected_release}", "README release summary drifted")
    require("readme", "## Post-closure phase", "README no longer identifies the post-closure phase")
    require("readme", f"`{CURRENT_CORE}`", "README current core-theory identity drifted")
    require("readme", "Historical v1.0", "README no longer preserves historical v1.0 boundary")

    require("status", f"Current published repository release: [`{expected_release}`]", "canonical status release drifted")
    require("status", f"Current governing theory: `{CURRENT_CORE}`", "canonical status governing core drifted")
    require("status", f"Current program: `{program_id}`", "canonical status program drifted")

    release_doc = f"releases/project-far-{expected_release}.md"
    require("map", f"Current Project FAR release: [`{release_doc}`]({release_doc})", "canonical map current-release navigation drifted")
    require("map", "Project FAR Core Theory v1.1", "canonical map current core authority drifted")
    require("map", "Historical Project FAR Core Theory v1.0", "canonical map historical core boundary drifted")
    require("map", "Post-Closure Assurance and Application Program", "canonical map lacks current assurance authority")

    require("roadmap", f"Current published repository release: [`{expected_release}`]", "roadmap release drifted")
    require("roadmap", f"Current governing core: [`{CURRENT_CORE}`]", "roadmap governing core drifted")
    require("roadmap", f"Current program: [`{program_id}`]", "roadmap program drifted")

    require("generated", "# Historical Bounded-Program Status (Generated)", "generated bounded report can masquerade as current status")
    require("generated", "not a current project-status authority", "generated bounded report lacks an authority boundary")
    if "## Current Research Mode" in texts.get("generated", ""):
        errors.append("generated: historical report still declares a Current Research Mode")

    require("next_actions", f"Program: `{program_id}`", "next-actions program drifted")
    require("next_actions", f"Current governing theory: `{CURRENT_CORE}`.", "next-actions theory target drifted")
    require("next_actions", "Historical v1.0 Core", "next-actions historical core boundary drifted")
    if "PTE-W1-INDEPENDENT-REVIEW" in texts.get("next_actions", ""):
        errors.append("next_actions: superseded UPP evaluation planning survived into the current task queue")

    if next_workstream is None:
        require("readme", "`POST-CLOSURE-001` is complete at all six registered workstream scopes.", "README terminal program state drifted")
        require("readme", "No W7 is registered by `POST-CLOSURE-001`.", "README invented or lost terminal no-W7 boundary")
        require("status", "**complete at its six registered workstream scopes**", "canonical status terminal program state drifted")
        require("status", "No `POST-CLOSURE-001` W7 is registered.", "canonical status lost no-W7 boundary")
        require("roadmap", "complete at its six registered workstream scopes", "roadmap terminal program state drifted")
        require("roadmap", "No W7 is currently registered.", "roadmap lost no-W7 boundary")
        require("next_actions", "There is **no registered next `POST-CLOSURE-001` workstream**.", "next-actions invented a terminal successor")
        require("next_actions", "OPEN-EXTERNAL-OP-28", "next-actions lost external/human effectiveness obligation")
        for surface in ("readme", "status", "roadmap"):
            require(surface, "PCA-W6-EMPIRICAL-AUDIT-UTILITY", "terminal W6 disposition missing")
        if "**Next / Active**" in texts.get("status", ""):
            errors.append("status: terminal program still marks a workstream Next / Active")
        if re.search(r"`PCA-W\d[^`]*`\s*[—:-]+\s*next\b", texts.get("roadmap", ""), re.I):
            errors.append("roadmap: terminal program still declares a PCA workstream next")
        if "Canonical next workstream:" in texts.get("next_actions", ""):
            errors.append("next_actions: terminal program still declares a canonical next workstream")
    else:
        status_workstream = re.search(
            rf"\|\s*`{re.escape(next_workstream)}`\s*\|\s*\*\*Next / Active\*\*\s*\|",
            texts.get("status", ""),
        )
        if not status_workstream:
            errors.append("status: canonical status next-workstream drifted")
        require("roadmap", f"`{next_workstream}` — next", "roadmap next-workstream drifted")
        require("next_actions", f"Canonical next workstream: `{next_workstream}`.", "next-actions workstream drifted")

    require("agents", "If purported current-authority surfaces conflict", "agent routing does not fail closed on authority conflicts")
    require("agents", "project memory", "agent routing does not subordinate memory to repository authority")
    require("agents", "repository presence as evidence that an artifact exists, not that its contents are Accepted", "agent routing conflates repository presence with epistemic authority")

    stale_current_phrases = {
        "status": [
            "v0.4.0 is the current release baseline",
            "Theory/dependency freeze before experiment preregistration",
            f"Current governing theory: `{HISTORICAL_CORE}`",
        ],
        "roadmap": [
            "v0.4.0 is the current release baseline",
            "## Current Research Reset",
            "W5 remains blocked",
        ],
        "map": ["Current Project FAR release: [`releases/project-far-v0.4.0.md`]"],
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
    program_text = program_path.read_text(encoding="utf-8")
    program_id, next_workstream = program_identity(program_text)
    if program_id is None:
        return ["program: could not parse current program identity"]

    terminal = "Status: **Complete at the six registered workstream scopes" in program_text
    no_w7 = "No W7 is registered by this program." in program_text
    if next_workstream is None and not (terminal and no_w7):
        return ["program: no next workstream found without explicit terminal/no-W7 authority"]
    if next_workstream is not None and terminal:
        return ["program: terminal program also declares a next workstream"]

    texts: dict[str, str] = {}
    for key, canonical_path in CURRENT_FILES.items():
        path = root / canonical_path.relative_to(ROOT)
        texts[key] = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""

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
