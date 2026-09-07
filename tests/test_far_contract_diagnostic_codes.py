"""The published diagnostic vocabulary must match what the verifiers actually emit.

`EFR-R2` requires two clean-room implementations to agree with the frozen expected result
on outcome, error category, and recomputed evidence, using only the published `far-ir/2.0`
and `far-ir/2.1` specifications. That criterion is unsatisfiable unless every emitted
diagnostic code is published. These tests fail closed on the three ways that can break:
an undocumented code, a documented code the implementation cannot emit, and a new emission
site that never reaches the specification.

The v2.1 verifier builds two codes at runtime as ``DUPLICATE_{label}``, so a source scan
alone is not sufficient; the label arguments are recovered from the call sites.

The declarations live in ``diagnostic_vocabulary`` rather than in the verifiers, because
``contract_v2.py`` is the git-blob-pinned ``PCA-W6`` preregistered protocol base and
``contract_v21.py`` is SHA-256 pinned by the completed ``PCA-W5`` manifest. These tests read
those sources without modifying them.
"""
from __future__ import annotations

import ast
import re
import unittest
from pathlib import Path

from mechanization.far_mechanization import contract_v2, contract_v21
from mechanization.far_mechanization.diagnostic_vocabulary import (
    FAR_IR_2_0_DIAGNOSTIC_CODES,
    FAR_IR_2_1_DIAGNOSTIC_CODES,
)

ROOT = Path(__file__).resolve().parents[1]

CODE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]{5,}$")
DOC_ROW_PATTERN = re.compile(r"^\| `([A-Z0-9_]+)` \|", re.MULTILINE)

# Uppercase string literals in the verifiers that are contract vocabulary rather than
# diagnostic codes. Keeping this list explicit means a new status value must be declared
# deliberately, and a new diagnostic code cannot be hidden by an over-broad filter.
NON_DIAGNOSTIC_LITERALS = {
    "CHECKED_FINITE_EXPLICIT",
    "EXPLICIT",
    "FROZEN",
    "PROVED",
    "REFUTED",
}

# Literals passed as the ``label`` argument of ``contract_v21._unique_values``, which the
# verifier composes into ``DUPLICATE_{label}``. Recovered from call sites below.
DYNAMIC_CODE_BUILDERS = {"_unique_values": "DUPLICATE_{}"}

# Constant prefixes of f-string code templates. These are fragments, not codes, and every
# one of them must correspond to a declared builder in DYNAMIC_CODE_BUILDERS.
KNOWN_CODE_TEMPLATE_PREFIXES = {"DUPLICATE_"}


def _module_source(module) -> str:
    return Path(module.__file__).read_text(encoding="utf-8")


def _fstring_fragments(tree: ast.AST) -> set[str]:
    """Constant parts of f-strings, which are code fragments rather than whole codes."""
    return {
        part.value
        for node in ast.walk(tree)
        if isinstance(node, ast.JoinedStr)
        for part in node.values
        if isinstance(part, ast.Constant) and isinstance(part.value, str)
    }


def _literal_codes(source: str) -> set[str]:
    tree = ast.parse(source)
    fragments = _fstring_fragments(tree)
    literals = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and CODE_PATTERN.match(node.value)
    }
    return literals - NON_DIAGNOSTIC_LITERALS - fragments


def _dynamic_codes(source: str) -> tuple[set[str], set[str]]:
    """Return (composed codes, label literals consumed by the builders)."""
    tree = ast.parse(source)
    composed: set[str] = set()
    labels: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        template = DYNAMIC_CODE_BUILDERS.get(node.func.id)
        if template is None:
            continue
        for argument in node.args:
            if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                if CODE_PATTERN.match(argument.value):
                    composed.add(template.format(argument.value))
                    labels.add(argument.value)
    return composed, labels


def _emitted_codes(module) -> set[str]:
    source = _module_source(module)
    composed, labels = _dynamic_codes(source)
    # A builder label is an argument, not a code the verifier can emit on its own.
    return (_literal_codes(source) - labels) | composed


