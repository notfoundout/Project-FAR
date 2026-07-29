#!/usr/bin/env python3
"""Fail-closed expanded bounded FARA campaign validator."""
from __future__ import annotations
import argparse,copy,hashlib,importlib.util,itertools,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=ROOT/'theory/formal/fara-expanded-bounded-campaign-v1.0.json';PROOF=ROOT/'theory/evaluation/fara-expanded-bounded-campaign-proof-v1.0.json';REPORT=ROOT/'theory/evaluation/generated-fara-expanded-bounded-campaign-report.md';TRACE_DIR=ROOT/'artifacts/fara-expanded-bounded-campaign/traces'
UNKNOWN=('oracle','continuous','hybrid','embodied');FORBIDDEN=('universality','uniqueness','global superiority','global minimality','necessity','completeness','W7')
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def git_blob_sha(data):return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path)
 if s is None or s.loader is None:raise RuntimeError(f'cannot load {path}')
 m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def universe(carrier,arity):return tuple(itertools.product(carrier,repeat=arity))
def relation_from_mask(carrier,arity,mask):return tuple(t for i,t in enumerate(universe(carrier,arity)) if mask&(1<<i))
def mask_from_relation(carrier,arity,relation):
 pos={t:i for i,t in enumerate(universe(carrier,arity))};mask=0
 for t in relation:
  if t not in pos:raise ValueError('tuple outside carrier')
  mask|=1<<pos[t]
 return mask
def relation_errors(carrier,arity,relation):
 e=[]
 if arity not in (1,2):e.append('unsupported arity')
 if len(relation)!=len(set(relation)):e.append('duplicate tuple')
 for t in relation:
  if len(t)!=arity:e.append('wrong tuple arity')
  if any(x not in carrier for x in t):e.append('tuple outside carrier')
 return sorted(set(e))
def evaluate_relation(carrier,arity,relation):
 u=universe(carrier,arity);first=u[0] if u else None
 alt=tuple(t for t in relation if t!=first) if first in relation else tuple(sorted((*relation,first))) if first is not None else relation
 model_a={'carrier':carrier,'relation':relation};model_b={'carrier':carrier,'relation':alt}
 reduct_a={'carrier':model_a['carrier']};reduct_b={'carrier':model_b['carrier']}
 ok=first is not None and reduct_a==reduct_b and model_a['relation']!=model_b['relation']
 return {'tuple_count':len(relation),'complement_count':len(u)-len(relation),'contains_first_tuple':first in relation if first else False,'contains_last_tuple':u[-1] in relation if u else False,'diagonal_count':sum(a==b for a,b in relation) if arity==2 else None,'reduct_digest':digest(reduct_a),'alternate_relation_digest':digest(alt),'paired_reduct_verified':ok,'outcome':'paired-reduct-witness' if ok else 'no-distinct-relation-at-empty-carrier'}
def enumerate_axis(maximum,arity):
 rows=[];totals={'constructed':0,'admissible':0,'evaluated':0,'rejected':0,'paired_reduct_pass':0};ah=hashlib.sha256();rh=hashlib.sha256()
 for n in range(maximum+1):
  carrier=tuple(f'o{i}' for i in range(n));count=1<<(n**arity);eh=hashlib.sha256();sh=hashlib.sha256();c=a=v=r=p=0;out={'paired-reduct-witness':0,'no-distinct-relation-at-empty-carrier':0}
  for mask in range(count):
   rel=relation_from_mask(carrier,arity,mask);c+=1;errs=relation_errors(carrier,arity,rel)
   if errs:r+=1;rec={'carrier_size':n,'arity':arity,'mask':mask,'relation':rel,'errors':errs};eh.update(canonical(rec).encode());ah.update(canonical(rec).encode());continue
   if mask_from_relation(carrier,arity,rel)!=mask:raise ValueError('relation/mask mismatch')
   a+=1;res=evaluate_relation(carrier,arity,rel);v+=1;p+=int(res['paired_reduct_verified']);out[res['outcome']]+=1;exe={'carrier':carrier,'arity':arity,'mask':mask,'relation':rel};full={'execution':exe,'result':res};eh.update(canonical(exe).encode());sh.update(canonical(full).encode());ah.update(canonical(exe).encode());rh.update(canonical(full).encode())
  if c!=count or a+r!=c or v!=a:raise ValueError('incomplete relation execution')
  row={'carrier_size':n,'interpretations':count,'constructed':c,'admissible':a,'evaluated':v,'rejected':r,'paired_reduct_pass':p,'outcomes':out,'execution_digest':eh.hexdigest(),'result_digest':sh.hexdigest()};rows.append(row)
  for k,val in (('constructed',c),('admissible',a),('evaluated',v),('rejected',r),('paired_reduct_pass',p)):totals[k]+=val
 return {'arity':arity,'algorithm':'materialize-validate-evaluate-v3','per_size':rows,'interpretations_examined':totals['evaluated'],**totals,'execution_digest':ah.hexdigest(),'result_digest':rh.hexdigest()}
