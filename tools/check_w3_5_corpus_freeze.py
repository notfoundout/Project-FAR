#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
FAILURE_CODE='FAR-VAL-CORPUS-001'
REQ_OBS={'observable_or_formal_states','transitions_and_constraints','represented_distinctions','declared_semantics','history_and_path_dependence','objectives_or_tasks','grounds_or_dependencies','commitment_or_alternative_structure','uncertainty_and_revision','provenance_and_correspondence_limits'}
BANNED=('fara','grel','universal structure','candidate invariant','pb-001','expected w3.5')
PATHS={'scope':'theory/evaluation/reasoning-and-contrast-scope-v1.0.json','catalog':'theory/evaluation/rcs-concrete-source-catalog-v1.0.json','positive':'theory/evaluation/rcs-positive-corpus-v1.0.json','contrast':'theory/evaluation/rcs-contrast-corpus-v1.0.json','disputed':'theory/evaluation/rcs-disputed-corpus-v1.0.json','result':'theory/evaluation/w3-5-corpus-freeze-result-v1.0.json','w35':'theory/evaluation/w3-5-specificity-and-discovery-gate.json','gates':'theory/evaluation/research-gates.json','doc':'docs/research/w3-5-concrete-corpus-freeze-v1.0.md','audit':'docs/audits/w3-5-concrete-corpus-freeze-audit.md'}

def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))
def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def req(ok:bool,msg:str,errors:list[str])->None:
    if not ok: errors.append(msg)

