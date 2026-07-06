#!/usr/bin/env python3
"""Prototype reasoning engine for machine-readable FAR objects."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from parse_far import load_far_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Run prototype FAR reasoning-engine diagnostics")
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true", help="emit machine-readable proof trace JSON")
    args = parser.parse_args()

    try:
        far = load_far_yaml(args.path)
        errors = far.validate_well_formed()
    except Exception as exc:
        print("REASONING ENGINE FAILED: object is not well-formed")
        print(f"- {exc}")
        return 1

    if errors:
        print("REASONING ENGINE FAILED: object is not well-formed")
        for error in errors:
            print(f"- {error}")
        return 1

    trace = far.proof_trace()
    if args.json:
        print(json.dumps(trace, indent=2, sort_keys=True))
        return 0

    cycles = trace["cycles"]
    derivation_tree = trace["derivation_tree"]

    print("REASONING ENGINE REPORT")
    print(f"investigation: {far.investigation}")
    print(f"representations: {len(far.representations)}")
    print(f"dependency edges: {len(trace['dependency_edges'])}")
    print(f"cycles: {len(cycles)}")

    if cycles:
        print("detected cycles:")
        for cycle in cycles:
            print("- " + " -> ".join(cycle))

    print("derivation tree:")
    for node in derivation_tree:
        print(
            f"- {node['order']}: {node['id']} "
            f"[{node['status']}] via {node['rule']} "
            f"from {node['source']} to {node['target']}"
        )

    statuses = {"admissible": 0, "unresolved": 0, "inadmissible": 0, "draft": 0}
    for transition in far.transitions.values():
        statuses[transition.status] = statuses.get(transition.status, 0) + 1

    print("transition summary:")
    for status in ["admissible", "unresolved", "inadmissible", "draft"]:
        print(f"- {status}: {statuses.get(status, 0)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
