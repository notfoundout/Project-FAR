#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/sc-w4-representation-escape-v1.0.json'
DOC=ROOT/'docs/research/sc-w4-representation-escape-v1.0.md'
AUDIT=ROOT/'docs/audits/sc-w4-representation-escape-audit.md'
def load(path:Path)->dict:return json.loads(path.read_text(encoding='utf-8'))
def main()->int:
    for path in (RESULT,DOC,AUDIT): assert path.is_file(),path
    data=load(RESULT)
    assert data['result_id']=='SC-W4-REPRESENTATION-ESCAPE-001'
    assert data['status']=='complete_internal_representation_escape_search'
    assert data['target_pr']==273
    assert len(data['representation_families'])==12
    assert len(data['escape_attempts'])==12
    assert len(data['hidden_machinery_ledger'])>=10
    assert all(x['result']!='escape' for x in data['representation_families'])
    outcomes={x['outcome'] for x in data['escape_attempts']}
    assert {'fails_contract','inadmissible_nonuniform','outside_effective_family','equivalent_reintroduction'}<=outcomes
    assert data['terminal_result']=='no_faithful_effective_representation_escape_found_across_broadened_families_without_rccd_equivalent_reintroduction'
    assert data['next_decisive_workstream']=='SC-W5-HELD-OUT-CONTEXTS'
    assert 'all mathematically possible representations have been enumerated' in data['nonclaims']
    assert 'the final internal answer has been issued' in data['nonclaims']
    text=DOC.read_text(encoding='utf-8'); audit=AUDIT.read_text(encoding='utf-8')
    assert 'Adversarial escape mechanisms' in text
    assert 'External review and independent replication remain deferred' in audit
    print('SC-W4 representation escape search: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
