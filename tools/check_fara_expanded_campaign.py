#!/usr/bin/env python3
"""Fail-closed executable campaign expanding bounded FARA evidence beyond size two."""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=ROOT/'theory/formal/fara-expanded-bounded-campaign-v1.0.json'
PROOF=ROOT/'theory/evaluation/fara-expanded-bounded-campaign-proof-v1.0.json'
REPORT=ROOT/'theory/evaluation/generated-fara-expanded-bounded-campaign-report.md'
TRACE_DIR=ROOT/'artifacts/fara-expanded-bounded-campaign/traces'
HISTORICAL=(
 'theory/formal/fara-core-formalization-v1.0.json','theory/evaluation/fara-core-formalization-proof-v1.0.json',
 'theory/evaluation/generated-fara-core-formalization-report.md','theory/formal/fara-foundation-comparison-v1.0.json',
 'theory/evaluation/fara-foundation-comparison-proof-v1.0.json','theory/evaluation/generated-fara-foundation-comparison-report.md')
FORBIDDEN=('universality','uniqueness','global superiority','minimality','necessity','completeness','W7')
UNKNOWN=('oracle','continuous','hybrid','embodied')
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def digest(x): return hashlib.sha256(canonical(x).encode()).hexdigest()
def file_digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load_module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
CORE=load_module('expanded_core',ROOT/'tools/check_fara_core_formalization.py')
FOUNDATION=load_module('expanded_foundation',ROOT/'tools/check_fara_foundation_comparison.py')
def enumerate_axis(maximum,arity):
 counts=[];total=0;checksum=hashlib.sha256()
 for n in range(maximum+1):
  interpretations=1 << (n**arity);counts.append({'carrier_size':n,'interpretations':interpretations});total+=interpretations
  for mask in range(interpretations): checksum.update(f'{n}:{arity}:{mask};'.encode())
 return {'arity':arity,'counts':counts,'interpretations_examined':total,'enumeration_digest':checksum.hexdigest()}
def countermodel(target,n):
 base={'Object':[f'o{i}' for i in range(n)],'Property':[],'Relation':[],'Representation':{},'Interpretation':{},'Investigation':{'objective':'q','conditions':[],'calculus':'r0'},'ReasoningCalculus':['r0']}
 a=copy.deepcopy(base);b=copy.deepcopy(base)
 if target=='Object': b[target]=base[target]+['extra']
 elif target=='Property': b[target]=[[base['Object'][0]]] if n else [[]]
 elif target=='Relation': b[target]=[[base['Object'][0],base['Object'][0]]] if n else [[]]
 elif target=='Representation': b[target]={'t0':base['Object'][0] if n else 'external'}
 elif target=='Interpretation': b[target]={'t0':'m0'}
 elif target=='Investigation': b[target]={'objective':'q2','conditions':[],'calculus':'r0'}
 else: b[target]=['r0','r1']
 ra={k:v for k,v in a.items() if k!=target};rb={k:v for k,v in b.items() if k!=target}
 return {'target':target,'carrier_size':n,'reducts_equal':ra==rb,'targets_differ':a[target]!=b[target],'model_a':a,'model_b':b,'verified':ra==rb and a[target]!=b[target]}
def build(spec):
 maximum=spec['bounds']['maximum_carrier_size']
 axes=[enumerate_axis(maximum,a) for a in spec['bounds']['exhaustive_relation_arities']]
 core_spec=json.loads(CORE.SPEC.read_text());core=CORE.build_proof(core_spec)
 foundation_spec=json.loads(FOUNDATION.SPEC.read_text());foundation=FOUNDATION.build(copy.deepcopy(foundation_spec))
 cms=[countermodel(t,n) for t in spec['derivability_targets'] for n in range(maximum+1)]
 statuses={u:'Unknown' for u in UNKNOWN}
 conclusions={'derivability':'all seven targets remain non-derivable within the explicitly enumerated axes and paired-reduct search only','ablations':f"{len(foundation['ablations'])} executable ablations reproduced; inference remains bounded",'translations':f"{len(foundation['traces'])} translation/reconstruction traces reproduced",'round_trips':f"{len(foundation['round_trip_ledger'])} bounded round-trip records reproduced",'preservation':'six-dimensional bounded preservation matrix reproduced; failures and partial results retained','pareto':foundation['terminal_result'],'core':core['terminal_result'],'external_cases':statuses}
 return {'campaign_id':spec['id'],'spec_digest':digest(spec),'base_commit':spec['base_commit'],'bounds':spec['bounds'],'cost_accounting':{'enumeration_axes':axes,'paired_reduct_models':len(cms)*2,'core_model_families':len(core['models']),'foundation_benchmarks':len(foundation_spec['benchmarks']),'foundation_executions':len(foundation['traces']),'ablation_executions':sum(len(x['executions']) for x in foundation['ablations']),'round_trip_records':len(foundation['round_trip_ledger'])},'countermodels':cms,'core':{'proof_digest':digest(core),'models':core['models'],'foundation_checks':core['foundation_checks'],'terminal_result':core['terminal_result']},'foundation':{'proof_digest':digest(foundation),'results':foundation['results'],'ablations':foundation['ablations'],'round_trip_ledger':foundation['round_trip_ledger'],'preservation_matrix':foundation['preservation_matrix'],'structural_accounting':foundation['structural_accounting'],'pareto_vectors':foundation['pareto_vectors'],'pareto_matrix':foundation['pareto_matrix'],'dominance_graph':foundation['dominance_graph'],'terminal_result':foundation['terminal_result']},'trace_manifest':{k:{'digest':digest(v),'status':v['status'],'preservation':v['preservation'],'structural_accounting':v['structural_accounting']} for k,v in foundation['traces'].items()},'historical_artifacts':{p:file_digest(ROOT/p) for p in HISTORICAL},'conclusions':conclusions,'nonclaims':spec['nonclaims'],'unknown_cases':statuses}
