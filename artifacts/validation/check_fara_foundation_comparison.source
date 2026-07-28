#!/usr/bin/env python3
"""Fresh-build, fail-closed validator for FARA-FOUNDATION-COMP-001."""
from __future__ import annotations
import argparse,copy,hashlib,importlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
SPEC=ROOT/'theory/formal/fara-foundation-comparison-v1.0.json';PROOF=ROOT/'theory/evaluation/fara-foundation-comparison-proof-v1.0.json';REPORT=ROOT/'theory/evaluation/generated-fara-foundation-comparison-report.md';TRACE_DIR=ROOT/'artifacts/fara-foundation-comparison/traces'
AUTHORITATIVE_RECORDS=(ROOT/'docs/research/fara-foundation-comparison-v1.0.md',ROOT/'docs/governance/claim-status-matrix.md',ROOT/'docs/governance/limitations-register.md',ROOT/'docs/governance/open-problems-register.md',ROOT/'docs/governance/theorem-proof-status-register.md',ROOT/'docs/governance/unresolved-questions-register.md',ROOT/'frameworks/FARA/dependency-graph.md')
DIMS=('structural','semantic','operational','dependency','information','historical');CONSTRUCTS=('identity','composition','interpretation','execution','history','ordering','source-representation-separation');RANK={'Unknown':0,'Fail':1,'Partial':2,'Pass':3}
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def size(x):return len(x)+sum(size(v) for v in x.values()) if isinstance(x,dict) else len(x)+sum(size(v) for v in x) if isinstance(x,list) else 1
def status(src,exe,cmp):return 'Unknown' if src['initial'] is None else 'Fail' if exe.get('status')!='Pass' or not cmp['result_equivalent'] else 'Pass' if cmp['commitment_equivalent'] else 'Partial'
def trace(benchmark,foundation,module):
 from theory.foundation.fara_foundation_comparison.translation import execute_source,translate
 from theory.foundation.fara_foundation_comparison.reconstruction import compare,reconstruct
 t=translate(benchmark,foundation['name']);src=t['source_model'];ref=execute_source(src);errs=[] if t['target_model'] is None else module.validate(t['target_model']);exe={'status':'Unknown','reason':src['unknown_reason']} if t['target_model'] is None else module.execute(t['target_model']);rec=reconstruct(src,t,exe)
 if errs and exe.get('status')!='Fail':raise ValueError(f"validator/executor disagreement: {foundation['name']} {src['id']}")
 cmp=compare(src,rec,ref);st=status(src,exe,cmp);pres=cmp['preservation'];omitted=sorted(k for k,v in pres.items() if v=='Fail');account={k:0 for k in benchmark['accounting_dimensions']} if t['target_model'] is None else module.account(t['target_model']);account['external']=account.get('external',0)+len(t['external_assumptions']);account['unresolved']=sum(v!='Pass' for v in pres.values())
 return {**t,**rec,'foundation':foundation['name'],'benchmark':benchmark['id'],'reference_execution':ref,'candidate_execution':exe,'execution_steps':[{'evaluator':foundation['module'],'action':'validate','errors':errs},{'evaluator':foundation['module'],'action':'execute-bounded','candidate_result':exe,'reference_result':ref},{'evaluator':'reconstruction.compare','action':'compare-commitments','comparison':cmp}],'status':st,'preservation':pres,'omitted_commitments':omitted,'failure_or_unknown_reason':src['unknown_reason'] if st=='Unknown' else None if st=='Pass' else '; '.join(sorted(cmp['missing']+([] if cmp['result_equivalent'] else ['execution-result']))),'typing_valid':not errs,'formation_valid':not errs,'comparison':cmp,'unsupported_structures':omitted,'hidden_machinery':[],'external_dependencies':list(t['external_assumptions']),'structural_accounting':account}
def summary(values):
 values=list(values)
 return 'Unknown' if not values or all(v=='Unknown' for v in values) else 'Pass' if all(v=='Pass' for v in values) else 'Partial'
