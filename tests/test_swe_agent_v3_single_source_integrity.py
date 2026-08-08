from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "research/external-validation/swe-agent-v3"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class SingleSourceIntegrityTests(unittest.TestCase):
    def test_mutable_current_identity_mirrors_are_absent(self) -> None:
        sources = {
            name: (DIR / name).read_text(encoding="utf-8")
            for name in (
                "verify_integrity.py",
                "verify_design.py",
                "verify_review_closure.py",
                "verify_amendment_v1_1.py",
            )
        }
        forbidden = {
            "verify_integrity.py": ("EXPECTED_MANIFEST_GIT_BLOB_SHA1",),
            "verify_design.py": ("ARTIFACT_BLOBS", "PILOT_DIGEST", "FREEZE_SEQUENCE_DIGEST", "INVALIDATION_RULES_DIGEST"),
            "verify_review_closure.py": ("SEED_BLOB", "TASK_BLOB", "CAPSULE_BLOB", "GATE_BLOB", "RECORD_SCHEMA_DIGEST", "TASK_BUNDLE_ROOT_DIGEST", "REPOSITORY_IDENTITY_DIGEST"),
            "verify_amendment_v1_1.py": ("AMEND_SHA", "README_SHA", "REPL_DIGEST", "ARITH_DIGEST"),
        }
        for filename, tokens in forbidden.items():
            for token in tokens:
                self.assertNotIn(token, sources[filename], f"mutable current mirror survived: {filename}:{token}")

    def test_historical_pins_remain_but_ancestry_assumption_is_gone(self) -> None:
        source = (DIR / "verify_amendment_v1_1.py").read_text(encoding="utf-8")
        self.assertIn('BASE_HEAD = "83c951aca9be6a09a4517044ae531a3ed1bcc9a9"', source)
        self.assertIn('PREREG_BLOB = "7147f6814f76eb0f73fd0741b17b2501e38e6f57"', source)
        self.assertIn('PLAN_BLOB = "15b352d54a524d9caf827018b608028c004f8f13"', source)
        self.assertNotIn("merge-base", source)
        self.assertNotIn("--is-ancestor", source)
        self.assertIn("git fetch --unshallow", source)

    def test_schema_1_3_identity_contract_is_preserved(self) -> None:
        data = json.loads((DIR / "task-manifest-contract-v1.0.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "1.3")
        self.assertFalse(data["execution_authorized"])
        self.assertEqual(data["repository_identity_contract"]["supported_provider"], "github.com only")
        self.assertIn("positive JSON integer", data["task_bundle_root_contract"]["descriptor_values"]["repository_provider_id"])
        self.assertTrue(data["record_schema"]["blind_task_id"]["unique"])
        self.assertTrue(data["record_schema"]["task_bundle_root_sha256"]["unique"])
        self.assertFalse(data["order_contract"]["runtime_sorting_permitted"])

    def test_semantic_weakening_fails_without_repinning_verifier(self) -> None:
        module = load_module("single_source_review_closure", DIR / "verify_review_closure.py")
        data = json.loads((DIR / "task-manifest-contract-v1.0.json").read_text(encoding="utf-8"))
        mutations = (
            lambda d: d.__setitem__("schema_version", "1.2"),
            lambda d: d["record_schema"]["task_bundle_root_sha256"].__setitem__("unique", False),
            lambda d: d["task_bundle_root_contract"]["descriptor_values"].__setitem__("repository_provider_id", "owner/name string"),
            lambda d: d["order_contract"].__setitem__("runtime_sorting_permitted", True),
        )
        for mutation in mutations:
            altered = json.loads(json.dumps(data))
            mutation(altered)
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "task.json"
                path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                with self.assertRaises(module.DesignError):
                    module.verify_task_identity_contract(path)


if __name__ == "__main__":
    unittest.main()
