"""Versioned FAR mechanization conformance runner for far-ir/1.0."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .diagnostics import Diagnostic
from .graph_engine import build_graph, graph_statistics, validate_dependencies, validate_graph
from .parser import parse_file
from .serialization import serialize_json, serialize_yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFORMANCE_ROOT = REPO_ROOT / "conformance" / "far-ir-1.0"
MANIFEST_PATH = CONFORMANCE_ROOT / "manifest.json"


@dataclass(frozen=True, slots=True)
class ConformanceCaseResult:
    case_id: str
    passed: bool
    expected_valid: bool
    actual_valid: bool
    expected_diagnostic_codes: tuple[str, ...]
    actual_diagnostic_codes: tuple[str, ...]
    message: str = ""


@dataclass(frozen=True, slots=True)
class ConformanceRunResult:
    suite: str
    passed: int
    failed: int
    total: int
    results: tuple[ConformanceCaseResult, ...]

    @property
    def success(self) -> bool:
        return self.failed == 0


def _diagnostic_codes(diagnostics: Sequence[Diagnostic]) -> tuple[str, ...]:
    return tuple(sorted({d.code.value for d in diagnostics}))


def load_manifest(path: str | Path = MANIFEST_PATH) -> Mapping[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_manifest(manifest: Mapping[str, Any]) -> tuple[str, ...]:
    errors: list[str] = []
    if manifest.get("format_version") != "far-ir/1.0":
        errors.append("manifest format_version must be far-ir/1.0")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("manifest cases must be a non-empty array")
        return tuple(errors)
    seen: set[str] = set()
    required = {"id", "title", "input_path", "input_format", "expected_validity", "expected_diagnostic_codes", "feature_category", "notes"}
    for case in cases:
        if not isinstance(case, dict):
            errors.append("case must be an object")
            continue
        missing = required - set(case)
        if missing:
            errors.append(f"{case.get('id', '<unknown>')}: missing {sorted(missing)}")
        cid = str(case.get("id", ""))
        if not cid:
            errors.append("case id must be non-empty")
        if cid in seen:
            errors.append(f"duplicate case id: {cid}")
        seen.add(cid)
        if not isinstance(case.get("expected_diagnostic_codes"), list):
            errors.append(f"{cid}: expected_diagnostic_codes must be an array")
    return tuple(errors)


def _case_path(case: Mapping[str, Any], root: Path) -> Path:
    return root / str(case["input_path"])


def _run_pipeline_case(case: Mapping[str, Any], root: Path) -> tuple[bool, tuple[str, ...], dict[str, Any]]:
    result = parse_file(_case_path(case, root), explicit_format=str(case.get("input_format")) if case.get("input_format") in {"json", "yaml"} else None)
    diagnostics = list(result.diagnostics)
    stats: dict[str, Any] = {}
    if result.document is not None:
        built = build_graph(result.document)
        diagnostics.extend(built.diagnostics)
        if built.graph is not None:
            graph_validation = validate_graph(built.graph, result.document)
            diagnostics.extend(graph_validation.diagnostics)
            diagnostics.extend(validate_dependencies(result.document, built.graph))
            stats = asdict(graph_statistics(built.graph, tuple(diagnostics)))
    return not diagnostics, _diagnostic_codes(diagnostics), stats


def _run_roundtrip_case(case: Mapping[str, Any], root: Path) -> tuple[bool, tuple[str, ...], dict[str, Any]]:
    result = parse_file(_case_path(case, root), explicit_format=str(case.get("input_format")))
    if not result.success or result.document is None:
        return False, _diagnostic_codes(result.diagnostics), {}
    serializer = serialize_yaml if str(case.get("roundtrip_format", "json")) == "yaml" else serialize_json
    serialized = serializer(result.document)
    if not serialized.success or serialized.text is None:
        return False, _diagnostic_codes(serialized.diagnostics), {}
    reparsed = parse_file(_case_path(case, root), explicit_format=str(case.get("input_format")))
    # Reparse the serialized text through a temporary file-free path by direct serializer format APIs.
    from .parser import parse_yaml_text, parse_json_text
    parsed_again = parse_yaml_text(serialized.text, "<roundtrip>") if serialized.output_format == "yaml" else parse_json_text(serialized.text, "<roundtrip>")
    return parsed_again.success and parsed_again.document == reparsed.document, _diagnostic_codes(parsed_again.diagnostics), {}


def _run_cli_case(case: Mapping[str, Any], root: Path) -> tuple[bool, tuple[str, ...], dict[str, Any]]:
    command = str(case.get("cli_command", "validate"))
    args = [sys.executable, str(REPO_ROOT / "far"), command]
    if case.get("json_output"):
        args.extend(["--output", "json"])
    if case.get("input_path"):
        args.append(str(_case_path(case, root)))
    if case.get("identifier"):
        args.append(str(case["identifier"]))
    completed = subprocess.run(args, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    expected_exit = int(case.get("expected_exit", 0 if case.get("expected_validity") else 1))
    ok = completed.returncode == expected_exit
    codes: tuple[str, ...] = ()
    if completed.stdout.strip().startswith("{"):
        try:
            payload = json.loads(completed.stdout)
            diagnostics = payload.get("diagnostics", []) if isinstance(payload, dict) else []
            codes = tuple(sorted({d.get("code", "") for d in diagnostics if isinstance(d, dict) and d.get("code")}))
        except json.JSONDecodeError:
            ok = False
    return ok, codes, {"exit_code": completed.returncode}


def run_case(case: Mapping[str, Any], root: str | Path = CONFORMANCE_ROOT) -> ConformanceCaseResult:
    root_path = Path(root)
    action = str(case.get("action", "pipeline"))
    if action == "cli":
        actual_valid, actual_codes, stats = _run_cli_case(case, root_path)
    elif action == "roundtrip":
        actual_valid, actual_codes, stats = _run_roundtrip_case(case, root_path)
    else:
        actual_valid, actual_codes, stats = _run_pipeline_case(case, root_path)
    expected_valid = bool(case["expected_validity"])
    expected_codes = tuple(sorted(case.get("expected_diagnostic_codes", [])))
    expected_stats = case.get("expected_graph_statistics") or {}
    stats_ok = all(stats.get(k) == v for k, v in expected_stats.items())
    passed = actual_valid == expected_valid and actual_codes == expected_codes and stats_ok
    msg = ""
    if not passed:
        msg = f"valid={actual_valid} codes={actual_codes} stats={stats}"
    return ConformanceCaseResult(str(case["id"]), passed, expected_valid, actual_valid, expected_codes, actual_codes, msg)


def run_conformance(manifest_path: str | Path | None = MANIFEST_PATH) -> ConformanceRunResult:
    manifest_path = MANIFEST_PATH if manifest_path is None else Path(manifest_path)
    manifest = load_manifest(manifest_path)
    manifest_errors = validate_manifest(manifest)
    if manifest_errors:
        results = tuple(ConformanceCaseResult(f"manifest-{i}", False, True, False, (), (), e) for i, e in enumerate(manifest_errors, start=1))
        return ConformanceRunResult(str(manifest.get("format_version", "unknown")), 0, len(results), len(results), results)
    root = Path(manifest_path).parent
    results = tuple(run_case(case, root) for case in manifest["cases"])
    passed = sum(1 for r in results if r.passed)
    return ConformanceRunResult(str(manifest["format_version"]), passed, len(results) - passed, len(results), results)


def _json_result(result: ConformanceRunResult) -> str:
    return json.dumps({"suite": result.suite, "passed": result.passed, "failed": result.failed, "total": result.total, "success": result.success, "results": [asdict(r) for r in result.results]}, indent=2, sort_keys=True) + "\n"


def _text_result(result: ConformanceRunResult) -> str:
    lines = [f"Conformance suite {result.suite}: {result.passed}/{result.total} passed"]
    for item in result.results:
        status = "PASS" if item.passed else "FAIL"
        suffix = f" - {item.message}" if item.message else ""
        lines.append(f"{status} {item.case_id}{suffix}")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m mechanization.far_mechanization.conformance")
    parser.add_argument("--manifest", default=str(MANIFEST_PATH))
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)
    result = run_conformance(args.manifest)
    sys.stdout.write(_json_result(result) if args.output == "json" else _text_result(result))
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
