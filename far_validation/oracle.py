from __future__ import annotations

import ast
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

ORACLE_SCHEMA = "far-independent-oracle-v1"
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


def analyze_checker_source(source: str, path: str) -> OracleFinding:
    failures: list[str] = []
    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as exc:
        return OracleFinding(path=path, accepted=False, failures=[f"syntax error: {exc}"])

    nodes = list(ast.walk(tree))
    branches = sum(isinstance(node, (ast.If, ast.Try, ast.Match, ast.For, ast.While)) for node in nodes)
    raises = sum(isinstance(node, (ast.Raise, ast.Assert)) for node in nodes)
    calls = [_call_name(node) for node in nodes if isinstance(node, ast.Call)]
    failure_calls = sum(
        name.split(".")[-1] in {"fail", "exit", "abort", "error", "assertEqual", "assertTrue", "assertFalse", "check_call"}
        or name in {"sys.exit", "raise_for_status"}
        for name in calls
    )
    file_calls = sum(
        name.split(".")[-1] in {
            "open", "read_text", "read_bytes", "exists", "is_file", "is_dir", "glob", "rglob", "load", "loads"
        }
        for name in calls
    )
    subprocess_calls = sum(name.startswith("subprocess.") for name in calls)
    functions = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in nodes)
    metrics = {
        "ast_nodes": len(nodes),
        "branches": branches,
        "failure_paths": raises + failure_calls,
        "file_accesses": file_calls,
        "subprocess_calls": subprocess_calls,
        "functions": functions,
    }
    if len(nodes) < 18:
        failures.append("checker is structurally trivial")
    if branches == 0:
        failures.append("checker has no decision branch")
    if raises + failure_calls == 0:
        failures.append("checker has no independently visible failure path")
    if file_calls + subprocess_calls == 0:
        failures.append("checker observes no repository artifact or subprocess result")
    return OracleFinding(path=path, accepted=not failures, failures=failures, metrics=metrics)


def _mutations(source: str) -> dict[str, str]:
    return {
        "empty": "",
        "trivial_success": "def main():\n    print('PASS')\n\nif __name__ == '__main__':\n    main()\n",
        "no_failure_path": "from pathlib import Path\n\ndef main():\n    if Path('.').exists():\n        print('PASS')\n\nif __name__ == '__main__':\n    main()\n",
        "syntax_corruption": source + "\nif (:\n",
    }


def _manifest_commands(root: Path) -> tuple[dict[str, str], list[str]]:
    payload = json.loads((root / "validation" / "manifest.json").read_text(encoding="utf-8"))
    commands: dict[str, str] = {}
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
        commands[check_id] = script
        inputs = raw.get("inputs", [])
        if not isinstance(inputs, list) or not inputs:
            failures.append(f"{check_id}: no declared inputs")
        failure_code = raw.get("failure_code")
        if not isinstance(failure_code, str) or not failure_code.startswith("FAR-VAL-"):
            failures.append(f"{check_id}: unstable or missing failure code")
    return commands, failures


def discover_legacy_checkers(root: Path, manifest_scripts: set[str]) -> list[str]:
    paths = set(manifest_scripts) | EXPLICIT_LEGACY_ENTRYPOINTS
    paths.update(path.relative_to(root).as_posix() for path in (root / "tools").glob("check_*.py"))
    return sorted(path for path in paths if (root / path).is_file())


def run_oracle(root: Path, *, execute_manifest: bool = False, timeout: int = 900) -> OracleReport:
    commands, coverage_failures = _manifest_commands(root)
    discovered = discover_legacy_checkers(root, set(commands.values()))
    missing = sorted(set(commands.values()) - set(discovered))
    coverage_failures.extend(f"manifest checker missing from discovery: {path}" for path in missing)

    findings: list[OracleFinding] = []
    by_path: dict[str, OracleFinding] = {}
    for path in discovered:
        source = (root / path).read_text(encoding="utf-8")
        finding = analyze_checker_source(source, path)
        for mutation_id, mutated in _mutations(source).items():
            finding.mutation_results[mutation_id] = not analyze_checker_source(mutated, path).accepted
        if not all(finding.mutation_results.values()):
            finding.failures.append("independent oracle accepted at least one hostile source mutation")
            finding.accepted = False
        findings.append(finding)
        by_path[path] = finding

    for check_id, path in commands.items():
        if path not in by_path:
            coverage_failures.append(f"{check_id}: independent oracle coverage missing for {path}")
        if execute_manifest:
            raw = json.loads((root / "validation" / "manifest.json").read_text(encoding="utf-8"))
            entry = next(item for item in raw["checks"] if item.get("id") == check_id)
            completed = subprocess.run(
                entry["command"], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=int(entry.get("timeout_seconds", timeout)), check=False,
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
            print(f"[{marker}] {finding.path}")
            for failure in finding.failures:
                print(f"  - {failure}")
        for failure in report.coverage_failures:
            print(f"[FAIL] coverage: {failure}")
        print("Result:", "PASS" if report.successful else "FAIL")
    return 0 if report.successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
