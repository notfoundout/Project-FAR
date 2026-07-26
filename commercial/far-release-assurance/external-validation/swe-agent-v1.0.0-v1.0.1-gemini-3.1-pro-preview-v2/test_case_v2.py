from __future__ import annotations

import copy
import inspect
import json
import unittest
from pathlib import Path

import access_probe_v2
import case_tools

ROOT = Path(__file__).resolve().parents[4]
WORKFLOW = ROOT / ".github/workflows/far-swe-agent-execution-v2.yml"
CASE_DIR = Path(__file__).resolve().parent


class CaseV2ContractTests(unittest.TestCase):
    def test_preregistration_or_access_freeze_is_valid(self) -> None:
        manifest = case_tools.validate_repository(require_frozen=False)
        self.assertIn(manifest["status"], {case_tools.PENDING, case_tools.FROZEN})
        self.assertEqual(
            manifest["frozen_inputs"]["model"],
            "gemini/gemini-3.1-pro-preview",
        )
        gate = manifest["provider_access_gate"]
        if manifest["status"] == case_tools.PENDING:
            self.assertIsNone(gate["attestation_sha256"])
        else:
            self.assertIsInstance(gate["attestation_sha256"], str)
            self.assertTrue(gate["attestation_sha256"])
            self.assertIsNotNone(case_tools.validate_attestation(manifest, required=True))

    def test_new_case_has_a_fresh_four_run_matrix(self) -> None:
        runs = case_tools.load_manifest()["execution_requirements"]["runs"]
        self.assertEqual(
            [(item["release"], item["repetition"]) for item in runs],
            [
                ("v1.0.0", 1),
                ("v1.0.0", 2),
                ("v1.0.1", 1),
                ("v1.0.1", 2),
            ],
        )
        self.assertFalse((CASE_DIR / "execution-output").exists())

    def test_prior_blocked_case_is_preserved_and_not_reused(self) -> None:
        manifest = case_tools.load_manifest()
        old_dir = (CASE_DIR / manifest["supersedes_case"]["path"]).resolve()
        old_manifest = json.loads((old_dir / "manifest.json").read_text())
        self.assertEqual(old_manifest["case_id"], "swe-agent-v1.0.0-v1.0.1")
        self.assertEqual(
            old_manifest["frozen_inputs"]["model"], "gemini/gemini-2.5-pro"
        )
        self.assertEqual(manifest["supersedes_case"]["disposition"], "BLOCKED")
        self.assertTrue(
            manifest["comparison_design"]["cross_case_results_must_not_be_pooled"]
        )

    def test_agent_configuration_is_hash_frozen(self) -> None:
        manifest = case_tools.load_manifest()
        config = (CASE_DIR / "agent-config.yaml").read_text()
        self.assertIn("name: gemini/gemini-3.1-pro-preview", config)
        self.assertNotIn("name: gemini/gemini-2.5-pro", config)
        self.assertEqual(
            case_tools.sha256_file(CASE_DIR / "agent-config.yaml"),
            manifest["frozen_inputs"]["agent_config_sha256"],
        )

    def test_shared_controller_is_blob_locked(self) -> None:
        case_tools.verify_shared_implementation()

    def test_access_probe_is_nonbenchmark_and_does_not_read_task(self) -> None:
        source = inspect.getsource(access_probe_v2.access_probe)
        source += inspect.getsource(access_probe_v2.base_failure)
        self.assertNotIn("TASK_PATH", source)
        self.assertIn("benchmark_task_data_accessed", source)
        self.assertIn("benchmark_outcomes_accessed", source)
        gate = case_tools.load_manifest()["provider_access_gate"]
        self.assertEqual(
            case_tools.sha256_bytes(gate["probe_prompt"].encode()),
            gate["probe_prompt_sha256"],
        )
        self.assertEqual(gate["required_exact_response"], "FAR_ACCESS_OK")
        self.assertEqual(
            gate["probe_request_contract"], access_probe_v2.REQUEST_CONTRACT
        )

    def test_planning_never_reads_provider_secret(self) -> None:
        source = inspect.getsource(case_tools.plan)
        source += inspect.getsource(case_tools.build_plan)
        self.assertNotIn("GEMINI_API_KEY", source)
        manifest = case_tools.load_manifest()
        plan = case_tools.build_plan(manifest, case_tools.read_json(case_tools.LOCK_PATH))
        self.assertEqual(plan["model"], "gemini/gemini-3.1-pro-preview")
        self.assertEqual(len(plan["runs"]), 4)
        self.assertTrue(all(item["state"] == "pending" for item in plan["runs"]))
        self.assertTrue(all(item["outcomes_accessible"] is False for item in plan["runs"]))

    def test_frozen_manifest_requires_attestation_binding(self) -> None:
        manifest = copy.deepcopy(case_tools.load_manifest())
        manifest["status"] = case_tools.FROZEN
        with self.assertRaisesRegex(SystemExit, "attestation"):
            case_tools.validate_manifest(manifest)
        gate = manifest["provider_access_gate"]
        gate["attestation_path"] = "access-freeze/provider-access-attestation.json"
        gate["attestation_sha256"] = "a" * 64
        gate["verified_at"] = "2026-07-26T00:00:00+00:00"
        case_tools.validate_manifest(manifest)


