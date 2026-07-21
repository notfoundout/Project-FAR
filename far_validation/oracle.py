from __future__ import annotations

import ast
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

ORACLE_SCHEMA = "far-independent-oracle-v1"
DEFAULT_TEST_FAILURE_CODE = "FAR-VAL-TEST-001"
EXPLICIT_LEGACY_ENTRYPOINTS = {
    "tools/run_tests.py",
    "tools/verify_theory.py",
    "tools/repo_health_check.py",
    "tools/generate_next_tasks.py",
    "tools/project_status_report.py",
    "tools/update_readme_dashboard.py",
}


@dataclass
class OracleFinding:
    path: str
    accepted: bool
    failures: list[str] = field(default_factory=list)
    metrics: dict[str, int] = field(default_factory=dict)
    mutation_results: dict[str, bool] = field(default_factory=dict)
    role: str = "checker"
    delegated_modules: list[str] = field(default_factory=list)


@dataclass
class OracleReport:
    schema: str
    checker_count: int
    manifest_command_count: int
    findings: list[OracleFinding]
    coverage_failures: list[str]

    @property
    def successful(self) -> bool:
        return not self.coverage_failures and all(item.accepted for item in self.findings)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["successful"] = self.successful
        return payload


def _call_name(node: ast.Call) -> str:
    target = node.func
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        parts: list[str] = [target.attr]
        value = target.value
        while isinstance(value, ast.Attribute):
            parts.append(value.attr)
            value = value.value
        if isinstance(value, ast.Name):
            parts.append(value.id)
        return ".".join(reversed(parts))
    return ""


def _empty_metrics() -> dict[str, int]:
    return {
        "ast_nodes": 0,
        "branches": 0,
        "failure_paths": 0,
        "file_accesses": 0,
        "file_writes": 0,
        "subprocess_calls": 0,
        "functions": 0,
    }


def _source_metrics(source: str, path: str) -> tuple[dict[str, int], ast.Module | None, str | None]:
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as exc:
        return _empty_metrics(), None, f"syntax error: {exc}"
    nodes = list(ast.walk(tree))
    branches = sum(isinstance(node, (ast.If, ast.Try, ast.Match, ast.For, ast.While)) for node in nodes)
    raises = sum(isinstance(node, (ast.Raise, ast.Assert)) for node in nodes)
    calls = [_call_name(node) for node in nodes if isinstance(node, ast.Call)]
    failure_calls = sum(
        name.split(".")[-1]
        in {
            "fail",
            "exit",
            "abort",
            "error",
            "assertEqual",
            "assertTrue",
            "assertFalse",
            "check_call",
            "check_returncode",
        }
        or name in {"sys.exit", "raise_for_status"}
        for name in calls
    )
    read_calls = {
        "open",
        "read_text",
        "read_bytes",
        "exists",
        "is_file",
        "is_dir",
        "glob",
        "rglob",
        "iterdir",
        "load",
        "loads",
    }
    write_calls = {
        "write_text",
        "write_bytes",
        "mkdir",
        "unlink",
        "rename",
        "replace",
        "dump",
        "dumps",
    }
    file_accesses = sum(name.split(".")[-1] in read_calls | write_calls for name in calls)
    file_writes = sum(name.split(".")[-1] in write_calls for name in calls)
    subprocess_calls = sum(name.startswith("subprocess.") for name in calls)
    functions = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in nodes)
    return (
        {
            "ast_nodes": len(nodes),
            "branches": branches,
            "failure_paths": raises + failure_calls,
            "file_accesses": file_accesses,
            "file_writes": file_writes,
            "subprocess_calls": subprocess_calls,
            "functions": functions,
        },
        tree,
        None,
    )


def _merge_metrics(items: Iterable[dict[str, int]]) -> dict[str, int]:
    result = _empty_metrics()
    for item in items:
        for key in result:
            result[key] += item.get(key, 0)
    return result


