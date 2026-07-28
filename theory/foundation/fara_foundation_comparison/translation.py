"""Concrete source fixtures and candidate-specific translations."""
from __future__ import annotations
import copy
from fractions import Fraction

FOUNDATIONS=("many-sorted-relational","typed-hypergraph","algebraic-state-transition")
DIMENSIONS=("structural","semantic","operational","dependency","information","historical")

def ins(i,op,**a): return {"id":i,"opcode":op,"arguments":a}

def _fixture(i):
    if i=="BFC-001": return ({"states":["s0"]},[ins("r2","transition",source="s1",target="s2"),ins("r1","transition",source="s0",target="s1")],{"transition_meaning":"reachable-state closure"},[["r1","r2"]],{"initial_state":"s0"},[{"id":"h1","after":None},{"id":"h2","after":"h1"}])
    if i=="BFC-002": return ({},[ins("bayes-1","bayes",prior={"H":[1,1],"notH":[1,1]},likelihood={"H":[3,1],"notH":[1,1]})],{"normalization":"exact rational"},[["prior","posterior"],["likelihood","posterior"]],{"hypotheses":["H","notH"]},[{"id":"observation-1","after":None}])
    if i=="BFC-003": return ({"facts":["bird"]},[ins("d1","derive",premise="bird",conclusion="flies"),ins("x1","retract",proposition="flies")],{"policy":"later explicit retraction defeats default"},[["bird","flies"]],{"defaults":[["bird","flies"]]},[{"id":"derive-flies","after":None},{"id":"retract-flies","after":"derive-flies"}])
    if i=="BFC-004": return ({"facts":[]},[ins("a1","assert",proposition="p"),ins("a2","assert",proposition="not_p"),ins("q1","query",proposition="q",explosion=False)],{"consequence":"paraconsistent-no-explosion"},[],{"queried":"q"},[{"id":"assert-p","after":None},{"id":"assert-not-p","after":"assert-p"}])
    if i=="BFC-005": return ({"variables":{"x":1}},[ins("eq1","equation",target="y",source="x"),ins("do1","intervene",variable="x",value=0)],{"intervention":"surgical replacement"},[["x","y"]],{"observational_x":1,"interventional_x":0},[{"id":"equation-y-x","after":None},{"id":"do-x-0","after":"equation-y-x"}])
    if i=="BFC-006": return ({"value":1,"increment":1},[ins("apply-v1","increment"),ins("replace-v2","replace_increment",value=2),ins("apply-v2","increment")],{"rule_versions":["v1","v2"]},[["replace-v2","apply-v2"]],{"initial_increment":1},[{"id":"use-v1","after":None},{"id":"install-v2","after":"use-v1"},{"id":"use-v2","after":"install-v2"}])
    if i=="BFC-007": return ({"interpretations":{}},[ins("i1","interpret",token="t",meaning="hot"),ins("i2","interpret",token="t",meaning="cold")],{"token":"t","versions":["hot","cold"]},[["i1","i2"]],{"source_token":"t","meaning_carrier":["hot","cold"]},[{"id":"meaning-hot","after":None},{"id":"meaning-cold","after":"meaning-hot"}])
    if i=="BFC-008": return ({"classifications":[]},[ins("c1","classify",ontology="left",entity="a",category="person"),ins("c2","classify",ontology="right",entity="a",category="account")],{"alignment":"categories incompatible"},[["left:a","right:a"]],{"ontologies":["left","right"]},[{"id":"left-load","after":None},{"id":"right-load","after":None}])
    if i=="BFC-009": return ({"records":[]},[ins("m1","merge_preserve",records=[{"id":"e1","value":"x"},{"id":"e2","value":"x"}])],{"merge_policy":"preserve distinct identities"},[],{"shared_value":"x"},[{"id":"merge-e1","after":None},{"id":"merge-e2","after":None}])
    if i=="BFC-010": return ({"records":[{"id":"a","value":"x"},{"id":"b","value":"x"}]},[ins("q1","quotient",aliases=["a","b"],representative="a")],{"merge_policy":"explicit quotient"},[["b","a"]],{"equivalence_class":["a","b"]},[{"id":"identify-a-b","after":None}])
    if i=="BFC-011": return ({"constraints":["p","q"]},[ins("d1","delete_constraint",constraint="q")],{"relaxation":"explicit deletion"},[],{"original_constraints":["p","q"]},[{"id":"delete-q","after":None}])
    if i=="BFC-012": return ({"observations":[]},[ins("o1","observe",source="sensorA",value=1),ins("o2","observe",source="sensorB",value=1)],{"same_value_distinct_provenance":True},[["sensorA","value=1"],["sensorB","value=1"]],{"value":1},[{"id":"sensorA:1","after":None},{"id":"sensorB:1","after":None}])
    if i=="BFC-013": return ({"events":["a","b","c"]},[ins("p1","before",earlier="a",later="c"),ins("p2","before",earlier="b",later="c")],{"order":"partial-not-total"},[["a","c"],["b","c"]],{"concurrent":["a","b"]},[{"id":"a","after":None},{"id":"b","after":None},{"id":"c","after":["a","b"]}])
    if i=="BFC-014": return ({"proofs":[]},[ins("p1","prove",proof_id="proof-1",formula="T"),ins("p2","prove",proof_id="proof-2",formula="T")],{"same_formula_distinct_proofs":True},[],{"formula":"T"},[{"id":"proof-1","after":None},{"id":"proof-2","after":None}])
    if i=="BFC-015": return ({"bindings":{}},[ins("b1","bind",variable="x",scope="P(x)")],{"scope":"lexical"},[["x","P(x)"]],{"free_variables_before":["x"]},[{"id":"bind-x","after":None}])
    if i=="BFC-016": return ({"authorities":{"court":"valid","blog":"invalid"}},[ins("a1","authorize",source="court",claim="C")],{"authority_is_institutional":True},[["court","C"]],{"claim":"C"},[{"id":"court-authorizes-C","after":None}])
    return None

