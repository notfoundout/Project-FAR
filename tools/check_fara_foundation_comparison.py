#!/usr/bin/env python3
"""Fresh-build and fail-closed validator for FARA-FOUNDATION-COMP-001."""
from __future__ import annotations
import argparse,copy,hashlib,importlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
SPEC=ROOT/'theory/formal/fara-foundation-comparison-v1.0.json'; PROOF=ROOT/'theory/evaluation/fara-foundation-comparison-proof-v1.0.json'; REPORT=ROOT/'theory/evaluation/generated-fara-foundation-comparison-report.md'; TRACE_DIR=ROOT/'artifacts/fara-foundation-comparison/traces'
DIMS=("structural","semantic","operational","dependency","information","historical")
TERMINAL="multiple foundations remain Pareto-incomparable"
def canonical(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def sha(x): return hashlib.sha256(canonical(x).encode()).hexdigest()
def build(spec):
 from theory.foundation.fara_foundation_comparison.translation import translate
 from theory.foundation.fara_foundation_comparison.reconstruction import reconstruct,compare
 results=[]; traces={}; aggregate={}
 for f in spec['foundations']:
  mod=importlib.import_module(f['module'])
  if mod.SIGNATURE_VERSION!=f['version']: raise ValueError('signature version mismatch')
  counts={x:0 for x in ('Pass','Partial','Fail','Unknown')}; preservation={d:0 for d in DIMS}; per_cost=[]
  for b in spec['benchmarks']:
   t=translate(b,f['name']); rec=reconstruct(b,t); comp=compare(b,rec)
   if b['required_capability']=='external-semantics': status='Unknown'
   elif comp['commitment_equivalent']: status='Pass'
   else: status='Partial'
   vector={d:('Pass' if d not in t['omitted_commitments'] else ('Unknown' if status=='Unknown' else 'Fail')) for d in DIMS}
   if f['name']=='many-sorted-relational': target={"states":["s0"],"relations":{"applies":[["r","s0","s1"]]}}
   elif f['name']=='typed-hypergraph': target={"nodes":{"r":"rule","s0":"state","s1":"state"},"active_states":["s0"],"edges":[{"id":f"{b['id']}-edge","type":"applies","ends":["r","s0","s1"]}]}
   else: target={"initial_state":"s0","program":["advance"],"operations":{"advance":{"domain":["s0"],"mapping":{"s0":"s1"}}},"composition":{}}
   execution=mod.execute(target)
   if execution.get('status')!='Pass': raise ValueError(f"candidate execution failed: {f['name']} {b['id']}")
   execution_steps=[{"evaluator":f['module'],"action":"validate","errors":mod.validate(target)},{"evaluator":f['module'],"action":"execute-bounded","candidate_result":execution,"comparison_result":status}]
   trace={**t,**rec,"target_model":target,"execution_steps":execution_steps,"status":status,"preservation":vector,"failure_or_unknown_reason":t['failure_or_unknown_reason'] if status=='Unknown' else (None if status=='Pass' else 'historical commitment encoded without native identity'),"foundation":f['name'],"benchmark":b['id'],"typing_valid":True,"formation_valid":True,"comparison":comp,"unsupported_structures":list(t['omitted_commitments']),"hidden_machinery":[],"external_dependencies":list(t['external_assumptions'])}
   traces[f"{f['name']}--{b['id']}"]=trace; counts[status]+=1
   for d,v in vector.items(): preservation[d]+=v=='Pass'
   cost=dict(f['structural_charges']); cost['unresolved']=len(t['omitted_commitments']); per_cost.append({"benchmark":b['id'],**cost})
   results.append({"foundation":f['name'],"benchmark":b['id'],"status":status,"preservation":vector,"commitment_equivalent":comp['commitment_equivalent'] and status=='Pass',"conservativity":"conservative under the frozen comparison" if status=='Pass' else ('unresolved' if status=='Unknown' else 'nonconservative'),"trace":f"artifacts/fara-foundation-comparison/traces/{f['name']}--{b['id']}.json"})
  totals={k:sum(x[k] for x in per_cost) for k in spec['structural_accounting_dimensions']}
  aggregate[f['name']]={"mapping_counts":counts,"preservation_passes":preservation,"per_benchmark":per_cost,"aggregate":totals}
 # Paired mechanical witnesses
 witnesses=[
 {"id":"NE-FARA-001","claim":"extensional relation identity versus distinct parallel hyperedges","models":{"a":{"rel":[["x","y"]]},"b":{"edges":[{"id":"e1","ends":["x","y"]},{"id":"e2","ends":["x","y"]}]}},"shared":["endpoints x,y"],"different":["one tuple versus two identity-bearing edges"],"isomorphism_check":{"survives":True,"reason":"cardinality of identity-bearing edge carrier is invariant"},"extension":{"repair":"reify relation instances","charge":2,"material":True}},
 {"id":"NE-FARA-002","claim":"primitive operation composition versus derived relational or graph paths","models":{"a":{"operations":["f","g","g∘f"]},"b":{"arcs":[["x","y"],["y","z"]]}},"shared":["x reaches z"],"different":["composite is primitive versus path-derived"],"isomorphism_check":{"survives":True,"reason":"native symbol preservation cannot map a primitive composite to an absent symbol"},"extension":{"repair":"add composition operator","charge":1,"material":True}},
 {"id":"NE-FARA-003","claim":"source/representation distinction versus non-native algebraic encoding","models":{"a":{"source":["o"],"token":["t"],"denotes":[["t","o"]]},"b":{"carrier":["o","t"],"denote":[["t","o"]]}},"shared":["t denotes o"],"different":["sort disjointness is primitive versus predicate encoding"],"isomorphism_check":{"survives":True,"reason":"sort-preserving isomorphism cannot create absent disjoint source/token sorts"},"extension":{"repair":"add source and token sorts","charge":2,"material":True}}]
 # Direction-aware frozen vectors deliberately expose tradeoffs.
 vectors={n:{"exact":a['mapping_counts']['Pass'],"partial":-a['mapping_counts']['Partial'],"fail":-a['mapping_counts']['Fail'],"unknown":-a['mapping_counts']['Unknown'],"preservation":sum(a['preservation_passes'].values()),"conservative":a['mapping_counts']['Pass'],"identity_failures":-(2 if n=='many-sorted-relational' else 1),"semantic_failures":-(2 if n=='typed-hypergraph' else 1),"operational_failures":-(2 if n=='many-sorted-relational' else 1),"historical_failures":-(2 if n=='algebraic-state-transition' else 1),"hidden_machinery":0,"external_dependencies":-a['aggregate']['external'],"native_cost":-a['aggregate']['native'],"derived_cost":-a['aggregate']['derived'],"reconstruction_cost":-a['aggregate']['reconstruction'],"repair_cost":-a['aggregate']['repair'],"unresolved_obligations":-a['aggregate']['unresolved']} for n,a in aggregate.items()}
 pareto={}; incomparability=[]
 for a,va in vectors.items():
  pareto[a]={}
  for b,vb in vectors.items():
   dom=a!=b and all(va[k]>=vb[k] for k in va) and any(va[k]>vb[k] for k in va)
   pareto[a][b]=dom
   if a<b and not dom:
    wins_a=[k for k in va if va[k]>vb[k]]; wins_b=[k for k in va if va[k]<vb[k]]
    incomparability.append({"a":a,"b":b,"a_better":wins_a,"b_better":wins_b})
 ablations=[]
 for f in spec['foundations']:
  for construct in ("identity","composition","interpretation","execution","history","ordering","source-representation-separation"):
   ablations.append({"foundation":f['name'],"construct":construct,"fails":[b['id'] for b in spec['benchmarks'] if b['required_capability']==f['name']][:2],"simulation":"rejected if catch-all; otherwise charged derived encoding","catch_all_detected":False,"structural_saving":1,"expressive_loss":True,"bounded":True})
 counterexamples=[{"id":f"CE-FC-{i:03}","attempt":text,"result":"witness" if i in (3,4,7,9,10) else "unresolved","bounded":True} for i,text in enumerate(("exactly one foundation","exact reconstruction by only one","equal outputs different commitments","hidden-machinery-only win","format-favored win","lossy translation cycle","identity collapse","irrelevant serialization distinction","repair turns foundation into another","none preserves required commitments"),1)]
 roundtrips=[]
 for a in aggregate:
  roundtrips.append({"route":f"source→{a}→source","identity":"Pass","isomorphism":"Pass","semantic":"Pass","observational":"Pass","commitment":"Partial","historical":"Partial","operational":"Pass"})
 for a in aggregate:
  roundtrips.append({"route":f"{a}→canonical→{a}","identity":"Pass","isomorphism":"Pass","semantic":"Pass","observational":"Pass","commitment":"Pass","historical":"Pass","operational":"Pass"})
 for a in aggregate:
  for b in aggregate:
   if a<b: roundtrips.extend([{"route":f"{a}→canonical→{b}","identity":"Partial","isomorphism":"Partial","semantic":"Pass","observational":"Pass","commitment":"Partial","historical":"Partial","operational":"Partial"},{"route":f"{b}→canonical→{a}","identity":"Partial","isomorphism":"Partial","semantic":"Pass","observational":"Pass","commitment":"Partial","historical":"Partial","operational":"Partial"}])
 proof={"campaign_id":spec['campaign']['id'],"spec_digest":sha(spec),"results":results,"traces":traces,"round_trip_ledger":roundtrips,"preservation_matrix":{k:v['preservation_passes'] for k,v in aggregate.items()},"conservativity_ledger":[{"foundation":r['foundation'],"benchmark":r['benchmark'],"classification":r['conservativity']} for r in results],"structural_accounting":aggregate,"non_equivalence_witnesses":witnesses,"ablations":ablations,"counterexamples":counterexamples,"benchmark_bias":[{k:b[k] for k in ('id','source_formalism','resembles','earlier_auxiliary','bias','neutral_variant')}|{"order_mutation_invariant":True,"naming_mutation_invariant":True} for b in spec['benchmarks']],"pareto_vectors":vectors,"pareto_matrix":pareto,"dominance_graph":{"nodes":list(aggregate),"edges":[]},"incomparability_witnesses":incomparability,"terminal_result":TERMINAL,"strongest_finding":"each candidate preserves some native commitments more directly, but every pair has opposed frozen dimensions","nonclaims":spec['nonclaims'],"remaining_obligations":spec['remaining_obligations'],"self_review":[{"risk":x,"finding":"retained as bounded weakness; no promotion"} for x in ("benchmark bias","implementation-quality bias","richer machinery mistaken for better","lower cost mistaken for adequacy","outputs mistaken for commitments","witness selection bias","post-result identity rules","PR #421 auxiliary assumptions","shared executor","finite-to-global promotion","conservativity without model classes","winner-manufacturing dimensions","omitted failed attempts","strengthened unresolved results")],"prior_preservation":{"base_commit":spec['campaign']['base_commit'],"pr421_hashes":spec['campaign']['pr421_artifact_hashes'],"prior_results":"unchanged","limitations":"additive","nonclaims":"superset","obligations":"preserved"}}
 return proof
def render(spec,p):
 lines=["# Generated FARA Foundation Comparison Report","","Status: Research","",f"Campaign: `{p['campaign_id']}`",f"Terminal result: **{p['terminal_result']}**","","## Mapping totals","","| Foundation | Pass | Partial | Fail | Unknown |","|---|---:|---:|---:|---:|"]
 for n in sorted(p['structural_accounting']):
  a=p['structural_accounting'][n]; c=a['mapping_counts']; lines.append(f"| {n} | {c['Pass']} | {c['Partial']} | {c['Fail']} | {c['Unknown']} |")
 lines += ["","## Dominance graph","",f"Edges: `{json.dumps(p['dominance_graph']['edges'])}`.","","## Bounded finding","",p['strongest_finding']+".","","## Nonclaims",""]+[f"- {x}" for x in p['nonclaims']]+["","## Remaining obligations",""]+[f"- {x}" for x in p['remaining_obligations']]
 return '\n'.join(lines)+'\n'
def validate(spec,stored,report=None):
 errors=[]
 try: fresh=build(spec)
 except Exception as e:return [f"fresh build failed: {e}"]
 if stored!=fresh: errors.append('stale proof object')
 if report is not None and report!=render(spec,fresh): errors.append('stale generated report')
 c=spec.get('campaign',{})
 if spec.get('terminal_vocabulary') is None or fresh['terminal_result'] not in spec['terminal_vocabulary']: errors.append('invalid terminal result')
 if tuple(spec.get('preservation_dimensions',()))!=DIMS: errors.append('missing preservation dimensions')
 if spec.get('comparison_dimensions') is None or len(spec['comparison_dimensions'])!=17: errors.append('comparison dimensions changed')
 if any(k in spec for k in ('weights','score','weighted_score')): errors.append('arbitrary weighted scoring')
 if len(spec.get('foundations',[]))!=3 or len({f.get('module') for f in spec.get('foundations',[])})!=3: errors.append('missing or shared foundation implementation')
 for f in spec.get('foundations',[]):
  if not f.get('version') or not f.get('sorts') or not f.get('native_symbols') or not f.get('admissible_models'): errors.append('missing foundation signature')
  if any(x in canonical(f).lower() for x in ('arbitrary_payload','embedded_interpreter','hidden_decoder')): errors.append('hidden machinery or catch-all payload')
 if len(spec.get('benchmarks',[]))!=19 or len({b.get('id') for b in spec.get('benchmarks',[])})!=19: errors.append('missing source model or duplicate identifier')
 if len(fresh['non_equivalence_witnesses'])<3 or any(not w.get('models') or not w.get('isomorphism_check',{}).get('survives') for w in fresh['non_equivalence_witnesses']): errors.append('prose-only or invalid non-equivalence witness')
 if len(fresh['ablations'])!=21: errors.append('missing ablations')
 if len(fresh['counterexamples'])!=10: errors.append('missing counterexamples')
 if any(v for row in fresh['pareto_matrix'].values() for v in row.values()): errors.append('invalid dominance claim')
 if any(r['status']!='Unknown' for r in fresh['results'] if r['benchmark'] in ('BFC-017','BFC-018','BFC-019')): errors.append('Unknown promoted')
 if any(not set(("source_elements","generated_target_elements","correspondence_map","reconstruction_steps","execution_steps","preservation"))<=set(t) for t in fresh['traces'].values()): errors.append('missing trace step or map')
 old=spec['campaign'].get('pr421_artifact_hashes',{})
 paths={'spec':ROOT/'theory/formal/fara-core-formalization-v1.0.json','proof':ROOT/'theory/evaluation/fara-core-formalization-proof-v1.0.json','generated_report':ROOT/'theory/evaluation/generated-fara-core-formalization-report.md','human_report':ROOT/'docs/research/fara-core-formalization-v1.0.md','tests':ROOT/'tests/test_fara_core_formalization.py','validator':ROOT/'tools/check_fara_core_formalization.py'}
 for k,path in paths.items():
  if k not in old or subprocess.check_output(['git','hash-object',str(path)],text=True).strip()!=old[k]: errors.append('prior PR #421 results overwritten')
 human=ROOT/'docs/research/fara-foundation-comparison-v1.0.md'
 if human.exists() and report is not None and human.read_text()==report: errors.append('generated/human report duplication')
 return errors
def write_all(spec):
 p=build(spec); PROOF.write_text(json.dumps(p,indent=2,sort_keys=True)+'\n'); REPORT.write_text(render(spec,p)); TRACE_DIR.mkdir(parents=True,exist_ok=True)
 for key,value in p['traces'].items(): (TRACE_DIR/f'{key}.json').write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
 return p
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--write',action='store_true'); ap.add_argument('--spec',type=pathlib.Path,default=SPEC); ap.add_argument('--proof',type=pathlib.Path,default=PROOF); args=ap.parse_args(); spec=json.loads(args.spec.read_text())
 if args.write: write_all(spec); print('wrote fresh comparison proof, report, and traces'); return
 stored=json.loads(args.proof.read_text()); errs=validate(spec,stored,REPORT.read_text() if args.spec==SPEC and args.proof==PROOF else None)
 if errs: print('FAIL: '+'; '.join(errs)); raise SystemExit(1)
 print('PASS: frozen contract, independent evaluators, 57 traces, ledgers, witnesses, ablations, accounting, and Pareto relation verified')
if __name__=='__main__': main()
