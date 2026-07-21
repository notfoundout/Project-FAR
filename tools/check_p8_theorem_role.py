#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/p8-theorem-role-decision-v1.0.md'; REG=ROOT/'theory/evaluation/p8-theorem-role-decision.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; PREMISES=ROOT/'theory/evaluation/thm-target-001-premise-ledger.json'; LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; W3=ROOT/'theory/evaluation/s-core-w3-global-witness-proof.json'; W4=ROOT/'theory/evaluation/s-core-w4-negative-control-proof.json'; GATES=ROOT/'theory/evaluation/research-gates.json'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
    for p in (DOC,REG,TARGET,PREMISES,LEDGER,W3,W4,GATES): assert p.is_file(),p
    text=DOC.read_text(encoding='utf-8')
    for phrase in ('Selected mode: **`split`**','P8-I — Internal evidential-status preservation','P8-E — External process-to-presentation correspondence','Faithful_split','ApplicableFaithful','does not prove a representation theorem'): assert phrase in text
    r=load(REG); assert r['decision_id']=='P8-ROLE-001' and r['selected_mode']=='split'; assert r['w3_proof_registry']==W3.relative_to(ROOT).as_posix(); assert r['w4_proof_registry']==W4.relative_to(ROOT).as_posix(); internal=r['internal_obligation']; assert internal['predicate']=='Pres_8I' and internal['target_direct_axis_embedding_status']=='proved_LEM-SC-014' and internal['target_recovery_status']=='proved_LEM-SC-018' and internal['semantic_and_coherence_status']=='proved_LEM-SC-019_LEM-SC-020' and internal['negative_control_protection_status']=='proved_OBS-SC-010_NC-08_when_applicable' and internal['no_evidential_upgrade'] is True; external=r['external_obligation']; assert external['predicate']=='Corr_8E' and external['not_implied_by_formal_representation'] is True and external['status']=='unproved'; assert r['proof_status']=='internal_preservation_construction_recovery_and_registered_nontriviality_proved_theorem_unproved'; assert r['next_required_artifact'].startswith('Evidence-backed W3.5')
    t=load(TARGET); assert t['p8']['selected_value']=='split' and t['proof_status']=='partial_lemma_progress_only'; family={x['id']:x for x in t['theorem_family']}; assert family['THM-CORE-REP-001']['status']!='proved' and family['THM-P8-CORR-001']['predicate']=='Corr_8E'
    premises=load(PREMISES); assert premises['version']=='1.7' and next(x for x in premises['entries'] if x['id']=='PRM-010')['decision']=='split'
    ledger=load(LEDGER); by={x['id']:x for x in ledger['obligations']}; assert by['LEM-SC-014']['status']=='proved' and by['LEM-SC-018']['status']=='proved' and by['OBS-SC-006']['status']=='refuted' and by['OBS-SC-010']['status']=='obstruction_established'
    w4=load(W4); assert w4['result']['global_nontriviality_status']=='proved_for_registered_control_families_over_S_core'
    gates={x['name']:x for x in load(GATES)['gates']}; assert gates['formal-negative-controls']['status']=='satisfied'; assert gates['scoped-representation-proof']['status']=='not_satisfied'; assert gates['baseline-factorization-resolved']['status']=='satisfied' and gates['baseline-factorization-resolved']['evidence']; assert gates['fara-specificity-resolved']['status']=='not_satisfied'; assert gates['reasoning-contrast-execution']['status']=='not_satisfied'
    print('P8 theorem-role decision: PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
