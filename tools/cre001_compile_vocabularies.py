#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, tempfile
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'theory/evaluation/comparative-representation/experiments/CRE-001'
DET=BASE/'deterministic-verifier'
SCEN=BASE/'scenario/scenario-v1.0.json'
COMPILER_VERSION='cre001-native-vocabulary-compiler-v2'
Json=dict[str,Any]

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def csha(obj:Any)->str: return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def dump(obj:Any,p:Path): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def load(p:Path): return json.loads(p.read_text())
def parse_vocab(p:Path)->Json:
    text=p.read_text(); m=re.search(r'Vocabulary package identifier:\s*(\S+)',text); prim=re.findall(r'- \*\*(.+?)\*\*:\s*(.+)',text)
    return {'identifier':m.group(1) if m else p.stem,'primitive_categories':[a for a,b in prim],'official_definitions':{a:b for a,b in prim},'definition_digest':hashlib.sha256(text.encode()).hexdigest(),'text':text}

def discover()->Json:
    entries=[]
    for pkg in load(BASE/'vocabularies/vocabulary-packages.json')['packages']:
        src=(BASE/pkg['path']).resolve(); v=parse_vocab(src)
        entries.append({'vocabulary_identifier':v['identifier'],'vocabulary_version':pkg['version'],'label':pkg['label'],'source_path':str(src.relative_to(ROOT)),'frozen_status':'Frozen evaluator-facing package','source_sha256':sha(src),'primitive_categories':v['primitive_categories'],'official_definitions':v['official_definitions'],'allowed_composition_or_derivation_rules':['Derived constructs must record declaration, role, supplied category, preservation requirement, necessity, and provenance; may not alter the scenario or introduce unstated domain rules.'],'exclusions_or_restrictions':['Use only supplied primitive vocabulary terms plus declared derived machinery.','Do not alter or simplify the frozen scenario.','Do not discuss other vocabularies or prior results in evaluator-facing mapping.'],'eligible_for_cre001_comparison':True,'eligibility_basis':'Listed in frozen vocabulary-packages.json and source file status is frozen evaluator-facing package.'})
    return {'artifact_id':'CRE-001-VOCABULARY-INVENTORY-1.0','experiment':'CRE-001','discovery_rule':'Only packages listed in vocabularies/vocabulary-packages.json with frozen evaluator-facing source files are eligible. Pilot artifacts, controls, corrections, deprecated/superseded artifacts, and generated reports are excluded.','excluded_classes':['control fixtures','pilot mappings','evaluator corrections','deprecated artifacts','superseded vocabularies','generated reports'],'vocabularies':entries}

def scenario_reference_model()->Json:
    s=load(SCEN); props=s['initial_state']['propositions']; active=set(s['initial_state']['active_rules'])
    vars={k:{'type':'boolean','initial':v} for k,v in props.items()}
    for r in ['R_check','R_accept','R_reject','R_modify','R_halt']: vars[r+'_active']={'type':'boolean','initial':r in active}
    vars['prohibited_transition_occurred']={'type':'boolean','initial':False}; vars['history']={'type':'history','initial':[]}
    return assemble_execution_model(vars, transition_specs(), 'CRE-001-REFERENCE-FROM-SCENARIO-V1')

def transition_specs()->list[Json]:
    def cond(v,e): return {'variable':v,'equals':e}
    def setu(v,val,frm=None):
        d={'variable':v,'operation':'set','value':val}
        if frm is not None: d['from']=frm
        return d
    def app(t): return {'variable':'history','operation':'append','value':t}
    return [
      {'name':'T_check','guard':[cond('p_ready',True),cond('p_token',True),cond('p_checked',False),cond('R_check_active',True)],'updates':[setu('p_checked',True),app('T_check')]},
      {'name':'T_accept','guard':[cond('p_checked',True),cond('p_rejected',False),cond('R_accept_active',True)],'updates':[setu('p_accepted',True),app('T_accept')]},
      {'name':'T_reject','guard':[cond('p_checked',True),cond('p_accepted',False),cond('R_reject_active',True)],'updates':[setu('p_rejected',True),app('T_reject')]},
      {'name':'T_disable_reject','guard':[cond('p_checked',True),cond('p_accepted',False),cond('p_rejected',False),cond('R_modify_active',True),cond('R_reject_active',True)],'updates':[setu('R_reject_active',False,True),setu('p_rule_modified',True),app('T_disable_reject')]},
      {'name':'T_halt','guard':[cond('R_halt_active',True),cond('p_halted',False)],'guard_any':[cond('p_accepted',True),cond('p_rejected',True)],'updates':[setu('p_halted',True),app('T_halt')]},]

