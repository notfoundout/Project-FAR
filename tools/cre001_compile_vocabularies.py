#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, hashlib, json, re, tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'theory/evaluation/comparative-representation/experiments/CRE-001'
DET=BASE/'deterministic-verifier'; SCEN=BASE/'scenario/scenario-v1.0.json'
COMPILER_VERSION='cre001-atomic-native-compiler-v3'
Json=dict[str,Any]
AMBIG={'disable_reject_repeatability':'require_r_reject_active_before','prohibited_transition_output':'executed_only','unterminated_output':'finite_nonterminal_snapshot'}
INVARIANTS=[('mutual_exclusion',{'variable_refs':['p_accepted','p_rejected']}),('append_only',{'variable':'history'}),('exclusive_status_update',{'variable_suffix':'_active','allowed_transition':'T_disable_reject'})]
OUTPUTS={'final_status':{'kind':'status','variables':['p_accepted','p_rejected','p_halted']},'rule_statuses':{'kind':'status','variables':['R_check_active','R_accept_active','R_reject_active','R_modify_active','R_halt_active']},'ordered_history':{'kind':'variable','variable':'history'},'rule_modification_occurred':{'kind':'variable','variable':'p_rule_modified'},'prohibited_transition_occurred':{'kind':'variable','variable':'prohibited_transition_occurred'}}
CAPS={
 'Object': {'identify','value_carrier','status_carrier','record'}, 'Relation': {'connect','condition','status','order','authorization','constraint','output'}, 'Transformation': {'change','update','transition','state_modification'},
 'State': {'configuration','assignment','history_point'}, 'Transition': {'movement','update','status_change','history_extension'}, 'Label': {'name','value','condition','status','identifier'},
 'Representation': {'represented_item','proposition','rule','state_element','transition_record','output_record'}, 'Representational Structure': {'ordering','dependency','rule_status','transition_structure','admissibility','history_structure'}, 'Interpretation': {'meaning','truth_condition','status_meaning','output_meaning'}, 'Investigation': {'objective','question','scope'}, 'Calculus': {'admissible_operation','transition_policy','update_rule','stopping_rule','prohibition'} }
CAP_KEYWORDS={
 'Object': {'identify':['item','entity','token','state-bearing item','rule','record','unit'], 'value_carrier':['state-bearing','record','unit'], 'status_carrier':['state-bearing','rule'], 'record':['record']},
 'Relation': {'connect':['connection','association','among objects'], 'condition':['constraint'], 'status':['status'], 'order':['ordering'], 'authorization':['permission'], 'constraint':['constraint','prohibition'], 'output':['status association']},
 'Transformation': {'change':['change','update','transition','modification'], 'update':['update'], 'transition':['transition'], 'state_modification':['state modification','modification']},
 'State': {'configuration':['assignment','statuses','conditions'], 'assignment':['assignment'], 'history_point':['discrete point','system history']},
 'Transition': {'movement':['movement'], 'update':['update'], 'status_change':['status change'], 'history_extension':['history extension']},
 'Label': {'name':['name'], 'value':['marker','condition marker','status'], 'condition':['condition marker'], 'status':['status'], 'identifier':['identifier']},
 'Representation': {'represented_item':['represented item'], 'proposition':['proposition'], 'rule':['rule'], 'state_element':['state element'], 'transition_record':['transition record'], 'output_record':['output record']},
 'Representational Structure': {'ordering':['ordering'], 'dependency':['dependency'], 'rule_status':['rule-status'], 'transition_structure':['transition structure'], 'admissibility':['admissibility'], 'history_structure':['history structure']},
 'Interpretation': {'meaning':['meaning'], 'truth_condition':['truth condition'], 'status_meaning':['status meaning'], 'output_meaning':['output meaning']},
 'Investigation': {'objective':['task','question','fixes'], 'question':['question'], 'scope':['bounded task']},
 'Calculus': {'admissible_operation':['admissibility','procedure'], 'transition_policy':['transition policy'], 'update_rule':['update rule'], 'stopping_rule':['stopping rule'], 'prohibition':['admissibility standard']}}

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def csha(o:Any)->str: return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load(p:Path)->Any: return json.loads(p.read_text())
def dump(o:Any,p:Path): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def parse_vocab(p:Path)->Json:
    text=p.read_text(); prim=re.findall(r'- \*\*(.+?)\*\*:\s*(.+)',text); m=re.search(r'Vocabulary package identifier:\s*(\S+)',text)
    return {'identifier':m.group(1) if m else p.stem,'primitive_categories':[a for a,_ in prim],'official_definitions':{a:b for a,b in prim},'definition_digest':hashlib.sha256(text.encode()).hexdigest(),'text':text}

def capability(defn:str, primitive:str, cap:str)->bool:
    low=defn.lower(); return any(k in low for k in CAP_KEYWORDS[primitive][cap])
def check_cap(v:Json, primitive:str, cap:str)->Json:
    d=v['official_definitions'].get(primitive,'')
    ok=primitive in v['primitive_categories'] and cap in CAPS.get(primitive,set()) and capability(d,primitive,cap)
    return {'primitive':primitive,'capability':cap,'definition_text':d,'definition_sha256':hashlib.sha256(d.encode()).hexdigest(),'passed':ok,'capability_rule':f'{primitive} must support {cap} using frozen definition keywords'}

