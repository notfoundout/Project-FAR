import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "tools/reconcile_merged_pr_review_findings.py"
spec = importlib.util.spec_from_file_location("reconcile", PATH)
assert spec and spec.loader
reconcile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reconcile)


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.baseline = {
            "findings": [{
                "finding_id": "PR1:T1", "pr_number": 1, "thread_id": "T1",
                "comment_id": "C1", "url": "u", "path": "missing", "line": 2,
                "reviewer_claim": "Fix defect", "disposition": "resolved_incorrectly",
                "risk": "high", "evidence": ["baseline evidence"],
            }]
        }
        self.decisions = {
            "source": "source.json", "baseline_commit": "a",
            "audited_main_commit": "b", "decisions": [],
        }

    def generate(self):
        return reconcile.reconcile(Path.cwd(), self.baseline, self.decisions)

    def test_unaudited_finding_fails_closed_to_cannot_verify(self):
        data = self.generate()
        self.assertEqual(["PR1:T1"], [x["finding_id"] for x in data["findings"]])
        record = data["findings"][0]
        self.assertEqual("cannot_verify", record["disposition"])
        self.assertNotIn("baseline evidence", record["evidence"])
        self.assertFalse(record["root_cause_verified"])

    def test_unknown_and_duplicate_decisions_fail_closed(self):
        self.decisions["decisions"] = [{"finding_id": "PR9:X", "disposition": "cannot_verify"}]
        with self.assertRaises(ValueError):
            self.generate()
        self.decisions["decisions"] = [{"finding_id": "PR1:T1", "disposition": "cannot_verify"}] * 2
        with self.assertRaises(ValueError):
            self.generate()

    def test_definitive_override_requires_new_explicit_evidence(self):
        self.decisions["decisions"] = [{"finding_id": "PR1:T1", "disposition": "fixed_on_current_main"}]
        with self.assertRaisesRegex(ValueError, "disposition-specific evidence"):
            self.generate()
        self.decisions["decisions"] = [{
            "finding_id": "PR1:T1", "disposition": "fixed_on_current_main", "evidence": []
        }]
        with self.assertRaisesRegex(ValueError, "disposition-specific evidence"):
            self.generate()

    def test_reproducible_override_requires_evidence_and_verified_mechanism(self):
        self.decisions["decisions"] = [{
            "finding_id": "PR1:T1", "disposition": "still_reproducible",
            "evidence": ["reproduced on current main"],
        }]
        data = self.generate()
        queue = reconcile.render_queue(data)
        self.assertTrue(any("verified mechanism" in error for error in reconcile.validate(data, self.baseline, queue)))

    def test_queue_exactly_matches_residual_ledger(self):
        data = self.generate()
        queue = reconcile.render_queue(data)
        self.assertEqual([], reconcile.validate(data, self.baseline, queue))
        self.assertTrue(reconcile.validate(data, self.baseline, queue.replace("`PR1:T1`", "`removed`")))

    def test_fixed_finding_cannot_remain_in_queue(self):
        self.decisions["decisions"] = [{
            "finding_id": "PR1:T1", "disposition": "fixed_on_current_main",
            "evidence": ["fix commit and regression test"], "root_cause_id": "cause:one",
        }]
        data = self.generate()
        queue = reconcile.render_queue(data)
        self.assertNotIn("`PR1:T1`", queue)
        self.assertEqual(0, data["counts"]["residual"])

    def test_unresolved_p1_is_prominent(self):
        self.assertIn(
            "**1 unresolved P1 findings require verification or remediation.**",
            reconcile.render_report(self.generate()),
        )

    def test_unrelated_same_path_findings_keep_distinct_boundaries(self):
        second = dict(self.baseline["findings"][0])
        second.update({
            "finding_id": "PR1:T2", "thread_id": "T2", "comment_id": "C2",
            "reviewer_claim": "Fix another unrelated defect",
        })
        self.baseline["findings"].append(second)
        data = self.generate()
        records = data["findings"]
        self.assertNotEqual(records[0]["root_cause_id"], records[1]["root_cause_id"])
        batches = reconcile.render_batches(data)
        for record in records:
            self.assertIn(record["finding_id"], batches)
            self.assertIn(record["smallest_complete_remediation_boundary"], batches)
            self.assertIn(record["thread_id"], batches)
            self.assertIn(record["comment_id"], batches)

    def test_generation_is_deterministic(self):
        self.assertEqual(self.generate(), self.generate())


if __name__ == "__main__":
    unittest.main()