def base_model(n):return {'Object':[f'o{i}' for i in range(n)],'Property':[],'Relation':[],'Representation':{},'Interpretation':{},'Investigation':{'objective':'q','conditions':[],'calculus':'r0'},'ReasoningCalculus':['r0']}
def model_errors(m,maximum):
 e=[];required={'Object','Property','Relation','Representation','Interpretation','Investigation','ReasoningCalculus'}
 if set(m)!=required:return ['model schema mismatch']
 o=m['Object']
 if not isinstance(o,list) or len(o)!=len(set(o)):e.append('invalid Object carrier');o=[]
 if len(o)>maximum:e.append('Object carrier exceeds bound')
 if not isinstance(m['Property'],list):e.append('Property must be list')
 else:
  if len(m['Property'])!=len({tuple(t) for t in m['Property'] if isinstance(t,list)}):e.append('duplicate Property tuple')
  for t in m['Property']:
   if not isinstance(t,list) or len(t)!=1:e.append('Property tuple must be unary')
   elif t[0] not in o:e.append('Property outside Object')
 if not isinstance(m['Relation'],list):e.append('Relation must be list')
 else:
  if len(m['Relation'])!=len({tuple(t) for t in m['Relation'] if isinstance(t,list)}):e.append('duplicate Relation tuple')
  for t in m['Relation']:
   if not isinstance(t,list) or len(t)!=2:e.append('Relation tuple must be binary')
   elif any(x not in o for x in t):e.append('Relation outside Object')
 rep=m['Representation']
 if not isinstance(rep,dict):e.append('Representation must be mapping');rep={}
 elif any(v not in o for v in rep.values()):e.append('Representation outside Object')
 inter=m['Interpretation']
 if not isinstance(inter,dict):e.append('Interpretation must be mapping');inter={}
 elif not set(inter)<=set(rep):e.append('Interpretation token outside Representation')
 calc=m['ReasoningCalculus']
 if not isinstance(calc,list) or not calc or len(calc)!=len(set(calc)):e.append('invalid ReasoningCalculus');calc=[]
 inv=m['Investigation']
 if not isinstance(inv,dict) or set(inv)!={'objective','conditions','calculus'}:e.append('invalid Investigation')
 else:
  if inv['calculus'] not in calc:e.append('Investigation references absent calculus')
  if not isinstance(inv['conditions'],list):e.append('conditions must be list')
 return sorted(set(e))
def reduct(m,target):return {k:copy.deepcopy(v) for k,v in m.items() if k!=target}
def validate_countermodel(rec,maximum,metadata=True):
 e=[];target=rec.get('target');a=rec.get('model_a');b=rec.get('model_b');bound=rec.get('support_bound')
 if target not in {'Object','Property','Relation','Representation','Interpretation','Investigation','ReasoningCalculus'}:return ['unknown target']
 if not isinstance(a,dict) or not isinstance(b,dict):return ['missing model']
 if not isinstance(bound,int) or not 0<=bound<=maximum:e.append('invalid support bound');bound=maximum
 e += [f'model_a: {x}' for x in model_errors(a,maximum)]+[f'model_b: {x}' for x in model_errors(b,maximum)]
 sizes=[len(a.get('Object',[])),len(b.get('Object',[]))]
 if any(n>bound for n in sizes):e.append('actual carrier exceeds support bound')
 ra,rb=reduct(a,target),reduct(b,target)
 if ra!=rb:e.append('reducts differ')
 if a.get(target)==b.get(target):e.append('targets do not differ')
 if metadata:
  before=sorted(set(e));ok=not before
  if rec.get('actual_carrier_sizes')!=sizes:e.append('stored cardinality mismatch')
  if rec.get('reduct_a')!=ra or rec.get('reduct_b')!=rb:e.append('stored reduct mismatch')
  if rec.get('verified')!=ok:e.append('stored verified mismatch')
  if rec.get('validation_errors')!=before:e.append('stored validation errors mismatch')
 return sorted(set(e))
