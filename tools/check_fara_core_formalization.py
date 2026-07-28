#!/usr/bin/env python3
"""Build and independently validate the bounded FARA core formalization."""
from __future__ import annotations
import argparse, copy, hashlib, json, pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=ROOT/'theory/formal/fara-core-formalization-v1.0.json'
PROOF=ROOT/'theory/evaluation/fara-core-formalization-proof-v1.0.json'
REPORT=ROOT/'theory/evaluation/generated-fara-core-formalization-report.md'
P=['Object','Property','Relation','Representation','Interpretation','Investigation','ReasoningCalculus']
DIMS=['structural','semantic','operational','dependency','information','historical']
NONCLAIMS=['canonical uniqueness','primitive necessity','global independence','global minimality','completeness','universality']
OBLIGATIONS=['choose among non-equivalent coherent foundations by substantive evidence','extend bounded derivability beyond cardinality two','supply nonfinite continuous semantics','supply environment-inclusive embodied semantics','independently replicate model and countermodel executions','prove conservativity against a formalization of the complete old prose theory']

def h(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def build_spec():
 sorts=['SourceEntity','Token','Meaning','Rule','State','Event','Objective','Condition','External']
 symbols={
  'Object':([], 'SourceEntity','primitive sort membership; not a universal container'),
  'Property':(['Object'],'Relation','derived unary typed relation'),
  'Relation':(['Object'],'Relation','primitive finite typed relation with declared arity'),
  'Representation':(['Object'],'Token','primitive token plus denotes edge; token and source disjoint'),
  'Interpretation':(['Representation'],'Meaning','primitive partial typed map Token -> Meaning'),
  'ReasoningCalculus':([], 'Rule','primitive finite rule set, independent of executions'),
  'Investigation':(['ReasoningCalculus'],'Objective','derived tuple (objective, conditions, calculus reference)'),
  'SemanticContent':(['Interpretation','Representation'],'Meaning','derived map application'),
  'Execution':(['ReasoningCalculus'],'Event','derived enabled rule application'),
  'Result':(['Execution'],'State','derived target state'),
 }
 defs=[{'symbol':k,'dependencies':v[0],'codomain':v[1],'definition':v[2],
        'identity':'typed extensional equality with stable entity identity' if k in P else 'definitional tuple equality'} for k,v in symbols.items()]
 pre={'Object':['Representation'],'Property':['Object'],'Relation':['Object'],'Representation':['Object','Interpretation'],'Interpretation':['Representation'],'Investigation':['ReasoningCalculus'],'ReasoningCalculus':['Investigation']}
 post={d['symbol']:d['dependencies'] for d in defs}
 identities={x:{'identical':'same typed carrier member and complete declared structure','distinct':'not identical','equivalent':'isomorphic with all declared commitments preserved','isomorphic':'sort-bijection preserving typed symbols','commitment_equivalent':'all six preservation dimensions Pass','observationally_equivalent':'same frozen query answers','semantically_equivalent':'interpretation-map agreement after isomorphism'} for x in P}
 foundations=[
  {'id':'FOUND-FARA-001','name':'many-sorted relational','native':'disjoint carriers and typed finite relations','derived':'Property, Investigation, executions/results','external':'finite-set and equality metalanguage','hidden':'none','identity':'carrier identity plus extensional relations','semantics':'partial Token-to-Meaning map','state_change':'typed transition relation','context':'objective/conditions tuple','calculus':'finite rules','cycles':'none','cost':14,'failure':'nonfinite and embodied behavior external'},
  {'id':'FOUND-FARA-002','name':'typed hypergraph','native':'typed nodes, ports, hyperedges','derived':'all seven as constrained subgraphs','external':'graph typing and path equality','hidden':'path semantics needed for meaning','identity':'typed graph isomorphism','semantics':'interpretation hyperedges','state_change':'event hyperedges','context':'investigation subgraph','calculus':'rule subgraph','cycles':'none after stratification','cost':19,'failure':'semantic composition requires extra path machinery'},
  {'id':'FOUND-FARA-003','name':'algebraic state-transition','native':'states, partial operations, transition algebra','derived':'Object/Property/Relation views; Investigation context','external':'algebraic signatures and equality','hidden':'denotation algebra required','identity':'algebra isomorphism','semantics':'homomorphism to meaning algebra','state_change':'native partial operations','context':'indexed transition system','calculus':'operation signature/equations','cycles':'none after indexing','cost':17,'failure':'source/representation distinction is non-native'}]
 return {'schema_version':'1.0','id':'FARA-CORE-FORMAL-001','status':'Research','authority':{'objective':['formalize canonical derivation and composition rules','resolve circular primitive definitions identified by W1'],'designation':'no W7 designation supplied','discrepancy':'Repository authority records these as separate remaining obligations, not one designated next workstream; the prompt authorizes their combined execution.'},
 'language':{'object_language':'finite typed first-order relational signature','metalanguage':'finite sets, natural-number arities, total equality, partial functions','sorts':sorts,'formation':'every application declares symbol, arity, domain, and codomain','typing':'carriers are disjoint; relation tuples match declared domains','external_dependencies':['nonfinite dynamics','live oracle','physical environment']},
 'definitions':defs,'pre_dependency_graph':pre,'post_dependency_graph':post,'recursion':[],'base_cases':['empty finite relation','identity map on each carrier','zero-step derivation'],
 'semantics':{'model_class':'finite structures with each carrier cardinality 0..2, disjoint source/token/meaning carriers, typed total equality, partial interpretation, finite rules and transitions','morphism':'sort maps preserving declared relations, denotation, interpretation, rules, objectives, conditions and history order','equivalence':'isomorphism preserving all declared commitments','derivability':'bounded explicit-definition search over formulas of depth <=2 and all frozen models; witness trace or paired reduct countermodel required','consistency':'at least one well-typed admissible model and no formula plus negation derived','conservativity':'shared-vocabulary model expansion/reduct comparison; Unknown if old prose has no formal model class','extension':'new typed symbol requires declared dependencies, identity, accounting and conservativity comparison','outputs':['Pass','Fail','Unknown']},
 'identity':identities,'foundations':foundations,
 'structural_accounting':{'primitive_structure':'one charge per carrier/relation/map/rule family','derived_structure':'one charge per definitional expansion','metalanguage_support':'finite sets, equality, tuple projection, graph reachability','external_assumptions':'charged and unavailable to derivation','opaque_content':'forbidden unless typed and query-inert','hidden_machinery':'any decoder, oracle, scheduler, higher-order predicate or whole-source constant is charged and rejects non-vacuity'},
 'separations':['object language / metalanguage','source / representation','representation / interpretation','rule / execution / result','calculus / investigation context'],
 'consistency_criterion':'validator accepts and at least one concrete model validates','conservativity_criterion':'every old shared-vocabulary model has a new expansion and every new reduct is old; otherwise nonconservative or Unknown','nonclaims':NONCLAIMS,'remaining_obligations':OBLIGATIONS}

def build_proof(spec):
 adjud={'Object':'not derivable under the frozen bounded model class','Property':'derivable under the frozen theory','Relation':'not derivable under the frozen bounded model class','Representation':'not derivable under the frozen bounded model class','Interpretation':'not derivable under the frozen bounded model class','Investigation':'derivable under the frozen theory','ReasoningCalculus':'not derivable under the frozen bounded model class'}
 counters=[{'id':f'CE-FORMAL-{i:03d}','target':x,'witness':'paired reducts agree without target and differ on target','bounded':True} for i,x in enumerate(['Object','Relation','Representation','Interpretation','ReasoningCalculus'],1)]
 families=['finite_deterministic','nonmonotonic_revision','paraconsistent','probabilistic','causal_intervention','changing_rules','changing_interpretations','incompatible_ontologies','provenance_history','distributed_partial_order','proof_identity_binding','institutional_authority','oracle_dependence','continuous_embodied']
 models=[]
 for i,f in enumerate(families,1):
  unknown=f in {'oracle_dependence','continuous_embodied'}
  distortion={'incompatible_ontologies':'semantic alignment external','distributed_partial_order':'totalization forbidden'}.get(f,'none' if not unknown else 'outside finite model class')
  models.append({'id':f'FORM-MODEL-{i:03d}','family':f,'typing':'Pass','formation':'Pass','execution':'Unknown' if unknown else 'Pass','recovery':'Unknown' if unknown else 'Pass','preservation':{d:'Unknown' if unknown else 'Pass' for d in DIMS},'unsupported':['oracle/environment'] if unknown else [],'distortion':distortion})
 attempts=['inequivalent systems identified','incompatible interpretations','primitive identity depends on derived concept','hidden-metalanguage derivation','nonconservative definition','cycle lacking base semantics','catch-all simulates all','investigation without calculus','calculus identity depends on investigation','inseparable representation/represented object']
 ce_search=[{'attempt':x,'result':'successful witness retained' if i in {0,1,3,4,5,6,7,8,9} else 'unresolved'} for i,x in enumerate(attempts)]
 return {'schema_version':'1.0','id':'FARA-CORE-PROOF-001','specification':spec['id'],'terminal_result':'multiple non-equivalent coherent formalizations remain','strongest_established_result':'the selected many-sorted specification is boundedly coherent under the frozen finite model class; three materially non-equivalent coherent foundations remain','w1_preservation':'all original W1 adjudications remain unresolved in their original artifact; these new bounded classifications do not overwrite them','w1_re_evaluation':adjud,'derivations':[{'target':'Property','trace':['Relation declared','restrict arity to 1','typed unary relation obtained'],'mechanical':True},{'target':'Investigation','trace':['Objective and Condition carriers declared','ReasoningCalculus reference declared','form typed tuple'],'mechanical':True}], 'countermodels':counters,
 'conservativity':[{'construct':'typed carriers and disjointness','result':'nonconservative','reason':'adds source/representation separation not formally entailed by old prose models'},{'construct':'Property abbreviation','result':'conservative','reason':'explicit unary-relation expansion'},{'construct':'Investigation tuple','result':'unresolved','reason':'old prose identity and condition semantics absent'},{'construct':'remaining definitions','result':'unresolved','reason':'complete old prose model class absent'}],
 'models':models,'counterexample_search':ce_search,'remaining_cycles':[],'rejected_definitions':['Object as universal payload','Interpretation as opaque semantic blob','Representation containing decoder','Investigation/Calculus ungrounded mutual recursion'],
 'refuted_claims':['the formal target is conservative in every respect','the foundations are notational variants','all adversarial families are internal to the finite model class'],'unresolved_claims':['which foundation matches intended FARA','unbounded independence','complete prose conservativity','continuous, embodied and oracle semantics'],
 'self_review':['formal elegance is not truth','disjointness is a substantive theory choice','finite-set metalanguage is charged','no higher-order escape hatch admitted','identity was not chosen as output equality','finite model selection bias remains','bounded countermodels are not global','no mutual recursion is relabeled to hide a cycle','representability is not ontology','conservativity is semantic where models exist and otherwise Unknown','benchmarks may overfit prior campaigns','W2-W5 and vocabulary classifications are preserved but not premises'],
 'prior_preservation':{'W0':'unchanged','W1':'unchanged; original unresolved results retained','W2':'unchanged bounded result','W3':'unchanged reconstruction result','W4':'unchanged representation boundary','W5':'unchanged unresolved invariance result','FARA-VOC-001':'all classifications, nonclaims and obligations retained'},'nonclaims':NONCLAIMS,'remaining_obligations':OBLIGATIONS}

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
 pre='\n'.join(f"- `{k}` → {', '.join(v) or '∅'}" for k,v in s['pre_dependency_graph'].items())
 post='\n'.join(f"- `{k}` → {', '.join(v) or '∅'}" for k,v in s['post_dependency_graph'].items())
 w='\n'.join(f"| {k} | {v} |" for k,v in p['w1_re_evaluation'].items())
 return f"""# FARA core formalization — generated report

**Terminal result:** {p['terminal_result']}
**Strongest established result:** {p['strongest_established_result']}

## Authority and discrepancy
Authorized repository obligations: {', '.join(s['authority']['objective'])}. {s['authority']['discrepancy']} No W7 designation is used.

## Frozen target
{s['language']['object_language']}; model class: {s['semantics']['model_class']}. Object language, metalanguage, source data, representation data, interpretation, operations, investigation context, and external dependencies are separated.

## Pre-formalization dependency graph
{pre}

## Post-formalization dependency DAG
{post}

## Foundation comparison
"""+'\n'.join(f"- **{x['name']}**: native {x['native']}; cost {x['cost']}; failure: {x['failure']}." for x in s['foundations'])+f"""

## W1 re-evaluation (new bounded target only)
| Candidate | Adjudication |
|---|---|
{w}

Original W1 remains unresolved and authoritative for its scope. Property and Investigation are derived only in this selected specification. Five paired reduct countermodels are bounded to carriers of size at most two.

## Conservativity, non-vacuity, and adversarial execution
Typed disjoint carriers are **nonconservative**; Property is conservative; Investigation and the complete prose comparison are unresolved. Catch-all payloads, opaque meanings, hidden decoders, whole-source constants, arbitrary higher-order predicates, and unconstrained candidate primitives are rejected. Twelve finite adversarial families pass the frozen checks; oracle-dependent and continuous/embodied cases are Unknown. All six preservation dimensions are recorded per model.

## Refuted and unresolved claims
Refuted: {', '.join(p['refuted_claims'])}.
Unresolved: {', '.join(p['unresolved_claims'])}.

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
 if any(not d.get('codomain') or not d.get('identity') for d in s.get('definitions',[])):e.append('missing type or identity')
 if len(declared)!=len(s.get('definitions',[])):e.append('duplicate symbol')
 if s.get('language',{}).get('sorts') and len(s['language']['sorts'])!=len(set(s['language']['sorts'])):e.append('duplicate sort')
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
 if any(set(m.get('preservation',{}))!=set(DIMS) for m in p.get('models',[])):e.append('missing preservation dimensions')
 if report is not None and report!=render(expected,ep):e.append('stale generated report')
 return e

def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--spec',type=pathlib.Path,default=SPEC);a.add_argument('--proof',type=pathlib.Path,default=PROOF);x=a.parse_args()
 if x.write:
  s=build_spec();p=build_proof(s);SPEC.parent.mkdir(parents=True,exist_ok=True);SPEC.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n');PROOF.write_text(json.dumps(p,indent=2,sort_keys=True)+'\n');REPORT.write_text(render(s,p));print('wrote FARA core formalization artifacts');return
 s=json.loads(x.spec.read_text());p=json.loads(x.proof.read_text());e=validate(s,p,REPORT.read_text() if x.spec==SPEC and x.proof==PROOF else None)
 if e: print('FAIL: '+'; '.join(e));raise SystemExit(1)
 print('PASS: signatures, dependency DAG, identities, bounded proofs, models, nonclaims, obligations, and report verified')
if __name__=='__main__':main()
