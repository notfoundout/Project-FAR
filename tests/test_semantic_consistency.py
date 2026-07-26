import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("semantic_check", ROOT / "tools/check_semantic_consistency.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class SemanticConsistencyTest(unittest.TestCase):
    def test_registry_and_canonical_documents_are_consistent(self):
        self.assertEqual([], MODULE.validate())

    def test_frozen_swe_agent_evidence_is_not_a_required_theory_input(self):
        data = __import__("json").loads(MODULE.REGISTRY.read_text(encoding="utf-8"))
        self.assertFalse(any("swe-agent-v2" in path for path in data["required_documents"]))


if __name__ == "__main__":
    unittest.main()
