#!/usr/bin/env python3
"""Validate retained SCORE-W2-PROOF-001 after later wave progress."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/s-core-w2-dynamics-history-proof-v1.0.md'; REG=ROOT/'theory/evaluation/s-core-w2-dynamics-history-proof.json'; FIX=ROOT/'theory/evaluation/s-core-w2-reference-fixtures.json'; LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; GATES=ROOT/'theory/evaluation/research-gates.json'; REF=ROOT/'tools/s_core_w2_reference.py'; TEST=ROOT/'tests/test_s_core_w2_reference.py'; AUDIT=ROOT/'docs/audits/s-core-w2-proof-audit.md'; MAKE=ROOT/'Makefile'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
    for p in (DOC,REG,FIX,LEDGER,TARGET,GATES,REF,TEST,AUDIT,MAKE): assert p.is_file(),p
    proof=load(REG); assert proof['proof_id']=='SCORE-W2-PROOF-001' and proof['status']=='project_authored_human_checkable_proof'; results={x['id']:x for x in proof['results']}; assert all(results[x]['status']=='proved' for x in ('LEM-SC-010','LEM-SC-011','LEM-SC-013','LEM-SC-015','LEM-SC-016')); assert all(results[x]['status']=='refuted' for x in ('OBS-SC-004','OBS-SC-005')); assert proof['verification']['proof_assistant_status']=='not_started' and proof['verification']['independent_review_status']=='not_started'
    ledger=load(LEDGER); by={x['id']:x for x in ledger['obligations']}; assert all(by[x]['status']=='proved' for x in ('LEM-SC-010','LEM-SC-011','LEM-SC-013','LEM-SC-015','LEM-SC-016')); assert by['OBS-SC-004']['status']=='refuted' and by['OBS-SC-005']['status']=='refuted'; assert ledger['completed_waves'][:3]==['W0','W1','W2']; assert ledger['execution_summary']['proved']>=16 and ledger['execution_summary']['refuted']>=4 and ledger['execution_summary']['open']<=16
    target=load(TARGET); assert target['lemma_program']['completed_waves'][:3]==['W0','W1','W2']; assert target['proof_status'] in {'partial_lemma_progress_only','bounded_theorem_proved'} and target['independent_review_status']=='not_started'
    gates={x['name']:x for x in load(GATES)['gates']}; assert gates['mechanized-proof-verification']['status']=='not_satisfied' and gates['independent-proof-review']['status']=='not_satisfied'
    assert MAKE.read_text(encoding='utf-8').count('python tools/check_s_core_w2.py')==3
    cp=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_s_core_w2_reference.py'],cwd=ROOT,text=True,capture_output=True); assert cp.returncode==0,cp.stdout+cp.stderr
    print('S_core W2 proof: PASS (retained through W5)'); return 0
if __name__=='__main__': raise SystemExit(main())
