#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

EXPECTED="CRE-002-EXT-001-SCENARIO-1.0"
REQUIRED=("scenario_id","title","status","semantic_authority","bounds","initial_state","evidence_schema","transitions","interleaving","invariants","outputs")

def validate(v: Any) -> dict[str, Any]:
    if type(v) is not dict: raise ValueError("scenario must be an object")
    absent=[k for k in REQUIRED if k not in v]
    if absent: raise ValueError(f"missing keys: {absent}")
    if v["scenario_id"] != EXPECTED: raise ValueError("unexpected scenario_id")
    ts=v["transitions"]
    if type(ts) is not list or len(ts)==0: raise ValueError("transitions must be non-empty")
    seen=set()
    for t in ts:
        if type(t) is not dict or not isinstance(t.get("id"),str) or not t["id"] or t["id"] in seen: raise ValueError("transition ids must be present and unique")
        seen.add(t["id"])
    return v

def normalize(root: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any]={}
    stack=[(out,k,root[k]) for k in sorted(root,reverse=True)]
    while stack:
        parent,key,value=stack.pop()
        if type(value) is dict:
            child={}; parent[key]=child
            for k in sorted(value,reverse=True): stack.append((child,k,value[k]))
        elif type(value) is list:
            child=[None]*len(value); parent[key]=child
            for i in range(len(value)-1,-1,-1): stack.append((child,i,value[i]))
        else: parent[key]=value
    return out

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("source",type=Path); p.add_argument("output",type=Path); a=p.parse_args()
    decoder=json.JSONDecoder(); parsed=decoder.decode(a.source.read_text(encoding="utf-8")); result=normalize(validate(parsed))
    a.output.write_bytes((json.dumps(result,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n").encode())
    return 0
if __name__=="__main__": raise SystemExit(main())
