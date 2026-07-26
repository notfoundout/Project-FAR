from __future__ import annotations

import hashlib
import json
import tempfile
import types
import unittest
from dataclasses import asdict, dataclass
from pathlib import Path

import budget_limited_completion_v2 as budget


@dataclass
class Outcome:
    category: str
    state: str
    retryable: bool
    internal_status: str | None
    patch_present: bool
    no_change_submission: bool
    reason: str
    evidence: dict

    def to_dict(self) -> dict:
        return asdict(self)


class BudgetLimitedClassifierTests(unittest.TestCase):
    def terminal(self, **overrides):
        values = {
            "category": "terminal_agent_error",
            "state": "failed_terminal",
            "retryable": False,
            "internal_status": "submitted (exit_cost)",
            "patch_present": True,
            "no_change_submission": False,
            "reason": "legacy rejection",
            "evidence": {"provider_classification_signal": None},
        }
        values.update(overrides)
        return Outcome(**values)

    def classify(self, outcome: Outcome, rc: int = 0):
        wrapped = budget.wrap_classifier(lambda **_kwargs: outcome, Outcome)
        return wrapped(
            outer_returncode=rc,
            swe_output=Path("."),
            task_id="task",
            stdout="",
            stderr="",
            allow_no_change=False,
        )

    def test_exact_budget_autosubmission_is_complete(self) -> None:
        outcome = self.classify(self.terminal())
        self.assertEqual(outcome.state, "complete")
        self.assertEqual(outcome.category, budget.COMPLETE_CATEGORY)
        self.assertTrue(outcome.patch_present)
        self.assertFalse(outcome.evidence["benchmark_quality_evaluated"])

    def test_provider_failure_is_not_reclassified(self) -> None:
        original = self.terminal(
            category="provider_quota_exhaustion",
            state="failed_retryable",
            retryable=True,
        )
        self.assertIs(self.classify(original), original)

    def test_empty_patch_is_not_reclassified(self) -> None:
        original = self.terminal(patch_present=False)
        self.assertIs(self.classify(original), original)

    def test_nonzero_outer_return_is_not_reclassified(self) -> None:
        original = self.terminal()
        self.assertIs(self.classify(original, rc=1), original)


