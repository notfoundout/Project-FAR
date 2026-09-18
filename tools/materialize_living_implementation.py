#!/usr/bin/env python3
"""Materialize an already-authorized living-research implementation plan without executing payloads."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath

from tools.living_implementation_contract import (
    ImplementationContractError,
    expected_preimage,
    load_json,
    read_regular,
    safe_path,
    sha256,
)


def target_path(root: Path, raw: str) -> Path:
    path = safe_path(raw)
    current = root
    for part in PurePosixPath(path).parts:
        current = current / part
        if current.is_symlink():
            raise ImplementationContractError(f"symlink target rejected: {path}")
    return current


def materialize(root: Path, source_root: Path, plan: dict) -> dict:
    if plan.get("program_id") != "FAR-LIVING-IMPLEMENTATION-001" or plan.get("schema_version") != "1.0":
        raise ImplementationContractError("implementation plan identity drift")
    proposals = plan.get("proposals")
    if not isinstance(proposals, list) or not proposals or not plan.get("actionable"):
        raise ImplementationContractError("implementation plan is not actionable")
    sealed = []
    seen = set()
    for proposal in proposals:
        if not isinstance(proposal, dict):
            raise ImplementationContractError("malformed implementation proposal")
        pid = proposal.get("proposal_id")
        operations = proposal.get("operations")
        if not isinstance(pid, str) or not isinstance(operations, list) or not operations:
            raise ImplementationContractError("malformed implementation proposal")
        for operation in operations:
            target = safe_path(operation["path"])
            source_path = safe_path(operation["source_path"])
            if target in seen:
                raise ImplementationContractError(f"duplicate target: {target}")
            seen.add(target)
            if operation.get("expected_main_sha256") != expected_preimage(root, target):
                raise ImplementationContractError(f"main preimage changed before materialization: {target}")
            payload = read_regular(source_root, source_path)
            if payload is None or sha256(payload) != operation.get("result_sha256"):
                raise ImplementationContractError(f"payload changed before materialization: {target}")
            destination = target_path(root, target)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(payload)
            sealed.append({"path": target, "sha256": sha256(payload), "proposal_id": pid})
    manifest = {
        "schema_version": "1.0",
        "program_id": "FAR-LIVING-IMPLEMENTATION-001",
        "source_pr": plan["source_pr"],
        "source_branch": plan["source_branch"],
        "source_head_sha": plan["source_head_sha"],
        "base_main_sha": plan["base_main_sha"],
        "proposals": proposals,
        "sealed_files": sorted(sealed, key=lambda row: row["path"]),
    }
    manifest_path = target_path(root, plan["manifest_path"])
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--plan", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    source_root = Path(args.source_root).resolve()
    try:
        plan = load_json(Path(args.plan))
        manifest = materialize(root, source_root, plan)
    except (ImplementationContractError, KeyError, TypeError) as exc:
        print(f"living implementation materialization failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"sealed_files": len(manifest["sealed_files"]), "manifest": plan["manifest_path"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