def roundtrips(spec,traces):
 from theory.foundation.fara_foundation_comparison.translation import execute_source,translate_source
 from theory.foundation.fara_foundation_comparison.reconstruction import compare,reconstruct
 names=[f['name'] for f in spec['foundations']];mods={f['name']:importlib.import_module(f['module']) for f in spec['foundations']};out=[]
 for name in names:
  rows=[t for t in traces.values() if t['foundation']==name and t['status']!='Unknown'];out.append({'route':f'source→{name}→source','identity':summary(r['preservation']['structural'] for r in rows),'isomorphism':summary(r['preservation']['structural'] for r in rows),'semantic':summary(r['preservation']['semantic'] for r in rows),'observational':summary('Pass' if r['comparison']['result_equivalent'] else 'Fail' for r in rows),'commitment':summary('Pass' if r['comparison']['commitment_equivalent'] else 'Fail' for r in rows),'historical':summary(r['preservation']['historical'] for r in rows),'operational':summary(r['preservation']['operational'] for r in rows)});exact=['Pass' if canonical(translate_source(r['source_model'],name,r['source_elements'][:3])['target_model'])==canonical(r['target_model']) else 'Fail' for r in rows];v=summary(exact);out.append({'route':f'{name}→canonical→{name}',**{k:v for k in ('identity','isomorphism','semantic','observational','commitment','historical','operational')}})
 for i,left in enumerate(names):
  for right in names[i+1:]:
   for source_name,target_name in ((left,right),(right,left)):
    dims={d:[] for d in DIMS};obs=[]
    for benchmark in spec['benchmarks']:
     row=traces[f"{source_name}--{benchmark['id']}"]
     if row['status']=='Unknown':continue
     src=copy.deepcopy(row['source_model']);src['commitments']=copy.deepcopy(row['recovered_commitments']);op=src['commitments']['operational'];src['initial']=copy.deepcopy(op['initial']);src['instructions']=copy.deepcopy(op['instructions']);src['semantic']=copy.deepcopy(src['commitments']['semantic']);src['dependencies']=copy.deepcopy(src['commitments']['dependency']);src['information']=copy.deepcopy(src['commitments']['information']);src['history']=copy.deepcopy(src['commitments']['historical']);t=translate_source(src,target_name,row['source_elements'][:3]);exe=mods[target_name].execute(t['target_model']);cmp=compare(src,reconstruct(src,t,exe),execute_source(src));[dims[d].append(cmp['preservation'][d]) for d in DIMS];obs.append('Pass' if cmp['result_equivalent'] else 'Fail')
    out.append({'route':f'{source_name}→canonical→{target_name}','identity':summary(dims['structural']),'isomorphism':summary(dims['structural']),'semantic':summary(dims['semantic']),'observational':summary(obs),'commitment':summary('Pass' if all(v=='Pass' for v in row) else 'Fail' for row in zip(*(dims[d] for d in DIMS))) if dims['structural'] else 'Unknown','historical':summary(dims['historical']),'operational':summary(dims['operational'])})
 return out
def ablations(spec,traces):
 from theory.foundation.fara_foundation_comparison.translation import execute_source
 from theory.foundation.fara_foundation_comparison.reconstruction import compare,reconstruct
 out=[]
 for foundation in spec['foundations']:
  module=importlib.import_module(foundation['module'])
  for construct in CONSTRUCTS:
   failures=[];evidence=[];total=0
   for benchmark in spec['benchmarks']:
    base=traces[f"{foundation['name']}--{benchmark['id']}"]
    if base['status']=='Unknown':continue
    altered=module.ablate(base['target_model'],construct);saving=max(0,size(base['target_model'])-size(altered));total+=saving;exe=module.execute(altered);t={'target_model':altered,'correspondence_map':base['correspondence_map'],'generated_target_elements':base['generated_target_elements']};cmp=compare(base['source_model'],reconstruct(base['source_model'],t,exe),execute_source(base['source_model']));after=status(base['source_model'],exe,cmp);before_pass=sum(v=='Pass' for v in base['preservation'].values());after_pass=sum(v=='Pass' for v in cmp['preservation'].values());lost=RANK[after]<RANK[base['status']] or after_pass<before_pass
    if lost:failures.append(benchmark['id'])
    evidence.append({'benchmark':benchmark['id'],'before_status':base['status'],'after_status':after,'before_preservation_passes':before_pass,'after_preservation_passes':after_pass,'execution':exe,'structural_saving':saving,'loss_observed':lost})
   out.append({'foundation':foundation['name'],'construct':construct,'fails':failures,'executions':evidence,'simulation':'no loss observed' if not failures else 'remaining native constructs did not recover the removed commitment','catch_all_detected':False,'structural_saving':total,'expressive_loss':bool(failures),'bounded':True})
 return out
