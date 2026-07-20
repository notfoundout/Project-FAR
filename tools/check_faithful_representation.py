#!/usr/bin/env python3
"""Validate FAITHFUL-REP-001 after W0/W1 partial construction proofs."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/faithful-representation-specification-v1.0.md'; REG=ROOT/'theory/evaluation/faithful-representation-specification-v1.0.json'
TARGET=ROOT/'theory/evaluation/thm-target-001.json'; PREMISES=ROOT/'theory/evaluation/thm-target-001-premise-ledger.json'
P8=ROOT/'theory/evaluation/p8-theorem-role-decision.json'; LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'
W1=ROOT/'theory/evaluation/s-core-w1-direct-axis-proof.json'; GATES=ROOT/'theory/evaluation/research-gates.json'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def truth(m,keys):
    for k in keys: assert m.get(k) is True,k
def main()->int:
    for p in (DOC,REG,TARGET,PREMISES,P8,LEDGER,W1,GATES): assert p.is_file(),p
    text=DOC.read_text(encoding='utf-8')
    for phrase in ('strong typed correspondence','Relation preservation and reflection','finite labeled probabilistic bisimulation','Cross-axis coherence','Uniform construction','Complete machinery ledger','Faithful_{m_8}','unknown` blocks theorem acceptance'): assert phrase in text
    d=load(REG)
    assert d['specification_id']=='FAITHFUL-REP-001' and d['version']=='1.0'
    assert d['status']=='frozen_definition_w0_w1_partial_construction_proved_global_satisfiability_unproved'
    assert d['direct_axis_construction_status']=='proved_without_global_recovery'
    assert d['w1_direct_axis_proof_registry']==W1.relative_to(ROOT).as_posix()
    source=d['source_contract']; truth(source,{'owned_by_source','materiality_closure_required','exclusion_certificate_required'}); assert source['target_may_weaken'] is False
    assert source['finite_normalization_status']=='proved_LEM-SC-001' and source['source_isomorphism_transport_status']=='proved_LEM-SC-004'
    axes={x['id']:x for x in d['axis_reducts']}; assert set(axes)=={f'P{i}' for i in range(1,8)}
    for axis in ('P1','P2','P3','P4','P6'): assert axes[axis]['direct_axis_construction_status'].startswith('proved_LEM-SC-')
    assert axes['P5']['direct_axis_construction_status']=='unproved_W2' and axes['P7']['direct_axis_construction_status']=='unproved_W2'
    allocation=d['target_allocation']; assert allocation['status']=='proved_LEM-SC-005'; assert allocation['object_representation_separation'] is True; assert allocation['new_fara_primitive_added'] is False
    recovery=d['recovery_contract']; truth(recovery,{'fixed_versioned_interface','target_only_after_construction','deterministic','terminates_on_S_core','pure','derived_relations_declared_in_ledger'}); assert recovery['proof_status']=='unproved_LEM-SC-018'
    corr=d['correspondence_package']; truth(corr,{'totality','type_preservation','element_injectivity','relation_preservation','relation_reflection','attribute_preservation_under_source_equivalence','exact_equality_default','image_accountability'}); assert corr['direct_axis_status']=='proved_for_P1_P2_P3_P4_P6_P8I_without_recovery'
    assert d['p8']['internal_direct_axis_embedding_status']=='proved_LEM-SC-014_recovery_unproved'
    assert d['semantic_agreement']['global_proof_status']=='unproved_LEM-SC-019'; assert d['cross_axis_coherence']['global_proof_status']=='unproved_LEM-SC-020'; assert d['machinery_ledger']['complete_global_status']=='unproved_LEM-SC-021'
    controls=d['nontriviality']['negative_control_mapping']; assert set(controls)=={f'NC-{i:02d}' for i in range(1,11)}
    assert d['nontriviality']['w1_obstruction_results']=={'OBS-SC-003':'refuted_by_generic_direct_axis_relation_embedding','OBS-SC-006':'refuted_by_exact_internal_evidence_embedding'}
    assert d['decision_semantics']['unknown']=='blocks_theorem_acceptance'
    assert d['next_required_artifact']=='W2 dynamics history revision and self-modification proof-or-obstruction package'
    lemma=load(LEDGER); assert lemma['status']=='frozen_dependency_decomposition_w0_w1_complete_w2_active'; assert lemma['execution_summary']['proved']==11 and lemma['execution_summary']['open']==23
    w1=load(W1); assert w1['proof_id']=='SCORE-W1-PROOF-001'; assert w1['construction_properties']['complete_global_recovery_proved'] is False
    target=load(TARGET); assert target['proof_status']=='partial_lemma_progress_only'; assert target['theorem_family'][1]['status']!='proved'
    premises=load(PREMISES); assert premises['version']=='1.4'; assert premises['proof_progress']['premise_change'] is False
    p8=load(P8); assert p8['internal_construction_status']=='direct_axis_embedding_proved_recovery_unproved'; assert p8['external_obligation']['not_implied_by_formal_representation'] is True
    gates={x['name']:x for x in load(GATES)['gates']}; assert gates['scoped-representation-proof']['status']=='not_satisfied'; assert gates['mechanized-proof-verification']['status']=='not_satisfied'; assert gates['independent-proof-review']['status']=='not_satisfied'
    print('FAITHFUL-REP-001 validation PASS (direct axes proved; recovery/global witness unproved; W2 active)')
    return 0
if __name__=='__main__': raise SystemExit(main())
