#!/usr/bin/env python3
"""Validate the frozen W3.5 reasoning-discrimination and FARA-specificity package."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any
from w3_5_specificity import SpecificityError, run_discrimination
ROOT=Path(__file__).resolve().parents[1]
LICENSING=ROOT/'theory/evaluation/w3-5-reasoning-licensing-v1.0.json'; DISC=ROOT/'theory/evaluation/w3-5-reasoning-discrimination-result-v1.0.json'; SPEC=ROOT/'theory/evaluation/w3-5-fara-specificity-result-v1.0.json'; FACTOR=ROOT/'theory/evaluation/w3-5-factorization-result-v1.0.json'; W35=ROOT/'theory/evaluation/w3-5-specificity-and-discovery-gate.json'; GATES=ROOT/'theory/evaluation/research-gates.json'; TARGET=ROOT/'theory/evaluation/thm-target-001.json'; CANDIDATES=ROOT/'theory/evaluation/universal-structure-candidate-registry.json'; DOC=ROOT/'docs/research/w3-5-reasoning-discrimination-and-specificity-v1.0.md'
EXPECTED_COUNTS={'positive':{'reasoning_like':8,'nonreasoning_like':0,'borderline':0,'unknown':0},'contrast':{'reasoning_like':0,'nonreasoning_like':8,'borderline':0,'unknown':0},'disputed':{'reasoning_like':0,'nonreasoning_like':0,'borderline':2,'unknown':0}}
class ValidationError(ValueError): pass
def load(path:Path)->dict[str,Any]: return json.loads(path.read_text(encoding='utf-8'))
def sha256_file(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def policy_errors(licensing,discrimination,specificity,w35,gates,target,candidates,factorization,digests):
    errors=[]
    def require(ok,msg):
        if not ok: errors.append(msg)
    require(licensing.get('registry_id')=='W35-REASONING-LICENSING-001','licensing identity changed')
    authored=licensing.get('authorship_and_blinding',{}); require(authored.get('admission_labels_hidden_from_runtime_scoring') is True,'runtime scoring is not label-hidden'); require(authored.get('semantic_coder_blind_to_admission_labels') is False,'semantic coding was misreported as blind'); require(authored.get('independent_external_evaluator') is False,'semantic coding was misreported as independent')
    require(discrimination.get('artifact_id')=='W35-SCOPE-RESULT-001','scope-result identity changed'); require(discrimination.get('status')=='complete','scope result is not complete'); require(discrimination.get('registered_results')==EXPECTED_COUNTS,'registered discrimination counts changed')
    require(discrimination.get('primary_metrics')=={'positive_sensitivity':'1.0','contrast_specificity':'1.0','balanced_accuracy':'1.0','statistical_inference':'not_authorized'},'primary metrics changed or statistical inference was added')
    contract=discrimination.get('execution_contract',{}); require(contract.get('labels_joined_after_all_scores') is True,'labels were not joined after scoring'); require(contract.get('semantic_coding_blind_or_independent') is False,'semantic coding was promoted'); require(contract.get('disputed_excluded_from_primary_metric') is True,'disputed cases entered the primary metric'); require(discrimination.get('licensing_registry',{}).get('content_sha256')==digests.get('licensing'),'discrimination licensing digest mismatch')
    require(specificity.get('artifact_id')=='W35-SPEC-RESULT-001','specificity-result identity changed'); require(specificity.get('status')=='complete_qualified_negative','specificity result must remain a qualified negative')
    result=specificity.get('result',{}); require(result.get('bounded_role_conjunctive_discrimination')=='established_on_registered_corpus','bounded discriminator result changed'); require(result.get('unique_discriminative_capacity_of_fara')=='refuted_at_registered_scope','FARA uniqueness was not preserved as refuted'); require(result.get('fara_primitive_necessity')=='not_established','FARA primitive necessity was promoted'); require(result.get('fara_reasoning_specificity_general')=='not_established','general FARA specificity was promoted'); require(specificity.get('gate_effect',{}).get('w5_authorized') is False,'specificity result authorized W5')
    deps={item.get('artifact_id'):item for item in specificity.get('depends_on',[])}; require(deps.get('W35-SCOPE-RESULT-001',{}).get('content_sha256')==digests.get('discrimination'),'specificity scope-result digest mismatch'); require(deps.get('W35-REASONING-LICENSING-001',{}).get('content_sha256')==digests.get('licensing'),'specificity licensing digest mismatch')
    require(factorization.get('artifact_id')=='W35-FACTOR-RESULT-001','factorization dependency changed'); require(factorization.get('dimensions',{}).get('reasoning_specificity')=='not_established','factorization was retrospectively promoted')
    current=w35.get('current_results',{}); stage=w35.get('status'); require(stage=='in_progress_specificity_complete','W3.5 status must remain at completed specificity while candidate execution is pending'); require(w35.get('w5_authorized') is False,'W3.5 authorized W5'); require(current.get('reasoning_discrimination')=='bounded_role_conjunctive_discrimination_established','reasoning discrimination state changed'); require(current.get('fara_specificity')=='not_unique_at_registered_scope','FARA specificity state changed'); require(current.get('machinery_and_cost')=='not_executed','cost execution was started by specificity'); require(current.get('candidate_invariants')=='not_executed','candidate execution was promoted without atomic evidence')
    artifacts={item.get('id'):item for item in w35.get('required_result_artifacts',[])}; scope=artifacts.get('W35-SCOPE-RESULT',{}); spec=artifacts.get('W35-SPEC-RESULT',{}); require(scope.get('status')=='complete' and scope.get('artifact_id')=='W35-SCOPE-RESULT-001' and scope.get('content_sha256')==digests.get('discrimination'),'W35 scope-result linkage invalid'); require(spec.get('status')=='complete' and spec.get('artifact_id')=='W35-SPEC-RESULT-001' and spec.get('content_sha256')==digests.get('specificity'),'W35 specificity-result linkage invalid'); require(artifacts.get('W35-CANDIDATE-RESULT',{}).get('status')=='missing','W35-CANDIDATE-RESULT was prematurely promoted')
    require(candidates.get('aggregate_result')=='candidate_structural_indispensability_unresolved_reexecution_required','candidate aggregate must preserve unresolved structural indispensability'); require(candidates.get('status')=='preliminary_internal_adjudication_reexecution_required','candidate registry status must preserve preliminary non-executed adjudication'); require(all(item.get('structural_commitment_necessity')=='unresolved' for item in candidates.get('candidates',[])),'structural necessity was prejudged'); require(all(item.get('trial_evidence_status')=='missing' for item in candidates.get('candidates',[])),'candidate trial evidence was falsely promoted')
    for artifact_id in ('W35-COST-RESULT','W35-CLAIM-RESULT','W35-FAILURE-RESULT'): require(artifacts.get(artifact_id,{}).get('status')=='missing',f'{artifact_id} was prematurely promoted')
    gate_map={item.get('name'):item for item in gates.get('gates',[])}; evidence={'docs/research/w3-5-reasoning-discrimination-and-specificity-v1.0.md','docs/audits/w3-5-specificity-audit.md','theory/evaluation/w3-5-reasoning-licensing-v1.0.json','theory/evaluation/w3-5-reasoning-discrimination-result-v1.0.json','theory/evaluation/w3-5-fara-specificity-result-v1.0.json'}
    for name in ('fara-specificity-resolved','reasoning-contrast-execution'):
        gate=gate_map.get(name,{}); require(gate.get('status')=='satisfied',f'{name} must be satisfied'); require(evidence<=set(gate.get('evidence',[])),f'{name} lacks complete evidence')
    require(gate_map.get('baseline-factorization-resolved',{}).get('status')=='satisfied','factorization gate regressed'); require(gate_map.get('universal-structure-result',{}).get('status')=='not_satisfied','universal structure was promoted')
    auth=target.get('w5_authorization',{}); require(auth.get('authorized') is False,'THM-TARGET-001 authorized W5'); require(auth.get('blocked_by')==['W3.5-SDG-001'],'THM-TARGET-001 blocker changed')
    return errors
def validate_static(root:Path=ROOT)->dict[str,Any]:
    relative={'licensing':LICENSING,'discrimination':DISC,'specificity':SPEC,'factorization':FACTOR,'w35':W35,'gates':GATES,'target':TARGET,'candidates':CANDIDATES,'doc':DOC}; paths={name:root/path.relative_to(ROOT) for name,path in relative.items()}
    for path in paths.values():
        if not path.is_file(): raise ValidationError(f'missing specificity dependency: {path.relative_to(root)}')
    data={name:load(path) for name,path in paths.items() if path.suffix=='.json'}; digests={'licensing':sha256_file(paths['licensing']),'discrimination':sha256_file(paths['discrimination']),'specificity':sha256_file(paths['specificity'])}; errors=policy_errors(data['licensing'],data['discrimination'],data['specificity'],data['w35'],data['gates'],data['target'],data['candidates'],data['factorization'],digests)
    if errors: raise ValidationError('; '.join(errors))
    return {**data,'digests':digests}
def validate(root:Path=ROOT)->dict[str,Any]:
    static=validate_static(root); runtime=run_discrimination(root)
    if runtime.get('class_counts')!=EXPECTED_COUNTS: raise ValidationError('runtime discrimination differs from frozen result')
    if runtime.get('specificity_analysis',{}).get('unique_discriminative_capacity_of_FARA') is not False: raise ValidationError('runtime analysis promoted unique FARA capacity')
    if runtime.get('licensing_registry',{}).get('content_sha256')!=static['digests']['licensing']: raise ValidationError('runtime licensing digest differs')
    return {'status':'pass','experiment_id':runtime['experiment_id'],'instance_count':runtime['scope']['instances'],'class_counts':runtime['class_counts'],'fara_specificity':runtime['specificity_analysis']['FARA_specificity_result']}
def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(description='Validate W3.5 discrimination and FARA specificity'); parser.add_argument('--root',type=Path,default=ROOT); parser.add_argument('--json',action='store_true'); args=parser.parse_args(argv)
    try: report=validate(args.root.resolve())
    except (ValidationError,SpecificityError,OSError,KeyError,TypeError,ValueError,json.JSONDecodeError) as exc: print(f'FAR-VAL-SPEC-001: {exc}'); return 1
    if args.json: print(json.dumps(report,indent=2,sort_keys=True))
    else: print('W3.5 specificity validation: PASS (8 positive; 8 contrast; 2 disputed preserved; FARA not unique at registered scope; W5 blocked)')
    return 0
if __name__=='__main__': raise SystemExit(main())