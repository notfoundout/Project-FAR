import copy
import importlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from mechanization.far_mechanization.intake_v1 import (
    _json_native_errors,
    _strict_json_loads,
    _terminal_saturation_errors,
    aggregate_manifest,
    freeze_manifest,
    new_manifest,
    sha256_json,
    validate_manifest,
)
from tests.test_far_intake_v1 import STAMP, manifest


class IntakeBoundaryHardeningTests(unittest.TestCase):
    def assert_has(self, errors, text):
        self.assertTrue(any(text in error for error in errors), (text, errors))

    def test_reload_preserves_validation_freeze_and_aggregation(self):
        from mechanization.far_mechanization import intake_v1

        for _ in range(2):
            importlib.reload(intake_v1)
            self.assertEqual(intake_v1.validate_manifest(manifest(), require_complete=True), [])
            frozen = intake_v1.freeze_manifest(manifest(), frozen_at=STAMP)
            self.assertEqual(validate_manifest(frozen), [])
            self.assertEqual(intake_v1.aggregate_manifest(frozen)["outcome"], "INCOMPLETE")
            invalid = manifest()
            invalid["discovery"]["terms"] = ()
            self.assertTrue(intake_v1.validate_manifest(invalid))
            with self.assertRaises(ValueError):
                intake_v1.freeze_manifest(invalid, frozen_at=STAMP)

    def test_malformed_shapes_fail_closed_across_public_operations(self):
        for value in (None, [], 42, "text", {}, {"freeze": None}, {"freeze": []}):
            with self.subTest(value=value):
                self.assertTrue(validate_manifest(value))
                self.assertEqual(aggregate_manifest(value)["outcome"], "INVALID")
                with self.assertRaisesRegex(ValueError, "cannot freeze invalid manifest"):
                    freeze_manifest(value, frozen_at=STAMP)

    def test_unpaired_surrogates_fail_closed_but_unicode_round_trips(self):
        for value in ("\ud800", "\udfff"):
            for location in ("text", "key", "contract"):
                m = manifest()
                if location == "text":
                    m["raw_input"]["text"] = value
                elif location == "key":
                    m["discovery"]["contract_candidates"][0]["contract"][value] = 1
                else:
                    m["discovery"]["contract_candidates"][0]["contract"]["bad"] = value
                with self.subTest(value=repr(value), location=location):
                    self.assert_has(validate_manifest(m), "not canonical-JSON serializable")
                    with self.assertRaises(ValueError):
                        freeze_manifest(m, frozen_at=STAMP)
                    with self.assertRaises(ValueError):
                        _strict_json_loads(json.dumps(m))
        raw = "Ω café 😀"
        self.assertEqual(validate_manifest(new_manifest(raw)), [])
        self.assertEqual(_strict_json_loads(json.dumps(raw)), raw)

    def test_cyclic_and_excessively_nested_inputs_fail_closed(self):
        cyclic = []
        cyclic.append(cyclic)
        nested = []
        for _ in range(sys.getrecursionlimit() + 10):
            nested = [nested]
        for value, diagnostic in ((cyclic, "cyclic container"), (nested, "nesting exceeds")):
            m = manifest()
            m["discovery"]["contract_candidates"][0]["contract"]["bad"] = value
            with self.subTest(diagnostic=diagnostic):
                self.assert_has(validate_manifest(m), diagnostic)
                self.assertEqual(aggregate_manifest(m)["outcome"], "INVALID")
                with self.assertRaises(ValueError):
                    freeze_manifest(m, frozen_at=STAMP)
        shared = ["valid"]
        self.assertEqual(_json_native_errors({"a": shared, "b": shared}), [])
        depth = sys.getrecursionlimit() + 10
        with self.assertRaisesRegex(ValueError, "nesting exceeds"):
            _strict_json_loads("[" * depth + "0" + "]" * depth)

    def test_saturation_timestamps_follow_round_order(self):
        m = manifest()
        rows = m["discovery"]["search_protocol"]["saturation_observations"]
        rows.append(copy.deepcopy(rows[0]))
        rows[-1].update(round=2, observed_at="2026-09-12T10:10:00Z")
        self.assert_has(validate_manifest(m, require_complete=True), "timestamps must be nondecreasing")
        with self.assertRaises(ValueError):
            freeze_manifest(m, frozen_at=STAMP)
        # Equivalent instants in different timezones are not backwards in time.
        rows[-1]["observed_at"] = "2026-09-12T12:30:00+02:00"
        self.assertEqual(validate_manifest(m, require_complete=True), [])

    def test_terminal_recheck_is_enforced_by_validate_and_freeze(self):
        m = manifest()
        protocol = m["discovery"]["search_protocol"]
        protocol["queries"].append(dict(protocol["queries"][0], id="q.2"))
        rows = protocol["saturation_observations"]
        rows[0]["query_ids"].append("q.2")
        rows.append(copy.deepcopy(rows[0]))
        rows[-1].update(round=2, query_ids=["q.1"], source_ids=["src.1"])
        errors = validate_manifest(m, require_complete=True)
        self.assert_has(errors, "registered queries: q.2")
        self.assert_has(errors, "registered sources: src.2")
        with self.assertRaisesRegex(ValueError, "final saturation observation"):
            freeze_manifest(m, frozen_at=STAMP)
        rows[-1].update(query_ids=["q.1", "q.2"], source_ids=["src.1", "src.2"])
        self.assertEqual(validate_manifest(freeze_manifest(m, frozen_at=STAMP)), [])

    def test_cli_rejects_malformed_input_with_json_diagnostic(self):
        depth = sys.getrecursionlimit() + 10
        for text in ('{"freeze": null}', '{"a": "\\ud800"}', '{"\\ud800": 1, "\\ud800": 2}', "[" * depth + "0" + "]" * depth):
            with self.subTest(text=text[:80]), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "intake.json"
                path.write_text(text, encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, "-m", "mechanization.far_mechanization.intake_v1", "freeze", str(path)],
                    text=True, capture_output=True, check=False, timeout=10,
                )
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertFalse(json.loads(result.stdout)["valid"])

    def test_explicit_invalid_freeze_timestamp_is_not_replaced_with_now(self):
        for stamp in ("", False, 0, [], {}):
            with self.subTest(stamp=stamp), self.assertRaisesRegex(ValueError, "frozen_at must be"):
                freeze_manifest(manifest(), frozen_at=stamp)

    def test_frozen_completeness_cannot_be_disabled(self):
        m = freeze_manifest(manifest(), frozen_at=STAMP)
        m["discovery"]["contract_candidates"].pop()
        m["freeze"]["intake_sha256"] = sha256_json({"raw_input": m["raw_input"], "discovery": m["discovery"]})
        m["freeze"]["freeze_sha256"] = sha256_json({"intake_sha256": m["freeze"]["intake_sha256"], "frozen_at": STAMP})
        self.assert_has(validate_manifest(m, require_complete=False), "omits 1 admissible")

    def test_large_missing_cartesian_family_is_rejected_without_expansion(self):
        # A small input describes 2**40 combinations. A finite input must not
        # require enumerating that absent family just to report incompleteness.
        code = '''
from tests.test_far_intake_v1 import manifest
from mechanization.far_mechanization.intake_v1 import validate_manifest
m = manifest()
d = m["discovery"]
d["terms"] = []
d["interpretations"] = []
for n in range(40):
    tid = f"term.{n}"
    ids = [f"i.{n}.0", f"i.{n}.1"]
    d["terms"].append({"id": tid, "surface": tid, "material": True,
        "materiality_basis": "RAW_INPUT", "materiality_source_ids": [],
        "materiality_derivation": "Explicit input choice", "effect_if_misclassified": "Changes contract",
        "interpretation_ids": ids})
    d["interpretations"].extend({"id": iid, "term_id": tid, "statement": iid,
        "origin": "SOURCE_EXPLICIT", "source_ids": ["src.1"], "derivation": None,
        "scope": "bounded"} for iid in ids)
ids = [row["id"] for row in d["terms"]]
d["claim_parses"][0]["term_ids"] = ids
d["search_protocol"]["queries"][0]["term_ids"] = ids
d["contract_candidates"] = []
assert validate_manifest(m, require_complete=True) == [
    "contract family omits 1099511627776 admissible interpretation combination(s)"
]
'''
        result = subprocess.run([sys.executable, "-c", code], text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_counted_family_preserves_exclusions_and_empty_assignment(self):
        m = manifest()
        d = m["discovery"]
        candidate = d["contract_candidates"][-1]
        d["compatibility_exclusions"].append({"claim_parse_id": "parse.a",
            "assignments": candidate["assignments"], "reason": "Scope restriction",
            "basis": "SOURCE", "source_ids": ["src.2"], "derivation": None})
        self.assert_has(validate_manifest(m, require_complete=True), "contains 1 non-admissible")
        d["contract_candidates"].pop()
        self.assertEqual(validate_manifest(m, require_complete=True), [])
        d["contract_candidates"].clear()
        self.assert_has(validate_manifest(m, require_complete=True), "omits 1 admissible")

        m = manifest()
        d = m["discovery"]
        for term in d["terms"]:
            term["material"] = False
        d["search_protocol"]["queries"][0]["term_ids"] = []
        contract = {"behavior": "fixed"}
        d["contract_candidates"] = [{"id": "contract.fixed", "claim_parse_id": "parse.a",
            "assignments": {}, "contract": contract, "sha256": sha256_json(contract),
            "parameter_provenance": [{"path": "/behavior", "basis": "RAW_INPUT", "source_ids": [],
                "interpretation_ids": [], "assumption_ids": [], "derivation": "Fixed by raw input"}]}]
        self.assertEqual(validate_manifest(freeze_manifest(m, frozen_at=STAMP)), [])
        d["contract_candidates"].clear()
        self.assert_has(validate_manifest(m, require_complete=True), "omits 1 admissible")

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
