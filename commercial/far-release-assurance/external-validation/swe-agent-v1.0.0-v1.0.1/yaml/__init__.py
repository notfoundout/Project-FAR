"""Transparent PyYAML shim for pinned SWE-agent configuration output.

The pinned releases serialize ``Path`` objects with Python-specific YAML tags,
may emit sets, and may write deterministic deployment diagnostics before the
final ``--print_config`` mapping. FAR accepts only the exact pathlib tags, only
a suffix with the complete RunBatchConfig shape, and normalizes that mapping to
deterministic JSON-safe evidence. Arbitrary Python object construction remains
rejected.
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


def _construct_unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                "found an unhashable key", key_node.start_mark,
            ) from exc
        if duplicate:
            raise constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"found duplicate key {key!r}", key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


SafeLoader.add_constructor(
    resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


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


def _json_safe(value):
    if isinstance(value, _Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, (set, frozenset)):
        normalized = [_json_safe(item) for item in value]
        return sorted(normalized, key=lambda item: repr(item))
    return value


def _validated_config(value):
    return _json_safe(value) if _is_complete_run_batch_config(value) else value


def safe_load(stream):
    """Load ordinary YAML, or one complete pinned config after diagnostics."""
    try:
        return _validated_config(_REAL_SAFE_LOAD(stream))
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
                candidates.append(_json_safe(parsed))
        if len(candidates) == 1:
            return candidates[0]
        raise original_error
