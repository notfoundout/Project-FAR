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


def validate_inventory(inventory, source_lock, root=ROOT, case=CASE):
 errors=[]
 if source_lock.get('case_id')!='swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2': errors.append('source lock case identity conflict')
 artifacts=inventory.get('artifacts',[]); paths=[x.get('path') for x in artifacts]
 duplicates=sorted({x for x in paths if x and paths.count(x)>1})
 if duplicates: errors.append(f'duplicate inventory paths: {duplicates}')
 by_path={x.get('path'):x for x in artifacts if x.get('path')}
 case_root=root/case.relative_to(ROOT) if case.is_absolute() else root/case
 committed={p.relative_to(root).as_posix() for p in case_root.rglob('*') if p.is_file()}
 locked={str((case_root/e['path']).relative_to(root)):e for e in source_lock.get('files',[])}
 external=set(locked)-committed
 present={p for p,x in by_path.items() if x.get('completeness')=='present'}
 declared_external={p for p,x in by_path.items() if x.get('artifact_type')=='external_source_evidence'}
 missing_inventory=sorted(committed-set(by_path)); orphaned=sorted(set(by_path)-(committed|external))
 if missing_inventory: errors.append(f'committed artifacts absent from inventory: {missing_inventory}')
 if orphaned: errors.append(f'orphaned or fabricated inventory paths: {orphaned}')
 mislabeled=sorted(committed & declared_external)
 if mislabeled: errors.append(f'committed artifacts mislabeled external-only: {mislabeled}')
 false_present=sorted(external & present)
 if false_present: errors.append(f'external artifacts falsely represented as committed: {false_present}')
 missing_locked=sorted(external-set(by_path))
 if missing_locked: errors.append(f'locked external artifacts absent from inventory: {missing_locked}')
 for path,item in by_path.items():
  target=root/path
  if path in committed:
   if not target.is_file(): errors.append(f'present inventory path missing: {path}'); continue
   actual_hash=hashlib.sha256(target.read_bytes()).hexdigest()
   if item.get('sha256')!=actual_hash: errors.append(f'inventory hash mismatch: {path}')
   if 'size_bytes' in item and item['size_bytes']!=target.stat().st_size: errors.append(f'inventory size mismatch: {path}')
   expected_format='JSON' if target.suffix=='.json' else 'text'
   if item.get('actual_format')!=expected_format: errors.append(f'inventory format mismatch: {path}')
   declared=item.get('schema_or_expected_format')
   if expected_format=='JSON' and str(declared).upper()!='JSON': errors.append(f'inventory expected-format mismatch: {path}')
  elif path in external:
   lock=locked[path]
   if item.get('sha256')!=lock.get('sha256'): errors.append(f'external lock hash conflict: {path}')
   if item.get('artifact_type')!='external_source_evidence' or item.get('actual_format')!='unavailable in Git': errors.append(f'external availability conflict: {path}')
   if item.get('authoritative') is not True or item.get('sufficient_for_diagnosis') is not False: errors.append(f'external provenance status conflict: {path}')
   if str(source_lock.get('source',{}).get('artifact_id')) not in item.get('provenance',''): errors.append(f'external artifact identity conflict: {path}')
 return errors

def expected_timeline_facts(run, package, outcome):
 report=outcome['report']; tests=report['tests_status']; behavior=package['behavioral_evidence']
 return {
  'blind_identity':package['run_id_blinded'],'revealed_identity':run,'agent_version':outcome['release'],
  'task_id':'scikit-learn__scikit-learn-14125','run_membership':True,'outcome':'unresolved','resolved':False,
  'patch_exists':report['patch_exists'],'patch_successfully_applied':report['patch_successfully_applied'],
  'grader_result':{'required_test':'sklearn/utils/tests/test_multiclass.py::test_type_of_target_pandas_sparse','required_test_result':'failed','pass_to_pass_success_count':len(tests['PASS_TO_PASS']['success'])},
  'call_budget_limit':31,'observed_call_count':behavior['api_calls'],'termination_reason':behavior['exit_status'],
  'final_classification':'unresolved','provider_status':'unknown','timeout_status':'unknown','quota_status':'unknown',
  'execution_status':package['execution']['completion_category'],'evidence_class':'directly derived',
  'sources':[f"primary-freeze/packages/{package['run_id_blinded']}.json",'post-freeze-reveal/outcome-reveal.json']}

def validate_timeline_facts(timeline, run, package, outcome):
 errors=[]; expected=expected_timeline_facts(run,package,outcome); actual=timeline.get('authoritative_facts')
 if actual!=expected:
  for key in sorted(set(expected)|set(actual or {})):
   if (actual or {}).get(key)!=expected.get(key): errors.append(f'timeline authoritative fact mismatch {run}.{key}')
 if timeline.get('outcome')!='unresolved': errors.append(f'timeline outcome mismatch: {run}')
 if timeline.get('agent_version')!=outcome['release'] or timeline.get('run_id')!=run: errors.append(f'timeline revealed identity mismatch: {run}')
 return errors

def validate(root=ROOT, check_git=True):
 f=root/'docs/audits/swe-agent-v2-forensics'; case=root/CASE.relative_to(ROOT); errors=[]
 report=load(case/'post-freeze-reveal/final-comparison-report.json')
 reveal=load(case/'post-freeze-reveal/outcome-reveal.json')
 packages={p.stem:load(p) for p in (case/'primary-freeze/packages').glob('*.json')}
 errors += validate_inventory(load(f/'evidence-inventory.json'),load(case/'primary-freeze/source-artifact-lock.json'),root,case)
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
  blind=('System-A' if run.startswith('v1.0.0') else 'System-B')+'-r'+run[-1]
  errors += validate_timeline_facts(d,run,packages[blind],reveal['outcomes'][run])
 if {x.get('run_id') for x in timelines}!=RUNS: errors.append('not every frozen run represented')
 errors += validate_records(load(f/'cause-to-control.json'),load(f/'future-v3-requirements.json'))
 taxonomy=load(f/'failure-taxonomy.json')['categories']
 expected={'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC'}
 if {x.get('code') for x in taxonomy}!=expected: errors.append('taxonomy incomplete')
 causal_codes={'A','B','C','D','E','F','G','H','I','J','K','L','M','N'}
 for category in taxonomy:
  if category.get('code') in causal_codes and category.get('occurrence')=='yes' and category.get('causal_attribution_supported') is not True:
   errors.append(f"causal taxonomy category marked observed without distinguishing evidence: {category.get('code')}")
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