def render(spec,p):
 axes='\n'.join(f"- arity {a['arity']}: {a['interpretations_examined']} interpretations; per carrier {a['counts']}" for a in p['cost_accounting']['enumeration_axes'])
 return f"""# Expanded bounded FARA executable campaign\n\nStatus: Research\n\nBase: `{p['base_commit']}`. Maximum carrier size: **{p['bounds']['maximum_carrier_size']}**.\n\n## Explicit bounds and cost\n{axes}\n- paired reduct models: {p['cost_accounting']['paired_reduct_models']}\n- foundation executions: {p['cost_accounting']['foundation_executions']}\n- ablation executions: {p['cost_accounting']['ablation_executions']}\n- round-trip records: {p['cost_accounting']['round_trip_records']}\n\n## Changed conclusions\n"""+'\n'.join(f'- **{k}:** {v}' for k,v in p['conclusions'].items())+'\n\n## Boundary\nOracle, continuous, hybrid, and embodied cases remain Unknown. Results are confined to the declared finite axes.\n\n## Nonclaims\n'+'\n'.join('- '+x for x in spec['nonclaims'])+'\n'
def validate(spec,stored,report=None,trace_dir=TRACE_DIR):
 errors=[]
 if spec!=json.loads(SPEC.read_text()):errors.append('noncanonical specification')
 fresh=build(copy.deepcopy(spec));normalized=copy.deepcopy(stored);expected=copy.deepcopy(fresh)
 if normalized!=expected:errors.append('stale, fabricated, or incomplete proof')
 if report is not None and report!=render(spec,fresh):errors.append('stale report')
 if spec.get('base_commit')!='b05e48f204e273938ef406168b83cafc0958f9a0':errors.append('wrong base')
 if spec.get('bounds',{}).get('maximum_carrier_size',0)<=2:errors.append('bound not expanded')
 if any(v!='Unknown' for v in stored.get('unknown_cases',{}).values()) or set(stored.get('unknown_cases',{}))!=set(UNKNOWN):errors.append('external case overclaimed')
 if any(term.lower() in canonical(stored.get('conclusions',{})).lower() for term in FORBIDDEN):errors.append('forbidden claim or label')
 if not all(c.get('verified') for c in stored.get('countermodels',[])):errors.append('invalid countermodel')
 if len(stored.get('countermodels',[]))!=len(spec['derivability_targets'])*(spec['bounds']['maximum_carrier_size']+1):errors.append('incomplete countermodel search')
 disk={p.stem:json.loads(p.read_text()) for p in trace_dir.glob('*.json')} if trace_dir.exists() else {}
 if disk!=fresh['trace_manifest']:errors.append('stale or incomplete trace manifest')
 if stored.get('historical_artifacts')!={p:file_digest(ROOT/p) for p in HISTORICAL}:errors.append('historical evidence overwritten')
 return sorted(set(errors))
def write_all(spec):
 p=build(copy.deepcopy(spec));PROOF.write_text(json.dumps(p,indent=2,sort_keys=True)+'\n');REPORT.write_text(render(spec,p));TRACE_DIR.mkdir(parents=True,exist_ok=True)
 for f in TRACE_DIR.glob('*.json'):f.unlink()
 for k,v in p['trace_manifest'].items():(TRACE_DIR/f'{k}.json').write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');x=a.parse_args();spec=json.loads(SPEC.read_text())
 if x.write:write_all(spec);print('wrote expanded bounded proof, traces, and report');return
 errors=validate(spec,json.loads(PROOF.read_text()),REPORT.read_text());
 if errors:raise SystemExit('FAIL: '+'; '.join(errors))
 print('PASS: expanded bounds, reruns, accounting, historical preservation, Unknown boundary, and nonclaims verified')
if __name__=='__main__':main()
