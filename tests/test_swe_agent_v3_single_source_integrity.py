from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "research/external-validation/swe-agent-v3"
STRATA = ["bug_fix", "test_failure", "behavioral_regression", "API_or_contract_change", "multi_file_change"]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def canonical_descriptor_bytes(record: dict) -> bytes:
    descriptor = {
        "algorithm_id": "far-swe-v3-task-bundle-root-v2",
        "repository_provider": record["repository_provider"],
        "repository_provider_id": record["repository_provider_id"],
        "canonical_repository_url": record["canonical_repository_url"],
        "repository_commit_sha": record["repository_commit_sha"],
        "task_payload_sha256": record["task_payload_sha256"],
        "task_payload_bytes": record["task_payload_bytes"],
    }
    return json.dumps(descriptor, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def build_manifest_and_ledger() -> tuple[list[dict], list[dict]]:
    manifest: list[dict] = []
    ledger: list[dict] = []
    for i in range(25):
        repo_index = i % 5 + 1
        identity = {
            "blind_task_id": f"TASK-{i + 1:06d}",
            "repository_blind_id": f"REPO-{repo_index:04d}",
            "task_bundle_root_sha256": "",
            "repository_provider": "github.com",
            "repository_provider_id": 1000 + repo_index,
            "canonical_repository_url": f"https://github.com/example/repo{repo_index}",
            "repository_commit_sha": f"{repo_index:040x}",
            "task_payload_sha256": f"{i + 1:064x}",
            "task_payload_bytes": 100 + i,
            "strata": [STRATA[i % len(STRATA)]],
            "github_fork_source_repository_id": None,
            "contains_project_far_treatment_material": False,
        }
        identity["task_bundle_root_sha256"] = hashlib.sha256(canonical_descriptor_bytes(identity)).hexdigest()
        ledger.append(identity)
        manifest.append({
            "blind_task_id": identity["blind_task_id"],
            "repository_blind_id": identity["repository_blind_id"],
            "task_bundle_root_sha256": identity["task_bundle_root_sha256"],
            "strata": identity["strata"],
        })
    return manifest, ledger


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
            "verify_review_closure.py": (
                "SEED_BLOB", "TASK_BLOB", "CAPSULE_BLOB", "GATE_BLOB", "RECORD_SCHEMA_DIGEST",
                "TASK_BUNDLE_ROOT_DIGEST", "REPOSITORY_IDENTITY_DIGEST", "CAPSULE_REL", "GATE_REL",
            ),
            "verify_amendment_v1_1.py": (
                "AMEND_SHA", "README_SHA", "REPL_DIGEST", "ARITH_DIGEST", "PREREG_BLOB", "PLAN_BLOB",
            ),
        }
        for filename, tokens in forbidden.items():
            for token in tokens:
                self.assertNotIn(token, sources[filename], f"mutable/current duplicate identity survived: {filename}:{token}")

    def test_historical_archive_is_self_contained_and_not_live_authority(self) -> None:
        verifier = (DIR / "verify_amendment_v1_1.py").read_text(encoding="utf-8")
        for token in ("import subprocess", "git fetch --unshallow", "rev-parse", "cat-file", "merge-base", "--is-ancestor"):
            self.assertNotIn(token, verifier)
        authority = json.loads((DIR / "historical-authority-v1.0.json").read_text(encoding="utf-8"))
        self.assertEqual(authority["schema_version"], "1.1")
        self.assertRegex(authority["claimed_historical_design_head"], r"^[0-9a-f]{40}$")
        self.assertEqual(authority["artifact_status"], "Archive")
        self.assertEqual(authority["authority_status"], "archival_context_not_live_authority")
        self.assertEqual(authority["provenance_status"], "not_self_proving")
        self.assertFalse(authority["current_design_authority"])
        self.assertFalse(authority["execution_authorized"])
        self.assertEqual(len(authority["snapshots"]), 2)
        for entry in authority["snapshots"]:
            self.assertRegex(entry["archived_git_blob_sha1"], r"^[0-9a-f]{40}$")
            snapshot = ROOT / entry["path"]
            self.assertEqual(git_blob_sha1(snapshot.read_bytes()), entry["archived_git_blob_sha1"])
            self.assertNotIn(entry["archived_git_blob_sha1"], verifier)

    def test_every_governed_final_contract_is_in_design_manifest(self) -> None:
        manifest = json.loads((DIR / "design-manifest-v1.0.json").read_text(encoding="utf-8"))
        paths = {entry["path"] for entry in manifest["artifacts"]}
        required = {
            "research/external-validation/swe-agent-v3/bootstrap-seed-commitment-contract-v1.0.json",
            "research/external-validation/swe-agent-v3/critical-harm-thresholds-v1.0.json",
            "research/external-validation/swe-agent-v3/historical-authority-v1.0.json",
            "research/external-validation/swe-agent-v3/historical-base-83c951/preregistration-v1.0.json",
            "research/external-validation/swe-agent-v3/historical-base-83c951/evidence-and-analysis-plan-v1.0.md",
            "research/external-validation/swe-agent-v3/task-manifest-contract-v1.0.json",
        }
        self.assertTrue(required.issubset(paths))

    def test_seed_is_direct_commitment_not_mutable_launch_derivation(self) -> None:
        data = json.loads((DIR / "bootstrap-seed-commitment-contract-v1.0.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "1.1")
        self.assertEqual(data["commitment"]["method"], "direct_precommitted_value")
        self.assertFalse(data["commitment"]["artifact_inputs_permitted"])
        self.assertFalse(data["commitment"]["mutable_launch_inputs_permitted"])
        self.assertFalse(data["commitment"]["task_identity_inputs_permitted"])
        self.assertFalse(data["commitment"]["outcome_or_grade_inputs_permitted"])
        self.assertRegex(data["rng_contract"]["seed_hex"], r"^[0-9a-f]{64}$")
        source = (DIR / "verify_review_closure.py").read_text(encoding="utf-8")
        self.assertNotIn("treatment_capsule_git_blob_sha1", source)
        self.assertNotIn("execution_gate_git_blob_sha1", source)
        self.assertIn(data["rng_contract"]["seed_hex"], source)

    def test_schema_1_6_identity_strata_and_sealed_ledger_contract_is_preserved(self) -> None:
        data = json.loads((DIR / "task-manifest-contract-v1.0.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "1.6")
        self.assertFalse(data["execution_authorized"])
        self.assertEqual(data["repository_identity_contract"]["supported_provider"], "github.com only")
        self.assertIn("positive JSON integer", data["task_bundle_root_contract"]["descriptor_values"]["repository_provider_id"])
        self.assertTrue(data["record_schema"]["blind_task_id"]["unique"])
        self.assertTrue(data["record_schema"]["task_bundle_root_sha256"]["unique"])
        self.assertEqual(data["record_schema"]["strata"]["allowed_values_in_canonical_order"], STRATA)
        self.assertFalse(data["order_contract"]["runtime_sorting_permitted"])
        ledger = data["sealed_identity_ledger_contract"]
        self.assertEqual(ledger["status"], "uninstantiated")
        self.assertFalse(ledger["execution_authorized"])
        self.assertIn("exactly one ledger record for every task-manifest record", ledger["array_binding_rule"])
        self.assertIn("committed before any sacrificial pilot or confirmatory execution", ledger["freeze_timing"])
        self.assertIn("agent and capsule authors", ledger["access_control"])
        prohibited = data["prohibited_repository_contract"]
        self.assertEqual(prohibited["project_far_repository_provider_id"], 1283452680)
        self.assertTrue(prohibited["reject_exact_project_far_repository"])
        self.assertTrue(prohibited["reject_github_fork_source_project_far"])
        self.assertTrue(prohibited["require_project_far_treatment_material_absent"])
        self.assertIn("github_fork_source_repository_id", ledger["record_required_keys_exactly"])
        self.assertIn("contains_project_far_treatment_material", ledger["record_required_keys_exactly"])

    def test_instantiated_manifest_enforces_unique_roots_canonical_strata_and_coverage(self) -> None:
        module = load_module("single_source_review_closure_records", DIR / "verify_review_closure.py")
        records = [
            {
                "blind_task_id": f"TASK-{i + 1:06d}",
                "repository_blind_id": f"REPO-{i + 1:04d}",
                "task_bundle_root_sha256": f"{i + 1:064x}",
                "strata": [label],
            }
            for i, label in enumerate(STRATA)
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
            self.assertEqual(len(module.validate_instantiated_task_manifest(path)), 5)
            cases = []
            duplicate_root = json.loads(json.dumps(records)); duplicate_root[1]["task_bundle_root_sha256"] = duplicate_root[0]["task_bundle_root_sha256"]; cases.append(duplicate_root)
            missing_stratum = json.loads(json.dumps(records)); missing_stratum[-1]["strata"] = [STRATA[0]]; cases.append(missing_stratum)
            bad_order = json.loads(json.dumps(records)); bad_order[0]["strata"] = [STRATA[1], STRATA[0]]; cases.append(bad_order)
            duplicate_stratum = json.loads(json.dumps(records)); duplicate_stratum[0]["strata"] = [STRATA[0], STRATA[0]]; cases.append(duplicate_stratum)
            for altered in cases:
                path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                with self.assertRaises(module.DesignError):
                    module.validate_instantiated_task_manifest(path)

    def test_sealed_identity_ledger_enforces_roots_repository_population_and_cap(self) -> None:
        module = load_module("single_source_review_closure_ledger", DIR / "verify_review_closure.py")
        manifest, ledger = build_manifest_and_ledger()
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            ledger_path = Path(tmp) / "ledger.json"

            def write(current_manifest: list[dict], current_ledger: list[dict]) -> None:
                manifest_path.write_text(json.dumps(current_manifest, indent=2) + "\n", encoding="utf-8")
                ledger_path.write_text(json.dumps(current_ledger, indent=2) + "\n", encoding="utf-8")

            write(manifest, ledger)
            self.assertEqual(len(module.validate_instantiated_identity_ledger(manifest_path, ledger_path)), 25)

            bad_root = json.loads(json.dumps(ledger)); bad_root[0]["task_payload_bytes"] += 1
            write(manifest, bad_root)
            with self.assertRaises(module.DesignError):
                module.validate_instantiated_identity_ledger(manifest_path, ledger_path)

            alias_split = json.loads(json.dumps(ledger)); alias_split[5]["repository_blind_id"] = "REPO-9999"
            alias_manifest = json.loads(json.dumps(manifest)); alias_manifest[5]["repository_blind_id"] = "REPO-9999"
            write(alias_manifest, alias_split)
            with self.assertRaises(module.DesignError):
                module.validate_instantiated_identity_ledger(manifest_path, ledger_path)

            cap_evasion = json.loads(json.dumps(ledger))
            cap_manifest = json.loads(json.dumps(manifest))
            # Move one task from repo 2 to repo 1 and recompute its authoritative root.
            moved = cap_evasion[6]
            moved["repository_blind_id"] = "REPO-0001"
            moved["repository_provider_id"] = 1001
            moved["canonical_repository_url"] = "https://github.com/example/repo1"
            moved["repository_commit_sha"] = f"{1:040x}"
            moved["task_bundle_root_sha256"] = hashlib.sha256(canonical_descriptor_bytes(moved)).hexdigest()
            cap_manifest[6]["repository_blind_id"] = moved["repository_blind_id"]
            cap_manifest[6]["task_bundle_root_sha256"] = moved["task_bundle_root_sha256"]
            write(cap_manifest, cap_evasion)
            with self.assertRaises(module.DesignError):
                module.validate_instantiated_identity_ledger(manifest_path, ledger_path)

    def test_sealed_identity_ledger_rejects_project_far_repository_forks_treatment_and_url_aliases(self) -> None:
        module = load_module("single_source_review_closure_prohibitions", DIR / "verify_review_closure.py")
        manifest, ledger = build_manifest_and_ledger()
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            ledger_path = Path(tmp) / "ledger.json"

            def write(current_manifest: list[dict], current_ledger: list[dict]) -> None:
                manifest_path.write_text(json.dumps(current_manifest, indent=2) + "\n", encoding="utf-8")
                ledger_path.write_text(json.dumps(current_ledger, indent=2) + "\n", encoding="utf-8")

            def bind_root(current_manifest: list[dict], current_ledger: list[dict], index: int) -> None:
                current_ledger[index]["task_bundle_root_sha256"] = hashlib.sha256(canonical_descriptor_bytes(current_ledger[index])).hexdigest()
                current_manifest[index]["task_bundle_root_sha256"] = current_ledger[index]["task_bundle_root_sha256"]

            cases: list[tuple[list[dict], list[dict]]] = []

            exact_manifest = json.loads(json.dumps(manifest)); exact_ledger = json.loads(json.dumps(ledger))
            exact_ledger[0]["repository_provider_id"] = 1283452680
            bind_root(exact_manifest, exact_ledger, 0)
            cases.append((exact_manifest, exact_ledger))

            fork_manifest = json.loads(json.dumps(manifest)); fork_ledger = json.loads(json.dumps(ledger))
            fork_ledger[0]["github_fork_source_repository_id"] = 1283452680
            cases.append((fork_manifest, fork_ledger))

            treatment_manifest = json.loads(json.dumps(manifest)); treatment_ledger = json.loads(json.dumps(ledger))
            treatment_ledger[0]["contains_project_far_treatment_material"] = True
            cases.append((treatment_manifest, treatment_ledger))

            alias_manifest = json.loads(json.dumps(manifest)); alias_ledger = json.loads(json.dumps(ledger))
            alias_ledger[1]["canonical_repository_url"] = alias_ledger[0]["canonical_repository_url"]
            bind_root(alias_manifest, alias_ledger, 1)
            cases.append((alias_manifest, alias_ledger))

            for current_manifest, current_ledger in cases:
                write(current_manifest, current_ledger)
                with self.assertRaises(module.DesignError):
                    module.validate_instantiated_identity_ledger(manifest_path, ledger_path)

    def test_semantic_weakening_fails_without_repinning_verifier(self) -> None:
        module = load_module("single_source_review_closure", DIR / "verify_review_closure.py")
        data = json.loads((DIR / "task-manifest-contract-v1.0.json").read_text(encoding="utf-8"))
        mutations = (
            lambda d: d.__setitem__("schema_version", "1.4"),
            lambda d: d["record_schema"]["task_bundle_root_sha256"].__setitem__("unique", False),
            lambda d: d["record_schema"]["strata"].__setitem__("allowed_values_in_canonical_order", STRATA[:-1]),
            lambda d: d["task_bundle_root_contract"]["descriptor_values"].__setitem__("repository_provider_id", "owner/name string"),
            lambda d: d["sealed_identity_ledger_contract"].__setitem__("access_control", "agent may inspect identities"),
            lambda d: d["order_contract"].__setitem__("runtime_sorting_permitted", True),
            lambda d: d["prohibited_repository_contract"].__setitem__("project_far_repository_provider_id", 1),
            lambda d: d["prohibited_repository_contract"].__setitem__("require_project_far_treatment_material_absent", False),
        )
        for mutation in mutations:
            altered = json.loads(json.dumps(data)); mutation(altered)
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "task.json"
                path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                with self.assertRaises(module.DesignError):
                    module.verify_task_identity_contract(path)

    def test_critical_harm_weakening_fails_semantically(self) -> None:
        module = load_module("single_source_review_closure_harm", DIR / "verify_review_closure.py")
        data = json.loads((DIR / "critical-harm-thresholds-v1.0.json").read_text(encoding="utf-8"))
        mutations = (
            lambda d: d["rate_harms"]["invalid_run_rate"].__setitem__("critical_threshold", {"numerator": 1, "denominator": 5}),
            lambda d: d["rate_harms"]["regression_introduction_rate"].__setitem__("slot_denominator", "complete cases only"),
            lambda d: d["rate_harms"]["regression_introduction_rate"].__setitem__("slot_numerator", "operator-attributed regressions only"),
            lambda d: d["zero_tolerance_harms"]["hidden_task_leakage"].__setitem__("trigger_rule", "slot_numerator > 1"),
            lambda d: d["zero_tolerance_harms"]["evidence_loss"].__setitem__("slot_denominator", "valid slots only"),
            lambda d: d.__setitem__("versioning_rule", "thresholds may change after exposure"),
        )
        for mutation in mutations:
            altered = json.loads(json.dumps(data)); mutation(altered)
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "harm.json"
                path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                with self.assertRaises(module.DesignError):
                    module.verify_critical_harm_contract(path)


if __name__ == "__main__":
    unittest.main()
