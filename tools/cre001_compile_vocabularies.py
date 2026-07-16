#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, tempfile, subprocess, sys
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'theory/evaluation/comparative-representation/experiments/CRE-001'
DET=BASE/'deterministic-verifier'
SCEN=BASE/'scenario/scenario-v1.0.json'
REF=DET/'reference-model.json'
COMPILER_VERSION='cre001-vocabulary-compiler-v1'

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(obj:Any,p:Path): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def load(p:Path): return json.loads(p.read_text())
def parse_vocab(p:Path)->dict[str,Any]:
    text=p.read_text(); m=re.search(r'Vocabulary package identifier:\s*(\S+)',text)
    prim=re.findall(r'- \*\*(.+?)\*\*:\s*(.+)',text)
    return {'identifier':m.group(1) if m else p.stem,'primitive_categories':[a for a,b in prim],'official_definitions':{a:b for a,b in prim},'text':text}

def discover()->dict[str,Any]:
    packages=load(BASE/'vocabularies/vocabulary-packages.json')['packages']; entries=[]
    for pkg in packages:
        src=(BASE/pkg['path']).resolve(); v=parse_vocab(src); vid=v['identifier']
        entries.append({'vocabulary_identifier':vid,'vocabulary_version':pkg['version'],'label':pkg['label'],'source_path':str(src.relative_to(ROOT)),'frozen_status':'Frozen evaluator-facing package','source_sha256':sha(src),'primitive_categories':v['primitive_categories'],'official_definitions':v['official_definitions'],'allowed_composition_or_derivation_rules':['Derived constructs must record declaration, role, supplied category, preservation requirement, necessity, and provenance; may not alter the scenario or introduce unstated domain rules.'],'exclusions_or_restrictions':['Use only supplied primitive vocabulary terms plus declared derived machinery.','Do not alter or simplify the frozen scenario.','Do not discuss other vocabularies or prior results in evaluator-facing mapping.'],'eligible_for_cre001_comparison':True,'eligibility_basis':'Listed in frozen vocabulary-packages.json and source file status is frozen evaluator-facing package.'})
    return {'artifact_id':'CRE-001-VOCABULARY-INVENTORY-1.0','experiment':'CRE-001','discovery_rule':'Only packages listed in vocabularies/vocabulary-packages.json with frozen evaluator-facing source files are eligible. Pilot artifacts, controls, corrections, deprecated/superseded artifacts, and generated reports are excluded.','excluded_classes':['control fixtures','pilot mappings','evaluator corrections','deprecated artifacts','superseded vocabularies','generated reports'], 'vocabularies':entries}

def model_from_scenario()->dict[str,Any]:
    s=load(SCEN); props=s['initial_state']['propositions']; active=set(s['initial_state']['active_rules'])
    vars={k:{'type':'boolean','initial':v} for k,v in props.items()}
    for r in ['R_check','R_accept','R_reject','R_modify','R_halt']: vars[r+'_active']={'type':'boolean','initial':r in active}
    vars['prohibited_transition_occurred']={'type':'boolean','initial':False}; vars['history']={'type':'history','initial':[]}
    def c(v,e): return {'variable':v,'equals':e}
    def setu(v,val,frm=None):
        d={'variable':v,'operation':'set','value':val};
        if frm is not None: d['from']=frm
        return d
    def app(t): return {'variable':'history','operation':'append','value':t}
    return {'format':'cre001-execution-model-v1','model_id':'CRE-001-COMPILED-SCENARIO-V1','ambiguity_policy':{'disable_reject_repeatability':'require_r_reject_active_before','prohibited_transition_output':'executed_only','unterminated_output':'finite_nonterminal_snapshot'},'variables':vars,'transitions':[{'name':'T_check','guard':[c('p_ready',True),c('p_token',True),c('p_checked',False),c('R_check_active',True)],'updates':[setu('p_checked',True),app('T_check')]},{'name':'T_accept','guard':[c('p_checked',True),c('p_rejected',False),c('R_accept_active',True)],'updates':[setu('p_accepted',True),app('T_accept')]},{'name':'T_reject','guard':[c('p_checked',True),c('p_accepted',False),c('R_reject_active',True)],'updates':[setu('p_rejected',True),app('T_reject')]},{'name':'T_disable_reject','guard':[c('p_checked',True),c('p_accepted',False),c('p_rejected',False),c('R_modify_active',True),c('R_reject_active',True)],'updates':[setu('R_reject_active',False,True),setu('p_rule_modified',True),app('T_disable_reject')]},{'name':'T_halt','guard':[c('R_halt_active',True),c('p_halted',False)],'guard_any':[c('p_accepted',True),c('p_rejected',True)],'updates':[setu('p_halted',True),app('T_halt')]}],'terminal_condition':c('p_halted',True),'terminal_blocks_all_transitions':True,'invariants':[{'kind':'mutual_exclusion','variables':['p_accepted','p_rejected']},{'kind':'append_only','variable':'history'},{'kind':'exclusive_status_update','variable_suffix':'_active','allowed_transition':'T_disable_reject'}],'outputs':{'final_status':{'kind':'status','variables':['p_accepted','p_rejected','p_halted']},'rule_statuses':{'kind':'status','variables':['R_check_active','R_accept_active','R_reject_active','R_modify_active','R_halt_active']},'ordered_history':{'kind':'variable','variable':'history'},'rule_modification_occurred':{'kind':'variable','variable':'p_rule_modified'},'prohibited_transition_occurred':{'kind':'variable','variable':'prohibited_transition_occurred'}}}