def _resolve_local_module(root: Path, current: Path, module: str | None, level: int) -> Path | None:
    if module is None:
        return None
    module_path = Path(*module.split("."))
    candidates: list[Path] = []
    if level:
        base = current.parent
        for _ in range(max(0, level - 1)):
            base = base.parent
        candidates.extend((base / module_path.with_suffix(".py"), base / module_path / "__init__.py"))
    else:
        candidates.extend(
            (
                current.parent / module_path.with_suffix(".py"),
                root / module_path.with_suffix(".py"),
                root / "tools" / module_path.with_suffix(".py"),
                root / module_path / "__init__.py",
            )
        )
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    return None


def _local_module_closure(root: Path, entry: Path, *, max_depth: int = 3) -> list[Path]:
    root = root.resolve()
    visited: set[Path] = {entry.resolve()}
    discovered: list[Path] = []

    def visit(path: Path, depth: int) -> None:
        if depth >= max_depth:
            return
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=path.as_posix())
        except (OSError, SyntaxError):
            return
        for node in tree.body:
            module: str | None = None
            level = 0
            if isinstance(node, ast.ImportFrom):
                module = node.module
                level = node.level
            elif isinstance(node, ast.Import) and len(node.names) == 1:
                module = node.names[0].name
            else:
                continue
            resolved = _resolve_local_module(root, path, module, level)
            if resolved is None or resolved in visited:
                continue
            try:
                resolved.relative_to(root)
            except ValueError:
                continue
            visited.add(resolved)
            discovered.append(resolved)
            visit(resolved, depth + 1)

    visit(entry.resolve(), 0)
    return discovered


def _evaluate_metrics(path: str, metrics: dict[str, int], role: str) -> OracleFinding:
    failures: list[str] = []
    if metrics["ast_nodes"] < 18:
        failures.append("checker is structurally trivial")
    if metrics["branches"] == 0:
        failures.append("checker has no decision branch")
    if metrics["file_accesses"] + metrics["subprocess_calls"] == 0:
        failures.append("checker observes no repository artifact or subprocess result")
    if role == "generator":
        if metrics["file_writes"] == 0:
            failures.append("generator has no independently visible repository output")
    elif metrics["failure_paths"] == 0:
        failures.append("checker has no independently visible failure path")
    return OracleFinding(path=path, accepted=not failures, failures=failures, metrics=metrics, role=role)


def analyze_checker_source(source: str, path: str, *, role: str = "checker") -> OracleFinding:
    metrics, _, syntax_failure = _source_metrics(source, path)
    if syntax_failure:
        return OracleFinding(path=path, accepted=False, failures=[syntax_failure], metrics=metrics, role=role)
    return _evaluate_metrics(path, metrics, role)


def analyze_checker_path(root: Path, path: str, *, role: str = "checker") -> OracleFinding:
    entry = (root / path).resolve()
    try:
        source = entry.read_text(encoding="utf-8")
    except OSError as exc:
        return OracleFinding(path=path, accepted=False, failures=[f"cannot read checker: {exc}"], role=role)
    primary, _, syntax_failure = _source_metrics(source, path)
    if syntax_failure:
        return OracleFinding(path=path, accepted=False, failures=[syntax_failure], metrics=primary, role=role)
    delegated = _local_module_closure(root, entry)
    delegated_metrics: list[dict[str, int]] = []
    delegated_paths: list[str] = []
    for module_path in delegated:
        relative = module_path.relative_to(root.resolve()).as_posix()
        metrics, _, failure = _source_metrics(module_path.read_text(encoding="utf-8"), relative)
        if failure is None:
            delegated_metrics.append(metrics)
            delegated_paths.append(relative)
    finding = _evaluate_metrics(path, _merge_metrics([primary, *delegated_metrics]), role)
    finding.delegated_modules = delegated_paths
    return finding


def _mutations(source: str) -> dict[str, str]:
    return {
        "empty": "",
        "trivial_success": "def main():\n    print('PASS')\n\nif __name__ == '__main__':\n    main()\n",
        "no_failure_path": "from pathlib import Path\n\ndef main():\n    if Path('.').exists():\n        print('PASS')\n\nif __name__ == '__main__':\n    main()\n",
        "syntax_corruption": source + "\nif (:\n",
    }


