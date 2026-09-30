from __future__ import annotations
import copy,json,tempfile,unittest
from pathlib import Path
from tools import reconcile_research_corpus as corpus

class ResearchCorpusTests(unittest.TestCase):
 def setUp(self): self.data=corpus.load(corpus.CORPUS)
 def test_real_available_corpus_is_complete_and_generated(self):
  self.assertEqual(corpus.validate(self.data),[]);r=corpus.derive(self.data)
  self.assertEqual((corpus.ROOT/corpus.OUTPUT).read_bytes(),corpus.canonical(r));self.assertEqual((corpus.ROOT/corpus.STATUS).read_text(),corpus.markdown(r))
  self.assertEqual(r['untrusted_lead_count'],2061);self.assertGreaterEqual(len(r['inventory']),20);self.assertEqual(len(r['normalized_findings']),18)
  self.assertTrue(any(s['id']=='SRC-SATURATION-OPEN-PR' and s['active'] for s in r['sources']))
 def test_omitted_material_input_fails_non_circular_inventory(self):
  bad=copy.deepcopy(self.data);bad['sources']=[s for s in bad['sources'] if s.get('path')!='docs/audits/far-core-epistemic-calibration-v1.0.md']
  self.assertIn('unclassified material input: docs/audits/far-core-epistemic-calibration-v1.0.md',corpus.validate(bad))
 def test_withdrawal_invalidates_downstream_conclusion(self):
  bad=copy.deepcopy(self.data)
  for source in bad['sources']:
   if any('MEC-CONTRACT' in o['mechanism_ids'] for o in source['observations']): source['availability']='withdrawn';source['evidence_usable']=False
  r=corpus.derive(bad);row=next(c for c in r['conclusions'] if c['id']=='CON-STABILITY')
  self.assertEqual(row['epistemic_class'],'UNRESOLVED');self.assertIn('MEC-CONTRACT',row['missing_mechanisms'])
 def test_correction_or_contradiction_invalidates_support(self):
  bad=copy.deepcopy(self.data);source=next(s for s in bad['sources'] if any(o['claim_key']=='FND-CONTRACT' for o in s['observations']));obs=next(o for o in source['observations'] if o['claim_key']=='FND-CONTRACT');obs['relation']='CONTRADICTS'
  r=corpus.derive(bad);row=next(c for c in r['conclusions'] if c['id']=='CON-STABILITY');self.assertIn('MEC-CONTRACT',row['contradicted_mechanisms']);self.assertEqual(row['epistemic_class'],'UNRESOLVED')
 def test_duplicate_mechanisms_and_cycles_fail(self):
  bad=copy.deepcopy(self.data);dup=copy.deepcopy(bad['mechanism_catalog'][0]);dup['id']='MEC-DUPLICATE';bad['mechanism_catalog'].append(dup)
  self.assertTrue(any('duplicate mechanism' in e for e in corpus.validate(bad)))
  cyc=copy.deepcopy(self.data);cyc['conclusion_rules'][0]['depends_on_conclusions']=[cyc['conclusion_rules'][0]['id']]
  self.assertTrue(any('circular support' in e for e in corpus.validate(cyc)))
 def test_open_world_nonadjacency_never_means_independence(self):
  self.assertTrue(any('nonadjacency' in n.lower() or 'absent graph edges' in n.lower() for n in self.data['nonclaims']))
  bad=copy.deepcopy(self.data);bad['conclusion_rules'][0]['depends_on_conclusions']=['CON-ABSENT']
  self.assertTrue(any('missing dependency' in e for e in corpus.validate(bad)))
 def test_external_ingestion_routes_receipt_into_living_reconciliation(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);incoming=root/'input';incoming.write_bytes(b'#!/bin/sh\nexit 99\n');corpus.freeze_external(incoming,'scheduled_task',root)
   receipts=list((root/'research/corpus/external').glob('*.json'));self.assertEqual(len(receipts),1);receipt=json.loads(receipts[0].read_text());self.assertFalse(receipt['primary_evidence_verified']);self.assertFalse(receipt['executable'])
   living=json.loads((root/corpus.LIVING_RECONCILIATION).read_text());self.assertEqual(living['candidate_count'],1);self.assertFalse(living['promotion_authority'])
 def test_automatic_living_loop_reconciles_candidate_changes(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);d=root/'research/living/inbox/candidates';d.mkdir(parents=True);(d/'FAR-LIT-TEST.json').write_text(json.dumps({'id':'FAR-LIT-TEST','source_key':'doi:test'}))
   first=corpus.write_living(root);(d/'FAR-LIT-SECOND.json').write_text(json.dumps({'id':'FAR-LIT-SECOND','source_key':'doi:second'}));second=corpus.write_living(root)
   self.assertEqual(first['candidate_count'],1);self.assertEqual(second['candidate_count'],2);self.assertNotEqual(first['candidate_set_sha256'],second['candidate_set_sha256'])
 def test_conclusion_order_does_not_change_dependency_synthesis(self):
  expected=corpus.derive(self.data)['conclusions'];reordered=copy.deepcopy(self.data);reordered['conclusion_rules'].reverse();actual={c['id']:c for c in corpus.derive(reordered)['conclusions']}
  for row in expected:self.assertEqual(row['epistemic_class'],actual[row['id']]['epistemic_class'])
 def test_unproved_architecture_gap_is_rejected(self):
  bad=copy.deepcopy(self.data);bad['mechanism_catalog'][0]['architecture_class']='genuine_architecture_gap'
  self.assertTrue(any('unproved genuine architecture gap' in e for e in corpus.validate(bad)))
 def test_stale_output_detected_by_dependency_hash(self):
  r=corpus.derive(self.data);changed=copy.deepcopy(self.data);next(o for s in changed['sources'] for o in s['observations'] if o['claim_key']=='FND-CONTRACT')['statement']+=' corrected'
  r2=corpus.derive(changed);self.assertNotEqual(r['corpus_sha256'],r2['corpus_sha256']);self.assertNotEqual(next(c for c in r['conclusions'] if c['id']=='CON-STABILITY')['dependency_sha256'],next(c for c in r2['conclusions'] if c['id']=='CON-STABILITY')['dependency_sha256'])

if __name__=='__main__':unittest.main()
