from __future__ import annotations

import argparse
import json
from pathlib import Path

from .external_trace import compile_trace
from .swe_agent import load_swe_agent_trace


def _package_payload(package) -> dict:
    return {
        "schema_version": package.schema_version,
        "decision_id": package.decision_id,
        "decision_type": package.decision_type,
        "policy_version": package.policy_version,
        "decision_root": package.decision_root,
        "proposed_action": package.proposed_action,
        "nodes": [
            {
                "node_id": node.node_id,
                "kind": node.kind,
                "statement": node.statement,
                "attributes": node.attributes,
            }
            for node in package.nodes
        ],
        "dependencies": [
            {
                "source_id": dependency.source_id,
                "target_id": dependency.target_id,
                "relation": dependency.relation,
            }
            for dependency in package.dependencies
        ],
        "authorization_requirements": list(package.authorization_requirements),
        "unknowns": list(package.unknowns),
        "trace_completeness": package.trace_completeness,
        "metadata": package.metadata,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="far-external-trace")
    parser.add_argument("trajectory")
    parser.add_argument("--format", choices=["swe-agent"], default="swe-agent")
    parser.add_argument("--trace-id")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        trace = load_swe_agent_trace(args.trajectory, trace_id=args.trace_id)
        package = compile_trace(trace)
    except ValueError as exc:
        print(json.dumps({"status": "invalid-input", "error": str(exc)}, sort_keys=True))
        return 40
    payload = _package_payload(package)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "compiled", "decision_id": package.decision_id, "output": str(target)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