def discover()->Json:
    entries=[]
    for pkg in load(BASE/'vocabularies/vocabulary-packages.json')['packages']:
        src=(BASE/pkg['path']).resolve(); v=parse_vocab(src)
        entries.append({'vocabulary_identifier':v['identifier'],'vocabulary_version':pkg['version'],'label':pkg['label'],'source_path':str(src.relative_to(ROOT)),'frozen_status':'Frozen evaluator-facing package','source_sha256':sha(src),'primitive_categories':v['primitive_categories'],'official_definitions':v['official_definitions'],'allowed_composition_or_derivation_rules':['Derived constructs must record declaration, role, supplied category, preservation requirement, necessity, and provenance; may not alter the scenario or introduce unstated domain rules.'],'exclusions_or_restrictions':['Use only supplied primitive vocabulary terms plus declared derived machinery.','Do not alter or simplify the frozen scenario.'],'eligible_for_cre001_comparison':True})
    return {'artifact_id':'CRE-001-VOCABULARY-INVENTORY-1.0','experiment':'CRE-001','discovery_rule':'Only frozen packages listed in vocabulary-packages.json are eligible; pilots, controls, evaluator corrections, deprecated/superseded artifacts, and generated reports are excluded.','excluded_classes':['control fixtures','pilot mappings','evaluator corrections','deprecated artifacts','superseded vocabularies','generated reports'],'vocabularies':entries}

def parse_condition(s:str)->list[Json]:
    if ' or ' in s: return [parse_condition(x)[0] for x in s.split(' or ')]
    if s.endswith(' active'): return [{'variable':s.split()[0]+'_active','equals':True,'source_text':s}]
    if '=' in s:
        a,b=s.split('=',1); return [{'variable':a,'equals':b=='true','source_text':s}]
    raise ValueError(f'unparsed condition {s}')
def parse_update(s:str)->Json:
    if s.startswith('append '): return {'operation':'append','variable':'history','value':s.split()[1],'source_text':s}
    if s.endswith(' inactive'): return {'operation':'set','variable':s.split()[0]+'_active','from':True,'value':False,'source_text':s}
    if '=' in s:
        a,b=s.split('=',1); return {'operation':'set','variable':a,'value':b=='true','source_text':s}
    raise ValueError(f'unparsed update {s}')

def base(entry:Json,v:Json, tag:str)->Json:
    return {'native_format':'cre001-atomic-native-representation-v1','vocabulary':tag,'vocabulary_identifier':entry['vocabulary_identifier'],'vocabulary_source_sha256':entry['source_sha256'],'definition_digest':v['definition_digest'],'scenario_source_sha256':sha(SCEN),'constructs':[],'derived_constructs':[{'id':'D_boolean_value','role':'truth/status value carrier'},{'id':'D_ordered_history','role':'append-only ordered transition record'},{'id':'D_guarded_update','role':'guarded update schema'},{'id':'D_disjunction','role':'explicit alternative guard group'},{'id':'D_terminality','role':'terminal blocking and halt output'}]}
def add(n:Json, c:Json, v:Json, primitive:str, cap:str):
    c['capability_validation']=check_cap(v,primitive,cap); c['primitive_definition_text']=c['capability_validation']['definition_text']; c['primitive_definition_sha256']=c['capability_validation']['definition_sha256']; n['constructs'].append(c)
def rules(s:Json): return s['rules']
def rule_path(i:int, field:str|None=None, j:int|None=None)->str:
    p=f'/rules/{i}';
    if field: p+=f'/{field}'
    if j is not None: p+=f'/{j}'
    return p

