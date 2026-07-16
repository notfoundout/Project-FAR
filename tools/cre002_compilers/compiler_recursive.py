#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

EXPECTED = "CRE-002-EXT-001-SCENARIO-1.0"
REQUIRED = {"scenario_id","title","status","semantic_authority","bounds","initial_state","evidence_schema","transitions","interleaving","invariants","outputs"}

def validate(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict): raise ValueError("scenario must be an object")
    missing = REQUIRED - set(value)
    if missing: raise ValueError(f"missing keys: {sorted(missing)}")
    if value.get("scenario_id") != EXPECTED: raise ValueError("unexpected scenario_id")
    transitions = value.get("transitions")
    if not isinstance(transitions, list) or not transitions: raise ValueError("transitions must be non-empty")
    ids = [x.get("id") for x in transitions if isinstance(x, dict)]
    if len(ids) != len(transitions) or any(not x for x in ids) or len(ids) != len(set(ids)): raise ValueError("transition ids must be present and unique")
    return value

def rebuild(value: Any) -> Any:
    if isinstance(value, dict): return {k: rebuild(value[k]) for k in sorted(value)}
    if isinstance(value, list): return [rebuild(x) for x in value]
    return value

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("source",type=Path); p.add_argument("output",type=Path); a=p.parse_args()
    result=rebuild(validate(json.loads(a.source.read_text(encoding="utf-8"))))
    a.output.write_text(json.dumps(result,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n",encoding="utf-8")
    return 0
if __name__=="__main__": raise SystemExit(main())
