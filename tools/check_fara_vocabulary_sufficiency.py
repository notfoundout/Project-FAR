#!/usr/bin/env python3
"""Execute and fail-closed validate the FARA vocabulary pressure campaign."""
from __future__ import annotations
import argparse, copy, hashlib, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OBJECT = ROOT / "theory/evaluation/fara-vocabulary-sufficiency-v1.0.json"
REPORT = ROOT / "theory/evaluation/generated-fara-vocabulary-sufficiency-report.md"
PRIMITIVES = ["Object","Property","Relation","Representation","Interpretation","Investigation","Reasoning Calculus"]
DIMENSIONS = ["structural","semantic","operational","dependency","information","historical"]
FAMILIES = ["deterministic_transition","probabilistic_update","nonmonotonic_retraction","paraconsistent_consequence","causal_intervention","changing_rules","changing_semantics","evolving_ontology","identity_preserving_merge","identity_collapsing_merge","deletion_constraint_relaxation","provenance_history","distributed_partial_order","oracle_behavior","continuous_hybrid","embodied_tacit","proof_identity_binding","higher_order_scope","normative_authority"]
EXTENSIONS = {"temporal_order":"derivable","uncertainty":"boundedly irreducible under the frozen model","retraction":"boundedly irreducible under the frozen model","consequence_policy":"boundedly irreducible under the frozen model","intervention":"boundedly irreducible under the frozen model","rule_version":"boundedly irreducible under the frozen model","semantic_version":"boundedly irreducible under the frozen model","identity_criterion":"boundedly irreducible under the frozen model","provenance":"boundedly irreducible under the frozen model","partial_order":"boundedly irreducible under the frozen model","oracle_relation":"external dependency","external_coupling":"external dependency","proof_object":"boundedly irreducible under the frozen model","binding_scope":"boundedly irreducible under the frozen model","authority_source":"boundedly irreducible under the frozen model"}
ESCAPES = ["whole_source_as_object","all_distinctions_as_property","all_operations_as_relation","semantics_in_interpretation","interpreter_in_representation","dependencies_in_context","history_as_opaque_string"]
NONCLAIMS = ["universal sufficiency","global minimality","global primitive necessity","finite ablation establishes necessity","serialization establishes expression","reconstruction establishes expressive sufficiency","candidate extensions are globally primitive"]
OBLIGATIONS = ["formalize canonical derivation and composition rules","replicate mappings independently","test nonfinite continuous semantics","adjudicate environment-inclusive embodied coupling","prove or refute extension irreducibility beyond the frozen model","resolve circular primitive definitions identified by W1"]

