#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'docs/research/external-falsification-and-replication/external-handoff-v1.0'
FREEZE=ROOT/'theory/evaluation/external-falsification-and-replication-input-freeze-v1.0.json'
EXPECTED_COMMIT='195fc079d0a8993e4db3e063e09cf45d0bcd78c2'
EXPECTED_TREE='a01517ed65f45e62b3d47ffba9dc955fff2bae9b'

def die(msg):
    print(f'EFR external handoff check: FAIL: {msg}')
    return 1

def main():
    verifier=PKG/'verify_packet.py'
    if not verifier.is_file(): return die('missing embedded verifier')
    run=subprocess.run([sys.executable,str(verifier)],cwd=PKG,text=True,capture_output=True)
    if run.returncode:
        print(run.stdout,end=''); print(run.stderr,end='',file=sys.stderr)
        return die('embedded packet verification failed')
    try: freeze=json.loads(FREEZE.read_text(encoding='utf-8'))
    except Exception as e: return die(f'cannot parse canonical EFR input freeze: {e}')
    base=freeze.get('evidence_baseline',{})
    if base.get('commit')!=EXPECTED_COMMIT or base.get('tree')!=EXPECTED_TREE: return die('canonical EFR scientific baseline changed')
    results=freeze.get('current_results',{})
    if results.get('tests_executed')!=0 or results.get('external_cases')!=0 or results.get('human_participants')!=0 or results.get('field_sites')!=0 or results.get('novelty_status')!='NO_CLAIM': return die('EFR freeze no longer represents pre-execution state')
    print(run.stdout.strip())
    print('EFR external handoff check: PASS (handoff frozen; EFR remains unexecuted)')
    return 0

if __name__=='__main__': raise SystemExit(main())
