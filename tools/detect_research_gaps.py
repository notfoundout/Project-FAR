#!/usr/bin/env python3
"""Detect advisory research gaps without changing Project FAR theory."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

import yaml

from report_link_utils import existing_file, markdown_line_link, markdown_link

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/reports/research-gap-report.md"
REG = [
    ROOT / "theory/evaluation/evidence-registry.yaml",
    ROOT / "theory/evaluation/external-validation-registry.yaml",
    ROOT / "theory/falsification/adversarial-test-suite.yaml",
    ROOT / "theory/falsification/primitive-pressure-registry.yaml",
]
REPORT_DIRS = [ROOT / "docs", ROOT / "theory"]


def load(p):
    with p.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def ent(d):
    return d.get("entries") or d.get("tests") or []


def add(gaps, typ, loc, sev, action, line=None):
    gaps.append({"type": typ, "location": loc, "severity": sev, "action": action, "line": line})


def linked_location(g):
    loc = str(g["location"])
    if existing_file(loc):
        line = g.get("line")
        if g.get("type") == "TODO/future-work note" and line is not None:
            # Line numbers in this generated advisory report are observation
            # metadata, not stable document identities. Show the observed line
            # in the label, but link to the file so ordinary edits cannot turn a
            # valid advisory pointer into a broken repository link.
            return markdown_link(loc, OUT, f"{loc}:L{line}")
        return markdown_line_link(loc, OUT, line)
    return f"`{loc}`"


def norm(s):
    return str(s or "").lower()


def nav_links(out_path: Path) -> list[str]:
    return [
        f"- README Command Center: {markdown_link(ROOT / 'README.md', out_path)}",
        f"- Current Project Status: {markdown_link(ROOT / 'docs/project-status.md', out_path)}",
        f"- Historical Bounded Status: {markdown_link(ROOT / 'docs/reports/project-status-generated.md', out_path)}",
        f"- Research Gaps: {markdown_link(ROOT / 'docs/reports/research-gap-report.md', out_path)}",
        f"- Next Actions: {markdown_link(ROOT / 'docs/planning/next-actions.md', out_path)}",
    ]


def newest_release_tag() -> str | None:
    release_docs = []
    for path in (ROOT / "docs/releases").glob("project-far-v*.md"):
        match = re.fullmatch(r"project-far-v(\d+)\.(\d+)\.(\d+)\.md", path.name)
        if match:
            release_docs.append((tuple(int(x) for x in match.groups()), path))
    if not release_docs:
        return None
    version, _ = max(release_docs, key=lambda item: item[0])
    return "v" + ".".join(str(x) for x in version)


def detect_stale_current_release(gaps: list[dict[str, object]]) -> None:
    current = newest_release_tag()
    if current is None:
        add(gaps, "missing release authority", "docs/releases", "high", "Restore a versioned Project FAR release authority document before using current-release language.")
        return

    version_pattern = re.compile(r"\bv\d+\.\d+\.\d+\b", re.I)
    current_pattern = re.compile(r"\b(latest|current)\b.*\brelease\b|\brelease\b.*\b(latest|current)\b", re.I)
    surfaces = [
        ROOT / "README.md",
        ROOT / "docs/project-status.md",
        ROOT / "docs/ROADMAP.md",
        ROOT / "docs/CANONICAL_MAP.md",
    ]
    for path in surfaces:
        if not path.exists():
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not current_pattern.search(line):
                continue
            versions = version_pattern.findall(line)
            stale = [version for version in versions if version.lower() != current.lower()]
            if stale:
                add(
                    gaps,
                    "stale current-release reference",
                    str(path.relative_to(ROOT)),
                    "high",
                    f"Current release authority is {current}; remove or reclassify stale current-release wording {', '.join(stale)}.",
                    lineno,
                )
                break


def detect_gaps() -> list[dict[str, object]]:
    data = {str(p): load(p) for p in REG}
    gaps = []
    evidence = ent(data[str(REG[0])])
    external = ent(data[str(REG[1])])
    adv = ent(data[str(REG[2])])
    pressure = data[str(REG[3])].get("primitives", [])

    for e in evidence + external:
        ident = e.get("id", "unknown")
        if "unresolved" in norm(e.get("registry_resolution")) or "unresolved" in norm(e.get("analysis_status")):
            add(gaps, "unresolved case", ident, "medium", "Review the case and decide whether it remains unresolved, is outside scope, or needs a conservative-extension report.")
        if "provisional" in norm(e.get("confidence")) or "provisional" in norm(e.get("review_status")):
            add(gaps, "provisional system", ident, "medium", "Perform human review and update confidence only if evidence warrants it.")
        if "candidate primitive" in norm(e.get("classification")):
            add(gaps, "candidate primitive failure", ident, "critical", "Human review required before any primitive-level conclusion or theory change.")
        report = e.get("report")
        if report and not (ROOT / report).exists():
            add(gaps, "missing analysis report", report, "high", "Create or correct the referenced analysis report after human approval.")

    for a in adv:
        ident = a.get("id", "unknown")
        if "unresolved" in norm(a.get("current_status")):
            add(gaps, "unresolved case", ident, "medium", "Review adversarial test status and document next validation step.")
        if "candidate primitive" in norm(a.get("current_status")):
            add(gaps, "candidate primitive failure", ident, "critical", "Escalate to human theory review; do not modify primitives automatically.")

    for p in pressure:
        prim = p.get("primitive", "unknown")
        if p.get("candidate_primitive_failures"):
            add(gaps, "candidate primitive failure", prim, "critical", "Human theory review required for recorded candidate primitive failures.")
        if p.get("unresolved_pressures"):
            add(gaps, "unresolved primitive pressure", prim, "high", "Analyze unresolved pressure before promoting stronger sufficiency claims.")
        if int(p.get("number_of_tests_stressing_it") or 0) < 2:
            add(gaps, "low primitive coverage", prim, "medium", "Add human-approved adversarial coverage for this primitive.")

    domains = Counter(e.get("domain", "unspecified") for e in external)
    for domain, count in domains.items():
        if count < 2:
            add(gaps, "underrepresented external-validation domain", domain, "medium", "Consider adding at least one additional external validation system for this domain.")

    for status, count in Counter(e.get("classification", "") for e in evidence + external).items():
        if "conservative extension" in norm(status) and count >= 3:
            add(gaps, "conservative-extension cluster", status, "medium", "Review cluster for recurring policy needs without assuming primitive failure.")

    reports = set(str(p.relative_to(ROOT)) for p in sorted((ROOT / "theory/evaluation/external-systems").glob("*.md")))
    registered = set(e.get("report") for e in external if e.get("report"))
    for report in sorted(reports - registered):
        add(gaps, "missing registry entry for report", report, "medium", "Decide whether this report should be entered in the external validation registry.")

    detect_stale_current_release(gaps)

    pattern = re.compile(r"\b(TODO|TBD|unresolved|future work)\b", re.I)
    for base in REPORT_DIRS:
        for p in sorted(base.rglob("*.md")):
            rel = str(p.relative_to(ROOT))
            if rel in {
                "docs/reports/project-status-generated.md",
                "docs/reports/research-gap-report.md",
                "docs/planning/next-actions.md",
                "docs/planning/dashboard-metrics.md",
                "docs/planning/repository-index.md",
            }:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            match_line = next((i for i, line in enumerate(text.splitlines(), 1) if pattern.search(line)), None)
            if match_line:
                add(gaps, "TODO/future-work note", rel, "low", "Review note and decide whether it blocks validation.", match_line)

    return gaps


def main():
    gaps = detect_gaps()
    lines = [
        "# Research Gap Report",
        "",
        "## Navigation",
        "",
        *nav_links(OUT),
        "",
        "Generated by `python tools/detect_research_gaps.py`. Findings are advisory and require human review.",
        "",
        "TODO/future-work line numbers in location labels are observation metadata. Their links intentionally target the file rather than the volatile line number.",
        "",
        "| Gap ID | Type | Location | Severity | Recommended Action |",
        "|---|---|---|---|---|",
    ]
    for i, gap in enumerate(gaps, 1):
        lines.append(f"| <a id=\"gap-{i:03d}\"></a>GAP-{i:03d} | {gap['type']} | {linked_location(gap)} | {gap['severity']} | {gap['action']} |")
    lines += ["", "## Navigation", "", *nav_links(OUT)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)} gaps={len(gaps)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
