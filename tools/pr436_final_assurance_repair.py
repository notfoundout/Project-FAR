from __future__ import annotations

import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAKENING = ROOT / "far_validation/weakening.py"
TEST = ROOT / "tests/test_target_category_weakening_aliases.py"


def patch_weakening() -> None:
    text = WEAKENING.read_text(encoding="utf-8")

    old_namespace = 'node.func.id in {"globals", "locals"}'
    new_namespace = 'node.func.id in {"globals", "locals", "vars"}'
    if old_namespace not in text:
        raise RuntimeError("namespace accessor patch anchor missing")
    text = text.replace(old_namespace, new_namespace, 1)

    start_marker = "def _definition_time_execution_failures(source: str, path: str) -> list[str]:"
    end_marker = "\ndef analyze(source: str, path: str) -> StrengthMetrics:"
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    replacement = textwrap.dedent(
        '''
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

            def dynamic_source(node: ast.AST) -> bool:
                if isinstance(node, ast.Name):
                    return node.id in dynamic_names
                return (
                    isinstance(node, ast.Attribute)
                    and isinstance(node.value, ast.Name)
                    and node.value.id == "builtins"
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
                for statement in tree.body:
                    value: ast.AST | None = None
                    targets: list[ast.AST] = []
                    if isinstance(statement, ast.Assign):
                        value = statement.value
                        targets = list(statement.targets)
                    elif isinstance(statement, ast.AnnAssign) and statement.value is not None:
                        value = statement.value
                        targets = [statement.target]
                    if value is None or not dynamic_source(value):
                        continue
                    for target in targets:
                        for name in assigned_names(target):
                            if name not in dynamic_names:
                                dynamic_names.add(name)
                                changed = True

            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id in dynamic_names
                ):
                    failures.append(
                        f"dynamic execution rejected in protected verifier: {node.func.id}"
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
        '''
    ).lstrip()
    text = text[:start] + replacement + text[end:]
    WEAKENING.write_text(text, encoding="utf-8")


def write_tests() -> None:
    TEST.write_text(
        r'''from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from far_validation import weakening

ROOT = Path(__file__).resolve().parents[1]
LEGACY_REL = "research/target-category-discovery/verify_compositional_invariant_legacy.py"
LEGACY = ROOT / LEGACY_REL


class TargetCategoryWeakeningAliasTests(unittest.TestCase):
    def _mutated_report(self, suffix: str):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            target = repo / LEGACY_REL
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(LEGACY.read_text(encoding="utf-8"), encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "assurance@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Validator Assurance"], cwd=repo, check=True)
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repo, check=True)
            base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
            target.write_text(target.read_text(encoding="utf-8") + suffix, encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-qm", "adversarial mutation"], cwd=repo, check=True)
            return weakening.detect_weakening(repo, base=base)

    def test_module_alias_to_exec_is_rejected_even_when_called_from_class_body(self) -> None:
        report = self._mutated_report(
            "\n_far_dynamic = exec\n"
            "class _FarAliasAttack:\n"
            "    _far_dynamic('globals()[\\\"validate_empirical_authority\\\"] = lambda *a, **k: None')\n"
        )
        self.assertFalse(report.successful)
        failures = [item for finding in report.findings for item in finding.failures]
        self.assertTrue(any("dynamic execution rejected" in item for item in failures), failures)

    def test_vars_namespace_rebinding_of_protected_helper_is_rejected(self) -> None:
        report = self._mutated_report(
            "\nvars()[\"_git_blob_sha1\"] = lambda payload: None\n"
        )
        self.assertFalse(report.successful)
        failures = [item for finding in report.findings for item in finding.failures]
        self.assertTrue(
            any("protected validator binding changed for _git_blob_sha1" in item for item in failures),
            failures,
        )


if __name__ == "__main__":
    unittest.main()
''',
        encoding="utf-8",
    )


if __name__ == "__main__":
    patch_weakening()
    write_tests()
