#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'mechanization/lean/SCoreW5.lean'; DOC=ROOT/'docs/research/s-core-w5-lean-mechanization-v1.0.md'; REG=ROOT/'theory/evaluation/s-core-w5-lean-mechanization.json'; W5=ROOT/'theory/evaluation/s-core-w5-theorem-assembly-proof.json'; MAKE=ROOT/'Makefile'; WF=ROOT/'.github/workflows/lean.yml'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def main()->int:
 for p in (LEAN,DOC,REG,W5,MAKE,WF): assert p.is_file(),p
 text=LEAN.read_text(encoding='utf-8')
 for token in ('namespace FAR.SCoreW5','theorem asm_sc_001_common_schema','theorem asm_sc_002_bounded_faithful_representation','theorem asm_sc_003_theorem_family','theorem thm_core_rep_001','theorem bounded_impossibility_refuted'): assert token in text,token
 lowered=text.lower(); assert 'sorry' not in lowered and 'admit' not in lowered and '\naxiom ' not in lowered
 r=load(REG); assert r['mechanization_id']=='SCORE-W5-LEAN-001'; assert r['status']=='machine_checked_bounded_theorem'; assert r['source_scope']=='S_core'; assert r['faithful_predicate']=='Faithful_split'; assert len(r['compiled_theorems'])==5; assert r['claim_effect']['universal_structure']=='unresolved'; assert r['claim_effect']['independent_proof_review']=='not_started'
 w=load(W5); assert w['proof_id']=='SCORE-W5-PROOF-001'; assert w['claim_effect']['bounded_faithful_representation']=='proved'; assert w['claim_effect']['S_IRD_representation']=='unresolved'
 assert MAKE.read_text(encoding='utf-8').count('python tools/check_s_core_w5_mechanization.py')==3
 workflow=WF.read_text(encoding='utf-8'); assert 'lean mechanization/lean/SCoreW5.lean' in workflow; assert 'python -m unittest tests.test_s_core_w5_lean_alignment' in workflow
 print('S_core W5 Lean mechanization: PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
