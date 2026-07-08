#!/usr/bin/env python3
"""Generate JSON and Mermaid dependency graphs from the dependency registry."""
from __future__ import annotations

from collections import Counter
import json
import re

from dependency_utils import ROOT, dependencies

JSON_OUT = ROOT / "docs/reports/dependency-graph.json"
MMD_OUT = ROOT / "docs/reports/dependency-graph.mmd"


def safe_id(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9_]", "_", value)
    if not re.match(r"[A-Za-z_]", token):
        token = "n_" + token
    return token[:80]


def main() -> int:
    deps = dependencies()
    node_types: dict[str, str] = {}
    for dep in deps:
        node_types.setdefault(dep["source"], dep["source_type"])
        node_types.setdefault(dep["target"], dep["target_type"])
    nodes = [{"id": node, "type": node_type} for node, node_type in sorted(node_types.items())]
    edges = [
        {
            "id": dep["id"],
            "source": dep["source"],
            "target": dep["target"],
            "relationship": dep["relationship"],
            "confidence": dep["confidence"],
            "status": dep["status"],
        }
        for dep in deps
    ]
    graph = {
        "metadata": {
            "schema": "project-far-dependency-graph-v0.4",
            "source_registry": "theory/dependencies/dependency-registry.yaml",
            "node_count": len(nodes),
            "edge_count": len(edges),
        },
        "nodes": nodes,
        "edges": edges,
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")

    type_counts = Counter(node["type"] for node in nodes)
    lines = ["flowchart TD", "  %% Generated from theory/dependencies/dependency-registry.yaml"]
    for node_type in sorted(type_counts):
        lines.append(f"  subgraph {safe_id('type_' + node_type)}[{node_type}]")
        for node in nodes:
            if node["type"] == node_type:
                lines.append(f"    {safe_id(node['id'])}[\"{node['id']}\"]")
        lines.append("  end")
    for edge in edges:
        lines.append(
            f"  {safe_id(edge['source'])} -- \"{edge['relationship']}\" --> {safe_id(edge['target'])}"
        )
    MMD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{JSON_OUT.relative_to(ROOT)} generated")
    print(f"{MMD_OUT.relative_to(ROOT)} generated")
    print(f"nodes: {len(nodes)}")
    print(f"edges: {len(edges)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
