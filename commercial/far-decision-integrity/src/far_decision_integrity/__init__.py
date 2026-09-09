"""FAR decision-integrity core."""

from .adjudicate import Adjudication, Finding, adjudicate
from .io import load_package
from .model import (
    LEGACY_SCHEMA_VERSION,
    SCHEMA_VERSION,
    SEMANTIC_SCHEMA_VERSION,
    SUPPORTED_SCHEMA_VERSIONS,
    DecisionNode,
    DecisionPackage,
    Dependency,
    IntegrityStatus,
    PackageValidationError,
)
from .report import report_payload, write_report
from .semantic_audit import (
    SemanticArtifact,
    SemanticAudit,
    SemanticDiagnostic,
    SemanticDisposition,
    SemanticVerifierUnavailable,
    audit_semantic_contract,
)

__all__ = [
    "Adjudication",
    "DecisionNode",
    "DecisionPackage",
    "Dependency",
    "Finding",
    "IntegrityStatus",
    "LEGACY_SCHEMA_VERSION",
    "PackageValidationError",
    "SCHEMA_VERSION",
    "SEMANTIC_SCHEMA_VERSION",
    "SUPPORTED_SCHEMA_VERSIONS",
    "SemanticArtifact",
    "SemanticAudit",
    "SemanticDiagnostic",
    "SemanticDisposition",
    "SemanticVerifierUnavailable",
    "adjudicate",
    "audit_semantic_contract",
    "load_package",
    "report_payload",
    "write_report",
]

__version__ = "1.0.0"
