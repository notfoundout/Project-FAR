#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001'
REQUIRED = ['README.md','preregistration.md','scenario/scenario-v1.0.json','ambiguity-policies.json','decision-rules.json','output-schema.json','package-manifest.json','execution-lock.json']
NONCLAIMS = {'universal sufficiency','primitive-only sufficiency','necessity','minimality','independence','superiority','FAR proof','universal structure of reasoning','retrospective validation of CRE-002'}


def load(name: str):
    return json.loads((PKG / name).read_text())


def verify_checksums() -> bool:
    cp = subprocess.run(
        [sys.executable, 'tools/check_cre002_ext001_checksums.py'],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return cp.returncode == 0


def main() -> int:
    errors = []
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
    checksum_valid = checksum_state == 'locked' and (PKG / 'checksum-lock.json').is_file() and verify_checksums()
    if checksum_state == 'locked' and not checksum_valid:
        errors.append('locked state requires successful checksum verification')

    execution = manifest.get('execution_permitted')
    compiler = manifest.get('compiler_implementation_permitted')
    if execution != lock.get('execution_permitted') or compiler != lock.get('compiler_implementation_permitted'):
        errors.append('manifest and execution lock authorization disagree')
    if execution is True or compiler is True:
        audit_path = PKG / 'execution-unlock-audit.json'
        if not checksum_valid:
            errors.append('execution authorization requires a valid checksum lock')
        if not audit_path.is_file():
            errors.append('execution authorization requires execution-unlock-audit.json')
        else:
            audit = load('execution-unlock-audit.json')
            if audit.get('authorization_type') != 'separate-reviewed-pull-request':
                errors.append('unlock audit has wrong authorization type')
            if audit.get('immutable_scientific_files_modified') is not False:
                errors.append('unlock audit must confirm scientific files unchanged')
            if audit.get('execution_authorized') is not True or audit.get('compiler_implementation_authorized') is not True:
                errors.append('unlock audit does not authorize execution and compiler implementation')
            if audit.get('official_results_present') is not False:
                errors.append('unlock audit must not claim results')
            if audit.get('preserved_prior_result') != 'CRE-002-COMPARISON-1.0':
                errors.append('unlock audit does not preserve prior result')
    elif execution is not False or compiler is not False:
        errors.append('authorization fields must be booleans')

    if manifest.get('official_results_present') is not False or lock.get('official_results_present') is not False:
        errors.append('results must be absent before execution')
    if scenario.get('scenario_id') != 'CRE-002-EXT-001-SCENARIO-1.0':
        errors.append('wrong scenario id')
    if scenario.get('semantic_authority') != 'VOCABULARY-SEMANTICS-BASELINE-1.1':
        errors.append('wrong semantic authority')
    if len(scenario.get('transitions', [])) != 9:
        errors.append('expected nine transition schemas')
    if len(policies.get('policies', [])) != 9:
        errors.append('expected nine ambiguity policies')
    if set(rules.get('candidate_outcomes', [])) != {'complete','partial','unsupported','error'}:
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