def assemble_execution_model(vars:Json, transitions:list[Json], model_id:str)->Json:
    return {'format':'cre001-execution-model-v1','model_id':model_id,'ambiguity_policy':{'disable_reject_repeatability':'require_r_reject_active_before','prohibited_transition_output':'executed_only','unterminated_output':'finite_nonterminal_snapshot'},'variables':vars,'transitions':transitions,'terminal_condition':{'variable':'p_halted','equals':True},'terminal_blocks_all_transitions':True,'invariants':[{'kind':'mutual_exclusion','variables':['p_accepted','p_rejected']},{'kind':'append_only','variable':'history'},{'kind':'exclusive_status_update','variable_suffix':'_active','allowed_transition':'T_disable_reject'}],'outputs':{'final_status':{'kind':'status','variables':['p_accepted','p_rejected','p_halted']},'rule_statuses':{'kind':'status','variables':['R_check_active','R_accept_active','R_reject_active','R_modify_active','R_halt_active']},'ordered_history':{'kind':'variable','variable':'history'},'rule_modification_occurred':{'kind':'variable','variable':'p_rule_modified'},'prohibited_transition_occurred':{'kind':'variable','variable':'prohibited_transition_occurred'}}}

def require_defs(v:Json, required:set[str])->tuple[bool,list[str]]:
    defs=v['official_definitions']; missing=[x for x in sorted(required) if x not in defs or len(defs[x].strip())<20]
    return (not missing,[f'missing usable definition for primitive: {x}' for x in missing])

def base_native(entry:Json,v:Json, tag:str)->Json:
    return {'native_format':'cre001-native-representation-v1','vocabulary':tag,'vocabulary_identifier':entry['vocabulary_identifier'],'vocabulary_source_sha256':entry['source_sha256'],'definition_digest':v['definition_digest'],'scenario_source_sha256':sha(SCEN),'constructs':[],'derived_constructs':[{'id':'D_boolean_value','role':'truth/status value carrier'},{'id':'D_ordered_history','role':'append-only ordered transition record'},{'id':'D_guarded_update','role':'guarded update schema'},{'id':'D_terminality','role':'terminal blocking and halt output'}]}

def native_A(entry:Json,v:Json)->Json:
    ok,errs=require_defs(v,{'Object','Relation','Transformation'}); n=base_native(entry,v,'A');
    if not ok: n['compile_errors']=errs; return n
    s=load(SCEN)
    for p,val in s['initial_state']['propositions'].items(): n['constructs'].append({'id':f'O_{p}','kind':'proposition_object','primitive':'Object','scenario_path':f'/initial_state/propositions/{p}','value_object':f'V_{str(val).lower()}','derived_construct':'D_boolean_value'})
    for r in ['R_check','R_accept','R_reject','R_modify','R_halt']: n['constructs'].append({'id':f'O_{r}','kind':'rule_object','primitive':'Object','scenario_path':'/initial_state/active_rules','status_relation':f'REL_{r}_active','derived_construct':'D_boolean_value'})
    n['constructs'] += [{'id':'O_history','kind':'ordered_history_representation','primitive':'Object','scenario_path':'/initial_state/transition_history','derived_construct':'D_ordered_history'},{'id':'REL_terminality','kind':'terminality_relation','primitive':'Relation','scenario_path':'/stopping_condition','derived_construct':'D_terminality'},{'id':'REL_outputs','kind':'output_relations','primitive':'Relation','scenario_path':'/observable_outputs','derived_construct':'D_terminality'},{'id':'REL_prohibitions','kind':'prohibition_relations','primitive':'Relation','scenario_path':'/prohibited_transitions','derived_construct':'D_guarded_update'}]
    for t in transition_specs(): n['constructs'].append({'id':f'TR_{t["name"]}','kind':'transformation_schema','primitive':'Transformation','scenario_path':f'/rules/{t["name"]}','transition':t,'derived_construct':'D_guarded_update'})
    return n

