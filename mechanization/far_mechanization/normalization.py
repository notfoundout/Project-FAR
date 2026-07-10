"""Deterministic normalization for FAR mechanization external models."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .diagnostics import Diagnostic
from .external_models import ExternalFARDocument

@dataclass(frozen=True, slots=True)
class NormalizationResult:
    document: ExternalFARDocument | None
    diagnostics: tuple[Diagnostic, ...] = ()
    @property
    def success(self) -> bool: return self.document is not None and not self.diagnostics

def sort_mapping(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: sort_mapping(value[k]) for k in sorted(value)}
    if isinstance(value, tuple):
        return tuple(sort_mapping(v) for v in value)
    if isinstance(value, list):
        return [sort_mapping(v) for v in value]
    return value

def normalize_external_document(document: ExternalFARDocument) -> NormalizationResult:
    # Prompt 3 normalization is structural and semantics-preserving. It does not
    # reorder reasoning_steps because their order field is meaningful.
    normalized = ExternalFARDocument(
        document.format_version,
        document.id,
        document.investigation,
        tuple(sorted(document.representations, key=lambda x: x.id)),
        tuple(sorted(document.structures, key=lambda x: x.id)),
        tuple(sorted(document.interpretations, key=lambda x: x.id)),
        tuple(sorted(document.claims, key=lambda x: x.id)),
        tuple(sorted(document.assumptions, key=lambda x: x.id)),
        tuple(sorted(document.evidence, key=lambda x: x.id)),
        tuple(sorted(document.operations, key=lambda x: x.id)),
        document.reasoning_steps,
        tuple(sorted(document.dependencies, key=lambda x: x.id)),
        tuple(sorted(document.proofs, key=lambda x: x.id)),
        document.graph,
        document.source,
        sort_mapping(document.metadata),
        sort_mapping(document.extensions),
    )
    if normalized.graph is not None:
        from .external_models import ExternalReasoningGraph
        object.__setattr__(normalized, "graph", ExternalReasoningGraph(
            tuple(sorted(normalized.graph.nodes, key=lambda x: x.id)),
            tuple(sorted(normalized.graph.edges, key=lambda x: x.id)),
            sort_mapping(normalized.graph.metadata),
            sort_mapping(normalized.graph.extensions),
        ))
    return NormalizationResult(normalized, ())

def normalize_ir_document(document):
    external, diagnostics = ExternalFARDocument.from_ir(document)
    if diagnostics:
        return NormalizationResult(None, diagnostics)
    return normalize_external_document(external)