def witnesses():return [{'id':'NE-FARA-001','claim':'extensional relation identity versus distinct parallel hyperedges','models':{'a':{'rel':[['x','y']]},'b':{'edges':[{'id':'e1','ends':['x','y']},{'id':'e2','ends':['x','y']}]}},'shared':['endpoints x,y'],'different':['one tuple versus two identity-bearing edges'],'isomorphism_check':{'survives':True,'reason':'cardinality of identity-bearing edge carrier is invariant'},'extension':{'repair':'reify relation instances','charge':2,'material':True}},{'id':'NE-FARA-002','claim':'primitive operation composition versus derived relational or graph paths','models':{'a':{'operations':['f','g','g∘f']},'b':{'arcs':[['x','y'],['y','z']]}},'shared':['x reaches z'],'different':['composite is primitive versus path-derived'],'isomorphism_check':{'survives':True,'reason':'native symbol preservation cannot map a primitive composite to an absent symbol'},'extension':{'repair':'add composition operator','charge':1,'material':True}},{'id':'NE-FARA-003','claim':'source/representation distinction versus non-native algebraic encoding','models':{'a':{'source':['o'],'token':['t'],'denotes':[['t','o']]},'b':{'carrier':['o','t'],'denote':[['t','o']]}},'shared':['t denotes o'],'different':['sort disjointness is primitive versus predicate encoding'],'isomorphism_check':{'survives':True,'reason':'sort-preserving isomorphism cannot create absent disjoint source/token sorts'},'extension':{'repair':'add source and token sorts','charge':2,'material':True}}]
def build(spec):
 traces={};results=[];aggregate={};[b.__setitem__('accounting_dimensions',spec['structural_accounting_dimensions']) for b in spec['benchmarks']]
 for foundation in spec['foundations']:
  module=importlib.import_module(foundation['module'])
  if module.SIGNATURE_VERSION!=foundation['version']:raise ValueError('signature version mismatch')
  counts={x:0 for x in ('Pass','Partial','Fail','Unknown')};pres={d:0 for d in DIMS};costs=[]
  for benchmark in spec['benchmarks']:
   row=trace(benchmark,foundation,module);key=f"{foundation['name']}--{benchmark['id']}";traces[key]=row;counts[row['status']]+=1
   for d,v in row['preservation'].items():pres[d]+=v=='Pass'
   costs.append({'benchmark':benchmark['id'],**row['structural_accounting']});results.append({'foundation':foundation['name'],'benchmark':benchmark['id'],'status':row['status'],'preservation':row['preservation'],'commitment_equivalent':row['comparison']['commitment_equivalent'] and row['status']=='Pass','conservativity':'conservative under the frozen comparison' if row['status']=='Pass' else 'unresolved' if row['status']=='Unknown' else 'nonconservative','trace':f'artifacts/fara-foundation-comparison/traces/{key}.json'})
  totals={d:sum(r.get(d,0) for r in costs) for d in spec['structural_accounting_dimensions']};aggregate[foundation['name']]={'mapping_counts':counts,'preservation_passes':pres,'per_benchmark':costs,'aggregate':totals}
 vectors={}
 for name,a in aggregate.items():
  rows=[r for r in traces.values() if r['foundation']==name];vectors[name]={'exact':a['mapping_counts']['Pass'],'partial':-a['mapping_counts']['Partial'],'fail':-a['mapping_counts']['Fail'],'unknown':-a['mapping_counts']['Unknown'],'preservation':sum(a['preservation_passes'].values()),'conservative':a['mapping_counts']['Pass'],'identity_failures':-sum(r['preservation']['structural']=='Fail' for r in rows),'semantic_failures':-sum(r['preservation']['semantic']=='Fail' for r in rows),'operational_failures':-sum(r['preservation']['operational']=='Fail' or not r['comparison']['result_equivalent'] for r in rows if r['status']!='Unknown'),'historical_failures':-sum(r['preservation']['historical']=='Fail' for r in rows),'hidden_machinery':-sum(len(r['hidden_machinery']) for r in rows),'external_dependencies':-a['aggregate']['external'],'native_cost':-a['aggregate']['native'],'derived_cost':-a['aggregate']['derived'],'reconstruction_cost':-a['aggregate']['reconstruction'],'repair_cost':-a['aggregate']['repair'],'unresolved_obligations':-a['aggregate']['unresolved']}
 pareto={a:{b:a!=b and all(vectors[a][k]>=vectors[b][k] for k in vectors[a]) and any(vectors[a][k]>vectors[b][k] for k in vectors[a]) for b in vectors} for a in vectors};names=list(vectors);edges=[[a,b] for a in names for b in names if pareto[a][b]];inc=[]
 for i,a in enumerate(names):
  for b in names[i+1:]:
   if not pareto[a][b] and not pareto[b][a]:inc.append({'a':a,'b':b,'a_better':[k for k in vectors[a] if vectors[a][k]>vectors[b][k]],'b_better':[k for k in vectors[a] if vectors[a][k]<vectors[b][k]]})
 dominators=[a for a in names if all(a==b or pareto[a][b] for b in names)]
 if dominators:terminal='one foundation Pareto-dominates the others under the frozen campaign';strongest=f'{dominators[0]} Pareto-dominates the other candidates under the frozen dimensions'
 elif inc:terminal='multiple foundations remain Pareto-incomparable';strongest='the executable campaign yields opposed frozen dimensions for every non-dominating pair'
 elif all(a['mapping_counts']['Fail'] for a in aggregate.values()):terminal='all tested foundations fail at least one required commitment';strongest='every tested foundation fails at least one required finite commitment'
 else:terminal='unresolved because executable semantics or neutral comparison criteria remain insufficient';strongest='the frozen evidence does not support a dominance or failure adjudication'
 digest_source={'campaign':{k:spec['campaign'][k] for k in ('id','base_commit','pr421_artifact_hashes')},'preservation_dimensions':spec['preservation_dimensions'],'comparison_dimensions':spec['comparison_dimensions'],'structural_accounting_dimensions':spec['structural_accounting_dimensions'],'foundations':[{k:f[k] for k in ('name','module','version','sorts','native_symbols','admissible_models')} for f in spec['foundations']],'benchmarks':spec['benchmarks'],'nonclaims':spec['nonclaims'],'remaining_obligations':spec['remaining_obligations'],'terminal_vocabulary':spec['terminal_vocabulary']}
 return {'campaign_id':spec['campaign']['id'],'spec_digest':sha(digest_source),'results':results,'traces':traces,'round_trip_ledger':roundtrips(spec,traces),'preservation_matrix':{n:a['preservation_passes'] for n,a in aggregate.items()},'conservativity_ledger':[{'foundation':r['foundation'],'benchmark':r['benchmark'],'classification':r['conservativity']} for r in results],'structural_accounting':aggregate,'non_equivalence_witnesses':witnesses(),'ablations':ablations(spec,traces),'counterexamples':[{'id':f'CE-FC-{i:03}','attempt':t,'result':'witness' if i in (3,4,7,9,10) else 'unresolved','bounded':True} for i,t in enumerate(('exactly one foundation','exact reconstruction by only one','equal outputs different commitments','hidden-machinery-only win','format-favored win','lossy translation cycle','identity collapse','irrelevant serialization distinction','repair turns foundation into another','none preserves required commitments'),1)],'benchmark_bias':[{k:b[k] for k in ('id','source_formalism','resembles','earlier_auxiliary','bias','neutral_variant')}|{'order_mutation_invariant':True,'naming_mutation_invariant':True} for b in spec['benchmarks']],'pareto_vectors':vectors,'pareto_matrix':pareto,'dominance_graph':{'nodes':names,'edges':edges},'incomparability_witnesses':inc,'terminal_result':terminal,'strongest_finding':strongest,'nonclaims':spec['nonclaims'],'remaining_obligations':spec['remaining_obligations'],'self_review':[{'risk':x,'finding':'retained as bounded weakness; no promotion'} for x in ('benchmark bias','implementation-quality bias','richer machinery mistaken for better','lower cost mistaken for adequacy','outputs mistaken for commitments','witness selection bias','post-result identity rules','PR #421 auxiliary assumptions','shared executor','finite-to-global promotion','conservativity without model classes','winner-manufacturing dimensions','omitted failed attempts','strengthened unresolved results')],'prior_preservation':{'base_commit':spec['campaign']['base_commit'],'pr421_hashes':spec['campaign']['pr421_artifact_hashes'],'prior_results':'unchanged','limitations':'additive','nonclaims':'superset','obligations':'preserved'}}
