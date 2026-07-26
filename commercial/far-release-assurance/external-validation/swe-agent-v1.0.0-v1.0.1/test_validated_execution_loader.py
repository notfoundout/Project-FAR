from __future__ import annotations

import hashlib
import json
import tempfile
import types
import unittest
from pathlib import Path

from validated_execution_recovery import install


class ReconcilableStateLoaderTests(unittest.TestCase):
    def test_loader_preserves_structural_checks_but_defers_sequence_repair(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = types.SimpleNamespace()
            base.STATE_PATH = root / "execution-state.json"
            base.MANIFEST_PATH = root / "manifest.json"
            base.LOCK_PATH = root / "lock.json"
            base.STATE_SCHEMA = "state/1"
            base.ALLOWED_STATES = {
                "pending",
                "failed_retryable",
                "failed_terminal",
                "complete",
            }
            base.MANIFEST_PATH.write_text("manifest", encoding="utf-8")
            base.LOCK_PATH.write_text("lock", encoding="utf-8")
            base.sha256_file = lambda path: hashlib.sha256(
                Path(path).read_bytes()
            ).hexdigest()
            base.read_json = lambda path: json.loads(
                Path(path).read_text(encoding="utf-8")
            )
            base.initial_state = lambda manifest, lock, plan: self.fail(
                "existing state must be loaded"
            )
            frozen = [
                {
                    "slot": 1,
                    "run_id": "v1.0.0-r1",
                    "release": "v1.0.0",
                    "commit": "short-a",
                    "full_commit": "full-a",
                    "repetition": 1,
                    "trajectory_artifact": "a.traj",
                },
                {
                    "slot": 2,
                    "run_id": "v1.0.0-r2",
                    "release": "v1.0.0",
                    "commit": "short-a",
                    "full_commit": "full-a",
                    "repetition": 2,
                    "trajectory_artifact": "b.traj",
                },
            ]
            base.expected_runs = lambda manifest: frozen
            manifest = {"case_id": "case"}
            lock = {"immutable_image_reference": "image@sha256:digest"}
            state = {
                "schema": base.STATE_SCHEMA,
                "case_id": "case",
                "manifest_sha256": base.sha256_file(base.MANIFEST_PATH),
                "environment_lock_sha256": base.sha256_file(base.LOCK_PATH),
                "execution_plan_sha256": "plan-hash",
                "immutable_image_reference": lock["immutable_image_reference"],
                "runs": [
                    {**frozen[0], "state": "failed_terminal"},
                    {**frozen[1], "state": "complete"},
                ],
            }
            base.STATE_PATH.write_text(json.dumps(state), encoding="utf-8")
            base.load_state = lambda manifest, lock, plan: self.fail(
                "strict loader must be replaced"
            )
            core = types.SimpleNamespace(
                base=base,
                reconcile_completed_runs=lambda state, task_id: False,
                _apply_state_correction=lambda state, run, outcome, record: None,
                _persist_outcome=None,
            )

            install(core)
            loaded = base.load_state(manifest, lock, "plan-hash")

            self.assertEqual(loaded, state)

    def test_loader_still_rejects_frozen_identity_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = types.SimpleNamespace()
            base.STATE_PATH = root / "execution-state.json"
            base.MANIFEST_PATH = root / "manifest.json"
            base.LOCK_PATH = root / "lock.json"
            base.STATE_SCHEMA = "state/1"
            base.ALLOWED_STATES = {"pending", "complete", "failed_terminal"}
            base.MANIFEST_PATH.write_text("manifest", encoding="utf-8")
            base.LOCK_PATH.write_text("lock", encoding="utf-8")
            base.sha256_file = lambda path: hashlib.sha256(
                Path(path).read_bytes()
            ).hexdigest()
            base.read_json = lambda path: json.loads(
                Path(path).read_text(encoding="utf-8")
            )
            base.initial_state = lambda manifest, lock, plan: {}
            frozen = [
                {
                    "slot": 1,
                    "run_id": "v1.0.0-r1",
                    "release": "v1.0.0",
                    "commit": "short-a",
                    "full_commit": "full-a",
                    "repetition": 1,
                    "trajectory_artifact": "a.traj",
                }
            ]
            base.expected_runs = lambda manifest: frozen
            manifest = {"case_id": "case"}
            lock = {"immutable_image_reference": "image@sha256:digest"}
            state = {
                "schema": base.STATE_SCHEMA,
                "case_id": "case",
                "manifest_sha256": base.sha256_file(base.MANIFEST_PATH),
                "environment_lock_sha256": base.sha256_file(base.LOCK_PATH),
                "execution_plan_sha256": "plan-hash",
                "immutable_image_reference": lock["immutable_image_reference"],
                "runs": [
                    {
                        **frozen[0],
                        "full_commit": "tampered",
                        "state": "pending",
                    }
                ],
            }
            base.STATE_PATH.write_text(json.dumps(state), encoding="utf-8")
            core = types.SimpleNamespace(
                base=base,
                reconcile_completed_runs=lambda state, task_id: False,
                _apply_state_correction=lambda state, run, outcome, record: None,
                _persist_outcome=None,
            )

            install(core)

            with self.assertRaisesRegex(SystemExit, "full_commit"):
                base.load_state(manifest, lock, "plan-hash")


if __name__ == "__main__":
    unittest.main()
