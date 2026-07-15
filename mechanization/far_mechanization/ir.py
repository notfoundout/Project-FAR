"""Canonical storage-independent FAR Intermediate Representation."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import StrEnum
from typing import ClassVar, Mapping

from .core import IRKind, Identifier, Reference, freeze_metadata
from .diagnostics import Diagnostic, DiagnosticCode, DiagnosticSeverity, SourceLocation


class GraphNodeKind(StrEnum):
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


class GraphEdgeKind(StrEnum):
    DEPENDS_ON = "depends_on"
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    INTERPRETS = "interprets"
    SCOPES = "scopes"
    TRANSFORMS = "transforms"
    DERIVES = "derives"
    CITES = "cites"
    RECORDS = "records"


@dataclass(frozen=True, slots=True)
class _IRObject:
    identifier: Identifier
    source: SourceLocation | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)

    kind: ClassVar[IRKind]
    required_text_fields: ClassVar[tuple[str, ...]] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", freeze_metadata(self.metadata))

    def validate(self) -> tuple[Diagnostic, ...]:
        diagnostics = list(self.identifier.validate())
        if self.source is not None:
            diagnostics.extend(self.source.validate())
        for name in self.required_text_fields:
            if not getattr(self, name).strip():
                diagnostics.append(Diagnostic(DiagnosticCode.MISSING_REQUIRED_FIELD, DiagnosticSeverity.ERROR, f"{self.__class__.__name__}.{name} is required", related_identifier=str(self.identifier)))
        for f in fields(self):
            value = getattr(self, f.name)
            if isinstance(value, Reference):
                diagnostics.extend(value.validate())
            elif isinstance(value, tuple):
                for item in value:
                    if isinstance(item, Reference):
                        diagnostics.extend(item.validate())
        return tuple(diagnostics)


@dataclass(frozen=True, slots=True)
class Representation(_IRObject):
    content: str = ""
    kind = IRKind.REPRESENTATION
    required_text_fields = ("content",)


@dataclass(frozen=True, slots=True)
class RepresentationalStructure(_IRObject):
    representations: tuple[Reference, ...] = ()
    description: str = ""
    kind = IRKind.STRUCTURE
    required_text_fields = ("description",)


@dataclass(frozen=True, slots=True)
class Interpretation(_IRObject):
    representation: Reference = field(default_factory=lambda: Reference(Identifier("missing"), IRKind.REPRESENTATION))
    meaning: str = ""
    kind = IRKind.INTERPRETATION
    required_text_fields = ("meaning",)


@dataclass(frozen=True, slots=True)
class Investigation(_IRObject):
    question: str = ""
    scope: str = ""
    kind = IRKind.INVESTIGATION
    required_text_fields = ("question",)


@dataclass(frozen=True, slots=True)
class Claim(_IRObject):
    statement: str = ""
    kind = IRKind.CLAIM
    required_text_fields = ("statement",)


@dataclass(frozen=True, slots=True)
class Assumption(_IRObject):
    statement: str = ""
    kind = IRKind.ASSUMPTION
    required_text_fields = ("statement",)


@dataclass(frozen=True, slots=True)
class Evidence(_IRObject):
    description: str = ""
    cites: tuple[Reference, ...] = ()
    kind = IRKind.EVIDENCE
    required_text_fields = ("description",)


@dataclass(frozen=True, slots=True)
class Operation(_IRObject):
    description: str = ""
    inputs: tuple[Reference, ...] = ()
    outputs: tuple[Reference, ...] = ()
    kind = IRKind.OPERATION
    required_text_fields = ("description",)


@dataclass(frozen=True, slots=True)
class ReasoningStep(_IRObject):
    order: int = 0
    operation: Reference | None = None
    premises: tuple[Reference, ...] = ()
    conclusions: tuple[Reference, ...] = ()
    rationale: str = ""
    kind = IRKind.REASONING_STEP
    required_text_fields = ("rationale",)

    def validate(self) -> tuple[Diagnostic, ...]:
        diagnostics = list(_IRObject.validate(self))
        if self.order < 0:
            diagnostics.append(Diagnostic(DiagnosticCode.INVALID_INTERNAL_OBJECT_SHAPE, DiagnosticSeverity.ERROR, "reasoning step order must be non-negative", related_identifier=str(self.identifier)))
        return tuple(diagnostics)


@dataclass(frozen=True, slots=True)
class Dependency(_IRObject):
    source_ref: Reference = field(default_factory=lambda: Reference(Identifier("missing")))
    target_ref: Reference = field(default_factory=lambda: Reference(Identifier("missing")))
    relation: str = "depends_on"
    kind = IRKind.DEPENDENCY


@dataclass(frozen=True, slots=True)
class Proof(_IRObject):
    claim: Reference = field(default_factory=lambda: Reference(Identifier("missing"), IRKind.CLAIM))
    steps: tuple[Reference, ...] = ()
    assumptions: tuple[Reference, ...] = ()
    evidence: tuple[Reference, ...] = ()
    kind = IRKind.PROOF


@dataclass(frozen=True, slots=True)
class GraphNode:
    identifier: Identifier
    node_kind: GraphNodeKind
    source: SourceLocation | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", freeze_metadata(self.metadata))

    def validate(self) -> tuple[Diagnostic, ...]:
        diagnostics = list(self.identifier.validate())
        if self.source:
            diagnostics.extend(self.source.validate())
        return tuple(diagnostics)


@dataclass(frozen=True, slots=True)
class GraphEdge:
    identifier: Identifier
    edge_kind: GraphEdgeKind
    source: Reference
    target: Reference
    provenance: SourceLocation | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", freeze_metadata(self.metadata))

    def validate(self) -> tuple[Diagnostic, ...]:
        diagnostics = list(self.identifier.validate()) + list(self.source.validate()) + list(self.target.validate())
        if self.provenance:
            diagnostics.extend(self.provenance.validate())
        return tuple(diagnostics)


@dataclass(frozen=True, slots=True)
class ReasoningGraph:
    nodes: tuple[GraphNode, ...] = ()
    edges: tuple[GraphEdge, ...] = ()
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", freeze_metadata(self.metadata))

    def validate(self) -> tuple[Diagnostic, ...]:
        diagnostics: list[Diagnostic] = []
        seen: set[str] = set()
        for node in self.nodes:
            diagnostics.extend(node.validate())
            key = str(node.identifier)
            if key in seen:
                diagnostics.append(Diagnostic(DiagnosticCode.DUPLICATE_LOCAL_IDENTIFIER, DiagnosticSeverity.ERROR, f"duplicate graph node identifier: {key}", related_identifier=key))
            seen.add(key)
        for edge in self.edges:
            diagnostics.extend(edge.validate())
        return tuple(diagnostics)


@dataclass(frozen=True, slots=True)
class FARDocument:
    identifier: Identifier
    investigation: Investigation
    representations: tuple[Representation, ...] = ()
    structures: tuple[RepresentationalStructure, ...] = ()
    interpretations: tuple[Interpretation, ...] = ()
    claims: tuple[Claim, ...] = ()
    assumptions: tuple[Assumption, ...] = ()
    evidence: tuple[Evidence, ...] = ()
    operations: tuple[Operation, ...] = ()
    reasoning_steps: tuple[ReasoningStep, ...] = ()
    dependencies: tuple[Dependency, ...] = ()
    proofs: tuple[Proof, ...] = ()
    graph: ReasoningGraph | None = None
    source: SourceLocation | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", freeze_metadata(self.metadata))

    def validate(self) -> tuple[Diagnostic, ...]:
        diagnostics = list(self.identifier.validate()) + list(self.investigation.validate())
        if self.source:
            diagnostics.extend(self.source.validate())
        if self.graph:
            diagnostics.extend(self.graph.validate())
        seen: dict[str, str] = {}
        for collection_name in ("representations", "structures", "interpretations", "claims", "assumptions", "evidence", "operations", "reasoning_steps", "dependencies", "proofs"):
            for item in getattr(self, collection_name):
                diagnostics.extend(item.validate())
                key = str(item.identifier)
                if key in seen:
                    diagnostics.append(Diagnostic(DiagnosticCode.DUPLICATE_LOCAL_IDENTIFIER, DiagnosticSeverity.ERROR, f"duplicate FARDocument identifier: {key}", related_identifier=key, details={"first_collection": seen[key], "duplicate_collection": collection_name}))
                else:
                    seen[key] = collection_name
        return tuple(diagnostics)