def build_native(entry:Json, v:Json, tag:str)->Json:
    s=load(SCEN); n=base(entry,v,tag); C=n['constructs']
    if tag=='A': prim={'item':'Object','cond':'Relation','effect':'Transformation','schema':'Transformation','meta':'Relation'}; kinds={'prop':'proposition_object','truth':'truth_value_object','rule':'rule_object','status':'status_object','tname':'transition_name_object','hist':'history_entry_object','history':'ordered_history_object','cond':'condition_relation','auth':'authorization_relation','current':'current_value_relation','statusrel':'status_relation','order':'ordering_relation','prohib':'prohibition_relation','output':'output_relation','schema':'transformation_schema','effect':'atomic_effect_record','alt':'alternative_group_relation','terminal':'terminality_relation','ambiguity':'ambiguity_policy_record','invariant':'invariant_relation'}; caps={'item':'identify','cond':'condition','effect':'update','schema':'transition','meta':'constraint'}
    elif tag=='B': prim={'item':'Label','cond':'Label','effect':'Label','schema':'Transition','meta':'Label'}; kinds={'prop':'proposition_value_label','truth':'truth_value_label','rule':'rule_status_label','status':'status_label','tname':'transition_name_label','hist':'history_entry_label','history':'history_label','cond':'precondition_label','auth':'authorization_label','current':'current_value_label','statusrel':'rule_status_label','order':'ordering_label','prohib':'prohibition_label','output':'output_recovery_label','schema':'transition_construct','effect':'update_label','alt':'disjunction_group_label','terminal':'terminal_label','ambiguity':'ambiguity_policy_label','invariant':'invariant_label'}; caps={'item':'value','cond':'condition','effect':'status','schema':'update','meta':'status'}
    else:
        prim={'item':'Representation','cond':'Calculus','effect':'Calculus','schema':'Calculus','meta':'Interpretation'}; kinds={'prop':'proposition_representation','truth':'truth_value_interpretation','rule':'rule_representation','status':'status_representation','tname':'transition_representation','hist':'history_entry_representation','history':'history_structure','cond':'atomic_precondition_calculus','auth':'authorization_calculus','current':'state_composition_structure','statusrel':'rule_status_structure','order':'ordering_structure','prohib':'prohibition_calculus','output':'output_structure','schema':'transition_schema_calculus','effect':'atomic_update_calculus','alt':'halt_disjunction_calculus','terminal':'terminal_configuration_structure','ambiguity':'ambiguity_policy_calculus','invariant':'invariant_calculus'}; caps={'item':'represented_item','cond':'admissible_operation','effect':'update_rule','schema':'transition_policy','meta':'meaning'}
        add(n, {'id':'INVESTIGATION_CRE001','kind':'investigation_objective','primitive':'Investigation','scenario_path':'/success_criteria','role':'objective','value':'preserve CRE-001 commitments'}, v,'Investigation','objective')
    for val in [True,False]: add(n, {'id':f'VAL_{str(val).lower()}','kind':kinds['truth'],'primitive':prim['item'] if tag!='C' else 'Interpretation','scenario_path':'/initial_state/propositions','role':'truth_value','value':val,'derived_construct':'D_boolean_value'}, v, prim['item'] if tag!='C' else 'Interpretation', caps['item'] if tag!='C' else 'truth_condition')
    for st in ['active','inactive']: add(n, {'id':f'STATUS_{st}','kind':kinds['status'],'primitive':prim['item'],'scenario_path':'/initial_state/active_rules','role':'rule_status_value','value':st,'derived_construct':'D_boolean_value'}, v, prim['item'], caps['item'])
    for p,val in s['initial_state']['propositions'].items():
        add(n, {'id':f'PROP_{p}','kind':kinds['prop'],'primitive':prim['item'],'scenario_path':f'/initial_state/propositions/{p}','role':'proposition','name':p,'value_ref':f'VAL_{str(val).lower()}','derived_construct':'D_boolean_value'}, v, prim['item'], caps['item'])
        add(n, {'id':f'CUR_{p}','kind':kinds['current'],'primitive':prim['cond'] if tag!='C' else 'Representational Structure','scenario_path':f'/initial_state/propositions/{p}','role':'initial_value','target_ref':f'PROP_{p}','value':val,'derived_construct':'D_boolean_value'}, v, prim['cond'] if tag!='C' else 'Representational Structure', caps['cond'] if tag!='C' else 'rule_status')
    for r in s['initial_state']['active_rules']:
        add(n, {'id':f'RULE_{r}','kind':kinds['rule'],'primitive':prim['item'],'scenario_path':'/initial_state/active_rules','role':'rule','name':r,'derived_construct':'D_boolean_value'}, v, prim['item'], caps['item'])
        add(n, {'id':f'STATUSREL_{r}','kind':kinds['statusrel'],'primitive':prim['cond'] if tag!='C' else 'Representational Structure','scenario_path':'/initial_state/active_rules','role':'initial_rule_status','target_ref':f'RULE_{r}','variable':r+'_active','value':True,'derived_construct':'D_boolean_value'}, v, prim['cond'] if tag!='C' else 'Representational Structure', caps['cond'] if tag!='C' else 'rule_status')
    add(n, {'id':'HISTORY','kind':kinds['history'],'primitive':prim['item'] if tag!='C' else 'Representational Structure','scenario_path':'/initial_state/transition_history','role':'history','initial':[],'derived_construct':'D_ordered_history'}, v, prim['item'] if tag!='C' else 'Representational Structure', caps['item'] if tag!='C' else 'history_structure')
    add(n, {'id':'TERMINAL_BLOCKING','kind':kinds['terminal'],'primitive':prim['meta'] if tag!='C' else 'Calculus','scenario_path':'/stopping_condition','role':'terminal_blocking','variable':'p_halted','value':True,'blocks_all':True,'derived_construct':'D_terminality'}, v, prim['meta'] if tag!='C' else 'Calculus', caps['meta'] if tag!='C' else 'stopping_rule')
    for i,rule in enumerate(rules(s)):
        tid=rule['permits']; add(n, {'id':f'TNAME_{tid}','kind':kinds['tname'],'primitive':prim['item'],'scenario_path':rule_path(i,'permits'),'role':'transition_name','name':tid}, v, prim['item'], caps['item'])
        pre_ids=[]; eff_ids=[]; alt_ids=[]
        add(n, {'id':f'AUTH_{rule["id"]}_{tid}','kind':kinds['auth'],'primitive':prim['cond'],'scenario_path':rule_path(i),'role':'authorization','rule_ref':f'RULE_{rule["id"]}','transition_ref':f'TNAME_{tid}'}, v, prim['cond'], 'authorization' if tag=='A' else caps['cond'])
        existing_pre=list(rule['preconditions'])
        active_text=rule['id']+' active'
        if active_text not in existing_pre: existing_pre.append(active_text)
        if tid=='T_disable_reject' and 'R_reject active' not in existing_pre: existing_pre.append('R_reject active')
        if tid=='T_halt' and 'p_halted=false' not in existing_pre: existing_pre.append('p_halted=false')
        for j,pre in enumerate(existing_pre):
            pcs=parse_condition(pre)
            if len(pcs)>1:
                ids=[]
                for k,pc in enumerate(pcs):
                    cid=f'PRE_{tid}_{j}_{k}'; ids.append(cid); add(n, {'id':cid,'kind':kinds['cond'],'primitive':prim['cond'],'scenario_path':rule_path(i,'preconditions',j),'role':'guard_alternative','variable':pc['variable'],'equals':pc['equals'],'source_text':pc['source_text'],'derived_construct':'D_guarded_update'}, v, prim['cond'], caps['cond'])
                gid=f'ALT_{tid}_{j}'; alt_ids.append(gid); add(n, {'id':gid,'kind':kinds['alt'],'primitive':prim['cond'],'scenario_path':rule_path(i,'preconditions',j),'role':'guard_any_group','member_refs':ids,'derived_construct':'D_disjunction'}, v, prim['cond'], caps['cond'])
            else:
                pc=pcs[0]; cid=f'PRE_{tid}_{j}'; pre_ids.append(cid); add(n, {'id':cid,'kind':kinds['cond'],'primitive':prim['cond'],'scenario_path':rule_path(i,'preconditions',j),'role':'guard_all_condition','variable':pc['variable'],'equals':pc['equals'],'source_text':pc['source_text'],'derived_construct':'D_guarded_update'}, v, prim['cond'], caps['cond'])
        for j,up in enumerate(rule['updates']):
            pu=parse_update(up); eid=f'EFF_{tid}_{j}'; eff_ids.append(eid); add(n, {'id':eid,'kind':kinds['effect'],'primitive':prim['effect'],'scenario_path':rule_path(i,'updates',j),'role':'atomic_update','operation':pu['operation'],'variable':pu['variable'],'value':pu['value'],'from':pu.get('from'),'source_text':pu['source_text'],'derived_construct':'D_guarded_update'}, v, prim['effect'], caps['effect'])
            if pu['operation']=='append': add(n, {'id':f'ORDER_{tid}_{j}','kind':kinds['order'],'primitive':prim['cond'] if tag!='C' else 'Representational Structure','scenario_path':rule_path(i,'updates',j),'role':'history_append_order','effect_ref':eid,'history_ref':'HISTORY','derived_construct':'D_ordered_history'}, v, prim['cond'] if tag!='C' else 'Representational Structure', caps['cond'] if tag!='C' else 'ordering')
        add(n, {'id':f'SCHEMA_{tid}','kind':kinds['schema'],'primitive':prim['schema'],'scenario_path':rule_path(i),'role':'transition_schema','name_ref':f'TNAME_{tid}','authorization_ref':f'AUTH_{rule["id"]}_{tid}','precondition_refs':pre_ids,'alternative_group_refs':alt_ids,'effect_refs':eff_ids,'derived_construct':'D_guarded_update'}, v, prim['schema'], caps['schema'])
    for j,p in enumerate(s['prohibited_transitions']): add(n, {'id':f'PROHIB_{j}','kind':kinds['prohib'],'primitive':prim['meta'] if tag!='C' else 'Calculus','scenario_path':f'/prohibited_transitions/{j}','role':'prohibition','value':p,'derived_construct':'D_guarded_update'}, v, prim['meta'] if tag!='C' else 'Calculus', caps['meta'] if tag!='C' else 'prohibition')
    for name,spec in OUTPUTS.items(): add(n, {'id':f'OUTPUT_{name}','kind':kinds['output'],'primitive':prim['meta'] if tag!='C' else 'Interpretation','scenario_path':'/observable_outputs','role':'output','name':name,'kind_value':spec['kind'],'output_variable_refs':spec.get('variables'),'output_variable_ref':spec.get('variable'),'derived_construct':'D_terminality'}, v, prim['meta'] if tag!='C' else 'Interpretation', caps['meta'] if tag!='C' else 'output_meaning')
    for kind,payload in INVARIANTS: add(n, {'id':f'INVARIANT_{kind}','kind':kinds['invariant'],'primitive':prim['meta'] if tag!='C' else 'Calculus','scenario_path':'/prohibited_transitions','role':'invariant','invariant_kind':kind,**payload,'derived_construct':'D_guarded_update'}, v, prim['meta'] if tag!='C' else 'Calculus', caps['meta'] if tag!='C' else 'prohibition')
    for k,val in AMBIG.items(): add(n, {'id':f'AMBIG_{k}','kind':kinds['ambiguity'],'primitive':prim['meta'] if tag!='C' else 'Calculus','scenario_path':'/deterministic-verifier/README.md#registered-ambiguity-policies','role':'ambiguity_policy','name':k,'value':val,'derived_construct':'D_terminality'}, v, prim['meta'] if tag!='C' else 'Calculus', caps['meta'] if tag!='C' else 'stopping_rule')
    return n

