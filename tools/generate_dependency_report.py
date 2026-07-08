#!/usr/bin/env python3
"""Generate a Markdown report from the Project FAR dependency registry."""
from __future__ import annotations

from collections import Counter, defaultdict

from dependency_utils import ROOT, REGISTRY, SCHEMA, dependencies
from report_link_utils import markdown_link

OUT = ROOT / "docs/reports/dependency-report.md"


def link_node(value: str) -> str:
    path = ROOT / value
    if path.exists():
        return markdown_link(path, OUT)
    return f"`{value}`"


def table(counter: Counter) -> list[str]:
    lines = ["| Value | Count |", "|---|---:|"]
    for key, value in sorted(counter.items()):
        lines.append(f"| `{key}` | {value} |")
    if not counter:
        lines.append("| None | 0 |")
    return lines


def dependency_rows(records: list[dict]) -> list[str]:
    lines = ["| ID | Source | Relationship | Target | Evidence |", "|---|---|---|---|---|"]
    for dep in records:
        lines.append(
            f"| `{dep['id']}` | {link_node(dep['source'])} | `{dep['relationship']}` | "
            f"{link_node(dep['target'])} | {dep['evidence']} |"
        )
    if not records:
        lines.append("| None |  |  |  |  |")
    return lines


def main() -> int:
    deps = dependencies()
    source_counts = Counter(dep.get("source_type", "unknown") for dep in deps)
    target_counts = Counter(dep.get("target_type", "unknown") for dep in deps)
    relationship_counts = Counter(dep.get("relationship", "unknown") for dep in deps)
    incoming: Counter = Counter(dep.get("target") for dep in deps)
    outgoing: Counter = Counter(dep.get("source") for dep in deps)
    nodes = set(incoming) | set(outgoing)
    orphan_like = sorted(node for node in nodes if incoming[node] == 0 or outgoing[node] == 0)
    by_confidence = defaultdict(list)
    by_status = defaultdict(list)
    for dep in deps:
        by_confidence[dep.get("confidence")].append(dep)
        by_status[dep.get("status")].append(dep)

    lines = [
        "# Dependency Report",
        "",
        f"Generated from {markdown_link(REGISTRY, OUT)} using {markdown_link('tools/generate_dependency_report.py', OUT)}.",
        "",
        "This report is repository-infrastructure evidence only. It does not infer controversial semantic dependencies or alter accepted theory content.",
        "",
        "## Registry Inputs",
        "",
        f"- Schema: {markdown_link(SCHEMA, OUT)}",
        f"- Registry: {markdown_link(REGISTRY, OUT)}",
        "",
        "## Summary",
        "",
        f"- Dependency records: {len(deps)}",
        f"- Registry nodes: {len(nodes)}",
        f"- Registry edges: {len(deps)}",
        "",
        "## Counts by Source Type",
        "",
        *table(source_counts),
        "",
        "## Counts by Target Type",
        "",
        *table(target_counts),
        "",
        "## Counts by Relationship",
        "",
        *table(relationship_counts),
        "",
        "## High-Confidence Dependencies",
        "",
        *dependency_rows(by_confidence.get("high", [])),
        "",
        "## Provisional Dependencies",
        "",
        *dependency_rows(by_status.get("provisional", [])),
        "",
        "## Needs-Review Dependencies",
        "",
        *dependency_rows(by_status.get("needs_review", [])),
        "",
        "## Orphan-Like Nodes Detected from Registry Only",
        "",
        "Orphan-like means a registered node currently has only incoming or only outgoing registry edges. This is not a repository-wide orphaned-file finding.",
        "",
    ]
    lines += [f"- {link_node(node)}" for node in orphan_like] or ["- None detected."]
    lines += [
        "",
        "## Top Referenced Targets",
        "",
        "| Target | Incoming Records |",
        "|---|---:|",
    ]
    for target, count in incoming.most_common(10):
        lines.append(f"| {link_node(target)} | {count} |")
    if not incoming:
        lines.append("| None | 0 |")
    lines += [
        "",
        "## Known Limitations",
        "",
        "- The registry is intentionally seeded from explicit repository structure only.",
        "- Absence of a dependency record does not imply absence of a real dependency.",
        "- Relationship labels are infrastructure classifications, not final semantic conclusions.",
        "- Generated graph outputs are derived from registry records and inherit registry incompleteness.",
        "- Future v0.4 tooling must distinguish accepted evidence from provisional or needs-review records.",
        "",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)} generated")
    print(f"records: {len(deps)}")
    print(f"nodes: {len(nodes)}")
    print(f"edges: {len(deps)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
