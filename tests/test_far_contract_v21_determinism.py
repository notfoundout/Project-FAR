"""The far-ir/2.1 diagnostic sequence is normative, so it must not depend on hash randomization.

The executed W5 verifier (``contract_v21``, frozen by the W5 manifest) iterates required-behavior
values as a Python set in the loss checks, so a record with one behavior value outside the metric
and another whose loss differs from the metric reports the two codes in an order that varies with
PYTHONHASHSEED. Errata 1 fixes first-occurrence order and ``contract_v21_errata1`` implements it.
The expected sequence below is derived by hand from that rule: behavior `false` (first row) has a
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
SEEDS = ("0", "1", "4", "5", "11", "23")


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
    def sequences(self, module: str) -> dict[str, list[str]]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "probe.json"
            path.write_text(json.dumps(probe_record()), encoding="utf-8")
            program = (
                "import json, sys\n"
                f"from mechanization.far_mechanization.{module} import load_and_validate\n"
                "print(json.dumps([d.code for d in load_and_validate(sys.argv[1]).diagnostics]))\n"
            )
            results = {}
            for seed in SEEDS:
                completed = subprocess.run(
                    [sys.executable, "-c", program, str(path)],
                    cwd=ROOT,
                    env={**os.environ, "PYTHONHASHSEED": seed},
                    capture_output=True,
                    text=True,
                    check=True,
                )
                results[seed] = json.loads(completed.stdout)
            return results

    def test_loss_check_order_is_independent_of_hash_seed(self) -> None:
        for seed, codes in self.sequences("contract_v21_errata1").items():
            with self.subTest(seed=seed):
                self.assertEqual(codes, EXPECTED)

    def test_executed_verifier_order_depends_on_hash_seed(self) -> None:
        """The defect the errata corrects is real in the frozen bytes, which stay unmodified."""
        observed = {tuple(codes) for codes in self.sequences("contract_v21").values()}
        self.assertEqual(observed, {tuple(EXPECTED), tuple(reversed(EXPECTED))})

if __name__ == "__main__":
    unittest.main()
