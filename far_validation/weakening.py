from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_LIVE_CALL_PREFIXES: dict[str, tuple[str, ...]] = {
    "research/target-category-discovery/verify_compositional_invariant.py": ("validate_empirical_authority", "validate_gate"),
    "research/target-category-discovery/verify_compositional_invariant_legacy.py": ("validate_empirical_authority", "validate_gate"),
}
REQUIRED_SEMANTIC_CALLS: dict[str, frozenset[str]] = {
    path: frozenset(prefix) for path, prefix in REQUIRED_LIVE_CALL_PREFIXES.items()
}


REQUIRED_MODULE_BINDING_SIGNATURES: dict[str, dict[str, tuple[str, ...]]] = {
    "research/target-category-discovery/verify_compositional_invariant.py": {
        "validate_empirical_authority": (),
        "validate_gate": ("function", "attribute:_core", "globals"),
    },
    "research/target-category-discovery/verify_compositional_invariant_legacy.py": {
        "validate_empirical_authority": ("function",),
        "validate_gate": ("function",),
    },
}


EXPECTED_PROTECTED_IMPLEMENTATION_DIGESTS: dict[str, dict[str, str]] = {'research/target-category-discovery/verify_compositional_invariant.py': {'validate_gate': 'cdc2c4a81cf2a598291aefc6bfe26dc31f3837cc6b3ae264d2dd6fdd8a9392b2',
                                                                          'verify': '957e2638ee31f343367c153c03ae881f326b51e1cee1b571f6b11e1f3c8f2fcc'},
 'research/target-category-discovery/verify_compositional_invariant_legacy.py': {'_free_category': '02552df6cd7ba5d4e795792819b2aaa68a14c5cdf1590e95b39a47935ceb56cb',
                                                                                 '_git_blob_sha1': 'b3af787b941adfb26fa95275252cfa7c063e610018eccbcb60e3ad8e24ab7d5e',
                                                                                 '_read_utf8': '5b9fe168d4b08a41951d9d39f8c832d6397c6170ecd9e5e09c8d57a6aa3ebdba',
                                                                                 '_render': 'e7b291475f6859f5a6ae8452124016eb1e080d5c759f325d16e6a649dfb43bfc',
                                                                                 'build_result': 'c6b8b2881459d686a4296a0df6fe66a034ecc8a079a413249b439824a36881aa',
                                                                                 'canonical_json': '8c56324447ec578fa3966b725ca77b2204dccc2d1156e35a563f5450d6005220',
                                                                                 'load_json': '1804352134db5a6bbdf4adb8a640a6a1513bde226d80a91edb32feb1f8ddf3c4',
                                                                                 'validate_empirical_authority': 'eb8b9adb90077a9914adfacce5dd188233037d375d3a5a7d7deb2d41fe114cbc',
                                                                                 'validate_gate': '228a099165c3878ee2edabb6664826b840f1b6fa7a2a07f935f6c68dd90811da',
                                                                                 'validate_public_surface': '8e611a7f7f5254f2eef0173d14ca37910c04e03495eec88605af992f3f97859b',
                                                                                 'validate_spec': 'd907f23869756758a43b96f0542e4131b0bf20857850efc3241531caca27baff',
                                                                                 'verify': '0a4675b2285452c0ce0cfc61f026eb1a2b3d0383c984d433542195337739677e'}}


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


def _called_functions(source: str, path: str) -> set[str]:
    tree = ast.parse(source, filename=path)
    return {_call_name(node) for node in ast.walk(tree) if isinstance(node, ast.Call)}


def _live_call_prefix(source: str, path: str, function_name: str = "verify", count: int = 2) -> tuple[str, ...]:
    """Return the exact unconditional call prefix of the public verification path.

    The protected verifiers must begin with fail-closed authority checks. Any
    assignment, conditional, loop, try, return, raise, or other statement inserted
    before those calls changes the prefix and is rejected, including conditionally
    terminating branches such as ``if True: return``.
    """
    tree = ast.parse(source, filename=path)
    matches = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name]
    if len(matches) != 1:
        return ()
    body = list(matches[0].body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        body = body[1:]
    names: list[str] = []
    for statement in body[:count]:
        if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Call):
            names.append(_call_name(statement.value))
        else:
            names.append("")
    return tuple(names)


