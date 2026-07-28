"""Independent finite evaluator for the frozen algebraic/state-transition candidate."""
from __future__ import annotations
import json, sys
SIGNATURE_VERSION="algebraic-state-transition/1.0"
SORTS=("Carrier","State","Operation","MeaningAlgebra")
def validate(model):
    errors=[]; ops=model.get("operations",{})
    for name,op in ops.items():
        if set(op)!={"domain","mapping"}: errors.append(f"ill-formed operation: {name}")
        elif any(source not in op["domain"] for source in op["mapping"]): errors.append(f"operation outside domain: {name}")
    for pair,result in model.get("composition",{}).items():
        if len(pair.split(";"))!=2 or result not in ops: errors.append(f"invalid composition: {pair}")
    return errors
def execute(model):
    errors=validate(model)
    if errors:return {"status":"Fail","errors":errors,"steps":[]}
    state=model.get("initial_state"); steps=[]
    for name in model.get("program",[]):
        op=model.get("operations",{}).get(name)
        if not op or state not in op["mapping"]: return {"status":"Partial","state":state,"steps":steps,"reason":"partial operation undefined"}
        nxt=op["mapping"][state]; steps.append({"operation":name,"source":state,"target":nxt}); state=nxt
    return {"status":"Pass","state":state,"steps":steps}
def main():
    model=json.load(sys.stdin); print(json.dumps(execute(model),sort_keys=True)); return bool(validate(model))
if __name__=="__main__": raise SystemExit(main())