def countermodel(target,bound,maximum):
 if bound<0 or bound>maximum or (target in {'Object','Property','Relation','Representation','Interpretation'} and bound==0):return None
 if target=='Object':a,b=base_model(bound-1),base_model(bound)
 else:
  a=base_model(bound);b=copy.deepcopy(a)
  if target=='Property':b[target]=[['o0']]
  elif target=='Relation':b[target]=[['o0','o0']]
  elif target=='Representation':b[target]={'t0':'o0'}
  elif target=='Interpretation':a['Representation']=b['Representation']={'t0':'o0'};b[target]={'t0':'m0'}
  elif target=='Investigation':b[target]={'objective':'q2','conditions':[],'calculus':'r0'}
  elif target=='ReasoningCalculus':b[target]=['r0','r1']
  else:raise KeyError(target)
 rec={'target':target,'support_bound':bound,'actual_carrier_sizes':[len(a['Object']),len(b['Object'])],'model_a':a,'model_b':b,'reduct_a':reduct(a,target),'reduct_b':reduct(b,target)};errs=validate_countermodel(rec,maximum,False);rec['verified']=not errs;rec['validation_errors']=errs;return rec
def summarize_countermodel(r):return {'target':r['target'],'support_bound':r['support_bound'],'actual_carrier_sizes':r['actual_carrier_sizes'],'model_a_digest':digest(r['model_a']),'model_b_digest':digest(r['model_b']),'reduct_digest':digest(r['reduct_a']),'target_values_digest':digest([r['model_a'][r['target']],r['model_b'][r['target']]]),'verified':r['verified'],'validation_errors':r['validation_errors']}
def build_countermodels(spec):
 maximum=spec['bounds']['maximum_carrier_size'];records=[];coverage={}
 for target in spec['derivability_targets']:
  yes=[];no=[]
  for bound in range(spec['bounds']['minimum_carrier_size'],maximum+1):
   rec=countermodel(target,bound,maximum)
   if rec is None:no.append(bound)
   else:
    if validate_countermodel(rec,maximum):raise ValueError(f'invalid generated witness {target}@{bound}')
    records.append(rec);yes.append(bound)
  coverage[target]={'supported_bounds':yes,'unsupported_bounds':no}
 return records,coverage
def historical_errors(spec,root=ROOT):
 e=[]
 for rel,record in spec['historical_artifacts'].items():
  p=root/rel
  if not p.exists():e.append(f'historical artifact missing: {rel}')
  elif git_blob_sha(p.read_bytes())!=record['git_blob_sha']:e.append(f'historical artifact changed from immutable base: {rel}')
 return e
def upstream_state(spec,root=ROOT):
 e=[];core=load('expanded_core',root/'tools/check_fara_core_formalization.py');cs=json.loads(core.SPEC.read_text());cp=json.loads(core.PROOF.read_text());ce=core.validate(cs,cp,core.REPORT.read_text());e += [f'core rerun: {x}' for x in ce];fresh_core=core.build_proof(copy.deepcopy(cs));c={'terminal_result':fresh_core['terminal_result'],'model_families':len(fresh_core['models'])}
 foundation=load('expanded_foundation',root/'tools/check_fara_foundation_comparison.py');fs=json.loads(foundation.SPEC.read_text());fp=json.loads(foundation.PROOF.read_text());fe=foundation.validate(fs,fp,foundation.REPORT.read_text());e += [f'foundation rerun: {x}' for x in fe];f=foundation.build(copy.deepcopy(fs));totals={n:d['mapping_counts'] for n,d in sorted(f['structural_accounting'].items())};summary={'terminal_result':f['terminal_result'],'foundation_executions':len(f['traces']),'ablations':len(f['ablations']),'ablation_executions':sum(len(x['executions']) for x in f['ablations']),'round_trip_records':len(f['round_trip_ledger']),'dominance_edges':f['dominance_graph']['edges'],'mapping_totals':totals};manifest={k:{'digest':digest(v),'status':v['status'],'preservation':v['preservation'],'structural_accounting':v['structural_accounting']} for k,v in f['traces'].items()};return c,summary,manifest,e

