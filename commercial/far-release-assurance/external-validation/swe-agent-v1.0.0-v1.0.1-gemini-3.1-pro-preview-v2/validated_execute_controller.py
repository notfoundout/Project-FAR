from __future__ import annotations

import importlib.util
import sys

from case_tools import CASE_DIR, load_manifest, verify_shared_implementation

LEGACY_DIR = (CASE_DIR / "../swe-agent-v1.0.0-v1.0.1").resolve()


def load_legacy_controller():
    manifest = load_manifest()
    if manifest["status"] != "execution_inputs_frozen":
        raise SystemExit(
            "The v2 case is not frozen. Complete and merge the exact-model "
            "access-freeze PR before invoking the execution controller."
        )
    verify_shared_implementation()
    sys.path.insert(0, str(LEGACY_DIR))
    path = LEGACY_DIR / "validated_execute_controller.py"
    spec = importlib.util.spec_from_file_location(
        "_far_locked_legacy_validated_execute_controller", path
    )
    if spec is None or spec.loader is None:
        raise SystemExit("Unable to load the locked validated controller")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    base = module._core.base
    base.CASE_DIR = CASE_DIR
    base.MANIFEST_PATH = CASE_DIR / "manifest.json"
    base.LOCK_PATH = CASE_DIR / "environment-freeze/environment-lock.json"
    base.TASK_PATH = CASE_DIR / "environment-freeze/task-record.public.json"
    base.CONFIG_PATH = CASE_DIR / "agent-config.yaml"
    base.OUTPUT_DIR = CASE_DIR / "execution-output"
    base.PLAN_PATH = base.OUTPUT_DIR / "execution-plan.json"
    base.STATE_PATH = base.OUTPUT_DIR / "execution-state.json"
    base.TRAJECTORY_DIR = base.OUTPUT_DIR / "trajectories"
    base.RUNS_DIR = base.OUTPUT_DIR / "runs"
    return module


def main() -> None:
    load_legacy_controller()._core.main()


if __name__ == "__main__":
    main()
