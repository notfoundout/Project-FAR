import copy
import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "tools/reconcile_merged_pr_review_findings.py"
spec = importlib.util.spec_from_file_location("reconcile", PATH); assert spec and spec.loader
reconcile = importlib.util.module_from_spec(spec); spec.loader.exec_module(reconcile)


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.baseline = {"findings": [{"finding_id": "PR1:T1", "pr_number": 1, "thread_id": "T1", "comment_id": "C1", "url": "u", "path": "missing", "line": 2, "reviewer_claim": "Fix defect", "disposition": "resolved_incorrectly", "risk": "high", "evidence": ["observed"]}]}
        self.decisions = {"source": "source.json", "baseline_commit": "a", "audited_main_commit": "b", "decisions": []}

    def generate(self): return reconcile.reconcile(Path.cwd(), self.baseline, self.decisions)

    def test_no_original_finding_disappears_and_disposition_is_unique(self):
        data = self.generate(); self.assertEqual(["PR1:T1"], [x["finding_id"] for x in data["findings"]]); self.assertEqual("still_reproducible", data["findings"][0]["disposition"])

    def test_unknown_and_duplicate_decisions_fail_closed(self):
        decision = {"finding_id": "PR9:X", "disposition": "cannot_verify"}
        self.decisions["decisions"] = [decision]
        with self.assertRaises(ValueError): self.generate()
        self.decisions["decisions"] = [{"finding_id": "PR1:T1", "disposition": "cannot_verify"}] * 2
        with self.assertRaises(ValueError): self.generate()

    def test_definitive_disposition_requires_evidence(self):
        self.decisions["decisions"] = [{"finding_id": "PR1:T1", "disposition": "fixed_on_current_main", "evidence": []}]
        with self.assertRaises(ValueError): self.generate()

    def test_queue_exactly_matches_residual_ledger(self):
        data = self.generate(); queue = reconcile.render_queue(data)
        self.assertEqual([], reconcile.validate(data, self.baseline, queue))
        self.assertTrue(reconcile.validate(data, self.baseline, queue.replace("`PR1:T1`", "`removed`")))

    def test_fixed_finding_cannot_remain_in_queue(self):
        self.decisions["decisions"] = [{"finding_id": "PR1:T1", "disposition": "fixed_on_current_main", "evidence": ["test"]}]
        data = self.generate(); queue = reconcile.render_queue(data)
        self.assertNotIn("`PR1:T1`", queue); self.assertEqual(0, data["counts"]["residual"])

    def test_unresolved_p1_is_prominent(self):
        self.assertIn("**1 unresolved P1 findings require remediation.**", reconcile.render_report(self.generate()))

    def test_generation_is_deterministic(self):
        self.assertEqual(self.generate(), self.generate())


if __name__ == "__main__": unittest.main()
