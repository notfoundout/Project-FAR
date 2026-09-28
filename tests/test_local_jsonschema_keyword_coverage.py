"""The local validator must enforce every keyword the governed schemas use, or fail closed.

Expected outcomes are literal values derived from the JSON Schema 2020-12 validation
vocabulary and ECMA-262 regular-expression semantics, not from this implementation. Before
this suite existed the validator silently ignored `if`/`then`/`else`, `propertyNames`,
`anyOf`, `not`, and `contains`, so constraints declared in `far-contract-v2`, `far-contract-v2.1`,
`far-epistemic-v1`, `far-source-lineage-v1`, and `far-knowledge-graph-v1` were never enforced.
"""
from __future__ import annotations

import copy
import json
import subprocess
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from mechanization.far_mechanization.contract_v2 import contract_sha256, validate_contract

ROOT = Path(__file__).resolve().parents[1]
# The only repository schema the local validator cannot evaluate: it references a sibling file,
# and no repository code validates instances against it with the local validator.
NON_LOCAL_REF_SCHEMAS = {
    "theory/evaluation/comparative-representation/schemas/evaluator-mapping-submission.schema.json",
}


def errors(schema, instance):
    return list(Draft202012Validator(schema).iter_errors(instance))


class KeywordSemanticsTests(unittest.TestCase):
    def test_if_then_else(self):
        schema = {
            "if": {"properties": {"mode": {"const": "approximate"}}, "required": ["mode"]},
            "then": {"required": ["approximation"]},
            "else": {"required": ["exact"]},
        }
        self.assertEqual(errors(schema, {"mode": "approximate", "approximation": {}}), [])
        self.assertEqual(len(errors(schema, {"mode": "approximate"})), 1)
        self.assertEqual(errors(schema, {"mode": "exact", "exact": 1}), [])
        self.assertEqual(len(errors(schema, {"mode": "exact"})), 1)
        self.assertEqual(errors({"then": {"required": ["x"]}}, {}), [])  # then without if is ignored

    def test_property_names(self):
        schema = {"type": "object", "propertyNames": {"pattern": "^[A-Za-z][A-Za-z0-9_.:-]*$"}}
        self.assertEqual(errors(schema, {"w4.domain": 1}), [])
        self.assertEqual(len(errors(schema, {"9bad": 1})), 1)
        self.assertEqual(len(errors(schema, {"ok": 1, "has space": 2, "-x": 3})), 2)

    def test_any_of_and_not(self):
        schema = {"anyOf": [{"type": "string"}, {"type": "integer", "minimum": 3}]}
        self.assertEqual(errors(schema, "s"), [])
        self.assertEqual(errors(schema, 3), [])
        self.assertEqual(len(errors(schema, 2)), 1)
        self.assertEqual(len(errors(schema, None)), 1)
        self.assertEqual(errors({"not": {"const": "x"}}, "y"), [])
        self.assertEqual(len(errors({"not": {"const": "x"}}, "x")), 1)

    def test_contains_min_and_max(self):
        schema = {"type": "array", "contains": {"const": 1}, "minContains": 2, "maxContains": 3}
        self.assertEqual(len(errors(schema, [1, 0])), 1)
        self.assertEqual(errors(schema, [1, 1, 0]), [])
        self.assertEqual(len(errors(schema, [1, 1, 1, 1])), 1)
        self.assertEqual(len(errors({"contains": {"const": 1}}, [])), 1)
        self.assertEqual(errors({"contains": {"const": 1}, "minContains": 0}, []), [])

    def test_boolean_subschemas(self):
        self.assertEqual(errors({"properties": {"a": True}}, {"a": 1}), [])
        self.assertEqual(len(errors({"properties": {"a": False}}, {"a": 1})), 1)
        self.assertEqual(len(errors({"items": False}, [1])), 1)
        self.assertEqual(errors({"items": False}, []), [])

    def test_ref_siblings_are_evaluated(self):
        schema = {"$defs": {"s": {"type": "string"}}, "$ref": "#/$defs/s", "minLength": 2}
        self.assertEqual(errors(schema, "ab"), [])
        self.assertEqual(len(errors(schema, "a")), 1)
        self.assertEqual(len(errors(schema, 1)), 1)

    def test_pattern_dollar_is_end_of_input(self):
        identifier = {"type": "string", "pattern": "^[A-Za-z][A-Za-z0-9_.:-]*$"}
        self.assertEqual(errors(identifier, "case.a"), [])
        self.assertEqual(len(errors(identifier, "case.a\n")), 1)
        self.assertEqual(errors({"pattern": "a\\$"}, "a$"), [])  # escaped dollar stays literal
        self.assertEqual(errors({"pattern": "^[$]$"}, "$"), [])  # class dollar stays literal

    def test_pattern_dot_excludes_line_terminators(self):
        schema = {"type": "string", "pattern": "^a.b$"}
        self.assertEqual(errors(schema, "axb"), [])
        for terminator in ("\n", "\r", " ", " "):
            with self.subTest(terminator=repr(terminator)):
                self.assertEqual(len(errors(schema, f"a{terminator}b")), 1)
        self.assertEqual(errors({"pattern": "^a[.]b$"}, "a.b"), [])

    def test_format_remains_an_annotation(self):
        self.assertEqual(errors({"type": "string", "format": "date-time"}, "not a time"), [])