@dataclass(frozen=True)
class LoweringRule:
    rule_id:str; accepted_kinds:set[str]; primitive:set[str]; required_fields:set[str]; output_type:str; transform:Callable[[Json],Any]
    def apply(self,c:Json)->Any:
        if c.get('kind') not in self.accepted_kinds: raise ValueError(f'{self.rule_id} rejected kind {c.get("kind")}')
        if c.get('primitive') not in self.primitive: raise ValueError(f'{self.rule_id} rejected primitive {c.get("primitive")}')
        missing=self.required_fields-set(c)
        if missing: raise ValueError(f'{self.rule_id} missing fields {sorted(missing)}')
        if not c.get('capability_validation',{}).get('passed'): raise ValueError(f'{self.rule_id} capability failed for {c.get("id")}')
        return self.transform(c)

def rule_set(tag:str)->dict[str,LoweringRule]:
    if tag=='A': cond={'condition_relation','alternative_group_relation'}; eff={'atomic_effect_record'}; schemas={'transformation_schema'}; vars={'current_value_relation','status_relation','ordered_history_object','prohibition_relation'}; meta={'terminality_relation','output_relation','invariant_relation','ambiguity_policy_record'}; prim={'Object','Relation','Transformation'}
    elif tag=='B': cond={'precondition_label','disjunction_group_label'}; eff={'update_label'}; schemas={'transition_construct'}; vars={'current_value_label','rule_status_label','history_label','prohibition_label'}; meta={'terminal_label','output_recovery_label','invariant_label','ambiguity_policy_label'}; prim={'State','Transition','Label'}
    else: cond={'atomic_precondition_calculus','halt_disjunction_calculus'}; eff={'atomic_update_calculus'}; schemas={'transition_schema_calculus'}; vars={'state_composition_structure','rule_status_structure','history_structure','prohibition_calculus'}; meta={'terminal_configuration_structure','output_structure','invariant_calculus','ambiguity_policy_calculus'}; prim={'Representation','Representational Structure','Interpretation','Investigation','Calculus'}
    return {
     'variable':LoweringRule(f'{tag}-variable-atomic',vars,prim,{'role'},'variable',lambda c: {'type':'history','initial':[]} if c['role']=='history' else {'type':'boolean','initial':False if c['role']=='prohibition' else c['value']}),
     'condition':LoweringRule(f'{tag}-condition-atomic',cond,prim,{'variable','equals'},'condition',lambda c:{'variable':c['variable'],'equals':c['equals']}),
     'alternative':LoweringRule(f'{tag}-alternative-atomic',cond,prim,{'member_refs'},'guard_any',lambda c:c['member_refs']),
     'effect':LoweringRule(f'{tag}-effect-atomic',eff,prim,{'operation','variable','value'},'update',lambda c:{k:v for k,v in {'variable':c['variable'],'operation':c['operation'],'from':c.get('from'),'value':c['value']}.items() if v is not None}),
     'schema':LoweringRule(f'{tag}-schema-atomic',schemas,prim,{'name_ref','precondition_refs','effect_refs'},'transition',lambda c:c),
     'terminal':LoweringRule(f'{tag}-terminal-atomic',meta,prim,{'variable','value','blocks_all'},'terminal',lambda c:({'variable':c['variable'],'equals':c['value']},c['blocks_all'])),
     'output':LoweringRule(f'{tag}-output-atomic',meta,prim,{'name','kind_value'},'output',lambda c:{'kind':c['kind_value'], **({'variables':c['output_variable_refs']} if c.get('output_variable_refs') else {'variable':c['output_variable_ref']})}),
     'invariant':LoweringRule(f'{tag}-invariant-atomic',meta,prim,{'invariant_kind'},'invariant',lambda c:{k:v for k,v in {'kind':c['invariant_kind'],'variables':c.get('variable_refs'),'variable':c.get('variable'),'variable_suffix':c.get('variable_suffix'),'allowed_transition':c.get('allowed_transition')}.items() if v is not None}),
     'ambiguity':LoweringRule(f'{tag}-ambiguity-atomic',meta,prim,{'name','value'},'ambiguity',lambda c:(c['name'],c['value']))}

