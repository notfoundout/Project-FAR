#!/usr/bin/env python3
"""Validate retained SCORE-W0-PROOF-001 after later wave progress."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'docs/research/s-core-w0-normalization-proof-v1.0.md'; REG=ROOT/'theory/evaluation/s-core-w0-normalization-proof.json'; FIX=ROOT/'theory/evaluation/s-core-w0-reference-fixtures.json'; LEDGER=ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; GATES=ROOT/'theory/evaluation/research-gates.json'; REF=ROOT/'tools/s_core_w0_reference.py'; TEST=ROOT/'tests/test_s_core_w0_reference.py'; AUDIT=ROOT/'docs/audits/s-core-w0-proof-audit.md'; MAKE=ROOT/'Makefile'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
    for p in (DOC,REG,FIX,LEDGER,TARGET,GATES,REF,TEST,AUDIT,MAKE): assert p.is_file(),p
    text=DOC.read_text(encoding='utf-8')
    for phrase in ('S_core W0 Normalization Kernel Proof v1.0','SCORE-W0-PROOF-001','Therefore `LEM-SC-001` is proved','Therefore `LEM-SC-004` is proved','OBS-SC-001` is resolved as `scope_boundary_established','No FARA target component','proof-assistant verification or independent proof review'): assert phrase in text
    proof=load(REG); assert proof['proof_id']=='SCORE-W0-PROOF-001' and proof['status']=='project_authored_human_checkable_proof'; assert proof['proof_artifact']==DOC.relative_to(ROOT).as_posix(); assert proof['reference_implementation']==REF.relative_to(ROOT).as_posix(); assert proof['reference_tests']==TEST.relative_to(ROOT).as_posix()
    results={x['id']:x for x in proof['results']}; assert all(results[x]['status']=='proved' for x in ('LEM-SC-001','LEM-SC-002','LEM-SC-003','LEM-SC-004')); assert results['OBS-SC-001']['status']=='scope_boundary_established'
    verification=proof['verification']; assert verification['human_proof_status']=='complete_project_authored'; assert verification['machine_check_status']=='bounded_executable_reference_only'; assert verification['proof_assistant_status']=='not_started'; assert verification['independent_review_status']=='not_started'
    assert proof['ledger_effect']=={'proved_obligations':4,'scope_boundaries_established':1,'open_obligations':32,'completed_wave':'W0','active_wave':'W1'}
    ledger=load(LEDGER); by_id={x['id']:x for x in ledger['obligations']}; assert all(by_id[x]['status']=='proved' for x in ('LEM-SC-001','LEM-SC-002','LEM-SC-003','LEM-SC-004')); assert by_id['OBS-SC-001']['status']=='scope_boundary_established'; assert ledger['completed_waves'][:1]==['W0']; assert ledger['execution_summary']['proved']>=4; assert ledger['execution_summary']['open']<=32
    target=load(TARGET); assert target['lemma_program']['completed_waves'][0]=='W0'; assert target['lemma_program']['proved_obligations']>=4; assert target['proof_status']=='partial_lemma_progress_only'; assert target['independent_review_status']=='not_started'
    gates={x['name']:x for x in load(GATES)['gates']}; assert gates['scoped-representation-proof']['status']=='not_satisfied'; assert gates['mechanized-proof-verification']['status']=='not_satisfied'; assert gates['independent-proof-review']['status']=='not_satisfied'
    assert MAKE.read_text(encoding='utf-8').count('python tools/check_s_core_w0.py')==3
    cp=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_s_core_w0_reference.py'],cwd=ROOT,text=True,capture_output=True); assert cp.returncode==0,cp.stdout+cp.stderr
    print('S_core W0 proof: PASS (retained after W2; 4 lemmas and 1 boundary remain established)')
    return 0
if __name__=='__main__': raise SystemExit(main())