class BudgetLimitedReclassificationTests(unittest.TestCase):
    TASK_ID = "scikit-learn__scikit-learn-14125"
    PLAN = "a" * 64
    IMAGE = "ghcr.io/example/image@sha256:" + "b" * 64
    CONFIG_HASH = "c" * 64

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.output = self.root / "execution-output"
        self.runs = self.output / "runs"
        self.trajectories = self.output / "trajectories"
        self.config = self.root / "agent-config.yaml"
        self.config.write_text("frozen config\n", encoding="utf-8")
        self.run_dir = self.runs / "v1.0.0-r1"
        self.swe_output = self.run_dir / "sweagent-output"
        self.native_dir = self.swe_output / self.TASK_ID
        self.native_dir.mkdir(parents=True)
        self.native_trajectory = self.native_dir / f"{self.TASK_ID}.traj"
        self.native_trajectory.write_text('{"trajectory": true}\n', encoding="utf-8")
        (self.run_dir / "stdout.log").write_text("", encoding="utf-8")
        (self.run_dir / "stderr.log").write_text("", encoding="utf-8")
        (self.run_dir / "instance.json").write_text(
            json.dumps([{"id": self.TASK_ID}]), encoding="utf-8"
        )
        (self.swe_output / "run_batch_exit_statuses.yaml").write_text(
            "instances_by_exit_status:\n"
            "  submitted (exit_cost):\n"
            f"    - {self.TASK_ID}\n",
            encoding="utf-8",
        )
        (self.native_dir / f"{self.TASK_ID}.pred").write_text(
            json.dumps(
                {
                    "instance_id": self.TASK_ID,
                    "model_patch": "diff --git a/a b/a\n",
                }
            ),
            encoding="utf-8",
        )
        self.invocation = {
            "schema": "far-swe-agent-invocation/1.3",
            "run_id": "v1.0.0-r1",
            "release": "v1.0.0",
            "commit": "1" * 40,
            "attempt": 1,
            "task_id": self.TASK_ID,
            "image": self.IMAGE,
            "agent_config_sha256": self.CONFIG_HASH,
            "execution_plan_sha256": self.PLAN,
            "benchmark_outcomes_accessible": False,
        }
        self.write_json(self.run_dir / "invocation.json", self.invocation)
        self.run = {
            "run_id": "v1.0.0-r1",
            "slot": 1,
            "release": "v1.0.0",
            "repetition": 1,
            "full_commit": "1" * 40,
            "attempts": 1,
            "state": "failed_terminal",
            "outcome_category": "terminal_agent_error",
            "record": "runs/v1.0.0-r1/run-record.json",
            "trajectory": "trajectories/baseline-run-1.traj",
            "trajectory_artifact": "baseline-run-1.traj",
        }
        self.state = {
            "runs": [
                self.run,
                {
                    "run_id": "v1.0.0-r2",
                    "slot": 2,
                    "state": "pending",
                    "attempts": 0,
                },
            ]
        }
        self.saved_states: list[dict] = []
        self.original_record_bytes = b""
        self.legacy = self.make_legacy()
        self.write_record()
        budget.install(self.legacy)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    @staticmethod
    def write_json(path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    @staticmethod
    def hash_file(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def current_hashes(self, run_dir: Path) -> dict[str, str]:
        hashes = {}
        for path in sorted(item for item in run_dir.rglob("*") if item.is_file()):
            relative = path.relative_to(run_dir)
            if (
                relative.parts[0] == "attempts"
                or relative.name in {"run-record.json", "run-record-correction.json"}
            ):
                continue
            hashes[str(relative)] = self.hash_file(path)
        return hashes

    def collect_hashes(self, root: Path) -> dict[str, str]:
        return {
            str(path.relative_to(root)): self.hash_file(path)
            for path in sorted(item for item in root.rglob("*") if item.is_file())
        }

    def write_record(self) -> None:
        record = {
            "schema": "far-swe-agent-run-record/1.2",
            "run_id": self.run["run_id"],
            "release": self.run["release"],
            "commit": self.run["full_commit"],
            "repetition": self.run["repetition"],
            "attempt": 1,
            "task_id": self.TASK_ID,
            "image": self.IMAGE,
            "execution_plan_sha256": self.PLAN,
            "returncode": 0,
            "completed_at": "2026-07-26T12:00:50+00:00",
            "benchmark_outcomes_accessed": False,
            "state": "failed_terminal",
            "outcome": {
                "category": "terminal_agent_error",
                "state": "failed_terminal",
            },
            "artifact_sha256": self.current_hashes(self.run_dir),
        }
        path = self.run_dir / "run-record.json"
        self.write_json(path, record)
        self.original_record_bytes = path.read_bytes()

    def make_legacy(self):
        test = self

        class Base:
            OUTPUT_DIR = test.output
            RUNS_DIR = test.runs
            TRAJECTORY_DIR = test.trajectories
            CONFIG_PATH = test.config

            @staticmethod
            def sha256_file(path: Path) -> str:
                if Path(path) == test.config:
                    return test.CONFIG_HASH
                return test.hash_file(Path(path))

            @staticmethod
            def read_json(path: Path):
                return json.loads(Path(path).read_text(encoding="utf-8"))

            @staticmethod
            def write_json(path: Path, value: object) -> None:
                test.write_json(Path(path), value)

            @staticmethod
            def collect_hashes(path: Path) -> dict[str, str]:
                return test.collect_hashes(Path(path))

            @staticmethod
            def save_state(state: dict) -> None:
                test.saved_states.append(json.loads(json.dumps(state)))

            @staticmethod
            def utc_now() -> str:
                return "2026-07-26T12:05:00+00:00"

            @staticmethod
            def locate_trajectory(output: Path, task_id: str) -> Path:
                candidates = sorted(Path(output).rglob("*.traj"))
                exact = [path for path in candidates if path.stem == task_id]
                if len(exact) != 1:
                    raise SystemExit("expected exact trajectory")
                return exact[0]

            @staticmethod
            def frozen_inputs():
                return {}, {"immutable_image_reference": test.IMAGE}, {
                    "instance_id": test.TASK_ID
                }

            @staticmethod
            def validate_plan(_manifest, _lock) -> str:
                return test.PLAN

            @staticmethod
            def load_state(_manifest, _lock, _plan) -> dict:
                return test.state

        def delegate(**_kwargs):
            return Outcome(
                "terminal_agent_error",
                "failed_terminal",
                False,
                budget.BUDGET_STATUS,
                True,
                False,
                "legacy rejection",
                {"provider_classification_signal": None},
            )

        core = types.SimpleNamespace(
            base=Base,
            ExecutionOutcome=Outcome,
            classify_execution=delegate,
            _record_path=lambda run: test.runs / run["run_id"] / "run-record.json",
            _current_artifact_hashes=test.current_hashes,
            _classify_preserved_run=lambda *_args, **_kwargs: (
                {},
                Outcome(
                    "terminal_agent_error",
                    "failed_terminal",
                    False,
                    None,
                    False,
                    False,
                    "missing completion provenance",
                    {},
                ),
            ),
            reconcile_completed_runs=lambda _state, _task: False,
            _ensure_progressable=lambda _state: None,
        )
        return types.SimpleNamespace(
            _core=core, _hardening=types.SimpleNamespace(classify_execution=delegate)
        )

    def test_reclassification_preserves_attempt_and_stops_at_correction(self) -> None:
        result = self.legacy._core.reconcile_only()
        self.assertTrue(result["changed"])
        self.assertEqual(self.run["attempts"], 1)
        self.assertEqual(self.run["state"], "complete")
        self.assertEqual(self.run["outcome_category"], budget.COMPLETE_CATEGORY)
        self.assertTrue((self.output / self.run["trajectory"]).is_file())
        self.assertTrue((self.output / self.run["correction"]).is_file())
        self.assertEqual(
            (self.run_dir / "run-record.json").read_bytes(),
            self.original_record_bytes,
        )
        self.assertEqual(self.state["runs"][1]["state"], "pending")

    def test_existing_correction_is_never_silently_reapplied(self) -> None:
        self.run["correction"] = "corrections/tampered.json"
        self.run["corrected_from"] = "complete"
        result = budget.reclassify_budget_limited_failure(
            self.legacy._core, self.state, self.TASK_ID
        )
        self.assertFalse(result)
        self.assertEqual(self.run["state"], "failed_terminal")
        self.assertFalse((self.output / "corrections").exists())

    def test_corrected_completion_revalidates_from_sidecar(self) -> None:
        self.legacy._core.reconcile_only()
        record, outcome = self.legacy._core._classify_preserved_run(
            self.run,
            self.TASK_ID,
            plan_sha256=self.PLAN,
            image=self.IMAGE,
        )
        self.assertEqual(record["state"], "failed_terminal")
        self.assertEqual(outcome.state, "complete")
        self.assertEqual(outcome.category, budget.COMPLETE_CATEGORY)


if __name__ == "__main__":
    unittest.main()