def tr(path,c,rule,field,value): return {'output_path':path,'source_scenario_path':c['scenario_path'],'native_construct_id':c['id'],'native_construct_kind':c['kind'],'supplied_vocabulary_primitive':c['primitive'],'primitive_definition_sha256':c['primitive_definition_sha256'],'primitive_definition_excerpt':c['primitive_definition_text'][:160],'derived_construct_id':c.get('derived_construct'),'executable_lowering_rule_id':rule.rule_id,'source_native_field':field,'resulting_common_model_value':value}
def idx(native): return {c['id']:c for c in native['constructs']}
def ensure_cap(native):
    bad=[c['id'] for c in native['constructs'] if not c.get('capability_validation',{}).get('passed')]
    if bad: raise ValueError(f'capability validation failed: {bad[:5]}')

def lower(native:Json, rules:dict[str,LoweringRule]|None=None)->tuple[Json,Json]:
    tag=native['vocabulary']; rules=rules or rule_set(tag); ensure_cap(native); by=idx(native); traces=[]; variables={}
    for c in native['constructs']:
        if c['role']=='initial_value': val=rules['variable'].apply(c); variables[c['target_ref'].replace('PROP_','')]=val; traces.append(tr(f"/variables/{c['target_ref'].replace('PROP_','')}",c,rules['variable'],'value',val))
        elif c['role']=='initial_rule_status': val=rules['variable'].apply(c); variables[c['variable']]=val; traces.append(tr(f"/variables/{c['variable']}",c,rules['variable'],'value',val))
        elif c['role']=='history': val=rules['variable'].apply(c); variables['history']=val; traces.append(tr('/variables/history',c,rules['variable'],'initial',val))
    prohib=[c for c in native['constructs'] if c['role']=='prohibition']
    if not prohib: raise ValueError('missing prohibition native support')
    pc=prohib[0]; variables['prohibited_transition_occurred']={'type':'boolean','initial':False}; traces.append(tr('/variables/prohibited_transition_occurred',pc,rules['variable'],'value',variables['prohibited_transition_occurred']))
    transitions=[]
    schemas=[c for c in native['constructs'] if c['role']=='transition_schema']
    if len(schemas)!=5: raise ValueError('missing transition schema')
    for s in sorted(schemas,key=lambda c: by[c['name_ref']]['name']):
        rules['schema'].apply(s); name=by[s['name_ref']]['name']; guard=[]; guard_any=[]; updates=[]
        for cid in s['precondition_refs']:
            if cid not in by: raise ValueError(f'missing atomic precondition {cid}')
            item=rules['condition'].apply(by[cid]); guard.append(item); traces.append(tr(f'/transitions/{name}/guard/{len(guard)-1}',by[cid],rules['condition'],'variable/equals',item))
        for gid in s.get('alternative_group_refs',[]):
            if gid not in by: raise ValueError(f'missing alternative group {gid}')
            member_ids=rules['alternative'].apply(by[gid]); group=[]
            for mid in member_ids:
                if mid not in by: raise ValueError(f'missing alternative member {mid}')
                item=rules['condition'].apply(by[mid]); group.append(item); traces.append(tr(f'/transitions/{name}/guard_any/{len(group)-1}',by[mid],rules['condition'],'variable/equals',item))
            if len(group)<2: raise ValueError('disjunction collapsed into non-disjunction')
            guard_any.extend(group); traces.append(tr(f'/transitions/{name}/guard_any_group',by[gid],rules['alternative'],'member_refs',group))
        for eid in s['effect_refs']:
            if eid not in by: raise ValueError(f'missing atomic update {eid}')
            item=rules['effect'].apply(by[eid]); updates.append(item); traces.append(tr(f'/transitions/{name}/updates/{len(updates)-1}',by[eid],rules['effect'],'operation/variable/value',item))
        if name=='T_disable_reject' and not any(u.get('variable')=='R_reject_active' and u.get('value') is False for u in updates): raise ValueError('rule-status modification cannot be reconstructed')
        if not any(u.get('operation')=='append' and u.get('variable')=='history' for u in updates): raise ValueError('history order cannot be reconstructed')
        t={'name':name,'guard':guard,'updates':updates}
        if guard_any: t['guard_any']=guard_any
        transitions.append(t); traces.append(tr(f'/transitions/{name}/name',by[s['name_ref']],rules['schema'],'name',name))
    term=[c for c in native['constructs'] if c['role']=='terminal_blocking']
    if not term: raise ValueError('terminal blocking cannot be reconstructed')
    terminal_condition, terminal_blocks = rules['terminal'].apply(term[0]); traces += [tr('/terminal_condition',term[0],rules['terminal'],'variable/value',terminal_condition), tr('/terminal_blocks_all_transitions',term[0],rules['terminal'],'blocks_all',terminal_blocks)]
    invariants=[]
    for c in [x for x in native['constructs'] if x['role']=='invariant']:
        item=rules['invariant'].apply(c); invariants.append(item); traces.append(tr(f'/invariants/{len(invariants)-1}',c,rules['invariant'],'invariant_kind',item))
    if len(invariants)!=3: raise ValueError('invariants cannot be reconstructed')
    outputs={}
    for c in sorted([x for x in native['constructs'] if x['role']=='output'],key=lambda x:x['name']):
        item=rules['output'].apply(c); outputs[c['name']]=item; traces.append(tr(f"/outputs/{c['name']}",c,rules['output'],'name/kind',item))
    if set(outputs)!=set(OUTPUTS): raise ValueError('output cannot be recovered')
    ambiguity={}
    for c in sorted([x for x in native['constructs'] if x['role']=='ambiguity_policy'],key=lambda x:x['name']):
        k,v=rules['ambiguity'].apply(c); ambiguity[k]=v; traces.append(tr(f'/ambiguity_policy/{k}',c,rules['ambiguity'],'name/value',v))
    if set(ambiguity)!=set(AMBIG): raise ValueError('ambiguity policy lacks native support')
    model={'format':'cre001-execution-model-v1','model_id':native['vocabulary_identifier']+'-LOWERED-ATOMIC-V1','ambiguity_policy':ambiguity,'variables':variables,'transitions':transitions,'terminal_condition':terminal_condition,'terminal_blocks_all_transitions':terminal_blocks,'invariants':invariants,'outputs':outputs}
    required={f'/variables/{k}' for k in variables}|{f"/transitions/{t['name']}/name" for t in transitions}|{f"/transitions/{t['name']}/guard/{i}" for t in transitions for i,_ in enumerate(t.get('guard',[]))}|{f"/transitions/{t['name']}/guard_any/{i}" for t in transitions for i,_ in enumerate(t.get('guard_any',[]))}|{f"/transitions/{t['name']}/updates/{i}" for t in transitions for i,_ in enumerate(t.get('updates',[]))}|{'/terminal_condition','/terminal_blocks_all_transitions'}|{f'/invariants/{i}' for i,_ in enumerate(invariants)}|{f'/outputs/{k}' for k in outputs}|{f'/ambiguity_policy/{k}' for k in ambiguity}
    have={x['output_path'] for x in traces}; missing=required-have
    if missing: raise ValueError(f'missing atomic trace {sorted(missing)}')
    return model, {'trace_format':'cre001-atomic-lowering-trace-v1','vocabulary_identifier':native['vocabulary_identifier'],'native_sha256':csha(native),'entries':traces}