def _module_scope_binding_signatures(source: str, path: str) -> dict[str, tuple[str, ...]]:
    """Return structural module-scope binding events for protected validators."""
    protected = REQUIRED_SEMANTIC_CALLS.get(path, frozenset())
    events: dict[str, list[str]] = {name: [] for name in protected}
    if not protected:
        return {}
    tree = ast.parse(source, filename=path)

    def namespace_scope(node: ast.AST) -> str | None:
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"globals", "locals"}
            and not node.args
            and not node.keywords
        ):
            return node.func.id
        return None

    def record_namespace_alias(target: ast.AST, value: ast.AST, kind: str) -> None:
        scope = namespace_scope(value)
        if scope is None:
            return
        targets: list[ast.AST] = list(target.elts) if isinstance(target, (ast.Tuple, ast.List)) else [target]
        for alias_target in targets:
            if isinstance(alias_target, ast.Name):
                for name in protected:
                    events[name].append(f"{scope}-namespace-alias:{kind}:{alias_target.id}")

    def record_target(target: ast.AST, kind: str) -> None:
        if isinstance(target, ast.Name) and target.id in protected:
            events[target.id].append(kind)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for item in target.elts:
                record_target(item, kind)
        elif isinstance(target, ast.Attribute) and target.attr in protected:
            root = target.value.id if isinstance(target.value, ast.Name) else ast.unparse(target.value)
            events[target.attr].append(f"attribute:{root}")
        elif isinstance(target, ast.Subscript):
            scope = namespace_scope(target.value)
            key = target.slice
            if (
                scope is not None
                and isinstance(key, ast.Constant)
                and isinstance(key.value, str)
                and key.value in protected
            ):
                events[key.value].append(scope)

    def record_namespace_mutator(node: ast.Call) -> None:
        """Record method-based writes to module namespace dictionaries.

        Direct ``globals()[name] = value`` assignments are handled by
        ``record_target``. This additionally catches equivalent method writes such
        as ``globals().__setitem__(name, value)`` and ``globals().update(...)``.
        Dynamic update mappings are treated conservatively as capable of changing
        every protected binding.
        """
        if not isinstance(node.func, ast.Attribute):
            return
        scope = namespace_scope(node.func.value)
        if scope is None:
            return
        method = node.func.attr
        if method == "__setitem__":
            if not node.args:
                return
            key = node.args[0]
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                if key.value in protected:
                    events[key.value].append(f"{scope}.__setitem__")
            else:
                for name in protected:
                    events[name].append(f"{scope}.__setitem__:dynamic")
            return
        if method not in {"update", "__ior__"}:
            return

        touched: set[str] = set()
        dynamic = False
        for arg in node.args:
            if isinstance(arg, ast.Dict):
                for key in arg.keys:
                    if isinstance(key, ast.Constant) and isinstance(key.value, str):
                        if key.value in protected:
                            touched.add(key.value)
                    else:
                        dynamic = True
            elif (
                isinstance(arg, ast.Call)
                and isinstance(arg.func, ast.Name)
                and arg.func.id == "dict"
                and not arg.args
            ):
                for keyword in arg.keywords:
                    if keyword.arg is None:
                        dynamic = True
                    elif keyword.arg in protected:
                        touched.add(keyword.arg)
            else:
                dynamic = True
        for keyword in node.keywords:
            if keyword.arg is None:
                dynamic = True
            elif keyword.arg in protected:
                touched.add(keyword.arg)
        if dynamic:
            touched.update(protected)
        for name in sorted(touched):
            events[name].append(f"{scope}.{method}")

    def scan_expr(expr: ast.AST) -> None:
        for node in ast.walk(expr):
            if isinstance(node, ast.NamedExpr):
                record_target(node.target, "namedexpr")
                record_namespace_alias(node.target, node.value, "namedexpr")
            if isinstance(node, ast.Call):
                record_namespace_mutator(node)
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "setattr"
                and len(node.args) >= 2
                and isinstance(node.args[1], ast.Constant)
                and isinstance(node.args[1].value, str)
                and node.args[1].value in protected
            ):
                events[node.args[1].value].append("setattr")

    def scan(stmts: list[ast.stmt]) -> None:
        for st in stmts:
            if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if st.name in protected:
                    events[st.name].append("function")
                for decorator in st.decorator_list:
                    scan_expr(decorator)
                for default in (*st.args.defaults, *[item for item in st.args.kw_defaults if item is not None]):
                    scan_expr(default)
                for arg in (*st.args.posonlyargs, *st.args.args, *st.args.kwonlyargs):
                    if arg.annotation is not None:
                        scan_expr(arg.annotation)
                if st.args.vararg is not None and st.args.vararg.annotation is not None:
                    scan_expr(st.args.vararg.annotation)
                if st.args.kwarg is not None and st.args.kwarg.annotation is not None:
                    scan_expr(st.args.kwarg.annotation)
                if st.returns is not None:
                    scan_expr(st.returns)
                continue
            if isinstance(st, ast.ClassDef):
                if st.name in protected:
                    events[st.name].append("class")
                for decorator in st.decorator_list:
                    scan_expr(decorator)
                for base in st.bases:
                    scan_expr(base)
                for keyword in st.keywords:
                    scan_expr(keyword.value)
                # Class bodies execute at definition time; inspect that executable scope.
                scan(st.body)
                continue
            if isinstance(st, ast.Assign):
                for target in st.targets:
                    record_target(target, "assign")
                    record_namespace_alias(target, st.value, "assign")
                scan_expr(st.value)
            elif isinstance(st, ast.AnnAssign):
                record_target(st.target, "annassign")
                if st.value is not None:
                    record_namespace_alias(st.target, st.value, "annassign")
                    scan_expr(st.value)
            elif isinstance(st, ast.AugAssign):
                record_target(st.target, "augassign")
                scan_expr(st.value)
            elif isinstance(st, ast.Delete):
                for target in st.targets:
                    record_target(target, "delete")
            elif isinstance(st, (ast.Import, ast.ImportFrom)):
                for alias in st.names:
                    bound = alias.asname or alias.name.split(".", 1)[0]
                    if bound in protected:
                        events[bound].append("import")
            elif isinstance(st, (ast.For, ast.AsyncFor)):
                record_target(st.target, "loop-target")
                scan_expr(st.iter)
                scan(st.body)
                scan(st.orelse)
            elif isinstance(st, ast.While):
                scan_expr(st.test)
                scan(st.body)
                scan(st.orelse)
            elif isinstance(st, ast.If):
                scan_expr(st.test)
                scan(st.body)
                scan(st.orelse)
            elif isinstance(st, (ast.With, ast.AsyncWith)):
                for item in st.items:
                    scan_expr(item.context_expr)
                    if item.optional_vars is not None:
                        record_target(item.optional_vars, "with-target")
                scan(st.body)
            elif isinstance(st, ast.Try):
                scan(st.body)
                for handler in st.handlers:
                    if handler.name in protected:
                        events[handler.name].append("except-target")
                    scan(handler.body)
                scan(st.orelse)
                scan(st.finalbody)
            else:
                scan_expr(st)

    scan(tree.body)
    return {name: tuple(kinds) for name, kinds in events.items()}