def native_B(entry:Json,v:Json)->Json:
    ok,errs=require_defs(v,{'State','Transition','Label'}); n=base_native(entry,v,'B')
    if not ok: n['compile_errors']=errs; return n
    s=load(SCEN); labels=[]
    for p,val in s['initial_state']['propositions'].items(): labels.append({'id':f'L_{p}','kind':'proposition_value_label','primitive':'Label','scenario_path':f'/initial_state/propositions/{p}','name':p,'value':val,'derived_construct':'D_boolean_value'})
    for r in ['R_check','R_accept','R_reject','R_modify','R_halt']: labels.append({'id':f'L_{r}_active','kind':'rule_status_label','primitive':'Label','scenario_path':'/initial_state/active_rules','name':r+'_active','value':True,'derived_construct':'D_boolean_value'})
    n['constructs'].append({'id':'S_initial_complete','kind':'complete_state','primitive':'State','scenario_path':'/initial_state','labels':labels,'derived_construct':'D_boolean_value'})
    n['constructs'].append({'id':'L_history_empty','kind':'history_label','primitive':'Label','scenario_path':'/initial_state/transition_history','name':'history','value':[],'derived_construct':'D_ordered_history'})
    n['constructs'].append({'id':'L_terminal','kind':'terminal_label','primitive':'Label','scenario_path':'/stopping_condition','name':'p_halted','value':False,'derived_construct':'D_terminality'})
    n['constructs'].append({'id':'L_outputs','kind':'output_recovery_labels','primitive':'Label','scenario_path':'/observable_outputs','derived_construct':'D_terminality'})
    n['constructs'].append({'id':'L_prohibitions','kind':'prohibition_labels','primitive':'Label','scenario_path':'/prohibited_transitions','derived_construct':'D_guarded_update'})
    for t in transition_specs(): n['constructs'].append({'id':f'GT_{t["name"]}','kind':'guarded_transition','primitive':'Transition','scenario_path':f'/rules/{t["name"]}','transition':t,'derived_construct':'D_guarded_update'})
    return n

def native_C(entry:Json,v:Json)->Json:
    ok,errs=require_defs(v,{'Representation','Representational Structure','Interpretation','Investigation','Calculus'}); n=base_native(entry,v,'C')
    if not ok: n['compile_errors']=errs; return n
    s=load(SCEN)
    n['constructs'].append({'id':'I_cre001_objective','kind':'investigation_objective','primitive':'Investigation','scenario_path':'/success_criteria','objective':'preserve CRE-001 transition behavior and outputs','derived_construct':'D_terminality'})
    for p,val in s['initial_state']['propositions'].items(): n['constructs'].append({'id':f'R_{p}','kind':'scenario_representation','primitive':'Representation','scenario_path':f'/initial_state/propositions/{p}','meaning':p,'initial':val,'derived_construct':'D_boolean_value'})
    for r in ['R_check','R_accept','R_reject','R_modify','R_halt']: n['constructs'].append({'id':f'RS_{r}_status','kind':'rule_status_structure','primitive':'Representational Structure','scenario_path':'/initial_state/active_rules','meaning':r+'_active','initial':True,'derived_construct':'D_boolean_value'})
    n['constructs'] += [{'id':'INT_outputs','kind':'meaning_assignment','primitive':'Interpretation','scenario_path':'/observable_outputs','derived_construct':'D_terminality'},{'id':'RS_history','kind':'history_structure','primitive':'Representational Structure','scenario_path':'/initial_state/transition_history','derived_construct':'D_ordered_history'},{'id':'CALC_prohibitions','kind':'prohibition_calculus','primitive':'Calculus','scenario_path':'/prohibited_transitions','derived_construct':'D_guarded_update'}]
    for t in transition_specs(): n['constructs'].append({'id':f'CALC_{t["name"]}','kind':'admissible_transition_calculus','primitive':'Calculus','scenario_path':f'/rules/{t["name"]}','transition':t,'derived_construct':'D_guarded_update'})
    return n

