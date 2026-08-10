"""Hardened entrypoint for the exploratory compositional-invariant verifier."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

_LEGACY_PATH = Path(__file__).with_name("verify_compositional_invariant_legacy.py")
_LEGACY_SPEC = importlib.util.spec_from_file_location(
    "_target_category_compositional_legacy", _LEGACY_PATH
)
if _LEGACY_SPEC is None or _LEGACY_SPEC.loader is None:
    raise ImportError(f"cannot load legacy compositional verifier: {_LEGACY_PATH}")
_core = importlib.util.module_from_spec(_LEGACY_SPEC)
sys.modules[_LEGACY_SPEC.name] = _core
_LEGACY_SPEC.loader.exec_module(_core)


_original_read_utf8 = _core._read_utf8
_original_validate_gate = _core.validate_gate
_original_verify = _core.verify
EXPECTED_RG07_REQUIRED_BEFORE = ["evidence_release", "theorem_release"]


def _read_utf8(path: Path):
    if path.is_symlink() or not path.is_file():
        raise _core.VerificationError(f"required artifact must be a regular non-symlink file: {path}")
    return _original_read_utf8(path)


def validate_gate(gates_path: Path) -> None:
    """Preserve the complete RG-07 release boundary, not only theorem release."""
    gates = _core.load_json(gates_path)
    entries = gates.get("gates")
    rg07 = [item for item in entries if isinstance(item, dict) and item.get("id") == "RG-07"] if isinstance(entries, list) else []
    if len(rg07) != 1 or rg07[0].get("required_before") != EXPECTED_RG07_REQUIRED_BEFORE:
        raise _core.VerificationError("RG-07 must remain required before evidence_release and theorem_release exactly")
    # Run the complete legacy state validation only after the exact release-boundary
    # contract has been checked so every boundary mutation has one stable error contract.
    _original_validate_gate(gates_path)


_core._read_utf8 = _read_utf8
_core.validate_gate = validate_gate

for _name, _value in vars(_core).items():
    if not _name.startswith("__"):
        globals()[_name] = _value

# Re-export the hardened gate validator after copying legacy globals.
globals()["validate_gate"] = validate_gate


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
    # The first two executable statements are fail-closed authority gates.
    # The weakening detector requires this exact unconditional live prefix.
    validate_empirical_authority(empirical_charter_path, empirical_manifest_path, audit_path)
    validate_gate(gates_path)
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
    return result


_core.verify = verify


def main() -> int:
    return _core.main()


if __name__ == "__main__":
    raise SystemExit(main())
