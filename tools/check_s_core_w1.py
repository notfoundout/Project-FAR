#!/usr/bin/env python3
"""Validate retained SCORE-W1-PROOF-001 after later wave progress."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/s-core-w1-direct-axis-proof-v1.0.md'; REG=ROOT/'theory/evaluation/s-core-w1-direct-axis-proof.json'; FIX=ROOT/'theory/evaluation/s-core-w1-reference-fixtures.json'; LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; GATES=ROOT/'theory/evaluation/research-gates.json'; REF=ROOT/'tools/s_core_w1_reference.py'; TEST=ROOT/'tests/test_s_core_w1_reference.py'; AUDIT=ROOT/'docs/audits/s-core-w1-proof-audit.md'; MAKE=ROOT/'Makefile'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
    for p in (DOC,REG,FIX,LEDGER,TARGET,GATES,REF,TEST,AUDIT,MAKE): assert p.is_file(),p
    proof=load(REG); assert proof['proof_id']=='SCORE-W1-PROOF-001'; results={x['id']:x for x in proof['results']}; proved={'LEM-SC-005','LEM-SC-006','LEM-SC-007','LEM-SC-008','LEM-SC-009','LEM-SC-012','LEM-SC-014'}; refuted={'OBS-SC-003','OBS-SC-006'}; assert all(results[x]['status']=='proved' for x in proved); assert all(results[x]['status']=='refuted' for x in refuted); assert proof['construction_properties']['complete_global_recovery_proved'] is False
    ledger=load(LEDGER); by={x['id']:x for x in ledger['obligations']}; assert all(by[x]['status']=='proved' for x in proved); assert all(by[x]['status']=='refuted' for x in refuted); assert ledger['completed_waves'][:2]==['W0','W1']; assert ledger['execution_summary']['proved']>=11 and ledger['execution_summary']['refuted']>=2 and ledger['execution_summary']['open']<=23
    target=load(TARGET); assert target['lemma_program']['completed_waves'][:2]==['W0','W1'] and target['proof_status']=='partial_lemma_progress_only'
    gates={x['name']:x for x in load(GATES)['gates']}; assert gates['scoped-representation-proof']['status']=='not_satisfied' and gates['mechanized-proof-verification']['status']=='not_satisfied' and gates['independent-proof-review']['status']=='not_satisfied'
    assert MAKE.read_text(encoding='utf-8').count('python tools/check_s_core_w1.py')==3
    cp=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_s_core_w1_reference.py'],cwd=ROOT,text=True,capture_output=True); assert cp.returncode==0,cp.stdout+cp.stderr
    print('S_core W1 proof: PASS (retained after W3; direct-axis results remain established)'); return 0
if __name__=='__main__': raise SystemExit(main())
