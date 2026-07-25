from __future__ import annotations

import importlib
import sys

_core_name = "validated_execute_controller_core"
if _core_name in sys.modules:
    _core = importlib.reload(sys.modules[_core_name])
else:
    _core = importlib.import_module(_core_name)

from validated_execution_hardening import install

install(_core)
for _key in dir(_core):
    if not _key.startswith("__"):
        globals()[_key] = getattr(_core, _key)

if __name__ == "__main__":
    _core.main()
