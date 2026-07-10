"""Structured diagnostics for FAR mechanization IR validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping


class DiagnosticSeverity(StrEnum):
    """Stable severity levels for non-terminating validation results."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class DiagnosticCode(StrEnum):
    """Stable IR-level diagnostic code registry."""

    INVALID_IDENTIFIER = "FAR-IR-001"
    MISSING_REQUIRED_FIELD = "FAR-IR-002"
    DUPLICATE_LOCAL_IDENTIFIER = "FAR-IR-003"
    INVALID_ENUM_VALUE = "FAR-IR-004"
    INVALID_INTERNAL_OBJECT_SHAPE = "FAR-IR-005"
    INVALID_SOURCE_RANGE = "FAR-IR-006"
    UNSUPPORTED_FORMAT_VERSION = "FAR-EXT-001"
    INVALID_EXTERNAL_OBJECT_KIND = "FAR-EXT-002"
    UNKNOWN_CORE_FIELD = "FAR-EXT-003"
    MISSING_EXTERNAL_FIELD = "FAR-EXT-004"
    EXTERNAL_FIELD_TYPE_MISMATCH = "FAR-EXT-005"
    SCHEMA_CONSTRAINT_VIOLATION = "FAR-EXT-006"
    LOSSY_CONVERSION_ATTEMPT = "FAR-EXT-007"
    UNSUPPORTED_FILE_FORMAT = "FAR-PARSE-001"
    UNKNOWN_FILE_EXTENSION = "FAR-PARSE-002"
    MALFORMED_JSON = "FAR-PARSE-003"
    MALFORMED_YAML = "FAR-PARSE-004"
    NON_OBJECT_ROOT = "FAR-PARSE-005"
    UNREADABLE_FILE = "FAR-PARSE-006"
    ENCODING_ERROR = "FAR-PARSE-007"
    AMBIGUOUS_FORMAT_DETECTION = "FAR-PARSE-008"
    FILE_WRITE_ERROR = "FAR-SER-001"


@dataclass(frozen=True, slots=True)
class SourceLocation:
    """Optional source provenance independent of any storage format."""

    source: str
    line: int | None = None
    column: int | None = None
    end_line: int | None = None
    end_column: int | None = None

    def validate(self) -> tuple["Diagnostic", ...]:
        diagnostics: list[Diagnostic] = []
        if not self.source:
            diagnostics.append(Diagnostic(DiagnosticCode.MISSING_REQUIRED_FIELD, DiagnosticSeverity.ERROR, "source location requires a non-empty source"))
        for name in ("line", "column", "end_line", "end_column"):
            value = getattr(self, name)
            if value is not None and value < 1:
                diagnostics.append(Diagnostic(DiagnosticCode.INVALID_SOURCE_RANGE, DiagnosticSeverity.ERROR, f"source location {name} must be positive when present", source=self))
        if self.line is None and (self.column is not None or self.end_line is not None or self.end_column is not None):
            diagnostics.append(Diagnostic(DiagnosticCode.INVALID_SOURCE_RANGE, DiagnosticSeverity.ERROR, "source location ranges require a start line", source=self))
        if self.end_line is not None and self.line is not None and self.end_line < self.line:
            diagnostics.append(Diagnostic(DiagnosticCode.INVALID_SOURCE_RANGE, DiagnosticSeverity.ERROR, "source location end line must not precede start line", source=self))
        if self.end_line == self.line and self.end_column is not None and self.column is not None and self.end_column < self.column:
            diagnostics.append(Diagnostic(DiagnosticCode.INVALID_SOURCE_RANGE, DiagnosticSeverity.ERROR, "source location end column must not precede start column", source=self))
        return tuple(diagnostics)


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """A structured validation diagnostic; ordinary user errors are reported here."""

    code: DiagnosticCode
    severity: DiagnosticSeverity
    message: str
    source: SourceLocation | None = None
    related_identifier: str | None = None
    details: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))
