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
        "validate_empirical_authority": ("globals:dynamic",),
        "validate_gate": ("function", "attribute:_core", "globals:dynamic", "globals"),
        "verify": ("globals:dynamic", "function", "attribute:_core"),
    },
    "research/target-category-discovery/verify_compositional_invariant_legacy.py": {
        "validate_empirical_authority": ("function",),
        "validate_gate": ("function",),
    },
}


EXPECTED_PROTECTED_IMPLEMENTATION_DIGESTS: dict[str, dict[str, str]] = {'research/target-category-discovery/verify_compositional_invariant.py': {'validate_gate': 'af3e3a20584f8b19e8989c99c7c85822dab584d1a2155df990c148ecca1f67b2',
                                                                          'verify': 'b8b2aa2a4ac0f68e9d420ab5e273954ab46eb5ee9a58f8967ced2d773709af30'},
 'research/target-category-discovery/verify_compositional_invariant_legacy.py': {'_free_category': '6dbae7c5fddbfe20a0ac0595395ffdf3dbf15c5db76881c43fb91ea5ce65758e',
                                                                                 '_git_blob_sha1': '0f84477ad146c85a9318c60d418d4b933481f6737e3c06a0786290b3fd221c41',
                                                                                 '_read_utf8': 'fb4ceb108ae5a5fb3eceb5181194c10945c673ef44e475a30d4a6961cf932bd6',
                                                                                 '_render': '7cdd6ca537e18171a48447c15b962e3a834d77d2e1921bc077f9001355ef744c',
                                                                                 'build_result': '256b1ea5340f9bde32f8a484a920e57fdb5158fb5dd93f1889db37ed9a3ad7ab',
                                                                                 'canonical_json': 'c98c9d6c980564fd8c377cdb14a1761ac6741577ef67faf9a2a68530424bea5c',
                                                                                 'load_json': '7186a47690f7cbf22cdd43c7be7abd2c024f546d57d8ff855e5251abd492f177',
                                                                                 'validate_empirical_authority': '973ddba18912d256c0f1442c098821f628bfd3516f6f19b9ae7c3dd329c346b9',
                                                                                 'validate_gate': '5f7006458d9a9542dd7965914229b82cbee549b7e2cb2c822cd7f73cb8a27920',
                                                                                 'validate_public_surface': 'bf91d77e74fa48ca3f461266012afe8d8e3f9c7abca7bfdca6ce49b3425fd9e0',
                                                                                 'validate_spec': 'dc15bb4595e1f24b0bc3bfd58289e451af7ff269d7a8d00fdc177e5325ea3ee4',
                                                                                 'verify': 'c05b14ff5e9d37f4eb1ede9aee3ce8b797fe64107fd6d5f2e2ffb7980fb7d6bf'}}


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


def _definition_time_statements(tree: ast.AST) -> list[ast.stmt]:
    """Return every statement in the module, not only module-scope statements.

    Class bodies, conditionals, loops, and try blocks all execute at definition
    time, so an import or alias assignment placed inside one binds a name just as
    a module-scope statement would. Alias resolution that inspects only
    ``tree.body`` misses those bindings.
    """
    return [node for node in ast.walk(tree) if isinstance(node, ast.stmt)]


def _alias_pairs(target: ast.AST, value: ast.AST) -> list[tuple[str, ast.AST]]:
    """Pair each assigned name with the expression it is bound to.

    Destructuring such as ``(alias,) = (vars,)`` binds the alias just as a plain
    assignment does. When the arities line up the pairing is element-wise;
    otherwise every extracted name is conservatively paired with the whole value.
    """
    if isinstance(target, ast.Name):
        return [(target.id, value)]
    if isinstance(target, (ast.Tuple, ast.List)):
        if isinstance(value, (ast.Tuple, ast.List)) and len(value.elts) == len(target.elts):
            pairs: list[tuple[str, ast.AST]] = []
            for item, item_value in zip(target.elts, value.elts):
                pairs.extend(_alias_pairs(item, item_value))
            return pairs
        pairs = []
        for item in target.elts:
            pairs.extend(_alias_pairs(item, value))
        return pairs
    return []


