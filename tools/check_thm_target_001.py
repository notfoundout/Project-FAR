#!/usr/bin/env python3
"""Validate THM-TARGET-001 after bounded W5 theorem assembly."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/thm-target-001-v1.0.md'
TARGET=ROOT/'theory/evaluation/thm-target-001.json'
PREMISES=ROOT/'theory/evaluation/thm-target-001-premise-ledger.json'
GATES=ROOT/'theory/evaluation/research-gates.json'
CLAIMS=ROOT/'theory/evaluation/central-claim-registry.json'
LEMMA=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'
CORPUS=ROOT/'theory/evaluation/w3-5-corpus-freeze-result-v1.0.json'
FACTOR=ROOT/'theory/evaluation/w3-5-factorization-result-v1.0.json'
DISC=ROOT/'theory/evaluation/w3-5-reasoning-discrimination-result-v1.0.json'
SPEC=ROOT/'theory/evaluation/w3-5-fara-specificity-result-v1.0.json'
W5=ROOT/'theory/evaluation/s-core-w5-theorem-assembly-proof.json'
PROOFS=[ROOT/f'theory/evaluation/s-core-w{i}-{name}.json' for i,name in [(0,'normalization-proof'),(1,'direct-axis-proof'),(2,'dynamics-history-proof'),(3,'global-witness-proof'),(4,'negative-control-proof'),(5,'theorem-assembly-proof')]]
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
 for p in (DOC,TARGET,PREMISES,GATES,CLAIMS,LEMMA,CORPUS,FACTOR,DISC,SPEC,W5,*PROOFS):
  assert p.is_file(),p
 text=DOC.read_text(encoding='utf-8')
 for phrase in ('Frozen prospective theorem target and premise boundary','Finite explicit core `S_core`','General extension class `S_IRD`','THM-CORE-REP-001','THM-IMP-001','This artifact does not establish'):
  assert phrase in text,phrase
 t=load(TARGET)
 assert t['theorem_target_id']=='THM-TARGET-001'
 assert t['version']=='1.2'
 assert t['status']=='proved_bounded_s_core'
 assert t['proof_status']=='bounded_theorem_proved'
 assert t['machine_check_status']=='bounded_executable_reference_only'
 assert t['independent_review_status']=='not_started'
 assert t['program_track']=='REP'
 assert t['universal_structure_target']=='THM-US-TARGET-001'
 assert set(t['source_classes'])=={'S_core','S_IRD'}
 assert t['target_class']['id']=='A_FARA'
 assert t['target_class']['adds_new_primitive'] is False
 assert t['representation_witness']['tuple']==['E','D','M','iota','kappa']
 assert t['w3_proof_registry']==PROOFS[3].relative_to(ROOT).as_posix()
 assert t['w4_proof_registry']==PROOFS[4].relative_to(ROOT).as_posix()
 p=t['lemma_program']
 assert p['status']=='w0_w1_w2_w3_w4_w5_complete_bounded_theorem_proved'
 assert (p['total_obligations'],p['proved_obligations'],p['established_obstructions'],p['refuted_obstruction_hypotheses'],p['scope_boundaries_established'],p['open_obligations'])==(37,27,1,8,1,0)
 assert p['completed_waves']==['W0','W1','W2','W3','W4','W5']
 assert p['active_wave']=='complete'
 assert p['active_obligations']==[]
 assert p['blocked_obligations']==[]
 family={x['id']:x for x in t['theorem_family']}
 assert family['THM-CORE-COMMON-001']['status']=='proved_for_S_core'
 assert family['THM-CORE-COMMON-001']['blocked_by']==[]
 assert family['THM-CORE-REP-001']['status']=='proved_for_S_core'
 assert family['THM-CORE-REP-001']['blocked_by']==[]
 assert family['THM-IMP-001']['status']=='refuted_for_S_core_under_frozen_target'
 assert family['THM-IMP-001']['blocked_by']==[]
 assert family['THM-IRD-EXT-001']['status']=='target_frozen_blocked'
 assert family['THM-P8-CORR-001']['status']=='target_frozen_unproved'
 assert t['next_required_artifact'].startswith('Mechanize the bounded W5 theorem')
 assert t['w5_authorization']['authorized'] is True
 assert t['w5_authorization']['blocked_by']==[]
 assert set(t['w5_authorization']['resolved_dependencies'])=={'OBS-SC-010','W3.5-SDG-001'}
 prem=load(PREMISES)
 assert prem['version']=='1.7'
 progress=prem['proof_progress']
 assert progress['premise_change'] is False
 assert progress['source_scope_change'] is False
 assert progress['target_interface_change'] is False
 assert progress['theorem_status_change'] is False
 s=load(LEMMA)['execution_summary']
 assert (s['proved'],s['obstruction_established'],s['scope_boundary_established'],s['refuted'],s['open'])==(27,1,1,8,0)
 assert [load(x)['proof_id'] for x in PROOFS]==['SCORE-W0-PROOF-001','SCORE-W1-PROOF-001','SCORE-W2-PROOF-001','SCORE-W3-PROOF-001','SCORE-W4-PROOF-001','SCORE-W5-PROOF-001']
 w=load(W5)
 assert w['proof_id']=='SCORE-W5-PROOF-001'
 assert w['status']=='complete_bounded_deductive_assembly'
 assert w['claim_effect']['bounded_faithful_representation']=='proved'
 assert w['claim_effect']['S_IRD_representation']=='unresolved'
 assert w['claim_effect']['actual_process_correspondence']=='unresolved'
 assert w['claim_effect']['primitive_necessity']=='unresolved'
 assert w['claim_effect']['minimality']=='unresolved'
 assert w['claim_effect']['uniqueness']=='unresolved'
 assert w['claim_effect']['universal_structure']=='unresolved'
 corpus=load(CORPUS)
 assert corpus['status']=='complete'
 assert corpus['artifact_id']=='RCS-CORPUS-001'
 assert corpus['candidate_scoring_status']=='not_started'
 assert corpus['claim_impact']['W5_authorized'] is False
 factor=load(FACTOR)
 assert factor['status']=='complete'
 assert factor['artifact_id']=='W35-FACTOR-RESULT-001'
 assert factor['dimensions']['reasoning_specificity']=='not_established'
 assert factor['factorization_contract']['primitive_reduction_established'] is False
 assert factor['gate_effect']['w5_authorized'] is False
 disc=load(DISC)
 assert disc['status']=='complete'
 assert disc['artifact_id']=='W35-SCOPE-RESULT-001'
 assert disc['primary_metrics']['statistical_inference']=='not_authorized'
 assert disc['gate_effect']['w5_authorized'] is False
 spec=load(SPEC)
 assert spec['status']=='complete_qualified_negative'
 assert spec['artifact_id']=='W35-SPEC-RESULT-001'
 assert spec['result']['unique_discriminative_capacity_of_fara']=='refuted_at_registered_scope'
 assert spec['result']['fara_reasoning_specificity_general']=='not_established'
 assert spec['result']['fara_primitive_necessity']=='not_established'
 assert spec['gate_effect']['w5_authorized'] is False
 gates={x['name']:x for x in load(GATES)['gates']}
 assert gates['formal-theorem-target']['status']=='satisfied'
 assert gates['premise-ledger-and-semantics']['status']=='satisfied'
 assert gates['faithful-representation-definition']['status']=='satisfied'
 assert gates['formal-negative-controls']['status']=='satisfied'
 assert gates['scoped-representation-proof']['status']=='satisfied'
 assert gates['scoped-representation-proof']['evidence']==['docs/research/s-core-w5-theorem-assembly-proof-v1.0.md','theory/evaluation/s-core-w5-theorem-assembly-proof.json']
 assert gates['reasoning-contrast-scope-framework-frozen']['status']=='satisfied'
 assert gates['reasoning-contrast-corpus-frozen']['status']=='satisfied' and gates['reasoning-contrast-corpus-frozen']['evidence']
 assert gates['baseline-factorization-resolved']['status']=='satisfied' and gates['baseline-factorization-resolved']['evidence']
 assert gates['fara-specificity-resolved']['status']=='satisfied' and gates['fara-specificity-resolved']['evidence']
 assert gates['reasoning-contrast-execution']['status']=='satisfied' and gates['reasoning-contrast-execution']['evidence']
 assert gates['mechanized-proof-verification']['status']=='not_satisfied'
 assert gates['independent-proof-review']['status']=='not_satisfied'
 assert gates['universal-structure-result']['status']=='not_satisfied'
 for claim in load(CLAIMS)['claims']:
  if claim['id'] in {'CLM-UNIVERSALITY','CLM-UNIVERSAL-STRUCTURE','CLM-NECESSITY','CLM-MINIMALITY'}:
   assert claim['current_status'] not in {'supported','supported_at_registered_control_scope'}
 print('THM-TARGET-001 validation: PASS (bounded S_core theorem proved; broader claims unresolved)')
 return 0
if __name__=='__main__': raise SystemExit(main())