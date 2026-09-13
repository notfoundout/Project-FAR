import unittest

from jsonschema import Draft202012Validator
from mechanization.far_mechanization.intake_v1 import (
    _json_native_errors,
    _strict_json_loads,
    _terminal_saturation_errors,
    new_manifest,
    validate_manifest,
)


class IntakeBoundaryHardeningTests(unittest.TestCase):
    def assert_has(self, errors, text):
        self.assertTrue(any(text in error for error in errors), (text, errors))

    def test_programmatic_intake_requires_strict_json_native_tree(self):
        cases = []

        m = new_manifest("raw", "INTAKE-NATIVE-TUPLE")
        m["discovery"]["search_protocol"]["limitations"] = ("not", "a", "list")
        cases.append(m)

        m = new_manifest("raw", "INTAKE-NATIVE-KEY")
        m["raw_input"][1] = "non-string key"
        cases.append(m)

        m = new_manifest("raw", "INTAKE-NATIVE-SET")
        m["discovery"]["search_protocol"]["limitations"] = [{"python-only"}]
        cases.append(m)

        m = new_manifest("raw", "INTAKE-NATIVE-NAN")
        m["freeze"]["frozen_at"] = float("nan")
        cases.append(m)

        for manifest in cases:
            with self.subTest(identifier=manifest["id"]):
                self.assert_has(
                    validate_manifest(manifest),
                    "not canonical-JSON serializable",
                )

    def test_json_native_checker_accepts_only_json_container_and_scalar_types(self):
        self.assertEqual(
            _json_native_errors(
                {"a": [None, True, False, 0, 1.0, "x", {"b": []}]}
            ),
            [],
        )
        self.assert_has(_json_native_errors((1, 2)), "unsupported Python type tuple")

    def test_strict_parser_rejects_duplicate_keys_at_every_depth(self):
        for text in (
            '{"a": 1, "a": 2}',
            '{"outer": {"a": 1, "a": 2}}',
        ):
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, "duplicate JSON object key: a"):
                    _strict_json_loads(text)

    def test_strict_parser_rejects_python_json_nonfinite_extensions(self):
        for token in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(token=token):
                with self.assertRaisesRegex(ValueError, "non-finite JSON number"):
                    _strict_json_loads('{"value": ' + token + '}')

    def test_terminal_zero_new_round_rechecks_every_registered_query_and_source(self):
        protocol = {
            "saturation_observations": [
                {
                    "round": 1,
                    "query_ids": ["q.2"],
                    "source_ids": ["src.2"],
                    "new_claim_parse_ids": [],
                    "new_material_interpretation_ids": [],
                },
                {
                    "round": 2,
                    "query_ids": ["q.1"],
                    "source_ids": ["src.1"],
                    "new_claim_parse_ids": [],
                    "new_material_interpretation_ids": [],
                },
            ]
        }
        errors = _terminal_saturation_errors(
            protocol,
            {"q.1", "q.2"},
            {"src.1", "src.2"},
        )
        self.assert_has(errors, "registered queries: q.2")
        self.assert_has(errors, "registered sources: src.2")

        protocol["saturation_observations"][-1]["query_ids"] = ["q.1", "q.2"]
        protocol["saturation_observations"][-1]["source_ids"] = ["src.1", "src.2"]
        self.assertEqual(
            _terminal_saturation_errors(
                protocol,
                {"q.1", "q.2"},
                {"src.1", "src.2"},
            ),
            [],
        )

    def test_draft_2020_12_integer_type_accepts_integral_floats_not_booleans(self):
        validator = Draft202012Validator({"type": "integer"})
        for value in (0, 1, -2, 0.0, 1.0, -2.0):
            with self.subTest(value=value):
                self.assertEqual(list(validator.iter_errors(value)), [])
        for value in (True, False, 1.5, -2.25):
            with self.subTest(value=value):
                self.assertTrue(list(validator.iter_errors(value)))


if __name__ == "__main__":
    unittest.main()
