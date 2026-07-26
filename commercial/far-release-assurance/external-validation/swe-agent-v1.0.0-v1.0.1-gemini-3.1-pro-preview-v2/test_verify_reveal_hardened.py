from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import evidence_pipeline_v2 as pipeline
import verify_reveal_hardened as hardened


class HardenedRevealTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.primary = self.root / "primary-freeze"
        self.output = self.root / "post-freeze-reveal"
        self.primary.mkdir()
        self.output.mkdir()

        self.source_lock = {
            "schema": pipeline.SOURCE_SCHEMA,
            "case_id": pipeline.CASE_ID,
            "outcomes_accessed": False,
            "content_root_sha256": "a" * 64,
        }
        self.adjudication = {
            "overall_decision": "REVIEW_REQUIRED",
            "findings": [{"question": "q", "decision": "REVIEW_REQUIRED"}],
        }
        pipeline.write_json(self.primary / "source-artifact-lock.json", self.source_lock)
        pipeline.write_json(self.primary / "outcome-blind-adjudication.json", self.adjudication)
        self.freeze = {
            "schema": pipeline.FREEZE_SCHEMA,
            "case_id": pipeline.CASE_ID,
            "outcomes_accessed": False,
            "artifacts": [],
            "artifact_count": 0,
            "root_sha256": pipeline.sha256_bytes(pipeline.canonical_json([])),
            "source_content_root_sha256": self.source_lock["content_root_sha256"],
            "outcome_blind_adjudication_sha256": pipeline.sha256_file(
                self.primary / "outcome-blind-adjudication.json"
            ),
        }
        pipeline.write_json(self.primary / "primary-freeze.json", self.freeze)
        (self.primary / "primary-freeze.sha256").write_text(
            pipeline.sha256_file(self.primary / "primary-freeze.json") + "\n",
            encoding="utf-8",
        )

        outcomes = {}
        for run_id, release, repetition in pipeline.EXPECTED_RUNS:
            resolved = run_id.endswith("r1")
            outcomes[run_id] = {
                "release": release,
                "repetition": repetition,
                "resolved": resolved,
                "report_sha256": "b" * 64,
                "test_output_sha256": "c" * 64,
                "run_instance_log_sha256": "d" * 64,
                "report": {"resolved": resolved},
            }
        counts, observed = pipeline.decision_summary(outcomes)
        self.reveal = {
            "schema": pipeline.REVEAL_SCHEMA,
            "case_id": pipeline.CASE_ID,
            "revealed_at": "2026-07-26T20:00:00+00:00",
            "primary_freeze_sha256": pipeline.sha256_file(
                self.primary / "primary-freeze.json"
            ),
            "primary_root_sha256": self.freeze["root_sha256"],
            "source_content_root_sha256": self.source_lock["content_root_sha256"],
            "blind_mapping": {"System-A": "v1.0.0", "System-B": "v1.0.1"},
            "outcomes": outcomes,
            "resolved_counts": counts,
            "observed_resolution_result": observed,
            "claim_boundary": "bounded",
        }
        self._write_valid_bundle()

        self.patches = patch.multiple(
            pipeline,
            PRIMARY_DIR=self.primary,
            SOURCE_LOCK_PATH=self.primary / "source-artifact-lock.json",
            FREEZE_PATH=self.primary / "primary-freeze.json",
            FREEZE_HASH_PATH=self.primary / "primary-freeze.sha256",
            ADJUDICATION_PATH=self.primary / "outcome-blind-adjudication.json",
        )
        self.patches.start()
        self.addCleanup(self.patches.stop)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write_valid_bundle(self) -> None:
        pipeline.write_json(self.output / "outcome-reveal.json", self.reveal)
        with patch.object(pipeline, "ADJUDICATION_PATH", self.primary / "outcome-blind-adjudication.json"):
            report = hardened.expected_report(self.reveal)
            report["generated_at"] = "2026-07-26T20:01:00+00:00"
            report["outcome_reveal_sha256"] = pipeline.sha256_file(
                self.output / "outcome-reveal.json"
            )
            pipeline.write_json(self.output / "final-comparison-report.json", report)
            (self.output / "final-comparison-report.md").write_text(
                hardened.expected_markdown(self.reveal), encoding="utf-8"
            )
        entries = []
        for name in sorted(hardened.EXPECTED_BUNDLE_FILES):
            path = self.output / name
            entries.append(
                {"path": name, "sha256": pipeline.sha256_file(path), "size_bytes": path.stat().st_size}
            )
        pipeline.write_json(
            self.output / "bundle-sha256.json",
            {
                "schema": "far-swe-agent-v2-final-bundle/1.0",
                "case_id": pipeline.CASE_ID,
                "created_at": "2026-07-26T20:02:00+00:00",
                "artifacts": entries,
                "root_sha256": pipeline.sha256_bytes(pipeline.canonical_json(entries)),
            },
        )

    def test_valid_bundle_passes(self) -> None:
        self.assertEqual(hardened.verify(self.output)["bounded_case_decision"], "REVIEW_REQUIRED")

    def test_stale_freeze_binding_fails(self) -> None:
        reveal = copy.deepcopy(self.reveal)
        reveal["primary_root_sha256"] = "f" * 64
        pipeline.write_json(self.output / "outcome-reveal.json", reveal)
        with self.assertRaisesRegex(SystemExit, "does not match the current primary freeze"):
            hardened.verify(self.output)

    def test_mutated_derived_report_fails_even_with_rehashed_bundle(self) -> None:
        report_path = self.output / "final-comparison-report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["resolved_counts"]["v1.0.1"] = 2
        pipeline.write_json(report_path, report)
        bundle_path = self.output / "bundle-sha256.json"
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        for entry in bundle["artifacts"]:
            path = self.output / entry["path"]
            entry["sha256"] = pipeline.sha256_file(path)
            entry["size_bytes"] = path.stat().st_size
        bundle["root_sha256"] = pipeline.sha256_bytes(
            pipeline.canonical_json(bundle["artifacts"])
        )
        pipeline.write_json(bundle_path, bundle)
        with self.assertRaisesRegex(SystemExit, "not the deterministic derivation"):
            hardened.verify(self.output)

    def test_mutated_markdown_fails_even_with_rehashed_bundle(self) -> None:
        markdown_path = self.output / "final-comparison-report.md"
        markdown_path.write_text(markdown_path.read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")
        bundle_path = self.output / "bundle-sha256.json"
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        for entry in bundle["artifacts"]:
            path = self.output / entry["path"]
            entry["sha256"] = pipeline.sha256_file(path)
            entry["size_bytes"] = path.stat().st_size
        bundle["root_sha256"] = pipeline.sha256_bytes(
            pipeline.canonical_json(bundle["artifacts"])
        )
        pipeline.write_json(bundle_path, bundle)
        with self.assertRaisesRegex(SystemExit, "Markdown report"):
            hardened.verify(self.output)


if __name__ == "__main__":
    unittest.main()
