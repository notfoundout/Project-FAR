#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/s-core-construction-obstruction-ledger-v1.0.md'; REG=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; GATES=ROOT/'theory/evaluation/research-gates.json'; MAKE=ROOT/'Makefile'
PROOFS={'W0':(ROOT/'docs/research/s-core-w0-normalization-proof-v1.0.md',ROOT/'theory/evaluation/s-core-w0-normalization-proof.json'),'W1':(ROOT/'docs/research/s-core-w1-direct-axis-proof-v1.0.md',ROOT/'theory/evaluation/s-core-w1-direct-axis-proof.json'),'W2':(ROOT/'docs/research/s-core-w2-dynamics-history-proof-v1.0.md',ROOT/'theory/evaluation/s-core-w2-dynamics-history-proof.json'),'W3':(ROOT/'docs/research/s-core-w3-global-witness-proof-v1.0.md',ROOT/'theory/evaluation/s-core-w3-global-witness-proof.json'),'W4':(ROOT/'docs/research/s-core-w4-negative-control-proof-v1.0.md',ROOT/'theory/evaluation/s-core-w4-negative-control-proof.json'),'W5':(ROOT/'docs/research/s-core-w5-theorem-assembly-proof-v1.0.md',ROOT/'theory/evaluation/s-core-w5-theorem-assembly-proof.json')}
WAVE_ORDER={f'W{i}':i for i in range(6)}; TERMINAL={'proved','refuted','obstruction_established','scope_boundary_established','superseded'}
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dag(items):
 by={x['id']:x for x in items}; incoming={k:set(v.get('depends_on',[])) for k,v in by.items()}; outgoing=defaultdict(set)
 for k,deps in incoming.items():
  assert deps<=set(by) and k not in deps
  for dep in deps:
   assert WAVE_ORDER[by[dep]['wave']]<=WAVE_ORDER[by[k]['wave']]
   outgoing[dep].add(k)
 ready=deque(sorted(k for k,v in incoming.items() if not v)); seen=[]
 while ready:
  k=ready.popleft(); seen.append(k)
  for child in outgoing[k]:
   incoming[child].remove(k)
   if not incoming[child]: ready.append(child)
 assert len(seen)==len(items)
def main()->int:
 paths=[DOC,REG,TARGET,GATES,MAKE]+[p for pair in PROOFS.values() for p in pair]
 for p in paths: assert p.is_file(),p
 d=load(REG); assert d['schema_version']=='1.0' and d['ledger_id']=='SCORE-LEMMA-LEDGER-001' and d['version']=='1.1'
 if d['status']=='w0_w1_w2_w3_w4_w5_complete_bounded_theorem_proved':
  assert d['completed_waves']==['W0','W1','W2','W3','W4','W5']; assert d['active_wave']=='complete'; assert d['active_obligations']==[] and d['blocked_obligations']==[] and d['external_blockers']==[]
 else:
  raise AssertionError('unexpected ledger status')
 assert d['proof_packages']==[PROOFS[x][1].relative_to(ROOT).as_posix() for x in ('W0','W1','W2','W3','W4','W5')]
 items=d['obligations']; assert len(items)==37; dag(items); by={x['id']:x for x in items}; assert all(by[f'LEM-SC-{i:03d}']['status']=='proved' for i in range(1,25)); assert by['OBS-SC-001']['status']=='scope_boundary_established'; assert all(by[f'OBS-SC-{i:03d}']['status']=='refuted' for i in range(2,10)); assert by['OBS-SC-010']['status']=='obstruction_established'; assert all(by[f'ASM-SC-{i:03d}']['status']=='proved' for i in range(1,4))
 for item in items:
  assert isinstance(item.get('evidence'),list)
  if item['status'] in TERMINAL:
   assert item['evidence']
   for rel in item['evidence']: assert (ROOT/rel).is_file(),rel
 counts=Counter(x['status'] for x in items); summary=d['execution_summary']; assert summary=={'total':37,'construction':24,'obstruction':10,'assembly':3,'proved':27,'obstruction_established':1,'scope_boundary_established':1,'refuted':8,'open':0}; assert counts['proved']==27; assert counts['obstruction_established']==1; assert counts['scope_boundary_established']==1; assert counts['refuted']==8
 target=load(TARGET)['lemma_program']; assert target['status']=='w0_w1_w2_w3_w4_w5_complete_bounded_theorem_proved'; assert target['proved_obligations']==27; assert target['open_obligations']==0; assert target['active_wave']=='complete'; assert target['active_obligations']==[]; assert target['blocked_obligations']==[]
 make=MAKE.read_text(encoding='utf-8')
 for checker in ('check_s_core_lemma_ledger.py','check_s_core_w0.py','check_s_core_w1.py','check_s_core_w2.py','check_s_core_w3.py','check_s_core_w4.py','check_s_core_w5.py'): assert make.count(f'python tools/{checker}')==3
 print('S_core lemma ledger: PASS (W5 complete)'); return 0
if __name__=='__main__': raise SystemExit(main())
