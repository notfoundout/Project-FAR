#!/usr/bin/env python3
"""Enforce separation between bounded representation results and universal-structure discovery."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from check_w3_5_corpus_freeze import validate as validate_corpus
from check_w3_5_factorization import validate as validate_factorization

ROOT=Path(__file__).resolve().parents[1]
PATHS={
'standard':ROOT/'docs/governance/representation-discovery-separation-standard-v1.0.md',
'baseline_doc':ROOT/'docs/research/generic-relational-baseline-v1.0.md','baseline':ROOT/'theory/evaluation/generic-relational-baseline-v1.0.json',
'scope_doc':ROOT/'docs/research/reasoning-and-contrast-scope-v1.0.md','scope':ROOT/'theory/evaluation/reasoning-and-contrast-scope-v1.0.json',
'corpus_doc':ROOT/'docs/research/w3-5-concrete-corpus-freeze-v1.0.md','corpus_result':ROOT/'theory/evaluation/w3-5-corpus-freeze-result-v1.0.json',
'factor_doc':ROOT/'docs/research/w3-5-grel-fara-factorization-v1.0.md','factor_result':ROOT/'theory/evaluation/w3-5-factorization-result-v1.0.json',
'us_doc':ROOT/'docs/research/universal-structure-discovery-target-v1.0.md','us_target':ROOT/'theory/evaluation/universal-structure-discovery-target-v1.0.json',
'w35_doc':ROOT/'docs/research/w3-5-specificity-and-discovery-gate-v1.0.md','w35':ROOT/'theory/evaluation/w3-5-specificity-and-discovery-gate.json',
'candidates':ROOT/'theory/evaluation/universal-structure-candidate-registry.json','gates':ROOT/'theory/evaluation/research-gates.json',
'claims':ROOT/'theory/evaluation/central-claim-registry.json','target':ROOT/'theory/evaluation/thm-target-001.json',
'ledger':ROOT/'theory/evaluation/s-core-construction-obstruction-ledger.json','central':ROOT/'docs/governance/central-research-program.md',
'proof_roadmap':ROOT/'docs/planning/deduction-first-proof-roadmap.md','neutral_roadmap':ROOT/'docs/planning/architecture-neutral-research-roadmap.md',
'readme':ROOT/'README.md','makefile':ROOT/'Makefile','task_generator':ROOT/'tools/generate_next_tasks.py',
'status_generator':ROOT/'tools/project_status_report.py','dashboard_generator':ROOT/'tools/update_readme_dashboard.py'}
TERMINAL={'proved','refuted','obstruction_established','scope_boundary_established','superseded'}
HEX64=re.compile(r'^[0-9a-f]{64}$')
DIMS={'expressiveness','translation','constraint_strength','reasoning_specificity','cost_relation','overall_interpretation'}
EXPECTED_FACTOR={'expressiveness':'equivalent','translation':'bidirectional','constraint_strength':'fara_stricter','reasoning_specificity':'not_established','cost_relation':'tradeoff','overall_interpretation':'fara_constrained_equivalent'}

def load(p:Path)->dict: return json.loads(p.read_text(encoding='utf-8'))
def require(ok:bool,msg:str,errors:list[str]):
    if not ok: errors.append(msg)
def gate_map(g): return {x.get('name'):x for x in g.get('gates',[])}
def obligation_map(l): return {x.get('id'):x for x in l.get('obligations',[])}

def authorization_errors(w35,target,scope,gates,ledger,root:Path=ROOT)->list[str]:
    e=[]; wa=w35.get('w5_authorized') is True; ta=target.get('w5_authorization',{}).get('authorized') is True
    obs=obligation_map(ledger).get('OBS-SC-010',{}); terminal=obs.get('status') in TERMINAL
    blockers=set(target.get('w5_authorization',{}).get('blocked_by',[]))
    if not (wa or ta):
        require('W3.5-SDG-001' in blockers,'unauthorized W5 state must retain W3.5-SDG-001',e)
        require(('OBS-SC-010' not in blockers) if terminal else ('OBS-SC-010' in blockers),'OBS-SC-010 blocker state is inconsistent',e)
        return e
    require(wa and ta,'W5 authorization flags must agree',e)
    require(w35.get('status')=='resolved','W3.5 status must be resolved',e)
    require(terminal,'OBS-SC-010 must have a terminal ledger status',e)
    require(scope.get('concrete_corpus_status')=='frozen','the concrete reasoning and contrast corpus must be frozen',e)
    require(bool(scope.get('positive_instances')),'positive instance registry must be nonempty',e)
    require(bool(scope.get('contrast_instances')),'contrast instance registry must be nonempty',e)
    values=w35.get('current_results',{}).get('factorization',{}); allowed=w35.get('factorization_result_dimensions',{})
    for dim,options in allowed.items():
        value=values.get(dim); require(value in options,f'factorization dimension {dim} has invalid value',e); require(value!='unresolved',f'factorization dimension {dim} remains unresolved',e)
    for key in ('fara_specificity','reasoning_discrimination','candidate_invariants','machinery_and_cost'):
        value=w35.get('current_results',{}).get(key)
        require(value not in {None,'unresolved','not_executed'} if key=='fara_specificity' else value=='complete',f'{key} must be complete or terminal',e)
    arts=w35.get('required_result_artifacts',[]); require(bool(arts),'W3.5 required result artifact list is empty',e)
    for a in arts:
        label=a.get('id','<missing-id>'); require(a.get('status')=='complete',f'{label} is not complete',e)
        path=a.get('path'); digest=a.get('content_sha256')
        require(isinstance(path,str) and bool(path),f'{label} lacks a path',e)
        require(isinstance(a.get('artifact_id'),str) and bool(a.get('artifact_id')),f'{label} lacks an immutable artifact id',e)
        require(isinstance(digest,str) and HEX64.fullmatch(digest) is not None,f'{label} lacks a valid SHA-256 digest',e)
        if isinstance(path,str) and path:
            fp=root/path; require(fp.is_file(),f'{label} artifact path does not exist: {path}',e)
            if fp.is_file() and isinstance(digest,str) and HEX64.fullmatch(digest): require(hashlib.sha256(fp.read_bytes()).hexdigest()==digest,f'{label} SHA-256 digest does not match its artifact',e)
    gm=gate_map(gates)
    for name in w35.get('authorization_contract',{}).get('requires_research_gates_satisfied_with_evidence',[]):
        require(gm.get(name,{}).get('status')=='satisfied',f'research gate {name} is not satisfied',e); require(bool(gm.get(name,{}).get('evidence')),f'research gate {name} lacks evidence',e)
    require(target.get('w5_authorization',{}).get('blocked_by')==[],'authorized W5 state must clear target blockers',e)
    require(bool(w35.get('authorization_evidence')),'W3.5 authorization evidence is empty',e)
    return e

def main()->int:
    e=[]
    for name,path in PATHS.items(): require(path.is_file(),f'missing {name}: {path.relative_to(ROOT)}',e)
    if e: return report(e)
    baseline=load(PATHS['baseline']); scope=load(PATHS['scope']); corpus=load(PATHS['corpus_result']); factor=load(PATHS['factor_result']); us=load(PATHS['us_target'])
    w35=load(PATHS['w35']); candidates=load(PATHS['candidates']); gates=load(PATHS['gates']); claims=load(PATHS['claims'])
    target=load(PATHS['target']); ledger=load(PATHS['ledger'])
    require(baseline.get('baseline_id')=='GREL-001','generic baseline id must be GREL-001',e)
    require(baseline.get('status')=='factorization_complete','generic baseline must record completed factorization',e)
    require(baseline.get('reasoning_specific_primitives')==[],'generic baseline must contain no reasoning-specific primitives',e)
    require(baseline.get('single_scalar_classification_prohibited') is True,'factorization may not collapse to one scalar',e)
    dims=baseline.get('result_dimensions',{}); current=baseline.get('current_result',{})
    require(set(dims)==DIMS,'generic baseline result dimensions are incomplete',e); require(set(current)==DIMS,'generic baseline current result dimensions are incomplete',e)
    require(current==EXPECTED_FACTOR,'generic baseline factorization results differ from frozen result',e)
    require(factor.get('artifact_id')=='W35-FACTOR-RESULT-001' and factor.get('status')=='complete','factorization result must be complete',e)
    require(factor.get('dimensions')==EXPECTED_FACTOR,'factorization result dimensions changed',e)
    require(factor.get('factorization_contract',{}).get('primitive_reduction_established') is False,'factorization must not be promoted to primitive reduction',e)
    e.extend([] if validate_factorization(ROOT).get('status')=='pass' else ['factorization validation failed'])

    admission=scope.get('admission_rules',{})
    for key in ('positive_independent_of_fara','positive_independent_of_candidate','contrast_independent_of_fara_failure','contrast_independent_of_candidate_absence','admission_decision_must_precede_candidate_scoring'):
        require(admission.get(key) is True,f'RCS-001 admission rule {key} must be true',e)
    require(scope.get('framework_frozen') is True,'RCS-001 admission framework must be frozen',e)
    require(scope.get('concrete_corpus_status')=='frozen','RCS-001 concrete corpus must be frozen',e)
    require(scope.get('concrete_corpus_id')=='RCS-CORPUS-001','RCS-001 concrete corpus id mismatch',e)
    require(len(scope.get('positive_instances',[]))==8,'RCS-001 positive registry must contain eight frozen instances',e)
    require(len(scope.get('contrast_instances',[]))==8,'RCS-001 contrast registry must contain eight frozen instances',e)
    require(len(scope.get('disputed_instances',[]))==2,'RCS-001 disputed registry must preserve two cases',e)
    require(scope.get('execution_status')=='ready_for_candidate_neutral_execution','RCS-001 execution must be ready but not executed',e)
    require(scope.get('candidate_scoring_status')=='not_started','RCS-001 candidate scoring must remain not_started',e)
    require(corpus.get('status')=='complete','RCS-CORPUS-001 freeze result must be complete',e)
    require(corpus.get('claim_impact',{}).get('W5_authorized') is False,'corpus freeze may not authorize W5',e)
    e.extend(validate_corpus(ROOT))

    require(us.get('target_id')=='THM-US-TARGET-001','universal target id mismatch',e)
    require(us.get('status')=='frozen_prospective','universal target must be frozen prospectively',e)
    require(us.get('representation_track_implication')=='none','REP must have no automatic USD implication',e)
    required={'THM-US-EXIST-001','THM-US-INV-001[K]','THM-US-DISC-001[K]','THM-US-NEC-001[K]','THM-US-RED-001[K]','THM-US-MIN-001','THM-US-EQUIV-001','THM-US-NO-001'}
    require(required<={x.get('id') for x in us.get('theorem_families',[])},'universal target is missing theorem families',e)

    require(w35.get('gate_id')=='W3.5-SDG-001','W3.5 gate id mismatch',e); require(w35.get('position')=='after_W3_before_W5','W3.5 must be after W3 and before W5',e)
    require(w35.get('status')=='in_progress_factorization_complete','W3.5 status must record factorization-complete progress only',e)
    require(w35.get('W5_blocked_until_resolved') is True,'W5 must be blocked until W3.5 resolves',e); require(w35.get('w5_authorized') is False,'W5 must not be authorized',e)
    require(w35.get('factorization_result_dimensions')==dims,'W3.5 dimensions must match GREL-001',e)
    require(w35.get('current_results',{}).get('factorization')==EXPECTED_FACTOR,'W3.5 factorization result changed',e)
    arts=w35.get('required_result_artifacts',[]); require(len(arts)>=8,'W3.5 must register required artifacts',e)
    for a in arts: require(set(a)>={'id','kind','status','path','artifact_id','content_sha256'},'W3.5 artifact record is incomplete',e)
    amap={a.get('id'):a for a in arts}
    require(amap.get('W35-CORPUS-RESULT',{}).get('status')=='complete','corpus result must be complete',e)
    require(amap.get('W35-FACTOR-RESULT',{}).get('status')=='complete','factorization result must be complete',e)
    for aid,a in amap.items():
        if aid not in {'W35-CORPUS-RESULT','W35-FACTOR-RESULT'}: require(a.get('status')=='missing',f'{aid} must remain missing after factorization',e)
    require(w35.get('current_results',{}).get('reasoning_contrast_corpus')=='frozen','W3.5 corpus result must be frozen',e)
    require(w35.get('current_results',{}).get('reasoning_discrimination')=='not_executed','reasoning discrimination must remain not executed',e)
    require(w35.get('current_results',{}).get('fara_specificity')=='unresolved','FARA specificity must remain unresolved',e)

    require(candidates.get('registry_id')=='US-CANDIDATES-001','candidate registry id mismatch',e)
    require(len(candidates.get('candidates',[]))>=10,'candidate registry must contain a broad hypothesis set',e)
    require(all(x.get('current_classification')=='unresolved' for x in candidates.get('candidates',[])),'candidate invariants may not be prejudged',e)

    gm=gate_map(gates)
    expected={'representation-discovery-separation':'satisfied','generic-baseline-frozen':'satisfied','universal-structure-target-frozen':'satisfied','reasoning-contrast-scope-framework-frozen':'satisfied','reasoning-contrast-corpus-frozen':'satisfied','baseline-factorization-resolved':'satisfied','fara-specificity-resolved':'not_satisfied','reasoning-contrast-execution':'not_satisfied','universal-structure-result':'not_satisfied','formal-negative-controls':'satisfied'}
    for name,status in expected.items(): require(gm.get(name,{}).get('status')==status,f'research gate {name} must be {status}',e)
    require(bool(gm.get('baseline-factorization-resolved',{}).get('evidence')),'factorization gate must have evidence',e)
    require('reasoning-contrast-scope-frozen' not in gm,'ambiguous scope-frozen gate must not remain',e)
    policy=gates.get('claim_policy',{})
    for key in ('representation_does_not_imply_universal_structure','common_schema_does_not_imply_reasoning_specificity','finite_core_does_not_imply_general_universality','w5_requires_w3_5_resolution','dashboard_tracks_may_not_be_aggregated','concrete_scope_requires_registered_instances','w5_authorization_requires_linked_immutable_evidence','factorization_dimensions_may_not_be_collapsed','registered_nontriviality_does_not_imply_fara_specificity'):
        require(policy.get(key) is True,f'claim_policy.{key} must be true',e)

    require(target.get('program_track')=='REP','THM-TARGET-001 must be REP',e); require(target.get('universal_structure_target')=='THM-US-TARGET-001','REP target must point to USD target',e)
    require({'reasoning_specificity','universal_structure','primitive_necessity','minimality','uniqueness'}<=set(target.get('does_not_imply',[])),'REP target lacks non-implications',e)
    for tid in ('THM-CORE-COMMON-001','THM-CORE-REP-001','THM-IMP-001'):
        theorem=next((x for x in target.get('theorem_family',[]) if x.get('id')==tid),{})
        require('specificity_discovery_bridge' in theorem.get('blocked_by',[]),f'{tid} must be blocked by W3.5',e)
    e.extend(authorization_errors(w35,target,scope,gates,ledger,ROOT))

    cb={x.get('id'):x for x in claims.get('claims',[])}
    require('CLM-UNIVERSAL-STRUCTURE' in cb.get('CLM-REP-CAPACITY',{}).get('does_not_imply',[]),'REP claim must not imply USD',e)
    require(cb.get('CLM-UNIVERSAL-STRUCTURE',{}).get('track')=='USD','universal claim must use USD',e)
    require(cb.get('CLM-UNIVERSAL-STRUCTURE',{}).get('current_status')=='unresolved','universal claim must remain unresolved',e)

    standard=PATHS['standard'].read_text(); central=PATHS['central'].read_text(); proof=PATHS['proof_roadmap'].read_text(); neutral=PATHS['neutral_roadmap'].read_text(); readme=PATHS['readme'].read_text(); make=PATHS['makefile'].read_text()
    require('faithful representation' in standard and 'universal structure' in standard,'separation standard lacks non-implication',e)
    require('W3.5' in central and 'representation track' in central.lower(),'central program lacks track separation',e)
    require(proof.find('W3.5')<proof.find('W5'),'proof roadmap must place W3.5 before W5',e)
    require('THM-US-TARGET-001' in neutral,'neutral roadmap lacks USD target',e)
    require('W3.5' in readme and 'universal-structure discovery' in readme.lower(),'README lacks W3.5/USD',e)
    require(make.count('python tools/check_representation_discovery_separation.py')==3,'separation checker must run three times',e)
    require(make.count('python tools/check_w3_5_corpus_freeze.py')==3,'corpus-freeze checker must run three times',e)
    require(make.count('python tools/check_w3_5_factorization.py')==3,'factorization checker must run three times',e)
    for name,path in (('task generator',PATHS['task_generator']),('status generator',PATHS['status_generator']),('dashboard generator',PATHS['dashboard_generator'])):
        text=path.read_text(); require('W3.5' in text,f'{name} must preserve W3.5',e); require('W5' in text and 'block' in text.lower(),f'{name} must preserve W5 block',e)
    return report(e)

def report(errors:list[str])->int:
    if errors:
        print('Representation-discovery separation FAILED')
        for error in errors: print(f'- {error}')
        return 1
    print('Representation-discovery separation PASS (REP isolated; W4 terminal; corpus and factorization complete; specificity and execution open; W3.5 evidence-blocks W5; USD unresolved)')
    return 0

if __name__=='__main__': raise SystemExit(main())