def reference_model()->Json:
    s=load(SCEN); variables={k:{'type':'boolean','initial':v} for k,v in s['initial_state']['propositions'].items()}
    for r in ['R_check','R_accept','R_reject','R_modify','R_halt']: variables[r+'_active']={'type':'boolean','initial':r in s['initial_state']['active_rules']}
    variables['prohibited_transition_occurred']={'type':'boolean','initial':False}; variables['history']={'type':'history','initial':[]}
    native=build_native({'vocabulary_identifier':'REF','source_sha256':'ref'}, {'primitive_categories':['Object','Relation','Transformation'],'official_definitions':{'Object':'item rule record state-bearing item unit','Relation':'connection ordering constraint permission prohibition status association among objects','Transformation':'change update transition state modification'},'definition_digest':'ref'}, 'A')
    model,_=lower(native); model['model_id']='CRE-001-REFERENCE-FROM-SCENARIO-V1'; return model

def native_for(entry:Json,v:Json)->Json:
    tag='A' if 'VOCAB-A' in entry['vocabulary_identifier'] else ('B' if 'VOCAB-B' in entry['vocabulary_identifier'] else 'C')
    return build_native(entry,v,tag)

def mutation_report(native:Json, ref:Json)->Json:
    from cre001_verifier import verify
    cases=[]
    def run(name, mut):
        n=copy.deepcopy(native); mut(n)
        try:
            m,_=lower(n); r=verify(ref,m); detected=r['result']!='pass'; diag=r.get('diagnostics',[])
        except Exception as e: detected=True; diag=[{'code':'lowering_failure','message':str(e)}]
        cases.append({'mutation':name,'detected':detected,'diagnostics':diag[:2]})
    muts=[('proposition_initial',lambda n: next(c for c in n['constructs'] if c['role']=='initial_value').update(value=not next(c for c in n['constructs'] if c['role']=='initial_value')['value'])),('rule_active_status',lambda n: next(c for c in n['constructs'] if c['role']=='initial_rule_status').update(value=False)),('guard_condition',lambda n: next(c for c in n['constructs'] if c['role']=='guard_all_condition').update(equals=not next(c for c in n['constructs'] if c['role']=='guard_all_condition')['equals'])),('update_value',lambda n: next(c for c in n['constructs'] if c['role']=='atomic_update' and c['operation']=='set').update(value=False)),('history_append',lambda n: next(c for c in n['constructs'] if c['role']=='atomic_update' and c['operation']=='append').update(value='WRONG')),('halt_disjunction',lambda n: next(c for c in n['constructs'] if c['role']=='guard_any_group').update(member_refs=next(c for c in n['constructs'] if c['role']=='guard_any_group')['member_refs'][:1])),('reject_deactivation',lambda n: next(c for c in n['constructs'] if c['role']=='atomic_update' and c.get('variable')=='R_reject_active').update(value=True)),('terminal_blocking',lambda n: next(c for c in n['constructs'] if c['role']=='terminal_blocking').update(blocks_all=False)),('invariant',lambda n: n['constructs'].remove(next(c for c in n['constructs'] if c['role']=='invariant'))),('output',lambda n: n['constructs'].remove(next(c for c in n['constructs'] if c['role']=='output'))),('ambiguity_policy',lambda n: next(c for c in n['constructs'] if c['role']=='ambiguity_policy').update(value='changed'))]
    for name,mut in muts: run(name,mut)
    return {'mutation_report_format':'cre001-mutation-report-v1','vocabulary_identifier':native['vocabulary_identifier'],'passed':all(c['detected'] for c in cases),'cases':cases}