def validate_data(*,scope,catalog,source_records,registries,result,w35,gates,actual_digests,actual_bundle_digests)->list[str]:
    e=[]
    req(scope.get('scope_id')=='RCS-001','scope id must be RCS-001',e)
    req(scope.get('framework_frozen') is True,'RCS-001 framework must remain frozen',e)
    req(scope.get('concrete_corpus_status')=='frozen','concrete corpus status must be frozen',e)
    req(scope.get('concrete_corpus_id')=='RCS-CORPUS-001','concrete corpus id mismatch',e)
    req(scope.get('execution_status')=='ready_for_candidate_neutral_execution','corpus must remain ready for candidate-neutral execution',e)
    req(scope.get('candidate_scoring_status')=='not_started','candidate scoring must remain not_started',e)
    req(catalog.get('catalog_id')=='RCS-SOURCES-001','source catalog id mismatch',e)
    req(catalog.get('status')=='frozen','source catalog must be frozen',e)
    req(catalog.get('freeze_basis')=='candidate_independent_admission_before_any_W3_5_candidate_scoring_with_explicit_candidate_registry_exposure','freeze basis mismatch',e)
    req(set(catalog.get('required_observation_fields',[]))==REQ_OBS,'catalog observation-field contract is incomplete',e)
    entries=catalog.get('records',[])
    req(isinstance(entries,list) and bool(entries),'source catalog records must be nonempty',e)
    entries=entries if isinstance(entries,list) else []
    entry_by_id={}
    for entry in entries:
        iid=entry.get('instance_id') if isinstance(entry,dict) else None
        req(isinstance(iid,str) and bool(iid),'catalog entry requires instance_id',e)
        if isinstance(iid,str): req(iid not in entry_by_id,f'duplicate catalog instance id: {iid}',e); entry_by_id[iid]=entry
        req(isinstance(entry.get('bundle_path'),str) and bool(entry.get('bundle_path')),f'{iid} catalog bundle path missing',e)
        req(re.fullmatch(r'[0-9a-f]{64}',str(entry.get('bundle_sha256',''))) is not None,f'{iid} catalog bundle digest invalid',e)
        req(entry.get('bundle_sha256')==actual_bundle_digests.get(entry.get('bundle_path')),f'{iid} source bundle digest mismatch',e)
        req(isinstance(entry.get('record_index'),int) and entry.get('record_index')>=0,f'{iid} record index invalid',e)
    records=source_records if isinstance(source_records,list) else []
    req(len(records)==len(entries) and bool(records),'loaded source record set differs from catalog',e)
    by_id={}; ids=set(); source_ids=set()
    for r in records:
        if not isinstance(r,dict): e.append('every source record must be an object'); continue
        iid=r.get('instance_id'); sid=r.get('source_record_id')
        req(isinstance(iid,str) and bool(iid),'source record requires instance_id',e)
        req(isinstance(sid,str) and bool(sid),f'{iid} requires source_record_id',e)
        if isinstance(iid,str): req(iid not in ids,f'duplicate instance id: {iid}',e); ids.add(iid); by_id[iid]=r
        if isinstance(sid,str): req(sid not in source_ids,f'duplicate source record id: {sid}',e); source_ids.add(sid)
        entry=entry_by_id.get(iid,{})
        req(entry.get('source_record_id')==sid,f'{iid} catalog source-record link mismatch',e)
        req(entry.get('family')==r.get('family'),f'{iid} catalog family mismatch',e)
        req(entry.get('admission_decision')==r.get('admission_decision'),f'{iid} catalog decision mismatch',e)
        req(entry.get('candidate_exposure_status')==r.get('candidate_exposure_status'),f'{iid} catalog exposure mismatch',e)
        decision=r.get('admission_decision'); req(decision in {'positive','contrast','disputed'},f'{iid} has invalid admission decision',e)
        rationale=r.get('admission_rationale'); req(isinstance(rationale,str) and len(rationale)>=40,f'{iid} requires a substantive admission rationale',e)
        if isinstance(rationale,str):
            for term in BANNED: req(term not in rationale.lower(),f'{iid} admission rationale is candidate-dependent: {term}',e)
        req(r.get('candidate_exposure_status')=='candidate_registry_preexisted_admission_rationale_independent_no_scores_or_results_exposed',f'{iid} must disclose the frozen candidate-registry exposure status',e)
        req(r.get('candidate_independence_attestation') is True,f'{iid} lacks candidate-independence attestation',e)
        req(isinstance(r.get('formalization_boundary'),str) and bool(r.get('formalization_boundary')),f'{iid} lacks formalization boundary',e)
        c=r.get('source_or_observation_contract'); req(isinstance(c,dict),f'{iid} lacks source or observation contract',e)
        if isinstance(c,dict):
            for key in ('kind','source_type','authoritative_fields','observation_boundary','excluded_processes','replay_requirement'): req(bool(c.get(key)),f'{iid} contract lacks {key}',e)
        o=r.get('candidate_neutral_observations'); req(isinstance(o,dict),f'{iid} lacks candidate-neutral observations',e)
        if isinstance(o,dict):
            missing=REQ_OBS-set(o); req(not missing,f"{iid} missing observations: {', '.join(sorted(missing))}",e)
            for key in REQ_OBS: req(o.get(key) not in (None,''),f'{iid} observation {key} is empty',e)
        req(isinstance(r.get('formal_system'),dict) and bool(r.get('formal_system')),f'{iid} lacks formal system',e)
    mins={'positive':8,'contrast':8,'disputed':2}; reg_ids={'positive':'RCS-POSITIVE-CORPUS-001','contrast':'RCS-CONTRAST-CORPUS-001','disputed':'RCS-DISPUTED-CORPUS-001'}; reg_instance_ids={}
    for decision,minimum in mins.items():
        reg=registries.get(decision,{})
        req(reg.get('registry_id')==reg_ids[decision],f'{decision} registry id mismatch',e)
        req(reg.get('corpus_id')=='RCS-CORPUS-001',f'{decision} corpus id mismatch',e)
        req(reg.get('status')=='frozen',f'{decision} registry must be frozen',e)
        req(reg.get('admission_decision')==decision,f'{decision} registry decision mismatch',e)
        req(reg.get('candidate_scoring_status')=='not_started',f'{decision} candidate scoring must remain not_started',e)
        req(reg.get('source_catalog_sha256')==actual_digests.get('catalog'),f'{decision} source catalog digest mismatch',e)
        items=reg.get('instances',[]); req(isinstance(items,list) and len(items)>=minimum,f'{decision} registry requires at least {minimum} instances',e)
        items=items if isinstance(items,list) else []; local_ids=[]; families=set()
        for item in items:
            iid=item.get('instance_id') if isinstance(item,dict) else None
            req(isinstance(iid,str) and iid in by_id,f'{decision} registry references unknown instance: {iid}',e)
            if isinstance(iid,str):
                local_ids.append(iid); src=by_id.get(iid,{})
                req(src.get('admission_decision')==decision,f'{iid} source decision conflicts with registry',e)
                req(item.get('source_record_id')==src.get('source_record_id'),f'{iid} source record link mismatch',e)
                req(item.get('candidate_exposure_status')=='candidate_registry_preexisted_admission_rationale_independent_no_scores_or_results_exposed',f'{iid} registry exposure status mismatch',e)
                req(item.get('candidate_independence_attestation') is True,f'{iid} registry attestation missing',e)
                if isinstance(item.get('family'),str): families.add(item['family'])
        req(len(local_ids)==len(set(local_ids)),f'{decision} registry contains duplicate instance ids',e)
        req(len(families)>=(minimum if decision!='disputed' else 1),f'{decision} family coverage is too narrow',e)
        reg_instance_ids[decision]=local_ids
    req(scope.get('positive_instances')==reg_instance_ids.get('positive'),'scope positive instance list differs from registry',e)
    req(scope.get('contrast_instances')==reg_instance_ids.get('contrast'),'scope contrast instance list differs from registry',e)
    req(scope.get('disputed_instances')==reg_instance_ids.get('disputed'),'scope disputed instance list differs from registry',e)
    req(result.get('result_id')=='W35-CORPUS-FREEZE-RESULT-001','freeze result id mismatch',e)
    req(result.get('artifact_id')=='RCS-CORPUS-001','freeze artifact id mismatch',e)
    req(result.get('status')=='complete','freeze result must be complete',e)
    req(result.get('freeze_status')=='frozen_candidate_independent_with_declared_candidate_registry_exposure','freeze result status mismatch',e)
    req(result.get('candidate_scoring_status')=='not_started','freeze result must precede candidate scoring',e)
    req(result.get('execution_status')=='ready_for_candidate_neutral_execution','freeze result execution status mismatch',e)
    req(result.get('counts')=={'positive':8,'contrast':8,'disputed':2,'total':18},'freeze result counts mismatch',e)
    for key in ('all_decisions_precede_candidate_scoring','all_candidate_exposure_statuses_explicit','candidate_registry_preexisted','candidate_scores_or_results_not_exposed_before_admission','all_records_have_source_or_observation_contracts','all_records_have_formalization_boundaries','all_records_have_candidate_neutral_observations','all_records_replayable_within_boundary'): req(result.get('admission_assurance',{}).get(key) is True,f'freeze result assurance {key} must be true',e)
    for result_key,digest_key in {'source_catalog':'catalog','positive_registry':'positive','contrast_registry':'contrast','disputed_registry':'disputed'}.items(): req(result.get('artifacts',{}).get(result_key,{}).get('content_sha256')==actual_digests.get(digest_key),f'freeze result digest mismatch for {result_key}',e)
    stage=w35.get('status')
    req(stage in {'in_progress_corpus_frozen','in_progress_factorization_complete','in_progress_specificity_complete'},'W3.5 must remain in a recognized in-progress stage after corpus freeze',e)
    req(w35.get('W5_blocked_until_resolved') is True,'W5 block must remain active',e)
    req(w35.get('w5_authorized') is False,'W5 must remain unauthorized',e)
    current=w35.get('current_results',{})
    req(current.get('reasoning_contrast_corpus')=='frozen','W3.5 current corpus result must be frozen',e)
    expected_disc='bounded_role_conjunctive_discrimination_established' if stage=='in_progress_specificity_complete' else 'not_executed'
    req(current.get('reasoning_discrimination')==expected_disc,'reasoning discrimination stage is inconsistent',e)
    req(current.get('candidate_invariants')=='not_executed','candidate tests must remain not_executed',e)
    arts={a.get('id'):a for a in w35.get('required_result_artifacts',[]) if isinstance(a,dict)}
    ca=arts.get('W35-CORPUS-RESULT',{})
    req(ca.get('status')=='complete','W35-CORPUS-RESULT must be complete',e)
    req(ca.get('artifact_id')=='RCS-CORPUS-001','W35-CORPUS-RESULT artifact id mismatch',e)
    req(ca.get('content_sha256')==actual_digests.get('result'),'W35-CORPUS-RESULT digest mismatch',e)
    allowed_complete={'W35-CORPUS-RESULT'}
    if stage in {'in_progress_factorization_complete','in_progress_specificity_complete'}: allowed_complete.add('W35-FACTOR-RESULT')
    if stage=='in_progress_specificity_complete': allowed_complete|={'W35-SPEC-RESULT','W35-SCOPE-RESULT'}
    for aid,a in arts.items():
        if aid not in allowed_complete: req(a.get('status')=='missing',f'{aid} must remain missing',e)
    gm={g.get('name'):g for g in gates.get('gates',[]) if isinstance(g,dict)}
    gate=gm.get('reasoning-contrast-corpus-frozen',{})
    req(gate.get('status')=='satisfied','reasoning-contrast-corpus-frozen gate must be satisfied',e)
    needed={PATHS['doc'],PATHS['audit'],PATHS['catalog'],PATHS['positive'],PATHS['contrast'],PATHS['disputed'],PATHS['result']}
    req(needed<=set(gate.get('evidence',[])),'corpus gate evidence is incomplete',e)
    req(gm.get('baseline-factorization-resolved',{}).get('status') in {'not_satisfied','satisfied'},'baseline factorization gate has invalid status',e)
    expected_later='satisfied' if stage=='in_progress_specificity_complete' else 'not_satisfied'
    for name in ('fara-specificity-resolved','reasoning-contrast-execution'): req(gm.get(name,{}).get('status')==expected_later,f'{name} stage is inconsistent',e)
    req(gm.get('universal-structure-result',{}).get('status')=='not_satisfied','universal-structure-result must remain not_satisfied',e)
    return e

