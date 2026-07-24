"""FAR decision-integrity core."""

from .adjudicate import Adjudication, Finding, adjudicate
from .io import load_package
from .model import (
    SCHEMA_VERSION,
    DecisionNode,
    DecisionPackage,
    Dependency,
    IntegrityStatus,
    PackageValidationError,
)
from .report import report_payload, write_report

__all__ = [
    "Adjudication",
    "DecisionNode",
    "DecisionPackage",
    "Dependency",
    "Finding",
    "IntegrityStatus",
    "PackageValidationError",
    "SCHEMA_VERSION",
    "adjudicate",
    "load_package",
    "report_payload",
    "write_report",
]

__version__ = "0.2.0"
