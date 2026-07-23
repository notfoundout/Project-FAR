#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, subprocess, sys, importlib.util
R=pathlib.Path(__file__).resolve().parents[1]
SPEC=R/'theory/evaluation/pte-w1-independent-review-v1.0.json'
MODEL=R/'theory/evaluation/pte_independent_review_v1.py'
RESULT=R/'theory/evaluation/pte-w1-independent-review-result-v1.0.json'
PROGRAM=R/'theory/evaluation/post-terminal-public-evaluation-program-v1.0.json'

def fail(x): raise SystemExit('FAIL: '+x)
def load(p): return json.loads(p.read_text())
def main():
 for p in (SPEC,MODEL,RESULT,PROGRAM):
  if not p.is_file(): fail(f'missing {p.relative_to(R)}')
 s,r,p=load(SPEC),load(RESULT),load(PROGRAM)
 if s['workstream']!='PTE-W1-INDEPENDENT-REVIEW': fail('workstream mismatch')
 if s['internal_agent_execution_counts_as_independent_review'] is not False: fail('anti-self-validation weakened')
 if r['outcome']!='independent_review_protocol_frozen_external_review_not_yet_executed': fail('result mismatch')
 if r['evidential_status']!='Unknown': fail('pending external review must remain Unknown')
 if p['next_action']['workstream']!='PTE-W1-EXTERNAL-REVIEW-EXECUTION': fail('program not advanced')
 q=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_pte_w1_independent_review.py'],cwd=R,text=True,capture_output=True)
 if q.returncode: sys.stderr.write(q.stdout+q.stderr); fail('tests failed')
 print('PASS: PTE-W1 independent review package is frozen and non-self-validating')
 return 0
if __name__=='__main__': raise SystemExit(main())
