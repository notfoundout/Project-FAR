#!/usr/bin/env python3
"""Executable replication of the pre-correction evidence-closure defect."""
from __future__ import annotations

import subprocess
import tempfile
import types
import unittest
from pathlib import Path

import yaml

from tools.check_investigation_execution import validate_manifest as current_validate_manifest

ROOT = Path(__file__).resolve().parents[1]
FROZEN_COMMIT = "4e258fd3b7c5a80b6f7263ad6f2e085f913b1d2a"
FROZEN_VALIDATOR_PATH = "tools/check_investigation_execution.py"
FROZEN_VALIDATOR_BLOB = "4d21937a471f55f3336d809a5378660e2a294c0c"
CONTRACT_ID = "FAR-EVIDENCE-CLOSURE-1.0"


def _git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def _load_frozen_validator() -> types.ModuleType:
    blob = _git("rev-parse", f"{FROZEN_COMMIT}:{FROZEN_VALIDATOR_PATH}").strip()
    if blob != FROZEN_VALIDATOR_BLOB:
        raise AssertionError(
            f"frozen validator blob drift: expected {FROZEN_VALIDATOR_BLOB}, got {blob}"
        )
    source = _git("show", f"{FROZEN_COMMIT}:{FROZEN_VALIDATOR_PATH}")
    module = types.ModuleType("far_frozen_investigation_validator")
    module.__file__ = str(ROOT / FROZEN_VALIDATOR_PATH)
    exec(compile(source, module.__file__, "exec"), module.__dict__)
    return module


class EvidenceClosureFrozenReplicationTests(unittest.TestCase):
    def test_frozen_validator_accepts_generic_pass_without_evidence_closure(self) -> None:
        frozen = _load_frozen_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "evidence.md"
            evidence.write_text("generic repository-backed evidence\n", encoding="utf-8")
            manifest = root / "VI-EC-REPLICATION.execution.yaml"
            manifest.write_text(
                yaml.safe_dump(
                    {
                        "investigation": "VI-EC-REPLICATION",
                        "result": "pass",
                        "required_steps": [
                            {
                                "id": "GENERIC-STEP",
                                "status": "complete",
                                "evidence": [{"path": "evidence.md"}],
                            }
                        ],
                        "upstream_dependencies": [],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )

            frozen_errors = frozen.validate_manifest(
                manifest,
                root=root,
                manifest_results={},
            )
            self.assertEqual(frozen_errors, [])

            current_errors = current_validate_manifest(
                manifest,
                root=root,
                manifest_results={},
            )
            self.assertIn(
                f"VI-EC-REPLICATION: PASS requires evidence_closure contract {CONTRACT_ID}",
                current_errors,
            )


if __name__ == "__main__":
    unittest.main()
