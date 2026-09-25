"""The far-ir/2.1 diagnostic sequence is normative, so it must not depend on hash randomization.

The executed W5 verifier iterated required-behavior values as a Python set in the loss checks, so a
record with one behavior value outside the metric and another whose loss differs from the metric
reported the two codes in an order that varied with PYTHONHASHSEED. The expected sequence below is
derived by hand from the specification's first-occurrence rule: behavior `false` (first row) has a
metric pair with loss 1 != d(false, false) = 0, and behavior `true` has no metric pair.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from mechanization.far_mechanization.contract_v21 import contract_sha256

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ["LOSS_METRIC_MISMATCH", "METRIC_LOSS_DOMAIN_MISMATCH"]


def probe_record() -> dict:
    record = json.loads((ROOT / "conformance/far-ir-2.1/valid-frontier.json").read_text(encoding="utf-8"))
    approximation = record["contract"]["approximation"]
    approximation["metric"] = {
        "kind": "finite_table_metric",
        "values": [False, "q"],
        "entries": [
            {"left": False, "right": False, "distance": "0"},
            {"left": False, "right": "q", "distance": "1"},
            {"left": "q", "right": False, "distance": "1"},
            {"left": "q", "right": "q", "distance": "0"},
        ],
    }
    approximation["loss"] = {
        "kind": "finite_decision_loss",
        "actions": [False],
        "entries": [
            {"truth": False, "action": False, "loss": "1"},
            {"truth": True, "action": False, "loss": "1"},
        ],
    }
    record["freeze"]["contract_sha256"] = contract_sha256(record["contract"])
    return record


class FarIr21DeterminismTests(unittest.TestCase):
    def test_loss_check_order_is_independent_of_hash_seed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "probe.json"
            path.write_text(json.dumps(probe_record()), encoding="utf-8")
            program = (
                "import json, sys\n"
                "from mechanization.far_mechanization.contract_v21 import load_and_validate\n"
                "print(json.dumps([d.code for d in load_and_validate(sys.argv[1]).diagnostics]))\n"
            )
            for seed in ("0", "1", "4", "5", "11", "23"):
                with self.subTest(seed=seed):
                    completed = subprocess.run(
                        [sys.executable, "-c", program, str(path)],
                        cwd=ROOT,
                        env={**os.environ, "PYTHONHASHSEED": seed},
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    self.assertEqual(json.loads(completed.stdout), EXPECTED)


if __name__ == "__main__":
    unittest.main()
