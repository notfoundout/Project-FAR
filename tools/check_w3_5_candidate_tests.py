#!/usr/bin/env python3
"""Validate the corrected W3.5 candidate-adjudication boundary."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/'theory/evaluation/w3-5-candidate-test-contract-v1.0.json'
RESULT=ROOT/'theory/evaluation/w3-5-candidate-test-result-v1.0.json'
REGISTRY=ROOT/'theory/evaluation/universal-structure-candidate-registry.json'
W35=ROOT/'theory/evaluation/w3-5-specificity-and-discovery-gate.json'
AXES={'primitive_necessity','explicit_representation_necessity','structural_commitment_necessity','reasoning_specificity','architecture_invariance'}
OUTCOMES={'supported_at_registered_scope','refuted_at_registered_scope','partial','unresolved'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(condition,message):
    if not condition: raise ValueError(message)
def validate(root:Path=ROOT):
    paths=[root/p.relative_to(ROOT) for p in (CONTRACT,RESULT,REGISTRY,W35)]
    for p in paths: require(p.is_file(),f'missing {p}')
    contract,result,registry,w35=map(load,paths)
    require(contract['contract_id']=='W35-CANDIDATE-CONTRACT-001','wrong contract id')
    require(set(contract['hypothesis_axes'])==AXES,'necessity axes changed')
    require(contract['method']['unit_of_analysis']=='candidate x corpus_case x representation_layer','wrong unit')
    require('registered_terminal_classification' not in json.dumps(contract),'contract freezes answers')
    require(result['artifact_id']=='W35-CANDIDATE-RESULT-001','wrong result id')
    require(result['contract']['content_sha256']==sha(paths[0]),'contract digest mismatch')
    require(result['status']=='preliminary_internal_adjudication_reexecution_required','unsupported completion status')
    require(result['execution']['expected_atomic_trials']==648,'wrong expected trial count')
    require(result['execution']['preserved_atomic_trials']==0,'summary records misreported as trials')
    require(not any(result['execution'][k] for k in ('ablation_evidence_complete','reconstruction_evidence_complete','equivalent_reintroduction_evidence_complete','machinery_cost_complete')),'missing evidence marked complete')
    by={x['id']:x for x in result['results']}
    require(set(by)==set(contract['candidate_ids'])=={f'USC-{i:03d}' for i in range(1,13)},'candidate set mismatch')
    for item in by.values():
        require(all(item[a] in OUTCOMES for a in AXES),'invalid axis outcome')
        require(item['structural_commitment_necessity']=='unresolved','structural necessity promoted without trials')
        require(item['trial_evidence_status']=='missing','missing trials hidden')
        require(item['machinery_cost_status']=='not_executed','cost status inflated')
    derived={o:sum(x['structural_commitment_necessity']==o for x in by.values()) for o in sorted(OUTCOMES)}
    require(result['axis_counts']['structural_commitment_necessity']==derived,'axis counts not derived')
    require(result['aggregate_result']=='candidate_structural_indispensability_unresolved_reexecution_required','aggregate overclaim')
    rb={x['id']:x for x in registry['candidates']}
    require(set(rb)==set(by),'registry candidate mismatch')
    require(registry['aggregate_result']==result['aggregate_result'],'registry aggregate mismatch')
    require(registry['result_artifact']['content_sha256']==sha(paths[1]),'registry result digest mismatch')
    for cid,item in by.items():
        require(rb[cid]['structural_commitment_necessity']==item['structural_commitment_necessity'],'registry axis disagreement')
        require(rb[cid]['trial_evidence_status']==item['trial_evidence_status'],'registry evidence disagreement')
    current=w35['current_results']
    require(current['candidate_invariants']=='not_executed','gate candidate status inflated')
    require(w35['w5_authorized'] is False and w35['status']=='in_progress_specificity_complete','W5/gate status invalid')
    arts={x['id']:x for x in w35['required_result_artifacts']}; a=arts['W35-CANDIDATE-RESULT']
    require(a['status']=='missing' and a['artifact_id'] is None and a['content_sha256'] is None,'preliminary observation promoted into gate evidence')
    return {'status':'pass','candidates':12,'aggregate_result':result['aggregate_result'],'atomic_trials_preserved':0}
def main():
    try: report=validate()
    except (OSError,KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:
        print(f'FAR-VAL-CAND-001: {exc}'); return 1
    print('W3.5 candidate boundary: PASS (preliminary observation only; 648 atomic trials required; W5 blocked)'); return 0
if __name__=='__main__': raise SystemExit(main())