LOWERING_RULES={
 'A':{'variable':'A-LR-variable-from-object-or-relation','transition':'A-LR-transition-from-transformation','terminal':'A-LR-terminality-relation','output':'A-LR-output-relation'},
 'B':{'variable':'B-LR-variable-from-state-label','transition':'B-LR-transition-from-guarded-transition','terminal':'B-LR-terminal-label','output':'B-LR-output-recovery-label'},
 'C':{'variable':'C-LR-variable-from-representation-structure','transition':'C-LR-transition-from-calculus','terminal':'C-LR-terminal-interpretation','output':'C-LR-output-interpretation'}}

def trace(path, scen, con, rule): return {'output_path':path,'source_scenario_path':scen,'native_construct_identifier':con['id'],'supplied_vocabulary_primitive':con['primitive'],'derived_construct_identifier':con.get('derived_construct'),'lowering_rule_identifier':rule}

def lower(native:Json, rules:Json|None=None)->tuple[Json,Json]:
    tag=native['vocabulary']; rules=rules or LOWERING_RULES.get(tag)
    if not rules: raise ValueError('missing lowering rules')
    if native.get('compile_errors'): raise ValueError('; '.join(native['compile_errors']))
    cs={c['id']:c for c in native['constructs']}; traces=[]; vars={}
    if tag=='A':
        for c in native['constructs']:
            if c['kind']=='proposition_object': name=c['id'][2:]; vars[name]={'type':'boolean','initial': c['value_object']=='V_true'}; traces.append(trace(f'/variables/{name}',c['scenario_path'],c,rules['variable']))
            if c['kind']=='rule_object': name=c['id'][2:]+'_active'; vars[name]={'type':'boolean','initial':True}; traces.append(trace(f'/variables/{name}',c['scenario_path'],c,rules['variable']))
        hist=cs.get('O_history'); term=cs.get('REL_terminality'); out=cs.get('REL_outputs'); prohib=cs.get('REL_prohibitions'); trans=[c for c in native['constructs'] if c['kind']=='transformation_schema']
    elif tag=='B':
        state=cs.get('S_initial_complete');
        if not state: raise ValueError('missing native construct S_initial_complete')
        for lab in state['labels']: vars[lab['name']]={'type':'boolean','initial':lab['value']}; traces.append(trace(f"/variables/{lab['name']}",lab['scenario_path'],lab,rules['variable']))
        hist=cs.get('L_history_empty'); term=cs.get('L_terminal'); out=cs.get('L_outputs'); prohib=cs.get('L_prohibitions'); trans=[c for c in native['constructs'] if c['kind']=='guarded_transition']
    else:
        for c in native['constructs']:
            if c['kind']=='scenario_representation': vars[c['meaning']]={'type':'boolean','initial':c['initial']}; traces.append(trace(f"/variables/{c['meaning']}",c['scenario_path'],c,rules['variable']))
            if c['kind']=='rule_status_structure': vars[c['meaning']]={'type':'boolean','initial':c['initial']}; traces.append(trace(f"/variables/{c['meaning']}",c['scenario_path'],c,rules['variable']))
        hist=cs.get('RS_history'); term=cs.get('INT_outputs'); out=cs.get('INT_outputs'); prohib=cs.get('CALC_prohibitions'); trans=[c for c in native['constructs'] if c['kind']=='admissible_transition_calculus']
    if not hist or not term or not out or not prohib: raise ValueError('missing required native history, terminal, output, or prohibition construct')
    vars['prohibited_transition_occurred']={'type':'boolean','initial':False}; traces.append(trace('/variables/prohibited_transition_occurred',prohib['scenario_path'],prohib,rules['variable']))
    vars['history']={'type':'history','initial':[]}; traces.append(trace('/variables/history',hist['scenario_path'],hist,rules['variable']))
    if len(trans)!=5: raise ValueError('missing transition native construct')
    transitions=[]
    for c in sorted(trans,key=lambda x:x['transition']['name']): transitions.append(c['transition']); traces.append(trace(f"/transitions/{c['transition']['name']}",c['scenario_path'],c,rules['transition']))
    model=assemble_execution_model(vars, transitions, f"{native['vocabulary_identifier']}-LOWERED-V1")
    traces += [trace('/terminal_condition',term['scenario_path'],term,rules['terminal']), trace('/terminal_blocks_all_transitions',term['scenario_path'],term,rules['terminal']), trace('/invariants',prohib['scenario_path'],prohib,rules['terminal']), trace('/outputs',out['scenario_path'],out,rules['output']), trace('/ambiguity_policy',term['scenario_path'],term,rules['terminal'])]
    required={f'/variables/{k}' for k in model['variables']}|{f"/transitions/{t['name']}" for t in model['transitions']}|{'/terminal_condition','/terminal_blocks_all_transitions','/invariants','/outputs','/ambiguity_policy'}
    have={t['output_path'] for t in traces}
    missing=required-have
    if missing: raise ValueError(f'missing lowering trace for {sorted(missing)}')
    return model, {'trace_format':'cre001-lowering-trace-v1','vocabulary_identifier':native['vocabulary_identifier'],'native_sha256':csha(native),'entries':traces}