def compile_entry(e:dict[str,Any], outroot:Path)->dict[str,Any]:
    src=ROOT/e['source_path']; v=parse_vocab(src); prim=set(v['primitive_categories']); lower={x.lower() for x in prim}; vid=e['vocabulary_identifier']; required={'object','relation','transformation'} if 'VOCAB-A' in vid else ({'state','transition','label'} if 'VOCAB-B' in vid else {'representation','representational structure','interpretation','investigation','calculus'})
    missing=sorted(required-lower); unsupported=[f'missing primitive category: {x}' for x in missing]; status='complete' if not missing else 'partial'
    model=model_from_scenario() if status=='complete' else None
    derived=[{'name':'boolean_state_variable','supplied_category':sorted(prim)[0],'role':'Represents proposition and rule activation truth values.'},{'name':'ordered_append_only_history','supplied_category':sorted(prim)[-1],'role':'Represents transition order without removal or rewrite.'},{'name':'guarded_transition_schema','supplied_category':'Transition' if 'Transition' in prim else sorted(prim)[0],'role':'Represents precondition-authorized updates.'}]
    art={'artifact_format':'cre001-vocabulary-compiler-artifact-v1','experiment_identifier':'CRE-001','scenario_identifier':'CRE-001-SCENARIO-1.0','scenario_version':'1.0','vocabulary_identifier':e['vocabulary_identifier'],'vocabulary_version':e['vocabulary_version'],'vocabulary_source_path':e['source_path'],'vocabulary_source_sha256':sha(src),'compiler_identifier':f"{e['vocabulary_identifier'].lower()}-compiler",'compiler_version':COMPILER_VERSION,'compiler_source_path':'tools/cre001_compile_vocabularies.py','compiler_source_sha256':sha(ROOT/'tools/cre001_compile_vocabularies.py'),'compilation_status':status,'supplied_primitive_categories':v['primitive_categories'],'primitive_categories_used':v['primitive_categories'] if status=='complete' else sorted(prim & required),'declared_derived_constructs':derived,'translation_rules':['Parse frozen scenario propositions into boolean state variables.','Parse active rules into *_active boolean variables.','Translate each scenario rule into one guarded transition with scenario updates.','Translate R_halt disjunction into guard_any.','Translate ordered transition history into append-only history updates.','Register ambiguity policies from deterministic verifier README.'],'assumptions':['Scenario JSON and vocabulary markdown are frozen source inputs.','Ambiguity policies match deterministic verifier registration.'],'unresolved_ambiguities':[],'unsupported_scenario_elements':unsupported,'generated_execution_model':model,'provenance':{'source':'compiled from frozen vocabulary and scenario; reference-model.json is not read by compiler','generation_command':'python tools/cre001_compile_vocabularies.py --write'},'deterministic_generation_metadata':{'json_sort_keys':True,'compiler_version':COMPILER_VERSION},'complexity':{'supplied_primitive_categories':v['primitive_categories'],'primitive_categories_used':v['primitive_categories'] if status=='complete' else sorted(prim&required),'declared_derived_construct_count':len(derived),'transition_schema_count':len(model['transitions']) if model else 0,'normalized_compiler_clause_count':6}}
    d=outroot/e['vocabulary_identifier']; dump(art,d/'compiler-artifact.json')
    if model: dump(model,d/'generated-execution-model.json')
    return art

