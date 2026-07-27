from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("investigation_gate", ROOT / "tools/check_investigation_execution.py")
gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(gate)


class InvestigationExecutionGateTests(unittest.TestCase):
    def setUp(self):
        self.source = yaml.safe_load((ROOT / "research/validation/executions/VI-002.execution.yaml").read_text())

    def validate(self, payload, canonical_manifests=None):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            executions = root / "research/validation/executions"
            executions.mkdir(parents=True, exist_ok=True)
            for step in payload.get("required_steps", []):
                for evidence in step.get("evidence", []):
                    declared = evidence.get("path")
                    if isinstance(declared, str) and not Path(declared).is_absolute() and ".." not in Path(declared).parts:
                        artifact = root / declared
                        artifact.parent.mkdir(parents=True, exist_ok=True)
                        artifact.write_text("evidence\n")
            path = executions / f"{payload.get('investigation', 'test')}.execution.yaml"
            path.write_text(yaml.safe_dump(payload), encoding="utf-8")
            for ident, result in (canonical_manifests or {}).items():
                manifest_path = executions / f"{ident}.execution.yaml"
                manifest_path.write_text(
                    yaml.safe_dump(
                        {
                            "investigation": ident,
                            "result": result,
                            "required_steps": [
                                {
                                    "id": "x",
                                    "status": "complete",
                                    "evidence": [{"path": "evidence.md"}],
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
            return gate.validate_manifest(path, root)

    def passing_payload(self):
        payload = copy.deepcopy(self.source)
        payload["result"] = "pass"
        for step in payload["required_steps"]:
            step["status"] = "complete"
            step["evidence"] = [{"path": "evidence.md"}]
        payload["upstream_dependencies"] = []
        return payload

    def test_vi002_is_explicitly_non_passing(self):
        self.assertEqual(self.source["result"], "incomplete")
        self.assertTrue(any(step["status"] == "not_executed" for step in self.source["required_steps"]))
        self.assertEqual(self.validate(self.source), [])

    def test_pass_rejected_when_a_required_step_is_incomplete(self):
        payload = copy.deepcopy(self.source)
        payload["result"] = "pass"
        self.assertTrue(any("incomplete required steps" in error for error in self.validate(payload)))

    def test_pass_rejected_when_evidence_is_absent(self):
        payload = self.passing_payload()
        payload["required_steps"][0]["evidence"] = []
        self.assertTrue(any("lacking evidence" in error for error in self.validate(payload)))

    def test_pass_rejected_when_required_steps_missing(self):
        payload = self.passing_payload()
        payload.pop("required_steps")
        self.assertTrue(any("non-empty required_steps" in error for error in self.validate(payload)))

    def test_pass_rejected_when_required_steps_empty(self):
        payload = self.passing_payload()
        payload["required_steps"] = []
        self.assertTrue(any("non-empty required_steps" in error for error in self.validate(payload)))

    def test_required_step_id_must_be_non_empty(self):
        payload = self.passing_payload()
        payload["required_steps"][0]["id"] = "  "
        self.assertTrue(any("missing or empty id" in error for error in self.validate(payload)))

    def test_duplicate_required_step_ids_are_rejected(self):
        payload = self.passing_payload()
        payload["required_steps"][1]["id"] = payload["required_steps"][0]["id"]
        self.assertTrue(any("duplicate required step id" in error for error in self.validate(payload)))

    def test_pass_rejected_when_upstream_manifest_is_missing(self):
        payload = self.passing_payload()
        payload["upstream_dependencies"] = [{"id": "VI-999", "status": "passed"}]
        self.assertTrue(any("unresolved upstream" in error for error in self.validate(payload)))

    def test_pass_rejected_when_inline_upstream_status_disagrees_with_canonical_manifest(self):
        payload = self.passing_payload()
        payload["upstream_dependencies"] = [{"id": "VI-001", "status": "passed"}]
        errors = self.validate(payload, {"VI-001": "incomplete"})
        self.assertTrue(any("unresolved upstream" in error for error in errors))

    def test_pass_accepts_canonical_passing_upstream_despite_stale_inline_status(self):
        payload = self.passing_payload()
        payload["upstream_dependencies"] = [{"id": "VI-001", "status": "incomplete"}]
        self.assertEqual(self.validate(payload, {"VI-001": "pass"}), [])

    def test_absolute_evidence_path_is_rejected(self):
        payload = self.passing_payload()
        payload["required_steps"][0]["evidence"] = [{"path": "/etc/passwd"}]
        self.assertTrue(any("within repository root" in error for error in self.validate(payload)))

    def test_parent_traversal_evidence_path_is_rejected(self):
        payload = self.passing_payload()
        payload["required_steps"][0]["evidence"] = [{"path": "../../outside.txt"}]
        self.assertTrue(any("within repository root" in error for error in self.validate(payload)))

    def test_duplicate_investigation_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            executions = root / "research/validation/executions"
            executions.mkdir(parents=True)
            first = {"investigation": "VI-001", "result": "incomplete"}
            second = {"investigation": "VI-001", "result": "pass"}
            (executions / "VI-001.execution.yaml").write_text(yaml.safe_dump(first))
            (executions / "VI-001-shadow.execution.yaml").write_text(yaml.safe_dump(second))
            errors = gate.validate_manifest_registry(root)
            self.assertTrue(any("duplicate execution manifests" in error for error in errors))

    def test_manifest_filename_must_match_investigation_id(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            executions = root / "research/validation/executions"
            executions.mkdir(parents=True)
            (executions / "VI-999.execution.yaml").write_text(
                yaml.safe_dump({"investigation": "VI-001", "result": "pass"})
            )
            errors = gate.validate_manifest_registry(root)
            self.assertTrue(any("does not match canonical filename" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
