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

    def validate(self, payload):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for step in payload["required_steps"]:
                for evidence in step.get("evidence", []):
                    artifact = root / evidence["path"]
                    artifact.parent.mkdir(parents=True, exist_ok=True)
                    artifact.write_text("evidence\n")
            path = root / "execution.yaml"
            path.write_text(yaml.safe_dump(payload), encoding="utf-8")
            return gate.validate_manifest(path, root)

    def test_vi002_is_explicitly_non_passing(self):
        self.assertEqual(self.source["result"], "incomplete")
        self.assertTrue(any(step["status"] == "not_executed" for step in self.source["required_steps"]))
        self.assertEqual(self.validate(self.source), [])

    def test_pass_rejected_when_a_required_step_is_incomplete(self):
        payload = copy.deepcopy(self.source)
        payload["result"] = "pass"
        self.assertTrue(any("incomplete required steps" in error for error in self.validate(payload)))

    def test_pass_rejected_when_evidence_is_absent(self):
        payload = copy.deepcopy(self.source)
        payload["result"] = "pass"
        for step in payload["required_steps"]:
            step["status"] = "complete"
        payload["required_steps"][0]["evidence"] = []
        self.assertTrue(any("lacking evidence" in error for error in self.validate(payload)))

    def test_pass_rejected_when_upstream_is_unresolved(self):
        payload = copy.deepcopy(self.source)
        payload["result"] = "pass"
        for step in payload["required_steps"]:
            step["status"] = "complete"
            step["evidence"] = [{"path": "evidence.md"}]
        payload["upstream_dependencies"][0]["status"] = "incomplete"
        self.assertTrue(any("unresolved upstream" in error for error in self.validate(payload)))


if __name__ == "__main__":
    unittest.main()
