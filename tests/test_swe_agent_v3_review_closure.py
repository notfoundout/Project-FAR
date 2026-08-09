from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "research/external-validation/swe-agent-v3"
PATH = DIR / "verify_review_closure.py"
SPEC = importlib.util.spec_from_file_location("swe_v3_review_closure", PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class ReviewClosureTests(unittest.TestCase):
    def test_canonical_review_closure_passes(self) -> None:
        module.verify()

    def test_complete_task_identity_contracts_are_semantically_locked(self) -> None:
        data = json.loads((DIR / "task-manifest-contract-v1.0.json").read_text(encoding="utf-8"))
        cases = (
            lambda d: d["record_schema"]["repository_blind_id"].__setitem__("unicode_permitted", True),
            lambda d: d["task_bundle_root_contract"]["descriptor_values"].__setitem__("repository_provider_id", "owner/name"),
            lambda d: d["repository_identity_contract"].__setitem__("minimum_repository_count_basis", "count URL strings"),
            lambda d: d["record_schema"]["task_bundle_root_sha256"].__setitem__("unique", False),
            lambda d: d["record_schema"]["strata"].__setitem__("allowed_values_in_canonical_order", ["bug_fix"]),
            lambda d: d["sealed_identity_ledger_contract"].__setitem__("access_control", "public to agent"),
        )
        for mutation in cases:
            with self.subTest(mutation=mutation):
                altered = json.loads(json.dumps(data)); mutation(altered)
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "task.json"
                    path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                    with self.assertRaises(module.DesignError):
                        module.verify_task_identity_contract(path)

    def test_seed_commitment_semantics_are_direct_and_preoutcome(self) -> None:
        data = json.loads((DIR / "bootstrap-seed-commitment-contract-v1.0.json").read_text(encoding="utf-8"))
        cases = (
            lambda d: d["authority"].__setitem__("outcome_exposure_status", "partial"),
            lambda d: d["authority"].__setitem__("execution_authorized", 0),
            lambda d: d["commitment"].__setitem__("artifact_inputs_permitted", True),
            lambda d: d["commitment"].__setitem__("mutable_launch_inputs_permitted", True),
            lambda d: d["timing"].__setitem__("must_precede_any_pilot_or_confirmatory_outcome_reveal", False),
        )
        for mutation in cases:
            with self.subTest(mutation=mutation):
                altered = json.loads(json.dumps(data)); mutation(altered)
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "seed.json"
                    path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                    with self.assertRaises(module.DesignError):
                        module.verify_seed_contract(path)

    def test_seed_value_is_well_formed_and_semantically_frozen(self) -> None:
        data = json.loads((DIR / "bootstrap-seed-commitment-contract-v1.0.json").read_text(encoding="utf-8"))
        self.assertEqual(data["commitment"]["method"], "direct_precommitted_value")
        self.assertFalse(data["commitment"]["artifact_inputs_permitted"])
        self.assertFalse(data["commitment"]["mutable_launch_inputs_permitted"])
        self.assertRegex(data["rng_contract"]["seed_hex"], r"^[0-9a-f]{64}$")
        self.assertEqual(len(bytes.fromhex(data["rng_contract"]["seed_hex"])), 32)
        source = (DIR / "verify_review_closure.py").read_text(encoding="utf-8")
        self.assertIn(data["rng_contract"]["seed_hex"], source)
        altered = json.loads(json.dumps(data))
        altered["rng_contract"]["seed_hex"] = "0" * 64
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "seed.json"
            path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(module.DesignError):
                module.verify_seed_contract(path)

    def test_critical_harm_contract_is_exact_and_preexecution(self) -> None:
        data = json.loads((DIR / "critical-harm-thresholds-v1.0.json").read_text(encoding="utf-8"))
        cases = (
            lambda d: d["zero_tolerance_harms"]["hidden_task_leakage"].__setitem__("trigger_rule", "slot_numerator > 1"),
            lambda d: d["zero_tolerance_harms"]["evidence_loss"].__setitem__("slot_denominator", "valid slots only"),
            lambda d: d["rate_harms"]["invalid_run_rate"].__setitem__("critical_threshold", {"numerator": 1, "denominator": 5}),
            lambda d: d["rate_harms"]["regression_introduction_rate"].__setitem__("slot_denominator", "complete cases only"),
            lambda d: d["rate_harms"]["regression_introduction_rate"].__setitem__("slot_numerator", "operator-attributed only"),
            lambda d: d.__setitem__("versioning_rule", "may change after outcomes"),
        )
        for mutation in cases:
            with self.subTest(mutation=mutation):
                altered = json.loads(json.dumps(data)); mutation(altered)
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "harm.json"
                    path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                    with self.assertRaises(module.DesignError):
                        module.verify_critical_harm_contract(path)

    def test_launch_gate_requires_complete_frozen_identity_binding(self) -> None:
        data = json.loads((DIR / "execution-gate-v1.0.json").read_text(encoding="utf-8"))
        cases = (
            lambda d: d["launch_record_required_bindings"].remove("sealed_identity_ledger_git_blob_sha1"),
            lambda d: d["launch_record_required_bindings"].remove("bootstrap_seed_commitment_git_blob_sha1"),
            lambda d: d["pilot_gates"].pop("critical_harm_thresholds_frozen_and_verified"),
            lambda d: d["gates"].__setitem__("manual_launch_authorization_recorded", True),
            lambda d: d.__setitem__("confirmatory_execution_authorized", 0),
        )
        for mutation in cases:
            altered = json.loads(json.dumps(data)); mutation(altered)
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "gate.json"
                path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                with self.assertRaises(module.DesignError):
                    module.verify_gate_closed(path)


if __name__ == "__main__":
    unittest.main()
