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
        )
        for mutation in cases:
            with self.subTest(mutation=mutation):
                altered = json.loads(json.dumps(data))
                mutation(altered)
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "task.json"
                    path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                    with self.assertRaises(module.DesignError):
                        module.verify_task_identity_contract(path)

    def test_seed_commitment_is_exact_and_preoutcome(self) -> None:
        data = json.loads((DIR / "bootstrap-seed-commitment-contract-v1.0.json").read_text(encoding="utf-8"))
        cases = (
            lambda d: d["rng_contract"].__setitem__("seed_hex", "0" * 64),
            lambda d: d["authority"].__setitem__("outcome_exposure_status", "partial"),
            lambda d: d["derivation"].__setitem__("outcome_or_grade_inputs_permitted", True),
            lambda d: d["timing"].__setitem__("must_precede_any_pilot_or_confirmatory_outcome_reveal", False),
        )
        for mutation in cases:
            with self.subTest(mutation=mutation):
                altered = json.loads(json.dumps(data))
                mutation(altered)
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "seed.json"
                    path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                    with self.assertRaises(module.DesignError):
                        module.verify_seed_contract(path)

    def test_seed_derivation_recomputes_from_governed_preoutcome_inputs(self) -> None:
        data = json.loads((DIR / "bootstrap-seed-commitment-contract-v1.0.json").read_text(encoding="utf-8"))
        payload = data["derivation"]["canonical_payload"]
        seed = data["rng_contract"]["seed_hex"]
        self.assertEqual(module.hashlib.sha256(payload.encode("utf-8")).hexdigest(), seed)
        self.assertEqual(len(bytes.fromhex(seed)), 32)


if __name__ == "__main__":
    unittest.main()