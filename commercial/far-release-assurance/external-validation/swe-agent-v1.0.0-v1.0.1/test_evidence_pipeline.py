from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import evidence_pipeline as ep


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class EvidencePipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.output = self.root / "execution-output"
        self.trajectories = self.output / "trajectories"
        self.primary = self.output / "primary"
        self.packages = self.primary / "packages"
        self.freeze = self.output / "primary-freeze.json"
        self.reveal = self.output / "post-freeze-reveal"
        self.patches = [
            patch.object(ep, "OUTPUT_DIR", self.output),
            patch.object(ep, "STATE_PATH", self.output / "execution-state.json"),
            patch.object(ep, "TRAJECTORY_DIR", self.trajectories),
            patch.object(ep, "PRIMARY_DIR", self.primary),
            patch.object(ep, "PACKAGES_DIR", self.packages),
            patch.object(ep, "COMPARISON_PATH", self.primary / "blinded-comparison.json"),
            patch.object(ep, "FREEZE_PATH", self.freeze),
            patch.object(ep, "REVEAL_DIR", self.reveal),
        ]
        for item in self.patches:
            item.start()
        self.addCleanup(self.cleanup)
        self.make_complete_state()

    def cleanup(self) -> None:
        for item in reversed(self.patches):
            item.stop()
        self.tmp.cleanup()

    def make_complete_state(self) -> None:
        runs = []
        matrix = [("v1.0.0", 1), ("v1.0.0", 2), ("v1.0.1", 1), ("v1.0.1", 2)]
        for release, repetition in matrix:
            run_id = f"{release}-r{repetition}"
            trajectory_rel = f"trajectories/{run_id}.traj"
            record_rel = f"runs/{run_id}/run-record.json"
            trajectory = {
                "history": [{"role": "assistant", "content": f"step-{repetition}"}],
                "info": {"exit_status": "submitted"},
            }
            trajectory_path = self.output / trajectory_rel
            write_json(trajectory_path, trajectory)
            write_json(self.output / record_rel, {"benchmark_outcomes_accessed": False})
            runs.append({
                "run_id": run_id,
                "release": release,
                "repetition": repetition,
                "state": "complete",
                "trajectory": trajectory_rel,
                "trajectory_sha256": ep.sha256_file(trajectory_path),
                "record": record_rel,
            })
        write_json(self.output / "execution-state.json", {
            "schema": "far-swe-agent-execution-state/1.1",
            "case_id": "case-test",
            "execution_plan_sha256": "a" * 64,
            "environment_lock_sha256": "b" * 64,
            "runs": runs,
        })

    def test_compile_creates_four_blinded_packages_and_comparison(self) -> None:
        paths = ep.compile_primary()
        self.assertEqual(len(paths), 5)
        packages = sorted(self.packages.glob("*.json"))
        self.assertEqual(len(packages), 4)
        for path in packages:
            package = json.loads(path.read_text())
            self.assertIn(package["blind_system"], {"System-A", "System-B"})
            self.assertNotIn("release", package)
            self.assertFalse(package["outcomes_accessed"])
        comparison = json.loads((self.primary / "blinded-comparison.json").read_text())
        self.assertEqual(set(comparison["systems"]), {"System-A", "System-B"})
        self.assertFalse(comparison["outcomes_accessed"])

    def test_outcome_field_before_freeze_is_rejected(self) -> None:
        trajectory = self.trajectories / "v1.0.0-r1.traj"
        value = json.loads(trajectory.read_text())
        value["grader_output"] = {"resolved": True}
        write_json(trajectory, value)
        state = json.loads((self.output / "execution-state.json").read_text())
        state["runs"][0]["trajectory_sha256"] = ep.sha256_file(trajectory)
        write_json(self.output / "execution-state.json", state)
        with self.assertRaises(SystemExit):
            ep.compile_primary()

    def test_incomplete_run_blocks_compile(self) -> None:
        state_path = self.output / "execution-state.json"
        state = json.loads(state_path.read_text())
        state["runs"][3]["state"] = "pending"
        write_json(state_path, state)
        with self.assertRaises(SystemExit):
            ep.compile_primary()

    def test_freeze_detects_tampering(self) -> None:
        ep.freeze_primary()
        ep.verify_freeze()
        package = next(self.packages.glob("*.json"))
        package.write_text(package.read_text() + "tamper", encoding="utf-8")
        with self.assertRaises(SystemExit):
            ep.verify_freeze()

    def test_reveal_requires_verified_freeze_and_exact_run_ids(self) -> None:
        ep.freeze_primary()
        outcomes = self.root / "outcomes.json"
        write_json(outcomes, {
            "v1.0.0-r1": {"resolved": False},
            "v1.0.0-r2": {"resolved": False},
            "v1.0.1-r1": {"resolved": True},
            "v1.0.1-r2": {"resolved": True},
        })
        target = ep.reveal(outcomes)
        reveal = json.loads(target.read_text())
        self.assertEqual(reveal["primary_freeze_sha256"], ep.sha256_file(self.freeze))
        self.assertEqual(set(reveal["outcomes"]), {
            "v1.0.0-r1", "v1.0.0-r2", "v1.0.1-r1", "v1.0.1-r2",
        })

    def test_reveal_rejects_missing_or_extra_runs(self) -> None:
        ep.freeze_primary()
        outcomes = self.root / "outcomes.json"
        write_json(outcomes, {"v1.0.0-r1": {"resolved": False}})
        with self.assertRaises(SystemExit):
            ep.reveal(outcomes)


if __name__ == "__main__":
    unittest.main()
