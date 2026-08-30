"""Conformance runner for the far-ir/2.0 comparison-contract successor."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .contract_v2 import load_and_validate

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFORMANCE_ROOT = REPO_ROOT / "conformance" / "far-ir-2.0"
MANIFEST_PATH = CONFORMANCE_ROOT / "manifest.json"


@dataclass(frozen=True, slots=True)
class CaseResult:
    case_id: str
    passed: bool
    expected_valid: bool
    actual_valid: bool
    expected_codes: tuple[str, ...]
    actual_codes: tuple[str, ...]


def load_manifest(path: str | Path = MANIFEST_PATH) -> Mapping[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_manifest(manifest: Mapping[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    if manifest.get("format_version") != "far-ir/2.0":
        errors.append("manifest format_version must be far-ir/2.0")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        return tuple(errors + ["cases must be a non-empty list"])
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append("case must be an object")
            continue
        required = {"id", "path", "expected_valid", "expected_codes", "obligation"}
        missing = required - set(case)
        if missing:
            errors.append(f"{case.get('id', '<unknown>')}: missing {sorted(missing)}")
        cid = str(case.get("id", ""))
        if not cid or cid in seen:
            errors.append(f"invalid or duplicate case id {cid!r}")
        seen.add(cid)
        if not isinstance(case.get("expected_codes"), list):
            errors.append(f"{cid}: expected_codes must be a list")
    return tuple(errors)


def run_manifest(path: str | Path = MANIFEST_PATH) -> tuple[CaseResult, ...]:
    manifest_path = Path(path)
    manifest = load_manifest(manifest_path)
    manifest_errors = validate_manifest(manifest)
    if manifest_errors:
        return tuple(CaseResult(f"manifest-{i}", False, True, False, (), (error,)) for i, error in enumerate(manifest_errors, 1))
    root = manifest_path.parent
    results: list[CaseResult] = []
    for case in manifest["cases"]:
        validation = load_and_validate(root / str(case["path"]))
        actual_codes = tuple(sorted({d.code for d in validation.diagnostics}))
        expected_codes = tuple(sorted(str(code) for code in case["expected_codes"]))
        expected_valid = bool(case["expected_valid"])
        results.append(CaseResult(str(case["id"]), validation.success == expected_valid and actual_codes == expected_codes, expected_valid, validation.success, expected_codes, actual_codes))
    return tuple(results)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m mechanization.far_mechanization.contract_conformance")
    parser.add_argument("--manifest", default=str(MANIFEST_PATH))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    results = run_manifest(args.manifest)
    success = bool(results) and all(item.passed for item in results)
    if args.json:
        print(json.dumps({"success": success, "passed": sum(item.passed for item in results), "total": len(results), "results": [asdict(item) for item in results]}, indent=2, sort_keys=True))
    else:
        print(f"far-ir/2.0 conformance: {sum(item.passed for item in results)}/{len(results)} passed")
        for item in results:
            print(f"{'PASS' if item.passed else 'FAIL'} {item.case_id} expected={item.expected_codes} actual={item.actual_codes}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