def _manifest_commands(root: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    payload = json.loads((root / "validation" / "manifest.json").read_text(encoding="utf-8"))
    commands: dict[str, dict[str, str]] = {}
    failures: list[str] = []
    for raw in payload.get("checks", []):
        if not isinstance(raw, dict) or raw.get("builtin"):
            continue
        check_id = str(raw.get("id", ""))
        command = raw.get("command", [])
        if not isinstance(command, list) or not command:
            failures.append(f"{check_id}: command missing")
            continue
        script = next((item for item in command[1:] if isinstance(item, str) and item.endswith(".py")), None)
        if script is None:
            failures.append(f"{check_id}: no Python checker entrypoint")
            continue
        role = "generator" if raw.get("expect_no_changes") is True or raw.get("category") == "generator" else "checker"
        commands[check_id] = {"path": script, "role": role}
        inputs = raw.get("inputs", [])
        if not isinstance(inputs, list) or not inputs:
            failures.append(f"{check_id}: no declared inputs")
        failure_code = raw.get("failure_code")
        if failure_code is None and raw.get("category") == "tests":
            failure_code = DEFAULT_TEST_FAILURE_CODE
        if not isinstance(failure_code, str) or not failure_code.startswith("FAR-VAL-"):
            failures.append(f"{check_id}: unstable or missing failure code")
    return commands, failures


def discover_legacy_checkers(root: Path, manifest_scripts: set[str]) -> list[str]:
    paths = set(manifest_scripts) | EXPLICIT_LEGACY_ENTRYPOINTS
    paths.update(path.relative_to(root).as_posix() for path in (root / "tools").glob("check_*.py"))
    return sorted(path for path in paths if (root / path).is_file())


def run_oracle(root: Path, *, execute_manifest: bool = False, timeout: int = 900) -> OracleReport:
    commands, coverage_failures = _manifest_commands(root)
    path_roles: dict[str, str] = {}
    for command in commands.values():
        previous = path_roles.get(command["path"])
        path_roles[command["path"]] = "checker" if previous == "checker" else command["role"]
    discovered = discover_legacy_checkers(root, {item["path"] for item in commands.values()})
    missing = sorted({item["path"] for item in commands.values()} - set(discovered))
    coverage_failures.extend(f"manifest checker missing from discovery: {path}" for path in missing)

    findings: list[OracleFinding] = []
    by_path: dict[str, OracleFinding] = {}
    for path in discovered:
        source = (root / path).read_text(encoding="utf-8")
        role = path_roles.get(path, "checker")
        finding = analyze_checker_path(root, path, role=role)
        for mutation_id, mutated in _mutations(source).items():
            finding.mutation_results[mutation_id] = not analyze_checker_source(mutated, path, role=role).accepted
        if not all(finding.mutation_results.values()):
            finding.failures.append("independent oracle accepted at least one hostile source mutation")
            finding.accepted = False
        findings.append(finding)
        by_path[path] = finding

    manifest = None
    if execute_manifest:
        manifest = json.loads((root / "validation" / "manifest.json").read_text(encoding="utf-8"))
    for check_id, command_info in commands.items():
        path = command_info["path"]
        if path not in by_path:
            coverage_failures.append(f"{check_id}: independent oracle coverage missing for {path}")
        if execute_manifest and manifest is not None:
            entry = next(item for item in manifest["checks"] if item.get("id") == check_id)
            completed = subprocess.run(
                entry["command"],
                cwd=root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=int(entry.get("timeout_seconds", timeout)),
                check=False,
            )
            if completed.returncode != 0:
                coverage_failures.append(f"{check_id}: baseline checker execution failed with {completed.returncode}")

    return OracleReport(
        schema=ORACLE_SCHEMA,
        checker_count=len(findings),
        manifest_command_count=len(commands),
        findings=findings,
        coverage_failures=sorted(set(coverage_failures)),
    )


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Independently validate every legacy checker contract")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = run_oracle(args.root.resolve(), execute_manifest=args.execute)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"independent oracle: {report.checker_count} legacy checkers")
        for finding in report.findings:
            marker = "PASS" if finding.accepted else "FAIL"
            print(f"[{marker}] {finding.path} ({finding.role})")
            for failure in finding.failures:
                print(f"  - {failure}")
        for failure in report.coverage_failures:
            print(f"[FAIL] coverage: {failure}")
        print("Result:", "PASS" if report.successful else "FAIL")
    return 0 if report.successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