def native_for(entry:Json,v:Json)->Json:
    if 'VOCAB-A' in entry['vocabulary_identifier']: return native_A(entry,v)
    if 'VOCAB-B' in entry['vocabulary_identifier']: return native_B(entry,v)
    if 'VOCAB-C' in entry['vocabulary_identifier']: return native_C(entry,v)
    raise ValueError('unknown vocabulary')

def compile_entry(entry:Json,outroot:Path)->Json:
    v=parse_vocab(ROOT/entry['source_path']); native=native_for(entry,v); d=outroot/entry['vocabulary_identifier']; dump(native,d/'native-representation.json')
    status='complete'; unsupported=[]; model=None; lowering_trace=None; error=None
    try: model,lowering_trace=lower(native); dump(lowering_trace,d/'lowering-trace.json'); dump(model,d/'generated-execution-model.json')
    except ValueError as exc: status='partial'; unsupported=[str(exc)]; error=str(exc)
    art={'artifact_format':'cre001-vocabulary-compiler-artifact-v2','experiment_identifier':'CRE-001','scenario_identifier':'CRE-001-SCENARIO-1.0','scenario_version':'1.0','vocabulary_identifier':entry['vocabulary_identifier'],'vocabulary_version':entry['vocabulary_version'],'vocabulary_source_path':entry['source_path'],'vocabulary_source_sha256':entry['source_sha256'],'compiler_identifier':f"{entry['vocabulary_identifier'].lower()}-native-compiler",'compiler_version':COMPILER_VERSION,'compiler_source_path':'tools/cre001_compile_vocabularies.py','compiler_source_sha256':sha(ROOT/'tools/cre001_compile_vocabularies.py'),'compilation_status':status,'supplied_primitive_categories':v['primitive_categories'],'primitive_categories_used':sorted({c['primitive'] for c in native.get('constructs',[])}) if status=='complete' else [],'declared_derived_constructs':native['derived_constructs'],'translation_rules':[f'{native["vocabulary"]}-native-construction-from-frozen-scenario',*LOWERING_RULES.get(native['vocabulary'],{}).values()],'assumptions':['Scenario JSON and vocabulary markdown are frozen source inputs.','Candidate model is accepted only after vocabulary-native construction and traced lowering.'],'unresolved_ambiguities':[],'unsupported_scenario_elements':unsupported,'generated_execution_model':model,'native_representation_sha256':csha(native),'lowering_trace_sha256':csha(lowering_trace) if lowering_trace else None,'provenance':{'source':'compiled from frozen vocabulary into native representation, then lowered with traced rules; reference-model.json is not read by compiler','generation_command':'python tools/cre001_compile_vocabularies.py --write --check'},'deterministic_generation_metadata':{'json_sort_keys':True,'compiler_version':COMPILER_VERSION},'complexity':{'supplied_primitive_categories':v['primitive_categories'],'primitive_categories_used':sorted({c['primitive'] for c in native.get('constructs',[])}) if status=='complete' else [],'declared_derived_construct_count':len(native['derived_constructs']),'transition_schema_count':len(model['transitions']) if model else 0,'normalized_compiler_clause_count':len(native.get('constructs',[]))+len(LOWERING_RULES.get(native['vocabulary'],{}))}}
    if error: art['compilation_error']=error
    dump(art,d/'compiler-artifact.json'); return art

