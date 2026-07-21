#!/usr/bin/env python3
"""Validate evidence-complete W3.5 candidate ablation and reconstruction."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from w3_5_candidate_execution import AXES,CANDIDATES,CASES,LAYERS,derive,execute

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/'theory/evaluation/w3-5-candidate-test-contract-v1.0.json'
EXECUTION=ROOT/'tools/w3_5_candidate_execution.py'
RESULT=ROOT/'theory/evaluation/w3-5-candidate-test-result-v1.0.json'
REGISTRY=ROOT/'theory/evaluation/universal-structure-candidate-registry.json'
W35=ROOT/'theory/evaluation/w3-5-specificity-and-discovery-gate.json'
OUTCOMES={'supported_at_registered_scope','refuted_at_registered_scope','partial','unresolved'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok: raise ValueError(msg)
def validate(root:Path=ROOT):
    paths={k:root/p.relative_to(ROOT) for k,p in {'contract':CONTRACT,'execution':EXECUTION,'result':RESULT,'registry':REGISTRY,'w35':W35}.items()}
    for p in paths.values(): require(p.is_file(),f'missing {p.relative_to(root)}')
    contract,result,registry,w35=(load(paths[k]) for k in ('contract','result','registry','w35'))
    require(contract['contract_id']=='W35-CANDIDATE-CONTRACT-001','wrong contract id')
    require(set(contract['hypothesis_axes'])==set(AXES),'axis set changed')
    require('registered_terminal_classification' not in json.dumps(contract),'contract freezes candidate answers')
    trials=execute()
    require(len(trials)==648,'atomic trial count must be 648')
    require(len({t['trial_id'] for t in trials})==648,'duplicate trial ids')
    expected={(cid,case,layer) for cid,_,_ in CANDIDATES for case,_,_ in CASES for layer in LAYERS}
    actual={(t['candidate_id'],t['case_id'],t['representation_layer']) for t in trials}
    require(actual==expected,'candidate-case-layer coverage incomplete')
    required=set(contract['required_trial_fields'])
    for t in trials:
        require(required<=set(t),f"{t['trial_id']} missing required fields")
        require(t['ablation_operation']['label_only_removal'] is False,'label-only ablation')
        require(t['ablation_operation']['dependent_values_recomputed'] is True,'dependent values not recomputed')
        require(set(t['preservation_after_ablation'])=={'structural','semantic','operational','dependency','information','historical'},'preservation vector incomplete')
        require(t['machinery_cost']['total_units']>=0,'negative machinery cost')
        if t['equivalent_commitment_reintroduced']:
            require(t['reconstruction_attempt']['status']=='successful_equivalent_reconstruction','equivalent reintroduction lacks reconstruction')
            require(t['equivalence_comparison']['verdict']=='commitment_equivalent','equivalent reintroduction lacks equivalence')
    generated={x['id']:x for x in derive(trials)}
    recorded={x['id']:x for x in result['results']}
    require(set(generated)==set(recorded)==set(contract['candidate_ids']),'candidate set mismatch')
    for cid,g in generated.items():
        r=recorded[cid]
        for axis in AXES: require(r[axis]==g[axis],f'{cid} {axis} not derived')
        require(r['trial_count']==54 and r['trial_evidence_status']=='complete' and r['machinery_cost_status']=='complete',f'{cid} incomplete')
    counts={axis:{o:sum(r[axis]==o for r in recorded.values()) for o in sorted(OUTCOMES)} for axis in AXES}
    require(result['axis_counts']==counts,'axis counts not derived')
    require(result['contract']['content_sha256']==sha(paths['contract']),'contract digest mismatch')
    require(result['trial_artifact']['content_sha256']==sha(paths['execution']),'execution digest mismatch')
    require(result['trial_artifact']['materialized_atomic_trials']==648,'materialized count mismatch')
    require(result['execution']=={'expected_atomic_trials':648,'preserved_atomic_trials':648,'ablation_evidence_complete':True,'reconstruction_evidence_complete':True,'equivalent_reintroduction_evidence_complete':True,'machinery_cost_complete':True},'execution completeness invalid')
    require(result['aggregate_result']=='registered_candidate_axes_resolved_at_frozen_internal_scope','aggregate invalid')
    require(result['claim_effect']['W5_authorized'] is False and result['claim_effect']['universal_structure']=='unresolved','historical candidate claim boundary violated')
    rb={x['id']:x for x in registry['candidates']}
    require(set(rb)==set(recorded),'registry mismatch')
    require(registry['result_artifact']['content_sha256']==sha(paths['result']),'registry result digest mismatch')
    require(registry['trial_artifact']['content_sha256']==sha(paths['execution']),'registry execution digest mismatch')
    for cid,r in recorded.items():
        for axis in AXES: require(rb[cid][axis]==r[axis],f'{cid} registry mismatch')
    current=w35['current_results']; resolved=w35['status']=='resolved'
    expected_candidate='complete' if resolved else 'complete_registered_scope_internal_execution'
    require(current['candidate_invariants']==expected_candidate,'gate candidate state invalid')
    require(w35['status'] in {'in_progress_candidate_complete','resolved'} and w35['w5_authorized'] is resolved,'gate/W5 state invalid')
    artifact={x['id']:x for x in w35['required_result_artifacts']}['W35-CANDIDATE-RESULT']
    require(artifact['status']=='complete' and artifact['artifact_id']=='W35-CANDIDATE-RESULT-001','candidate result not complete')
    require(artifact['content_sha256']==sha(paths['result']),'gate digest mismatch')
    return {'status':'pass','atomic_trials':648,'candidates':12,'axis_counts':counts,'aggregate_result':result['aggregate_result'],'w5_authorized':w35['w5_authorized']}
def main():
    try: report=validate()
    except (OSError,KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:
        print(f'FAR-VAL-CAND-001: {exc}'); return 1
    print(f"W3.5 candidate execution: PASS (648 atomic trials; five axes mechanically derived; W5 authorized={report['w5_authorized']})"); return 0
if __name__=='__main__': raise SystemExit(main())
