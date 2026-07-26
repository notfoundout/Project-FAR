#!/usr/bin/env python3
"""Fail-closed validation for derived SWE-agent v2 forensic records."""
from __future__ import annotations
import argparse, hashlib, json, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
FORENSICS=ROOT/'docs/audits/swe-agent-v2-forensics'
CASE=ROOT/'commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2'
RUNS={'v1.0.0-r1','v1.0.0-r2','v1.0.1-r1','v1.0.1-r2'}
STAGES=['task_ingestion','repository_checkout','environment_setup','dependency_installation','task_interpretation','repository_search','files_inspected','tests_discovered','hypotheses_formed','reproduction_attempts','edits_proposed','edits_applied','tests_executed','failures_encountered','retries','patch_generation','prediction_generation','controller_termination','artifact_collection','grading','final_classification']
EVIDENCE={'observed','directly derived','inferred','assumed','unknown','disproven'}

def load(p): return json.loads(p.read_text())
def validate_records(causes, requirements):
 errors=[]; req={x['requirement_id']:x for x in requirements['requirements']}
 for c in causes['claims']:
  if c.get('run') not in RUNS: errors.append(f"unknown run: {c.get('run')}")
  if c.get('evidence_class') not in EVIDENCE: errors.append(f"invalid evidence class: {c.get('claim_id')}")
  if c.get('evidence_class')=='inferred':
   for key in ('confidence','confidence_reasoning','falsification_condition','confirmation_condition','supporting_evidence','contradictory_evidence','alternative_explanations'):
    if not c.get(key): errors.append(f"inferred claim missing {key}: {c.get('claim_id')}")
   if c.get('confidence') not in {'high','medium','low'}: errors.append(f"invalid confidence: {c.get('claim_id')}")
  if c.get('remediable'):
   control=c.get('proposed_control')
   if not control or control not in req: errors.append(f"remediable claim lacks control: {c.get('claim_id')}")
   if not c.get('validation_test'): errors.append(f"control lacks validation test: {c.get('claim_id')}")
 for r in req.values():
  for key in ('failure_addressed','supporting_evidence','required_behavior','acceptance_criterion','negative_test','likely_cost','residual_risk'):
   if not r.get(key): errors.append(f"requirement missing {key}: {r.get('requirement_id')}")
 return errors

def validate(root=ROOT, check_git=True):
 f=root/'docs/audits/swe-agent-v2-forensics'; case=root/CASE.relative_to(ROOT); errors=[]
 report=load(case/'post-freeze-reveal/final-comparison-report.json')
 if report.get('resolved_counts')!={'v1.0.0':0,'v1.0.1':0}: errors.append('frozen outcomes changed')
 if report.get('observed_resolution_result')!='no_observed_resolution_difference': errors.append('bounded conclusion changed')
 if report.get('bounded_case_decision')!='REVIEW_REQUIRED': errors.append('decision changed')
 timelines=[]
 for run in RUNS:
  p=f/'timelines'/f'{run}.json'
  if not p.exists(): errors.append(f'missing timeline: {run}'); continue
  d=load(p); timelines.append(d)
  if d.get('run_id')!=run or d.get('task_id')!='scikit-learn__scikit-learn-14125' or d.get('agent_version')!=run.rsplit('-',1)[0]: errors.append(f'timeline identity mismatch: {run}')
  if [e.get('stage') for e in d.get('events',[])]!=STAGES: errors.append(f'timeline stages mismatch: {run}')
  required={'timestamp','source_artifact','stage','action','tool_or_command','input','result','exit_status','duration_seconds','budget_consumed','state_transition','uncertainty'}
  if any(not required <= set(e) for e in d.get('events',[])): errors.append(f'timeline fields missing: {run}')
 if {x.get('run_id') for x in timelines}!=RUNS: errors.append('not every frozen run represented')
 errors += validate_records(load(f/'cause-to-control.json'),load(f/'future-v3-requirements.json'))
 taxonomy=load(f/'failure-taxonomy.json')['categories']
 expected={'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC'}
 if {x.get('code') for x in taxonomy}!=expected: errors.append('taxonomy incomplete')
 base=load(f/'frozen-evidence-baseline.json')
 expected_paths={item['path'] for item in base['files']}
 actual_paths={
  p.relative_to(root).as_posix()
  for directory in (case/'primary-freeze',case/'post-freeze-reveal')
  for p in directory.rglob('*') if p.is_file()
 }
 if actual_paths != expected_paths:
  missing=sorted(expected_paths-actual_paths); unexpected=sorted(actual_paths-expected_paths)
  errors.append(f'frozen evidence path set changed: missing={missing}; unexpected={unexpected}')
 for item in base['files']:
  p=root/item['path']
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']: errors.append(f"frozen hash mismatch: {item['path']}")
 texts='\n'.join(p.read_text(errors='replace').lower() for p in [root/'docs/audits/swe-agent-v2-forensic-postmortem.md',*f.rglob('*.md')])
 for phrase in ('v1.0.0 and v1.0.1 are equivalent','v3 is guaranteed to succeed','held-out evaluation was executed'):
  if phrase in texts: errors.append(f'forbidden claim: {phrase}')
 prov=load(f/'provenance-manifest.json')
 if prov.get('rerun_frozen_experiment') is not False or prov.get('held_out_evaluation_executed') is not False: errors.append('prohibited execution recorded')
 return errors

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--root',type=pathlib.Path,default=ROOT); ns=ap.parse_args()
 errors=validate(ns.root.resolve(),check_git=ns.root.resolve()==ROOT)
 if errors:
  print('\n'.join('ERROR: '+e for e in errors)); return 1
 print('SWE-agent v2 forensic validation: PASS (4 runs, frozen hashes, causal/control contracts)'); return 0
if __name__=='__main__': sys.exit(main())
