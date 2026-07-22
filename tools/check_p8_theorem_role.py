#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/p8-theorem-role-decision-v1.0.md'; REG=ROOT/'theory/evaluation/p8-theorem-role-decision.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; PREMISES=ROOT/'theory/evaluation/thm-target-001-premise-ledger.json'; LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; W3=ROOT/'theory/evaluation/s-core-w3-global-witness-proof.json'; W4=ROOT/'theory/evaluation/s-core-w4-negative-control-proof.json'; W5=ROOT/'theory/evaluation/s-core-w5-theorem-assembly-proof.json'; GATES=ROOT/'theory/evaluation/research-gates.json'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
 for p in (DOC,REG,TARGET,PREMISES,LEDGER,W3,W4,W5,GATES): assert p.is_file(),p
 text=DOC.read_text(encoding='utf-8')
 for phrase in ('Selected mode: **`split`**','P8-I — Internal evidential-status preservation','P8-E — External process-to-presentation correspondence','Faithful_split','ApplicableFaithful','does not prove a representation theorem'): assert phrase in text
 r=load(REG); assert r['decision_id']=='P8-ROLE-001' and r['selected_mode']=='split'; assert r['w3_proof_registry']==W3.relative_to(ROOT).as_posix(); assert r['w4_proof_registry']==W4.relative_to(ROOT).as_posix()
 internal=r['internal_obligation']; assert internal['predicate']=='Pres_8I'; assert internal['target_direct_axis_embedding_status']=='proved_LEM-SC-014'; assert internal['target_recovery_status']=='proved_LEM-SC-018'; assert internal['semantic_and_coherence_status']=='proved_LEM-SC-019_LEM-SC-020'; assert internal['negative_control_protection_status']=='proved_OBS-SC-010_NC-08_when_applicable'; assert internal['no_evidential_upgrade'] is True
 external=r['external_obligation']; assert external['predicate']=='Corr_8E'; assert external['not_implied_by_formal_representation'] is True; assert external['status']=='unproved'
 t=load(TARGET)
 if t['proof_status']=='bounded_theorem_proved':
  family={x['id']:x for x in t['theorem_family']}; assert family['THM-CORE-REP-001']['status']=='proved_for_S_core'; assert family['THM-P8-CORR-001']['predicate']=='Corr_8E'; assert family['THM-P8-CORR-001']['status']=='target_frozen_unproved'
 else:
  raise AssertionError('unexpected theorem proof status')
 assert t['p8']['selected_value']=='split'
 premises=load(PREMISES); assert premises['version']=='1.7'; assert next(x for x in premises['entries'] if x['id']=='PRM-010')['decision']=='split'
 ledger=load(LEDGER); by={x['id']:x for x in ledger['obligations']}; assert by['LEM-SC-014']['status']=='proved'; assert by['LEM-SC-018']['status']=='proved'; assert by['OBS-SC-006']['status']=='refuted'; assert by['OBS-SC-010']['status']=='obstruction_established'; assert by['ASM-SC-002']['status']=='proved'
 w4=load(W4); assert w4['result']['global_nontriviality_status']=='proved_for_registered_control_families_over_S_core'
 w5=load(W5); assert w5['p8_mode']=='split'; assert w5['claim_effect']['actual_process_correspondence']=='unresolved'
 gates={x['name']:x for x in load(GATES)['gates']}; assert gates['formal-negative-controls']['status']=='satisfied'; assert gates['universal-structure-result']['status']=='not_satisfied'
 print('P8 theorem-role decision: PASS (internal P8 assembled; external correspondence open)'); return 0
if __name__=='__main__': raise SystemExit(main())
