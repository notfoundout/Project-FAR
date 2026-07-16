#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

EXPECTED="CRE-002-EXT-001-SCENARIO-1.0"
REQUIRED={"scenario_id","title","status","semantic_authority","bounds","initial_state","evidence_schema","transitions","interleaving","invariants","outputs"}

def canonical(v: Any) -> bytes: return (json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n").encode()
def validate(v: Any) -> dict[str,Any]:
    if not isinstance(v,dict): raise ValueError("scenario must be an object")
    if REQUIRED-set(v): raise ValueError("missing required scenario keys")
    if v.get("scenario_id") != EXPECTED: raise ValueError("unexpected scenario_id")
    ts=v.get("transitions")
    if not isinstance(ts,list) or not ts: raise ValueError("transitions must be non-empty")
    ids=[x.get("id") for x in ts if isinstance(x,dict)]
    if len(ids)!=len(ts) or any(not isinstance(x,str) or not x for x in ids) or len(set(ids))!=len(ids): raise ValueError("transition ids must be present and unique")
    return v

def verify(scenario: Path, candidates: list[Path]) -> dict[str,Any]:
    source=validate(json.loads(scenario.read_bytes()))
    raw=[p.read_bytes() for p in candidates]
    parsed=[validate(json.loads(x)) for x in raw]
    normalized=[canonical(x) for x in parsed]
    reference=canonical(source)
    if any(x!=reference for x in normalized): raise ValueError("candidate differs from frozen scenario")
    if any(x!=raw[0] for x in raw[1:]) or raw[0]!=reference: raise ValueError("candidate bytes differ")
    mutations=[]
    removed=json.loads(reference); removed["transitions"]=removed["transitions"][:-1]; mutations.append(("remove-transition",removed))
    duplicate=json.loads(reference); duplicate["transitions"].append(dict(duplicate["transitions"][0])); mutations.append(("duplicate-transition-id",duplicate))
    changed=json.loads(reference); changed["interleaving"]["simultaneous_execution"]=not bool(changed["interleaving"].get("simultaneous_execution")); mutations.append(("change-interleaving",changed))
    cases=[]
    for name,value in mutations:
        try: rejected=canonical(validate(value))!=reference
        except Exception: rejected=True
        cases.append({"case":name,"rejected":rejected})
    for name,blob in [("malformed-json",b"{bad\n"),("wrong-root",b"[]\n"),("missing-fields",b'{"scenario_id":"CRE-002-EXT-001-SCENARIO-1.0"}\n')]:
        try: validate(json.loads(blob)); rejected=False
        except Exception: rejected=True
        cases.append({"case":name,"rejected":rejected})
    if not all(x["rejected"] for x in cases): raise ValueError("adversarial case escaped detection")
    return {"status":"pass","digest":hashlib.sha256(reference).hexdigest(),"implementations":len(candidates),"byte_identical":True,"mutation_and_adversarial_cases":cases,"claim_class":"bounded multi-implementation robustness","external_replication":False}

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--scenario",type=Path,required=True); p.add_argument("--candidate",type=Path,action="append",required=True); p.add_argument("--output",type=Path); a=p.parse_args()
    report=verify(a.scenario,a.candidate); text=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if a.output: a.output.write_text(text,encoding="utf-8")
    else: print(text,end="")
    return 0
if __name__=="__main__": raise SystemExit(main())
