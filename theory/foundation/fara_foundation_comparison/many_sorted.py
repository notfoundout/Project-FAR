"""Independent finite evaluator for the frozen many-sorted relational candidate."""
from __future__ import annotations
import json, sys
SIGNATURE_VERSION="many-sorted-relational/1.0"
SORTS=("Entity","Token","Meaning","Rule","State","Event","Objective","Condition","Relation")
SYMBOLS={"denotes":("Token","Entity"),"interprets":("Token","Meaning"),"applies":("Rule","State","State"),"targets":("Objective","Condition")}
def validate(model):
    errors=[]; declared=set(SORTS)
    for name,sorts in model.get("relations",{}).items():
        if name not in SYMBOLS: errors.append(f"undeclared symbol: {name}"); continue
        if any(s not in declared for s in SYMBOLS[name]): errors.append(f"undeclared sort in {name}")
        if any(len(row)!=len(SYMBOLS[name]) for row in sorts): errors.append(f"ill-typed tuple in {name}")
    return errors
def execute(model):
    errors=validate(model)
    if errors:return {"status":"Fail","errors":errors,"steps":[]}
    states=list(model.get("states",[])); steps=[]
    for rule,source,target in model.get("relations",{}).get("applies",[]):
        if source in states: states.append(target); steps.append({"rule":rule,"source":source,"target":target})
    return {"status":"Pass","states":sorted(set(states)),"steps":steps}
def main():
    model=json.load(sys.stdin); print(json.dumps(execute(model),sort_keys=True)); return bool(validate(model))
if __name__=="__main__": raise SystemExit(main())
