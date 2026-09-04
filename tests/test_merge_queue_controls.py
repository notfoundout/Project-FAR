import importlib.util
from pathlib import Path
import unittest
from unittest import mock

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
        self.assertEqual(payload["conditions"]["ref_name"]["exclude"], [])
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

    def test_canonical_ruleset_exact_match_passes(self):
        ruleset = CONFIG.desired_ruleset()
        self.assertEqual(CHECK.validate_canonical_ruleset(ruleset), [])

    def test_canonical_ruleset_scope_drift_fails(self):
        ruleset = CONFIG.desired_ruleset()
        ruleset["conditions"]["ref_name"]["include"] = ["refs/heads/main", "refs/heads/release"]
        errors = CHECK.validate_canonical_ruleset(ruleset)
        self.assertTrue(any("include scope" in error for error in errors))

    def test_canonical_ruleset_bypass_actor_fails(self):
        ruleset = CONFIG.desired_ruleset()
        ruleset["bypass_actors"] = [{"actor_id": 1, "actor_type": "Team", "bypass_mode": "always"}]
        errors = CHECK.validate_canonical_ruleset(ruleset)
        self.assertTrue(any("bypass_actors" in error for error in errors))

    def test_canonical_ruleset_inactive_fails(self):
        ruleset = CONFIG.desired_ruleset()
        ruleset["enforcement"] = "disabled"
        errors = CHECK.validate_canonical_ruleset(ruleset)
        self.assertTrue(any("enforcement" in error for error in errors))

    def test_merge_queue_parameter_drift_fails(self):
        parameters = dict(CHECK.EXPECTED)
        parameters["grouping_strategy"] = "HEADGREEN"
        errors = CHECK.validate_active_branch_rules([
            {"type": "merge_queue", "parameters": parameters}
        ])
        self.assertTrue(any("grouping_strategy" in error for error in errors))

    def test_duplicate_active_queue_rules_fail(self):
        rules = [
            {"type": "merge_queue", "parameters": dict(CHECK.EXPECTED)},
            {"type": "merge_queue", "parameters": dict(CHECK.EXPECTED)},
        ]
        self.assertTrue(CHECK.validate_active_branch_rules(rules))

    def test_duplicate_named_repository_rulesets_fail_closed(self):
        matches = [
            {"id": 1, "name": CONFIG.RULESET_NAME, "source_type": "Repository"},
            {"id": 2, "name": CONFIG.RULESET_NAME, "source_type": "Repository"},
        ]
        with self.assertRaises(SystemExit):
            CONFIG.select_existing_canonical_ruleset(matches)
        selected, errors = CHECK.select_canonical_ruleset(matches)
        self.assertIsNone(selected)
        self.assertTrue(errors)

    def test_configurator_paginates_until_short_page(self):
        page1 = [{"id": i} for i in range(CONFIG.PAGE_SIZE)]
        page2 = [{"id": CONFIG.PAGE_SIZE}]
        with mock.patch.object(CONFIG, "request", side_effect=[page1, page2]) as request:
            result = CONFIG.list_repository_rulesets("https://api.example/repos/o/r", "token")
        self.assertEqual(len(result), CONFIG.PAGE_SIZE + 1)
        self.assertEqual(request.call_count, 2)
        self.assertIn("page=1", request.call_args_list[0].args[1])
        self.assertIn("page=2", request.call_args_list[1].args[1])

    def test_workflow_must_handle_merge_group(self):
        errors = CHECK.validate_workflow(ROOT / ".github/workflows/validator-assurance.yml")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
