"""Run trusted validator commands from a lock-verified temporary package.

The candidate checkout is data, not an import root.  ``python -I`` removes the working directory
from ``sys.path``; this launcher then copies only SHA-256-bound ``far_validation`` modules from the
assurance lock into a fresh temporary directory and imports from that directory.  A missing or
undeclared dependency therefore fails closed instead of resolving from candidate-controlled
checkout bytes.

Only the three pre-candidate-code commands used by the assurance workflows are exposed here:
``oracle``, ``weakening`` and ``formal``.  General validation continues through the normal package
after the workflow crosses the candidate-code boundary.
"""
from __future__ import annotations

import hashlib
import importlib
import importlib.machinery
import json
import sys
import tempfile
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "validation_bootstrap" / "assurance-lock.json"
COMMANDS = {
    "oracle": "far_validation.oracle",
    "weakening": "far_validation.weakening",
    "formal": "far_validation.formal_model",
}


def _fail(message: str) -> int:
    print(f"FAR-VAL-ISOLATED-001: {message}", file=sys.stderr)
    return 2


def _locked_modules() -> dict[str, str]:
    try:
        payload = json.loads(LOCK.read_text(encoding="utf-8"))
        files = payload["files"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load assurance lock: {exc}") from exc
    if not isinstance(files, dict):
        raise ValueError("assurance lock files must be an object")
    modules = {
        path: digest
        for path, digest in files.items()
        if isinstance(path, str)
        and path.startswith("far_validation/")
        and path.endswith(".py")
        and isinstance(digest, str)
        and len(digest) == 64
    }
    required = {f"far_validation/{name}.py" for name in ("oracle", "weakening", "formal_model")}
    missing = sorted(required - set(modules))
    if missing:
        raise ValueError(f"trusted command module is not assurance-locked: {missing}")
    return modules


def _copy_verified_modules(destination: Path, modules: dict[str, str]) -> None:
    for relative, expected in sorted(modules.items()):
        source = ROOT / relative
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"locked module is missing or not a regular file: {relative}")
        data = source.read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            raise ValueError(f"locked module hash mismatch: {relative}: {actual} != {expected}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def _install_synthetic_package(package_dir: Path) -> None:
    # Do not execute candidate ``far_validation/__init__.py``.  The synthetic package exposes only
    # the verified temporary directory to relative imports made by the locked command modules.
    package = types.ModuleType("far_validation")
    package.__package__ = "far_validation"
    package.__path__ = [str(package_dir)]
    package.__spec__ = importlib.machinery.ModuleSpec("far_validation", loader=None, is_package=True)
    package.__spec__.submodule_search_locations = package.__path__
    sys.modules["far_validation"] = package


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] not in COMMANDS:
        return _fail(f"command must be one of {sorted(COMMANDS)}")
    command = args.pop(0)
    try:
        modules = _locked_modules()
        with tempfile.TemporaryDirectory(prefix="far-locked-validator-") as directory:
            root = Path(directory)
            _copy_verified_modules(root, modules)
            _install_synthetic_package(root / "far_validation")
            module = importlib.import_module(COMMANDS[command])
            entry = getattr(module, "main", None)
            if not callable(entry):
                raise ValueError(f"trusted command {command} has no callable main")
            return int(entry(args))
    except (OSError, ValueError, ImportError, AttributeError) as exc:
        return _fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
