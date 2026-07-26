from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

from case_tools import CASE_DIR, verify_shared_implementation

LEGACY_DIR = (CASE_DIR / "../swe-agent-v1.0.0-v1.0.1").resolve()


def load_validator():
    verify_shared_implementation()
    sys.path.insert(0, str(LEGACY_DIR))
    path = LEGACY_DIR / "validate_agent_config.py"
    spec = importlib.util.spec_from_file_location(
        "_far_locked_legacy_validate_agent_config", path
    )
    if spec is None or spec.loader is None:
        raise SystemExit("Unable to load the locked SWE-agent config validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CASE_DIR = CASE_DIR
    module.CONFIG_PATH = CASE_DIR / "agent-config.yaml"
    module.LOCK_PATH = CASE_DIR / "environment-freeze/environment-lock.json"
    module.TASK_PATH = CASE_DIR / "environment-freeze/task-record.public.json"
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-default", type=Path, required=True)
    args = parser.parse_args()
    load_validator().validate(args.release_default)


if __name__ == "__main__":
    main()
