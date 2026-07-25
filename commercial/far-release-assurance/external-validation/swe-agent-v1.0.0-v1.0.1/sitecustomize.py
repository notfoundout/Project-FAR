"""Narrow PyYAML compatibility for the pinned SWE-agent --print_config output.

SWE-agent v1.0.0/v1.0.1 serializes ``Path`` values with Python-specific
``pathlib`` tags even though FAR deliberately parses the result with
``yaml.safe_load``. Register only the exact path constructors required by the
pinned output; do not enable PyYAML's unsafe loader or arbitrary object
construction.
"""

from __future__ import annotations

from pathlib import Path

import yaml


def _construct_path(loader: yaml.SafeLoader, node: yaml.Node) -> Path:
    parts = loader.construct_sequence(node, deep=True)
    if not all(isinstance(part, str) for part in parts):
        raise yaml.constructor.ConstructorError(
            None,
            None,
            "pathlib YAML tag contained a non-string path component",
            node.start_mark,
        )
    return Path(*parts)


_PATHLIB_MODULES = ("pathlib", "pathlib._local")
_PATHLIB_CLASSES = ("Path", "PosixPath", "PurePath", "PurePosixPath", "WindowsPath", "PureWindowsPath")

for _module in _PATHLIB_MODULES:
    for _class_name in _PATHLIB_CLASSES:
        yaml.SafeLoader.add_constructor(
            f"tag:yaml.org,2002:python/object/apply:{_module}.{_class_name}",
            _construct_path,
        )
