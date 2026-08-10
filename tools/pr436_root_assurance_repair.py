from pathlib import Path

p = Path("far_validation/weakening.py")
s = p.read_text(encoding="utf-8")

old = "    protected = REQUIRED_SEMANTIC_CALLS.get(path, frozenset())\n"
new = "    protected = frozenset(set(REQUIRED_SEMANTIC_CALLS.get(path, frozenset())) | set(EXPECTED_PROTECTED_IMPLEMENTATION_DIGESTS.get(path, {})))\n"
assert s.count(old) == 1, "protected-set anchor drifted"
s = s.replace(old, new, 1)

old = '''def _binding_integrity_failures(source: str, path: str) -> list[str]:
    expected = REQUIRED_MODULE_BINDING_SIGNATURES.get(path)
    if expected is None:
        return []
    actual = _module_scope_binding_signatures(source, path)
'''
new = '''def _binding_integrity_failures(source: str, path: str) -> list[str]:
    expected = dict(REQUIRED_MODULE_BINDING_SIGNATURES.get(path, {}))
    for name in EXPECTED_PROTECTED_IMPLEMENTATION_DIGESTS.get(path, {}):
        expected.setdefault(name, ("function",))
    if not expected:
        return []
    actual = _module_scope_binding_signatures(source, path)
'''
assert s.count(old) == 1, "binding-integrity anchor drifted"
s = s.replace(old, new, 1)

start = s.index("def _definition_time_execution_failures(")
end = s.index("\ndef analyze(", start)
newfun = '''def _definition_time_execution_failures(source: str, path: str) -> list[str]:
    """Reject dynamic execution and decorators in protected verifier source."""
    if path not in REQUIRED_SEMANTIC_CALLS:
        return []
    tree = ast.parse(source, filename=path)
    failures: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval", "compile"}:
            failures.append(f"dynamic execution rejected in protected verifier: {node.func.id}")
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.decorator_list:
            failures.append(f"protected verifier definition-time decorator rejected: {getattr(node, 'name', '<definition>')}")
    return failures

'''
s = s[:start] + newfun + s[end + 1 :]
p.write_text(s, encoding="utf-8")

t = Path("tests/test_target_category_validator_assurance_hardening.py")
x = t.read_text(encoding="utf-8")
anchor = '\n\nif __name__ == "__main__":\n    unittest.main()\n'
assert x.count(anchor) == 1, "test append anchor drifted"
add = r'''

    def test_class_body_dynamic_exec_rebinding_is_rejected(self) -> None:
        tmp, repo, base = self._repo()
        self.addCleanup(tmp.cleanup)
        for protected in weakening.REQUIRED_SEMANTIC_CALLS:
            target = repo / protected
            text = target.read_text(encoding="utf-8")
            text += "\nclass _FarDefinitionTimeAttack:\n    exec(\"globals()['validate_empirical_authority'] = lambda *a, **k: None\")\n    exec(\"globals()['validate_gate'] = lambda *a, **k: None\")\n"
            target.write_text(text, encoding="utf-8")
        report = self._commit_and_report(repo, base, "class-body dynamic execution attack")
        self.assertFalse(report.successful)
        checked = 0
        for finding in report.findings:
            if finding.path in weakening.REQUIRED_SEMANTIC_CALLS:
                checked += 1
                self.assertTrue(any("dynamic execution rejected" in item for item in finding.failures))
        self.assertEqual(checked, len(weakening.REQUIRED_SEMANTIC_CALLS))

    def test_protected_helper_rebinding_is_rejected(self) -> None:
        tmp, repo, base = self._repo()
        self.addCleanup(tmp.cleanup)
        rel = "research/target-category-discovery/verify_compositional_invariant_legacy.py"
        target = repo / rel
        text = target.read_text(encoding="utf-8")
        target.write_text(text + "\n_git_blob_sha1 = lambda raw: '0' * 40\n", encoding="utf-8")
        report = self._commit_and_report(repo, base, "protected helper rebinding attack")
        self.assertFalse(report.successful)
        failures = next(f.failures for f in report.findings if f.path == rel)
        self.assertTrue(any("protected validator binding changed for _git_blob_sha1" in item for item in failures))

    def test_verify_early_return_after_authority_prefix_is_rejected(self) -> None:
        tmp, repo, base = self._repo()
        self.addCleanup(tmp.cleanup)
        rel = "research/target-category-discovery/verify_compositional_invariant_legacy.py"
        target = repo / rel
        text = target.read_text(encoding="utf-8")
        needle = "    validate_gate(gates_path)\n    actual = build_result(load_json(spec_path))\n"
        self.assertEqual(text.count(needle), 1)
        target.write_text(text.replace(needle, "    validate_gate(gates_path)\n    return {}\n    actual = build_result(load_json(spec_path))\n", 1), encoding="utf-8")
        report = self._commit_and_report(repo, base, "verify post-prefix early-return attack")
        self.assertFalse(report.successful)
        failures = next(f.failures for f in report.findings if f.path == rel)
        self.assertTrue(any("protected validator implementation changed for verify" in item for item in failures))
'''
t.write_text(x.replace(anchor, add + anchor, 1), encoding="utf-8")