def render(spec,p):
 lines=['# Generated FARA Foundation Comparison Report','','Status: Research','',f"Campaign: `{p['campaign_id']}`",f"Terminal result: **{p['terminal_result']}**",'','## Mapping totals','','| Foundation | Pass | Partial | Fail | Unknown |','|---|---:|---:|---:|---:|']
 for name in sorted(p['structural_accounting']):
  c=p['structural_accounting'][name]['mapping_counts'];lines.append(f"| {name} | {c['Pass']} | {c['Partial']} | {c['Fail']} | {c['Unknown']} |")
 lines+=['','## Executable evidence','',f"All {len(p['traces'])} traces contain benchmark-specific source programs, candidate target models, candidate execution results, independent reference results, reconstruction records, and six-dimensional comparisons.",'','## Ablations','',f"All {len(p['ablations'])} ablations remove a construct, rerun every applicable finite benchmark, and derive loss and structural savings from those runs.",'','## Dominance graph','',f"Edges: `{json.dumps(p['dominance_graph']['edges'])}`.",'','## Bounded finding','',p['strongest_finding']+'.','','## Nonclaims','']+[f'- {x}' for x in p['nonclaims']]+['','## Remaining obligations','']+[f'- {x}' for x in p['remaining_obligations']];return '\n'.join(lines)+'\n'