def _commitments(m):
    rules=copy.deepcopy(m["instructions"])
    return {"structural":{"instruction_ids":[x["id"] for x in rules],"opcodes":[x["opcode"] for x in rules],"identity_bearing_arguments":[copy.deepcopy(x["arguments"]) for x in rules if x["opcode"] in {"merge_preserve","observe","prove"}]},"semantic":copy.deepcopy(m["semantic"]),"operational":{"initial":copy.deepcopy(m["initial"]),"instructions":rules},"dependency":copy.deepcopy(m["dependencies"]),"information":copy.deepcopy(m["information"]),"historical":copy.deepcopy(m["history"])}

def source_model(b):
    f=_fixture(b["id"])
    if f is None: return {"id":b["id"],"name":b["name"],"external":list(b.get("external",[])),"unknown_reason":b.get("unknown_reason"),"initial":None,"instructions":[],"commitments":{d:None for d in DIMENSIONS}}
    initial,rules,semantic,deps,info,history=f
    m={"id":b["id"],"name":b["name"],"external":list(b.get("external",[])),"unknown_reason":b.get("unknown_reason"),"initial":initial,"instructions":rules,"semantic":semantic,"dependencies":deps,"information":info,"history":history}
    m["commitments"]=_commitments(m); return m

def _run(initial,rules):
    s=copy.deepcopy(initial); steps=[]; transitions=[x for x in rules if x["opcode"]=="transition"]
    if transitions:
        reachable=set(s.get("states",[])); changed=True
        while changed:
            changed=False
            for x in transitions:
                a=x["arguments"]
                if a["source"] in reachable and a["target"] not in reachable: reachable.add(a["target"]);steps.append(x["id"]);changed=True
        s["states"]=sorted(reachable)
    for x in rules:
        op,a=x["opcode"],x["arguments"]
        if op=="transition": continue
        if op=="bayes":
            n={k:Fraction(*a["prior"][k])*Fraction(*a["likelihood"][k]) for k in a["prior"]};z=sum(n.values(),Fraction(0,1));s["posterior"]={k:str(v/z) for k,v in sorted(n.items())}
        elif op=="derive":
            facts=set(s.setdefault("facts",[])); facts.add(a["conclusion"]) if a["premise"] in facts else None; s["facts"]=sorted(facts)
        elif op=="retract": s["facts"]=sorted(set(s.setdefault("facts",[]))-{a["proposition"]})
        elif op=="assert": s["facts"]=sorted(set(s.setdefault("facts",[]))|{a["proposition"]})
        elif op=="query": s["query"]={"proposition":a["proposition"],"entailed":a["proposition"] in set(s.setdefault("facts",[])),"explosion":a["explosion"]}
        elif op=="equation": s.setdefault("equations",{})[a["target"]]=a["source"];s.setdefault("variables",{})[a["target"]]=s["variables"][a["source"]]
        elif op=="intervene":
            s.setdefault("variables",{})[a["variable"]]=a["value"]
            for t,src in s.get("equations",{}).items(): s["variables"][t]=s["variables"][src]
        elif op=="increment": s["value"]+=s["increment"];s.setdefault("results",[]).append(s["value"])
        elif op=="replace_increment": s["increment"]=a["value"]
        elif op=="interpret": s.setdefault("interpretations",{})[a["token"]]=a["meaning"];s.setdefault("meaning_history",[]).append([a["token"],a["meaning"]])
        elif op=="classify": s.setdefault("classifications",[]).append([a["ontology"],a["entity"],a["category"]]);s["conflict"]=len({r[2] for r in s["classifications"] if r[1]==a["entity"]})>1
        elif op=="merge_preserve": s["records"]=copy.deepcopy(a["records"])
        elif op=="quotient": s["records"]=[r for r in s.get("records",[]) if r["id"]==a["representative"]];s["quotient"]={x:a["representative"] for x in a["aliases"]}
        elif op=="delete_constraint": s["constraints"]=[x for x in s.get("constraints",[]) if x!=a["constraint"]]
        elif op=="observe": s.setdefault("observations",[]).append({"source":a.get("source","quotiented"),"value":a["value"]})
        elif op=="before": s.setdefault("before",[]).append([a["earlier"],a["later"]]);ev=set(s.get("events",[]));ear={x for x,_ in s["before"]};late={y for _,y in s["before"]};s["minimal"]=sorted(ev-late);s["maximal"]=sorted(ev-ear)
        elif op=="prove": s.setdefault("proofs",[]).append({"id":a.get("proof_id",a["formula"]),"formula":a["formula"]})
        elif op=="bind": s.setdefault("bindings",{})[a["variable"]]=a["scope"]
        elif op=="authorize": s["authorization"]={"source":a["source"],"claim":a["claim"],"admissible":s.get("authorities",{}).get(a["source"])=="valid"}
        steps.append(x["id"])
    return {"status":"Pass","state":s,"steps":steps}

