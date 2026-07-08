#!/usr/bin/env python3
"""Analyze downstream impact using only the Project FAR dependency registry."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/dependencies/dependency-registry.yaml"
OUT = ROOT / "docs/reports/theory-impact-report.md"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_registry() -> dict[str, Any]:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    return data if isinstance(data, dict) else {}


def records() -> list[dict[str, Any]]:
    deps = load_registry().get("dependencies") or []
    return [dep for dep in deps if isinstance(dep, dict)] if isinstance(deps, list) else []


def nodes_from(deps: list[dict[str, Any]]) -> list[str]:
    nodes = {str(dep.get(key)) for dep in deps for key in ("source", "target") if dep.get(key)}
    return sorted(nodes)


def build_graphs(deps: list[dict[str, Any]]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    outgoing: dict[str, list[dict[str, Any]]] = defaultdict(list)
    incoming: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for dep in sorted(deps, key=lambda d: str(d.get("id", ""))):
        source = str(dep.get("source", ""))
        target = str(dep.get("target", ""))
        if source and target:
            outgoing[source].append(dep)
            incoming[target].append(dep)
    return outgoing, incoming


def impact_for(node: str, deps: list[dict[str, Any]]) -> dict[str, Any]:
    _outgoing, incoming = build_graphs(deps)
    direct = sorted({str(dep["source"]) for dep in incoming.get(node, []) if dep.get("source")})
    depths: dict[str, int] = {}
    rels: Counter[str] = Counter()
    confidences: Counter[str] = Counter()
    statuses: Counter[str] = Counter()
    q: deque[tuple[str, int]] = deque()
    for dep in sorted(incoming.get(node, []), key=lambda d: str(d.get("id", ""))):
        src = str(dep.get("source", ""))
        if not src:
            continue
        if src not in depths or 1 < depths[src]:
            depths[src] = 1
            q.append((src, 1))
        rels[str(dep.get("relationship", "unknown"))] += 1
        confidences[str(dep.get("confidence", "unknown"))] += 1
        statuses[str(dep.get("status", "unknown"))] += 1
    while q:
        current, depth = q.popleft()
        for dep in sorted(incoming.get(current, []), key=lambda d: str(d.get("id", ""))):
            src = str(dep.get("source", ""))
            if not src:
                continue
            rels[str(dep.get("relationship", "unknown"))] += 1
            confidences[str(dep.get("confidence", "unknown"))] += 1
            statuses[str(dep.get("status", "unknown"))] += 1
            nd = depth + 1
            if src not in depths or nd < depths[src]:
                depths[src] = nd
                q.append((src, nd))
    indirect = sorted(node for node, depth in depths.items() if depth > 1)
    return {
        "node": node,
        "directly_affected_nodes": direct,
        "indirectly_affected_nodes": indirect,
        "dependency_depth": max(depths.values(), default=0),
        "affected_node_count": len(depths),
        "depths": dict(sorted(depths.items())),
        "relationship_types_encountered": dict(sorted(rels.items())),
        "confidence_distribution": dict(sorted(confidences.items())),
        "status_distribution": dict(sorted(statuses.items())),
    }


def find_cycles(deps: list[dict[str, Any]]) -> list[list[str]]:
    outgoing, _incoming = build_graphs(deps)
    found: set[tuple[str, ...]] = set()
    cycles: list[list[str]] = []

    def canonical(cycle: list[str]) -> tuple[str, ...]:
        body = cycle[:-1]
        rotations = [tuple(body[i:] + body[:i]) for i in range(len(body))]
        best = min(rotations)
        return best + (best[0],)

    def dfs(start: str, current: str, path: list[str]) -> None:
        for dep in sorted(outgoing.get(current, []), key=lambda d: (str(d.get("target", "")), str(d.get("id", "")))):
            nxt = str(dep.get("target", ""))
            if nxt == start:
                can = canonical(path + [start])
                if can not in found:
                    found.add(can); cycles.append(list(can))
            elif nxt not in path:
                dfs(start, nxt, path + [nxt])

    for node in nodes_from(deps):
        dfs(node, node, [node])
    return sorted(cycles)


def registry_diagnostics(deps: list[dict[str, Any]]) -> dict[str, Any]:
    ids = [str(dep.get("id")) for dep in deps if dep.get("id")]
    id_counts = Counter(ids)
    nodes = nodes_from(deps)
    incoming_counts = Counter(str(dep.get("target")) for dep in deps if dep.get("target"))
    outgoing_counts = Counter(str(dep.get("source")) for dep in deps if dep.get("source"))
    broken = []
    missing_nodes = []
    for dep in deps:
        for field in ("source", "target"):
            value = dep.get(field)
            if not value:
                missing_nodes.append({"id": dep.get("id", "unknown"), "field": field})
            elif not (ROOT / str(value)).exists():
                broken.append({"id": dep.get("id", "unknown"), "field": field, "node": str(value)})
    return {
        "duplicate_ids": sorted([id_ for id_, count in id_counts.items() if count > 1]),
        "broken_references": sorted(broken, key=lambda x: (str(x["id"]), x["field"], x.get("node", ""))),
        "missing_nodes": sorted(missing_nodes, key=lambda x: (str(x["id"]), x["field"])),
        "nodes_with_no_incoming_edges": sorted([n for n in nodes if incoming_counts[n] == 0]),
        "nodes_with_no_outgoing_edges": sorted([n for n in nodes if outgoing_counts[n] == 0]),
        "orphan_registry_entries": sorted([n for n in nodes if incoming_counts[n] == 0 and outgoing_counts[n] == 0]),
        "cycles": find_cycles(deps),
    }


def histogram(values: list[int]) -> dict[str, int]:
    return {str(k): v for k, v in sorted(Counter(values).items())}


def full_analysis(node: str | None = None) -> dict[str, Any]:
    deps = records()
    nodes = nodes_from(deps)
    impacts = {n: impact_for(n, deps) for n in nodes}
    diag = registry_diagnostics(deps)
    return {
        "registry": rel(REGISTRY),
        "summary": {"dependency_records": len(deps), "registry_nodes": len(nodes), "registry_edges": len(deps)},
        "registry_statistics": {
            "source_types": dict(sorted(Counter(str(d.get("source_type", "unknown")) for d in deps).items())),
            "target_types": dict(sorted(Counter(str(d.get("target_type", "unknown")) for d in deps).items())),
        },
        "dependency_depth_histogram": histogram([i["dependency_depth"] for i in impacts.values()]),
        "top_20_highest_impact_nodes": sorted(impacts.values(), key=lambda i: (-i["affected_node_count"], i["node"]))[:20],
        "diagnostics": diag,
        "confidence_summary": dict(sorted(Counter(str(d.get("confidence", "unknown")) for d in deps).items())),
        "status_summary": dict(sorted(Counter(str(d.get("status", "unknown")) for d in deps).items())),
        "relationship_summary": dict(sorted(Counter(str(d.get("relationship", "unknown")) for d in deps).items())),
        "node_impact": impact_for(node, deps) if node else None,
    }


def table(counter: dict[str, int]) -> list[str]:
    lines = ["| Value | Count |", "|---|---:|"]
    lines += [f"| `{k}` | {v} |" for k, v in counter.items()] or ["| None | 0 |"]
    return lines


def bullet_nodes(values: list[str]) -> list[str]:
    return [f"- `{v}`" for v in values] or ["- None detected."]


def write_report(data: dict[str, Any]) -> None:
    diag = data["diagnostics"]
    lines = [
        "# Theory Impact Report", "",
        "Results are based only on registered dependencies in `theory/dependencies/dependency-registry.yaml` and do not imply semantic dependence.", "",
        "## Summary", "",
        f"- Dependency records: {data['summary']['dependency_records']}",
        f"- Registry nodes: {data['summary']['registry_nodes']}",
        f"- Registry edges: {data['summary']['registry_edges']}",
        "- Dependency inference: disabled; absent registry edges are never inferred.", "",
        "## Registry Statistics", "", "### Source Types", "", *table(data["registry_statistics"]["source_types"]), "", "### Target Types", "", *table(data["registry_statistics"]["target_types"]), "",
        "## Dependency Depth Histogram", "", *table(data["dependency_depth_histogram"]), "",
        "## Top 20 Highest-Impact Nodes", "", "| Node | Affected Nodes | Max Depth |", "|---|---:|---:|",
    ]
    for item in data["top_20_highest_impact_nodes"]:
        lines.append(f"| `{item['node']}` | {item['affected_node_count']} | {item['dependency_depth']} |")
    lines += ["", "## Nodes with No Incoming Edges", "", *bullet_nodes(diag["nodes_with_no_incoming_edges"]), "", "## Nodes with No Outgoing Edges", "", *bullet_nodes(diag["nodes_with_no_outgoing_edges"]), "", "## Circular Dependency Analysis", ""]
    lines += ["- " + " -> ".join(f"`{n}`" for n in c) for c in diag["cycles"]] or ["- No circular dependency chains detected."]
    lines += ["", "## Broken Dependency Analysis", ""]
    lines += [f"- `{b['id']}` {b['field']}: `{b['node']}`" for b in diag["broken_references"]] or ["- No broken references detected."]
    lines += ["", "## Missing Node Analysis", ""]
    lines += [f"- `{m['id']}` is missing `{m['field']}`." for m in diag["missing_nodes"]] or ["- No missing source or target node fields detected."]
    lines += ["", "## Duplicate ID Analysis", "", *bullet_nodes(diag["duplicate_ids"]), "", "## Orphan Registry Entries", "", "Orphan registry entries are defined here as registered nodes with neither incoming nor outgoing registry edges after registry parsing.", "", *bullet_nodes(diag["orphan_registry_entries"]), "", "## Confidence Summary", "", *table(data["confidence_summary"]), "", "## Status Summary", "", *table(data["status_summary"]), "", "## Relationship Summary", "", *table(data["relationship_summary"]), "", "## Known Limitations", "", "- The analyzer uses only explicit registry edges.", "- Results do not imply semantic dependence.", "- Missing registry edges mean unknown impact, not no impact.", "- File existence checks validate repository paths only, not theory correctness.", ""]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node", help="Registry node to analyze for downstream impact.")
    parser.add_argument("--json", action="store_true", help="Print deterministic JSON instead of status text.")
    args = parser.parse_args()
    data = full_analysis(args.node)
    write_report(data)
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(f"{rel(OUT)} generated")
        if args.node:
            impact = data["node_impact"]
            print(f"node: {args.node}")
            print(f"affected_node_count: {impact['affected_node_count']}")
            print(f"dependency_depth: {impact['dependency_depth']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
