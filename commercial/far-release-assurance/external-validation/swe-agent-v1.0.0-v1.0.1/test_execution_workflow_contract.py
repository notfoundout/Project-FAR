from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

import execute_controller as controller


ROOT = Path(__file__).resolve().parents[4]
WORKFLOW = ROOT / ".github/workflows/far-swe-agent-execution.yml"


class ExecutionWorkflowContractTests(unittest.TestCase):
    def test_restore_step_invokes_case_local_planner(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        match = re.search(
            r"- name: Restore latest validated execution state\n(?P<body>.*?)(?=\n\s*- name: Resolve next frozen SWE-agent release)",
            text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match, "restore step is missing")
        body = match.group("body")
        self.assertIn('python "$CASE_DIR/run_comparison.py" plan', body)
        self.assertNotRegex(body, r"(?m)^\s*python run_comparison\.py plan\s*$")

    def test_contract_runs_before_any_model_execution(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        validation = text.index("- name: Validate manifest and regression tests")
        execution = text.index("- name: Execute exactly one next frozen run")
        self.assertLess(validation, execution)
        self.assertIn("test_execution_workflow_contract.py", text[validation:execution])


class PinnedCliContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.agent_repo = self.root / "agent"
        (self.agent_repo / "config").mkdir(parents=True)
        (self.agent_repo / "config" / "default.yaml").write_text("agent: {}\n", encoding="utf-8")
        self.case_config = self.root / "agent-config.yaml"
        self.case_config.write_text("agent: {}\n", encoding="utf-8")
        self.instance = self.root / "instance.json"
        self.instance.write_text("[]\n", encoding="utf-8")
        self.output = self.root / "output"
        self.path_patch = patch.object(controller, "CONFIG_PATH", self.case_config)
        self.path_patch.start()
        self.executable = "/usr/bin/sweagent"
        self.command = controller.build_cli_command(
            self.executable,
            self.agent_repo,
            self.instance,
            self.output,
        )

    def tearDown(self) -> None:
        self.path_patch.stop()
        self.tmp.cleanup()

    def parsed_config(self) -> dict[str, object]:
        return {
            "output_dir": str(self.output.resolve()),
            "num_workers": 1,
            "progress_bar": False,
            "random_delay_multiplier": 0,
            "raise_exceptions": True,
            "redo_existing": False,
            "instances": {"type": "file", "path": str(self.instance.resolve())},
        }

    @patch("execute_controller.shutil.which", return_value="/usr/bin/sweagent")
    def test_canonical_command_binds_both_configs_in_order(self, _which) -> None:
        controller.validate_command_contract(self.command, self.agent_repo, self.instance, self.output)
        positions = [index for index, token in enumerate(self.command) if token == "--config"]
        self.assertEqual(len(positions), 2)
        self.assertEqual(self.command[positions[0] + 1], str((self.agent_repo / "config/default.yaml").resolve()))
        self.assertEqual(self.command[positions[1] + 1], str(self.case_config.resolve()))

    @patch("execute_controller.shutil.which", return_value="/usr/bin/sweagent")
    def test_missing_second_config_is_rejected(self, _which) -> None:
        drifted = self.command.copy()
        second = [index for index, token in enumerate(drifted) if token == "--config"][1]
        del drifted[second : second + 2]
        with self.assertRaisesRegex(SystemExit, "canonical command"):
            controller.validate_command_contract(drifted, self.agent_repo, self.instance, self.output)

    @patch("execute_controller.shutil.which", return_value="/usr/bin/sweagent")
    def test_renamed_worker_setting_is_rejected(self, _which) -> None:
        drifted = ["--num-workers=1" if token == "--num_workers=1" else token for token in self.command]
        with self.assertRaisesRegex(SystemExit, "canonical command"):
            controller.validate_command_contract(drifted, self.agent_repo, self.instance, self.output)

    def test_parser_output_drift_is_rejected(self) -> None:
        parsed = self.parsed_config()
        parsed["num_workers"] = 2
        with self.assertRaisesRegex(SystemExit, "num_workers"):
            controller.validate_parsed_config(parsed, self.instance, self.output)

    def test_ignored_instance_path_is_rejected(self) -> None:
        parsed = self.parsed_config()
        parsed["instances"] = {"type": "file", "path": str(self.root / "other.json")}
        with self.assertRaisesRegex(SystemExit, "instance path"):
            controller.validate_parsed_config(parsed, self.instance, self.output)

    @patch("execute_controller.shutil.which", return_value="/usr/bin/sweagent")
    @patch("execute_controller.subprocess.run")
    def test_exact_command_is_parse_validated_without_model_execution(self, run, _which) -> None:
        run.return_value.returncode = 0
        run.return_value.stdout = yaml.safe_dump(self.parsed_config())
        run.return_value.stderr = ""
        parsed = controller.verify_cli_contract(self.command, self.agent_repo, self.instance, self.output)
        self.assertEqual(parsed["num_workers"], 1)
        called = run.call_args.args[0]
        self.assertEqual(called[:-1], self.command)
        self.assertEqual(called[-1], "--print_config")
        self.assertEqual(run.call_args.kwargs["cwd"], self.agent_repo)

    @patch("execute_controller.shutil.which", return_value="/usr/bin/sweagent")
    @patch("execute_controller.subprocess.run")
    def test_parse_failure_stops_before_execution(self, run, _which) -> None:
        run.return_value.returncode = 1
        run.return_value.stdout = ""
        run.return_value.stderr = "invalid configuration"
        with self.assertRaisesRegex(SystemExit, "parse-only validation"):
            controller.verify_cli_contract(self.command, self.agent_repo, self.instance, self.output)
        self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
