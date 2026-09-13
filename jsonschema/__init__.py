"""Constrained local jsonschema-compatible validator used when PyPI is unavailable.

The implementation lives in ``_validator``; this package facade pins the JSON
Schema Draft 2020-12 integer type semantics that Python's ``int`` test alone does
not capture.  A mathematically integral finite float is an integer instance,
while booleans are not numeric instances for JSON Schema type checking.
"""
from __future__ import annotations

import math
from typing import Any

from . import _validator as _core

__version__ = _core.__version__
ValidationError = _core.ValidationError

_original_type_ok = _core._type_ok


def _type_ok(instance: Any, typ: Any) -> bool:
    if isinstance(typ, list):
        return any(_type_ok(instance, member) for member in typ)
    if typ == "integer":
        if isinstance(instance, bool):
            return False
        if isinstance(instance, int):
            return True
        return isinstance(instance, float) and math.isfinite(instance) and instance.is_integer()
    return _original_type_ok(instance, typ)


# _validate resolves _type_ok in the implementation module at call time.
_core._type_ok = _type_ok
Draft202012Validator = _core.Draft202012Validator
