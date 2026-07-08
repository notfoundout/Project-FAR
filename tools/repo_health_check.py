#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys
from pathlib import Path
from common_health import ROOT, run, rel

parser=argparse.ArgumentParser(); g=parser.add_mutually_exclusive_group(); g.add_argument('--fast',action='store_true'); g.add_argument('--full',action='store_true'); args=parser.parse_args()
full=args.full
checks=[]
def add(name, cmd, required=True): checks.append((name,cmd,required))
for tool in ['verify_theory.py','check_dependencies.py','check_dependency_registry.py','check_registry.py','check_notation.py','check_circularity.py','generate_theorem_index.py','check_repository_hygiene.py','check_math_rendering.py','check_markdown_hygiene.py','check_release_consistency.py','check_internal_links.py']:
    if (ROOT/'tools'/tool).exists(): add(tool, [sys.executable, f'tools/{tool}'])
if full:
    add('theory_impact_analyzer.py', [sys.executable,'tools/theory_impact_analyzer.py'])
    for tool in ['evaluate_reasoning_systems.py','evaluate_primitive_sufficiency.py','run_adversarial_suite.py','check_evaluation_consistency.py']:
        if (ROOT/'tools'/tool).exists(): add(tool, [sys.executable, f'tools/{tool}'])
    add('check_orphaned_docs.py', [sys.executable,'tools/check_orphaned_docs.py'], required=False)
else:
    add('check_orphaned_docs.py (warnings)', [sys.executable,'tools/check_orphaned_docs.py'], required=False)
for p in sorted((ROOT/'examples/far').glob('**/*.far.yaml')) if (ROOT/'examples/far').exists() else []:
    add(f'parse FAR {rel(p)}', [sys.executable,'tools/parse_far.py',rel(p)])
    add(f'reason FAR {rel(p)}', [sys.executable,'tools/reasoning_engine.py',rel(p)])
    add(f'reason FAR JSON {rel(p)}', [sys.executable,'tools/reasoning_engine.py','--json',rel(p)])
for p in sorted((ROOT/'theory/proof-objects').glob('T-*.proof.yaml')) if (ROOT/'theory/proof-objects').exists() else []:
    add(f'proof object {rel(p)}', [sys.executable,'tools/check_proof_object.py',rel(p)])
failures=[]; warnings=[]
for name,cmd,required in checks:
    print(f"\n==> {name}: {' '.join(cmd)}")
    cp=run(cmd)
    if cp.stdout: print(cp.stdout.rstrip())
    if cp.returncode==0: print(f'PASS {name}')
    elif required:
        print(f'FAIL {name} (exit {cp.returncode})'); failures.append((name,cmd,cp.returncode,cp.stdout or ''))
    else:
        print(f'WARN {name} (exit {cp.returncode})'); warnings.append((name,cmd,cp.returncode,cp.stdout or ''))
print('\nRepository health summary:')
print(f'passed: {len(checks)-len(failures)-len(warnings)} warnings: {len(warnings)} failures: {len(failures)}')
if warnings:
    print('warning checks:')
    for name,cmd,code,output in warnings:
        print(f'- {name}')
if failures:
    print('failed checks:')
    for name,cmd,code,output in failures:
        print(f'- name: {name}')
        print(f'  command: {" ".join(cmd)}')
        print(f'  exit code: {code}')
        print('  last 30 output lines:')
        lines=output.rstrip().splitlines()[-30:]
        for line in lines:
            print(f'    {line}')
if failures: raise SystemExit(1)
