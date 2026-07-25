from __future__ import annotations

import importlib
import sys

_name = "validated_execute_controller_legacy"
if _name in sys.modules:
    _legacy = importlib.reload(sys.modules[_name])
else:
    _legacy = importlib.import_module(_name)

from validated_execution_hardening import install

install(_legacy)
for _key in dir(_legacy):
    if not _key.startswith("__"):
        globals()[_key] = getattr(_legacy, _key)

if __name__ == "__main__":
    _legacy.main()
