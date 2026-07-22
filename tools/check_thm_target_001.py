#!/usr/bin/env python3
"""Validate THM-TARGET-001 after bounded W5 theorem assembly."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/thm-target-001-v1.0.md'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; PREMISES=ROOT/'theory/evaluation/thm-target-001-premise-ledger.json'; GATES=ROOT/'theory/evaluation/research-gates.json'; CLAIMS=ROOT/'theory/evaluation/central-claim-registry.json'; LEMMA=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; W5=ROOT/'theory/evaluation/s-core-w5-theorem-assembly-proof.json'; PROOFS=[ROOT/f'theory/evaluation/s-core-w{i}-{name}.json' for i,name in [(0,'normalization-proof'),(1,'direct-axis-proof'),(2,'dynamics-history-proof'),(3,'global-witness-proof'),(4,'negative-control-proof'),(5,'theorem-assembly-proof')]]
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
 for p in (DOC,TARGET,PREMISES,GATES,CLAIMS,LEMMA,W5,*PROOFS): assert p.is_file(),p
 t=load(TARGET); assert t['theorem_target_id']=='THM-TARGET-001' and t['version']=='1.2'; assert t['status']=='proved_bounded_s_core' and t['proof_status']=='bounded_theorem_proved'; assert t['machine_check_status']=='bounded_executable_reference_only' and t['independent_review_status']=='not_started'; assert t['program_track']=='REP' and t['universal_structure_target']=='THM-US-TARGET-001'
 p=t['lemma_program']; assert p['status']=='w0_w1_w2_w3_w4_w5_complete_bounded_theorem_proved'; assert (p['total_obligations'],p['proved_obligations'],p['open_obligations'])==(37,27,0); assert p['completed_waves']==['W0','W1','W2','W3','W4','W5'] and p['active_wave']=='complete' and p['active_obligations']==[]
 family={x['id']:x for x in t['theorem_family']}; assert family['THM-CORE-COMMON-001']['status']=='proved_for_S_core'; assert family['THM-CORE-REP-001']['status']=='proved_for_S_core'; assert family['THM-IMP-001']['status']=='refuted_for_S_core_under_frozen_target'; assert family['THM-IRD-EXT-001']['status']=='target_frozen_blocked'; assert t['next_required_artifact'].startswith('Mechanize the bounded W5 theorem')
 w=load(W5); assert w['proof_id']=='SCORE-W5-PROOF-001' and w['status']=='complete_bounded_deductive_assembly'; assert w['claim_effect']['bounded_faithful_representation']=='proved' and w['claim_effect']['universal_structure']=='unresolved'
 s=load(LEMMA)['execution_summary']; assert (s['proved'],s['obstruction_established'],s['scope_boundary_established'],s['refuted'],s['open'])==(27,1,1,8,0)
 assert [load(x)['proof_id'] for x in PROOFS]==['SCORE-W0-PROOF-001','SCORE-W1-PROOF-001','SCORE-W2-PROOF-001','SCORE-W3-PROOF-001','SCORE-W4-PROOF-001','SCORE-W5-PROOF-001']
 assert t['w5_authorization']['authorized'] is True and t['w5_authorization']['blocked_by']==[]
 for claim in load(CLAIMS)['claims']:
  if claim['id'] in {'CLM-UNIVERSALITY','CLM-UNIVERSAL-STRUCTURE','CLM-NECESSITY','CLM-MINIMALITY'}: assert claim['current_status'] not in {'supported','supported_at_registered_control_scope'}
 print('THM-TARGET-001 validation: PASS (bounded S_core theorem proved; broader claims unresolved)'); return 0
if __name__=='__main__': raise SystemExit(main())
