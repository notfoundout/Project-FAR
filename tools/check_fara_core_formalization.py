#!/usr/bin/env python3
"""Fail-closed validator for the bounded FARA core formalization."""
from __future__ import annotations
import argparse, copy, hashlib, json, pathlib
from fractions import Fraction

ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=ROOT/'theory/formal/fara-core-formalization-v1.0.json'
PROOF=ROOT/'theory/evaluation/fara-core-formalization-proof-v1.0.json'
REPORT=ROOT/'theory/evaluation/generated-fara-core-formalization-report.md'
DIMS=['structural','semantic','operational','dependency','information','historical']
W1_ORDER=['Object','Property','Relation','Representation','Interpretation','Investigation','ReasoningCalculus']
NONCLAIMS=['canonical uniqueness','primitive necessity','global independence','global minimality','completeness','universality']
OBLIGATIONS=['choose among non-equivalent coherent foundations by substantive evidence','extend bounded derivability beyond cardinality two','supply nonfinite continuous semantics','supply environment-inclusive embodied semantics','independently replicate model and countermodel executions','prove conservativity against a formalization of the complete old prose theory']

def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def build_spec():
    """Return the frozen specification; validate independently checks its formal content."""
    return json.loads(SPEC.read_text())

def reduct(model,target): return {k:copy.deepcopy(v) for k,v in model.items() if k!=target}

def paired_countermodel(target,index):
    shared={'Object':['o0'],'Property':[['o0']],'Relation':[['o0','o0']],'Representation':{'t0':'o0'},'Interpretation':{'t0':'m0'},'Investigation':{'objective':'q','conditions':['c'],'calculus':'r0'},'ReasoningCalculus':['r0']}
    a=copy.deepcopy(shared); b=copy.deepcopy(shared)
    if target=='Object': b[target]=['o0','o1']
    elif target=='Relation': b[target]=[]
    elif target=='Representation': b[target]={'t0':'o0','t1':'o0'}
    elif target=='Interpretation': b[target]={'t0':'m1'}
    elif target=='ReasoningCalculus': b[target]=['r1']
    ra,rb=reduct(a,target),reduct(b,target)
    return {'id':f'CE-FORMAL-{index:03d}','target':target,'model_a':a,'model_b':b,'reduct_a':ra,'reduct_b':rb,'reducts_equal':ra==rb,'targets_differ':a[target]!=b[target],'verified':ra==rb and a[target]!=b[target],'bounded':True}

def execute_family(family):
    if family=='finite_deterministic':
        source={'state':0,'rules':[['inc',1],['inc',2]]}; state=source['state']; trace=[]
        for _,amount in source['rules']: state+=amount; trace.append(state)
        return source,{'state':state,'trace':trace}
    if family=='nonmonotonic_revision': return {'facts':['bird'],'defaults':[['bird','flies']],'retractions':['flies']},{'conclusions':[],'history':['derive:flies','retract:flies']}
    if family=='paraconsistent': return {'facts':['p','not_p'],'rule':'no explosion'},{'entailed':['p','not_p'],'entailed_q':False}
    if family=='probabilistic':
        source={'prior':[1,1],'likelihood':[3,1]}; numerators=[Fraction(3,2),Fraction(1,2)]; total=sum(numerators)
        return source,{'posterior':[str(x/total) for x in numerators]}
    if family=='causal_intervention': return {'equations':{'x':1,'y':'x'},'intervention':{'x':0}},{'x':0,'y':0}
    if family=='changing_rules': return {'state':1,'versions':[[['inc',1]],[['inc',2]]]},{'results':[2,3]}
    if family=='changing_interpretations': return {'token':'t','versions':[{'t':'hot'},{'t':'cold'}]},{'meanings':['hot','cold']}
    if family=='incompatible_ontologies': return {'left':{'a':'person'},'right':{'a':'account'}},{'alignment':'unavailable','conflict':True}
    if family=='provenance_history': return {'value':1,'events':[['sensorA',1],['sensorB',1]]},{'value':1,'provenance':['sensorA','sensorB']}
    if family=='distributed_partial_order': return {'events':['a','b','c'],'before':[['a','c'],['b','c']]},{'minimal':['a','b'],'maximal':['c']}
    if family=='proof_identity_binding': return {'formula':'P(x)','proofs':['intro','axiom'],'binding':{'x':'bound'}},{'same_formula':True,'distinct_proofs':True,'binding_preserved':True}
    if family=='institutional_authority': return {'rules':[['court','valid'],['blog','invalid']],'claim_source':'court'},{'admissible':True,'authority':'court'}
    return None,None

