#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/sc-w3-contract-ladder-v1.0.json'
DOC=ROOT/'docs/research/sc-w3-contract-ladder-v1.0.md'
AUDIT=ROOT/'docs/audits/sc-w3-contract-ladder-audit.md'
def load(path:Path)->dict:return json.loads(path.read_text(encoding='utf-8'))
def main()->int:
    for path in (RESULT,DOC,AUDIT): assert path.is_file(),path
    data=load(RESULT)
    assert data['result_id']=='SC-W3-CONTRACT-LADDER-001'
    assert data['status']=='complete_internal_contract_ladder'
    assert data['target_pr']==272
    assert len(data['contract_ladder'])==5
    assert data['contract_ladder'][0]['required_rccd']==[]
    assert data['contract_ladder'][-1]['required_rccd']==['R1','R2','R3','R4','R5']
    assert len(data['single_duty_ablations'])==5
    removed={x['component_no_longer_forced'] for x in data['single_duty_ablations']}
    assert removed=={'R1','R2','R3','R4','R5'}
    assert len(data['alternative_contracts'])==4
    assert data['terminal_result']=='rccd_is_contract_relative_but_not_shown_construct_loaded_under_independently_justified_full_contract'
    assert data['next_decisive_workstream']=='SC-W4-REPRESENTATION-ESCAPE'
    findings=' '.join(data['neutrality_findings'])
    assert 'not contract-independent' in findings
    assert 'without being shown construct-loaded' in findings
    assert 'RCCD is necessary under every conceivable preservation contract' in data['nonclaims']
    text=DOC.read_text(encoding='utf-8'); audit=AUDIT.read_text(encoding='utf-8')
    assert 'Generic residue' in text
    assert 'External review remains deferred' in audit
    print('SC-W3 contract ladder: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
