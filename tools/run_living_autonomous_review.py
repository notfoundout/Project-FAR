#!/usr/bin/env python3
"""Compatibility entry point for bounded autonomous living-research review."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from tools.living_autonomous_review_core import *
from tools.living_autonomous_review_model import *
from tools.living_autonomous_review_plan import *
from tools.living_autonomous_review_build import *

def materialize(plan: dict[str, Any], out_root: Path) -> None:
    out_root.mkdir(parents=True, exist_ok=True)
    manifest = {k: v for k, v in plan.items() if k not in {"review_files", "inbox_files"}}
    (out_root / "manifest.json").write_bytes(pretty_bytes(manifest))
    for field, folder in (("review_files", "review"), ("inbox_files", "inbox")):
        for rel, raw in plan.get(field, {}).items():
            path = out_root / folder / promoter.safe(rel)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--out-root", required=True)
    parser.add_argument("--model")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    try:
        policy = load_json(root / POLICY)
        validate_policy(policy)
        model = GeminiModel(args.model or policy["default_model"], os.environ.get("GEMINI_API_KEY", ""))
        plan = build_plan(root, Path(args.source_root).resolve(), model)
        materialize(plan, Path(args.out_root).resolve())
        print(json.dumps({k: v for k, v in plan.items() if k not in {"review_files", "inbox_files"}}, sort_keys=True))
        return 0
    except ReviewError as exc:
        print(f"living autonomous review failed closed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