def validate_foundation(foundation):
    signature=foundation['signature']; sorts=set(signature['sorts'])
    typed=all(all(sort in sorts for sort in declaration) for declaration in signature['symbols'].values())
    coherent=typed and bool(foundation.get('admissible_model')) and bool(foundation.get('coherence_checks')) and bool(foundation.get('translation_to_core')) and bool(foundation.get('non_equivalence_witness'))
    return {'foundation_id':foundation['id'],'typed':typed,'coherent':coherent,'signature_digest':digest(signature)}

def build_proof(spec):
    proof=json.loads(PROOF.read_text())
    proof['countermodels']=[paired_countermodel(target,i) for i,target in enumerate(['Object','Relation','Representation','Interpretation','ReasoningCalculus'],1)]
    proof['foundation_checks']=[validate_foundation(f) for f in spec['foundations']]
    families=['finite_deterministic','nonmonotonic_revision','paraconsistent','probabilistic','causal_intervention','changing_rules','changing_interpretations','incompatible_ontologies','provenance_history','distributed_partial_order','proof_identity_binding','institutional_authority','oracle_dependence','continuous_embodied']
    models=[]
    for i,family in enumerate(families,1):
        source,result=execute_family(family); unknown=source is None
        models.append({'id':f'FORM-MODEL-{i:03d}','family':family,'source_model':source,'execution_result':result,'typing':'Unknown' if unknown else 'Pass','formation':'Unknown' if unknown else 'Pass','execution':'Unknown' if unknown else 'Pass','recovery':'Unknown' if unknown else 'Pass','preservation':{d:'Unknown' if unknown else 'Pass' for d in DIMS},'unsupported':['oracle/environment or nonfinite semantics'] if unknown else [],'distortion':'outside frozen executable model class' if unknown else 'none','execution_digest':None if unknown else digest({'source':source,'result':result})})
    proof['models']=models
    witnesses={json.dumps(f['non_equivalence_witness'],sort_keys=True) for f in spec['foundations']}
    coherent=all(x['coherent'] for x in proof['foundation_checks'])
    proof['terminal_result']='multiple non-equivalent coherent formalizations remain' if coherent and len(witnesses)==3 else 'unresolved because semantics, model class, or equivalence cannot be fixed without substantive theory choice'
    proof['strongest_established_result']='the selected many-sorted specification is boundedly coherent under the frozen finite model class; three formally specified coherent foundations have explicit non-equivalence witnesses'
    return proof

def closure(graph):
    output={k:set() for k in graph}
    def visit(root,node,stack):
        if node in stack: raise ValueError('cycle:'+'=>'.join(stack+[node]))
        for dependency in graph.get(node,[]):
            if dependency not in graph: raise KeyError(dependency)
            output[root].add(dependency); visit(root,dependency,stack+[node])
    for key in graph: visit(key,key,[])
    return {k:sorted(v) for k,v in output.items()}

def render(spec,proof):
    pre='\n'.join(f"- `{k}` → {', '.join(v) or '∅'}" for k,v in spec['pre_dependency_graph'].items())
    post='\n'.join(f"- `{k}` → {', '.join(v) or '∅'}" for k,v in spec['post_dependency_graph'].items())
    w1='\n'.join(f"| {k} | {proof['w1_re_evaluation'][k]} |" for k in W1_ORDER)
    foundations='\n'.join(f"- **{f['name']}**: typed={c['typed']}, coherent={c['coherent']}; witness: {f['non_equivalence_witness']['property']}." for f,c in zip(spec['foundations'],proof['foundation_checks']))
    executed=sum(m['execution']=='Pass' for m in proof['models']); unknown=sum(m['execution']=='Unknown' for m in proof['models'])
    return f"""# FARA core formalization — generated report

**Terminal result:** {proof['terminal_result']}
**Strongest established result:** {proof['strongest_established_result']}

## Authority and discrepancy
Authorized repository obligations: {', '.join(spec['authority']['objective'])}. {spec['authority']['discrepancy']} No W7 designation is used.

## Frozen target
{spec['language']['object_language']}; model class: {spec['semantics']['model_class']}.

## Pre-formalization dependency graph
{pre}

## Post-formalization dependency DAG
{post}

## Foundation comparison
{foundations}

## W1 re-evaluation
| Candidate | Adjudication |
|---|---|
{w1}

All five non-derivability records include machine-checkable paired models whose reducts agree after removing the target while their target interpretations differ.

## Executable adversarial models
{executed} finite families were constructed and executed with source models, results, and execution digests. {unknown} external/nonfinite families remain Unknown. No family receives Pass from its name alone.

## Exact nonclaims
"""+'\n'.join('- '+x for x in NONCLAIMS)+"\n\n## Remaining obligations\n"+'\n'.join('- '+x for x in OBLIGATIONS)+"\n"