class FailClosedTests(unittest.TestCase):
    def test_unsupported_keywords_raise_instead_of_passing(self):
        for keyword, value in (
            ("patternProperties", {"^x": {"type": "string"}}),
            ("multipleOf", 2),
            ("dependentRequired", {"a": ["b"]}),
            ("prefixItems", [{"type": "string"}]),
            ("unevaluatedProperties", False),
        ):
            with self.subTest(keyword=keyword):
                with self.assertRaises(ValidationError):
                    Draft202012Validator({"type": "object", keyword: value})

    def test_nested_unsupported_keyword_raises(self):
        with self.assertRaises(ValidationError):
            Draft202012Validator({"properties": {"a": {"allOf": [{"multipleOf": 3}]}}})

    def test_unknown_type_non_local_ref_and_bad_pattern_raise(self):
        for schema in ({"type": "strng"}, {"$ref": "other.json"}, {"$ref": "#/$defs/missing"}, {"pattern": "("}):
            with self.subTest(schema=schema):
                with self.assertRaises(ValidationError):
                    Draft202012Validator(schema)

    def test_every_repository_schema_is_fully_enforced(self):
        tracked = subprocess.run(
            ["git", "ls-files", "*.json"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.split()
        checked = 0
        for rel in tracked:
            try:
                document = json.loads((ROOT / rel).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if not isinstance(document, dict) or "json-schema.org" not in str(document.get("$schema", "")):
                continue
            with self.subTest(schema=rel):
                if rel in NON_LOCAL_REF_SCHEMAS:
                    with self.assertRaises(ValidationError):
                        Draft202012Validator.check_schema(document)
                else:
                    Draft202012Validator.check_schema(document)
                    checked += 1
        self.assertGreaterEqual(checked, 40)


class ContractSchemaRegressionTests(unittest.TestCase):
    """Constraints the far-ir/2.0 schema declares but the validator previously ignored."""

    def setUp(self):
        self.base = json.loads((ROOT / "conformance/far-ir-2.0/valid-quotient.json").read_text(encoding="utf-8"))

    def codes(self, document):
        return [diagnostic.code for diagnostic in validate_contract(document).diagnostics]

    def test_fixture_is_clean(self):
        self.assertEqual(self.codes(self.base), [])

    def test_frozen_record_requires_freeze_time(self):
        document = copy.deepcopy(self.base)
        document["freeze"]["frozen_at"] = None
        self.assertEqual(self.codes(document), ["SCHEMA_CONSTRAINT_VIOLATION"])

    def test_approximate_mode_requires_approximation_block(self):
        document = copy.deepcopy(self.base)
        document["contract"]["mode"] = "approximate"
        document["report"]["evidence"]["status"] = "DECLARED_UNCHECKED"
        document["freeze"]["contract_sha256"] = contract_sha256(document["contract"])
        self.assertEqual(self.codes(document), ["SCHEMA_CONSTRAINT_VIOLATION"])

    def test_extension_names_are_constrained(self):
        document = copy.deepcopy(self.base)
        document["report"]["extensions"] = {"9bad name": 1}
        self.assertEqual(self.codes(document), ["SCHEMA_CONSTRAINT_VIOLATION"])

    def test_identifier_with_trailing_newline_is_rejected(self):
        document = copy.deepcopy(self.base)
        document["contract"]["id"] = "quotient.contract\n"
        document["freeze"]["contract_sha256"] = contract_sha256(document["contract"])
        self.assertEqual(self.codes(document), ["SCHEMA_CONSTRAINT_VIOLATION"])


if __name__ == "__main__":
    unittest.main()
