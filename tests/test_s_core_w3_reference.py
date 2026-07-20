from __future__ import annotations
import copy, json, unittest
from pathlib import Path
from s_core_w3_reference import W3Error, canonical_json, component_view, construct_witness, cross_axis_coherent, recover_target, semantic_agreement, structural_digest, validate_package, validate_source, verify_witness
ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'theory/evaluation/s-core-w3-reference-fixtures.json'
def load_source(): return json.loads(FIXTURE.read_text(encoding='utf-8'))['source']
def rename_source(source,mapping):
    v=copy.deepcopy(source); r=lambda x:mapping.get(str(x),str(x))
    for x in v['carriers']: x['id']=r(x['id'])
    for a in v['axes'].values():
        a['members']=[r(x) for x in a['members']]
        for x in a['relations']: x['id']=r(x['id']); x['args']=[r(y) for y in x['args']]
        for x in a['attributes']: x['id']=r(x['id']); x['owner']=r(x['owner'])
    d=v['dynamics']
    for x in d['rules']: x['id']=r(x['id'])
    for x in d['rule_versions']: x['id']=r(x['id']); x['rule']=r(x['rule'])
    for x in d['states']: x['id']=r(x['id']); x['active_rule_versions']=[r(y) for y in x['active_rule_versions']]; x['commitments']={r(k):z for k,z in x['commitments'].items()}
    for x in d['transitions']:
        x['id']=r(x['id']); x['from']=r(x['from']); x['to']=r(x['to'])
        if x.get('rule_version') is not None: x['rule_version']=r(x['rule_version'])
    h=d['history']
    for x in h['events']:
        x['id']=r(x['id']); x['state']=r(x['state'])
        if x.get('transition') is not None: x['transition']=r(x['transition'])
    for k in ('order','causal','dependency_ancestry'): h[k]=[[r(a),r(b)] for a,b in h[k]]
    for x in h['provenance']: x['event']=r(x['event'])
    for x in h['revisions']: x['event']=r(x['event']); x['before_state']=r(x['before_state']); x['after_state']=r(x['after_state']); x['subject']=r(x['subject'])
    for x in h['modifications']: x['event']=r(x['event']); x['before_state']=r(x['before_state']); x['after_state']=r(x['after_state']); x['deactivates']=[r(y) for y in x['deactivates']]; x['activates']=[r(y) for y in x['activates']]
    for x in h['path_conditions']: x['path']=[r(y) for y in x['path']]
    q=v['decomposition']
    for x in q['components']: x['id']=r(x['id']); x['members']=[r(y) for y in x['members']]
    for x in q['interfaces']: x['id']=r(x['id']); x['members']=[r(y) for y in x['members']]; x['components']=[r(y) for y in x['components']]
    for x in q['cross_component_relations']: x['id']=r(x['id']); x['args']=[r(y) for y in x['args']]
    return v
def translate(v,m):
    if isinstance(v,str): return m.get(v,v)
    if isinstance(v,list): return [translate(x,m) for x in v]
    if isinstance(v,dict): return {k:translate(x,m) for k,x in v.items()}
    return v
def norm(v):
    v=copy.deepcopy(v); v['carriers'].sort(key=canonical_json)
    for x in v['axes'].values(): x['members'].sort(); x['relations'].sort(key=canonical_json); x['attributes'].sort(key=canonical_json)
    for x in v['dynamics']['states']: x['commitments'].sort(key=canonical_json); x['resources'].sort(key=canonical_json); x['active_rule_versions'].sort()
    for x in v['dynamics']['transitions']:
        for k in ('preconditions','resource_conditions','action_dependencies','observation_dependencies'): x[k].sort()
    for x in v['dynamics']['history']['modifications']: x['deactivates'].sort(); x['activates'].sort()
    for k in ('rules','rule_versions','states','transitions','transition_statuses'): v['dynamics'][k].sort(key=canonical_json)
    for k in v['dynamics']['history']: v['dynamics']['history'][k].sort(key=canonical_json)
    for k in v['semantics']: v['semantics'][k].sort(key=canonical_json)
    for k in v['decomposition']: v['decomposition'][k].sort(key=canonical_json)
    v['provenance'].sort(key=canonical_json); return v