def execute_source(m): return {"status":"Unknown","reason":m["unknown_reason"]} if m["initial"] is None else _run(m["initial"],m["instructions"])

def _many(m):
    out=[];seen=set()
    for x in copy.deepcopy(m["instructions"]):
        if x["opcode"]=="merge_preserve": x["arguments"]["records"]=sorted({r["value"] if isinstance(r,dict) else r for r in x["arguments"]["records"]})
        elif x["opcode"]=="prove": x["arguments"]={"formula":x["arguments"]["formula"]}
        key=repr((x["opcode"],sorted(x["arguments"].items())))
        if key not in seen: out.append(x);seen.add(key)
    return {"candidate":FOUNDATIONS[0],"initial":copy.deepcopy(m["initial"]),"rules":out,"semantic_relations":copy.deepcopy(m["semantic"]),"dependency_relations":copy.deepcopy(m["dependencies"]),"information_relations":copy.deepcopy(m["information"]),"history_relations":copy.deepcopy(m["history"])}

def _graph(m):
    return {"candidate":FOUNDATIONS[1],"initial":copy.deepcopy(m["initial"]),"nodes":{x["id"]:"instruction" for x in m["instructions"]},"edges":[{"id":x["id"],"type":x["opcode"],"arguments":copy.deepcopy(x["arguments"])} for x in m["instructions"]],"semantic_nodes":copy.deepcopy(m["semantic"]),"dependency_edges":copy.deepcopy(m["dependencies"]),"information_nodes":copy.deepcopy(m["information"]),"history_edges":copy.deepcopy(m["history"])}

def _alg(m):
    ops={};program=[];seen=set()
    for x in copy.deepcopy(m["instructions"]):
        if x["opcode"]=="merge_preserve": x["arguments"]["records"]=sorted({r["value"] if isinstance(r,dict) else r for r in x["arguments"]["records"]})
        elif x["opcode"]=="observe": x["arguments"]={"value":x["arguments"]["value"]}
        elif x["opcode"]=="prove": x["arguments"]={"formula":x["arguments"]["formula"]}
        key=repr((x["opcode"],sorted(x["arguments"].items())))
        if key in seen: continue
        seen.add(key);ops[x["id"]]={"kind":x["opcode"],"arguments":x["arguments"]};program.append(x["id"])
    return {"candidate":FOUNDATIONS[2],"initial":copy.deepcopy(m["initial"]),"operations":ops,"program":program,"semantic_map":copy.deepcopy(m["semantic"]),"dependency_map":copy.deepcopy(m["dependencies"]),"information_map":copy.deepcopy(m["information"]),"history":[copy.deepcopy(r) for r in m["history"] if not str(r.get("id","")).startswith(("sensor","proof-"))]}

def translate_source(source,foundation,declared_elements=()):
    if foundation not in FOUNDATIONS: raise ValueError("undeclared foundation")
    target=None if source["initial"] is None else (_many(source) if foundation==FOUNDATIONS[0] else _graph(source) if foundation==FOUNDATIONS[1] else _alg(source))
    elements=list(declared_elements)+[x["id"] for x in source.get("instructions",[])];corr={x:f"{foundation}:{x}" for x in elements}
    return {"source_model":copy.deepcopy(source),"source_elements":elements,"generated_target_elements":sorted(corr.values()),"correspondence_map":corr,"target_model":target,"introduced_commitments":[],"external_assumptions":list(source["external"]),"opaque_content":[],"failure_or_unknown_reason":source["unknown_reason"]}

def translate(benchmark,foundation): return translate_source(source_model(benchmark),foundation,[x["id"] for x in benchmark.get("elements",[])])