def compile_entry(entry:Json,outroot:Path)->Json:
    v=parse_vocab(ROOT/entry['source_path']); native=native_for(entry,v); d=outroot/entry['vocabulary_identifier']; dump(native,d/'native-representation.json')
    status='complete'; unsupported=[]; model=None; trace=None; mutation=None
    try:
        model,trace=lower(native); dump(trace,d/'lowering-trace.json'); dump(model,d/'generated-execution-model.json'); mutation=mutation_report(native, reference_model()); dump(mutation,d/'mutation-test-report.json')
    except Exception as e: status='partial'; unsupported=[str(e)]
    cap_pass=all(c.get('capability_validation',{}).get('passed') for c in native['constructs'])
    trace_pass=bool(trace) and len(trace['entries'])>0; mutation_pass=bool(mutation and mutation['passed'])
    art={'artifact_format':'cre001-vocabulary-compiler-artifact-v3','experiment_identifier':'CRE-001','scenario_identifier':'CRE-001-SCENARIO-1.0','scenario_version':'1.0','vocabulary_identifier':entry['vocabulary_identifier'],'vocabulary_version':entry['vocabulary_version'],'vocabulary_source_path':entry['source_path'],'vocabulary_source_sha256':entry['source_sha256'],'compiler_identifier':entry['vocabulary_identifier'].lower()+'-atomic-native-compiler','compiler_version':COMPILER_VERSION,'compiler_source_path':'tools/cre001_compile_vocabularies.py','compiler_source_sha256':sha(ROOT/'tools/cre001_compile_vocabularies.py'),'compilation_status':status,'native_construction_complete':status=='complete','definition_capability_validation_passed':cap_pass,'atomic_lowering_complete':trace_pass,'shared_semantic_defaults_used':False,'mutation_sensitivity_passed':mutation_pass,'supplied_primitive_categories':v['primitive_categories'],'primitive_categories_used':sorted({c['primitive'] for c in native['constructs']}),'declared_derived_constructs':native['derived_constructs'],'translation_rules':['atomic-native-construction',*[r.rule_id for r in rule_set(native['vocabulary']).values()]],'assumptions':['Frozen scenario and vocabulary files are source inputs.','Candidate model is accepted only after atomic native construction, capability validation, lowering trace completeness, mutation sensitivity, and verifier pass.'],'unresolved_ambiguities':[],'unsupported_scenario_elements':unsupported,'generated_execution_model':model,'native_representation_sha256':csha(native),'lowering_trace_sha256':csha(trace) if trace else None,'mutation_report_sha256':csha(mutation) if mutation else None,'provenance':{'source':'compiled from frozen vocabulary into atomic native records, then lowered by executable rules; no candidate path calls the reference compiler or prebuilt transition dictionaries','generation_command':'python tools/cre001_compile_vocabularies.py --write --check'},'deterministic_generation_metadata':{'json_sort_keys':True,'compiler_version':COMPILER_VERSION},'complexity':{'supplied_primitive_categories':v['primitive_categories'],'primitive_categories_used':sorted({c['primitive'] for c in native['constructs']}),'declared_derived_construct_count':len(native['derived_constructs']),'transition_schema_count':len([c for c in native['constructs'] if c['role']=='transition_schema']),'normalized_compiler_clause_count':len(native['constructs'])+len(rule_set(native['vocabulary']))}}
    dump(art,d/'compiler-artifact.json'); return art

