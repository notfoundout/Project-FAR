#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

EXPECTED="CRE-002-EXT-001-SCENARIO-1.0"
REQUIRED={"scenario_id","title","status","semantic_authority","bounds","initial_state","evidence_schema","transitions","interleaving","invariants","outputs"}
TAG=object()

def hook(items: list[tuple[str,Any]]) -> tuple[object,list[tuple[str,Any]]]: return (TAG,items)

def materialize(v: Any) -> Any:
    if isinstance(v,tuple) and len(v)==2 and v[0] is TAG:
        return {str(k):materialize(x) for k,x in sorted(v[1],key=lambda pair:pair[0])}
    if isinstance(v,list): return [materialize(x) for x in v]
    return v

def validate(v: Any) -> dict[str,Any]:
    if not isinstance(v,dict): raise ValueError("scenario must be an object")
    missing=sorted(REQUIRED.difference(v))
    if missing: raise ValueError(f"missing keys: {missing}")
    if v.get("scenario_id") != EXPECTED: raise ValueError("unexpected scenario_id")
    ts=v.get("transitions")
    if not isinstance(ts,list) or not ts: raise ValueError("transitions must be non-empty")
    ids=[]
    for item in ts:
        if not isinstance(item,dict) or not isinstance(item.get("id"),str) or not item["id"]: raise ValueError("transition ids must be present and unique")
        ids.append(item["id"])
    if len(set(ids)) != len(ids): raise ValueError("transition ids must be present and unique")
    return v

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("source",type=Path); p.add_argument("output",type=Path); a=p.parse_args()
    parsed=json.loads(a.source.read_text(encoding="utf-8"),object_pairs_hook=hook)
    result=validate(materialize(parsed))
    a.output.write_text(json.dumps(result,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n",encoding="utf-8")
    return 0
if __name__=="__main__": raise SystemExit(main())
