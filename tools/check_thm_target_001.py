#!/usr/bin/env python3
"""Validate frozen THM-TARGET-001 after W3 construction closure."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/thm-target-001-v1.0.md'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; PREMISES=ROOT/'theory/evaluation/thm-target-001-premise-ledger.json'; GATES=ROOT/'theory/evaluation/research-gates.json'; CLAIMS=ROOT/'theory/evaluation/central-claim-registry.json'; LEMMA=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; PROOFS=[ROOT/f'theory/evaluation/s-core-w{i}-{name}.json' for i,name in [(0,'normalization-proof'),(1,'direct-axis-proof'),(2,'dynamics-history-proof'),(3,'global-witness-proof')]]
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
    for p in (DOC,TARGET,PREMISES,GATES,CLAIMS,LEMMA,*PROOFS): assert p.is_file(),p
    text=DOC.read_text(encoding='utf-8')
    for phrase in ('Frozen prospective theorem target and premise boundary','Finite explicit core `S_core`','General extension class `S_IRD`','THM-CORE-REP-001','THM-IMP-001','This artifact does not establish'): assert phrase in text
    t=load(TARGET); assert t['theorem_target_id']=='THM-TARGET-001' and t['version']=='1.0'; assert t['status']=='frozen_unproved' and t['proof_status']=='partial_lemma_progress_only'; assert t['machine_check_status']=='bounded_executable_reference_only' and t['independent_review_status']=='not_started'; assert set(t['source_classes'])=={'S_core','S_IRD'}; assert t['target_class']['id']=='A_FARA' and t['target_class']['adds_new_primitive'] is False; assert t['representation_witness']['tuple']==['E','D','M','iota','kappa']; assert t['w3_proof_registry']==PROOFS[3].relative_to(ROOT).as_posix()
    p=t['lemma_program']; assert p['status']=='w0_w1_w2_w3_complete_w4_active'; assert (p['total_obligations'],p['proved_obligations'],p['refuted_obstruction_hypotheses'],p['scope_boundaries_established'],p['open_obligations'])==(37,24,8,1,4); assert p['completed_waves']==['W0','W1','W2','W3'] and p['active_wave']=='W4' and p['active_obligations']==['OBS-SC-010']
    family={x['id']:x for x in t['theorem_family']}; assert all(x.get('status')!='proved' for x in family.values()); assert family['THM-CORE-COMMON-001']['blocked_by']==['formal_negative_controls','theorem_assembly']; assert family['THM-CORE-REP-001']['blocked_by']==['formal_negative_controls','theorem_assembly']; assert family['THM-IMP-001']['blocked_by']==['formal_negative_controls','theorem_assembly']; assert t['next_required_artifact'].startswith('W4 formal negative-control')
    prem=load(PREMISES); assert prem['version']=='1.6'; progress=prem['proof_progress']; assert all(progress[x] is False for x in ('premise_change','source_scope_change','target_interface_change','theorem_status_change'))
    s=load(LEMMA)['execution_summary']; assert (s['proved'],s['scope_boundary_established'],s['refuted'],s['open'])==(24,1,8,4)
    assert [load(x)['proof_id'] for x in PROOFS]==['SCORE-W0-PROOF-001','SCORE-W1-PROOF-001','SCORE-W2-PROOF-001','SCORE-W3-PROOF-001']
    gates={x['name']:x for x in load(GATES)['gates']}; assert gates['formal-theorem-target']['status']=='satisfied' and gates['premise-ledger-and-semantics']['status']=='satisfied' and gates['faithful-representation-definition']['status']=='satisfied'; assert gates['scoped-representation-proof']['status']=='not_satisfied' and gates['scoped-representation-proof']['evidence']==[]
    for claim in load(CLAIMS)['claims']:
        if claim['id'] in {'CLM-EXISTENCE','CLM-UNIVERSALITY','CLM-NECESSITY','CLM-MINIMALITY'}: assert claim['current_status']!='supported'
    print('THM-TARGET-001 validation: PASS (all construction lemmas proved; negative controls and W5 open; theorem unproved)'); return 0
if __name__=='__main__': raise SystemExit(main())
