#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from s_core_w3_reference import construct_witness, recover_target, verify_witness
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/s-core-w3-global-witness-proof-v1.0.md'; REG=ROOT/'theory/evaluation/s-core-w3-global-witness-proof.json'; FIX=ROOT/'theory/evaluation/s-core-w3-reference-fixtures.json'; LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; FAITHFUL=ROOT/'theory/evaluation/faithful-representation-specification-v1.0.json'; P8=ROOT/'theory/evaluation/p8-theorem-role-decision.json'; GATES=ROOT/'theory/evaluation/research-gates.json'; W4=ROOT/'theory/evaluation/s-core-w4-negative-control-proof.json'; AUDIT=ROOT/'docs/audits/s-core-w3-proof-audit.md'; TEST=ROOT/'tests/test_s_core_w3_reference.py'; MAKE=ROOT/'Makefile'
PROVED={f'LEM-SC-{i:03d}' for i in range(17,25)}; REFUTED={'OBS-SC-002','OBS-SC-007','OBS-SC-008','OBS-SC-009'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
    for p in (DOC,REG,FIX,LEDGER,TARGET,FAITHFUL,P8,GATES,W4,AUDIT,TEST,MAKE): assert p.is_file(),p
    text=DOC.read_text(encoding='utf-8')
    for phrase in ('S_core W3 Global-Witness Construction Proof v1.0','SCORE-W3-PROOF-001','RECOVER-FARA-1.0','LEM-SC-017','LEM-SC-024','OBS-SC-002','OBS-SC-009','does not mark `Faithful_split` proved'): assert phrase in text,phrase
    reg=load(REG); assert reg['proof_id']=='SCORE-W3-PROOF-001'; assert reg['target_schema']['recovery_uses_source'] is False; assert reg['target_schema']['adds_new_primitive'] is False
    results={x['id']:x for x in reg['results']}; assert set(results)==PROVED|REFUTED; assert all(results[x]['status']=='proved' for x in PROVED); assert all(results[x]['status']=='refuted' for x in REFUTED)
    props=reg['construction_properties']
    for key in ('target_only_recovery','recovery_deterministic','recovery_terminating','complete_axis_recovery','semantic_agreement','cross_axis_coherence','complete_machinery_ledger','uniform_constructor','source_isomorphism_equivariant','distributed_decomposition','compositional_accountability','well_formed_witness_assembly'): assert props[key] is True,key
    assert props['formal_negative_controls_proved'] is False and props['faithful_split_proved'] is False and props['theorem_assembly_proved'] is False
    fixture=load(FIX); source=fixture['source']; package=construct_witness(source); assert verify_witness(source,package)
    recovered=recover_target(package['A'],package['W']['D'],package['W']['kappa']); stripped=json.loads(json.dumps(package)); stripped['W']['E']={}; stripped['W']['M']={}; assert recovered==recover_target(stripped['A'],stripped['W']['D'],stripped['W']['kappa'])
    ledger=load(LEDGER); summary=ledger['execution_summary']; assert (summary['proved'],summary['obstruction_established'],summary['scope_boundary_established'],summary['refuted'],summary['open'])==(24,1,1,8,3); assert ledger['completed_waves']==['W0','W1','W2','W3','W4']; assert ledger['active_wave']=='W5_blocked'; assert ledger['active_obligations']==[]
    by_id={x['id']:x for x in ledger['obligations']}; assert all(by_id[x]['status']=='proved' for x in PROVED); assert all(by_id[x]['status']=='refuted' for x in REFUTED); assert by_id['OBS-SC-010']['status']=='obstruction_established'; assert all(by_id[f'ASM-SC-{i:03d}']['status']=='registered_unproved' for i in range(1,4))
    target=load(TARGET); assert target['lemma_program']['proved_obligations']==24 and target['lemma_program']['open_obligations']==3; assert target['proof_status']=='partial_lemma_progress_only'; assert target['next_required_artifact']==ledger['next_required_artifact']; assert target['w5_authorization']['blocked_by']==['W3.5-SDG-001']
    faithful=load(FAITHFUL); assert faithful['recovery_contract']['proof_status']=='proved_LEM-SC-018'; assert faithful['semantic_agreement']['global_proof_status']=='proved_LEM-SC-019'; assert faithful['nontriviality']['formal_negative_control_status']=='proved_OBS-SC-010'
    p8=load(P8); assert p8['internal_obligation']['target_recovery_status']=='proved_LEM-SC-018'; assert p8['external_obligation']['status']=='unproved'
    w4=load(W4); assert w4['result']['status']=='obstruction_established' and w4['result']['faithful_split_satisfiability_proved'] is False
    gates={x['name']:x for x in load(GATES)['gates']}; assert gates['formal-negative-controls']['status']=='satisfied'; assert gates['scoped-representation-proof']['status']=='not_satisfied'; assert gates['baseline-factorization-resolved']['status']=='satisfied' and gates['baseline-factorization-resolved']['evidence']; assert gates['fara-specificity-resolved']['status']=='not_satisfied'; assert gates['reasoning-contrast-execution']['status']=='not_satisfied'; assert gates['mechanized-proof-verification']['status']=='not_satisfied'; assert gates['independent-proof-review']['status']=='not_satisfied'
    assert MAKE.read_text(encoding='utf-8').count('python tools/check_s_core_w3.py')==3
    cp=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_s_core_w3_reference.py'],cwd=ROOT,text=True,capture_output=True); assert cp.returncode==0,cp.stdout+cp.stderr
    print('S_core W3 proof: PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
