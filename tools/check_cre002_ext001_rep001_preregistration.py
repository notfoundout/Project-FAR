#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001-REP-001'
FILES = ['README.md','preregistration.md','isolation-protocol.json','decision-rules.json','output-schema.json','package-manifest.json','execution-lock.json']


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    for name in FILES:
        if not (PKG / name).is_file():
            fail(f'missing file: {name}')
    isolation = json.loads((PKG / 'isolation-protocol.json').read_text())
    rules = json.loads((PKG / 'decision-rules.json').read_text())
    manifest = json.loads((PKG / 'package-manifest.json').read_text())
    lock = json.loads((PKG / 'execution-lock.json').read_text())
    json.loads((PKG / 'output-schema.json').read_text())
    if isolation.get('minimum_implementation_teams', 0) < 2:
        fail('at least two implementation teams are required')
    if isolation.get('minimum_verifier_teams', 0) < 1:
        fail('an independent verifier team is required')
    if isolation['team_separation'].get('shared_personnel_permitted') is not False:
        fail('shared personnel must be prohibited')
    if isolation['team_separation'].get('verifier_personnel_may_build_candidates') is not False:
        fail('verifier personnel must be independent')
    if 'contaminated' not in rules.get('submission_outcomes', {}):
        fail('contaminated outcome missing')
    if 'inconclusive' not in rules.get('submission_outcomes', {}):
        fail('inconclusive outcome missing')
    if manifest.get('checksum_state') != 'locked':
        fail('checksum state must remain locked')
    if not (PKG / 'checksum-lock.json').is_file():
        fail('locked package requires checksum-lock.json')
    subprocess.run([sys.executable, 'tools/check_cre002_ext001_rep001_checksums.py'], cwd=ROOT, check=True)
    phase = manifest.get('status')
    if phase not in {'preregistered-checksum-locked', 'team-registration-open'}:
        fail(f'unsupported administrative phase: {phase}')
    if lock.get('state') not in {'locked', 'team-registration-open-execution-locked'}:
        fail('execution lock state is invalid')
    for key in ('execution_authorized','compiler_implementation_authorized','official_results_present'):
        if manifest.get(key) is not False or lock.get(key) is not False:
            fail(f'{key} must remain false')
    if phase == 'team-registration-open':
        if manifest.get('team_registration_authorized') is not True:
            fail('manifest must authorize team registration')
        if lock.get('team_registration_authorized') is not True:
            fail('execution control must authorize team registration')
        for name in ('team-registration-schema.json', 'team-registry.json'):
            if not (PKG / name).is_file():
                fail(f'missing registration control: {name}')
    for name in ('generated','results','submissions'):
        if (PKG / name).exists():
            fail(f'forbidden pre-execution path exists: {name}')
    print('CRE-002-EXT-001-REP-001 PREREGISTRATION CHECK PASSED')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
