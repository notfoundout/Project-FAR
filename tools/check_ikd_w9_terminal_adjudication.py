#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'theory/evaluation/ikd-w9-terminal-adjudication-v1.0.json'
RESEARCH=ROOT/'docs/research/ikd-w9-terminal-adjudication-v1.0.md'
AUDIT=ROOT/'docs/audits/ikd-w9-terminal-adjudication-audit.md'
def main()->int:
    for path in (RESULT,RESEARCH,AUDIT): assert path.is_file(),path
    data=json.loads(RESULT.read_text(encoding='utf-8'))
    assert data['result_id']=='IKD-W9-TERMINAL-ADJUDICATION-001'
    assert data['status']=='complete_internal_terminal_adjudication'
    assert data['target_pr']==269
    assert len(data['evidence_basis'])==8
    scope=data['scope']
    assert scope['universality_class']['id']=='C-EFFECTIVE-REASONING-001'
    assert scope['preservation_contract']['id']=='P-RCCD-FAITHFUL-001'
    assert scope['representation_family']['id']=='E-EFFECTIVE-REP-001'
    assert data['terminal_outcome']=='one_nontrivial_common_kernel'
    assert data['kernel']['id']=='RCCD-001'
    assert len(data['kernel']['necessary_commitments'])==5
    theorem=data['bounded_theorem']
    for token in ('every system in C-EFFECTIVE-REASONING-001','R1-R5','necessary nontrivial common kernel','relative to P and E'): assert token in theorem
    assert data['terminal_result']=='bounded_rccd_universality_theorem_supported_internally'
    assert data['program_status']=='internal_discovery_program_complete_external_validation_pending'
    claims='\n'.join(data['excluded_claims'])
    for token in ('unrestricted universality','actual brains','independent proof review','global ontological minimality'): assert token in claims
    assert len(data['external_requirements'])>=5
    stop=data['post_internal_stopping_rule']; assert len(stop['reopen_conditions'])==4
    answer=data['internal_answer']; assert answer.startswith('Yes.'); assert 'An unrestricted claim' in answer
    research=RESEARCH.read_text(encoding='utf-8'); audit=AUDIT.read_text(encoding='utf-8')
    assert 'bounded universality theorem' in research
    assert 'Internal CI is evidence of repository consistency, not independent scientific validation' in audit
    print('IKD-W9 terminal adjudication: PASS (bounded RCCD universality theorem supported internally)')
    return 0
if __name__=='__main__': raise SystemExit(main())
