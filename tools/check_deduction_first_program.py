#!/usr/bin/env python3
"""Validate the deduction-first dependency structure after completed W2."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={
'standard':ROOT/'docs/governance/deduction-first-research-standard.md','central':ROOT/'docs/governance/central-research-program.md','roadmap':ROOT/'docs/planning/deduction-first-proof-roadmap.md','arch':ROOT/'docs/planning/architecture-neutral-research-roadmap.md','target':ROOT/'theory/evaluation/thm-target-001.json','premises':ROOT/'theory/evaluation/thm-target-001-premise-ledger.json','faithful':ROOT/'theory/evaluation/faithful-representation-specification-v1.0.json','p8':ROOT/'theory/evaluation/p8-theorem-role-decision.json','ledger':ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json','w0':ROOT/'theory/evaluation/s-core-w0-normalization-proof.json','w1':ROOT/'theory/evaluation/s-core-w1-direct-axis-proof.json','w2':ROOT/'theory/evaluation/s-core-w2-dynamics-history-proof.json','gates':ROOT/'theory/evaluation/research-gates.json','claims':ROOT/'theory/evaluation/central-claim-registry.json','make':ROOT/'Makefile'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
    for p in FILES.values(): assert p.is_file(),p
    standard=FILES['standard'].read_text(encoding='utf-8'); assert 'The primary route to an answer is therefore deductive' in standard; assert 'It is not required before attempting a mathematical proof' in standard
    central=FILES['central'].read_text(encoding='utf-8'); assert 'SCORE-LEMMA-LEDGER-001' in central and 'W3' in central
    roadmap=FILES['roadmap'].read_text(encoding='utf-8'); assert 'Stage D4 — Construction and obstruction lemmas' in roadmap and 'W3' in roadmap
    arch=FILES['arch'].read_text(encoding='utf-8'); assert 'Milestone 8 — Construction and obstruction lemmas' in arch and 'W3' in arch
    target=load(FILES['target']); assert target['status']=='frozen_unproved'; assert target['proof_status']=='partial_lemma_progress_only'; assert target['next_required_artifact'].startswith('W3 global witness')
    program=target['lemma_program']; assert program['status']=='w0_w1_w2_complete_w3_active'; assert program['proved_obligations']==16; assert program['scope_boundaries_established']==1; assert program['refuted_obstruction_hypotheses']==4; assert program['open_obligations']==16; assert program['completed_waves']==['W0','W1','W2']; assert set(program['active_obligations'])=={f'LEM-SC-{i:03d}' for i in range(17,25)}
    premises=load(FILES['premises']); assert premises['version']=='1.5'; assert premises['proof_progress']['premise_change'] is False; assert premises['proof_progress']['theorem_status_change'] is False
    faithful=load(FILES['faithful']); assert faithful['direct_axis_construction_status']=='proved_without_global_recovery'; assert faithful['dynamics_history_construction_status']=='proved_without_global_recovery'; assert faithful['recovery_contract']['proof_status']=='unproved_LEM-SC-018'
    p8=load(FILES['p8']); assert p8['selected_mode']=='split'; assert p8['internal_construction_status']=='direct_axis_embedding_proved_recovery_unproved'; assert p8['external_obligation']['not_implied_by_formal_representation'] is True
    ledger=load(FILES['ledger']); assert ledger['status']=='frozen_dependency_decomposition_w0_w1_w2_complete_w3_active'; summary=ledger['execution_summary']; assert (summary['proved'],summary['scope_boundary_established'],summary['refuted'],summary['open'])==(16,1,4,16)
    by_id={x['id']:x for x in ledger['obligations']}; assert all(by_id[f'LEM-SC-{i:03d}']['status']=='proved' for i in range(1,17)); assert by_id['OBS-SC-001']['status']=='scope_boundary_established'; assert all(by_id[x]['status']=='refuted' for x in ('OBS-SC-003','OBS-SC-004','OBS-SC-005','OBS-SC-006'))
    assert load(FILES['w0'])['proof_id']=='SCORE-W0-PROOF-001'; assert load(FILES['w1'])['proof_id']=='SCORE-W1-PROOF-001'; assert load(FILES['w2'])['proof_id']=='SCORE-W2-PROOF-001'
    gates=load(FILES['gates']); required=set(gates['required_canonical_artifacts']); assert FILES['w1'].relative_to(ROOT).as_posix() in required and FILES['w2'].relative_to(ROOT).as_posix() in required; by_name={x['name']:x for x in gates['gates']}; assert by_name['scoped-representation-proof']['status']=='not_satisfied'; assert by_name['mechanized-proof-verification']['status']=='not_satisfied'; assert by_name['independent-proof-review']['status']=='not_satisfied'
    for claim in load(FILES['claims'])['claims']:
        if claim['id'] in {'CLM-EXISTENCE','CLM-UNIVERSALITY','CLM-NECESSITY','CLM-MINIMALITY'}: assert claim['current_status']!='supported'
    make=FILES['make'].read_text(encoding='utf-8')
    for checker in ('check_faithful_representation.py','check_p8_theorem_role.py','check_s_core_lemma_ledger.py','check_s_core_w0.py','check_s_core_w1.py','check_s_core_w2.py'): assert make.count(f'python tools/{checker}')==3
    print('Deduction-first research program: PASS (W0-W2 complete; W3 active; theorem gate closed)')
    return 0
if __name__=='__main__': raise SystemExit(main())
