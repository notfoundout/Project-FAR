"""Typed external FAR IR interchange models and conversion helpers."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any, ClassVar, Mapping, TypeVar

from .core import IDENTIFIER_PATTERN_TEXT, IRKind, Identifier, Reference
from .diagnostics import Diagnostic, DiagnosticCode, DiagnosticSeverity, SourceLocation
from .ir import (
    Assumption, Claim, Dependency, Evidence, FARDocument, GraphEdge, GraphEdgeKind,
    GraphNode, GraphNodeKind, Interpretation, Investigation, Operation, Proof,
    ReasoningGraph, ReasoningStep, Representation, RepresentationalStructure,
)

FORMAT_VERSION = "far-ir/1.0"

EXTERNAL_DIAGNOSTIC_MESSAGES = {
    "FAR-EXT-001": "unsupported format version",
    "FAR-EXT-002": "invalid external object kind",
    "FAR-EXT-003": "unknown core field",
    "FAR-EXT-004": "missing external field",
    "FAR-EXT-005": "external field type mismatch",
    "FAR-EXT-006": "schema constraint violation",
    "FAR-EXT-007": "lossy conversion attempt",
}

class ExternalDiagnosticCode(StrEnum):
    UNSUPPORTED_FORMAT_VERSION = "FAR-EXT-001"
    INVALID_EXTERNAL_OBJECT_KIND = "FAR-EXT-002"
    UNKNOWN_CORE_FIELD = "FAR-EXT-003"
    MISSING_EXTERNAL_FIELD = "FAR-EXT-004"
    EXTERNAL_FIELD_TYPE_MISMATCH = "FAR-EXT-005"
    SCHEMA_CONSTRAINT_VIOLATION = "FAR-EXT-006"
    LOSSY_CONVERSION_ATTEMPT = "FAR-EXT-007"


def _diag(code: ExternalDiagnosticCode, message: str, related: str | None = None) -> Diagnostic:
    return Diagnostic(DiagnosticCode(code.value), DiagnosticSeverity.ERROR, message, related_identifier=related)

def _frozen(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))

def _expect(data: Mapping[str, Any], allowed: set[str], required: set[str]) -> list[Diagnostic]:
    out=[]
    for k in data:
        if k not in allowed:
            out.append(_diag(ExternalDiagnosticCode.UNKNOWN_CORE_FIELD, f"unknown core field: {k}"))
    for k in required:
        if k not in data:
            out.append(_diag(ExternalDiagnosticCode.MISSING_EXTERNAL_FIELD, f"missing external field: {k}"))
    return out

def _metadata(data: Mapping[str, Any]) -> Mapping[str, Any]:
    return _frozen(data.get("metadata", {}))

def _extensions(data: Mapping[str, Any]) -> Mapping[str, Any]:
    return _frozen(data.get("extensions", {}))

def _source(data: Any) -> SourceLocation | None:
    if data is None:
        return None
    return SourceLocation(data.get("source", ""), data.get("line"), data.get("column"), data.get("end_line"), data.get("end_column"))

def _source_dict(source: SourceLocation | None) -> dict[str, Any] | None:
    if source is None:
        return None
    return {k: v for k, v in {"source": source.source, "line": source.line, "column": source.column, "end_line": source.end_line, "end_column": source.end_column}.items() if v is not None}

def _ref(data: Mapping[str, Any]) -> Reference:
    kind = data.get("expected_kind")
    return Reference(Identifier(data["identifier"]), IRKind(kind) if kind is not None else None, _source(data.get("source")))

def _ref_dict(ref: Reference) -> dict[str, Any]:
    out={"identifier": str(ref.identifier), "expected_kind": ref.expected_kind.value if ref.expected_kind else None, "source": _source_dict(ref.source)}
    return out

T = TypeVar("T", bound="ExternalObject")

@dataclass(frozen=True, slots=True)
class ExternalObject:
    id: str
    kind: str
    source: SourceLocation | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    extensions: Mapping[str, Any] = field(default_factory=dict)
    allowed_fields: ClassVar[set[str]] = {"id","kind","source","metadata","extensions"}
    required_fields: ClassVar[set[str]] = {"id","kind"}
    expected_kind: ClassVar[str] = ""
    def __post_init__(self):
        object.__setattr__(self,"metadata",_frozen(self.metadata)); object.__setattr__(self,"extensions",_frozen(self.extensions))
    @classmethod
    def validate_mapping(cls, data: Mapping[str, Any]) -> tuple[Diagnostic,...]:
        ds=_expect(data, cls.allowed_fields, cls.required_fields)
        if data.get("kind") != cls.expected_kind:
            ds.append(_diag(ExternalDiagnosticCode.INVALID_EXTERNAL_OBJECT_KIND, f"expected kind {cls.expected_kind}, got {data.get('kind')}"))
        if "id" in data and not isinstance(data["id"], str):
            ds.append(_diag(ExternalDiagnosticCode.EXTERNAL_FIELD_TYPE_MISMATCH,"id must be a string"))
        return tuple(ds)
    def common_diags(self):
        return Identifier(self.id).validate() + (() if self.source is None else self.source.validate())

@dataclass(frozen=True, slots=True)
class ExternalRepresentation(ExternalObject):
    content: str = ""
    expected_kind: ClassVar[str] = "representation"
    allowed_fields: ClassVar[set[str]] = ExternalObject.allowed_fields | {"content"}
    required_fields: ClassVar[set[str]] = {"id","kind","content"}
    def to_ir(self): return Representation(Identifier(self.id), self.source, self.metadata, self.content)
    @classmethod
    def from_mapping(cls,data): return cls(data.get("id",""),data.get("kind",""),_source(data.get("source")),_metadata(data),_extensions(data),data.get("content",""))

@dataclass(frozen=True, slots=True)
class ExternalStructure(ExternalObject):
    representations: tuple[Reference,...] = (); description: str = ""
    expected_kind: ClassVar[str] = "structure"; allowed_fields: ClassVar[set[str]] = ExternalObject.allowed_fields | {"representations","description"}; required_fields: ClassVar[set[str]]={"id","kind","description","representations"}
    def to_ir(self): return RepresentationalStructure(Identifier(self.id), self.source, self.metadata, self.representations, self.description)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""),d.get("kind",""),_source(d.get("source")),_metadata(d),_extensions(d),tuple(_ref(x) for x in d.get("representations",[])),d.get("description",""))

@dataclass(frozen=True, slots=True)
class ExternalInterpretation(ExternalObject):
    representation: Reference = field(default_factory=lambda: Reference(Identifier("missing"),IRKind.REPRESENTATION)); meaning: str = ""
    expected_kind: ClassVar[str]="interpretation"; allowed_fields: ClassVar[set[str]]=ExternalObject.allowed_fields | {"representation","meaning"}; required_fields: ClassVar[set[str]]={"id","kind","representation","meaning"}
    def to_ir(self): return Interpretation(Identifier(self.id), self.source, self.metadata, self.representation, self.meaning)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""),d.get("kind",""),_source(d.get("source")),_metadata(d),_extensions(d),_ref(d.get("representation",{"identifier":"missing"})),d.get("meaning",""))

@dataclass(frozen=True, slots=True)
class ExternalInvestigation(ExternalObject):
    question: str=""; scope: str=""
    expected_kind: ClassVar[str]="investigation"; allowed_fields: ClassVar[set[str]]=ExternalObject.allowed_fields | {"question","scope"}; required_fields: ClassVar[set[str]]={"id","kind","question"}
    def to_ir(self): return Investigation(Identifier(self.id), self.source, self.metadata, self.question, self.scope)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""),d.get("kind",""),_source(d.get("source")),_metadata(d),_extensions(d),d.get("question",""),d.get("scope",""))

@dataclass(frozen=True, slots=True)
class ExternalStatementObject(ExternalObject):
    statement: str=""
    allowed_fields: ClassVar[set[str]]=ExternalObject.allowed_fields | {"statement"}; required_fields: ClassVar[set[str]]={"id","kind","statement"}

class ExternalClaim(ExternalStatementObject):
    expected_kind: ClassVar[str]="claim"
    def to_ir(self): return Claim(Identifier(self.id), self.source, self.metadata, self.statement)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""),d.get("kind",""),_source(d.get("source")),_metadata(d),_extensions(d),d.get("statement",""))
class ExternalAssumption(ExternalStatementObject):
    expected_kind: ClassVar[str]="assumption"
    def to_ir(self): return Assumption(Identifier(self.id), self.source, self.metadata, self.statement)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""),d.get("kind",""),_source(d.get("source")),_metadata(d),_extensions(d),d.get("statement",""))

@dataclass(frozen=True, slots=True)
class ExternalEvidence(ExternalObject):
    description: str=""; cites: tuple[Reference,...]=()
    expected_kind: ClassVar[str]="evidence"; allowed_fields: ClassVar[set[str]]=ExternalObject.allowed_fields | {"description","cites"}; required_fields: ClassVar[set[str]]={"id","kind","description"}
    def to_ir(self): return Evidence(Identifier(self.id), self.source, self.metadata, self.description, self.cites)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""),d.get("kind",""),_source(d.get("source")),_metadata(d),_extensions(d),d.get("description",""),tuple(_ref(x) for x in d.get("cites",[])))

@dataclass(frozen=True, slots=True)
class ExternalOperation(ExternalObject):
    description: str=""; inputs: tuple[Reference,...]=(); outputs: tuple[Reference,...]=()
    expected_kind: ClassVar[str]="operation"; allowed_fields: ClassVar[set[str]]=ExternalObject.allowed_fields | {"description","inputs","outputs"}; required_fields: ClassVar[set[str]]={"id","kind","description"}
    def to_ir(self): return Operation(Identifier(self.id), self.source, self.metadata, self.description, self.inputs, self.outputs)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""),d.get("kind",""),_source(d.get("source")),_metadata(d),_extensions(d),d.get("description",""),tuple(_ref(x) for x in d.get("inputs",[])),tuple(_ref(x) for x in d.get("outputs",[])))

@dataclass(frozen=True, slots=True)
class ExternalReasoningStep(ExternalObject):
    order:int=0; operation:Reference|None=None; premises:tuple[Reference,...]=(); conclusions:tuple[Reference,...]=(); rationale:str=""
    expected_kind: ClassVar[str]="reasoning_step"; allowed_fields: ClassVar[set[str]]=ExternalObject.allowed_fields | {"order","operation","premises","conclusions","rationale"}; required_fields: ClassVar[set[str]]={"id","kind","order","rationale"}
    def to_ir(self): return ReasoningStep(Identifier(self.id), self.source, self.metadata, self.order, self.operation, self.premises, self.conclusions, self.rationale)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""),d.get("kind",""),_source(d.get("source")),_metadata(d),_extensions(d),d.get("order",0), _ref(d["operation"]) if d.get("operation") else None, tuple(_ref(x) for x in d.get("premises",[])), tuple(_ref(x) for x in d.get("conclusions",[])), d.get("rationale",""))

@dataclass(frozen=True, slots=True)
class ExternalDependency(ExternalObject):
    source_ref:Reference=field(default_factory=lambda:Reference(Identifier("missing"))); target_ref:Reference=field(default_factory=lambda:Reference(Identifier("missing"))); relation:str="depends_on"
    expected_kind: ClassVar[str]="dependency"; allowed_fields: ClassVar[set[str]]=ExternalObject.allowed_fields | {"source_ref","target_ref","relation"}; required_fields: ClassVar[set[str]]={"id","kind","source_ref","target_ref","relation"}
    def to_ir(self): return Dependency(Identifier(self.id), self.source, self.metadata, self.source_ref, self.target_ref, self.relation)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""),d.get("kind",""),_source(d.get("source")),_metadata(d),_extensions(d),_ref(d.get("source_ref",{"identifier":"missing"})),_ref(d.get("target_ref",{"identifier":"missing"})),d.get("relation","depends_on"))

@dataclass(frozen=True, slots=True)
class ExternalProof(ExternalObject):
    claim:Reference=field(default_factory=lambda:Reference(Identifier("missing"),IRKind.CLAIM)); steps:tuple[Reference,...]=(); assumptions:tuple[Reference,...]=(); evidence:tuple[Reference,...]=()
    expected_kind: ClassVar[str]="proof"; allowed_fields: ClassVar[set[str]]=ExternalObject.allowed_fields | {"claim","steps","assumptions","evidence"}; required_fields: ClassVar[set[str]]={"id","kind","claim"}
    def to_ir(self): return Proof(Identifier(self.id), self.source, self.metadata, self.claim, self.steps, self.assumptions, self.evidence)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""),d.get("kind",""),_source(d.get("source")),_metadata(d),_extensions(d),_ref(d.get("claim",{"identifier":"missing"})),tuple(_ref(x) for x in d.get("steps",[])),tuple(_ref(x) for x in d.get("assumptions",[])),tuple(_ref(x) for x in d.get("evidence",[])))

MODEL_BY_KIND={c.expected_kind:c for c in [ExternalRepresentation,ExternalStructure,ExternalInterpretation,ExternalInvestigation,ExternalClaim,ExternalAssumption,ExternalEvidence,ExternalOperation,ExternalReasoningStep,ExternalDependency,ExternalProof]}

@dataclass(frozen=True, slots=True)
class ExternalGraphNode:
    id:str; kind:GraphNodeKind; source:SourceLocation|None=None; metadata:Mapping[str,Any]=field(default_factory=dict); extensions:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self): object.__setattr__(self,"metadata",_frozen(self.metadata)); object.__setattr__(self,"extensions",_frozen(self.extensions))
    def to_ir(self): return GraphNode(Identifier(self.id), self.kind, self.source, self.metadata)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""), GraphNodeKind(d.get("kind")), _source(d.get("source")), _metadata(d), _extensions(d))

@dataclass(frozen=True, slots=True)
class ExternalGraphEdge:
    id:str; kind:GraphEdgeKind; source_ref:Reference; target_ref:Reference; provenance:SourceLocation|None=None; metadata:Mapping[str,Any]=field(default_factory=dict); extensions:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self): object.__setattr__(self,"metadata",_frozen(self.metadata)); object.__setattr__(self,"extensions",_frozen(self.extensions))
    def to_ir(self): return GraphEdge(Identifier(self.id), self.kind, self.source_ref, self.target_ref, self.provenance, self.metadata)
    @classmethod
    def from_mapping(cls,d): return cls(d.get("id",""), GraphEdgeKind(d.get("kind")), _ref(d.get("source_ref",{"identifier":"missing"})), _ref(d.get("target_ref",{"identifier":"missing"})), _source(d.get("provenance")), _metadata(d), _extensions(d))

@dataclass(frozen=True, slots=True)
class ExternalReasoningGraph:
    nodes:tuple[ExternalGraphNode,...]=(); edges:tuple[ExternalGraphEdge,...]=(); metadata:Mapping[str,Any]=field(default_factory=dict); extensions:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self): object.__setattr__(self,"metadata",_frozen(self.metadata)); object.__setattr__(self,"extensions",_frozen(self.extensions))
    def to_ir(self): return ReasoningGraph(tuple(n.to_ir() for n in self.nodes), tuple(e.to_ir() for e in self.edges), self.metadata)
    @classmethod
    def from_mapping(cls,d): return cls(tuple(ExternalGraphNode.from_mapping(x) for x in d.get("nodes",[])), tuple(ExternalGraphEdge.from_mapping(x) for x in d.get("edges",[])), _metadata(d), _extensions(d))

@dataclass(frozen=True, slots=True)
class ExternalFARDocument:
    format_version:str; id:str; investigation:ExternalInvestigation; representations:tuple[ExternalRepresentation,...]=(); structures:tuple[ExternalStructure,...]=(); interpretations:tuple[ExternalInterpretation,...]=(); claims:tuple[ExternalClaim,...]=(); assumptions:tuple[ExternalAssumption,...]=(); evidence:tuple[ExternalEvidence,...]=(); operations:tuple[ExternalOperation,...]=(); reasoning_steps:tuple[ExternalReasoningStep,...]=(); dependencies:tuple[ExternalDependency,...]=(); proofs:tuple[ExternalProof,...]=(); graph:ExternalReasoningGraph|None=None; source:SourceLocation|None=None; metadata:Mapping[str,Any]=field(default_factory=dict); extensions:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self): object.__setattr__(self,"metadata",_frozen(self.metadata)); object.__setattr__(self,"extensions",_frozen(self.extensions))
    @classmethod
    def validate_mapping(cls,data:Mapping[str,Any])->tuple[Diagnostic,...]:
        allowed={"format_version","id","investigation","representations","structures","interpretations","claims","assumptions","evidence","operations","reasoning_steps","dependencies","proofs","graph","source","metadata","extensions"}
        ds=_expect(data,allowed,{"format_version","id","investigation"})
        if data.get("format_version") != FORMAT_VERSION:
            ds.append(_diag(ExternalDiagnosticCode.UNSUPPORTED_FORMAT_VERSION, f"expected {FORMAT_VERSION}, got {data.get('format_version')}", data.get("id") if isinstance(data.get("id"),str) else None))
        for k in ("representations","structures","interpretations","claims","assumptions","evidence","operations","reasoning_steps","dependencies","proofs"):
            if k in data and not isinstance(data[k], list): ds.append(_diag(ExternalDiagnosticCode.EXTERNAL_FIELD_TYPE_MISMATCH, f"{k} must be an array"))
        return tuple(ds)
    @classmethod
    def from_mapping(cls,data:Mapping[str,Any])->tuple["ExternalFARDocument|None",tuple[Diagnostic,...]]:
        ds=list(cls.validate_mapping(data))
        if ds: return None, tuple(ds)
        try:
            doc=cls(data["format_version"], data["id"], ExternalInvestigation.from_mapping(data["investigation"]), tuple(ExternalRepresentation.from_mapping(x) for x in data.get("representations",[])), tuple(ExternalStructure.from_mapping(x) for x in data.get("structures",[])), tuple(ExternalInterpretation.from_mapping(x) for x in data.get("interpretations",[])), tuple(ExternalClaim.from_mapping(x) for x in data.get("claims",[])), tuple(ExternalAssumption.from_mapping(x) for x in data.get("assumptions",[])), tuple(ExternalEvidence.from_mapping(x) for x in data.get("evidence",[])), tuple(ExternalOperation.from_mapping(x) for x in data.get("operations",[])), tuple(ExternalReasoningStep.from_mapping(x) for x in data.get("reasoning_steps",[])), tuple(ExternalDependency.from_mapping(x) for x in data.get("dependencies",[])), tuple(ExternalProof.from_mapping(x) for x in data.get("proofs",[])), ExternalReasoningGraph.from_mapping(data["graph"]) if data.get("graph") is not None else None, _source(data.get("source")), _metadata(data), _extensions(data))
        except Exception as exc:
            return None, (_diag(ExternalDiagnosticCode.SCHEMA_CONSTRAINT_VIOLATION, str(exc)),)
        pairs = [(doc.investigation, data["investigation"])]
        for objects, raw_items in (
            (doc.representations, data.get("representations", [])),
            (doc.structures, data.get("structures", [])),
            (doc.interpretations, data.get("interpretations", [])),
            (doc.claims, data.get("claims", [])),
            (doc.assumptions, data.get("assumptions", [])),
            (doc.evidence, data.get("evidence", [])),
            (doc.operations, data.get("operations", [])),
            (doc.reasoning_steps, data.get("reasoning_steps", [])),
            (doc.dependencies, data.get("dependencies", [])),
            (doc.proofs, data.get("proofs", [])),
        ):
            pairs.extend(zip(objects, raw_items))
        ds.extend(Identifier(doc.id).validate())
        if doc.source is not None:
            ds.extend(doc.source.validate())
        for obj, raw in pairs:
            ds.extend(obj.validate_mapping(raw))
            ds.extend(obj.common_diags())
        return doc, tuple(ds)
    def to_ir(self)->tuple[FARDocument,tuple[Diagnostic,...]]:
        ir=FARDocument(Identifier(self.id), self.investigation.to_ir(), tuple(x.to_ir() for x in self.representations), tuple(x.to_ir() for x in self.structures), tuple(x.to_ir() for x in self.interpretations), tuple(x.to_ir() for x in self.claims), tuple(x.to_ir() for x in self.assumptions), tuple(x.to_ir() for x in self.evidence), tuple(x.to_ir() for x in self.operations), tuple(x.to_ir() for x in self.reasoning_steps), tuple(x.to_ir() for x in self.dependencies), tuple(x.to_ir() for x in self.proofs), self.graph.to_ir() if self.graph else None, self.source, self.metadata)
        return ir, ir.validate()
    @classmethod
    def from_ir(cls,doc:FARDocument)->tuple["ExternalFARDocument",tuple[Diagnostic,...]]:
        ext=cls(FORMAT_VERSION,str(doc.identifier),ExternalInvestigation(str(doc.investigation.identifier),"investigation",doc.investigation.source,doc.investigation.metadata,{},doc.investigation.question,doc.investigation.scope),tuple(ExternalRepresentation(str(x.identifier),"representation",x.source,x.metadata,{},x.content) for x in doc.representations),tuple(ExternalStructure(str(x.identifier),"structure",x.source,x.metadata,{},x.representations,x.description) for x in doc.structures),tuple(ExternalInterpretation(str(x.identifier),"interpretation",x.source,x.metadata,{},x.representation,x.meaning) for x in doc.interpretations),tuple(ExternalClaim(str(x.identifier),"claim",x.source,x.metadata,{},x.statement) for x in doc.claims),tuple(ExternalAssumption(str(x.identifier),"assumption",x.source,x.metadata,{},x.statement) for x in doc.assumptions),tuple(ExternalEvidence(str(x.identifier),"evidence",x.source,x.metadata,{},x.description,x.cites) for x in doc.evidence),tuple(ExternalOperation(str(x.identifier),"operation",x.source,x.metadata,{},x.description,x.inputs,x.outputs) for x in doc.operations),tuple(ExternalReasoningStep(str(x.identifier),"reasoning_step",x.source,x.metadata,{},x.order,x.operation,x.premises,x.conclusions,x.rationale) for x in doc.reasoning_steps),tuple(ExternalDependency(str(x.identifier),"dependency",x.source,x.metadata,{},x.source_ref,x.target_ref,x.relation) for x in doc.dependencies),tuple(ExternalProof(str(x.identifier),"proof",x.source,x.metadata,{},x.claim,x.steps,x.assumptions,x.evidence) for x in doc.proofs),None if doc.graph is None else ExternalReasoningGraph(tuple(ExternalGraphNode(str(n.identifier),n.node_kind,n.source,n.metadata,{}) for n in doc.graph.nodes),tuple(ExternalGraphEdge(str(e.identifier),e.edge_kind,e.source,e.target,e.provenance,e.metadata,{}) for e in doc.graph.edges),doc.graph.metadata,{}),doc.source,doc.metadata,{})
        return ext, ()