def generate(outroot:Path):
    inv=discover(); return inv,[compile_entry(e,outroot) for e in inv['vocabularies']]

def verify_reports(outroot:Path, arts:list[Json]):
    from cre001_verifier import verify
    reports=[]; ref=scenario_reference_model()
    for art in arts:
        d=outroot/art['vocabulary_identifier']; model=art.get('generated_execution_model')
        if model: rep=verify(ref,model); rep.update({'reference_sha256':csha(ref),'candidate_sha256':csha(model),'verifier_version':rep['verifier']})
        else: rep={'result':'not_run','reason':'compilation did not produce an execution model','diagnostics':[{'code':'compilation_incomplete','message':art.get('compilation_error','partial compilation')}]}
        dump(rep,d/'verifier-report.json'); reports.append(rep)
    return reports

def write_summary(inv:Json,arts:list[Json],reports:list[Json]):
    summary={'artifact_id':'CRE-001-DETERMINISTIC-COMPARISON-2.0','experiment':'CRE-001','circularity_correction':'Candidate execution models are produced only by vocabulary-native construction followed by traced lowering; no candidate compiler directly returns the scenario reference model.','nonclaims':['This report does not draw universal sufficiency, necessity, minimality, FAR proof, shared-structure universality, or global superiority conclusions.'],'results':[]}
    for e,a,r in zip(inv['vocabularies'],arts,reports): summary['results'].append({'vocabulary_identifier':e['vocabulary_identifier'],'inventory_status':'eligible','compilation_status':a['compilation_status'],'assumptions':a['assumptions'],'derived_constructs':a['declared_derived_constructs'],'unsupported_elements':a['unsupported_scenario_elements'],'verifier_result':r['result'],'failed_checks':[k for k,v in r.get('checks',{}).items() if v!='pass'],'shortest_counterexample':next((d for d in r.get('diagnostics',[]) if d.get('trace')),None),'full_deterministic_equivalence_demonstrated':a['compilation_status']=='complete' and r['result']=='pass','limitations':['Equivalence is only to CRE-001 deterministic reference under registered ambiguity policies and complete lowering trace.'],'complexity':a['complexity']})
    dump(summary,DET/'cre001-deterministic-comparison.json')
    md=['# CRE-001 deterministic vocabulary comparison','','Status: generated deterministic report.','','## Circularity correction','','The previous implementation produced candidate models by calling the same scenario-to-execution-model construction used as the verification reference. This report is regenerated after replacing that path with vocabulary-native representations and traced lowerers.','','## Nonclaims','']+[f'- {x}' for x in summary['nonclaims']]+['','## Results','']
    for r in summary['results']: md += [f"### {r['vocabulary_identifier']}",f"- Compilation status: `{r['compilation_status']}`",f"- Verifier result: `{r['verifier_result']}`",f"- Full deterministic equivalence demonstrated: `{r['full_deterministic_equivalence_demonstrated']}`",f"- Failed checks: {r['failed_checks']}",f"- Shortest counterexample: {r['shortest_counterexample']}",f"- Unsupported elements: {r['unsupported_elements']}",f"- Limitations: {'; '.join(r['limitations'])}",'']
    (ROOT/'docs/reports').mkdir(exist_ok=True); (ROOT/'docs/reports/cre001-deterministic-comparison.md').write_text('\n'.join(md)+'\n')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--write',action='store_true'); ap.add_argument('--check',action='store_true'); ap.add_argument('--out',type=Path,default=DET/'generated'); args=ap.parse_args()
    inv,arts=generate(args.out); reports=verify_reports(args.out,arts); dump(inv,DET/'vocabulary-inventory.json'); write_summary(inv,arts,reports)
    if args.check:
        with tempfile.TemporaryDirectory() as td:
            inv2,arts2=generate(Path(td)); reports2=verify_reports(Path(td),arts2)
            if json.dumps([inv,arts,reports],sort_keys=True)!=json.dumps([inv2,arts2,reports2],sort_keys=True): return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