def _module_scope_binding_signatures(source: str, path: str) -> dict[str, tuple[str, ...]]:
    """Return structural module-scope binding events for protected validators."""
    protected = frozenset(set(REQUIRED_SEMANTIC_CALLS.get(path, frozenset())) | set(EXPECTED_PROTECTED_IMPLEMENTATION_DIGESTS.get(path, {})))
    events: dict[str, list[str]] = {name: [] for name in protected}
    if not protected:
        return {}
    tree = ast.parse(source, filename=path)
    namespace_names: dict[str, str] = {name: name for name in ("globals", "locals", "vars")}
    builtins_names: set[str] = {"builtins"}

    # Resolve aliases before scanning binding writes. Protected verifier code
    # cannot hide namespace access behind imported builtins aliases, direct
    # provider aliases, destructured aliases, or transitive assignments, in any
    # definition-time scope.
    statements = _definition_time_statements(tree)
    for statement in statements:
        if isinstance(statement, ast.Import):
            for alias in statement.names:
                if alias.name == "builtins":
                    builtins_names.add(alias.asname or "builtins")
        elif isinstance(statement, ast.ImportFrom) and statement.module == "builtins":
            for alias in statement.names:
                if alias.name in {"globals", "locals", "vars"}:
                    namespace_names[alias.asname or alias.name] = alias.name

    changed = True
    while changed:
        changed = False
        for statement in statements:
            value: ast.AST | None = None
            targets: list[ast.AST] = []
            if isinstance(statement, ast.Assign):
                value = statement.value
                targets = list(statement.targets)
            elif isinstance(statement, ast.AnnAssign) and statement.value is not None:
                value = statement.value
                targets = [statement.target]
            if value is None:
                continue
            for target in targets:
                for name, bound in _alias_pairs(target, value):
                    if isinstance(bound, ast.Name) and bound.id in builtins_names and name not in builtins_names:
                        builtins_names.add(name)
                        changed = True
                    provider: str | None = None
                    if isinstance(bound, ast.Name) and bound.id in namespace_names:
                        provider = namespace_names[bound.id]
                    elif (
                        isinstance(bound, ast.Attribute)
                        and isinstance(bound.value, ast.Name)
                        and bound.value.id in builtins_names
                        and bound.attr in {"globals", "locals", "vars"}
                    ):
                        provider = bound.attr
                    if provider is not None and namespace_names.get(name) != provider:
                        namespace_names[name] = provider
                        changed = True

    def namespace_provider(node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return namespace_names.get(node.id)
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id in builtins_names
            and node.attr in {"globals", "locals", "vars"}
        ):
            return node.attr
        return None

    def namespace_scope(node: ast.AST) -> str | None:
        # A module's __dict__ is the same writable mapping globals() returns, and
        # it is reached by attribute access rather than by calling a provider.
        if isinstance(node, ast.Attribute) and node.attr == "__dict__":
            return "__dict__"
        if not isinstance(node, ast.Call) or node.keywords:
            return None
        provider = namespace_provider(node.func)
        if provider is None:
            return None
        if not node.args:
            return provider
        # vars(module) exposes the same writable namespace mapping as globals(),
        # so a single-argument vars() call is still a namespace provider.
        if provider == "vars" and len(node.args) == 1:
            return provider
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
            if scope is None:
                return
            key = target.slice
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                if key.value in protected:
                    events[key.value].append(scope)
                return
            # A computed key can name any binding, so fail closed and record the
            # write against every protected validator.
            for name in protected:
                events[name].append(f"{scope}:dynamic")

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
            ):
                attribute = node.args[1]
                if isinstance(attribute, ast.Constant) and isinstance(attribute.value, str):
                    if attribute.value in protected:
                        events[attribute.value].append("setattr")
                else:
                    # A computed attribute name can target any protected validator.
                    for name in protected:
                        events[name].append("setattr:dynamic")

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

    # Fail closed when a namespace provider is captured rather than called.
    #
    # Recognising individual namespace expressions is open-ended: a provider
    # stored in a class attribute, container, or returned from a helper can be
    # called later through an expression this scanner cannot resolve. Protected
    # verifiers never need to capture globals/locals/vars -- every legitimate use
    # is a direct call -- so treat any non-call reference as capable of rebinding
    # every protected validator.
    called_directly = {
        id(node.func)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
    }
    captured: list[str] = []
    # A namespace handed to another callable is written through that callee, not
    # through a receiver this scanner can inspect -- operator.setitem(globals(),
    # name, value) is a module-scope rebinding whose receiver is `operator`.
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for argument in (*node.args, *(kw.value for kw in node.keywords)):
            inner = argument.value if isinstance(argument, ast.Starred) else argument
            scope = namespace_scope(inner)
            if scope is not None:
                captured.append(f"namespace-passed-to-call:{scope}:{_call_name(node) or '<expr>'}")
    for node in ast.walk(tree):
        if id(node) in called_directly:
            continue
        if isinstance(node, ast.Name) and node.id in namespace_names:
            captured.append(f"captured-namespace-provider:{node.id}")
        elif (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id in builtins_names
            and node.attr in {"globals", "locals", "vars"}
        ):
            captured.append(f"captured-namespace-provider:{node.value.id}.{node.attr}")
    for marker in captured:
        for name in protected:
            events[name].append(marker)

    return {name: tuple(kinds) for name, kinds in events.items()}


