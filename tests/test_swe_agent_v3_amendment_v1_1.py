from __future__ import annotations
import importlib.util,json,sys,tempfile,unittest
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DIR=ROOT/'research/external-validation/swe-agent-v3';P=DIR/'verify_amendment_v1_1_rooted.py'
s=importlib.util.spec_from_file_location('v',P);assert s and s.loader;m=importlib.util.module_from_spec(s);sys.path.insert(0,str(DIR));sys.modules[s.name]=m;s.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_canonical(self):
  a=m.validate();self.assertEqual(a['authority']['outcome_exposure_status'],'none');self.assertFalse(a['authority']['execution_authorized'])
 def test_taxonomy(self):
  c=m.validate()['replacement_contract'];x=c['terminal_reason_classes'];f=[i for v in x.values() for i in v]
  self.assertEqual(len(f),len(set(f)));self.assertFalse(c['operator_discretion_permitted']);self.assertIn('provider_timeout_or_failure_after_request_acceptance',x['unresolved_nonreplaceable']);self.assertNotIn('provider_timeout_or_failure_after_request_acceptance',x['infrastructure_invalid_replacement_eligible'])
 def test_unlisted_preserved(self):
  r=m.validate()['replacement_contract']['unlisted_terminal_reason_rule'];self.assertIn('invalid_nonreplaceable',r);self.assertIn('never retroactively reclassify',r)
 def test_exact_boundaries(self):
  self.assertEqual(m.probability(2,3)-m.probability(1,3),Fraction(1,3));self.assertEqual(m.classify(Fraction(1,10),Fraction(1,100),Fraction(1,10)),'bounded_positive');self.assertEqual(m.classify(Fraction(0),Fraction(-1,100),Fraction(999,10000)),'no_practical_advantage');self.assertEqual(m.classify(Fraction(-1,100),Fraction(-1,50),Fraction(-1,1000)),'bounded_harm')
 def test_type7(self):
  v=[Fraction(0),Fraction(1,3),Fraction(2,3),Fraction(1)];self.assertEqual(m.type7(v,Fraction(1,40)),Fraction(1,40));self.assertEqual(m.type7(v,Fraction(39,40)),Fraction(39,40))
 def test_mutation_fails(self):
  src=DIR/'failure-arithmetic-amendment-v1.1.json';d=json.loads(src.read_text());d['replacement_contract']['terminal_reason_classes']['infrastructure_invalid_replacement_eligible'].append('provider_timeot_or_failure_after_request_acceptance')
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/src.name;p.write_text(json.dumps(d,indent=2)+'\n')
   with self.assertRaises(m.AmendmentError):m.validate(amend=p)
 def test_rooted_snapshots_are_history_independent(self):
  self.assertEqual(m._snapshot(m.legacy.PREREG_REL)[1],m.legacy.PREREG_BLOB);self.assertEqual(m._snapshot(m.legacy.PLAN_REL)[1],m.legacy.PLAN_BLOB)
if __name__=='__main__':unittest.main()
