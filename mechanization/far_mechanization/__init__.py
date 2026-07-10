"""Project FAR mechanization package."""

from .core import IDENTIFIER_PATTERN_TEXT, IRKind, Identifier, Reference
from .diagnostics import Diagnostic, DiagnosticCode, DiagnosticSeverity, SourceLocation
from .external_models import *
from .normalization import *
from .parser import *
from .serialization import *
from .graph_engine import *
from .ir import *

__all__ = [name for name in globals() if not name.startswith("_")]