def summarize_countermodels(records,coverage):
 summaries=[summarize_countermodel(r) for r in records];by_target=[]
 for target,bounds in coverage.items():
  rows=[r for r in summaries if r['target']==target];by_target.append({'target':target,'supported_bounds':bounds['supported_bounds'],'unsupported_bounds':bounds['unsupported_bounds'],'witness_count':len(rows),'model_count':2*len(rows),'evidence_digest':digest(rows)})
 return {'witness_count':len(records),'model_count':2*len(records),'evidence_digest':digest(summaries),'by_target':by_target}
def build(spec):
 axes=[enumerate_axis(spec['bounds']['maximum_carrier_size'],a) for a in spec['bounds']['exhaustive_relation_arities']];records,coverage=build_countermodels(spec);unknown={u:'Unknown' for u in UNKNOWN};up=spec['upstream_expectations']['foundation']
 return {'campaign_id':spec['id'],'spec_digest':digest(spec),'base_commit':spec['base_commit'],'bounds':spec['bounds'],'enumeration_axes':axes,'countermodel_evidence':summarize_countermodels(records,coverage),'countermodel_coverage':coverage,'cost_accounting':{'relation_interpretations_constructed_and_evaluated':sum(a['evaluated'] for a in axes),'paired_reduct_witnesses':len(records),'paired_reduct_models':2*len(records),'foundation_executions':up['foundation_executions'],'ablations':up['ablations'],'ablation_executions':up['ablation_executions'],'round_trip_records':up['round_trip_records']},'upstream_reruns':spec['upstream_expectations'],'historical_artifacts':copy.deepcopy(spec['historical_artifacts']),'conclusions':{'relation_axes':'every unary and binary relation interpretation on carriers 0..4 was materialized, type-checked, and evaluated independently; full-signature cross-products were not searched','derivability':'paired-reduct witnesses establish bounded non-derivability only at target-specific support bounds recorded in countermodel_coverage','foundation':up['terminal_result'],'external_cases':unknown},'unknown_cases':unknown,'nonclaims':spec['nonclaims']}
def render(spec,p):
 lines=['# Expanded bounded FARA executable campaign','','Status: Research','',f"Base: `{p['base_commit']}`. Maximum carrier size: **{p['bounds']['maximum_carrier_size']}**.",'','## Executed relation axes','']
 for axis in p['enumeration_axes']:
  lines.append(f"- arity {axis['arity']}: {axis['evaluated']} concrete interpretations constructed, admitted, and evaluated; rejected={axis['rejected']}; execution digest `{axis['execution_digest']}`; result digest `{axis['result_digest']}`")
  for row in axis['per_size']:lines.append(f"  - carrier {row['carrier_size']}: constructed={row['constructed']}, admissible={row['admissible']}, evaluated={row['evaluated']}, rejected={row['rejected']}, paired-reduct={row['paired_reduct_pass']}")
 lines += ['','## Paired-reduct coverage','']+[f"- {t}: supported bounds {r['supported_bounds']}; unsupported bounds {r['unsupported_bounds']}" for t,r in p['countermodel_coverage'].items()]+['',f"The campaign contains {p['cost_accounting']['paired_reduct_witnesses']} independently revalidated witnesses ({p['cost_accounting']['paired_reduct_models']} models). It makes no unsupported size-0 claim for Object, Property, Relation, Representation, or Interpretation.",'','## Upstream reruns','',f"- foundation executions: {p['upstream_reruns']['foundation']['foundation_executions']}",f"- ablations: {p['upstream_reruns']['foundation']['ablations']} ({p['upstream_reruns']['foundation']['ablation_executions']} executions)",f"- round trips: {p['upstream_reruns']['foundation']['round_trip_records']}",f"- dominance edges: `{json.dumps(p['upstream_reruns']['foundation']['dominance_edges'])}`",f"- terminal result: **{p['upstream_reruns']['foundation']['terminal_result']}**",'','## Historical preservation','',f"All six historical artifacts are pinned to immutable Git blob identities from `{p['base_commit']}`. `--write` refuses to regenerate evidence if any current blob differs.",'','## Boundary','','Oracle, continuous, hybrid, and embodied cases remain Unknown. Results are confined to the declared finite independent axes; full-signature cross-products and carriers above four are untested.','','## Nonclaims','']+[f'- {x}' for x in spec['nonclaims']];return '\n'.join(lines)+'\n'
