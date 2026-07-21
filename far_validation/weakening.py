from __future__ import annotations

import ast
import json
import os
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class StrengthMetrics:
    tests: tuple[str, ...] = ()
    assertions: int = 0
    raises: int = 0
    failure_paths: int = 0
    branches: int = 0
    skips: int = 0
    ast_nodes: int = 0


@dataclass
class WeakeningFinding:
    path: str
    failures: list[str] = field(default_factory=list)
    before: StrengthMetrics | None = None
    after: StrengthMetrics | None = None


@dataclass
class WeakeningReport:
    base: str
    findings: list[WeakeningFinding]
    waivers_used: list[str]

    @property
    def successful(self) -> bool:
        return all(not finding.failures for finding in self.findings)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["successful"] = self.successful
        return payload


def _call_name(node: ast.Call) -> str:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return ""


def analyze(source: str, path: str) -> StrengthMetrics:
    tree = ast.parse(source, filename=path)
    nodes = list(ast.walk(tree))
    tests: list[str] = []
    assertions = 0
    raises = 0
    failure_paths = 0
    skips = 0
    for node in nodes:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
            tests.append(node.name)
        if isinstance(node, ast.Assert):
            assertions += 1
        if isinstance(node, ast.Raise):
            raises += 1
        if isinstance(node, ast.Call):
            name = _call_name(node)
            if name.startswith("assert"):
                assertions += 1
            if name in {"fail", "exit", "abort", "error"}:
                failure_paths += 1
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for decorator in node.decorator_list:
                text = ast.unparse(decorator) if hasattr(ast, "unparse") else ""
                if "skip" in text.lower():
                    skips += 1
    branches = sum(isinstance(node, (ast.If, ast.Try, ast.Match, ast.For, ast.While)) for node in nodes)
    return StrengthMetrics(
        tests=tuple(sorted(tests)),
        assertions=assertions,
        raises=raises,
        failure_paths=failure_paths,
        branches=branches,
        skips=skips,
        ast_nodes=len(nodes),
    )


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def _resolve_base(root: Path, requested: str | None) -> str:
    candidates = [requested, os.environ.get("FAR_VALIDATION_BASE_SHA"), os.environ.get("GITHUB_BASE_SHA")]
    for candidate in candidates:
        if candidate:
            probe = _git(root, "rev-parse", "--verify", candidate)
            if probe.returncode == 0:
                return probe.stdout.strip()
    for candidate in ("origin/main", "main", "HEAD^1"):
        probe = _git(root, "merge-base", "HEAD", candidate)
        if probe.returncode == 0 and probe.stdout.strip():
            return probe.stdout.strip()
    raise RuntimeError("cannot resolve comparison base for weakening detection")


def _show(root: Path, revision: str, path: str) -> str | None:
    completed = _git(root, "show", f"{revision}:{path}")
    return completed.stdout if completed.returncode == 0 else None


def _load_waivers(root: Path) -> dict[str, dict[str, Any]]:
    path = root / "validation" / "test-weakening-waivers.json"
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    result: dict[str, dict[str, Any]] = {}
    for item in payload.get("waivers", []):
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            result[item["path"]] = item
    return result


def _changed_python(root: Path, base: str) -> list[tuple[str, str]]:
    completed = _git(root, "diff", "--name-status", f"{base}...HEAD", "--", "tests", "tools", "far_validation", "validation_bootstrap")
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "git diff failed")
    changed: list[tuple[str, str]] = []
    for line in completed.stdout.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        status, path = fields[0], fields[-1]
        if path.endswith(".py") and (path.startswith("tests/") or "/check_" in path or path.startswith("far_validation/") or path.startswith("validation_bootstrap/")):
            changed.append((status[0], path))
    return sorted(changed)


def compare_strength(before: StrengthMetrics, after: StrengthMetrics, *, is_test: bool) -> list[str]:
    failures: list[str] = []
    if is_test:
        missing = sorted(set(before.tests) - set(after.tests))
        if missing:
            failures.append("test functions removed: " + ", ".join(missing))
        if after.assertions < before.assertions:
            failures.append(f"assertion count decreased: {before.assertions} -> {after.assertions}")
        if after.skips > before.skips:
            failures.append(f"skip count increased: {before.skips} -> {after.skips}")
    else:
        if after.failure_paths + after.raises < before.failure_paths + before.raises:
            failures.append("failure-path count decreased")
        if after.branches < before.branches:
            failures.append(f"decision-branch count decreased: {before.branches} -> {after.branches}")
    if after.ast_nodes < max(12, int(before.ast_nodes * 0.60)):
        failures.append(f"semantic structure shrank by more than 40%: {before.ast_nodes} -> {after.ast_nodes}")
    return failures


def detect_weakening(root: Path, *, base: str | None = None) -> WeakeningReport:
    resolved = _resolve_base(root, base)
    waivers = _load_waivers(root)
    findings: list[WeakeningFinding] = []
    used: list[str] = []
    for status, path in _changed_python(root, resolved):
        finding = WeakeningFinding(path=path)
        before_source = _show(root, resolved, path)
        current_path = root / path
        if status == "D" or not current_path.is_file():
            finding.failures.append("protected validation/test source deleted")
            findings.append(finding)
            continue
        after_source = current_path.read_text(encoding="utf-8")
        try:
            finding.after = analyze(after_source, path)
        except SyntaxError as exc:
            finding.failures.append(f"current source has syntax error: {exc}")
            findings.append(finding)
            continue
        if before_source is not None:
            try:
                finding.before = analyze(before_source, path)
            except SyntaxError:
                finding.before = None
            if finding.before is not None:
                finding.failures.extend(compare_strength(finding.before, finding.after, is_test=path.startswith("tests/")))
        if finding.failures and path in waivers:
            waiver = waivers[path]
            if waiver.get("base") == resolved and isinstance(waiver.get("justification"), str) and len(waiver["justification"].strip()) >= 20:
                finding.failures.clear()
                used.append(path)
        findings.append(finding)
    return WeakeningReport(base=resolved, findings=findings, waivers_used=used)


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Detect deleted or weakened tests and validators")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--base")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = detect_weakening(args.root.resolve(), base=args.base)
    except (RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"FAR-VAL-WEAKEN-001: {exc}")
        return 2
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"test-weakening comparison base: {report.base}")
        for finding in report.findings:
            marker = "PASS" if not finding.failures else "FAIL"
            print(f"[{marker}] {finding.path}")
            for failure in finding.failures:
                print(f"  - {failure}")
        print("Result:", "PASS" if report.successful else "FAIL")
    return 0 if report.successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
