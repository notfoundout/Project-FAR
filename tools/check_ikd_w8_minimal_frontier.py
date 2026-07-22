#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w8-minimal-frontier-v1.0.json'
RESEARCH=ROOT/'docs/research/ikd-w8-minimal-frontier-v1.0.md'
AUDIT=ROOT/'docs/audits/ikd-w8-minimal-frontier-audit.md'
W7=ROOT/'theory/evaluation/ikd-w7-lower-bounds-v1.0.json'
def load(path:Path)->dict:return json.loads(path.read_text(encoding='utf-8'))
def main()->int:
    for path in (RESULT,RESEARCH,AUDIT,W7): assert path.is_file(),path
    data=load(RESULT); w7=load(W7)
    assert data['result_id']=='IKD-W8-MINIMAL-FRONTIER-001'
    assert data['status']=='complete_bounded_frontier_recomputation'
    assert data['target_pr']==268
    assert data['comparison_rule']=='componentwise_commitment_and_pareto_only_no_scalar_score'
    assert w7['terminal_result']=='all_five_rccd_components_have_conditional_lower_bounds_on_defined_class'
    assert set(data['architectures'])=={'RCCD-001','FARA-001','LTS-PROV-001','COALG-DYN-001'}
    rows=data['bidirectional_reconstructions']; assert len(rows)==3
    assert {x['architecture'] for x in rows}=={'FARA-001','LTS-PROV-001','COALG-DYN-001'}
    for row in rows:
        assert row['from_rccd']; assert row['to_rccd']; assert row['hidden_machinery_charged']
        assert row['classification']=='rccd_equivalent_realization'
    classes=data['commitment_equivalence_classes']; assert len(classes)==1
    c=classes[0]; assert c['id']=='CEC-RCCD-001'
    assert set(c['members'])=={'RCCD-001','FARA-001','LTS-PROV-001','COALG-DYN-001'}
    assert len(c['shared_necessary_commitments'])==5
    assert data['additional_essential_commitment_search']['result']=='none_required_across_all_successful_architectures'
    assert data['rccd_reducibility']['result']=='not_reducible_under_registered_contract'
    assert data['incomparable_kernel_search']['result']=='no_surviving_incomparable_kernel_in_registered_successful_set'
    assert data['pareto_frontier']['kernel_level']==['CEC-RCCD-001']
    assert set(data['pareto_frontier']['realization_level'])=={'FARA-001','LTS-PROV-001','COALG-DYN-001'}
    assert data['terminal_result']=='one_nontrivial_common_kernel_on_defined_class_pending_terminal_adjudication'
    assert data['next_decisive_workstream']=='IKD-W9-TERMINAL-ADJUDICATION'
    nonclaims='\n'.join(data['nonclaims']); assert 'unrestricted universality' in nonclaims; assert 'external validation' in nonclaims
    audit=AUDIT.read_text(encoding='utf-8'); assert 'no scalar score' in audit; assert 'Bidirectional reconstruction is required' in audit
    print('IKD-W8 minimal frontier: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