def validate(spec,stored,report=None,trace_dir=TRACE_DIR,root=ROOT,check_upstream=True):
 e=[]
 if spec!=json.loads((root/SPEC.relative_to(ROOT)).read_text()):e.append('noncanonical specification')
 e+=historical_errors(spec,root);fresh=build(copy.deepcopy(spec))
 if stored!=fresh:e.append('stale, fabricated, or incomplete proof')
 if report is not None and report!=render(spec,fresh):e.append('stale report')
 if spec.get('base_commit')!='b05e48f204e273938ef406168b83cafc0958f9a0':e.append('wrong immutable base')
 if spec.get('bounds',{}).get('maximum_carrier_size',0)<=2:e.append('bound not expanded')
 if set(stored.get('unknown_cases',{}))!=set(UNKNOWN) or any(v!='Unknown' for v in stored.get('unknown_cases',{}).values()):e.append('external case overclaimed')
 if any(x.lower() in canonical(stored.get('conclusions',{})).lower() for x in FORBIDDEN):e.append('forbidden claim or label')
 axes=stored.get('enumeration_axes',[])
 if [a.get('arity') for a in axes]!=spec['bounds']['exhaustive_relation_arities']:e.append('missing executable relation axis')
 for a in axes:
  if not a.get('constructed')==a.get('admissible')==a.get('evaluated')==a.get('interpretations_examined'):e.append('relation masks counted without complete execution')
  if a.get('rejected')!=0:e.append('unexpected rejected generated relation')
  if not a.get('execution_digest') or not a.get('result_digest'):e.append('missing execution digest')
 records,coverage=build_countermodels(spec);summary=summarize_countermodels(records,coverage)
 if any(validate_countermodel(r,spec['bounds']['maximum_carrier_size']) for r in records):e.append('invalid generated countermodel')
 if stored.get('countermodel_evidence')!=summary:e.append('countermodel evidence not reproducible')
 if stored.get('countermodel_coverage')!=coverage:e.append('false countermodel size coverage')
 if stored.get('historical_artifacts')!=spec.get('historical_artifacts'):e.append('historical identities not copied from specification')
 if check_upstream:
  try:
   c,f,manifest,ue=upstream_state(spec,root);e+=ue
   if c!=spec['upstream_expectations']['core']:e.append('core rerun differs')
   if f!=spec['upstream_expectations']['foundation']:e.append('foundation rerun differs')
   disk={p.stem:json.loads(p.read_text()) for p in trace_dir.glob('*.json')} if trace_dir.exists() else {}
   if disk!=manifest:e.append('stale or incomplete trace manifest')
  except Exception as x:e.append(f'upstream rerun failed: {x}')
 return sorted(set(e))
def write_all(spec,root=ROOT,validate_upstream=True):
 h=historical_errors(spec,root)
 if h:raise ValueError('; '.join(h))
 manifest=None
 if validate_upstream:
  c,f,manifest,e=upstream_state(spec,root)
  if e:raise ValueError('; '.join(e))
  if c!=spec['upstream_expectations']['core'] or f!=spec['upstream_expectations']['foundation']:raise ValueError('upstream rerun differs')
 p=build(copy.deepcopy(spec));pp=root/PROOF.relative_to(ROOT);rp=root/REPORT.relative_to(ROOT);pp.parent.mkdir(parents=True,exist_ok=True);rp.parent.mkdir(parents=True,exist_ok=True);pp.write_text(json.dumps(p,indent=2,sort_keys=True)+'\n');rp.write_text(render(spec,p))
 if manifest is not None:
  td=root/TRACE_DIR.relative_to(ROOT);td.mkdir(parents=True,exist_ok=True)
  for f in td.glob('*.json'):f.unlink()
  for k,v in manifest.items():(td/f'{k}.json').write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
 return p
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();spec=json.loads(SPEC.read_text())
 if a.write:write_all(spec);print('wrote corrected expanded proof, report, and traces');return
 e=validate(spec,json.loads(PROOF.read_text()),REPORT.read_text())
 if e:raise SystemExit('FAIL: '+'; '.join(e))
 print('PASS: concrete relation execution, admissible witnesses, immutable historical identities, upstream reruns, Unknown boundary, and nonclaims verified')
if __name__=='__main__':main()
