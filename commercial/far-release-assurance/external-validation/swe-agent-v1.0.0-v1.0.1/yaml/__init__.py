"""Transparent PyYAML shim for pinned SWE-agent configuration output.

The pinned releases serialize ``Path`` objects with Python-specific YAML tags
and may write deterministic deployment diagnostics before the final
``--print_config`` mapping. FAR accepts only the exact pathlib tags and only a
suffix that has the complete RunBatchConfig shape. Arbitrary Python object
construction remains rejected.
"""

from __future__ import annotations

import sys
from pathlib import Path as _Path

_THIS_FILE = _Path(__file__).resolve()
_REAL_INIT: _Path | None = None

for _entry in sys.path:
    if not _entry:
        continue
    _candidate = (_Path(_entry) / "yaml" / "__init__.py").resolve()
    if _candidate.is_file() and _candidate != _THIS_FILE:
        _REAL_INIT = _candidate
        break

if _REAL_INIT is None:
    raise ModuleNotFoundError("Installed PyYAML package could not be located")

__path__.append(str(_REAL_INIT.parent))
exec(compile(_REAL_INIT.read_bytes(), str(_REAL_INIT), "exec"), globals(), globals())


def _construct_path(loader, node):
    parts = loader.construct_sequence(node, deep=True)
    if not all(isinstance(part, str) for part in parts):
        raise constructor.ConstructorError(
            None,
            None,
            "pathlib YAML tag contained a non-string path component",
            node.start_mark,
        )
    return _Path(*parts)


_PATHLIB_MODULES = ("pathlib", "pathlib._local")
_PATHLIB_CLASSES = ("Path", "PosixPath", "PurePath", "PurePosixPath", "WindowsPath", "PureWindowsPath")

for _module in _PATHLIB_MODULES:
    for _class_name in _PATHLIB_CLASSES:
        SafeLoader.add_constructor(
            f"tag:yaml.org,2002:python/object/apply:{_module}.{_class_name}",
            _construct_path,
        )


_REAL_SAFE_LOAD = safe_load
_REQUIRED_RUN_BATCH_KEYS = {
    "agent",
    "instances",
    "output_dir",
    "num_workers",
    "progress_bar",
    "random_delay_multiplier",
    "raise_exceptions",
    "redo_existing",
}


def _is_complete_run_batch_config(value) -> bool:
    return isinstance(value, dict) and _REQUIRED_RUN_BATCH_KEYS <= set(value)


def safe_load(stream):
    """Load normal YAML, or one complete pinned config after stdout diagnostics."""
    try:
        return _REAL_SAFE_LOAD(stream)
    except YAMLError as original_error:
        text = stream.read() if hasattr(stream, "read") else str(stream)
        lines = text.splitlines()
        candidates = []
        for index, line in enumerate(lines):
            if line != "agent:":
                continue
            suffix = "\n".join(lines[index:]) + "\n"
            try:
                parsed = _REAL_SAFE_LOAD(suffix)
            except YAMLError:
                continue
            if _is_complete_run_batch_config(parsed):
                candidates.append(parsed)
        if len(candidates) == 1:
            return candidates[0]
        raise original_error