class WorkflowV2ContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = WORKFLOW.read_text()

    def test_workflow_is_manual_and_uses_distinct_v2_artifacts(self) -> None:
        self.assertIn("workflow_dispatch:", self.text)
        self.assertIn("far-swe-agent-v2-execute-", self.text)
        self.assertNotIn('startswith("far-swe-agent-execute-")', self.text)

    def test_exact_confirmation_gates_are_present(self) -> None:
        self.assertIn("PROBE-FAR-GEMINI-3-1-PRO-PREVIEW", self.text)
        self.assertIn("PLAN-FAR-GEMINI-3-1-PRO-PREVIEW-V2", self.text)
        self.assertIn(
            "EXECUTE-FAR-GEMINI-3-1-PRO-PREVIEW-V2-NEXT-RUN", self.text
        )

    def test_secret_is_injected_only_for_probe_and_model_call(self) -> None:
        binding = "GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}"
        self.assertEqual(self.text.count(binding), 2)
        plan_start = self.text.index("- name: Generate frozen v2 execution plan")
        plan_end = self.text.index(
            "- name: Restore latest v2 validated execution state"
        )
        self.assertNotIn("GEMINI_API_KEY", self.text[plan_start:plan_end])
        execute_start = self.text.index(
            "- name: Execute exactly one next frozen v2 run"
        )
        self.assertIn("GEMINI_API_KEY", self.text[execute_start:])

    def test_access_probe_creates_reviewable_freeze_pr(self) -> None:
        self.assertIn("python access_probe_v2.py", self.text)
        self.assertNotIn("python case_tools.py access-probe", self.text)
        self.assertIn("python case_tools.py finalize-access-freeze", self.text)
        self.assertIn("gh pr create", self.text)
        self.assertIn("pull-requests: write", self.text)

    def test_access_probe_regressions_run_before_and_after_probe(self) -> None:
        command = "python -m unittest -v test_case_v2.py test_access_probe_v2.py"
        self.assertEqual(self.text.count(command), 2)

    def test_execution_restores_before_resolving_or_calling_model(self) -> None:
        restore = self.text.index(
            "- name: Restore latest v2 validated execution state"
        )
        resolve = self.text.index("- name: Resolve next frozen v2 SWE-agent release")
        execute = self.text.index("- name: Execute exactly one next frozen v2 run")
        self.assertLess(restore, resolve)
        self.assertLess(resolve, execute)


if __name__ == "__main__":
    unittest.main()
