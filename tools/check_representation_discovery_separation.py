#!/usr/bin/env python3
"""Enforce separation between bounded representation results and universal-structure discovery."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from check_w3_5_candidate_tests import validate as validate_candidates
from check_w3_5_corpus_freeze import validate as validate_corpus
from check_w3_5_factorization import validate as validate_factorization
from check_w3_5_specificity import validate as validate_specificity

ROOT=Path(__file__).resolve().parents[1]
PATHS={
 'baseline':ROOT/'theory/evaluation/generic-relational-baseline-v1.0.json',
 'scope':ROOT/'theory/evaluation/reasoning-and-contrast-scope-v1.0.json',
 'corpus_result':ROOT/'theory/evaluation/w3-5-corpus-freeze-result-v1.0.json',
 'factor_result':ROOT/'theory/evaluation/w3-5-factorization-result-v1.0.json',
 'discrimination_result':ROOT/'theory/evaluation/w3-5-reasoning-discrimination-result-v1.0.json',
 'specificity_result':ROOT/'theory/evaluation/w3-5-fara-specificity-result-v1.0.json',
 'candidate_result':ROOT/'theory/evaluation/w3-5-candidate-test-result-v1.0.json',
 'us_target':ROOT/'theory/evaluation/universal-structure-discovery-target-v1.0.json',
 'w35':ROOT/'theory/evaluation/w3-5-specificity-and-discovery-gate.json',
 'candidates':ROOT/'theory/evaluation/universal-structure-candidate-registry.json',
 'gates':ROOT/'theory/evaluation/research-gates.json',
 'claims':ROOT/'theory/evaluation/central-claim-registry.json',
 'target':ROOT/'theory/evaluation/thm-target-001.json',
 'ledger':ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json',
 'standard':ROOT/'docs/governance/representation-discovery-separation-standard-v1.0.md',
 'central':ROOT/'docs/governance/central-research-program.md',
 'proof_roadmap':ROOT/'docs/planning/deduction-first-proof-roadmap.md',
 'neutral_roadmap':ROOT/'docs/planning/architecture-neutral-research-roadmap.md',
 'readme':ROOT/'README.md','makefile':ROOT/'Makefile',
 'task_generator':ROOT/'tools/generate_next_tasks.py','status_generator':ROOT/'tools/project_status_report.py','dashboard_generator':ROOT/'tools/update_readme_dashboard.py',
}
TERMINAL={'proved','refuted','obstruction_established','scope_boundary_established','superseded'}
HEX64=re.compile(r'^[0-9a-f]{64}$')
EXPECTED_FACTOR={'expressiveness':'equivalent','translation':'bidirectional','constraint_strength':'fara_stricter','reasoning_specificity':'not_established','cost_relation':'tradeoff','overall_interpretation':'fara_constrained_equivalent'}

def load(path:Path)->dict: return json.loads(path.read_text(encoding='utf-8'))
def require(ok:bool,message:str,errors:list[str])->None:
    if not ok: errors.append(message)
def gate_map(gates:dict)->dict: return {x.get('name'):x for x in gates.get('gates',[])}
def obligation_map(ledger:dict)->dict: return {x.get('id'):x for x in ledger.get('obligations',[])}

def authorization_errors(w35:dict,target:dict,scope:dict,gates:dict,ledger:dict,root:Path=ROOT)->list[str]:
    errors=[]; wa=w35.get('w5_authorized') is True; ta=target.get('w5_authorization',{}).get('authorized') is True
    obstruction=obligation_map(ledger).get('OBS-SC-010',{}); terminal=obstruction.get('status') in TERMINAL; blockers=set(target.get('w5_authorization',{}).get('blocked_by',[]))
    if not (wa or ta):
        require('W3.5-SDG-001' in blockers,'unauthorized W5 state must retain W3.5-SDG-001',errors)
        require(('OBS-SC-010' not in blockers) if terminal else ('OBS-SC-010' in blockers),'OBS-SC-010 blocker state is inconsistent',errors)
        return errors
    require(wa and ta,'W5 authorization flags must agree',errors); require(w35.get('status')=='resolved','W3.5 status must be resolved',errors); require(terminal,'OBS-SC-010 must have a terminal ledger status',errors)
    require(scope.get('concrete_corpus_status')=='frozen','the concrete reasoning and contrast corpus must be frozen',errors)
    current=w35.get('current_results',{}); require(current.get('candidate_invariants')=='complete','candidate_invariants must be complete',errors); require(current.get('machinery_and_cost')=='complete','machinery_and_cost must be complete',errors)
    for a in w35.get('required_result_artifacts',[]):
        label=a.get('id','<missing-id>'); require(a.get('status')=='complete',f'{label} is not complete',errors); p=a.get('path'); d=a.get('content_sha256'); require(bool(p),f'{label} lacks a path',errors); require(bool(a.get('artifact_id')),f'{label} lacks an immutable artifact id',errors); require(isinstance(d,str) and HEX64.fullmatch(d) is not None,f'{label} lacks a valid SHA-256 digest',errors)
        if isinstance(p,str) and p and (root/p).is_file() and isinstance(d,str) and HEX64.fullmatch(d): require(hashlib.sha256((root/p).read_bytes()).hexdigest()==d,f'{label} SHA-256 digest does not match its artifact',errors)
    gm=gate_map(gates)
    for name in w35.get('authorization_contract',{}).get('requires_research_gates_satisfied_with_evidence',[]): require(gm.get(name,{}).get('status')=='satisfied',f'research gate {name} is not satisfied',errors); require(bool(gm.get(name,{}).get('evidence')),f'research gate {name} lacks evidence',errors)
    require(target.get('w5_authorization',{}).get('blocked_by')==[],'authorized W5 state must clear target blockers',errors); require(bool(w35.get('authorization_evidence')),'W3.5 authorization evidence is empty',errors)
    return errors

def main()->int:
    errors=[]
    for name,path in PATHS.items(): require(path.is_file(),f'missing {name}: {path.relative_to(ROOT)}',errors)
    if errors: return report(errors)
    baseline=load(PATHS['baseline']); scope=load(PATHS['scope']); corpus=load(PATHS['corpus_result']); factor=load(PATHS['factor_result']); discrimination=load(PATHS['discrimination_result']); specificity=load(PATHS['specificity_result']); candidate_result=load(PATHS['candidate_result']); universal_target=load(PATHS['us_target']); w35=load(PATHS['w35']); candidates=load(PATHS['candidates']); gates=load(PATHS['gates']); claims=load(PATHS['claims']); target=load(PATHS['target']); ledger=load(PATHS['ledger'])
    require(baseline.get('baseline_id')=='GREL-001','generic baseline id must be GREL-001',errors); require(baseline.get('current_result')==EXPECTED_FACTOR,'generic baseline factorization results differ from frozen result',errors); require(factor.get('artifact_id')=='W35-FACTOR-RESULT-001' and factor.get('status')=='complete','factorization result must be complete',errors)
    try: require(validate_factorization(ROOT).get('status')=='pass','factorization validation failed',errors)
    except Exception as exc: errors.append(f'factorization validation failed: {exc}')
    require(discrimination.get('artifact_id')=='W35-SCOPE-RESULT-001' and discrimination.get('status')=='complete','reasoning discrimination result must be complete',errors); require(specificity.get('artifact_id')=='W35-SPEC-RESULT-001' and specificity.get('status')=='complete_qualified_negative','specificity result must remain a qualified negative',errors)
    try: require(validate_specificity(ROOT).get('status')=='pass','specificity validation failed',errors)
    except Exception as exc: errors.append(f'specificity validation failed: {exc}')
    require(scope.get('concrete_corpus_status')=='frozen','RCS-001 concrete corpus must be frozen',errors); require(len(scope.get('positive_instances',[]))==8 and len(scope.get('contrast_instances',[]))==8 and len(scope.get('disputed_instances',[]))==2,'RCS-001 frozen corpus counts changed',errors); errors.extend(validate_corpus(ROOT))
    require(candidate_result.get('artifact_id')=='W35-CANDIDATE-RESULT-001','candidate-result identity changed',errors); require(candidate_result.get('status')=='preliminary_internal_adjudication_reexecution_required','candidate result must remain preliminary and require re-execution',errors); require(candidate_result.get('aggregate_result')=='candidate_structural_indispensability_unresolved_reexecution_required','candidate aggregate result changed',errors); require(candidate_result.get('claim_effect',{}).get('universal_structure')=='unresolved','candidate result promoted universal structure',errors); require(candidate_result.get('claim_effect',{}).get('W5_authorized') is False,'candidate result authorized W5',errors)
    execution=candidate_result.get('execution',{})
    if execution.get('preserved_atomic_trials') != 0: errors.append('preliminary candidate result must preserve zero completed atomic trials')
    if execution.get('expected_atomic_trials') != 648: errors.append('candidate execution must require exactly 648 atomic trials')
    if len(candidate_result.get('results',[])) != 12: errors.append('candidate result must preserve all twelve preliminary hypotheses')
    if any(item.get('trial_evidence_status') != 'missing' for item in candidate_result.get('results',[])): errors.append('preliminary candidate summaries may not claim trial evidence')
    try: require(validate_candidates(ROOT).get('status')=='pass','candidate validation failed',errors)
    except Exception as exc: errors.append(f'candidate validation failed: {exc}')
    require(universal_target.get('target_id')=='THM-US-TARGET-001','universal target id mismatch',errors); require(all(x.get('status')!='proved' for x in universal_target.get('theorem_families',[])),'candidate package may not prove a universal theorem',errors)
    require(w35.get('gate_id')=='W3.5-SDG-001','W3.5 gate id mismatch',errors); require(w35.get('status')=='in_progress_specificity_complete','W3.5 must remain at completed specificity while candidate execution is pending',errors); require(w35.get('w5_authorized') is False,'W5 must not be authorized',errors)
    artifacts={a.get('id'):a for a in w35.get('required_result_artifacts',[])}; completed={'W35-CORPUS-RESULT','W35-FACTOR-RESULT','W35-SCOPE-RESULT','W35-SPEC-RESULT'}
    for aid in completed: require(artifacts.get(aid,{}).get('status')=='complete',f'{aid} must be complete',errors)
    for aid in ('W35-CANDIDATE-RESULT','W35-COST-RESULT','W35-CLAIM-RESULT','W35-FAILURE-RESULT'): require(artifacts.get(aid,{}).get('status')=='missing',f'{aid} must remain missing',errors)
    current=w35.get('current_results',{}); require(current.get('candidate_invariants')=='not_executed','candidate invariants must remain unexecuted',errors); require(current.get('machinery_and_cost')=='not_executed','machinery and cost must remain unexecuted',errors)
    items=candidates.get('candidates',[]); require(len(items)==12,'candidate registry must contain twelve hypotheses',errors); require(all(x.get('structural_commitment_necessity')=='unresolved' and x.get('trial_evidence_status')=='missing' for x in items),'candidate registry contains prejudged or fabricated evidence',errors); require(candidates.get('aggregate_result')=='candidate_structural_indispensability_unresolved_reexecution_required','candidate registry aggregate changed',errors); require(candidates.get('status')=='preliminary_internal_adjudication_reexecution_required','candidate registry status changed',errors)
    gm=gate_map(gates)
    for name in ('representation-discovery-separation','generic-baseline-frozen','universal-structure-target-frozen','reasoning-contrast-scope-framework-frozen','reasoning-contrast-corpus-frozen','baseline-factorization-resolved','fara-specificity-resolved','reasoning-contrast-execution','formal-negative-controls'): require(gm.get(name,{}).get('status')=='satisfied',f'research gate {name} must be satisfied',errors)
    require(gm.get('universal-structure-result',{}).get('status')=='not_satisfied','universal structure result must remain unsatisfied',errors)
    require(target.get('program_track')=='REP','THM-TARGET-001 must be REP',errors); errors.extend(authorization_errors(w35,target,scope,gates,ledger,ROOT))
    cb={x.get('id'):x for x in claims.get('claims',[])}; require(cb.get('CLM-UNIVERSAL-STRUCTURE',{}).get('current_status')=='unresolved','universal claim must remain unresolved',errors)
    makefile=PATHS['makefile'].read_text(encoding='utf-8')
    for command in ('check_representation_discovery_separation.py','check_w3_5_corpus_freeze.py','check_w3_5_factorization.py','check_w3_5_specificity.py','check_w3_5_candidate_tests.py'): require(makefile.count(f'python tools/{command}')==3,f'{command} must run three times',errors)
    return report(errors)

def report(errors:list[str])->int:
    if errors:
        print('Representation-discovery separation FAILED')
        for error in errors: print(f'- {error}')
        return 1
    print('Representation-discovery separation PASS (REP isolated; candidate execution pending; W5 blocked; USD unresolved)')
    return 0
if __name__=='__main__': raise SystemExit(main())