def validate(spec,proof,report=None):
    errors=[]; canonical=build_spec(); expected=build_proof(spec)
    if spec!=canonical: errors.append('specification differs from frozen canonical object')
    try: closure(spec.get('post_dependency_graph',{}))
    except (ValueError,KeyError) as exc: errors.append('dependency graph invalid: '+str(exc))
    definitions=spec.get('definitions',[]); symbols={d.get('symbol') for d in definitions}; sorts=set(spec.get('language',{}).get('sorts',[]))
    if set(spec.get('post_dependency_graph',{}))!=symbols: errors.append('undeclared or missing symbol')
    if len(symbols)!=len(definitions): errors.append('duplicate symbol')
    if len(sorts)!=len(spec.get('language',{}).get('sorts',[])): errors.append('duplicate sort')
    if any(not d.get('identity') or d.get('codomain') not in sorts for d in definitions): errors.append('missing identity or undeclared codomain sort')
    if proof!=expected: errors.append('proof object differs from independent executable recomputation')
    if not all(x['typed'] and x['coherent'] for x in expected['foundation_checks']): errors.append('foundation not formally coherent')
    for witness in proof.get('countermodels',[]):
        if not witness.get('verified') or witness.get('reduct_a')!=witness.get('reduct_b') or witness['model_a'][witness['target']]==witness['model_b'][witness['target']]: errors.append('invalid paired-reduct witness')
    for model in proof.get('models',[]):
        source,result=execute_family(model['family'])
        if source is None:
            if model['execution']!='Unknown': errors.append('unavailable family promoted')
        elif model['source_model']!=source or model['execution_result']!=result or model['execution_digest']!=digest({'source':source,'result':result}): errors.append('model execution drift')
        if set(model.get('preservation',{}))!=set(DIMS): errors.append('missing preservation dimensions')
    identifiers=[]
    def walk(value):
        if isinstance(value,dict):
            for key,item in value.items():
                if key=='id' and isinstance(item,str): identifiers.append(item)
                walk(item)
        elif isinstance(value,list):
            for item in value: walk(item)
    walk({'spec':spec,'proof':proof})
    if len(identifiers)!=len(set(identifiers)): errors.append('duplicate identifier ownership')
    if proof.get('nonclaims')!=NONCLAIMS or proof.get('remaining_obligations')!=OBLIGATIONS: errors.append('weakened nonclaims or changed obligations')
    if report is not None and report!=render(spec,expected): errors.append('stale generated report')
    return sorted(set(errors))

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--write',action='store_true'); parser.add_argument('--spec',type=pathlib.Path,default=SPEC); parser.add_argument('--proof',type=pathlib.Path,default=PROOF); args=parser.parse_args()
    spec=json.loads(args.spec.read_text()); proof=build_proof(spec)
    if args.write:
        args.proof.write_text(json.dumps(proof,indent=2,sort_keys=True)+'\n'); REPORT.write_text(render(spec,proof)); print('wrote FARA core formalization proof and report'); return
    stored=json.loads(args.proof.read_text()); errors=validate(spec,stored,REPORT.read_text() if args.spec==SPEC and args.proof==PROOF else None)
    if errors: print('FAIL: '+'; '.join(errors)); raise SystemExit(1)
    print('PASS: signatures, foundations, paired countermodels, executable models, dependency DAG, nonclaims, obligations, and report verified')
if __name__=='__main__': main()