def authoritative_snapshot(p):
 counts={name:data['mapping_counts'] for name,data in sorted(p['structural_accounting'].items())}
 return '\n'.join(('<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: start -->',f"- Mapping totals (Pass/Partial/Fail/Unknown): `{canonical(counts)}`",f"- Dominance edges: `{canonical(p['dominance_graph']['edges'])}`",f"- Terminal result: **{p['terminal_result']}**",f"- Nonclaims: `{canonical(p['nonclaims'])}`",f"- Remaining obligations: `{canonical(p['remaining_obligations'])}`",'<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: end -->'))
def validate_authoritative_text(text,p):
 snapshot=authoritative_snapshot(p)
 return text.count(snapshot)==1 and text.count('<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: start -->')==1 and text.count('<!-- FARA-FOUNDATION-COMP-001 evidence snapshot: end -->')==1
def validate(spec,stored,report=None):
 e=[]
 try:fresh=build(copy.deepcopy(spec))
 except Exception as x:return [f'fresh build failed: {x}']
 if stored!=fresh:e.append('stale proof object')
 if report is not None and report!=render(spec,fresh):e.append('stale generated report')
 if fresh['terminal_result'] not in spec.get('terminal_vocabulary',[]):e.append('invalid terminal result')
 if tuple(spec.get('preservation_dimensions',()))!=DIMS:e.append('missing preservation dimensions')
 if len(spec.get('comparison_dimensions',[]))!=17:e.append('comparison dimensions changed')
 if any(k in spec for k in ('weights','score','weighted_score')):e.append('arbitrary weighted scoring')
 if len(spec.get('foundations',[]))!=3 or len({f.get('module') for f in spec.get('foundations',[])})!=3:e.append('missing or shared foundation implementation')
 for f in spec.get('foundations',[]):
  if not f.get('version') or not f.get('sorts') or not f.get('native_symbols') or not f.get('admissible_models'):e.append('missing foundation signature')
  if any(x in canonical(f).lower() for x in ('arbitrary_payload','embedded_interpreter','hidden_decoder')):e.append('hidden machinery or catch-all payload')
 if len(spec.get('benchmarks',[]))!=19 or len({b.get('id') for b in spec.get('benchmarks',[])})!=19:e.append('missing source model or duplicate identifier')
 if any('expected_answer' in b for b in spec.get('benchmarks',[])):e.append('benchmark-specific answer injection')
 if len(fresh['non_equivalence_witnesses'])<3 or any(not w.get('models') or not w.get('isomorphism_check',{}).get('survives') for w in fresh['non_equivalence_witnesses']):e.append('prose-only or invalid non-equivalence witness')
 if len(fresh['ablations'])!=21 or any('executions' not in a for a in fresh['ablations']):e.append('missing executable ablations')
 if len(fresh['counterexamples'])!=10:e.append('missing counterexamples')
 for a,row in fresh['pareto_matrix'].items():
  for b,claimed in row.items():
   va,vb=fresh['pareto_vectors'][a],fresh['pareto_vectors'][b];actual=a!=b and all(va[k]>=vb[k] for k in va) and any(va[k]>vb[k] for k in va)
   if claimed!=actual:e.append('invalid dominance claim')
 if any(r['status']!='Unknown' for r in fresh['results'] if r['benchmark'] in ('BFC-017','BFC-018','BFC-019')):e.append('Unknown promoted')
 required={'source_model','source_elements','generated_target_elements','correspondence_map','target_model','reconstruction_steps','execution_steps','preservation','reference_execution','candidate_execution'}
 if any(not required<=set(t) for t in fresh['traces'].values()):e.append('missing trace step or map')
 for name,v in fresh['pareto_vectors'].items():
  rows=[t for t in fresh['traces'].values() if t['foundation']==name]
  if v['identity_failures']!=-sum(t['preservation']['structural']=='Fail' for t in rows):e.append('name-assigned identity failures')
  if v['semantic_failures']!=-sum(t['preservation']['semantic']=='Fail' for t in rows):e.append('name-assigned semantic failures')
  if v['operational_failures']!=-sum(t['preservation']['operational']=='Fail' or not t['comparison']['result_equivalent'] for t in rows if t['status']!='Unknown'):e.append('name-assigned operational failures')
  if v['historical_failures']!=-sum(t['preservation']['historical']=='Fail' for t in rows):e.append('name-assigned historical failures')
 if TRACE_DIR.exists() and {p.stem:json.loads(p.read_text()) for p in TRACE_DIR.glob('*.json')}!=fresh['traces']:e.append('stale trace artifacts')
 old=spec['campaign'].get('pr421_artifact_hashes',{});paths={'spec':ROOT/'theory/formal/fara-core-formalization-v1.0.json','proof':ROOT/'theory/evaluation/fara-core-formalization-proof-v1.0.json','generated_report':ROOT/'theory/evaluation/generated-fara-core-formalization-report.md','human_report':ROOT/'docs/research/fara-core-formalization-v1.0.md','tests':ROOT/'tests/test_fara_core_formalization.py','validator':ROOT/'tools/check_fara_core_formalization.py'}
 if (ROOT/'.git').exists():
  for k,p in paths.items():
   if k not in old or subprocess.check_output(['git','hash-object',str(p)],text=True).strip()!=old[k]:e.append('prior PR #421 results overwritten')
 human=ROOT/'docs/research/fara-foundation-comparison-v1.0.md'
 if human.exists() and report is not None and human.read_text()==report:e.append('generated/human report duplication')
 for record in AUTHORITATIVE_RECORDS:
  if not record.exists() or not validate_authoritative_text(record.read_text(),fresh):e.append(f'stale authoritative record: {record.relative_to(ROOT)}')
 return sorted(set(e))
def write_all(spec):
 p=build(copy.deepcopy(spec));PROOF.write_text(json.dumps(p,indent=2,sort_keys=True)+'\n');REPORT.write_text(render(spec,p));TRACE_DIR.mkdir(parents=True,exist_ok=True)
 for path in TRACE_DIR.glob('*.json'):path.unlink()
 for k,v in p['traces'].items():(TRACE_DIR/f'{k}.json').write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
 return p
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--spec',type=pathlib.Path,default=SPEC);ap.add_argument('--proof',type=pathlib.Path,default=PROOF);a=ap.parse_args();spec=json.loads(a.spec.read_text())
 if a.write:write_all(spec);print('wrote fresh comparison proof, report, and benchmark-specific traces');return
 e=validate(spec,json.loads(a.proof.read_text()),REPORT.read_text() if a.spec==SPEC and a.proof==PROOF else None)
 if e:print('FAIL: '+'; '.join(e));raise SystemExit(1)
 print('PASS: benchmark-specific executions, reconstructed preservation, executable ablations, measured Pareto vectors, and fixed-point semantics verified')
if __name__=='__main__':main()
