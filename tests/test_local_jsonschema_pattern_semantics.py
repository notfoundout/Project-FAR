import unittest

from jsonschema import Draft202012Validator


class LocalJsonSchemaPatternSemanticsTests(unittest.TestCase):
    def test_pattern_uses_search_semantics(self):
        validator = Draft202012Validator({"type": "string", "pattern": "^/"})
        self.assertEqual(list(validator.iter_errors("/a/b")), [])

    def test_pattern_still_rejects_nonmatching_string(self):
        validator = Draft202012Validator({"type": "string", "pattern": "^/"})
        self.assertTrue(list(validator.iter_errors("a/b")))


if __name__ == "__main__":
    unittest.main()
