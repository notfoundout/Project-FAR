#!/usr/bin/env python3
"""Validate frozen THM-TARGET-001 after W0-W2 partial lemma progress."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/thm-target-001-v1.0.md'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'
PREMISES=ROOT/'theory/evaluation/thm-target-001-premise-ledger.json'; GATES=ROOT/'theory/evaluation/research-gates.json'
CLAIMS=ROOT/'theory/evaluation/central-claim-registry.json'; LEMMA=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'
W0=ROOT/'theory/evaluation/s-core-w0-normalization-proof.json'; W1=ROOT/'theory/evaluation/s-core-w1-direct-axis-proof.json'; W2=ROOT/'theory/evaluation/s-core-w2-dynamics-history-proof.json'

def load(path): return json.loads(path.read_text(encoding='utf-8'))

def main()->int:
    for path in (DOC,TARGET,PREMISES,GATES,CLAIMS,LEMMA,W0,W1,W2): assert path.is_file(), path
    text=DOC.read_text(encoding='utf-8')
    for phrase in ('Frozen prospective theorem target and premise boundary','Finite explicit core `S_core`','General extension class `S_IRD`','THM-CORE-REP-001','THM-IMP-001','This artifact does not establish'): assert phrase in text
    target=load(TARGET)
    assert target['theorem_target_id']=='THM-TARGET-001' and target['version']=='1.0'
    assert target['status']=='frozen_unproved' and target['proof_status']=='partial_lemma_progress_only'
    assert target['machine_check_status']=='bounded_executable_reference_only' and target['independent_review_status']=='not_started'
    assert target['w0_proof_registry']==W0.relative_to(ROOT).as_posix()
    assert target['w1_proof_registry']==W1.relative_to(ROOT).as_posix()
    assert target['w2_proof_registry']==W2.relative_to(ROOT).as_posix()
    assert set(target['source_classes'])=={'S_core','S_IRD'}
    assert target['target_class']['id']=='A_FARA' and target['target_class']['adds_new_primitive'] is False
    assert target['representation_witness']['tuple']==['E','D','M','iota','kappa']
    assert target['preservation_obligations']==['P1_configuration','P2_commitment','P3_stake_and_alternative','P4_ground_and_justification','P5_admissibility_and_dynamics','P6_consequence','P7_historical_and_path','P8I_internal_evidential_status']
    p8=target['p8']; assert p8['selected_value']=='split' and p8['internal_predicate']=='Pres_8I' and p8['external_predicate']=='Corr_8E'
    program=target['lemma_program']
    assert program['id']=='SCORE-LEMMA-LEDGER-001' and program['status']=='w0_w1_w2_complete_w3_active'
    assert (program['total_obligations'],program['proved_obligations'],program['refuted_obstruction_hypotheses'],program['scope_boundaries_established'],program['open_obligations'])==(37,16,4,1,16)
    assert program['completed_waves']==['W0','W1','W2'] and program['active_wave']=='W3'
    assert set(program['active_obligations'])=={f'LEM-SC-{i:03d}' for i in range(17,25)}
    family={x['id']:x for x in target['theorem_family']}
    assert all(x.get('status')!='proved' for x in family.values())
    assert family['THM-CORE-COMMON-001']['blocked_by']==['lemma_ledger_execution']
    assert family['THM-CORE-REP-001']['blocked_by']==['lemma_ledger_execution']
    assert family['THM-IMP-001']['blocked_by']==['obstruction_lemma_execution']
    assert target['next_required_artifact'].startswith('W3 global witness')
    premises=load(PREMISES); assert premises['version']=='1.5'
    progress=premises['proof_progress']; assert progress['premise_change'] is False and progress['source_scope_change'] is False and progress['target_interface_change'] is False and progress['theorem_status_change'] is False
    lemma=load(LEMMA); summary=lemma['execution_summary']; assert (summary['proved'],summary['scope_boundary_established'],summary['refuted'],summary['open'])==(16,1,4,16)
    assert load(W0)['proof_id']=='SCORE-W0-PROOF-001' and load(W1)['proof_id']=='SCORE-W1-PROOF-001' and load(W2)['proof_id']=='SCORE-W2-PROOF-001'
    gates={x['name']:x for x in load(GATES)['gates']}
    assert gates['formal-theorem-target']['status']=='satisfied'; assert gates['premise-ledger-and-semantics']['status']=='satisfied'; assert gates['faithful-representation-definition']['status']=='satisfied'
    assert gates['scoped-representation-proof']['status']=='not_satisfied' and gates['scoped-representation-proof']['evidence']==[]
    for claim in load(CLAIMS)['claims']:
        if claim['id'] in {'CLM-EXISTENCE','CLM-UNIVERSALITY','CLM-NECESSITY','CLM-MINIMALITY'}: assert claim['current_status']!='supported'
    print('THM-TARGET-001 validation: PASS (W0-W2 partial lemmas; W3 active; theorem unproved)')
    return 0
if __name__=='__main__': raise SystemExit(main())
