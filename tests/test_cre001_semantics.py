from __future__ import annotations
import re, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CRE001SemanticRegressionTests(unittest.TestCase):
    def test_semantics_are_prospective_not_retrospective(self):
        formal=(ROOT/'theory/evaluation/comparative-representation/experiments/CRE-001/semantics/formal-semantics.md').read_text(encoding='utf-8')
        generated=(ROOT/'docs/reports/project-status-generated.md').read_text(encoding='utf-8')
        self.assertIn('formalized after completion of deterministic CRE-001',formal)
        self.assertIn('frozen for future experiments beginning with CRE-002',formal)
        self.assertIn('not independent evidence supporting CRE-001',formal)
        self.assertIn('cannot be used as retrospective validation of CRE-001',formal)
        self.assertIn('CRE-001: deterministic comparison complete at its registered retrospective scope under compiler-authored declared interpretations',generated)
        self.assertNotIn('Established at CRE-001 vocabulary-semantics scope',generated)
        self.assertNotRegex(generated,'CRE-001.*formal vocabulary licensing.*established')
    def test_frozen_semantic_specification_is_consistent(self):
        cp=subprocess.run([sys.executable,'tools/check_cre001_semantics.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        self.assertIn('CRE-001 SEMANTIC CHECK PASSED',cp.stdout)
    def test_generated_task_ids_and_provenance_are_unambiguous(self):
        path=ROOT/'docs/planning/next-actions.md'; before=path.read_text(encoding='utf-8')
        cp=subprocess.run([sys.executable,'tools/generate_next_tasks.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        text=path.read_text(encoding='utf-8'); self.assertEqual(text,before)
        ranked=text.split('## Maintainer Task Briefs',1)[0]
        ids=re.findall(r'^### ([A-Z]+-\d{3}):',ranked,re.M); self.assertEqual(len(ids),len(set(ids)))
        self.assertNotIn('### STRATEGIC-001: Freeze the concrete reasoning and contrast corpora',ranked)
        self.assertNotIn('### STRATEGIC-002: Execute dimensioned GREL-FARA factorization',ranked)
        self.assertNotIn('### STRATEGIC-002: Execute reasoning/contrast discrimination and FARA specificity',ranked)
        self.assertNotIn('### STRATEGIC-003: Execute candidate ablation and reconstruction',ranked)
        self.assertIn('### STRATEGIC-004: Complete W3.5 machinery cost, claim-impact, and preserved-failure closure',ranked)
        self.assertIn('### STRATEGIC-005: Assemble the finite-core theorem or strongest obstruction',ranked)
        self.assertIn('all twelve registered candidate tests are complete',ranked)
        self.assertIn('No registered candidate is indispensable within the frozen class',ranked)
        self.assertIn('Machinery/cost, claim-impact, and preserved-failure closure are next',ranked)
        self.assertIn('- Source: central research program',ranked)
        self.assertIn('- Priority: blocked',ranked)
        self.assertNotIn('W5 is authorized',ranked)
        for stale in ('Execute the W4 S_core formal negative controls','Execute W3.5 baseline factorization and universal-discovery gate','Prove the W0 S_core normalization kernel','Prove the W1 S_core base carriers and direct axes','Prove the W2 S_core dynamics history and revision package','Prove the W3 S_core global witness obligations','Build the S_core construction and obstruction ledger','Resolve the formal role of P8','Formalize faithful representation and nontriviality','Freeze THM-TARGET-001 and premise ledger','Plan independent replication of CRE-002-EXT-001','Source gap:'):
            self.assertNotIn(stale,ranked)
if __name__=='__main__': unittest.main()