def _documented_codes(path: Path) -> set[str]:
    return set(DOC_ROW_PATTERN.findall(path.read_text(encoding="utf-8")))


class DiagnosticVocabularyTests(unittest.TestCase):
    cases = (
        (
            "far-ir/2.0",
            contract_v2,
            FAR_IR_2_0_DIAGNOSTIC_CODES,
            ROOT / "docs" / "specification" / "far-ir-2.0-contract.md",
        ),
        (
            "far-ir/2.1",
            contract_v21,
            FAR_IR_2_1_DIAGNOSTIC_CODES,
            ROOT / "docs" / "specification" / "far-ir-2.1-approximation-cost.md",
        ),
    )

    def test_declared_set_matches_emission_sites(self) -> None:
        """A new emission site must be added to the published vocabulary."""
        for name, module, declared, _spec in self.cases:
            with self.subTest(format=name):
                self.assertEqual(
                    _emitted_codes(module),
                    set(declared),
                    f"{name}: published vocabulary does not match the verifier's emission sites",
                )

    def test_declared_set_matches_published_specification(self) -> None:
        """Every declared code must be published, and nothing extra may be published."""
        for name, _module, declared, spec in self.cases:
            with self.subTest(format=name):
                self.assertEqual(
                    set(declared),
                    _documented_codes(spec),
                    f"{name}: specification table does not match the published vocabulary",
                )

    def test_runtime_composed_codes_are_published(self) -> None:
        """The DUPLICATE_{label} codes have no source literal and are easy to omit."""
        composed, _labels = _dynamic_codes(_module_source(contract_v21))
        self.assertEqual(composed, {"DUPLICATE_METRIC_VALUE", "DUPLICATE_LOSS_ACTION"})
        self.assertTrue(composed <= set(FAR_IR_2_1_DIAGNOSTIC_CODES))

    def test_every_code_template_has_a_declared_builder(self) -> None:
        """A new runtime-composed code cannot slip past the source scan unnoticed."""
        for name, module, _declared, _spec in self.cases:
            with self.subTest(format=name):
                tree = ast.parse(_module_source(module))
                templates = {
                    fragment
                    for fragment in _fstring_fragments(tree)
                    if fragment.isupper() and fragment.endswith("_")
                }
                self.assertTrue(
                    templates <= KNOWN_CODE_TEMPLATE_PREFIXES,
                    f"{name}: undeclared code template(s) "
                    f"{sorted(templates - KNOWN_CODE_TEMPLATE_PREFIXES)}; add the builder "
                    "to DYNAMIC_CODE_BUILDERS and publish the composed codes",
                )

    def test_detects_an_undocumented_emission_site(self) -> None:
        """The control fails closed on the defect it exists to prevent."""
        source = _module_source(contract_v2)
        injected = source.replace(
            '"FACTORIZATION_FAILURE"', '"FACTORIZATION_FAILURE_UNPUBLISHED"', 1
        )
        self.assertNotEqual(injected, source)
        self.assertNotIn(
            "FACTORIZATION_FAILURE_UNPUBLISHED", _literal_codes(source)
        )
        self.assertIn("FACTORIZATION_FAILURE_UNPUBLISHED", _literal_codes(injected))
        self.assertNotEqual(_literal_codes(injected), set(FAR_IR_2_0_DIAGNOSTIC_CODES))

    def test_vocabulary_is_not_claimed_complete_or_validated(self) -> None:
        """Publishing the codes is a completeness obligation, not an assurance upgrade."""
        for name, _module, _declared, spec in self.cases:
            with self.subTest(format=name):
                text = spec.read_text(encoding="utf-8")
                self.assertIn("not a claim that the code set is minimal", text)
                self.assertIn("The code is normative and the message is not.", text)


if __name__ == "__main__":
    unittest.main()
