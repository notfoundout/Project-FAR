from pathlib import Path
import hashlib, json

p = Path("far_validation/weakening.py")
s = p.read_text(encoding="utf-8")

anchor = 'REQUIRED_SEMANTIC_CALLS: dict[str, frozenset[str]] = {\n    path: frozenset(prefix) for path, prefix in REQUIRED_LIVE_CALL_PREFIXES.items()\n}\n\n\n'
policy = anchor + 'REQUIRED_MODULE_BINDING_SIGNATURES: dict[str, dict[str, tuple[str, ...]]] = {\n    "research/target-category-discovery/verify_compositional_invariant.py": {\n        "validate_empirical_authority": (),\n        "validate_gate": ("function", "attribute:_core", "globals"),\n    },\n    "research/target-category-discovery/verify_compositional_invariant_legacy.py": {\n        "validate_empirical_authority": ("function",),\n        "validate_gate": ("function",),\n    },\n}\n\n\n'
if s.count(anchor) != 1:
    raise SystemExit(f"binding policy anchor count={s.count(anchor)}")
s = s.replace(anchor, policy, 1)

helper_anchor = "def analyze(source: str, path: str) -> StrengthMetrics:\n"
helper = '''def _module_scope_binding_signatures(source: str, path: str) -> dict[str, tuple[str, ...]]:
    """Return structural module-scope binding events for protected validators."""
    protected = REQUIRED_SEMANTIC_CALLS.get(path, frozenset())
    events: dict[str, list[str]] = {name: [] for name in protected}
    if not protected:
        return {}
    tree = ast.parse(source, filename=path)

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
            value = target.value
            key = target.slice
            if (
                isinstance(value, ast.Call)
                and isinstance(value.func, ast.Name)
                and value.func.id in {"globals", "locals"}
                and not value.args
                and isinstance(key, ast.Constant)
                and isinstance(key.value, str)
                and key.value in protected
            ):
                events[key.value].append(value.func.id)

    def scan_expr(expr: ast.AST) -> None:
        for node in ast.walk(expr):
            if isinstance(node, ast.NamedExpr):
                record_target(node.target, "namedexpr")
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
                continue
            if isinstance(st, ast.ClassDef):
                if st.name in protected:
                    events[st.name].append("class")
                continue
            if isinstance(st, ast.Assign):
                for target in st.targets:
                    record_target(target, "assign")
                scan_expr(st.value)
            elif isinstance(st, ast.AnnAssign):
                record_target(st.target, "annassign")
                if st.value is not None:
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


'''
if s.count(helper_anchor) != 1:
    raise SystemExit("analyze helper anchor drifted")
s = s.replace(helper_anchor, helper + helper_anchor, 1)

detect_anchor = '            required_prefix = REQUIRED_LIVE_CALL_PREFIXES.get(path)\n            if required_prefix:\n                actual_prefix = _live_call_prefix(after_source, path, count=len(required_prefix))\n                if actual_prefix != required_prefix:\n                    finding.failures.append(\n                        "required live verify call prefix changed: expected "\n                        + " -> ".join(required_prefix)\n                        + "; got "\n                        + " -> ".join(name or "<non-call>" for name in actual_prefix)\n                    )\n'
if s.count(detect_anchor) != 1:
    raise SystemExit(f"detect anchor count={s.count(detect_anchor)}")
s = s.replace(detect_anchor, detect_anchor + "            finding.failures.extend(_binding_integrity_failures(after_source, path))\n", 1)
p.write_text(s, encoding="utf-8", newline="\n")

tests = Path("tests/test_target_category_compositional_invariant.py")
t = tests.read_text(encoding="utf-8")
tail = '            for protected in weakening.REQUIRED_SEMANTIC_CALLS:\n                self.assertIn(protected, early_failures)\n                self.assertTrue(any("required live verify call prefix changed" in item for item in early_failures[protected]))\n'
mutation = tail + '\n            subprocess.run(["git", "reset", "--hard", base], cwd=repo, check=True, stdout=subprocess.DEVNULL)\n            for protected in weakening.REQUIRED_SEMANTIC_CALLS:\n                target = repo / protected\n                source = target.read_text(encoding="utf-8")\n                source += "\\nvalidate_empirical_authority = lambda *args, **kwargs: None\\n"\n                source += "validate_gate = lambda *args, **kwargs: None\\n"\n                target.write_text(source, encoding="utf-8")\n            subprocess.run(["git", "add", "."], cwd=repo, check=True)\n            subprocess.run(["git", "commit", "-qm", "rebind protected authority validators"], cwd=repo, check=True)\n            rebound_report = weakening.detect_weakening(repo, base=base)\n            self.assertFalse(rebound_report.successful)\n            rebound_failures = {finding.path: finding.failures for finding in rebound_report.findings}\n            for protected in weakening.REQUIRED_SEMANTIC_CALLS:\n                self.assertIn(protected, rebound_failures)\n                self.assertTrue(any("protected validator binding changed" in item for item in rebound_failures[protected]))\n'
if t.count(tail) != 1:
    raise SystemExit(f"test insertion anchor count={t.count(tail)}")
tests.write_text(t.replace(tail, mutation, 1), encoding="utf-8", newline="\n")

lock_path = Path("validation_bootstrap/assurance-lock.json")
lock = json.loads(lock_path.read_text(encoding="utf-8"))
lock["files"]["far_validation/weakening.py"] = hashlib.sha256(p.read_bytes()).hexdigest()
lock_path.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
