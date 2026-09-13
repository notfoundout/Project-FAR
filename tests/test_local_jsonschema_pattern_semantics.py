import importlib
import unittest

import jsonschema
from jsonschema import Draft202012Validator


class LocalJsonSchemaSemanticsTests(unittest.TestCase):
    def errors(self, schema, instance):
        return list(Draft202012Validator(schema).iter_errors(instance))

    def test_pattern_uses_search_semantics(self):
        self.assertEqual(self.errors({"type": "string", "pattern": "^/"}, "/a/b"), [])
        self.assertTrue(self.errors({"type": "string", "pattern": "^/"}, "a/b"))

    def test_array_cardinality_and_uniqueness(self):
        schema = {"type": "array", "minItems": 2, "maxItems": 3, "uniqueItems": True}
        self.assertTrue(self.errors(schema, [1]))
        self.assertEqual(self.errors(schema, [1, 2]), [])
        self.assertTrue(self.errors(schema, [1, 1]))
        self.assertTrue(self.errors(schema, [1, 2, 3, 4]))

    def test_json_equality_distinguishes_boolean_from_number(self):
        self.assertTrue(self.errors({"const": 1}, True))
        self.assertTrue(self.errors({"enum": [1]}, True))
        schema = {"type": "array", "uniqueItems": True}
        self.assertEqual(self.errors(schema, [True, 1]), [])
        self.assertEqual(self.errors(schema, [{"value": True}, {"value": 1}]), [])
        self.assertTrue(self.errors(schema, [1, 1.0]))

    def test_object_cardinality(self):
        schema = {"type": "object", "minProperties": 1, "maxProperties": 2}
        self.assertTrue(self.errors(schema, {}))
        self.assertEqual(self.errors(schema, {"a": 1}), [])
        self.assertTrue(self.errors(schema, {"a": 1, "b": 2, "c": 3}))

    def test_schema_valued_additional_properties(self):
        schema = {
            "type": "object",
            "properties": {"fixed": {"type": "string"}},
            "additionalProperties": {"type": "integer"},
        }
        self.assertEqual(self.errors(schema, {"fixed": "x", "dynamic": 1}), [])
        self.assertTrue(self.errors(schema, {"fixed": "x", "dynamic": "wrong"}))

    def test_module_reload_does_not_mutate_validator_semantics(self):
        """Reloading the package must not stack wrappers or alter global type behavior."""
        for _ in range(2):
            module = importlib.reload(jsonschema)
            validator = module.Draft202012Validator
            self.assertEqual(list(validator({"type": "string"}).iter_errors("x")), [])
            self.assertEqual(list(validator({"type": "integer"}).iter_errors(1.0)), [])
            self.assertTrue(list(validator({"type": "integer"}).iter_errors(True)))
            self.assertEqual(
                list(validator({"type": "array", "uniqueItems": True}).iter_errors([True, 1])),
                [],
            )


if __name__ == "__main__":
    unittest.main()
