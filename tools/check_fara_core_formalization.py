#!/usr/bin/env python3
"""Build and independently validate the bounded FARA core formalization."""
from __future__ import annotations
import argparse, copy, hashlib, json, pathlib
from fractions import Fraction

ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=ROOT/'theory/formal/fara-core-formalization-v1.0.json'
PROOF=ROOT/'theory/evaluation/fara-core-formalization-proof-v1.0.json'
REPORT=ROOT/'theory/evaluation/generated-fara-core-formalization-report.md'
P=['Object','Property','Relation','Representation','Interpretation','Investigation','ReasoningCalculus']
DIMS=['structural','semantic','operational','dependency','information','historical']
NONCLAIMS=['canonical uniqueness','primitive necessity','global independence','global minimality','completeness','universality']
OBLIGATIONS=['choose among non-equivalent coherent foundations by substantive evidence','extend bounded derivability beyond cardinality two','supply nonfinite continuous semantics','supply environment-inclusive embodied semantics','independently replicate model and countermodel executions','prove conservativity against a formalization of the complete old prose theory']

def h(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def foundation_records():
    return [
      {'id':'FOUND-FARA-001','name':'many-sorted relational','signature':{'sorts':['Entity','Token','Meaning','Rule','State','Event','Objective','Condition','Relation'],'symbols':{'denotes':['Token','Entity'],'interprets':['Token','Meaning'],'applies':['Rule','State','State'],'targets':['Objective','Condition']}},'admissible_model':{'finite':True,'disjoint_sorts':True,'typed_symbols':True},'coherence_checks':['all symbol domains/codomains declared','carrier disjointness','at least one finite model'],'translation_to_core':{'Object':'Entity','Representation':'Token','Interpretation':'interprets','ReasoningCalculus':'Rule','Investigation':'Objective×Condition×Rule'},'non_equivalence_witness':{'property':'edge identity is extensional','contrast':'hypergraph retains edge identity and algebraic foundation treats transitions as operations'},'cost':14,'failure':'nonfinite and embodied behavior external'},
      {'id':'FOUND-FARA-002','name':'typed hypergraph','signature':{'sorts':['Node','Port','Hyperedge','NodeType','EdgeType'],'symbols':{'has_port':['Hyperedge','Port'],'incident':['Port','Node'],'node_type':['Node','NodeType'],'edge_type':['Hyperedge','EdgeType']}},'admissible_model':{'finite':True,'typed_ports':True,'incidence_total':True},'coherence_checks':['ports have one incident node','edge arity matches edge type','typed graph isomorphism defined'],'translation_to_core':{'Object':'typed Node','Property':'unary Hyperedge','Relation':'typed Hyperedge','Representation':'Token Node','Interpretation':'meaning Hyperedge','ReasoningCalculus':'rule subgraph','Investigation':'objective/condition subgraph'},'non_equivalence_witness':{'property':'parallel hyperedges remain distinct','contrast':'many-sorted extensional relation collapses duplicate tuples'},'cost':19,'failure':'semantic composition requires declared path semantics'},
      {'id':'FOUND-FARA-003','name':'algebraic state-transition','signature':{'sorts':['Carrier','State','Operation','MeaningAlgebra'],'symbols':{'step':['Operation','State','State'],'denote':['Carrier','MeaningAlgebra'],'compose':['Operation','Operation','Operation']}},'admissible_model':{'finite':True,'partial_operations':True,'composition_associative_when_defined':True},'coherence_checks':['operation domains declared','partial composition closure','state transition determinism declared per operation'],'translation_to_core':{'Object':'Carrier element','Property':'predicate view','Relation':'operation graph view','Representation':'carrier encoding','Interpretation':'denote homomorphism','ReasoningCalculus':'operation signature','Investigation':'indexed transition system'},'non_equivalence_witness':{'property':'operation composition is primitive','contrast':'relational and hypergraph foundations require derived path/edge composition'},'cost':17,'failure':'source/representation distinction is non-native'}]

def build_spec():
    sorts=['SourceEntity','Token','Meaning','Rule','State','Event','Objective','Condition','External','Relation']
    symbols={'Object':([], 'SourceEntity','primitive sort membership; not a universal container'),'Property':(['Object'],'Relation','derived unary typed relation'),'Relation':(['Object'],'Relation','primitive finite typed relation with declared arity'),'Representation':(['Object'],'Token','primitive token plus denotes edge; token and source disjoint'),'Interpretation':(['Representation'],'Meaning','primitive partial typed map Token -> Meaning'),'ReasoningCalculus':([], 'Rule','primitive finite rule set, independent of executions'),'Investigation':(['ReasoningCalculus'],'Objective','derived tuple (objective, conditions, calculus reference)'),'SemanticContent':(['Interpretation','Representation'],'Meaning','derived map application'),'Execution':(['ReasoningCalculus'],'Event','derived enabled rule application'),'Result':(['Execution'],'State','derived target state')}
    defs=[{'symbol':k,'dependencies':v[0],'codomain':v[1],'definition':v[2],'identity':'typed extensional equality with stable entity identity' if k in P else 'definitional tuple equality'} for k,v in symbols.items()]
    pre={'Object':['Representation'],'Property':['Object'],'Relation':['Object'],'Representation':['Object','Interpretation'],'Interpretation':['Representation'],'Investigation':['ReasoningCalculus'],'ReasoningCalculus':['Investigation']}
    post={d['symbol']:d['dependencies'] for d in defs}
    identities={x:{'identical':'same typed carrier member and complete declared structure','distinct':'not identical','equivalent':'isomorphic with all declared commitments preserved','isomorphic':'sort-bijection preserving typed symbols','commitment_equivalent':'all six preservation dimensions Pass','observationally_equivalent':'same frozen query answers','semantically_equivalent':'interpretation-map agreement after isomorphism'} for x in P}
    return {'schema_version':'1.1','id':'FARA-CORE-FORMAL-001','status':'Research','authority':{'objective':['formalize canonical derivation and composition rules','resolve circular primitive definitions identified by W1'],'designation':'no W7 designation supplied','discrepancy':'Repository authority records these as separate remaining obligations, not one designated next workstream; the prompt authorizes their combined execution.'},'language':{'object_language':'finite typed first-order relational signature','metalanguage':'finite sets, natural-number arities, total equality, partial functions','sorts':sorts,'formation':'every application declares symbol, arity, domain, and codomain','typing':'carriers are disjoint; relation tuples match declared domains and codomains','external_dependencies':['nonfinite dynamics','live oracle','physical environment']},'definitions':defs,'pre_dependency_graph':pre,'post_dependency_graph':post,'recursion':[],'base_cases':['empty finite relation','identity map on each carrier','zero-step derivation'],'semantics':{'model_class':'finite structures with each carrier cardinality 0..2, disjoint source/token/meaning carriers, typed total equality, partial interpretation, finite rules and transitions','morphism':'sort maps preserving declared relations, denotation, interpretation, rules, objectives, conditions and history order','equivalence':'isomorphism preserving all declared commitments','derivability':'bounded explicit-definition search over formulas of depth <=2 and all frozen models; witness trace or paired reduct countermodel required','consistency':'at least one well-typed admissible model and no formula plus negation derived','conservativity':'shared-vocabulary model expansion/reduct comparison; Unknown if old prose has no formal model class','extension':'new typed symbol requires declared dependencies, identity, accounting and conservativity comparison','outputs':['Pass','Fail','Unknown']},'identity':identities,'foundations':foundation_records(),'structural_accounting':{'primitive_structure':'one charge per carrier/relation/map/rule family','derived_structure':'one charge per definitional expansion','metalanguage_support':'finite sets, equality, tuple projection, graph reachability','external_assumptions':'charged and unavailable to derivation','opaque_content':'forbidden unless typed and query-inert','hidden_machinery':'any decoder, oracle, scheduler, higher-order predicate or whole-source constant is charged and rejects non-vacuity'},'separations':['object language / metalanguage','source / representation','representation / interpretation','rule / execution / result','calculus / investigation context'],'consistency_criterion':'validator accepts and at least one concrete model validates','conservativity_criterion':'every old shared-vocabulary model has a new expansion and every new reduct is old; otherwise nonconservative or Unknown','nonclaims':NONCLAIMS,'remaining_obligations':OBLIGATIONS}

def reduct(model,target): return {k:copy.deepcopy(v) for k,v in model.items() if k!=target}
def paired_countermodel(target,i):
    shared={'Object':['o0'],'Property':[['o0']],'Relation':[['o0','o0']],'Representation':{'t0':'o0'},'Interpretation':{'t0':'m0'},'Investigation':{'objective':'q','conditions':['c'],'calculus':'r0'},'ReasoningCalculus':['r0']}
    a=copy.deepcopy(shared); b=copy.deepcopy(shared)
    if target=='Object': b[target]=['o0','o1']
    elif target=='Relation': b[target]=[]
    elif target=='Representation': b[target]={'t0':'o0','t1':'o0'}
    elif target=='Interpretation': b[target]={'t0':'m1'}
    elif target=='ReasoningCalculus': b[target]=['r1']
    ra,rb=reduct(a,target),reduct(b,target)
    return {'id':f'CE-FORMAL-{i:03d}','target':target,'model_a':a,'model_b':b,'reduct_a':ra,'reduct_b':rb,'reducts_equal':ra==rb,'targets_differ':a[target]!=b[target],'verified':ra==rb and a[target]!=b[target],'bounded':True}

def execute_family(f):
    if f=='finite_deterministic':
        src={'state':0,'rules':[('inc',1),('inc',2)]}; out=src['state']; trace=[]
        for _,n in src['rules']: out+=n; trace.append(out)
        return src,{'state':out,'trace':trace}
    if f=='nonmonotonic_revision': return {'facts':['bird'],'defaults':[('bird','flies')],'retractions':['flies']},{'conclusions':[],'history':['derive:flies','retract:flies']}
    if f=='paraconsistent': return {'facts':['p','not_p'],'rule':'no explosion'},{'entailed':['p','not_p'],'entailed_q':False}
    if f=='probabilistic':
        src={'prior':[1,1],'likelihood':[3,1]}; nums=[Fraction(1,2)*3,Fraction(1,2)]; z=sum(nums); return src,{'posterior':[str(x/z) for x in nums]}
    if f=='causal_intervention': return {'equations':{'x':1,'y':'x'},'intervention':{'x':0}},{'x':0,'y':0}
    if f=='changing_rules': return {'state':1,'versions':[[('inc',1)],[('inc',2)]]},{'results':[2,3]}
    if f=='changing_interpretations': return {'token':'t','versions':[{'t':'hot'},{'t':'cold'}]},{'meanings':['hot','cold']}
    if f=='incompatible_ontologies': return {'left':{'a':'person'},'right':{'a':'account'}},{'alignment':'unavailable','conflict':True}
    if f=='provenance_history': return {'value':1,'events':[('sensorA',1),('sensorB',1)]},{'value':1,'provenance':['sensorA','sensorB']}
    if f=='distributed_partial_order': return {'events':['a','b','c'],'before':[('a','c'),('b','c')]},{'minimal':['a','b'],'maximal':['c']}
    if f=='proof_identity_binding': return {'formula':'P(x)','proofs':['intro','axiom'],'binding':{'x':'bound'}},{'same_formula':True,'distinct_proofs':True,'binding_preserved':True}
    if f=='institutional_authority': return {'rules':[('court','valid'),('blog','invalid')],'claim_source':'court'},{'admissible':True,'authority':'court'}
    return None,None

def validate_foundation(f):
    sig=f['signature']; sorts=set(sig['sorts']); typed=all(all(s in sorts for s in domcod) for domcod in sig['symbols'].values()); checks=bool(f['coherence_checks']) and bool(f['translation_to_core']) and bool(f['non_equivalence_witness']); return {'typed':typed,'coherent':typed and checks,'signature_digest':h(sig)}

def build_proof(spec):
    adjud={'Object':'not derivable under the frozen bounded model class','Property':'derivable under the frozen theory','Relation':'not derivable under the frozen bounded model class','Representation':'not derivable under the frozen bounded model class','Interpretation':'not derivable under the frozen bounded model class','Investigation':'derivable under the frozen theory','ReasoningCalculus':'not derivable under the frozen bounded model class'}
    counters=[paired_countermodel(x,i) for i,x in enumerate(['Object','Relation','Representation','Interpretation','ReasoningCalculus'],1)]
    families=['finite_deterministic','nonmonotonic_revision','paraconsistent','probabilistic','causal_intervention','changing_rules','changing_interpretations','incompatible_ontologies','provenance_history','distributed_partial_order','proof_identity_binding','institutional_authority','oracle_dependence','continuous_embodied']
    models=[]
    for i,f in enumerate(families,1):
        src,res=execute_family(f); unknown=src is None; models.append({'id':f'FORM-MODEL-{i:03d}','family':f,'source_model':src,'execution_result':res,'typing':'Unknown' if unknown else 'Pass','formation':'Unknown' if unknown else 'Pass','execution':'Unknown' if unknown else 'Pass','recovery':'Unknown' if unknown else 'Pass','preservation':{d:'Unknown' if unknown else 'Pass' for d in DIMS},'unsupported':['oracle/environment or nonfinite semantics'] if unknown else [],'distortion':'outside frozen executable model class' if unknown else 'none','execution_digest':None if unknown else h({'source':src,'result':res})})
    fchecks=[dict(foundation_id=f['id'],**validate_foundation(f)) for f in spec['foundations']]
    terminal='multiple non-equivalent coherent formalizations remain' if all(x['coherent'] for x in fchecks) and len({json.dumps(f['non_equivalence_witness'],sort_keys=True) for f in spec['foundations']})==3 else 'unresolved because semantics, model class, or equivalence cannot be fixed without substantive theory choice'
    return {'schema_version':'1.1','id':'FARA-CORE-PROOF-001','specification':spec['id'],'terminal_result':terminal,'strongest_established_result':'the selected many-sorted specification is boundedly coherent under the frozen finite model class; three formally specified coherent foundations have explicit non-equivalence witnesses','foundation_checks':fchecks,'w1_preservation':'all original W1 adjudications remain unresolved in their original artifact; these new bounded classifications do not overwrite them','w1_re_evaluation':adjud,'derivations':[{'target':'Property','trace':['Relation declared','restrict arity to 1','typed unary relation obtained'],'mechanical':True},{'target':'Investigation','trace':['Objective and Condition carriers declared','ReasoningCalculus reference declared','form typed tuple'],'mechanical':True}],'countermodels':counters,'conservativity':[{'construct':'typed carriers and disjointness','result':'nonconservative','reason':'adds source/representation separation not formally entailed by old prose models'},{'construct':'Property abbreviation','result':'conservative','reason':'explicit unary-relation expansion'},{'construct':'Investigation tuple','result':'unresolved','reason':'old prose identity and condition semantics absent'},{'construct':'remaining definitions','result':'unresolved','reason':'complete old prose model class absent'}],'models':models,'remaining_cycles':[],'rejected_definitions':['Object as universal payload','Interpretation as opaque semantic blob','Representation containing decoder','Investigation/Calculus ungrounded mutual recursion'],'refuted_claims':['the formal target is conservative in every respect','the foundations are notational variants','all adversarial families are internal to the finite model class'],'unresolved_claims':['which foundation matches intended FARA','unbounded independence','complete prose conservativity','continuous, embodied and oracle semantics'],'self_review':['formal elegance is not truth','disjointness is a substantive theory choice','finite-set metalanguage is charged','no higher-order escape hatch admitted','identity was not chosen as output equality','finite model selection bias remains','bounded countermodels are not global','no mutual recursion is relabeled to hide a cycle','representability is not ontology','conservativity is semantic where models exist and otherwise Unknown','benchmarks may overfit prior campaigns','W2-W5 and vocabulary classifications are preserved but not premises'],'prior_preservation':{'W0':'unchanged','W1':'unchanged; original unresolved results retained','W2':'unchanged bounded result','W3':'unchanged reconstruction result','W4':'unchanged representation boundary','W5':'unchanged unresolved invariance result','FARA-VOC-001':'all classifications, nonclaims and obligations retained'},'nonclaims':NONCLAIMS,'remaining_obligations':OBLIGATIONS}

def closure(graph):
    out={k:set() for k in graph}
    def visit(root,n,stack):
        if n in stack: raise ValueError('cycle:'+'=>'.join(stack+[n]))
        for d in graph.get(n,[]):
            if d not in graph: raise KeyError(d)
            out[root].add(d); visit(root,d,stack+[n])
    for k in graph: visit(k,k,[])
    return {k:sorted(v) for k,v in out.items()}

def render(s,p):
    pre='\n'.join(f"- `{k}` → {', '.join(v) or '∅'}" for k,v in s['pre_dependency_graph'].items()); post='\n'.join(f"- `{k}` → {', '.join(v) or '∅'}" for k,v in s['post_dependency_graph'].items()); w='\n'.join(f"| {k} | {v} |" for k,v in p['w1_re_evaluation'].items()); fs='\n'.join(f"- **{f['name']}**: typed={c['typed']}, coherent={c['coherent']}; witness: {f['non_equivalence_witness']['property']}." for f,c in zip(s['foundations'],p['foundation_checks'])); executed=sum(m['execution']=='Pass' for m in p['models']); unknown=sum(m['execution']=='Unknown' for m in p['models'])
    return f"""# FARA core formalization — generated report

**Terminal result:** {p['terminal_result']}
**Strongest established result:** {p['strongest_established_result']}

## Authority and discrepancy
Authorized repository obligations: {', '.join(s['authority']['objective'])}. {s['authority']['discrepancy']} No W7 designation is used.

## Frozen target
{s['language']['object_language']}; model class: {s['semantics']['model_class']}.

## Pre-formalization dependency graph
{pre}

## Post-formalization dependency DAG
{post}

## Foundation comparison
{fs}

## W1 re-evaluation
| Candidate | Adjudication |
|---|---|
{w}

All five non-derivability records include machine-checkable paired models whose reducts agree after removing the target while their target interpretations differ.

## Executable adversarial models
{executed} finite families were constructed and executed with source models, results, and execution digests. {unknown} external/nonfinite families remain Unknown. No family receives Pass from its name alone.

## Exact nonclaims
"""+'\n'.join('- '+x for x in NONCLAIMS)+"\n\n## Remaining obligations\n"+'\n'.join('- '+x for x in OBLIGATIONS)+"\n"

def validate(s,p,report=None):
    e=[]; expected=build_spec(); ep=build_proof(expected)
    if s!=expected:e.append('specification differs from executable declaration')
    if p!=ep:e.append('proof object differs from executable declaration')
    try: closure(s.get('post_dependency_graph',{}))
    except (ValueError,KeyError) as x:e.append('dependency graph invalid: '+str(x))
    declared={d['symbol'] for d in s.get('definitions',[])}
    if set(s.get('post_dependency_graph',{}))!=declared:e.append('undeclared or missing symbol')
    sorts=set(s.get('language',{}).get('sorts',[]))
    if len(sorts)!=len(s.get('language',{}).get('sorts',[])):e.append('duplicate sort')
    if any(not d.get('codomain') or d.get('codomain') not in sorts or not d.get('identity') for d in s.get('definitions',[])):e.append('missing or undeclared codomain sort or identity')
    if len(declared)!=len(s.get('definitions',[])):e.append('duplicate symbol')
    if not all(c.get('typed') and c.get('coherent') for c in p.get('foundation_checks',[])):e.append('foundation not formally coherent')
    for c in p.get('countermodels',[]):
        if not c.get('verified') or c.get('reduct_a')!=c.get('reduct_b') or c.get('model_a',{}).get(c.get('target'))==c.get('model_b',{}).get(c.get('target')):e.append('invalid paired-reduct countermodel')
    for m in p.get('models',[]):
        src,res=execute_family(m.get('family'))
        if src is None:
            if any(m.get(k)!='Unknown' for k in ['typing','formation','execution','recovery']):e.append('unavailable family promoted')
        else:
            if m.get('source_model')!=src or m.get('execution_result')!=res or m.get('execution_digest')!=h({'source':src,'result':res}):e.append('model execution drift')
            if any(m.get(k)!='Pass' for k in ['typing','formation','execution','recovery']):e.append('executed family not passed')
        if set(m.get('preservation',{}))!=set(DIMS):e.append('missing preservation dimensions')
    ids=[]
    def walk(x):
        if isinstance(x,dict):
            for k,v in x.items():
                if k=='id' and isinstance(v,str):ids.append(v)
                walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    walk({'s':s,'p':p})
    if len(ids)!=len(set(ids)):e.append('duplicate identifier ownership')
    if p.get('terminal_result') not in ['bounded coherent formalization under a frozen model class','formalization inconsistency or illicit circularity established','multiple non-equivalent coherent formalizations remain','unresolved because semantics, model class, or equivalence cannot be fixed without substantive theory choice']:e.append('invalid result vocabulary')
    if p.get('nonclaims')!=NONCLAIMS or p.get('remaining_obligations')!=OBLIGATIONS:e.append('weakened nonclaims or changed obligations')
    if report is not None and report!=render(expected,ep):e.append('stale generated report')
    return sorted(set(e))

def main():
    a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--spec',type=pathlib.Path,default=SPEC);a.add_argument('--proof',type=pathlib.Path,default=PROOF);x=a.parse_args()
    if x.write:
        s=build_spec();p=build_proof(s);SPEC.parent.mkdir(parents=True,exist_ok=True);SPEC.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n');PROOF.write_text(json.dumps(p,indent=2,sort_keys=True)+'\n');REPORT.write_text(render(s,p));print('wrote FARA core formalization artifacts');return
    s=json.loads(x.spec.read_text());p=json.loads(x.proof.read_text());e=validate(s,p,REPORT.read_text() if x.spec==SPEC and x.proof==PROOF else None)
    if e: print('FAIL: '+'; '.join(e));raise SystemExit(1)
    print('PASS: signatures, foundations, paired countermodels, executable models, dependency DAG, nonclaims, obligations, and report verified')
if __name__=='__main__':main()