def _binding_integrity_failures(source: str, path: str) -> list[str]:
    expected = dict(REQUIRED_MODULE_BINDING_SIGNATURES.get(path, {}))
    for name in EXPECTED_PROTECTED_IMPLEMENTATION_DIGESTS.get(path, {}):
        expected.setdefault(name, ("function",))
    if not expected:
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
    """Digest a protected function's implementation reproducibly.

    ``ast.dump`` is a debugging representation with no cross-version stability
    guarantee: byte-identical source digests differently on CPython 3.11, 3.12,
    and 3.13, which would make this integrity pin pass only on the interpreter
    that generated it. ``ast.unparse`` renders canonical source instead, so the
    digest tracks the implementation rather than the interpreter.
    """
    tree = ast.parse(source, filename=path)
    nodes = [n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name == function_name]
    if len(nodes) != 1:
        return None
    return hashlib.sha256(ast.unparse(nodes[0]).encode("utf-8")).hexdigest()


def _protected_implementation_failures(source: str, path: str) -> list[str]:
    failures: list[str] = []
    for name, expected in EXPECTED_PROTECTED_IMPLEMENTATION_DIGESTS.get(path, {}).items():
        actual = _protected_implementation_digest(source, path, name)
        if actual != expected:
            failures.append(f"protected validator implementation changed for {name}: expected {expected}; got {actual or '<missing-or-ambiguous>'}")
    return failures


def _definition_time_execution_failures(source: str, path: str) -> list[str]:
    """Reject dynamic execution aliases and decorators in protected verifier source.

    Definition-time dynamic execution can rewrite protected verifier bindings even
    when the call is reached through a module-level alias such as ``runner = exec``.
    Resolve those aliases transitively before scanning calls. Explicit
    ``builtins.exec/eval/compile`` aliases are treated identically.
    """
    if path not in REQUIRED_SEMANTIC_CALLS:
        return []
    tree = ast.parse(source, filename=path)
    failures: list[str] = []
    direct = {"exec", "eval", "compile"}
    dynamic_names = set(direct)
    builtins_names: set[str] = {"builtins"}

    statements = _definition_time_statements(tree)
    for statement in statements:
        if isinstance(statement, ast.Import):
            for alias in statement.names:
                if alias.name == "builtins":
                    builtins_names.add(alias.asname or "builtins")
        elif isinstance(statement, ast.ImportFrom) and statement.module == "builtins":
            for alias in statement.names:
                if alias.name in direct:
                    dynamic_names.add(alias.asname or alias.name)

    def dynamic_source(node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            return node.id in dynamic_names
        return (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id in builtins_names
            and node.attr in direct
        )

    def assigned_names(node: ast.AST) -> set[str]:
        if isinstance(node, ast.Name):
            return {node.id}
        if isinstance(node, (ast.Tuple, ast.List)):
            names: set[str] = set()
            for item in node.elts:
                names.update(assigned_names(item))
            return names
        return set()

    changed = True
    while changed:
        changed = False
        for statement in statements:
            value: ast.AST | None = None
            targets: list[ast.AST] = []
            if isinstance(statement, ast.Assign):
                value = statement.value
                targets = list(statement.targets)
            elif isinstance(statement, ast.AnnAssign) and statement.value is not None:
                value = statement.value
                targets = [statement.target]
            if value is None:
                continue
            names = set().union(*(assigned_names(target) for target in targets))
            if isinstance(value, ast.Name) and value.id in builtins_names:
                for name in names:
                    if name not in builtins_names:
                        builtins_names.add(name)
                        changed = True
            if dynamic_source(value):
                for name in names:
                    if name not in dynamic_names:
                        dynamic_names.add(name)
                        changed = True

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and dynamic_source(node.func):
            failures.append(
                "dynamic execution rejected in protected verifier: "
                f"{ast.unparse(node.func) if hasattr(ast, 'unparse') else _call_name(node)}"
            )
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and node.decorator_list
        ):
            failures.append(
                "protected verifier definition-time decorator rejected: "
                f"{getattr(node, 'name', '<definition>')}"
            )
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


