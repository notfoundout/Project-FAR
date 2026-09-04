import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


CONFIG = load("configure_validation_merge_queue", ROOT / "tools/configure_validation_merge_queue.py")
CHECK = load("check_validation_merge_queue", ROOT / "tools/check_validation_merge_queue.py")


class MergeQueueControlTests(unittest.TestCase):
    def test_desired_ruleset_is_conservative_and_default_branch_scoped(self):
        payload = CONFIG.desired_ruleset()
        self.assertEqual(payload["enforcement"], "active")
        self.assertEqual(payload["conditions"]["ref_name"]["include"], ["~DEFAULT_BRANCH"])
        self.assertEqual(payload["bypass_actors"], [])
        queue = payload["rules"][0]
        self.assertEqual(queue["type"], "merge_queue")
        self.assertEqual(queue["parameters"]["grouping_strategy"], "ALLGREEN")
        self.assertEqual(queue["parameters"]["max_entries_to_merge"], 1)
        self.assertEqual(queue["parameters"]["min_entries_to_merge"], 1)

    def test_personal_owner_is_rejected(self):
        with self.assertRaises(SystemExit):
            CONFIG.require_organization({"owner": {"type": "User"}})

    def test_organization_owner_is_accepted(self):
        CONFIG.require_organization({"owner": {"type": "Organization"}})

    def test_merge_queue_rule_exact_match_passes(self):
        rules = [{"type": "merge_queue", "parameters": dict(CHECK.EXPECTED)}]
        self.assertEqual(CHECK.validate_merge_queue_rule(rules), [])

    def test_merge_queue_rule_drift_fails(self):
        parameters = dict(CHECK.EXPECTED)
        parameters["grouping_strategy"] = "HEADGREEN"
        errors = CHECK.validate_merge_queue_rule([
            {"type": "merge_queue", "parameters": parameters}
        ])
        self.assertTrue(any("grouping_strategy" in error for error in errors))

    def test_duplicate_queue_rules_fail(self):
        rules = [
            {"type": "merge_queue", "parameters": dict(CHECK.EXPECTED)},
            {"type": "merge_queue", "parameters": dict(CHECK.EXPECTED)},
        ]
        self.assertTrue(CHECK.validate_merge_queue_rule(rules))

    def test_workflow_must_handle_merge_group(self):
        errors = CHECK.validate_workflow(ROOT / ".github/workflows/validator-assurance.yml")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
