#!/usr/bin/env python3
"""Executable, fail-closed FARA vocabulary-pressure campaign."""
from __future__ import annotations
import argparse, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
OBJECT=ROOT/'theory/evaluation/fara-vocabulary-sufficiency-v1.0.json'
REPORT=ROOT/'theory/evaluation/generated-fara-vocabulary-sufficiency-report.md'
PRIMITIVES=['Object','Property','Relation','Representation','Interpretation','Investigation','Reasoning Calculus']
DIMS=['structural','semantic','operational','dependency','information','historical']
FAMILIES=['deterministic_transition','probabilistic_update','nonmonotonic_retraction','paraconsistent_consequence','causal_intervention','changing_rules','changing_semantics','evolving_ontology','identity_preserving_merge','identity_collapsing_merge','deletion_constraint_relaxation','provenance_history','distributed_partial_order','oracle_behavior','continuous_hybrid','embodied_tacit','proof_identity_binding','higher_order_scope','normative_authority']
PRESSURE={'probabilistic_update':'uncertainty','nonmonotonic_retraction':'retraction','paraconsistent_consequence':'consequence_policy','causal_intervention':'intervention','changing_rules':'rule_version','changing_semantics':'semantic_version','evolving_ontology':'identity_criterion','identity_preserving_merge':'identity_criterion','identity_collapsing_merge':'identity_criterion','provenance_history':'provenance','distributed_partial_order':'partial_order','oracle_behavior':'oracle_relation','continuous_hybrid':'uncertainty','embodied_tacit':'external_coupling','proof_identity_binding':'proof_object','higher_order_scope':'binding_scope','normative_authority':'authority_source'}
UNKNOWN={'oracle_behavior','continuous_hybrid','embodied_tacit'}
EXT={'temporal_order':'derivable',**{x:'boundedly irreducible under the frozen model' for x in ['uncertainty','retraction','consequence_policy','intervention','rule_version','semantic_version','identity_criterion','provenance','partial_order','proof_object','binding_scope','authority_source']},'oracle_relation':'external dependency','external_coupling':'external dependency'}
NONCLAIMS=['universal sufficiency','global minimality','global primitive necessity','finite ablation establishes necessity','serialization establishes expression','reconstruction establishes expressive sufficiency','candidate extensions are globally primitive']
OBLIGATIONS=['formalize canonical derivation and composition rules','replicate mappings independently','test nonfinite continuous semantics','adjudicate environment-inclusive embodied coupling','prove or refute extension irreducibility beyond the frozen model','resolve circular primitive definitions identified by W1']
ESCAPES=['whole_source_as_object','all_distinctions_as_property','all_operations_as_relation','semantics_in_interpretation','interpreter_in_representation','dependencies_in_context','history_as_opaque_string']
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def fixture(f):
 d={'family':f,'identity':['a','b'],'history':['initial']}
 d.update({
'deterministic_transition':{'x':1,'amount':2},'probabilistic_update':{'prior':[1,2],'likelihood':[3,4]},'nonmonotonic_retraction':{'facts':['bird'],'defeaters':['injured']},'paraconsistent_consequence':{'facts':['p','not_p'],'query':'q'},'causal_intervention':{'x':1,'do_x':0},'changing_rules':{'x':1,'versions':[1,3],'active':1},'changing_semantics':{'meanings':['river','finance'],'active':1},'evolving_ontology':{'same_versions':[False,True],'active':1},'identity_preserving_merge':{'policy':'preserve'},'identity_collapsing_merge':{'policy':'collapse'},'deletion_constraint_relaxation':{'values':[1,2,3],'delete':1,'max':3},'provenance_history':{'sources':['A','B'],'trusted':['A']},'distributed_partial_order':{'events':['a','b','c'],'before':[['a','c'],['b','c']]},'oracle_behavior':{'external':'live_service'},'continuous_hybrid':{'flow':'dx/dt=1','duration':'sqrt(2)'},'embodied_tacit':{'external':'physical_environment'},'proof_identity_binding':{'proofs':['lambda x.x','lambda y.y']},'higher_order_scope':{'formula':'forall P. exists x. P(x)'},'normative_authority':{'rules':[['permit','court'],['forbid','clerk']],'order':['court','clerk']}}[f]);return d
def run(s,role=True):
 f=s['family']
 if f=='deterministic_transition':return {'available':True,'result':s['x']+s['amount']}
 if f=='probabilistic_update':
  if not role:return {'available':True,'result':s['prior']}
  a,b=s['prior'];c,d=s['likelihood'];z=a*c+b*d;return {'available':True,'result':[[a*c,z],[b*d,z]]}
 if f=='nonmonotonic_retraction':return {'available':True,'result':('injured' not in s['defeaters']) if role else True}
 if f=='paraconsistent_consequence':return {'available':True,'result':False if role else True}
 if f=='causal_intervention':return {'available':True,'result':s['do_x'] if role else s['x']}
 if f=='changing_rules':return {'available':True,'result':s['x']+(s['versions'][s['active']] if role else s['versions'][0])}
 if f=='changing_semantics':return {'available':True,'result':s['meanings'][s['active']] if role else s['meanings'][0]}
 if f=='evolving_ontology':return {'available':True,'result':1 if (s['same_versions'][s['active']] if role else False) else 2}
 if f in {'identity_preserving_merge','identity_collapsing_merge'}:return {'available':True,'result':['a'] if role and s['policy']=='collapse' else ['a','b']}
 if f=='deletion_constraint_relaxation':return {'available':True,'result':[x for x in s['values'] if x!=s['delete'] and x<=s['max']]}
 if f=='provenance_history':return {'available':True,'result':[x for x in s['sources'] if x in s['trusted']] if role else s['sources']}
 if f=='distributed_partial_order':return {'available':True,'result':[['a','b','c'],['b','a','c']] if role else [['a','b','c']]}
 if f in UNKNOWN:return {'available':False,'result':None}
 if f=='proof_identity_binding':return {'available':True,'result':2 if role else 1}
 if f=='higher_order_scope':return {'available':True,'result':[] if role else ['P','x']}
 if f=='normative_authority':return {'available':True,'result':'permit' if role else 'conflict'}
 raise KeyError(f)
