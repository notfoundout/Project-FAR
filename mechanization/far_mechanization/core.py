"""Core immutable primitives for the FAR canonical IR."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping

from .diagnostics import Diagnostic, DiagnosticCode, DiagnosticSeverity, SourceLocation

IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
IDENTIFIER_PATTERN_TEXT = "^[A-Za-z][A-Za-z0-9_.:-]*$"


class IRKind(StrEnum):
    REPRESENTATION = "representation"
    STRUCTURE = "structure"
    INTERPRETATION = "interpretation"
    INVESTIGATION = "investigation"
    CLAIM = "claim"
    ASSUMPTION = "assumption"
    EVIDENCE = "evidence"
    OPERATION = "operation"
    REASONING_STEP = "reasoning_step"
    DEPENDENCY = "dependency"
    PROOF = "proof"


@dataclass(frozen=True, slots=True)
class Identifier:
    """Stable, case-sensitive, human-readable IR identifier."""

    value: str

    def validate(self) -> tuple[Diagnostic, ...]:
        if not self.value:
            return (Diagnostic(DiagnosticCode.INVALID_IDENTIFIER, DiagnosticSeverity.ERROR, "identifier must be non-empty"),)
        if not IDENTIFIER_PATTERN.fullmatch(self.value):
            return (Diagnostic(DiagnosticCode.INVALID_IDENTIFIER, DiagnosticSeverity.ERROR, f"identifier '{self.value}' must match {IDENTIFIER_PATTERN_TEXT}", related_identifier=self.value),)
        return ()

    @property
    def is_valid(self) -> bool:
        return not self.validate()

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class Reference:
    """Typed but unresolved reference to another IR object."""

    identifier: Identifier
    expected_kind: IRKind | None = None
    source: SourceLocation | None = None

    def validate(self) -> tuple[Diagnostic, ...]:
        diagnostics = list(self.identifier.validate())
        if self.source is not None:
            diagnostics.extend(self.source.validate())
        return tuple(diagnostics)


def freeze_metadata(metadata: Mapping[str, object]) -> Mapping[str, object]:
    return MappingProxyType(dict(metadata))
