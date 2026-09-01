from __future__ import annotations
import copy,json,unittest
from pathlib import Path
from mechanization.far_mechanization.contract_v21 import SCHEMA_PATH,contract_sha256,validate_contract
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]; FIX=ROOT/'conformance/far-ir-2.1'
def load(name='valid-frontier.json'):return json.loads((FIX/name).read_text())
def codes(d):return {x.code for x in validate_contract(d).diagnostics}
def rehash(d):d['freeze']['contract_sha256']=contract_sha256(d['contract'])
class W5Tests(unittest.TestCase):
 def test_additive_version_preserves_v20(self):
  s=json.loads(SCHEMA_PATH.read_text());Draft202012Validator.check_schema(s)
  self.assertEqual(s['properties']['format_version']['const'],'far-ir/2.1')
  self.assertEqual(json.loads((ROOT/'schemas/far-contract-v2.schema.json').read_text())['properties']['format_version']['const'],'far-ir/2.0')
 def test_frontier_randomized_and_zero_boundary_controls(self):
  self.assertTrue(validate_contract(load()).success)
  self.assertTrue(validate_contract(load('valid-zero-boundary.json')).success)
 def test_random_probability_mutation(self):
  d=load();d['report']['evidence']['candidates'][0]['decoder_table'][0]['distribution'][0]['probability']='1/3'
  self.assertIn('DECODER_NOT_PROBABILITY',codes(d))
 def test_reference_and_aggregation_are_operational(self):
  d=load();d['contract']['approximation']['reference']['weights'][0]['weight']='3/4';rehash(d)
  self.assertIn('REFERENCE_NOT_PROBABILITY',codes(d))
  d=load();d['contract']['approximation']['aggregation']='maximum';rehash(d)
  # Candidate "dominated" has one case loss 1: expected-feasible, maximum-infeasible.
  self.assertIn('FEASIBLE_SET_MISMATCH',codes(d))
 def test_metric_axioms_and_loss_link(self):
  d=load();d['contract']['approximation']['metric']['entries'][1]['distance']='0';rehash(d)
  c=codes(d);self.assertIn('METRIC_SEPARATION_FAILURE',c);self.assertIn('LOSS_METRIC_MISMATCH',c)
 def test_tolerance_is_not_implicit(self):
  d=load();d['contract']['approximation']['tolerance']='1/3';rehash(d)
  self.assertIn('FEASIBLE_SET_MISMATCH',codes(d))
 def test_pareto_is_not_least(self):
  d=load();d['report']['evidence']['claimed_least_elements']=['exact']
  self.assertIn('LEAST_SET_MISMATCH',codes(d))
  d=load();d['report']['evidence']['claimed_pareto_minimal']=['exact']
  self.assertIn('PARETO_SET_MISMATCH',codes(d))
 def test_cost_is_multidimensional_partial_order(self):
  d=load();d['report']['evidence']['candidates'][0]['costs'][0]['dimension_id']='evaluation'
  self.assertIn('COST_COVERAGE_MISMATCH',codes(d))
 def test_false_exact_recovery_rejected(self):
  d=load();d['report']['evidence']['exact_recovery_claims'].append('randomized')
  self.assertIn('EXACT_RECOVERY_SET_MISMATCH',codes(d))
 def test_freeze_provenance_binding(self):
  d=load();d['contract']['frame']['description']='mutation'
  self.assertIn('FREEZE_HASH_MISMATCH',codes(d))
if __name__=='__main__':unittest.main()
