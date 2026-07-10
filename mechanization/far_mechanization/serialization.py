"""Deterministic JSON and YAML serialization for FAR mechanization."""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
import yaml
from .core import Reference
from .diagnostics import Diagnostic, DiagnosticCode, DiagnosticSeverity, SourceLocation
from .external_models import ExternalFARDocument
from .normalization import normalize_ir_document, normalize_external_document, sort_mapping

@dataclass(frozen=True, slots=True)
class SerializationResult:
    text: str | None
    diagnostics: tuple[Diagnostic, ...]
    output_format: str
    @property
    def success(self) -> bool: return self.text is not None and not self.diagnostics

def _diag(code: DiagnosticCode, msg: str, source: str | None=None):
    return Diagnostic(code, DiagnosticSeverity.ERROR, msg, SourceLocation(source) if source else None)

def _source_dict(s: SourceLocation | None):
    if s is None: return None
    return {k:v for k,v in {"source":s.source,"line":s.line,"column":s.column,"end_line":s.end_line,"end_column":s.end_column}.items() if v is not None}

def _ref_dict(r: Reference):
    return {k:v for k,v in {"identifier":str(r.identifier),"expected_kind":r.expected_kind.value if r.expected_kind else None,"source":_source_dict(r.source)}.items() if v is not None}

def _common(o, data):
    kind = o.kind.value if hasattr(o.kind, "value") else o.kind
    data = {"id": o.id, "kind": kind, **data}
    if getattr(o, "source", None) is not None: data["source"]=_source_dict(o.source)
    if o.metadata: data["metadata"]=sort_mapping(o.metadata)
    if o.extensions: data["extensions"]=sort_mapping(o.extensions)
    return data

def external_to_data(doc: ExternalFARDocument) -> dict[str, Any]:
    d={"format_version":doc.format_version,"id":doc.id,"investigation":_common(doc.investigation,{"question":doc.investigation.question})}
    if doc.investigation.scope: d["investigation"]["scope"]=doc.investigation.scope
    def add(name, items, fn):
        if items: d[name]=[fn(x) for x in items]
    add("representations", doc.representations, lambda x:_common(x,{"content":x.content}))
    add("structures", doc.structures, lambda x:_common(x,{"description":x.description,"representations":[_ref_dict(r) for r in x.representations]}))
    add("interpretations", doc.interpretations, lambda x:_common(x,{"representation":_ref_dict(x.representation),"meaning":x.meaning}))
    add("claims", doc.claims, lambda x:_common(x,{"statement":x.statement}))
    add("assumptions", doc.assumptions, lambda x:_common(x,{"statement":x.statement}))
    add("evidence", doc.evidence, lambda x:_common(x,{"description":x.description, **({"cites":[_ref_dict(r) for r in x.cites]} if x.cites else {})}))
    add("operations", doc.operations, lambda x:_common(x,{"description":x.description, **({"inputs":[_ref_dict(r) for r in x.inputs]} if x.inputs else {}), **({"outputs":[_ref_dict(r) for r in x.outputs]} if x.outputs else {})}))
    add("reasoning_steps", doc.reasoning_steps, lambda x:_common(x,{"order":x.order,"rationale":x.rationale, **({"operation":_ref_dict(x.operation)} if x.operation else {}), **({"premises":[_ref_dict(r) for r in x.premises]} if x.premises else {}), **({"conclusions":[_ref_dict(r) for r in x.conclusions]} if x.conclusions else {})}))
    add("dependencies", doc.dependencies, lambda x:_common(x,{"source_ref":_ref_dict(x.source_ref),"target_ref":_ref_dict(x.target_ref),"relation":x.relation}))
    add("proofs", doc.proofs, lambda x:_common(x,{"claim":_ref_dict(x.claim), **({"steps":[_ref_dict(r) for r in x.steps]} if x.steps else {}), **({"assumptions":[_ref_dict(r) for r in x.assumptions]} if x.assumptions else {}), **({"evidence":[_ref_dict(r) for r in x.evidence]} if x.evidence else {})}))
    if doc.graph is not None:
        d["graph"]={"nodes":[_common(n,{}) for n in doc.graph.nodes],"edges":[_common(e,{"source_ref":_ref_dict(e.source_ref),"target_ref":_ref_dict(e.target_ref), **({"provenance":_source_dict(e.provenance)} if e.provenance else {})}) for e in doc.graph.edges]}
        if doc.graph.metadata: d["graph"]["metadata"]=sort_mapping(doc.graph.metadata)
        if doc.graph.extensions: d["graph"]["extensions"]=sort_mapping(doc.graph.extensions)
    if doc.source is not None: d["source"]=_source_dict(doc.source)
    if doc.metadata: d["metadata"]=sort_mapping(doc.metadata)
    if doc.extensions: d["extensions"]=sort_mapping(doc.extensions)
    return sort_mapping(d)

def _normalized_external(document):
    if isinstance(document, ExternalFARDocument): return normalize_external_document(document)
    return normalize_ir_document(document)

def serialize_json(document) -> SerializationResult:
    norm=_normalized_external(document)
    if not norm.success: return SerializationResult(None, norm.diagnostics, "json")
    text=json.dumps(external_to_data(norm.document), ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True)+"\n"
    return SerializationResult(text, (), "json")

def serialize_yaml(document) -> SerializationResult:
    norm=_normalized_external(document)
    if not norm.success: return SerializationResult(None, norm.diagnostics, "yaml")
    text=yaml.safe_dump(external_to_data(norm.document), allow_unicode=True, sort_keys=True, default_flow_style=False)
    if not text.endswith("\n"): text += "\n"
    return SerializationResult(text, (), "yaml")

def write_json_file(document, path: str | Path) -> SerializationResult:
    result=serialize_json(document)
    if not result.success: return result
    try: Path(path).write_text(result.text, encoding="utf-8")
    except OSError as exc: return SerializationResult(None, (_diag(DiagnosticCode.FILE_WRITE_ERROR, str(exc), str(path)),), "json")
    return result

def write_yaml_file(document, path: str | Path) -> SerializationResult:
    result=serialize_yaml(document)
    if not result.success: return result
    try: Path(path).write_text(result.text, encoding="utf-8")
    except OSError as exc: return SerializationResult(None, (_diag(DiagnosticCode.FILE_WRITE_ERROR, str(exc), str(path)),), "yaml")
    return result