ASSURANCE_REGISTRY_PATH = "far_validation/weakening.py"
ASSURANCE_LOCK_PATH = "validation_bootstrap/assurance-lock.json"
_PINNED_REGISTRIES = (
    "EXPECTED_PROTECTED_IMPLEMENTATION_DIGESTS",
    "REQUIRED_MODULE_BINDING_SIGNATURES",
    "REQUIRED_LIVE_CALL_PREFIXES",
)


def _registry_literals(source: str) -> dict[str, Any]:
    """Read the pinned registries out of a source revision without importing it."""
    values: dict[str, Any] = {}
    try:
        tree = ast.parse(source, filename=ASSURANCE_REGISTRY_PATH)
    except SyntaxError:
        return values
    for statement in tree.body:
        target: str | None = None
        if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            target = statement.target.id
        elif isinstance(statement, ast.Assign) and len(statement.targets) == 1 and isinstance(statement.targets[0], ast.Name):
            target = statement.targets[0].id
        if target not in _PINNED_REGISTRIES or statement.value is None:
            continue
        try:
            values[target] = ast.literal_eval(statement.value)
        except (ValueError, SyntaxError):
            continue
    return values


def _lock_file_digests(source: str) -> dict[str, str]:
    """Read the assurance lock's per-file content pins from a source revision."""
    try:
        payload = json.loads(source)
    except json.JSONDecodeError:
        return {}
    files = payload.get("files") if isinstance(payload, dict) else None
    if not isinstance(files, dict):
        return {}
    return {key: value for key, value in files.items() if isinstance(key, str) and isinstance(value, str)}


def _self_repin_failures(root: Path, revision: str, changed_paths: set[str]) -> dict[str, list[str]]:
    """Reject changing a protected verifier and its own expected pins together.

    The expected values live in the same tree as the code they protect, so a
    change can weaken an implementation and refresh its own pin in one step. That
    cannot be prevented in-tree, but it can be made visible: when a protected
    path and the pins describing it both move in the same change, say so instead
    of reporting success. Paths that do not exist at the comparison base are
    being introduced, which has no prior pin to contradict.
    """
    failures: dict[str, list[str]] = {}
    candidates = sorted(path for path in changed_paths if _show(root, revision, path) is not None)

    # Registries carried inside the detector module.
    base_registry_source = _show(root, revision, ASSURANCE_REGISTRY_PATH)
    if ASSURANCE_REGISTRY_PATH in changed_paths and base_registry_source is not None:
        base_values = _registry_literals(base_registry_source)
        head_values = _registry_literals((root / ASSURANCE_REGISTRY_PATH).read_text(encoding="utf-8"))
        for path in candidates:
            if path == ASSURANCE_REGISTRY_PATH:
                continue
            for registry in _PINNED_REGISTRIES:
                before = (base_values.get(registry) or {}).get(path)
                after = (head_values.get(registry) or {}).get(path)
                if before is not None and before != after:
                    failures.setdefault(path, []).append(
                        f"protected pin {registry} for {path} changed in the same change as {path}; "
                        "an implementation and its own expected value must not be repinned together"
                    )

    # Content pins carried in the bootstrap assurance lock. These live in a
    # different file from the registries above, so a verifier edit paired with a
    # lock refresh needs no change to this module at all.
    base_lock_source = _show(root, revision, ASSURANCE_LOCK_PATH)
    if base_lock_source is not None:
        base_locked = _lock_file_digests(base_lock_source)
        try:
            head_locked = _lock_file_digests((root / ASSURANCE_LOCK_PATH).read_text(encoding="utf-8"))
        except OSError:
            head_locked = {}
        for path in candidates:
            # This module cannot pin itself: any legitimate edit to the detector
            # necessarily updates its own hash. That irreducible self-reference is
            # the documented residual, not something this check can decide.
            if path == ASSURANCE_REGISTRY_PATH:
                continue
            before = base_locked.get(path)
            after = head_locked.get(path)
            if before is not None and before != after:
                failures.setdefault(path, []).append(
                    f"content pin for {path} in {ASSURANCE_LOCK_PATH} changed in the same change as "
                    f"{path}; a protected file and its own expected hash must not be repinned together"
                )
    return failures


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

    # Applied after waivers: a waiver excuses a metric drop on one file, not a
    # change that rewrites the expected values guarding another file.
    repin_failures = _self_repin_failures(root, resolved, {path for _status, path in _changed_python(root, resolved)})
    if repin_failures:
        by_path = {finding.path: finding for finding in findings}
        for path, messages in repin_failures.items():
            finding = by_path.get(path)
            if finding is None:
                finding = WeakeningFinding(path=path)
                findings.append(finding)
            finding.failures.extend(messages)
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