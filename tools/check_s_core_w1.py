#!/usr/bin/env python3
"""Validate retained SCORE-W1-PROOF-001 after later wave progress."""
from __future__ import annotations
import json
from pathlib import Path
from s_core_w1_reference import DIRECT_AXES, construct_target, verify_all

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/s-core-w1-direct-axis-proof-v1.0.md'; REG=ROOT/'theory/evaluation/s-core-w1-direct-axis-proof.json'; FIXTURES=ROOT/'theory/evaluation/s-core-w1-reference-fixtures.json'
LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; FAITHFUL=ROOT/'theory/evaluation/faithful-representation-specification-v1.0.json'; P8=ROOT/'theory/evaluation/p8-theorem-role-decision.json'; GATES=ROOT/'theory/evaluation/research-gates.json'; AUDIT=ROOT/'docs/audits/s-core-w1-proof-audit.md'; TEST=ROOT/'tests/test_s_core_w1_reference.py'; REFERENCE=ROOT/'tools/s_core_w1_reference.py'; MAKEFILE=ROOT/'Makefile'; W2=ROOT/'theory/evaluation/s-core-w2-dynamics-history-proof.json'
PROVED={'LEM-SC-005','LEM-SC-006','LEM-SC-007','LEM-SC-008','LEM-SC-009','LEM-SC-012','LEM-SC-014'}; REFUTED={'OBS-SC-003','OBS-SC-006'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
    for p in (DOC,REG,FIXTURES,LEDGER,TARGET,FAITHFUL,P8,GATES,AUDIT,TEST,REFERENCE,MAKEFILE,W2): assert p.is_file(),p
    text=DOC.read_text(encoding='utf-8')
    for phrase in ('S_core W1 Direct-Axis Construction Proof v1.0','SCORE-W1-PROOF-001','DIR-INCIDENCE-1.0','Relation reflection','LEM-SC-005','LEM-SC-014','OBS-SC-003','OBS-SC-006','does not yet establish the full predicates `Pres_i`'): assert phrase in text
    reg=load(REG); assert reg['proof_id']=='SCORE-W1-PROOF-001' and reg['version']=='1.0'; assert reg['status']=='project_authored_human_checkable_proof_complete'; assert reg['construction_schema']=='DIR-INCIDENCE-1.0'
    schema=reg['fixed_target_schema']; assert schema['object_representation_separation'] is True and schema['new_fara_primitive_added'] is False and schema['source_case_branching'] is False
    properties=reg['construction_properties']
    for key in ('finite_on_S_core','total_on_direct_axis_reducts','source_element_injective','sort_preserving','material_sort_disjointness_preserved','relation_preservation','relation_reflection','attribute_preservation','image_accountability','lexical_label_independent','direct_axis_isomorphism_equivariant','internal_evidence_no_upgrade'): assert properties[key] is True,key
    assert properties['complete_global_recovery_proved'] is False and properties['complete_global_machinery_ledger_proved'] is False
    results={x['id']:x for x in reg['results']}; assert set(results)==PROVED|REFUTED; assert all(results[x]['status']=='proved' for x in PROVED); assert all(results[x]['status']=='refuted' for x in REFUTED)
    assert reg['ledger_effect']=={'total':37,'proved':11,'obstruction_established':0,'scope_boundary_established':1,'refuted':2,'open':23,'completed_waves':['W0','W1'],'active_wave':'W2'}
    verification=reg['verification']; assert verification['human_checkable_proof']=='complete_project_authored'; assert verification['executable_reference']=='complete_bounded_corroboration'; assert verification['proof_assistant']=='not_started'; assert verification['independent_review']=='not_started'
    fixture=load(FIXTURES); assert fixture['fixture_set_id']=='SCORE-W1-FIXTURES-001' and fixture['constructor_schema']=='DIR-INCIDENCE-1.0'; assert set(fixture['source']['axes'])==set(DIRECT_AXES)
    target,correspondence=construct_target(fixture['source']); assert target['schema']=='DIR-INCIDENCE-1.0'; assert verify_all(fixture['source'],target,correspondence); assert len(target['U'])==len(target['Rep']); assert {x['id'] for x in target['U']}.isdisjoint({x['id'] for x in target['Rep']})
    ledger=load(LEDGER); assert ledger['status']=='frozen_dependency_decomposition_w0_w1_w2_complete_w3_active'; assert REG.relative_to(ROOT).as_posix() in ledger['proof_packages']; assert W2.relative_to(ROOT).as_posix() in ledger['proof_packages']
    obligations={x['id']:x for x in ledger['obligations']}
    for item_id in PROVED: assert obligations[item_id]['status']=='proved' and DOC.relative_to(ROOT).as_posix() in obligations[item_id]['evidence'] and REG.relative_to(ROOT).as_posix() in obligations[item_id]['evidence']
    for item_id in REFUTED: assert obligations[item_id]['status']=='refuted' and DOC.relative_to(ROOT).as_posix() in obligations[item_id]['evidence'] and REG.relative_to(ROOT).as_posix() in obligations[item_id]['evidence']
    summary=ledger['execution_summary']; assert (summary['proved'],summary['scope_boundary_established'],summary['refuted'],summary['open'])==(16,1,4,16); assert ledger['completed_waves']==['W0','W1','W2']; assert ledger['active_wave']=='W3'
    target_reg=load(TARGET); program=target_reg['lemma_program']; assert program['status']=='w0_w1_w2_complete_w3_active' and program['proved_obligations']==16 and program['refuted_obstruction_hypotheses']==4 and program['open_obligations']==16 and program['active_wave']=='W3'; assert target_reg['proof_status']=='partial_lemma_progress_only'
    faithful=load(FAITHFUL); assert faithful['w1_direct_axis_proof_registry']==REG.relative_to(ROOT).as_posix(); assert faithful['direct_axis_construction_status']=='proved_without_global_recovery'; assert faithful['next_required_artifact']==ledger['next_required_artifact']
    p8=load(P8); assert p8['w1_direct_axis_proof_registry']==REG.relative_to(ROOT).as_posix(); assert p8['internal_construction_status']=='direct_axis_embedding_proved_recovery_unproved'; assert p8['external_obligation']['not_implied_by_formal_representation'] is True
    gates=load(GATES); required=set(gates['required_canonical_artifacts']); assert all(p.relative_to(ROOT).as_posix() in required for p in (DOC,REG,AUDIT,W2)); by_name={x['name']:x for x in gates['gates']}; assert by_name['scoped-representation-proof']['status']=='not_satisfied'; assert by_name['mechanized-proof-verification']['status']=='not_satisfied'; assert by_name['independent-proof-review']['status']=='not_satisfied'
    assert MAKEFILE.read_text(encoding='utf-8').count('python tools/check_s_core_w1.py')==3
    print('S_core W1 proof: PASS (retained after W2; 7 lemmas and 2 refutations remain established)')
    return 0
if __name__=='__main__': raise SystemExit(main())
