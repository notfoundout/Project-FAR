#!/usr/bin/env python3
"""Validate deduction-first dependencies after bounded W4 and factorization closure."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
F={'standard':ROOT/'docs/governance/deduction-first-research-standard.md','central':ROOT/'docs/governance/central-research-program.md','roadmap':ROOT/'docs/planning/deduction-first-proof-roadmap.md','arch':ROOT/'docs/planning/architecture-neutral-research-roadmap.md','target':ROOT/'theory/evaluation/thm-target-001.json','premises':ROOT/'theory/evaluation/thm-target-001-premise-ledger.json','faithful':ROOT/'theory/evaluation/faithful-representation-specification-v1.0.json','p8':ROOT/'theory/evaluation/p8-theorem-role-decision.json','ledger':ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json','w3':ROOT/'theory/evaluation/s-core-w3-global-witness-proof.json','w4':ROOT/'theory/evaluation/s-core-w4-negative-control-proof.json','gates':ROOT/'theory/evaluation/research-gates.json','claims':ROOT/'theory/evaluation/central-claim-registry.json','make':ROOT/'Makefile'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
    for p in F.values(): assert p.is_file(),p
    standard=F['standard'].read_text(encoding='utf-8'); assert 'The primary route to an answer is therefore deductive' in standard and 'It is not required before attempting a mathematical proof' in standard
    target=load(F['target']); assert target['status']=='frozen_unproved' and target['proof_status']=='partial_lemma_progress_only' and target['next_required_artifact'].startswith('Evidence-backed W3.5')
    p=target['lemma_program']; assert p['status']=='w0_w1_w2_w3_w4_complete_w5_blocked_by_w3_5' and (p['proved_obligations'],p['established_obstructions'],p['scope_boundaries_established'],p['refuted_obstructions'],p['open_obligations'])==(24,1,1,8,3) and p['completed_waves']==['W0','W1','W2','W3','W4'] and p['active_obligations']==[] and p['active_wave']=='W5_blocked'
    premises=load(F['premises']); assert premises['version']=='1.7' and premises['proof_progress']['premise_change'] is False and premises['proof_progress']['theorem_status_change'] is False
    faithful=load(F['faithful']); assert faithful['recovery_contract']['proof_status']=='proved_LEM-SC-018' and faithful['nontriviality']['formal_negative_control_status']=='proved_OBS-SC-010' and faithful['nontriviality']['global_nontrivial_status']=='proved_for_registered_control_families_over_S_core'
    p8=load(F['p8']); assert p8['selected_mode']=='split' and p8['internal_obligation']['target_recovery_status']=='proved_LEM-SC-018' and p8['external_obligation']['not_implied_by_formal_representation'] is True
    ledger=load(F['ledger']); s=ledger['execution_summary']; assert (s['proved'],s['obstruction_established'],s['scope_boundary_established'],s['refuted'],s['open'])==(24,1,1,8,3); by={x['id']:x for x in ledger['obligations']}; assert all(by[f'LEM-SC-{i:03d}']['status']=='proved' for i in range(1,25)); assert by['OBS-SC-010']['status']=='obstruction_established'; assert all(by[f'ASM-SC-{i:03d}']['status']=='registered_unproved' for i in range(1,4))
    w3=load(F['w3']); assert w3['proof_id']=='SCORE-W3-PROOF-001' and w3['construction_properties']['formal_negative_controls_proved'] is False and w3['construction_properties']['theorem_assembly_proved'] is False
    w4=load(F['w4']); assert w4['proof_id']=='SCORE-W4-PROOF-001' and w4['result']['status']=='obstruction_established' and w4['result']['faithful_split_satisfiability_proved'] is False
    names={x['name']:x for x in load(F['gates'])['gates']}; assert names['formal-negative-controls']['status']=='satisfied'; assert names['scoped-representation-proof']['status']=='not_satisfied'; assert names['baseline-factorization-resolved']['status']=='satisfied' and names['baseline-factorization-resolved']['evidence']; assert names['fara-specificity-resolved']['status']=='not_satisfied'; assert names['reasoning-contrast-execution']['status']=='not_satisfied'; assert names['mechanized-proof-verification']['status']=='not_satisfied'; assert names['independent-proof-review']['status']=='not_satisfied'
    for claim in load(F['claims'])['claims']:
        if claim['id'] in {'CLM-EXISTENCE','CLM-UNIVERSALITY','CLM-UNIVERSAL-STRUCTURE','CLM-NECESSITY','CLM-MINIMALITY'}: assert claim['current_status'] not in {'supported','supported_at_registered_control_scope'}
    make=F['make'].read_text(encoding='utf-8')
    for checker in ('check_faithful_representation.py','check_p8_theorem_role.py','check_s_core_lemma_ledger.py','check_s_core_w0.py','check_s_core_w1.py','check_s_core_w2.py','check_s_core_w3.py','check_s_core_w4.py'): assert make.count(f'python tools/{checker}')==3
    print('Deduction-first research program: PASS (W0-W4 and bounded factorization complete; specificity and execution evidence still block W5; theorem gate closed)'); return 0
if __name__=='__main__': raise SystemExit(main())
