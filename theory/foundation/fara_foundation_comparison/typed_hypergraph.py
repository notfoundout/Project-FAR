"""Independent finite evaluator for the frozen typed-hypergraph candidate."""
from __future__ import annotations
import json, sys
SIGNATURE_VERSION="typed-hypergraph/1.0"
NODE_TYPES=("entity","token","meaning","rule","state","objective","condition")
EDGE_TYPES={"denotes":("token","entity"),"interprets":("token","meaning"),"applies":("rule","state","state"),"targets":("objective","condition")}
def validate(model):
    errors=[]; nodes=model.get("nodes",{}); seen=set()
    for edge in model.get("edges",[]):
        if edge.get("id") in seen: errors.append("duplicate edge identity")
        seen.add(edge.get("id")); typ=edge.get("type")
        if typ not in EDGE_TYPES: errors.append(f"undeclared edge type: {typ}"); continue
        ends=edge.get("ends",[])
        if len(ends)!=len(EDGE_TYPES[typ]) or any(n not in nodes for n in ends): errors.append(f"ill-typed edge: {edge.get('id')}")
        elif tuple(nodes[n] for n in ends)!=EDGE_TYPES[typ]: errors.append(f"invalid endpoint typing: {edge.get('id')}")
    return errors
def execute(model):
    errors=validate(model)
    if errors:return {"status":"Fail","errors":errors,"steps":[]}
    active=set(model.get("active_states",[])); steps=[]
    for edge in model.get("edges",[]):
        if edge["type"]=="applies" and edge["ends"][1] in active:
            active.add(edge["ends"][2]); steps.append({"edge":edge["id"],"path":edge["ends"]})
    return {"status":"Pass","states":sorted(active),"steps":steps}
def main():
    model=json.load(sys.stdin); print(json.dumps(execute(model),sort_keys=True)); return bool(validate(model))
if __name__=="__main__": raise SystemExit(main())