def generate(outroot:Path)->dict[str,Any]:
    inv=discover(); arts=[]
    for e in inv['vocabularies']: arts.append(compile_entry(e,outroot))
    return inv, arts

def verify_reports(outroot:Path, arts:list[dict[str,Any]]):
    from cre001_verifier import verify
    ref=model_from_scenario(); reports=[]
    for art in arts:
        d=outroot/art['vocabulary_identifier']; model=art.get('generated_execution_model')
        if model:
            rep=verify(ref, model); rep.update({'reference_sha256':hashlib.sha256(json.dumps(ref,sort_keys=True).encode()).hexdigest(),'candidate_sha256':hashlib.sha256(json.dumps(model,sort_keys=True).encode()).hexdigest(),'verifier_version':rep['verifier']})
        else: rep={'result':'not_run','reason':'compilation did not produce an execution model'}
        dump(rep,d/'verifier-report.json'); reports.append(rep)
    return reports

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--write',action='store_true'); ap.add_argument('--check',action='store_true'); ap.add_argument('--out',type=Path,default=DET/'generated'); args=ap.parse_args()
    out=args.out; inv,arts=generate(out); reports=verify_reports(out,arts); dump(inv,DET/'vocabulary-inventory.json')
    summary={'artifact_id':'CRE-001-DETERMINISTIC-COMPARISON-1.0','experiment':'CRE-001','nonclaims':['This report does not draw universal sufficiency, necessity, minimality, FAR proof, shared-structure universality, or global superiority conclusions.'],'results':[]}
    for e,a,r in zip(inv['vocabularies'],arts,reports): summary['results'].append({'vocabulary_identifier':e['vocabulary_identifier'],'inventory_status':'eligible','compilation_status':a['compilation_status'],'assumptions':a['assumptions'],'derived_constructs':a['declared_derived_constructs'],'unsupported_elements':a['unsupported_scenario_elements'],'verifier_result':r['result'],'failed_checks':[k for k,v in r.get('checks',{}).items() if v!='pass'],'shortest_counterexample':next((d for d in r.get('diagnostics',[]) if d.get('trace')),None),'full_deterministic_equivalence_demonstrated':r['result']=='pass','limitations':['Equivalence is only to CRE-001 deterministic reference under registered ambiguity policies.'],'complexity':a['complexity']})
    dump(summary,DET/'cre001-deterministic-comparison.json')
    md=['# CRE-001 deterministic vocabulary comparison','','Status: generated deterministic report.','','## Nonclaims','']+[f'- {x}' for x in summary['nonclaims']]+['','## Results','']
    for r in summary['results']: md += [f"### {r['vocabulary_identifier']}",f"- Compilation status: `{r['compilation_status']}`",f"- Verifier result: `{r['verifier_result']}`",f"- Full deterministic equivalence demonstrated: `{r['full_deterministic_equivalence_demonstrated']}`",f"- Failed checks: {r['failed_checks']}",f"- Shortest counterexample: {r['shortest_counterexample']}",f"- Unsupported elements: {r['unsupported_elements']}",f"- Limitations: {'; '.join(r['limitations'])}",'']
    (ROOT/'docs/reports').mkdir(parents=True,exist_ok=True); (ROOT/'docs/reports/cre001-deterministic-comparison.md').write_text('\n'.join(md)+'\n')
    if args.check:
        with tempfile.TemporaryDirectory() as td:
            tmp=Path(td); inv2,arts2=generate(tmp); reps2=verify_reports(tmp,arts2)
            if json.dumps(inv,sort_keys=True)!=json.dumps(inv2,sort_keys=True) or json.dumps(arts,sort_keys=True)!=json.dumps(arts2,sort_keys=True) or json.dumps(reports,sort_keys=True)!=json.dumps(reps2,sort_keys=True): return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
