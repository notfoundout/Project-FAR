#!/usr/bin/env python3
"""Prototype reasoning engine for machine-readable FAR objects."""

from __future__ import annotations

import argparse
from pathlib import Path

from parse_far import load_far_yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Run prototype FAR reasoning-engine diagnostics")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    far = load_far_yaml(args.path)
    errors = far.validate_well_formed()
    if errors:
        print("REASONING ENGINE FAILED: object is not well-formed")
        for error in errors:
            print(f"- {error}")
        return 1

    cycles = far.detect_cycles()
    derivation_tree = far.derivation_tree()

    print("REASONING ENGINE REPORT")
    print(f"investigation: {far.investigation}")
    print(f"representations: {len(far.representations)}")
    print(f"dependency edges: {len(far.dependency_edges())}")
    print(f"cycles: {len(cycles)}")

    if cycles:
        print("detected cycles:")
        for cycle in cycles:
            print("- " + " -> ".join(cycle))

    print("derivation tree:")
    for node in derivation_tree:
        print(
            f"- {node['order']}: {node['transition']} "
            f"[{node['status']}] via {node['rule']} "
            f"from {node['source']} to {node['target']}"
        )

    admissible = [t for t in far.transitions.values() if t.status == "admissible"]
    unresolved = [t for t in far.transitions.values() if t.status == "unresolved"]
    inadmissible = [t for t in far.transitions.values() if t.status == "inadmissible"]

    print("transition summary:")
    print(f"- admissible: {len(admissible)}")
    print(f"- unresolved: {len(unresolved)}")
    print(f"- inadmissible: {len(inadmissible)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
