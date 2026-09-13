"""Constrained local jsonschema-compatible validator used when PyPI is unavailable."""
from __future__ import annotations

from ._validator import Draft202012Validator, ValidationError, __version__

__all__ = ["Draft202012Validator", "ValidationError", "__version__"]
