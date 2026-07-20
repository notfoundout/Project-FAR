#!/usr/bin/env python3
"""Validate P8-ROLE-001 after W2 while preserving the split boundary."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/p8-theorem-role-decision-v1.0.md'; REG=ROOT/'theory/evaluation/p8-theorem-role-decision.json'
TARGET=ROOT/'theory/evaluation/thm-target-001.json'; PREMISES=ROOT/'theory/evaluation/thm-target-001-premise-ledger.json'
LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; W1=ROOT/'theory/evaluation/s-core-w1-direct-axis-proof.json'; W2=ROOT/'theory/evaluation/s-core-w2-dynamics-history-proof.json'; GATES=ROOT/'theory/evaluation/research-gates.json'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
    for p in (DOC,REG,TARGET,PREMISES,LEDGER,W1,W2,GATES): assert p.is_file(),p
    text=DOC.read_text(encoding='utf-8')
    for phrase in ('Selected mode: **`split`**','P8-I — Internal evidential-status preservation','P8-E — External process-to-presentation correspondence','Faithful_split','ApplicableFaithful','does not prove a representation theorem'): assert phrase in text
    reg=load(REG)
    assert reg['decision_id']=='P8-ROLE-001' and reg['selected_mode']=='split'
    assert reg['status']=='frozen_partial_internal_construction_only'
    assert reg['internal_construction_status']=='direct_axis_embedding_proved_recovery_unproved'
    internal=reg['internal_obligation']; assert internal['predicate']=='Pres_8I'; assert internal['source_reduct_extraction_status']=='proved_LEM-SC-002'; assert internal['target_direct_axis_embedding_status']=='proved_LEM-SC-014'; assert internal['registered_impossibility_status']=='OBS-SC-006_refuted_for_finite_direct_axis_reducts'; assert internal['no_evidential_upgrade'] is True
    external=reg['external_obligation']; assert external['predicate']=='Corr_8E'; assert external['not_implied_by_formal_representation'] is True; assert external['status']=='unproved'
    assert reg['w1_direct_axis_proof_registry']==W1.relative_to(ROOT).as_posix()
    assert reg['w2_dynamics_history_proof_registry']==W2.relative_to(ROOT).as_posix()
    assert reg['proof_status']=='partial_internal_direct_axis_lemma_only'; assert reg['machine_check_status']=='bounded_executable_reference_only'; assert reg['independent_review_status']=='not_started'
    assert reg['next_required_artifact'].startswith('W3 global witness')
    target=load(TARGET); p8=target['p8']; assert p8['selected_value']=='split'; assert p8['internal_direct_axis_embedding_status']=='proved_recovery_unproved'; assert target['proof_status']=='partial_lemma_progress_only'
    family={x['id']:x for x in target['theorem_family']}; assert family['THM-CORE-REP-001']['blocked_by']==['lemma_ledger_execution']; assert family['THM-P8-CORR-001']['predicate']=='Corr_8E'
    premises=load(PREMISES); assert premises['version']=='1.5'; assert next(x for x in premises['entries'] if x['id']=='PRM-010')['decision']=='split'
    ledger=load(LEDGER); by_id={x['id']:x for x in ledger['obligations']}; assert by_id['LEM-SC-014']['status']=='proved'; assert by_id['OBS-SC-006']['status']=='refuted'; assert ledger['execution_summary']['open']==16 and ledger['active_wave']=='W3'
    w1=load(W1); assert next(x for x in w1['results'] if x['id']=='LEM-SC-014')['status']=='proved'; assert next(x for x in w1['results'] if x['id']=='OBS-SC-006')['status']=='refuted'
    assert load(W2)['proof_id']=='SCORE-W2-PROOF-001'
    required=set(load(GATES)['required_canonical_artifacts']); assert W1.relative_to(ROOT).as_posix() in required and W2.relative_to(ROOT).as_posix() in required
    gates={x['name']:x for x in load(GATES)['gates']}; assert gates['scoped-representation-proof']['status']=='not_satisfied'
    print('P8 theorem-role decision: PASS (P8-I direct embedding proved; recovery and Corr_8E unproved; W3 active)')
    return 0
if __name__=='__main__': raise SystemExit(main())
