"""Transparent PyYAML shim with narrow pathlib-tag support.

The pinned SWE-agent releases serialize ``Path`` objects in ``--print_config``
using Python-specific YAML tags. FAR must parse those exact tags while still
rejecting arbitrary Python object construction. This module delegates to the
installed PyYAML package, then adds only the required pathlib constructors to
``SafeLoader``.
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
