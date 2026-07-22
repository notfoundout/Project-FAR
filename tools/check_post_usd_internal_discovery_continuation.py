#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROGRAM=ROOT/'theory/evaluation/post-usd-internal-discovery-continuation-v1.0.json'
QUEUE=ROOT/'theory/evaluation/post-usd-internal-discovery-next-actions-v1.0.json'
RESEARCH=ROOT/'docs/research/post-usd-internal-discovery-continuation-v1.0.md'
AUDIT=ROOT/'docs/audits/post-usd-internal-discovery-continuation-audit.md'
EVC=ROOT/'theory/evaluation/post-w5-usd-next-program-v1.0.json'
W1_FREEZE=ROOT/'theory/evaluation/ikd-w1-candidate-architecture-freeze-v1.0.json'
W2_RESULT=ROOT/'theory/evaluation/ikd-w2-expanded-candidate-competition-v1.0.json'
W3_RESULT=ROOT/'theory/evaluation/ikd-w3-common-factor-v1.0.json'
W4_RESULT=ROOT/'theory/evaluation/ikd-w4-cross-feature-composition-v1.0.json'
W5_RESULT=ROOT/'theory/evaluation/ikd-w5-expanded-invariance-v1.0.json'
W6_RESULT=ROOT/'theory/evaluation/ikd-w6-global-reconstruction-v1.0.json'
W7_RESULT=ROOT/'theory/evaluation/ikd-w7-lower-bounds-v1.0.json'
W8_RESULT=ROOT/'theory/evaluation/ikd-w8-minimal-frontier-v1.0.json'
def load(path:Path)->dict:return json.loads(path.read_text(encoding='utf-8'))
def main()->int:
    for path in (PROGRAM,QUEUE,RESEARCH,AUDIT,EVC): assert path.is_file(),path
    program=load(PROGRAM); queue=load(QUEUE); evc=load(EVC)
    assert program['program_id']=='POST-USD-IKD-001'; assert program['registration_pr']==260
    disposition=program['external_package_disposition']
    for key in ('EVC-W1-EXTERNAL-PROOF-REVIEW','EVC-W2-R3-TECHNICAL-REPLICATION','EVC-W3-R4-ADVERSARIAL-REPLICATION'): assert disposition[key]=='frozen_preserved_execution_deferred'
    assert 'not withdrawn' in disposition['rule']; assert 'No external package is released' in disposition['rule']
    streams=program['workstreams']; assert len(streams)==9; assert [x['sequence'] for x in streams]==list(range(1,10)); assert [x['target_pr'] for x in streams]==list(range(261,270))
    assert streams[0]['id']=='IKD-W1-CANDIDATE-ARCHITECTURES'; assert streams[-1]['id']=='IKD-W9-TERMINAL-ADJUDICATION'
    rules='\n'.join(program['decision_rules']); assert 'Cross-feature conjunctions' in rules; assert 'Equivalent reintroduction' in rules; assert 'External validation remains deferred' in rules
    assert queue['queue_id']=='POST-USD-IKD-QUEUE-001'; assert queue['parent_program']==program['program_id']; assert queue['registration_pr']==260
    next_pr=queue['next_action']['target_pr']; assert next_pr in {261,262,263,264,265,266,267,268,269}
    if next_pr>=262: assert W1_FREEZE.is_file(); assert queue['completed_workstreams'][0]['target_pr']==261
    if next_pr>=263: assert W2_RESULT.is_file(); assert load(W2_RESULT)['status']=='complete_bounded_comparison'; assert queue['completed_workstreams'][1]['target_pr']==262
    if next_pr>=264: assert W3_RESULT.is_file(); assert load(W3_RESULT)['terminal_result']=='one_bounded_nontrivial_common_factor_candidate_supported'
    if next_pr>=265: assert W4_RESULT.is_file(); assert load(W4_RESULT)['terminal_result']=='bounded_cross_feature_compositional_closure_supported_with_explicit_compatibility_conditions'
    if next_pr>=266: assert W5_RESULT.is_file(); assert load(W5_RESULT)['terminal_result']=='bounded_expanded_representation_invariance_supported'
    if next_pr==266:
        result=load(W5_RESULT); assert result['next_decisive_workstream']=='IKD-W6-GLOBAL-RECONSTRUCTION'
        assert queue['next_action']['workstream']=='IKD-W6-GLOBAL-RECONSTRUCTION'
        assert [x['target_pr'] for x in queue['completed_workstreams']]==[261,262,263,264,265]
        assert [x['target_pr'] for x in queue['ordered_followups']]==[267,268,269]
    if next_pr>=267:
        assert W6_RESULT.is_file(); result=load(W6_RESULT)
        assert result['status']=='complete_expanded_registered_reconstruction_search'
        assert result['terminal_result']=='no_strictly_cheaper_non_equivalent_reconstruction_found_in_expanded_registered_search'
    if next_pr==267:
        assert queue['next_action']['workstream']=='IKD-W7-LOWER-BOUNDS'
        assert [x['target_pr'] for x in queue['completed_workstreams']]==[261,262,263,264,265,266]
        assert [x['target_pr'] for x in queue['ordered_followups']]==[268,269]
    if next_pr>=268:
        assert W7_RESULT.is_file(); result=load(W7_RESULT)
        assert result['status']=='complete_conditional_lower_bound_program'
        assert result['terminal_result']=='all_five_rccd_components_have_conditional_lower_bounds_on_defined_class'
    if next_pr==268:
        assert result['next_decisive_workstream']=='IKD-W8-MINIMAL-FRONTIER'
        assert queue['next_action']['workstream']=='IKD-W8-MINIMAL-FRONTIER'
        assert [x['target_pr'] for x in queue['completed_workstreams']]==[261,262,263,264,265,266,267]
        assert [x['target_pr'] for x in queue['ordered_followups']]==[269]
    if next_pr==269:
        assert W8_RESULT.is_file(); result=load(W8_RESULT)
        assert result['status']=='complete_bounded_frontier_recomputation'
        assert result['terminal_result']=='one_nontrivial_common_kernel_on_defined_class_pending_terminal_adjudication'
        assert result['next_decisive_workstream']=='IKD-W9-TERMINAL-ADJUDICATION'
        assert queue['next_action']['workstream']=='IKD-W9-TERMINAL-ADJUDICATION'
        assert [x['target_pr'] for x in queue['completed_workstreams']]==[261,262,263,264,265,266,267,268]
        assert queue['ordered_followups']==[]
    assert any('release EVC-W1 external review package' in item for item in queue['blocked_actions']); assert evc['status']=='registered_unexecuted'
    assert 'External-package hold' in RESEARCH.read_text(encoding='utf-8'); assert 'Separate featurewise success is not treated as compositional closure' in AUDIT.read_text(encoding='utf-8')
    print(f'POST-USD internal discovery continuation: PASS (external execution deferred; PR #{next_pr} authorized)')
    return 0
if __name__=='__main__': raise SystemExit(main())
