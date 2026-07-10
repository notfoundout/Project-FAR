"""JSON/YAML parser pipeline for FAR mechanization documents."""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml
from jsonschema import Draft202012Validator
from .diagnostics import Diagnostic, DiagnosticCode, DiagnosticSeverity, SourceLocation
from .external_models import ExternalFARDocument
from .ir import FARDocument
from .normalization import normalize_ir_document

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "far-document.schema.json"

@dataclass(frozen=True, slots=True)
class ParseResult:
    document: FARDocument | None
    diagnostics: tuple[Diagnostic, ...]
    source: str | None
    detected_format: str | None
    format_version: str | None
    @property
    def success(self) -> bool: return self.document is not None and not self.diagnostics

def _diag(code: DiagnosticCode, msg: str, source: str | None=None, line: int | None=None, column: int | None=None, details: dict[str,object] | None=None):
    return Diagnostic(code, DiagnosticSeverity.ERROR, msg, SourceLocation(source or "<input>", line, column), details=details or {})

def detect_format(source: str | Path | None = None, text: str | None = None, explicit_format: str | None = None) -> tuple[str | None, tuple[Diagnostic,...]]:
    if explicit_format is not None:
        fmt=explicit_format.lower()
        if fmt in {"json","yaml"}: return fmt, ()
        return None, (_diag(DiagnosticCode.UNSUPPORTED_FILE_FORMAT, f"unsupported file format: {explicit_format}", str(source) if source else None),)
    if source is not None:
        suffix=Path(source).suffix.lower()
        if suffix == ".json": return "json", ()
        if suffix in {".yaml", ".yml"}: return "yaml", ()
        if suffix: return None, (_diag(DiagnosticCode.UNKNOWN_FILE_EXTENSION, f"unknown file extension: {suffix}", str(source)),)
    if text is not None:
        stripped=text.lstrip()
        if stripped.startswith("{"): return "json", ()
        if stripped.startswith("---") or ":" in stripped.splitlines()[0] if stripped.splitlines() else False: return "yaml", ()
        return None, (_diag(DiagnosticCode.AMBIGUOUS_FORMAT_DETECTION, "could not detect JSON or YAML format", str(source) if source else None),)
    return None, (_diag(DiagnosticCode.AMBIGUOUS_FORMAT_DETECTION, "no source or text available for detection", str(source) if source else None),)

def _load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

def _schema_diagnostics(data: Any, source: str | None) -> tuple[Diagnostic,...]:
    schema=_load_schema(); Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema)
    diagnostics=[]
    for err in sorted(validator.iter_errors(data), key=lambda e: (tuple(e.path), tuple(e.schema_path), e.message)):
        diagnostics.append(_diag(DiagnosticCode.SCHEMA_CONSTRAINT_VIOLATION, err.message, source, details={"path": list(err.path), "schema_path": list(err.schema_path)}))
    return tuple(diagnostics)

def _parse_primitive(text: str, fmt: str, source: str | None):
    try:
        if fmt == "json": return json.loads(text), ()
        return yaml.safe_load(text), ()
    except json.JSONDecodeError as exc:
        return None, (_diag(DiagnosticCode.MALFORMED_JSON, exc.msg, source, exc.lineno, exc.colno),)
    except yaml.YAMLError as exc:
        mark=getattr(exc, "problem_mark", None)
        line=(mark.line+1) if mark else None; col=(mark.column+1) if mark else None
        return None, (_diag(DiagnosticCode.MALFORMED_YAML, str(exc), source, line, col),)

def _pipeline(text: str, fmt: str, source: str | None) -> ParseResult:
    data, ds = _parse_primitive(text, fmt, source)
    if ds: return ParseResult(None, ds, source, fmt, None)
    if not isinstance(data, dict):
        return ParseResult(None, (_diag(DiagnosticCode.NON_OBJECT_ROOT, "root document must be an object", source),), source, fmt, None)
    format_version=data.get("format_version") if isinstance(data.get("format_version"), str) else None
    ds=_schema_diagnostics(data, source)
    if ds: return ParseResult(None, ds, source, fmt, format_version)
    external, model_ds = ExternalFARDocument.from_mapping(data)
    if model_ds or external is None: return ParseResult(None, model_ds, source, fmt, format_version)
    ir, ir_ds = external.to_ir()
    if ir_ds: return ParseResult(None, ir_ds, source, fmt, format_version)
    norm = normalize_ir_document(ir)
    if not norm.success: return ParseResult(None, norm.diagnostics, source, fmt, format_version)
    normalized_ir, normalized_ds = norm.document.to_ir()
    if normalized_ds: return ParseResult(None, normalized_ds, source, fmt, format_version)
    return ParseResult(normalized_ir, (), source, fmt, format_version)

def parse_json_text(text: str, source: str | None=None) -> ParseResult:
    return _pipeline(text, "json", source)

def parse_yaml_text(text: str, source: str | None=None) -> ParseResult:
    return _pipeline(text, "yaml", source)

def parse_document(text: str, source: str | Path | None=None, explicit_format: str | None=None) -> ParseResult:
    fmt, ds=detect_format(source, text, explicit_format)
    if ds or fmt is None: return ParseResult(None, ds, str(source) if source else None, fmt, None)
    return _pipeline(text, fmt, str(source) if source else None)

def _read(path: str | Path):
    try: return Path(path).read_text(encoding="utf-8"), ()
    except UnicodeDecodeError as exc: return None, (_diag(DiagnosticCode.ENCODING_ERROR, str(exc), str(path)),)
    except OSError as exc: return None, (_diag(DiagnosticCode.UNREADABLE_FILE, str(exc), str(path)),)

def parse_json_file(path: str | Path) -> ParseResult:
    text, ds=_read(path)
    if ds: return ParseResult(None, ds, str(path), "json", None)
    return parse_json_text(text, str(path))

def parse_yaml_file(path: str | Path) -> ParseResult:
    text, ds=_read(path)
    if ds: return ParseResult(None, ds, str(path), "yaml", None)
    return parse_yaml_text(text, str(path))

def parse_file(path: str | Path, explicit_format: str | None=None) -> ParseResult:
    fmt, ds=detect_format(path, explicit_format=explicit_format)
    if ds or fmt is None: return ParseResult(None, ds, str(path), fmt, None)
    text, rds=_read(path)
    if rds: return ParseResult(None, rds, str(path), fmt, None)
    return _pipeline(text, fmt, str(path))
