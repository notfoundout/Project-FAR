from __future__ import annotations

import json
from pathlib import Path

from .model import DecisionPackage, PackageValidationError


def load_package(path: str | Path) -> DecisionPackage:
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except OSError as exc:
        raise PackageValidationError(f"unable to read decision package {source}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise PackageValidationError(
            f"decision package {source} is not valid JSON: {exc.msg}"
        ) from exc
    return DecisionPackage.from_dict(payload)
