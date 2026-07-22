#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROGRAM=ROOT/'theory/evaluation/post-w9-internal-scope-challenge-v1.0.json'
QUEUE=ROOT/'theory/evaluation/post-w9-internal-scope-challenge-queue-v1.0.json'
DOC=ROOT/'docs/research/post-w9-internal-scope-challenge-v1.0.md'
def load(path:Path)->dict:return json.loads(path.read_text(encoding='utf-8'))
def main()->int:
    for path in (PROGRAM,QUEUE,DOC): assert path.is_file(),path
    program=load(PROGRAM); queue=load(QUEUE)
    assert program['program_id']=='POST-W9-SCOPE-CHALLENGE-001'
    assert program['status']=='registered_unexecuted'
    assert program['external_disposition']=='deferred_until_final_internal_adjudication'
    assert len(program['workstreams'])==6
    assert [x['sequence'] for x in program['workstreams']]==list(range(1,7))
    assert [x['target_pr'] for x in program['workstreams']]==list(range(270,276))
    assert len(program['terminal_outcomes'])==6
    assert 'current_theorem_scope_construct_loaded' in program['terminal_outcomes']
    assert len(program['downgrade_rules'])==6
    assert queue['queue_id']=='POST-W9-SCOPE-CHALLENGE-QUEUE-001'
    assert queue['next_action']['target_pr']==270
    assert queue['next_action']['workstream']=='SC-W1-SCOPE-NEUTRALITY'
    assert queue['ordered_followups']==[271,272,273,274,275]
    text=DOC.read_text(encoding='utf-8')
    assert 'External hold' in text
    assert 'construct-loaded' in text
    print('POST-W9 internal scope challenge: PASS (PR #270 authorized; external work deferred)')
    return 0
if __name__=='__main__': raise SystemExit(main())
