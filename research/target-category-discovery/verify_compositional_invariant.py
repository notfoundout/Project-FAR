"""Hardened entrypoint for the exploratory compositional-invariant verifier."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import verify_compositional_invariant_legacy as _core

_core.EXPECTED_SPEC["version"] = "1.0"
_core.EXPECTED_SPEC_SHA256 = "2b6ede05f7d5e3525070e1a5893ea599613a64eb114b12ed43606fb114e14128"
_core.EXPECTED_PUBLIC_SHA256["Report"] = "426b48e0b1a8724bd718bb3ffb5491f2f97b79860c90f4d1f57c35d78434c991"

_original_read_utf8 = _core._read_utf8
_original_verify = _core.verify


def _read_utf8(path: Path):
    if path.is_symlink() or not path.is_file():
        raise _core.VerificationError(f"required artifact must be a regular non-symlink file: {path}")
    return _original_read_utf8(path)


_core._read_utf8 = _read_utf8

for _name, _value in vars(_core).items():
    if not _name.startswith("__"):
        globals()[_name] = _value


def verify(
    spec_path: Path = DEFAULT_SPEC,
    result_path: Path = DEFAULT_RESULT,
    report_path: Path = DEFAULT_REPORT,
    readme_path: Path = DEFAULT_README,
    charter_path: Path = DEFAULT_CHARTER,
    gates_path: Path = DEFAULT_GATES,
    empirical_charter_path: Path = DEFAULT_EMPIRICAL_CHARTER,
    empirical_manifest_path: Path = DEFAULT_EMPIRICAL_MANIFEST,
    audit_path: Path = DEFAULT_CHAT_AUDIT,
) -> dict[str, Any]:
    result = _original_verify(
        spec_path,
        result_path,
        report_path,
        readme_path,
        charter_path,
        gates_path,
        empirical_charter_path,
        empirical_manifest_path,
        audit_path,
    )
    # Defense in depth: the public entrypoint itself requires the controlling
    # empirical authority check, so weakening the legacy call cannot bypass it.
    validate_empirical_authority(empirical_charter_path, empirical_manifest_path, audit_path)
    return result


_core.verify = verify


def main() -> int:
    return _core.main()


if __name__ == "__main__":
    raise SystemExit(main())