def validate(root:Path=ROOT)->list[str]:
    errors=[]
    for label,rel in PATHS.items():
        if not (root/rel).is_file(): errors.append(f'missing {label}: {rel}')
    if errors: return errors
    digests={k:sha(root/PATHS[k]) for k in ('catalog','positive','contrast','disputed','result')}
    catalog=load(root/PATHS['catalog']); source_records=[]; bundle_digests={}; bundles={}
    for entry in catalog.get('records',[]):
        relative=entry.get('bundle_path',''); path=root/relative
        if not path.is_file(): errors.append(f"missing source bundle: {relative}"); continue
        if relative not in bundles: bundles[relative]=load(path); bundle_digests[relative]=sha(path)
        records=bundles[relative].get('records',[]); index=entry.get('record_index')
        if not isinstance(index,int) or index<0 or index>=len(records): errors.append(f"invalid source bundle index: {entry.get('instance_id')}"); continue
        source_records.append(records[index])
    if errors: return errors
    return validate_data(scope=load(root/PATHS['scope']),catalog=catalog,source_records=source_records,registries={k:load(root/PATHS[k]) for k in ('positive','contrast','disputed')},result=load(root/PATHS['result']),w35=load(root/PATHS['w35']),gates=load(root/PATHS['gates']),actual_digests=digests,actual_bundle_digests=bundle_digests)

def main()->int:
    errors=validate()
    if errors:
        print(f'{FAILURE_CODE}: W3.5 concrete corpus freeze FAILED')
        for error in errors: print(f'- {error}')
        return 1
    print('W3.5 concrete corpus freeze PASS (8 positive; 8 contrast; 2 disputed; admission frozen; candidate scoring not started; W5 blocked)')
    return 0
if __name__=='__main__': raise SystemExit(main())
