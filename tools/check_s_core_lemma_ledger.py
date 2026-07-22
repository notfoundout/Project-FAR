#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/s-core-construction-obstruction-ledger-v1.0.md'; REG=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; GATES=ROOT/'theory/evaluation/research-gates.json'; MAKE=ROOT/'Makefile'
PROOFS={'W0':(ROOT/'docs/research/s-core-w0-normalization-proof-v1.0.md',ROOT/'theory/evaluation/s-core-w0-normalization-proof.json'),'W1':(ROOT/'docs/research/s-core-w1-direct-axis-proof-v1.0.md',ROOT/'theory/evaluation/s-core-w1-direct-axis-proof.json'),'W2':(ROOT/'docs/research/s-core-w2-dynamics-history-proof-v1.0.md',ROOT/'theory/evaluation/s-core-w2-dynamics-history-proof.json'),'W3':(ROOT/'docs/research/s-core-w3-global-witness-proof-v1.0.md',ROOT/'theory/evaluation/s-core-w3-global-witness-proof.json'),'W4':(ROOT/'docs/research/s-core-w4-negative-control-proof-v1.0.md',ROOT/'theory/evaluation/s-core-w4-negative-control-proof.json')}
WAVE_ORDER={f'W{i}':i for i in range(6)}; TERMINAL={'proved','refuted','obstruction_established','scope_boundary_established','superseded'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dag(items):
    by={x['id']:x for x in items}; incoming={k:set(v.get('depends_on',[])) for k,v in by.items()}; outgoing=defaultdict(set)
    for k,deps in incoming.items():
        assert deps<=set(by) and k not in deps
        for d in deps: assert WAVE_ORDER[by[d]['wave']]<=WAVE_ORDER[by[k]['wave']]; outgoing[d].add(k)
    ready=deque(sorted(k for k,v in incoming.items() if not v)); seen=[]
    while ready:
        k=ready.popleft(); seen.append(k)
        for child in outgoing[k]:
            incoming[child].remove(k)
            if not incoming[child]: ready.append(child)
    assert len(seen)==len(items),'dependency graph must be acyclic'
def main()->int:
    paths=[DOC,REG,TARGET,GATES,MAKE]+[p for pair in PROOFS.values() for p in pair]
    for p in paths: assert p.is_file(),p
    assert 'S_core Construction and Obstruction Lemma Ledger v1.0' in DOC.read_text(encoding='utf-8')
    d=load(REG); assert d['schema_version']=='1.0' and d['ledger_id']=='SCORE-LEMMA-LEDGER-001' and d['version']=='1.0'; assert d['status']=='frozen_dependency_decomposition_w0_w1_w2_w3_w4_complete_w5_blocked_by_w3_5'; assert d['statement_authority']=='source_artifact' and d['source_artifact']==DOC.relative_to(ROOT).as_posix(); assert set(d['waves'])==set(WAVE_ORDER); assert d['completed_waves']==['W0','W1','W2','W3','W4']; assert d['active_wave']=='W5_blocked'; assert d['active_obligations']==[]; assert set(d['blocked_obligations'])=={'ASM-SC-001','ASM-SC-002','ASM-SC-003'}; assert d['external_blockers']==['W3.5-SDG-001']; assert d['proof_packages']==[PROOFS[x][1].relative_to(ROOT).as_posix() for x in ('W0','W1','W2','W3','W4')]
    items=d['obligations']; assert len(items)==37; ids={x['id'] for x in items}; assert ids=={*[f'LEM-SC-{i:03d}' for i in range(1,25)],*[f'OBS-SC-{i:03d}' for i in range(1,11)],*[f'ASM-SC-{i:03d}' for i in range(1,4)]}; assert Counter(x['class'] for x in items)=={'construction':24,'obstruction':10,'assembly':3}; dag(items)
    by={x['id']:x for x in items}; assert all(by[f'LEM-SC-{i:03d}']['status']=='proved' for i in range(1,25)); assert by['OBS-SC-001']['status']=='scope_boundary_established'; assert all(by[f'OBS-SC-{i:03d}']['status']=='refuted' for i in range(2,10)); assert by['OBS-SC-010']['status']=='obstruction_established'; assert all(by[f'ASM-SC-{i:03d}']['status']=='registered_unproved' for i in range(1,4))
    for x in items:
        assert isinstance(x.get('evidence'),list)
        if x['status'] in TERMINAL:
            assert x['evidence']
            for rel in x['evidence']: assert (ROOT/rel).is_file(),rel
        else: assert x['evidence']==[]
    counts=Counter(x['status'] for x in items); s=d['execution_summary']; assert s=={'total':37,'construction':24,'obstruction':10,'assembly':3,'proved':24,'obstruction_established':1,'scope_boundary_established':1,'refuted':8,'open':3}; assert counts['proved']==24 and counts['refuted']==8 and counts['obstruction_established']==1 and counts['scope_boundary_established']==1 and counts['registered_unproved']==3
    t=load(TARGET)['lemma_program']; assert t['status']=='w0_w1_w2_w3_w4_complete_w5_authorized' and t['proved_obligations']==24 and t['established_obstructions']==1 and t['refuted_obstruction_hypotheses']==8 and t['open_obligations']==3 and set(t['active_obligations'])=={'ASM-SC-001','ASM-SC-002','ASM-SC-003'} and t['active_wave']=='W5'
    gates=load(GATES); req=set(gates['required_canonical_artifacts']); canonical_paths=[DOC,REG,TARGET]+[p for pair in PROOFS.values() for p in pair]
    for p in canonical_paths: assert p.relative_to(ROOT).as_posix() in req,p
    g={x['name']:x for x in gates['gates']}; assert g['formal-negative-controls']['status']=='satisfied'; assert g['scoped-representation-proof']['status']=='not_satisfied' and g['scoped-representation-proof']['evidence']==[]; assert g['baseline-factorization-resolved']['status']=='satisfied' and g['baseline-factorization-resolved']['evidence']; assert g['fara-specificity-resolved']['status']=='satisfied' and g['fara-specificity-resolved']['evidence']; assert g['reasoning-contrast-execution']['status']=='satisfied' and g['reasoning-contrast-execution']['evidence']; assert g['universal-structure-result']['status']=='not_satisfied'
    make=MAKE.read_text(encoding='utf-8')
    for checker in ('check_s_core_lemma_ledger.py','check_s_core_w0.py','check_s_core_w1.py','check_s_core_w2.py','check_s_core_w3.py','check_s_core_w4.py'): assert make.count(f'python tools/{checker}')==3
    print('S_core lemma ledger: PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
