import importlib.util
import json
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
        raw = json.dumps(self.baseline, sort_keys=True).encode("utf-8")
        self.decisions = {
            "source": "source.json", "baseline_commit": "a",
            "baseline_git_blob_sha": reconcile.git_blob_sha(raw),
            "audited_main_commit": "b", "decisions": [],
        }

    def generate(self):
        return reconcile.reconcile(Path.cwd(), self.baseline, self.decisions)

    def test_frozen_baseline_digest_is_required_and_verified(self):
        raw = json.dumps(self.baseline, sort_keys=True).encode("utf-8")
        reconcile.verify_frozen_baseline(raw, self.decisions)
        missing = dict(self.decisions)
        missing.pop("baseline_git_blob_sha")
        with self.assertRaisesRegex(ValueError, "must pin"):
            reconcile.verify_frozen_baseline(raw, missing)
        changed = raw + b"\n"
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            reconcile.verify_frozen_baseline(changed, self.decisions)

    def test_unaudited_finding_fails_closed_to_cannot_verify(self):
        record = self.generate()["findings"][0]
        self.assertEqual("cannot_verify", record["disposition"])
        self.assertNotIn("baseline evidence", record["evidence"])
        self.assertFalse(record["root_cause_verified"])
        self.assertEqual("unknown", record["blocks_experiment_reconstruction"])

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
        self.decisions["decisions"] = [{"finding_id": "PR1:T1", "disposition": "fixed_on_current_main", "evidence": []}]
        with self.assertRaisesRegex(ValueError, "disposition-specific evidence"):
            self.generate()

    def test_definitive_override_requires_new_explicit_rationale(self):
        self.decisions["decisions"] = [{
            "finding_id": "PR1:T1", "disposition": "fixed_on_current_main",
            "evidence": ["fix commit and regression test"],
        }]
        with self.assertRaisesRegex(ValueError, "disposition-specific rationale"):
            self.generate()

    def test_reproducible_override_requires_verified_mechanism(self):
        self.decisions["decisions"] = [{
            "finding_id": "PR1:T1", "disposition": "still_reproducible",
            "evidence": ["reproduced on current main"],
            "failure_mechanism": "current behavior still violates the requirement",
        }]
        errors = reconcile.validate(self.generate(), self.baseline)
        self.assertTrue(any("verified mechanism" in error for error in errors))

    def test_fixed_finding_is_removed_from_residual_count(self):
        self.decisions["decisions"] = [{
            "finding_id": "PR1:T1", "disposition": "fixed_on_current_main",
            "evidence": ["fix commit and regression test"],
            "failure_mechanism": "the former defect is now prevented by the regression test",
            "root_cause_id": "cause:one",
            "blocks_experiment_reconstruction": False,
        }]
        data = self.generate()
        self.assertEqual(0, data["counts"]["residual"])
        self.assertEqual([], reconcile.validate(data, self.baseline))

    def test_invalid_experiment_blocking_status_fails_closed(self):
        self.decisions["decisions"] = [{
            "finding_id": "PR1:T1", "disposition": "cannot_verify",
            "blocks_experiment_reconstruction": "probably",
        }]
        with self.assertRaisesRegex(ValueError, "invalid experiment-blocking status"):
            self.generate()

    def test_unresolved_p1_is_prominent(self):
        self.assertIn(
            "**1 unresolved P1 findings require verification or remediation.**",
            reconcile.render_report(self.generate()),
        )

    def test_unrelated_same_path_findings_are_not_false_batched(self):
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
        self.assertIn("No residual finding currently has a verified root-cause batch.", batches)
        self.assertNotIn(records[0]["root_cause_id"], batches)
        self.assertNotIn(records[1]["root_cause_id"], batches)

    def test_unaudited_batch_count_is_derived(self):
        self.assertIn("The 1 unaudited findings remain", reconcile.render_batches(self.generate()))
        self.decisions["decisions"] = [{
            "finding_id": "PR1:T1", "disposition": "fixed_on_current_main",
            "evidence": ["fixed"], "failure_mechanism": "fixed mechanism",
            "root_cause_id": "cause:one",
        }]
        self.assertIn("The 0 unaudited findings remain", reconcile.render_batches(self.generate()))

    def test_verified_batch_renders_each_member_metadata(self):
        second = dict(self.baseline["findings"][0])
        second.update({"finding_id": "PR1:T2", "thread_id": "T2", "comment_id": "C2"})
        self.baseline["findings"].append(second)
        self.decisions["decisions"] = [
            {
                "finding_id": finding_id,
                "disposition": "still_reproducible",
                "evidence": [f"reproduced {finding_id}"],
                "failure_mechanism": "shared demonstrated mechanism",
                "root_cause_id": "shared:cause",
                "smallest_complete_remediation_boundary": f"repair boundary for {finding_id}",
                "blocks_experiment_reconstruction": blocks,
            }
            for finding_id, blocks in (("PR1:T1", True), ("PR1:T2", False))
        ]
        batches = reconcile.render_batches(self.generate())
        for expected in (
            "PR1:T1", "PR1:T2", "T1", "T2", "C1", "C2",
            "repair boundary for PR1:T1", "repair boundary for PR1:T2",
            "Experiment blocking: `true`", "Experiment blocking: `false`",
        ):
            self.assertIn(expected, batches)

    def test_compact_ledger_preserves_complete_source_by_composition(self):
        ledger = reconcile.compact_ledger(self.generate())
        self.assertEqual(1, ledger["source_finding_count"])
        self.assertEqual("cannot_verify", ledger["default_disposition"])
        self.assertEqual("unknown", ledger["default_experiment_blocking_status"])
        self.assertEqual(self.decisions["baseline_git_blob_sha"], ledger["baseline_git_blob_sha"])
        self.assertEqual([], ledger["explicit_findings"])

    def test_generation_is_deterministic(self):
        self.assertEqual(self.generate(), self.generate())


if __name__ == "__main__":
    unittest.main()
