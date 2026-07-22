#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROGRAM=ROOT/'theory/evaluation/post-w9-internal-scope-challenge-v1.0.json'
QUEUE=ROOT/'theory/evaluation/post-w9-internal-scope-challenge-queue-v1.0.json'
DOC=ROOT/'docs/research/post-w9-internal-scope-challenge-v1.0.md'
W2=ROOT/'theory/evaluation/sc-w2-boundary-reasoning-v1.0.json'
W3=ROOT/'theory/evaluation/sc-w3-contract-ladder-v1.0.json'
W4=ROOT/'theory/evaluation/sc-w4-representation-escape-v1.0.json'
def load(path:Path)->dict:return json.loads(path.read_text(encoding='utf-8'))
def main()->int:
    for path in (PROGRAM,QUEUE,DOC): assert path.is_file(),path
    program=load(PROGRAM); queue=load(QUEUE)
    assert program['program_id']=='POST-W9-SCOPE-CHALLENGE-001'
    assert program['status']=='registered_unexecuted'
    assert program['external_disposition']=='deferred_until_final_internal_adjudication'
    assert len(program['workstreams'])==6
    assert [x['sequence'] for x in program['workstreams']]==list(range(1,7))
    assert [x['target_pr'] for x in program['workstreams']]==list(range(270,276))
    assert len(program['terminal_outcomes'])==6
    assert 'current_theorem_scope_construct_loaded' in program['terminal_outcomes']
    assert len(program['downgrade_rules'])==6
    assert queue['queue_id']=='POST-W9-SCOPE-CHALLENGE-QUEUE-001'
    next_pr=queue['next_action']['target_pr']; assert next_pr in {270,271,272,273,274,275}
    expected={270:'SC-W1-SCOPE-NEUTRALITY',271:'SC-W2-BOUNDARY-REASONING',272:'SC-W3-CONTRACT-LADDER',273:'SC-W4-REPRESENTATION-ESCAPE',274:'SC-W5-HELD-OUT-CONTEXTS',275:'SC-W6-FINAL-INTERNAL-ADJUDICATION'}
    assert queue['next_action']['workstream']==expected[next_pr]
    if next_pr==270:
        assert queue['ordered_followups']==[271,272,273,274,275]
    if next_pr==272:
        assert W2.is_file(); result=load(W2)
        assert result['status']=='complete_internal_boundary_adjudication'
        assert result['terminal_result']=='no_boundary_case_yet_requires_new_kernel_primitive_but_evidential_boundary_must_remain_open'
        assert [x['target_pr'] for x in queue['completed_workstreams']]==[270,271]
        assert queue['ordered_followups']==[273,274,275]
    if next_pr==273:
        assert W2.is_file(); boundary=load(W2)
        assert boundary['status']=='complete_internal_boundary_adjudication'
        assert boundary['terminal_result']=='no_boundary_case_yet_requires_new_kernel_primitive_but_evidential_boundary_must_remain_open'
        assert W3.is_file(); contract=load(W3)
        assert contract['status']=='complete_internal_contract_ladder'
        assert contract['terminal_result']=='rccd_is_contract_relative_but_not_shown_construct_loaded_under_independently_justified_full_contract'
        assert contract['next_decisive_workstream']=='SC-W4-REPRESENTATION-ESCAPE'
        assert [x['target_pr'] for x in queue['completed_workstreams']]==[270,271,272]
        assert queue['ordered_followups']==[274,275]
    if next_pr>=274:
        assert W2.is_file(); boundary=load(W2)
        assert boundary['status']=='complete_internal_boundary_adjudication'
        assert boundary['terminal_result']=='no_boundary_case_yet_requires_new_kernel_primitive_but_evidential_boundary_must_remain_open'
        assert W3.is_file(); contract=load(W3)
        assert contract['status']=='complete_internal_contract_ladder'
        assert contract['terminal_result']=='rccd_is_contract_relative_but_not_shown_construct_loaded_under_independently_justified_full_contract'
        assert W4.is_file(); escape=load(W4)
        assert escape['status']=='complete_internal_representation_escape_search'
        assert escape['terminal_result']=='no_faithful_effective_representation_escape_found_across_broadened_families_without_rccd_equivalent_reintroduction'
        assert escape['next_decisive_workstream']=='SC-W5-HELD-OUT-CONTEXTS'
        assert [x['target_pr'] for x in queue['completed_workstreams']]==[270,271,272,273]
        assert queue['ordered_followups']==[275]
    text=DOC.read_text(encoding='utf-8')
    assert 'External hold' in text
    assert 'construct-loaded' in text
    print(f'POST-W9 internal scope challenge: PASS (PR #{next_pr} authorized; external work deferred)')
    return 0
if __name__=='__main__': raise SystemExit(main())
