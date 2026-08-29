import unittest

from jsonschema import Draft202012Validator


class LocalJsonSchemaShimTests(unittest.TestCase):
    def errors(self, schema, instance):
        return list(Draft202012Validator(schema).iter_errors(instance))

    def test_union_type_accepts_each_declared_member(self):
        schema = {"type": ["string", "null"]}
        self.assertEqual(self.errors(schema, "bounded"), [])
        self.assertEqual(self.errors(schema, None), [])

    def test_union_type_rejects_undeclared_member(self):
        schema = {"type": ["string", "null"]}
        self.assertEqual(len(self.errors(schema, 7)), 1)

    def test_string_constraints_apply_inside_union_type(self):
        schema = {"type": ["string", "null"], "minLength": 3}
        self.assertEqual(self.errors(schema, None), [])
        self.assertEqual(self.errors(schema, "abc"), [])
        self.assertEqual(len(self.errors(schema, "ab")), 1)

    def test_array_item_validation_applies_inside_union_type(self):
        schema = {"type": ["array", "null"], "items": {"type": "integer"}}
        self.assertEqual(self.errors(schema, None), [])
        self.assertEqual(self.errors(schema, [1, 2]), [])
        self.assertEqual(len(self.errors(schema, [1, "2"])), 1)

    def test_number_type_excludes_boolean(self):
        schema = {"type": "number"}
        self.assertEqual(self.errors(schema, 1.5), [])
        self.assertEqual(self.errors(schema, 1), [])
        self.assertEqual(len(self.errors(schema, True)), 1)


if __name__ == "__main__":
    unittest.main()
