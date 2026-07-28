#!/usr/bin/env python3
"""Executable fail-closed validator for FARA-INV-W5-001."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "theory/evaluation/fara-w5-cross-representation-invariance-v1.0.json"
REPORT = ROOT / "theory/evaluation/generated-fara-w5-invariance-summary.md"
DIMENSIONS = ("structural","semantic","operational","dependency","information","historical")
STATUSES = {"Pass","Partial","Fail","Unknown"}
FAMILIES = {"lsts","trs","graphs","logic","traces","tables"}
TOPICS = {"deterministic transitions","probabilistic information","nonmonotonic revision","paraconsistent consequence","causal intervention","changing rules or semantics","identity merge and deletion","provenance-sensitive history","distributed partial order","external oracle dependence","continuous case","embodied case"}
TERMINALS = {"bounded invariance under a frozen representation class","explicit representation-sensitive counterexample","unresolved because equivalence, recovery, or coverage is insufficient"}
OWNER_FIELDS = ("id","proof_object_id","claim_id","theorem_id")
CANONICAL_SHA256 = "e9070a503b46a2371192d97ed470403b47ef4da697861464101bce4cdc0e6a78"

def load():
    return json.loads(ARTIFACT.read_text(encoding="utf-8"))

def digest(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def encode(family, source, spec):
    """Construct a family-native executable object from the declared source."""
    if not spec["available"]:
        return None
    kept = {d: source[d] for d in DIMENSIONS if d not in spec["drops"]}
    if family == "lsts":
        return {"family":"lsts","states":[kept.get("structural")],"labels":[kept.get("semantic")],"transition":kept.get("operational"),"dependency":kept.get("dependency"),"information":kept.get("information"),"history":kept.get("historical")}
    if family == "trs":
        return {"family":"trs","sorts":[kept.get("structural")],"interpretation":kept.get("semantic"),"relations":{"step":kept.get("operational"),"dependency":kept.get("dependency"),"information":kept.get("information"),"history":kept.get("historical")}}
    if family == "graphs":
        return {"family":"graphs","vertices":[kept.get("structural")],"semantic_edge":kept.get("semantic"),"operation_edge":kept.get("operational"),"dependency_edge":kept.get("dependency"),"information_edge":kept.get("information"),"history_edge":kept.get("historical")}
    if family == "logic":
        return {"family":"logic","signature":kept.get("structural"),"axioms":kept.get("semantic"),"rules":kept.get("operational"),"dependency":kept.get("dependency"),"information":kept.get("information"),"history":kept.get("historical")}
    if family == "traces":
        return {"family":"traces","event_types":kept.get("structural"),"labels":kept.get("semantic"),"events":kept.get("operational"),"causality":kept.get("dependency"),"payload":kept.get("information"),"order":kept.get("historical")}
    if family == "tables":
        return {"family":"tables","state_table":kept.get("structural"),"semantic_table":kept.get("semantic"),"step_table":kept.get("operational"),"dependency_table":kept.get("dependency"),"information_table":kept.get("information"),"history_table":kept.get("historical")}
    raise AssertionError(f"unknown family: {family}")

def recover(encoded):
    if encoded is None:
        return None
    family = encoded["family"]
    maps = {
        "lsts": {"structural":("states",0),"semantic":"labels","operational":"transition","dependency":"dependency","information":"information","historical":"history"},
        "trs": {"structural":("sorts",0),"semantic":"interpretation","operational":("relations","step"),"dependency":("relations","dependency"),"information":("relations","information"),"historical":("relations","history")},
        "graphs": {"structural":("vertices",0),"semantic":"semantic_edge","operational":"operation_edge","dependency":"dependency_edge","information":"information_edge","historical":"history_edge"},
        "logic": {"structural":"signature","semantic":"axioms","operational":"rules","dependency":"dependency","information":"information","historical":"history"},
        "traces": {"structural":"event_types","semantic":"labels","operational":"events","dependency":"causality","information":"payload","historical":"order"},
        "tables": {"structural":"state_table","semantic":"semantic_table","operational":"step_table","dependency":"dependency_table","information":"information_table","historical":"history_table"},
    }[family]
    out={}
    for dim, key in maps.items():
        if isinstance(key,tuple):
            if len(key)==2 and isinstance(key[1],int):
                value=encoded.get(key[0],[])
                out[dim]=value[key[1]] if value and value[key[1]] is not None else None
            else:
                value=encoded.get(key[0],{})
                out[dim]=value.get(key[1])
        else:
            value=encoded.get(key)
            if dim=="semantic" and family=="lsts":
                out[dim]=value[0] if value and value[0] is not None else None
            else:
                out[dim]=value
    return out

def adjudicate(case):
    source=case["source"]
    recovered={}
    for family in case["representations"]:
        encoded=encode(family,source,case["representation_execution"][family])
        recovered[family]=recover(encoded)
    if any(v is None for v in recovered.values()):
        vector={d:"Unknown" for d in DIMENSIONS}
        return {"preservation":vector,"recovery":"unknown","admissible_pair":False,"conclusion_agreement":None}
    vector={}
    for dim in DIMENSIONS:
        values=[recovered[f][dim] for f in case["representations"]]
        vector[dim]="Pass" if all(v==source[dim] for v in values) else "Fail"
    exact=all(v=="Pass" for v in vector.values())
    conclusions=[]
    for f in case["representations"]:
        r=recovered[f]
        if any(r[d] is None for d in DIMENSIONS):
            conclusions.append(None)
        else:
            conclusions.append(hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest())
    agreement = conclusions[0] == conclusions[1] if exact else None
    return {"preservation":vector,"recovery":"exact" if exact else "partial","admissible_pair":exact,"conclusion_agreement":agreement}

def _owners(value,out):
    if isinstance(value,dict):
        for key,item in value.items():
            if key in OWNER_FIELDS and isinstance(item,str):
                out.add((key,item))
            _owners(item,out)
    elif isinstance(value,list):
        for item in value:
            _owners(item,out)

def duplicate_owner_paths(data):
    expected={(field,data[field]) for field in OWNER_FIELDS}; hits=[]
    for path in (ROOT/"theory/evaluation").glob("*.json"):
        if path==ARTIFACT: continue
        try: parsed=json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError,UnicodeDecodeError,OSError): continue
        got=set(); _owners(parsed,got)
        if expected & got: hits.append(str(path.relative_to(ROOT)))
    return hits

def validate(data, canonical=True):
    assert data["id"]=="FARA-INV-W5-001"
    assert data["proof_object_id"]=="FARA-W5-PROOF-001"
    assert data["claim_id"]=="CLM-INV-W5-001"
    assert data["theorem_id"]=="THM-INV-001"
    assert data["terminal_result"]=="unresolved because equivalence, recovery, or coverage is insufficient"
    assert data["status"]==data["terminal_result"]
    ar=data["authority_recovery"]
    assert ar["dependencies"]==["FARA-W1-PRIMITIVE-INDEPENDENCE-001","FARA-OPS-W2-001","FARA-REP-W4-001"]
    assert set(data["representation_families"])==FAMILIES
    assert set(data["contract"]["preservation_dimensions"])==set(DIMENSIONS)
    assert set(data["contract"]["outputs"])==TERMINALS
    assert "never defined by conclusion agreement" in data["contract"]["equivalence_criteria"]
    assert "decoder-held rule or conclusion" in data["contract"]["forbidden_hidden_machinery"]
    assert len(data["cases"])==12
    assert {c["topic"] for c in data["cases"]}==TOPICS
    assert len({c["id"] for c in data["cases"]})==12
    for case in data["cases"]:
        assert len(case["representations"])==2 and set(case["representations"])<=FAMILIES
        assert set(case["representation_execution"])==set(case["representations"])
        assert set(case["source"])==set(DIMENSIONS)
        assert set(case["preservation"])==set(DIMENSIONS)
        assert set(case["preservation"].values())<=STATUSES
        observed=adjudicate(case)
        assert observed["preservation"]==case["preservation"], f"fixture preservation drift: {case['id']}"
        assert observed["recovery"]==case["recovery"], f"fixture recovery drift: {case['id']}"
        assert observed["admissible_pair"] is case["admissible_pair"], f"admissibility drift: {case['id']}"
        assert observed["conclusion_agreement"] is case["conclusion_agreement"], f"conclusion drift: {case['id']}"
        if case["classification"]=="positive":
            assert case["admissible_pair"] and case["recovery"]=="exact" and case["conclusion_agreement"] is True
        elif case["classification"]=="inadmissible_boundary":
            assert not case["admissible_pair"] and case["conclusion_agreement"] is None and any(v=="Fail" for v in case["preservation"].values())
        elif case["classification"]=="unresolved":
            assert case["recovery"]=="unknown" and all(v=="Unknown" for v in case["preservation"].values())
        else:
            raise AssertionError(f"invalid classification: {case['classification']}")
    assert all(x["disposition"]!="accepted invariance counterexample" for x in data["failed_counterexample_attempts"])
    assert data["claim_levels"]["representation_independence"]=="unresolved"
    assert data["claim_levels"]["all_registered_representations"].startswith("unresolved")
    assert "inadmissible pairs refute invariance" in data["nonclaims"]
    assert data["remaining_obligations"]==[
        "produce an exact all-six-preserving same-source pair with different conclusions or retain unresolved",
        "independent specification and replication of each family",
        "formal semantic equivalence for nonclassical consequence",
        "nonfinite recovery theory for continuous systems",
        "environment-inclusive embodied equivalence",
        "oracle transcript/live-service boundary adjudication",
    ]
    if canonical:
        assert digest(data)==CANONICAL_SHA256, "canonical artifact drift"

def report(data):
    lines=["# Generated FARA W5 cross-representation invariance summary","",
           "Generated deterministically by `python tools/check_fara_w5_invariance.py --write`.","",
           "## Terminal adjudication","",data["strongest_result"],"",
           "## Executed fixture matrix","",
           "| Fixture | Pair | S/Sem/O/D/I/H | Recovery | Admissible | Agreement | Classification |",
           "|---|---|---|---|---:|---|---|"]
    for case in data["cases"]:
        vec="/".join(case["preservation"][d] for d in DIMENSIONS)
        agreement="Unknown" if case["conclusion_agreement"] is None else str(case["conclusion_agreement"])
        lines.append(f"| {case['id']} {case['topic']} | {' ↔ '.join(case['representations'])} | {vec} | {case['recovery']} | {str(case['admissible_pair']).lower()} | {agreement} | {case['classification']} |")
    lines += ["","## Failed counterexample attempts",""]
    lines += [f"- **{x['id']} ({x['kind']}):** {x['disposition']} — {x['reason']}" for x in data["failed_counterexample_attempts"]]
    for title,key in [("Refuted claims","refuted_claims"),("Unresolved claims","unresolved_claims"),("Explicit nonclaims","nonclaims"),("Remaining obligations","remaining_obligations"),("Self-review","self_review")]:
        lines += ["",f"## {title}",""]+[f"- {item}" for item in data[key]]
    return "\n".join(lines)+"\n"

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--write",action="store_true"); args=parser.parse_args()
    data=load(); validate(data)
    expected=report(data)
    if args.write: REPORT.write_text(expected,encoding="utf-8")
    else: assert REPORT.read_text(encoding="utf-8")==expected, "generated report stale"
    owners=duplicate_owner_paths(data); assert not owners, f"duplicate identifier owners: {owners}"
    print("FARA W5 invariance: PASS (12 fixtures executed; 2 admissible invariant pairs; terminal unresolved)")

if __name__=="__main__":
    main()
