#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w7-lower-bounds-v1.0.json'
RESEARCH=ROOT/'docs/research/ikd-w7-lower-bounds-v1.0.md'
AUDIT=ROOT/'docs/audits/ikd-w7-lower-bounds-audit.md'
def main()->int:
    for path in (RESULT,RESEARCH,AUDIT): assert path.is_file(),path
    data=json.loads(RESULT.read_text(encoding='utf-8'))
    assert data['result_id']=='IKD-W7-LOWER-BOUNDS-001'
    assert data['status']=='complete_conditional_lower_bound_program'
    assert data['target_pr']==267 and data['kernel_under_test']=='RCCD-001'
    assert data['universality_class']['id']=='C-EFFECTIVE-REASONING-001'
    assert data['preservation_contract']['id']=='P-RCCD-FAITHFUL-001'
    assert data['effective_representation_family']['id']=='E-EFFECTIVE-REP-001'
    bounds=data['lower_bounds']; assert len(bounds)==5
    assert {x['component'] for x in bounds}=={'R1_RECOVERABLE_COMMITMENTS','R2_CONSTRAINED_EVOLUTION','R3_DEPENDENCY_SENSITIVE_REVISION','R4_HISTORICAL_IDENTITY','R5_UNIFORM_BOUNDED_RECOVERY'}
    for bound in bounds:
        assert bound['paired_countermodel']; assert bound['indistinguishable_under_ablation']; assert bound['separating_query']; assert bound['theorem']; assert bound['classification'].startswith('conditionally_necessary')
    assert 'R1 through R5' in data['joint_theorem']
    assert data['terminal_result']=='all_five_rccd_components_have_conditional_lower_bounds_on_defined_class'
    assert data['claim_effect']['rccd_component_necessity_relative_to_C_P_E']=='supported'
    assert data['claim_effect']['global_necessity']=='not_supported'
    assert data['next_decisive_workstream']=='IKD-W8-MINIMAL-FRONTIER'
    nonclaims='\n'.join(data['nonclaims']); assert 'every possible conception of reasoning' in nonclaims; assert 'external validation' in nonclaims
    audit=AUDIT.read_text(encoding='utf-8'); research=RESEARCH.read_text(encoding='utf-8')
    assert 'Anti-circularity controls' in audit; assert 'paired countermodel' in audit
    assert 'For C, P, and E' in research; assert 'bidirectionally reconstructible' in research
    print('IKD-W7 conditional RCCD lower bounds: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
