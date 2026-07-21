#!/usr/bin/env python3
"""Validate W3.5 candidate ablation, reconstruction, and classification evidence."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/'theory/evaluation/w3-5-candidate-test-contract-v1.0.json'
RESULT=ROOT/'theory/evaluation/w3-5-candidate-test-result-v1.0.json'
REGISTRY=ROOT/'theory/evaluation/universal-structure-candidate-registry.json'
W35=ROOT/'theory/evaluation/w3-5-specificity-and-discovery-gate.json'
EXPECTED={'derivable':6,'replaceable':1,'architecture_dependent':1,'scope_dependent':1,'generic_system_property':3}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(root:Path=ROOT):
    paths=[root/p.relative_to(ROOT) for p in (CONTRACT,RESULT,REGISTRY,W35)]
    for p in paths:
        assert p.is_file(),p
    contract,result,registry,w35=map(load,paths)
    assert contract['contract_id']=='W35-CANDIDATE-CONTRACT-001'
    assert contract['independence']['project_authored'] is True and contract['independence']['blind'] is False
    assert len(contract['candidates'])==12 and contract['nonclaims']
    assert result['artifact_id']=='W35-CANDIDATE-RESULT-001' and result['status']=='complete'
    assert result['contract']['content_sha256']==sha(paths[0])
    assert result['classification_counts']==EXPECTED and len(result['results'])==12
    assert result['aggregate_result']=='no_registered_candidate_indispensable_within_frozen_class'
    assert result['claim_effect']=={'W3.5_resolved':False,'W5_authorized':False,'minimality':'not_established','necessity':'not_established','uniqueness':'not_established','universal_structure':'unresolved'}
    by={x['id']:x for x in result['results']}; assert set(by)=={f'USC-{i:03d}' for i in range(1,13)}
    assert all(x['ablation_status']=='executed_nonindispensable' for x in by.values())
    assert all(x['reconstruction_status']=='executed_reconstructed_or_replaced' for x in by.values())
    rb={x['id']:x for x in registry['candidates']}; assert set(rb)==set(by)
    assert registry['aggregate_result']==result['aggregate_result']
    for cid,item in by.items():
        assert rb[cid]['current_classification']==item['classification']
        assert rb[cid]['evidence_artifact']=='W35-CANDIDATE-RESULT-001'
    current=w35['current_results']; assert current['candidate_invariants']=='complete_no_indispensable_candidate'
    assert w35['w5_authorized'] is False and w35['status']=='in_progress_candidate_complete'
    arts={x['id']:x for x in w35['required_result_artifacts']}; a=arts['W35-CANDIDATE-RESULT']
    assert a['status']=='complete' and a['artifact_id']=='W35-CANDIDATE-RESULT-001' and a['content_sha256']==sha(paths[1])
    for aid in ('W35-COST-RESULT','W35-CLAIM-RESULT','W35-FAILURE-RESULT'): assert arts[aid]['status']=='missing'
    return {'status':'pass','candidates':12,'aggregate_result':result['aggregate_result']}
def main():
    try: report=validate()
    except (AssertionError,OSError,KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:
        print(f'FAR-VAL-CAND-001: {exc}'); return 1
    print('W3.5 candidate tests: PASS (12 candidates; none indispensable; W5 blocked)'); return 0
if __name__=='__main__': raise SystemExit(main())
