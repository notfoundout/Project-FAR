#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001'
REQUIRED = [
    'README.md',
    'preregistration.md',
    'scenario/scenario-v1.0.json',
    'ambiguity-policies.json',
    'decision-rules.json',
    'output-schema.json',
    'package-manifest.json',
    'execution-lock.json',
]
NONCLAIMS = {
    'universal sufficiency',
    'primitive-only sufficiency',
    'necessity',
    'minimality',
    'independence',
    'superiority',
    'FAR proof',
    'universal structure of reasoning',
    'retrospective validation of CRE-002',
}


def load(name: str):
    return json.loads((PKG / name).read_text())


def verify_checksums(errors: list[str]) -> None:
    checksum_path = PKG / 'checksum-lock.json'
    if not checksum_path.is_file():
        errors.append('locked state requires checksum-lock.json')
        return
    cp = subprocess.run(
        [sys.executable, 'tools/check_cre002_ext001_checksums.py'],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if cp.returncode != 0:
        errors.append('locked state checksum verification failed')


def validate_authorized_state(manifest: dict, lock: dict, errors: list[str]) -> None:
    audit_path = PKG / 'execution-unlock-audit.json'
    if not audit_path.is_file():
        errors.append('authorized state requires execution-unlock-audit.json')
        return
    audit = load('execution-unlock-audit.json')
    if manifest.get('status') != 'execution-authorized':
        errors.append('authorized manifest must have execution-authorized status')
    if lock.get('status') != 'execution-authorized' or lock.get('authorization_status') != 'authorized':
        errors.append('execution lock authorization fields are inconsistent')
    if manifest.get('execution_permitted') is not True or lock.get('execution_permitted') is not True:
        errors.append('authorized state must permit execution')
    if manifest.get('compiler_implementation_permitted') is not True or lock.get('compiler_implementation_permitted') is not True:
        errors.append('authorized state must permit compiler implementation')
    if audit.get('authorization_status') != 'authorized' or audit.get('status') != 'execution-authorized':
        errors.append('execution unlock audit is not authorized')
    if audit.get('immutable_package_lock_verified') is not True:
        errors.append('execution unlock audit must verify the immutable package lock')
    if audit.get('scientific_results_created_by_unlock') is not False:
        errors.append('unlock audit must not create scientific results')
    if audit.get('execution_permitted_after_merge') is not True:
        errors.append('unlock audit must authorize execution after merge')
    if audit.get('compiler_implementation_permitted_after_merge') is not True:
        errors.append('unlock audit must authorize compiler implementation after merge')
    if not NONCLAIMS.issubset(set(audit.get('nonclaims_preserved', []))):
        errors.append('unlock audit omits required nonclaims')


def main() -> int:
    errors: list[str] = []
    for name in REQUIRED:
        if not (PKG / name).is_file():
            errors.append(f'missing {name}')
    if errors:
        print('CRE-002-EXT-001 PREREGISTRATION FAILED')
        print('\n'.join(errors))
        return 1

    manifest = load('package-manifest.json')
    lock = load('execution-lock.json')
    scenario = load('scenario/scenario-v1.0.json')
    rules = load('decision-rules.json')
    policies = load('ambiguity-policies.json')
    output = load('output-schema.json')

    if manifest.get('package_id') != 'CRE-002-EXT-001-PACKAGE-1.0':
        errors.append('wrong package id')

    checksum_state = manifest.get('checksum_state')
    if checksum_state not in {'pending', 'locked'}:
        errors.append('checksum state must be pending or locked')
    elif checksum_state == 'locked':
        verify_checksums(errors)

    authorized = (
        manifest.get('execution_permitted') is True
        or lock.get('execution_permitted') is True
        or manifest.get('status') == 'execution-authorized'
        or lock.get('status') == 'execution-authorized'
    )
    if authorized:
        if checksum_state != 'locked':
            errors.append('execution cannot be authorized before checksum lock')
        validate_authorized_state(manifest, lock, errors)
    else:
        if manifest.get('execution_permitted') is not False or lock.get('execution_permitted') is not False:
            errors.append('pre-authorization execution must remain locked')
        if manifest.get('compiler_implementation_permitted') is not False or lock.get('compiler_implementation_permitted') is not False:
            errors.append('pre-authorization compiler implementation must remain locked')

    if manifest.get('official_results_present') is not False or lock.get('official_results_present') is not False:
        errors.append('results must remain absent until a separate execution result change')
    if scenario.get('scenario_id') != 'CRE-002-EXT-001-SCENARIO-1.0':
        errors.append('wrong scenario id')
    if scenario.get('semantic_authority') != 'VOCABULARY-SEMANTICS-BASELINE-1.1':
        errors.append('wrong semantic authority')
    if len(scenario.get('transitions', [])) != 9:
        errors.append('expected nine transition schemas')
    if len(policies.get('policies', [])) != 9:
        errors.append('expected nine ambiguity policies')
    if set(rules.get('candidate_outcomes', [])) != {'complete', 'partial', 'unsupported', 'error'}:
        errors.append('candidate outcomes mismatch')
    if not NONCLAIMS.issubset(set(rules.get('global_nonclaims', []))):
        errors.append('decision rules omit nonclaims')
    if output.get('schema_id') != 'CRE-002-EXT-001-OUTPUT-SCHEMA-1.0':
        errors.append('wrong output schema')
    if manifest.get('preserved_prior_result') != 'CRE-002-COMPARISON-1.0':
        errors.append('prior CRE-002 result not preserved')

    if errors:
        print('CRE-002-EXT-001 PREREGISTRATION FAILED')
        print('\n'.join(errors))
        return 1
    print('CRE-002-EXT-001 PREREGISTRATION PASSED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
