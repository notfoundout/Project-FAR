#!/usr/bin/env python3
"""Validate FAITHFUL-REP-001 after complete finite W3 construction work."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/faithful-representation-specification-v1.0.md'; REG=ROOT/'theory/evaluation/faithful-representation-specification-v1.0.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; PREMISES=ROOT/'theory/evaluation/thm-target-001-premise-ledger.json'; P8=ROOT/'theory/evaluation/p8-theorem-role-decision.json'; LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; W3=ROOT/'theory/evaluation/s-core-w3-global-witness-proof.json'; GATES=ROOT/'theory/evaluation/research-gates.json'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
    for p in (DOC,REG,TARGET,PREMISES,P8,LEDGER,W3,GATES): assert p.is_file(),p
    text=DOC.read_text(encoding='utf-8')
    for phrase in ('Faithful Representation Specification v1.0','Frozen prospective definition for `THM-TARGET-001`','Faithful_{m_8}','representation witness','source materiality contract'): assert phrase in text
    d=load(REG); assert d['specification_id']=='FAITHFUL-REP-001' and d['version']=='1.0'; assert d['w3_proof_registry']==W3.relative_to(ROOT).as_posix(); assert d['recovery_contract']['proof_status']=='proved_LEM-SC-018'; assert d['semantic_agreement']['global_proof_status']=='proved_LEM-SC-019'; assert d['cross_axis_coherence']['global_proof_status']=='proved_LEM-SC-020'; assert d['machinery_ledger']['complete_global_status']=='proved_LEM-SC-021'; assert d['uniformity']['global_target_constructor_equivariance_status']=='proved_LEM-SC-022'; assert d['compositional_accountability']['proof_status']=='proved_LEM-SC-017_LEM-SC-023'; assert d['witness_assembly']['proof_status']=='proved_LEM-SC-024'; assert d['nontriviality']['formal_negative_control_status']=='unproved_OBS-SC-010' and d['nontriviality']['global_nontrivial_status']=='unproved'; assert d['decision_semantics']['unknown']=='blocks_theorem_acceptance'; assert d['next_required_artifact'].startswith('W4 formal negative-control')
    axes={x['id']:x for x in d['axis_reducts']}; assert set(axes)=={f'P{i}' for i in range(1,8)}; assert all(x['construction_and_recovery_status'].startswith('proved_') for x in axes.values())
    ledger=load(LEDGER); assert ledger['execution_summary']['proved']==24 and ledger['execution_summary']['open']==4 and ledger['active_obligations']==['OBS-SC-010']
    w3=load(W3); assert w3['proof_id']=='SCORE-W3-PROOF-001' and w3['construction_properties']['faithful_split_proved'] is False
    target=load(TARGET); assert target['proof_status']=='partial_lemma_progress_only'; rep=next(x for x in target['theorem_family'] if x['id']=='THM-CORE-REP-001'); assert rep['status']!='proved' and 'specificity_discovery_bridge' in rep['blocked_by']
    premises=load(PREMISES); assert premises['version']=='1.6' and premises['proof_progress']['premise_change'] is False
    p8=load(P8); assert p8['internal_obligation']['target_recovery_status']=='proved_LEM-SC-018' and p8['external_obligation']['status']=='unproved'
    gates={x['name']:x for x in load(GATES)['gates']}; assert gates['scoped-representation-proof']['status']=='not_satisfied'; assert gates['mechanized-proof-verification']['status']=='not_satisfied'; assert gates['independent-proof-review']['status']=='not_satisfied'; assert gates['baseline-factorization-resolved']['status']=='not_satisfied'
    print('FAITHFUL-REP-001 validation PASS (finite construction/recovery conjuncts proved; W4, W3.5, Nontrivial, and theorem assembly open)'); return 0
if __name__=='__main__': raise SystemExit(main())
