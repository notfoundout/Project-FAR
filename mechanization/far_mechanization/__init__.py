"""Project FAR mechanization package."""

__version__ = "0.6.0"

from .core import IDENTIFIER_PATTERN_TEXT, IRKind, Identifier, Reference
from .diagnostics import Diagnostic, DiagnosticCode, DiagnosticSeverity, SourceLocation
from .external_models import *
from .normalization import *
from .graph_engine import *
from .ir import *

# The parser/serializer convenience exports require PyYAML.  Keep package import
# dependency-light so independent submodules such as ``intake_v1`` remain usable
# from a relocated wheel even when optional application dependencies are absent.
try:
    import yaml as _yaml  # noqa: F401
except ModuleNotFoundError:
    _yaml = None
else:
    from .parser import *
    from .serialization import *

__all__ = [name for name in globals() if not name.startswith("_")]
