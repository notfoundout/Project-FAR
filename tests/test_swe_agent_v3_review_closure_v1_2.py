from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "research/external-validation/swe-agent-v3"
PATH = DIR / "verify_review_closure_v1_2.py"
SPEC = importlib.util.spec_from_file_location("swe_v3_review_closure_v1_2", PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class ReviewClosureV12Tests(unittest.TestCase):
    def _mutated_amendment_fails(self, mutator) -> None:
        data = json.loads((DIR / "review-closure-amendment-v1.2.json").read_text(encoding="utf-8"))
        altered = copy.deepcopy(data)
        mutator(altered)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "amendment.json"
            path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(module.DesignError):
                module.validate(path)

    def test_canonical_closure_passes(self) -> None:
        module.validate()

    def test_historical_authority_is_snapshot_rooted(self) -> None:
        for path, expected_blob in module.HISTORICAL:
            self.assertEqual(module._blob(path), expected_blob)
            self.assertEqual(module._current_blob(path), expected_blob)

    def test_seed_input_binding_is_immutable(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["bootstrap_seed_effective_contract"]["inputs"][1].__setitem__(
                "git_blob_sha1", "0" * 40
            )
        )

    def test_seed_authority_correction_cannot_be_removed(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["bootstrap_seed_effective_contract"].__setitem__(
                "authority_correction", "all other fields remained unchanged"
            )
        )

    def test_task_stratum_is_required_and_root_bound(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"].__setitem__(
                "required_record_keys_exactly",
                ["blind_task_id", "repository_blind_id", "task_bundle_root_sha256"],
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"]["task_bundle_root_extension"].__setitem__(
                "task_stratum_is_root_member", False
            )
        )

    def test_required_stratum_set_is_exact(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["task_manifest_effective_contract"]["task_stratum"].__setitem__(
                "allowed_values_exactly", module.REQUIRED_STRATA[:-1]
            )
        )

    def test_harm_thresholds_are_frozen_and_exact(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["critical_harm_threshold_contract"]["rate_harms"]["invalid_run_rate"].__setitem__(
                "threshold", {"numerator": 1, "denominator": 5}
            )
        )
        self._mutated_amendment_fails(
            lambda d: d["critical_harm_threshold_contract"].__setitem__(
                "missing_harm_evidence_rule", "missing evidence may be ignored"
            )
        )

    def test_execution_and_theory_boundaries_remain_closed(self) -> None:
        self._mutated_amendment_fails(
            lambda d: d["authority"].__setitem__("model_calls_authorized", True)
        )
        self._mutated_amendment_fails(
            lambda d: d["execution_gate_extension"].__setitem__("current_execution_authorized", True)
        )
        self._mutated_amendment_fails(
            lambda d: d.__setitem__(
                "nonclaims",
                [x for x in d["nonclaims"] if "accepted Project FAR theory" not in x],
            )
        )


if __name__ == "__main__":
    unittest.main()
