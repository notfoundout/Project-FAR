from __future__ import annotations
import importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/'theory/contract/upp-faithfulness-contract-v1.0.json'
RESULT=ROOT/'theory/evaluation/upp-w3-contract-result-v1.0.json'
QUEUE=ROOT/'theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json'
MODEL=ROOT/'theory/contract/upp_faithfulness_contract_v1.py'
EXPECTED={'structural_fidelity','semantic_fidelity','operational_fidelity','dependency_fidelity','information_fidelity','historical_fidelity','query_totality_on_registered_questions','error_and_unknown_separation'}
KINDS={'definitional','logical','computational','normative','empirical','methodological'}
FORBIDDEN=('rccd','recoverable commitments','constrained evolution','dependency-sensitive revision','historical identity','uniform effective recovery','universal kernel')
def fail(x): raise SystemExit('FAIL: '+x)
def load(p): return json.loads(p.read_text())
def main():
 s,r,q=load(SPEC),load(RESULT),load(QUEUE)
 sp=importlib.util.spec_from_file_location('upp_contract',MODEL); m=importlib.util.module_from_spec(sp); sys.modules[sp.name]=m; sp.loader.exec_module(m)
 if s.get('workstream')!='UPP-W3-CONTRACT': fail('wrong workstream')
 clauses=s.get('clauses',[]); ids={x['id'] for x in clauses}
 if ids!=EXPECTED or len(clauses)!=8: fail('clause set changed')
 if {x.value for x in m.ClauseId}!=EXPECTED: fail('model/spec clause mismatch')
 if {x.value for x in m.AssumptionKind}!=KINDS: fail('assumption kinds mismatch')
 if {x['kind'] for x in s.get('assumptions',[])}!=KINDS: fail('all assumption kinds must be visible')
 clause_text=' '.join(x['id']+' '+x['question'] for x in clauses).casefold()
 if any(t in clause_text for t in FORBIDDEN): fail('conclusion vocabulary leaked into clauses')
 if len(s.get('clause_independence_witnesses',[]))!=8: fail('missing independence witnesses')
 controls=s.get('independence_controls',{})
 if not controls or not all(controls.values()): fail('independence control disabled')
 if s['aggregation']!={'rule':'fail_if_any_fail_unknown_if_none_fail_and_any_unknown_pass_only_if_all_pass','unknown_is_not_partial':True,'pass_requires_positive_evidence':True}: fail('aggregation changed')
 if r.get('status')!='complete' or r.get('unknowns_promoted') is not False: fail('result invalid')
 completed={x['target_pr']:x for x in q.get('completed_workstreams',[])}
 if completed.get(284,{}).get('result')!=r.get('result'): fail('queue missing completed W3')
 if q.get('next_action')!={'target_pr':285,'workstream':'UPP-W4-REPRESENTATIONS'}: fail('wrong next action')
 if q.get('ordered_followups')!=list(range(286,297)): fail('followups changed')
 if q.get('public_evaluation_authorized') is not False: fail('release gate opened')
 print('PASS: UPP-W3 contract is independent, assumption-visible, and queue-consistent'); return 0
if __name__=='__main__': raise SystemExit(main())