class W3ReferenceTests(unittest.TestCase):
    def setUp(self): self.s=load_source(); self.p=construct_witness(self.s)
    def test_baseline_witness(self): self.assertTrue(verify_witness(self.s,self.p))
    def test_recovery_is_target_only(self):
        a=recover_target(self.p['A'],self.p['W']['D'],self.p['W']['kappa']); q=copy.deepcopy(self.p); q['W']['E']={}; q['W']['M']={}; self.assertEqual(a,recover_target(q['A'],q['W']['D'],q['W']['kappa'])); self.assertNotIn('source_key',canonical_json(self.p['A']))
    def test_missing_direct_relation_is_rejected(self):
        q=copy.deepcopy(self.p); z=q['W']['E']['occ:p4:support']; q['A']['R']['occurrence_role']=[x for x in q['A']['R']['occurrence_role'] if x[0]!=z]; self.assertFalse(verify_witness(self.s,q))
    def test_undeclared_occurrence_is_rejected(self): q=copy.deepcopy(self.p); q['A']['R']['in_axis'].append(['unknown:occurrence','axis:P4']); self.assertFalse(verify_witness(self.s,q))
    def test_semantic_mutation_is_rejected(self):
        q=copy.deepcopy(self.p); z=q['W']['E']['commitment:c1']; next(x for x in q['A']['I'] if x['subject']==z)['denotation']=q['W']['M']['values'][canonical_json('the supporting observation')]; self.assertFalse(semantic_agreement(self.s,q)); self.assertFalse(verify_witness(self.s,q))
    def test_shared_image_split_is_rejected(self): q=copy.deepcopy(self.p); q['W']['E']['commitment:c1']=q['W']['E']['commitment:c2']; self.assertFalse(cross_axis_coherent(self.s,q)); self.assertRaises(W3Error,validate_package,q)
    def test_source_sort_conflict_is_rejected(self): q=copy.deepcopy(self.s); next(x for x in q['carriers'] if x['id']=='rule:r1')['sort']='ground'; self.assertRaises(W3Error,validate_source,q)
    def test_machinery_cycle_is_rejected(self): q=copy.deepcopy(self.p); q['W']['kappa']['edges'].append(['schema:FARA-WITNESS-1.0','algorithm:validate-source']); self.assertRaises(W3Error,validate_package,q)
    def test_incomplete_machinery_is_rejected(self): q=copy.deepcopy(self.p); del q['W']['kappa']['field_producers']['A.H']; self.assertRaises(W3Error,validate_package,q)
    def test_interface_loss_is_rejected(self): q=copy.deepcopy(self.p); a=q['W']['E']['interface:commitment']; b=q['W']['E']['commitment:c1']; q['A']['Res']['interface_members']=[x for x in q['A']['Res']['interface_members'] if x!=[a,b]]; self.assertFalse(verify_witness(self.s,q))
    def test_hidden_external_dependency_is_rejected(self): q=copy.deepcopy(self.p); q['W']['kappa']['external_dependencies']=['source-oracle']; self.assertRaises(W3Error,validate_package,q)
    def test_display_labels_are_not_structural(self):
        q=copy.deepcopy(self.s)
        for x in q['carriers']: x['display_label']='label::'+x['id']
        p=construct_witness(q); self.assertEqual(structural_digest(self.p),structural_digest(p)); self.assertTrue(verify_witness(q,p))
    def test_source_isomorphism_equivariance(self):
        m={x:f'renamed::{i}' for i,x in enumerate(sorted(self.p['W']['E']),1)}; s=rename_source(self.s,m); p=construct_witness(s); a=recover_target(self.p['A'],self.p['W']['D'],self.p['W']['kappa']); b=recover_target(p['A'],p['W']['D'],p['W']['kappa']); t={self.p['W']['E'][x]:p['W']['E'][y] for x,y in m.items()}; self.assertEqual(norm(translate(a,t)),norm(b)); self.assertTrue(verify_witness(s,p))
    def test_component_view_retains_interface_and_cross_relation(self): a=recover_target(self.p['A'],self.p['W']['D'],self.p['W']['kappa']); v=component_view(a,self.p['W']['E']['component:analysis']); self.assertIn(self.p['W']['E']['commitment:c1'],v['allowed']); self.assertEqual(len(v['cross_component_relations']),1)
    def test_recovery_descriptor_cannot_be_replaced(self): q=copy.deepcopy(self.p); q['W']['D']['algorithm']='case_specific_decoder'; self.assertRaises(W3Error,validate_package,q)
if __name__=='__main__': unittest.main()