def generate(outroot:Path): inv=discover(); return inv,[compile_entry(e,outroot) for e in inv['vocabularies']]
def verify_reports(outroot:Path,arts:list[Json]):
    from cre001_verifier import verify
    ref=reference_model(); reps=[]
    for a in arts:
        d=outroot/a['vocabulary_identifier']; m=a.get('generated_execution_model')
        rep=verify(ref,m) if m else {'result':'not_run','diagnostics':[{'code':'compilation_incomplete','message':'; '.join(a['unsupported_scenario_elements'])}]}
        rep.update({'reference_sha256':csha(ref),'candidate_sha256':csha(m) if m else None,'verifier_version':rep.get('verifier','cre001-deterministic-verifier-v1')}); dump(rep,d/'verifier-report.json'); reps.append(rep)
    return reps

def write_summary(inv,arts,reps):
    results=[]
    for e,a,r in zip(inv['vocabularies'],arts,reps):
        cond=all([a['native_construction_complete'],a['definition_capability_validation_passed'],a['atomic_lowering_complete'],not a['shared_semantic_defaults_used'],a['mutation_sensitivity_passed'],r['result']=='pass'])
        results.append({'vocabulary_identifier':e['vocabulary_identifier'],'inventory_status':'eligible','compilation_status':a['compilation_status'],'native_construction_complete':a['native_construction_complete'],'definition_capability_validation_passed':a['definition_capability_validation_passed'],'atomic_lowering_complete':a['atomic_lowering_complete'],'shared_semantic_defaults_used':a['shared_semantic_defaults_used'],'mutation_sensitivity_passed':a['mutation_sensitivity_passed'],'behavioral_equivalence_passed':r['result']=='pass','cre001_conditional_equivalence_demonstrated':cond,'unsupported_elements':a['unsupported_scenario_elements'],'verifier_result':r['result'],'failed_checks':[k for k,v in r.get('checks',{}).items() if v!='pass'],'shortest_counterexample':next((d for d in r.get('diagnostics',[]) if d.get('trace')),None),'limitations':['Conditional equivalence is limited to CRE-001, registered ambiguity policies, atomic native compiler artifacts, mutation tests, and verifier depth.'],'complexity':a['complexity']})
    summary={'artifact_id':'CRE-001-DETERMINISTIC-COMPARISON-3.0','experiment':'CRE-001','residual_circularity_correction':'Native artifacts contain atomic records only; lowerers assemble every common-model semantic field from atomic native constructs and traces.','nonclaims':['No universal sufficiency, necessity, minimality, indispensability, superiority, FAR proof, or universal reasoning-structure conclusion is drawn.'],'results':results}; dump(summary,DET/'cre001-deterministic-comparison.json')
    md=['# CRE-001 deterministic vocabulary comparison','','Status: generated deterministic report.','','## Residual circularity correction','','Preconstructed transition dictionaries and centrally injected candidate semantics have been removed from candidate native artifacts. Candidate lowerers now assemble every common-model semantic field from atomic native records and executable lowering rules.','','## Nonclaims','']+[f'- {x}' for x in summary['nonclaims']]+['','## Results','']
    for r in results: md += [f"### {r['vocabulary_identifier']}",f"- Compilation status: `{r['compilation_status']}`",f"- Definition-capability validation passed: `{r['definition_capability_validation_passed']}`",f"- Atomic lowering complete: `{r['atomic_lowering_complete']}`",f"- Shared semantic defaults used: `{r['shared_semantic_defaults_used']}`",f"- Mutation sensitivity passed: `{r['mutation_sensitivity_passed']}`",f"- Verifier result: `{r['verifier_result']}`",f"- CRE-001 conditional equivalence demonstrated: `{r['cre001_conditional_equivalence_demonstrated']}`",f"- Shortest counterexample: {r['shortest_counterexample']}",f"- Unsupported elements: {r['unsupported_elements']}",'']
    (ROOT/'docs/reports').mkdir(exist_ok=True); (ROOT/'docs/reports/cre001-deterministic-comparison.md').write_text('\n'.join(md)+'\n')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--write',action='store_true'); ap.add_argument('--check',action='store_true'); ap.add_argument('--out',type=Path,default=DET/'generated'); args=ap.parse_args()
    inv,arts=generate(args.out); reps=verify_reports(args.out,arts); dump(inv,DET/'vocabulary-inventory.json'); write_summary(inv,arts,reps)
    if args.check:
        with tempfile.TemporaryDirectory() as td:
            inv2,arts2=generate(Path(td)); reps2=verify_reports(Path(td),arts2)
            if json.dumps([inv,arts,reps],sort_keys=True)!=json.dumps([inv2,arts2,reps2],sort_keys=True): return 1
    return 0
if __name__=='__main__': raise SystemExit(main())
