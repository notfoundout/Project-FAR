from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import evidence_pipeline_v2 as ep

ROOT = Path(__file__).resolve().parents[4]
WORKFLOW = ROOT / ".github/workflows/far-swe-agent-v2-postprocess.yml"


class PrimaryFreezeContractTests(unittest.TestCase):
    def test_committed_primary_freeze_verifies(self) -> None:
        freeze = ep.verify_freeze()
        self.assertEqual(freeze["case_id"], ep.CASE_ID)
        self.assertFalse(freeze["outcomes_accessed"])
        self.assertTrue(
            freeze["reveal_permitted_only_after_merge_and_independent_verification"]
        )

    def test_source_artifact_identity_is_exact(self) -> None:
        lock = ep.read_json(ep.SOURCE_LOCK_PATH)
        source = lock["source"]
        self.assertEqual(source["workflow_run_id"], 30214963069)
        self.assertEqual(source["artifact_id"], 8635674915)
        self.assertEqual(
            source["artifact_digest"],
            "sha256:7277987300d4204c5108997b3ac6c0cde02c9a4d498178a702ea7a6cb0c19756",
        )
        self.assertEqual(
            source["workflow_head_sha"],
            "b0fc2e6d6bb8763a960679c445cc094e13fe8609",
        )
        self.assertEqual(lock["file_count"], 73)

    def test_four_blinded_packages_have_no_release_identity_or_outcome(self) -> None:
        packages = sorted((ep.PRIMARY_DIR / "packages").glob("*.json"))
        self.assertEqual(len(packages), 4)
        self.assertEqual(
            {path.stem for path in packages},
            {"System-A-r1", "System-A-r2", "System-B-r1", "System-B-r2"},
        )
        for path in packages:
            value = ep.read_json(path)
            self.assertFalse(value["outcomes_accessed"])
            self.assertNotIn("release", value)
            self.assertNotIn("resolved", json.dumps(value).lower())
            ep.scan_forbidden(value, path.name)

    def test_adjudication_remains_outcome_blind(self) -> None:
        value = ep.read_json(ep.ADJUDICATION_PATH)
        self.assertFalse(value["outcomes_accessed"])
        self.assertFalse(value["release_identity_used_for_judgment"])
        self.assertEqual(value["overall_decision"], "REVIEW_REQUIRED")
        body = {key: child for key, child in value.items() if key != "case_id"}
        text = json.dumps(body)
        self.assertNotIn("v1.0.0", text)
        self.assertNotIn("v1.0.1", text)
        ep.scan_forbidden(value, "adjudication")

    def test_decision_summary_is_bounded_observation(self) -> None:
        outcomes = {
            "v1.0.0-r1": {"release": "v1.0.0", "resolved": False},
            "v1.0.0-r2": {"release": "v1.0.0", "resolved": True},
            "v1.0.1-r1": {"release": "v1.0.1", "resolved": True},
            "v1.0.1-r2": {"release": "v1.0.1", "resolved": True},
        }
        counts, result = ep.decision_summary(outcomes)
        self.assertEqual(counts, {"v1.0.0": 1, "v1.0.1": 2})
        self.assertEqual(result, "candidate_higher_observed_resolution")

    def test_collect_outcomes_requires_exact_four_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for run_id, _release, _rep in ep.EXPECTED_RUNS[:-1]:
                run = root / run_id
                run.mkdir(parents=True)
                ep.write_json(run / "report.json", {ep.TASK_ID: {"resolved": False}})
                (run / "test_output.txt").write_text("test", encoding="utf-8")
                (run / "run_instance.log").write_text("log", encoding="utf-8")
            with self.assertRaises(SystemExit):
                ep.collect_outcomes(root)


class PostprocessWorkflowContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_exact_source_artifact_is_pinned(self) -> None:
        self.assertIn("8635674915", self.text)
        self.assertIn(
            "7277987300d4204c5108997b3ac6c0cde02c9a4d498178a702ea7a6cb0c19756",
            self.text,
        )
        self.assertIn("python evidence_pipeline_v2.py verify-source", self.text)
        self.assertIn("python evidence_pipeline_v2.py verify-freeze", self.text)

    def test_reveal_is_main_only_and_explicitly_confirmed(self) -> None:
        self.assertIn('test "$GITHUB_REF" = "refs/heads/main"', self.text)
        self.assertIn(
            "REVEAL-FAR-V2-OUTCOMES-AFTER-PRIMARY-FREEZE", self.text
        )
        verify = self.text.index("python evidence_pipeline_v2.py verify-freeze")
        harness = self.text.index("swebench.harness.run_evaluation")
        self.assertLess(verify, harness)

    def test_exact_harness_and_image_are_pinned(self) -> None:
        self.assertIn(
            "f7bbbb2ccdf479001d6467c9e34af59e44a840f9", self.text
        )
        self.assertIn(
            "ghcr.io/notfoundout/project-far-swebench-scikit-learn-14125@sha256:66615e837a9fdc6faf75dab3db90bf469364204b068af9da4d570fba8ab00ab4",
            self.text,
        )
        self.assertIn(
            "sweb.eval.x86_64.scikit-learn_1776_scikit-learn-14125:locked",
            self.text,
        )

    def test_no_model_secret_or_new_model_call_exists(self) -> None:
        self.assertNotIn("GEMINI_API_KEY", self.text)
        self.assertNotIn("validated_execute_controller.py execute-next", self.text)

    def test_all_four_runs_are_evaluated_separately(self) -> None:
        self.assertIn(
            'for RUN_ID in v1.0.0-r1 v1.0.0-r2 v1.0.1-r1 v1.0.1-r2',
            self.text,
        )
        self.assertIn("--max_workers 1", self.text)
        self.assertIn("--instance_ids scikit-learn__scikit-learn-14125", self.text)


if __name__ == "__main__":
    unittest.main()