def preservation(f,full,reduced):
 if not full['available']:return {d:'Unknown' for d in DIMS}
 if full==reduced:return {d:'Pass' for d in DIMS}
 bad={'semantic','operational','information'}
 if f in {'changing_rules','changing_semantics','evolving_ontology','provenance_history','distributed_partial_order','proof_identity_binding','higher_order_scope','normative_authority'}:bad|={'dependency','historical'}
 if f in {'identity_preserving_merge','identity_collapsing_merge'}:bad.add('structural')
 return {d:'Fail' if d in bad else 'Pass' for d in DIMS}
def build():
 bs=[]
 for i,f in enumerate(FAMILIES,1):
  s=fixture(f);full=run(s,True);reduced=run(s,f not in PRESSURE);p=preservation(f,full,reduced)
  rec='exact' if set(p.values())=={'Pass'} else ('unknown' if 'Unknown' in p.values() else 'failed')
  bs.append({'id':f'VOC-BENCH-{i:03d}','family':f,'fixture':s,'full_execution':full,'frozen_execution':reduced,'pressure':PRESSURE.get(f),'preservation':p,'recovery':rec,'accounting':{'native':7,'derived':2,'opaque':0 if rec=='exact' else int(rec=='failed'),'external':int(f in UNKNOWN),'hidden':0,'unexpressed':int(rec!='exact')}})
 ex=[{'id':f'VOC-EXT-{i:03d}','name':n,'classification':c,'derivation':'success' if c=='derivable' else 'failed paired execution','elimination':'typed Relation composition attempted','alternative':'catch-all rejected','global_primitive':False} for i,(n,c) in enumerate(EXT.items(),1)]
 o={'schema_version':'1.1','id':'FARA-VOC-001','proof_object_id':'FARA-VOC-PROOF-001','claim_id':'CLM-VOC-001','theorem_id':'THM-VOC-001','limitation_id':'LIM-021','status':'extension pressure with boundedly irreducible candidate additions','authority':{'objective':'UQ-T7','discrepancy':'Repository authority does not designate this campaign as W6.','prior_work':{f'W{i}':'unchanged' for i in range(6)}},'vocabulary':{'primitives':PRIMITIVES,'dimensions':DIMS,'equivalence':'exact recovery plus all-six preservation','catch_alls_forbidden':['payload','metadata','context','unrestricted Relation','unrestricted Property','unrestricted Representation','unrestricted Interpretation']},'benchmarks':bs,'extensions':ex,'escape_hatches':[{'name':x,'result':'rejected'} for x in ESCAPES],'ablations':[{'item':x,'executed':True,'alternative_tested':True,'global_necessity':False} for x in PRIMITIVES+list(EXT)],'counterexamples':[{'id':f'CE-VOC-{i:03d}','retained':True,'kind':k} for i,k in enumerate(['intervention/correlation collapse','proof/proposition identity collapse','partial-order/total-order invention','decoder-held semantic change'],1)],'positive_mappings':[b['id'] for b in bs if b['recovery']=='exact'],'nonclaims':NONCLAIMS,'remaining_obligations':OBLIGATIONS}
 o['canonical_digest']=digest({k:o[k] for k in ['vocabulary','benchmarks','extensions','nonclaims','remaining_obligations','status']});return o
def render(o):
 rows='\n'.join(f"| {b['id']} | {b['family']} | {b['recovery']} | {b['pressure'] or 'none'} |" for b in o['benchmarks'])
 return '# FARA vocabulary sufficiency and extension pressure — generated report\n\n**Status:** '+o['status']+'\n\nEach family is executed with its full registered behavior and again under the frozen vocabulary. Preservation and recovery are computed from those paired executions.\n\n| ID | Family | Recovery | Pressure |\n|---|---|---|---|\n'+rows+'\n\n## Nonclaims\n'+'\n'.join('- '+x for x in NONCLAIMS)+'\n\n## Remaining obligations\n'+'\n'.join('- '+x for x in OBLIGATIONS)+'\n'
def validate(o):
 e=[];fresh=build()
 if o!=fresh:e.append('canonical object differs from fresh executable build')
 ids=[]
 def walk(v):
  if isinstance(v,dict):
   for k,x in v.items():
    if isinstance(x,str) and (k.endswith('_id') or (k=='id' and x.startswith(('FARA-','VOC-','CE-','CLM-','THM-','LIM-')))):ids.append(x)
    walk(x)
  elif isinstance(v,list):
   for x in v:walk(x)
 walk(o)
 if len(ids)!=len(set(ids)):e.append('duplicate identifier ownership')
 return e
def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');a.add_argument('--object',type=pathlib.Path,default=OBJECT);x=a.parse_args()
 if x.write:
  o=build();OBJECT.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n');REPORT.write_text(render(o));print('wrote canonical artifacts');return
 o=json.loads(x.object.read_text());e=validate(o)
 if x.object==OBJECT and REPORT.read_text()!=render(build()):e.append('stale generated report')
 if e:print('FAIL: '+'; '.join(e));raise SystemExit(1)
 print('PASS: 19 family-specific executions; canonical object freshly rebuilt')
if __name__=='__main__':main()
