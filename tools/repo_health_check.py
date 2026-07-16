#!/usr/bin/env python3
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path
from common_health import DEFAULT_HEALTH_TIMEOUT_SECONDS, ROOT, run, rel


def git_snapshot() -> set[str]:
    cp = subprocess.run(['git','status','--porcelain'], cwd=ROOT, text=True, capture_output=True)
    return set(cp.stdout.splitlines())


def main() -> int:
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(); g.add_argument('--fast',action='store_true'); g.add_argument('--full',action='store_true')
    parser.add_argument('--timeout', type=int, default=DEFAULT_HEALTH_TIMEOUT_SECONDS, help='per-subprocess timeout in seconds')
    args=parser.parse_args(); full=args.full
    before = git_snapshot()
    checks=[]
    def add(name, cmd, required=True): checks.append((name,cmd,required))
    add('canonical tests', [sys.executable, 'tools/run_tests.py', '--fast' if args.fast else ''])
    add('vocabulary semantics baseline 1.1', [sys.executable, 'tools/check_vocabulary_semantics_baseline_1_1.py'])
    tools = ['verify_theory.py','check_dependencies.py','check_dependency_registry.py','check_registry.py','check_notation.py','check_circularity.py','generate_theorem_index.py','check_repository_hygiene.py','check_certification_compliance.py','check_math_rendering.py','check_markdown_hygiene.py','check_release_consistency.py','check_internal_links.py','check_status_consistency.py']
    if full:
        tools += ['check_claims_audit.py','check_project_status.py','check_proof_assurance.py','check_external_validation_terms.py','check_mechanization_claims.py','check_ci_workflows.py']
    for tool in tools:
        if (ROOT/'tools'/tool).exists():
            cmd=[sys.executable, f'tools/{tool}']
            if tool == 'generate_theorem_index.py': cmd.append('--check')
            if tool == 'check_status_consistency.py': cmd.append('--report-only')
            add(tool, cmd)
    if full:
        add('cre001 deterministic', [sys.executable, 'tools/cre001_compile_vocabularies.py', '--write', '--check'])
        add('cre002 prospective execution', [sys.executable, 'tools/cre002_execute.py', '--check'])
        add('theory_impact_analyzer.py', [sys.executable,'tools/theory_impact_analyzer.py'])
        for tool in ['evaluate_reasoning_systems.py','evaluate_primitive_sufficiency.py','run_adversarial_suite.py','check_evaluation_consistency.py']:
            if (ROOT/'tools'/tool).exists(): add(tool, [sys.executable, f'tools/{tool}'])
        add('check_orphaned_docs.py', [sys.executable,'tools/check_orphaned_docs.py'], required=False)
    else:
        add('cre002 prospective execution', [sys.executable, 'tools/cre002_execute.py', '--check'])
        add('check_orphaned_docs.py (warnings)', [sys.executable,'tools/check_orphaned_docs.py'], required=False)
    for p in sorted((ROOT/'examples/far').glob('**/*.far.yaml')) if (ROOT/'examples/far').exists() else []:
        add(f'parse FAR {rel(p)}', [sys.executable,'tools/parse_far.py',rel(p)])
        add(f'reason FAR {rel(p)}', [sys.executable,'tools/reasoning_engine.py',rel(p)])
        add(f'reason FAR JSON {rel(p)}', [sys.executable,'tools/reasoning_engine.py','--json',rel(p)])
    for p in sorted((ROOT/'theory/proof-objects').glob('T-*.proof.yaml')) if (ROOT/'theory/proof-objects').exists() else []:
        add(f'proof object {rel(p)}', [sys.executable,'tools/check_proof_object.py',rel(p)])
    failures=[]; warnings=[]
    for name,cmd,required in checks:
        cmd=[c for c in cmd if c]
        print(f"\n==> {name}: {' '.join(cmd)}")
        cp=run(cmd, timeout=args.timeout)
        if cp.stdout: print(cp.stdout.rstrip())
        timed_out = cp.returncode == 124 and str(cp.stdout).startswith('TIMEOUT')
        if cp.returncode==0: print(f'PASS {name}')
        elif required:
            label='TIMEOUT' if timed_out else 'FAIL'
            print(f'{label} {name} (exit {cp.returncode})'); failures.append((name,cmd,cp.returncode,cp.stdout or '', timed_out))
        else:
            print(f'WARN {name} (exit {cp.returncode})'); warnings.append((name,cmd,cp.returncode,cp.stdout or '', timed_out))
    after = git_snapshot()
    caused = after - before
    if caused:
        failures.append(('read-only health check', ['git','status','--porcelain'], 1, '\n'.join(sorted(caused)), False))
    print('\nRepository health summary:')
    print(f'passed: {len(checks)-len(failures)-len(warnings)} warnings: {len(warnings)} failures: {len(failures)}')
    if warnings:
        print('warning checks:')
        for name,cmd,code,output,timed_out in warnings: print(f'- {name}')
    if failures:
        print('failed checks:')
        for name,cmd,code,output,timed_out in failures:
            print(f'- name: {name}')
            print(f'  command: {" ".join(cmd)}')
            print(f'  exit code: {code}')
            print(f'  kind: {"timeout" if timed_out else "failure"}')
            print('  last 30 output lines:')
            for line in output.rstrip().splitlines()[-30:]: print(f'    {line}')
        return 1
    return 0
if __name__ == '__main__': raise SystemExit(main())
