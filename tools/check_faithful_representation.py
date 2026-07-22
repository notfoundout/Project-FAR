#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/faithful-representation-specification-v1.0.md'; REG=ROOT/'theory/evaluation/faithful-representation-specification-v1.0.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; PREMISES=ROOT/'theory/evaluation/thm-target-001-premise-ledger.json'; P8=ROOT/'theory/evaluation/p8-theorem-role-decision.json'; LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; W3=ROOT/'theory/evaluation/s-core-w3-global-witness-proof.json'; W4=ROOT/'theory/evaluation/s-core-w4-negative-control-proof.json'; W5=ROOT/'theory/evaluation/s-core-w5-theorem-assembly-proof.json'; GATES=ROOT/'theory/evaluation/research-gates.json'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
 for p in (DOC,REG,TARGET,PREMISES,P8,LEDGER,W3,W4,W5,GATES): assert p.is_file(),p
 d=load(REG); assert d['specification_id']=='FAITHFUL-REP-001' and d['version']=='1.0'; assert d['recovery_contract']['proof_status']=='proved_LEM-SC-018'; assert d['semantic_agreement']['global_proof_status']=='proved_LEM-SC-019'; assert d['cross_axis_coherence']['global_proof_status']=='proved_LEM-SC-020'; assert d['machinery_ledger']['complete_global_status']=='proved_LEM-SC-021'; assert d['uniformity']['global_target_constructor_equivariance_status']=='proved_LEM-SC-022'; assert d['compositional_accountability']['proof_status']=='proved_LEM-SC-017_LEM-SC-023'; assert d['witness_assembly']['proof_status']=='proved_LEM-SC-024'; assert d['nontriviality']['formal_negative_control_status']=='proved_OBS-SC-010'; assert d['nontriviality']['all_invalid_representations_rejected'] is False
 ledger=load(LEDGER); s=ledger['execution_summary']; assert (s['proved'],s['obstruction_established'],s['open'])==(27,1,0); assert ledger['active_obligations']==[] and ledger['active_wave']=='complete'
 w5=load(W5); assert w5['claim_effect']['bounded_faithful_representation']=='proved'; assert w5['claim_effect']['S_IRD_representation']=='unresolved'
 target=load(TARGET); assert target['proof_status']=='bounded_theorem_proved'; rep=next(x for x in target['theorem_family'] if x['id']=='THM-CORE-REP-001'); assert rep['status']=='proved_for_S_core' and rep['blocked_by']==[]; assert target['w5_authorization']['authorized'] is True
 premises=load(PREMISES); assert premises['version']=='1.7' and premises['proof_progress']['premise_change'] is False
 p8=load(P8); assert p8['internal_obligation']['target_recovery_status']=='proved_LEM-SC-018' and p8['external_obligation']['status']=='unproved'
 gates={x['name']:x for x in load(GATES)['gates']}; assert gates['formal-negative-controls']['status']=='satisfied'; assert gates['mechanized-proof-verification']['status']=='not_satisfied'; assert gates['independent-proof-review']['status']=='not_satisfied'; assert gates['universal-structure-result']['status']=='not_satisfied'
 print('FAITHFUL-REP-001 validation PASS (bounded S_core theorem proved)'); return 0
if __name__=='__main__': raise SystemExit(main())
