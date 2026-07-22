#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/sc-w2-boundary-reasoning-v1.0.json'
DOC=ROOT/'docs/research/sc-w2-boundary-reasoning-v1.0.md'
AUDIT=ROOT/'docs/audits/sc-w2-boundary-reasoning-audit.md'
def main()->int:
    for p in (RESULT,DOC,AUDIT): assert p.is_file(),p
    d=json.loads(RESULT.read_text(encoding='utf-8'))
    assert d['result_id']=='SC-W2-BOUNDARY-REASONING-001'
    assert d['status']=='complete_internal_boundary_adjudication'
    assert d['target_pr']==271
    assert len(d['cases'])==12
    assert d['counterexample_search']['genuine_new_primitive_found'] is False
    assert d['counterexample_search']['rccd_component_evaded_by_assessable_faithful_case'] is False
    assert len(d['counterexample_search']['blocking_cases'])==2
    assert d['terminal_result']=='no_boundary_case_yet_requires_new_kernel_primitive_but_evidential_boundary_must_remain_open'
    assert d['next_decisive_workstream']=='SC-W3-CONTRACT-LADDER'
    assert 'normatively assessable' in d['membership_rule']
    assert any(c['classification'].startswith('unassessable') for c in d['cases'])
    assert 'final internal answer established' in d['nonclaims']
    print('SC-W2 boundary reasoning: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