def _binding_integrity_failures(source: str, path: str) -> list[str]:
    expected = REQUIRED_MODULE_BINDING_SIGNATURES.get(path)
    if expected is None:
        return []
    actual = _module_scope_binding_signatures(source, path)
    failures: list[str] = []
    for name, expected_signature in expected.items():
        actual_signature = actual.get(name, ())
        if actual_signature != expected_signature:
            failures.append(
                f"protected validator binding changed for {name}: "
                f"expected {expected_signature!r}; got {actual_signature!r}"
            )
    return failures


def _protected_implementation_digest(source: str, path: str, function_name: str) -> str | None:
    tree = ast.parse(source, filename=path)
    nodes = [n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name == function_name]
    if len(nodes) != 1:
        return None
    return hashlib.sha256(ast.dump(nodes[0], annotate_fields=True, include_attributes=False).encode()).hexdigest()


def _protected_implementation_failures(source: str, path: str) -> list[str]:
    failures: list[str] = []
    for name, expected in EXPECTED_PROTECTED_IMPLEMENTATION_DIGESTS.get(path, {}).items():
        actual = _protected_implementation_digest(source, path, name)
        if actual != expected:
            failures.append(f"protected validator implementation changed for {name}: expected {expected}; got {actual or '<missing-or-ambiguous>'}")
    return failures


def _definition_time_execution_failures(source: str, path: str) -> list[str]:
    if path not in REQUIRED_SEMANTIC_CALLS:
        return []
    tree = ast.parse(source, filename=path)
    failures: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.decorator_list:
            failures.append(f"protected verifier definition-time decorator rejected: {getattr(node, 'name', '<definition>')}")
    return failures


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
    completed = _git(
        root,
        "diff",
        "--name-status",
        f"{base}...HEAD",
        "--",
        "tests",
        "tools",
        "far_validation",
        "validation_bootstrap",
        "research",
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "git diff failed")
    changed: list[tuple[str, str]] = []
    for line in completed.stdout.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        status, path = fields[0], fields[-1]
        protected_research_validator = path.startswith("research/") and Path(path).name.startswith("verify_")
        if path.endswith(".py") and (
            path.startswith("tests/")
            or "/check_" in path
            or path.startswith("far_validation/")
            or path.startswith("validation_bootstrap/")
            or protected_research_validator
        ):
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
            required_prefix = REQUIRED_LIVE_CALL_PREFIXES.get(path)
            if required_prefix:
                actual_prefix = _live_call_prefix(after_source, path, count=len(required_prefix))
                if actual_prefix != required_prefix:
                    finding.failures.append(
                        "required live verify call prefix changed: expected "
                        + " -> ".join(required_prefix)
                        + "; got "
                        + " -> ".join(name or "<non-call>" for name in actual_prefix)
                    )
            finding.failures.extend(_binding_integrity_failures(after_source, path))
            finding.failures.extend(_definition_time_execution_failures(after_source, path))
            finding.failures.extend(_protected_implementation_failures(after_source, path))
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