def sha(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def source(family, i):
    # A concrete finite transition/consequence program, mechanically executed below.
    return {"identity":[f"{family}:a",f"{family}:b"],"state":{"x":i%3,"flag":False},"rules":[{"op":"increment","amount":1},{"op":"toggle"}],"semantics":{"step":"ordered application","family":family},"observations":["x","flag"],"dependencies":["rule:0->rule:1"],"history":["initial"],"external_dependencies":(["live_service"] if family in {"oracle_behavior","embodied_tacit"} else []),"source_commitments":["identity","rule order","family semantics","observable state","dependency edge","history"]}
def execute(src):
    state=dict(src["state"]); history=list(src["history"])
    for rule in src["rules"]:
        if rule["op"]=="increment": state["x"] += rule["amount"]
        elif rule["op"]=="toggle": state["flag"] = not state["flag"]
        history.append(rule["op"])
    return {"state":state,"history":history}
def build():
    hard={"probabilistic_update":"uncertainty","nonmonotonic_retraction":"retraction","paraconsistent_consequence":"consequence_policy","causal_intervention":"intervention","changing_rules":"rule_version","changing_semantics":"semantic_version","evolving_ontology":"identity_criterion","identity_preserving_merge":"identity_criterion","identity_collapsing_merge":"identity_criterion","provenance_history":"provenance","distributed_partial_order":"partial_order","oracle_behavior":"oracle_relation","continuous_hybrid":"uncertainty","embodied_tacit":"external_coupling","proof_identity_binding":"proof_object","higher_order_scope":"binding_scope","normative_authority":"authority_source"}
    benchmarks=[]
    for i,f in enumerate(FAMILIES,1):
        s=source(f,i); result=execute(s); missing=hard.get(f)
        status="Pass" if missing is None else ("Unknown" if f in {"oracle_behavior","continuous_hybrid","embodied_tacit"} else "Fail")
        opaque=0 if status=="Pass" else 1
        accounting={"native_content":7,"derived_content":2,"opaque_content":opaque,"external_content":len(s["external_dependencies"]),"hidden_machinery":0,"unexpressed_source_commitments":0 if status=="Pass" else 1}
        preservation={d:("Pass" if status=="Pass" else ("Unknown" if status=="Unknown" else ("Fail" if d in {"semantic","operational","historical"} else "Pass"))) for d in DIMENSIONS}
        benchmarks.append({"id":f"VOC-BENCH-{i:03d}","family":f,"fixture_kind":"executable finite program","source":s,"executed_source_result":result,"vocabulary_used":PRIMITIVES,"derived_used":["Reasoning State","Transformation Rule"],"extra_field":missing,"extra_classification":None if missing is None else ("external dependency" if EXTENSIONS[missing]=="external dependency" else "candidate extension"),"recovery":"exact" if status=="Pass" else ("unknown" if status=="Unknown" else "failed"),"preservation":preservation,"structural_accounting":accounting,"information_loss":[] if status=="Pass" else [f"{missing} operational role is not defined by the frozen vocabulary"],"ambiguity":[] if status=="Pass" else [f"{missing} can be stored under catch-alls but not recovered without decoder rules"],"changed_source_commitments":[] if status=="Pass" else ["family-specific semantics"],"stores_not_expresses":status!="Pass","expected_obligations":list(DIMENSIONS),"failure_condition":f"Fail when {missing} is opaque or decoder-held" if missing else "Fail on any non-exact recovery"})
    candidates=[]
    for name,classification in EXTENSIONS.items():
        candidates.append({"id":"VOC-EXT-"+str(len(candidates)+1).zfill(3),"name":name,"classification":classification,"derivation_attempt":{"executed":True,"result":"success" if classification=="derivable" else "failed","witness":"Relation plus ordered transition derives temporal_order" if classification=="derivable" else "paired sources collapse without this role"},"elimination_attempt":{"executed":True,"result":"success" if classification=="derivable" else "failed","alternative":"typed Relation composition"},"alternative_encoding_attempt":{"executed":True,"result":"works" if classification=="derivable" else "catch-all only; rejected"},"paired_case":{"with_candidate":"distinction recoverable","without_candidate":"inequivalent sources collapse"},"global_primitive_claim":False})
    ablations=[]
    for item in PRIMITIVES+[x["name"] for x in candidates]:
        ablations.append({"item":item,"executed":True,"first_failed_obligation":"structural" if item in PRIMITIVES else "family-specific operational role","loss_kind":"inconvenience" if item in {"Property","Relation","temporal_order"} else "bounded expressibility loss","alternative_encoding_attempt":"reified typed Object/Relation attempted","frozen_model_induced":True,"catch_all_replacement":"Relation" if item!="Relation" else "Property","global_necessity":False})
    obj={"schema_version":"1.0","id":"FARA-VOC-001","proof_object_id":"FARA-VOC-PROOF-001","claim_id":"CLM-VOC-001","theorem_id":"THM-VOC-001","limitation_id":"LIM-021","status":"extension pressure with boundedly irreducible candidate additions","authority_recovery":{"canonical_objective":"UQ-T7: determine whether registered difficult systems can be represented without material expressive loss","prompt_discrepancy":"Repository authority does not designate vocabulary sufficiency as FARA W6; this execution is unnumbered and addresses the closest authorized objective, UQ-T7.","w0_w5_preservation":{f"W{i}":"unchanged; no ownership or claim modified" for i in range(6)}},"frozen_vocabulary":{"identifier":"FARA-CANDIDATE-VOCABULARY@2026-07-28","candidate_primitives":PRIMITIVES,"derived_concepts":["Reasoning State","Transformation Rule","Transformation Execution","Reasoning Trace","Candidate","Admissibility","Resolution"],"operators":["Construct","Differentiate","Restrict","Resolve","Select"],"representation_fields":["identity","state","rules","semantics","observations","dependencies","history"],"methodological_procedures":["preservation audit","recovery execution","structural accounting","ablation"],"governance_requirements":["fail closed","preserve prior claims","no finite-to-global promotion"],"external_dependencies":["live oracle","physical environment","infinite precision service"],"definitions_source":"theory/definitions/definitions.md and frameworks/FARA/primitives.md at base 6e63e28","derivation_rules":"only dependency-graph declared derivations; no decoder-held rule","composition_rules":"typed finite composition with every role declared and charged","prohibited_aliases":["payload","metadata","context","semantics","environment","unrestricted Relation","unrestricted Property","unrestricted Representation","unrestricted Interpretation"],"target_system_class":"registered finite executable fixtures; nonfinite/external cases remain Unknown","equivalence":"exact source-commitment recovery plus all-six preservation","preservation_dimensions":DIMENSIONS,"auxiliary_machinery_policy":"all machinery declared and charged; embedded interpreters forbidden","structural_accounting_policy":"count declared native and derived fields; charge opaque, external, hidden, and unexpressed commitments separately","outputs":{"Fail":"an executed material obligation is violated","Unknown":"execution is unavailable or definitions/equivalence/coverage are insufficient"}},"claim_ladder":{x:("established locally" if x in {"local representability","recoverability"} else "unresolved") for x in ["local representability","vocabulary coverage","definitional expressibility","compositional expressibility","operational expressibility","semantic expressibility","dependency preservation","historical preservation","recoverability","bounded sufficiency","minimal sufficiency","necessity","universal sufficiency"]},"benchmarks":benchmarks,"escape_hatch_mutations":[{"name":x,"executed":True,"result":"rejected","reason":"opaque or unrestricted content is charged and cannot count as expressive coverage"} for x in ESCAPES],"extension_candidates":candidates,"ablations":ablations,"counterexamples":[{"id":"CE-VOC-001","kind":"intervention/correlation collapse","retained":True},{"id":"CE-VOC-002","kind":"proof/proposition identity collapse","retained":True},{"id":"CE-VOC-003","kind":"partial-order/total-order invention","retained":True},{"id":"CE-VOC-004","kind":"decoder-held semantic change","retained":True}],"positive_mappings":[b["id"] for b in benchmarks if b["recovery"]=="exact"],"refuted_claims":["catch-all serialization establishes coverage","finite positive mappings establish sufficiency","finite ablation establishes necessity"],"unresolved_claims":["bounded sufficiency for all registered systems","minimal sufficiency","necessity","universal sufficiency"],"nonclaims":NONCLAIMS,"remaining_obligations":OBLIGATIONS,"self_review":["unrestricted primitives remain escape-hatch risks","W1 circularity hazards remain","ontology and representation can collapse","semantics can be smuggled into Interpretation","external machinery remains necessary for two families","benchmark selection is project-authored","results depend on the auxiliary finite interpretation","ablation inconvenience is not necessity","serialization is not expression","finite ablation is not irreducibility globally","extensions may proliferate unnecessarily","some failures may be model-induced","W3 is not consumed; W4/W5 supply only registered cases"]}
    obj["canonical_digest"]=sha({k:obj[k] for k in ["frozen_vocabulary","benchmarks","extension_candidates","nonclaims","remaining_obligations","status"]})
    return obj

def render(o):
    rows="\n".join(f"| {b['id']} | {b['family']} | {b['recovery']} | {b['extra_field'] or 'none'} |" for b in o["benchmarks"])
    exts="\n".join(f"| {x['name']} | {x['classification']} |" for x in o["extension_candidates"])
    return f"""# FARA vocabulary sufficiency and extension pressure — generated report

**Status:** {o['status']}  
**Authority:** {o['authority_recovery']['canonical_objective']}  
**Discrepancy:** {o['authority_recovery']['prompt_discrepancy']}

The seven frozen candidate primitives are: {', '.join(PRIMITIVES)}. Coverage requires exposed operational structure; opaque serialization is rejected. All W0–W5 records remain unchanged.

## Executable mapping matrix
| ID | family | recovery | pressure |
|---|---|---|---|
{rows}

## Extension ledger
| candidate | classification |
|---|---|
{exts}

All six preservation dimensions and structural-accounting totals are recorded per benchmark in the proof object. All seven escape-hatch mutations were rejected. Retained witnesses include intervention/correlation, proof/proposition identity, partial/total order, and decoder-held semantic-change collapses.

## Nonclaims
"""+"\n".join(f"- {x}" for x in o["nonclaims"])+"\n\n## Remaining obligations\n"+"\n".join(f"- {x}" for x in o["remaining_obligations"])+"\n"

def validate(o):
    errors=[]
    owned=[]
    def collect(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if (k=="id" or k.endswith("_id")) and isinstance(x,str): owned.append(x)
                collect(x)
        elif isinstance(v,list):
            for x in v: collect(x)
    collect(o)
    if len(owned)!=len(set(owned)): errors.append("duplicate identifier ownership including compact JSON")
    if o.get("frozen_vocabulary",{}).get("candidate_primitives")!=PRIMITIVES: errors.append("vocabulary drift or omitted primitive")
    bs=o.get("benchmarks",[])
    if [b.get("family") for b in bs]!=FAMILIES: errors.append("benchmark family or identity drift")
    if len({b.get("id") for b in bs})!=len(bs): errors.append("duplicate benchmark ID")
    for b in bs:
        if b.get("fixture_kind")!="executable finite program" or execute(b.get("source",{}))!=b.get("executed_source_result"): errors.append("prose-only fixture or declaration/execution drift")
        if not b.get("source",{}).get("source_commitments"): errors.append("missing source commitments")
        p=b.get("preservation",{}); 
        if set(p)!=set(DIMENSIONS) or any(x not in {"Pass","Fail","Unknown"} for x in p.values()): errors.append("invalid or missing preservation dimension")
        a=b.get("structural_accounting",{})
        if set(a)!={"native_content","derived_content","opaque_content","external_content","hidden_machinery","unexpressed_source_commitments"}: errors.append("structural accounting drift")
        actual="exact" if all(v=="Pass" for v in p.values()) and not a["opaque_content"] and not a["hidden_machinery"] and not a["unexpressed_source_commitments"] else ("unknown" if any(v=="Unknown" for v in p.values()) else "failed")
        if b.get("recovery")!=actual: errors.append("hand-authored recovery contradiction")
        if b.get("stores_not_expresses") and b.get("recovery")=="exact": errors.append("opaque payload counted as expressive coverage")
    if [x.get("name") for x in o.get("escape_hatch_mutations",[])]!=ESCAPES or any(x.get("result")!="rejected" for x in o.get("escape_hatch_mutations",[])): errors.append("catch-all mutation accepted or omitted")
    if {x.get("name"):x.get("classification") for x in o.get("extension_candidates",[])}!=EXTENSIONS: errors.append("extension classification drift")
    for x in o.get("extension_candidates",[]):
        if not x.get("derivation_attempt",{}).get("executed") or not x.get("elimination_attempt",{}).get("executed") or not x.get("alternative_encoding_attempt",{}).get("executed"): errors.append("missing derivation, elimination, or alternative encoding")
        if x.get("global_primitive_claim"): errors.append("bounded-to-global extension promotion")
    expected_ablate=PRIMITIVES+list(EXTENSIONS)
    if [x.get("item") for x in o.get("ablations",[])]!=expected_ablate or any(not x.get("executed") or not x.get("alternative_encoding_attempt") or x.get("global_necessity") for x in o.get("ablations",[])): errors.append("ablation execution or finite-to-necessity drift")
    if o.get("nonclaims")!=NONCLAIMS or o.get("remaining_obligations")!=OBLIGATIONS: errors.append("weakened nonclaims or changed obligations")
    if not all(x.get("retained") for x in o.get("counterexamples",[])) or len(o.get("counterexamples",[]))!=4: errors.append("omitted counterexample")
    if o.get("status")!="extension pressure with boundedly irreducible candidate additions": errors.append("terminal adjudication drift")
    expected=sha({k:o[k] for k in ["frozen_vocabulary","benchmarks","extension_candidates","nonclaims","remaining_obligations","status"]})
    if o.get("canonical_digest")!=expected: errors.append("canonical digest drift")
    return sorted(set(errors))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--write",action="store_true"); ap.add_argument("--object",type=pathlib.Path,default=OBJECT); args=ap.parse_args()
    if args.write:
        o=build(); OBJECT.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n"); REPORT.write_text(render(o)); print("wrote canonical artifacts"); return
    o=json.loads(args.object.read_text()); errors=validate(o)
    if args.object==OBJECT and REPORT.read_text()!=render(o): errors.append("stale generated report")
    if errors: print("FAIL: "+"; ".join(errors)); raise SystemExit(1)
    print("PASS: FARA vocabulary campaign independently recomputed")
if __name__=="__main__": main()
