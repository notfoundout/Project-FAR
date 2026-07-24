from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any

import yaml
from sweagent.run.common import BasicCLI
from sweagent.run.run_batch import RunBatchConfig
from sweagent.utils.config import _strip_abspath_from_dict

CASE_DIR = Path(__file__).parent
CONFIG_PATH = CASE_DIR / "agent-config.yaml"
LOCK_PATH = CASE_DIR / "environment-freeze" / "environment-lock.json"
TASK_PATH = CASE_DIR / "environment-freeze" / "task-record.public.json"


def assert_subset(expected: Any, actual: Any, path: str = "root") -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            raise AssertionError(f"{path}: expected mapping, got {type(actual).__name__}")
        for key, value in expected.items():
            if key not in actual:
                raise AssertionError(f"{path}.{key}: missing")
            assert_subset(value, actual[key], f"{path}.{key}")
        return
    if isinstance(expected, list):
        if actual != expected:
            raise AssertionError(f"{path}: list drift: expected {expected!r}, got {actual!r}")
        return
    if actual != expected:
        raise AssertionError(f"{path}: expected {expected!r}, got {actual!r}")


def validate(release_default: Path) -> None:
    release_default = release_default.resolve()
    release_root = release_default.parent.parent
    if not release_default.is_file() or not (release_root / "pyproject.toml").is_file():
        raise SystemExit(f"Invalid pinned SWE-agent checkout: {release_root}")

    task = json.loads(TASK_PATH.read_text(encoding="utf-8"))
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    frozen = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        instance_path = tmp_path / "instance.json"
        output_path = tmp_path / "output"
        instance_path.write_text(
            json.dumps([
                {
                    "image_name": lock["immutable_image_reference"],
                    "problem_statement": task["problem_statement"],
                    "id": task["instance_id"],
                    "repo_name": "testbed",
                    "base_commit": task["base_commit"],
                    "extra_fields": {"outcome_data_accessible": False},
                }
            ]),
            encoding="utf-8",
        )
        args = [
            "--config", str(release_default),
            "--config", str(CONFIG_PATH.resolve()),
            "--instances.type=file",
            f"--instances.path={instance_path}",
            f"--output_dir={output_path}",
            "--num_workers=1",
            "--progress_bar=False",
            "--random_delay_multiplier=0",
            "--raise_exceptions=True",
            "--redo_existing=False",
        ]
        parsed = BasicCLI(RunBatchConfig).get_config(args).model_dump(mode="json")
        normalized_agent = _strip_abspath_from_dict(parsed["agent"], root=release_root)
        assert_subset(frozen["agent"], normalized_agent, "agent")
        assert parsed["num_workers"] == 1
        assert parsed["redo_existing"] is False
        assert parsed["progress_bar"] is False
        assert parsed["random_delay_multiplier"] == 0
        assert parsed["raise_exceptions"] is True
        assert parsed["instances"]["type"] == "file"
        assert parsed["instances"]["path"] == str(instance_path)
        assert parsed["output_dir"] == str(output_path)
    print("Exact live SWE-agent configuration parsed without model access or semantic path drift.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-default", type=Path, required=True)
    args = parser.parse_args()
    validate(args.release_default)


if __name__ == "__main__":
    main()
