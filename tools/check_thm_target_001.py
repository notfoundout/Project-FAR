#!/usr/bin/env python3
"""Validate frozen THM-TARGET-001 after W0/W1 partial lemma progress."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/thm-target-001-v1.0.md'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'
PREMISES=ROOT/'theory/evaluation/thm-target-001-premise-ledger.json'; GATES=ROOT/'theory/evaluation/research-gates.json'
CLAIMS=ROOT/'theory/evaluation/central-claim-registry.json'; LEMMA=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'
W0=ROOT/'theory/evaluation/s-core-w0-normalization-proof.json'; W1=ROOT/'theory/evaluation/s-core-w1-direct-axis-proof.json'

def load(path): return json.loads(path.read_text(encoding='utf-8'))

def main()->int:
    for path in (DOC,TARGET,PREMISES,GATES,CLAIMS,LEMMA,W0,W1): assert path.is_file(), path
    text=DOC.read_text(encoding='utf-8')
    for phrase in ('Frozen prospective theorem target and premise boundary','Finite explicit core `S_core`','General extension class `S_IRD`','THM-CORE-REP-001','THM-IMP-001','This artifact does not establish'): assert phrase in text
    target=load(TARGET)
    assert target['theorem_target_id']=='THM-TARGET-001' and target['version']=='1.0'
    assert target['status']=='frozen_unproved' and target['proof_status']=='partial_lemma_progress_only'
    assert target['machine_check_status']=='bounded_executable_reference_only'
    assert target['independent_review_status']=='not_started'
    assert target['w0_proof_registry']==W0.relative_to(ROOT).as_posix()
    assert target['w1_proof_registry']==W1.relative_to(ROOT).as_posix()
    assert set(target['source_classes'])=={'S_core','S_IRD'}
    assert target['target_class']['id']=='A_FARA' and target['target_class']['adds_new_primitive'] is False
    assert target['representation_witness']['tuple']==['E','D','M','iota','kappa']
    assert target['preservation_obligations']==['P1_configuration','P2_commitment','P3_stake_and_alternative','P4_ground_and_justification','P5_admissibility_and_dynamics','P6_consequence','P7_historical_and_path','P8I_internal_evidential_status']
    p8=target['p8']; assert p8['selected_value']=='split' and p8['internal_predicate']=='Pres_8I' and p8['external_predicate']=='Corr_8E'
    program=target['lemma_program']
    assert program=={'id':'SCORE-LEMMA-LEDGER-001','status':'w0_w1_complete_w2_active','total_obligations':37,'construction_obligations':24,'obstruction_obligations':10,'assembly_obligations':3,'proved_obligations':11,'established_obstructions':0,'scope_boundaries_established':1,'refuted_obstructions':2,'open_obligations':23,'completed_waves':['W0','W1'],'active_wave':'W2','active_obligations':['LEM-SC-010','LEM-SC-011','LEM-SC-013','LEM-SC-015','LEM-SC-016']}
    family={x['id']:x for x in target['theorem_family']}
    assert all(x.get('status')!='proved' for x in family.values())
    assert family['THM-CORE-COMMON-001']['blocked_by']==['lemma_ledger_execution']
    assert family['THM-CORE-REP-001']['blocked_by']==['lemma_ledger_execution']
    assert family['THM-IMP-001']['blocked_by']==['obstruction_lemma_execution']
    assert target['next_required_artifact']=='W2 dynamics history revision and self-modification proof-or-obstruction package'
    premises=load(PREMISES); assert premises['version']=='1.4' and premises['proof_progress']['premise_change'] is False and premises['proof_progress']['theorem_status_change'] is False
    lemma=load(LEMMA); summary=lemma['execution_summary']; assert (summary['proved'],summary['scope_boundary_established'],summary['refuted'],summary['open'])==(11,1,2,23)
    assert load(W0)['proof_id']=='SCORE-W0-PROOF-001' and load(W1)['proof_id']=='SCORE-W1-PROOF-001'
    gates={x['name']:x for x in load(GATES)['gates']}
    assert gates['formal-theorem-target']['status']=='satisfied'; assert gates['premise-ledger-and-semantics']['status']=='satisfied'; assert gates['faithful-representation-definition']['status']=='satisfied'
    assert gates['scoped-representation-proof']['status']=='not_satisfied' and gates['scoped-representation-proof']['evidence']==[]
    for claim in load(CLAIMS)['claims']:
        if claim['id'] in {'CLM-EXISTENCE','CLM-UNIVERSALITY','CLM-NECESSITY','CLM-MINIMALITY'}: assert claim['current_status']!='supported'
    print('THM-TARGET-001 validation: PASS (W0/W1 partial lemmas; W2 active; theorem unproved)')
    return 0
if __name__=='__main__': raise SystemExit(main())
