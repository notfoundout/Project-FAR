import json
from pathlib import Path
import unittest

from mechanization.far_mechanization import (
    DiagnosticCode, ExternalFARDocument, FORMAT_VERSION, Identifier, Claim,
    Investigation, FARDocument, IRKind, Reference,
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schemas" / "far-document.schema.json"
VALID = ROOT / "tests" / "fixtures" / "mechanization" / "valid"
INVALID = ROOT / "tests" / "fixtures" / "mechanization" / "invalid"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ExternalModelTests(unittest.TestCase):
    def test_json_schema_loads_successfully(self):
        schema = load(SCHEMA)
        self.assertEqual(schema["properties"]["format_version"]["const"], FORMAT_VERSION)
        self.assertIn("FARDocument", schema.get("title", "") + schema.get("description", ""))
        self.assertIn("$defs", schema)

    def test_all_valid_fixtures_construct_and_validate(self):
        for path in VALID.glob("*.json"):
            with self.subTest(path=path.name):
                doc, diagnostics = ExternalFARDocument.from_mapping(load(path))
                self.assertIsNotNone(doc)
                self.assertEqual(diagnostics, ())
                ir, ir_diagnostics = doc.to_ir()
                self.assertEqual(ir_diagnostics, ())
                self.assertEqual(str(ir.identifier), doc.id)

    def test_all_invalid_fixtures_fail_for_expected_reason(self):
        expected = {
            "missing-format-version.json": DiagnosticCode.UNSUPPORTED_FORMAT_VERSION,
            "unsupported-format-version.json": DiagnosticCode.UNSUPPORTED_FORMAT_VERSION,
            "invalid-identifier.json": DiagnosticCode.INVALID_IDENTIFIER,
            "unknown-object-kind.json": DiagnosticCode.INVALID_EXTERNAL_OBJECT_KIND,
            "missing-required-field.json": DiagnosticCode.MISSING_REQUIRED_FIELD,
            "wrong-field-type.json": DiagnosticCode.EXTERNAL_FIELD_TYPE_MISMATCH,
            "unknown-core-property.json": DiagnosticCode.UNKNOWN_CORE_FIELD,
            "malformed-source-location.json": DiagnosticCode.INVALID_SOURCE_RANGE,
            "invalid-graph-node-kind.json": DiagnosticCode.SCHEMA_CONSTRAINT_VIOLATION,
            "invalid-graph-edge-kind.json": DiagnosticCode.SCHEMA_CONSTRAINT_VIOLATION,
        }
        for path in INVALID.glob("*.json"):
            with self.subTest(path=path.name):
                doc, diagnostics = ExternalFARDocument.from_mapping(load(path))
                if doc is not None:
                    _, ir_diagnostics = doc.to_ir()
                    diagnostics = diagnostics + ir_diagnostics
                codes = {d.code for d in diagnostics}
                self.assertIn(expected[path.name], codes)

    def test_round_trip_from_external_to_ir_and_back_is_lossless_for_supported_fields(self):
        original, diagnostics = ExternalFARDocument.from_mapping(load(VALID / "all-core-objects.json"))
        self.assertEqual(diagnostics, ())
        ir, ir_diagnostics = original.to_ir()
        self.assertEqual(ir_diagnostics, ())
        external, conversion_diagnostics = ExternalFARDocument.from_ir(ir)
        self.assertEqual(conversion_diagnostics, ())
        self.assertEqual(external.format_version, FORMAT_VERSION)
        self.assertEqual([s.order for s in external.reasoning_steps], [1])
        self.assertEqual(external.metadata["suite"], "mechanization")
        self.assertEqual(external.source.source, "fixture")

    def test_canonical_ir_to_external_model(self):
        ir = FARDocument(
            Identifier("DOC-native"),
            Investigation(Identifier("INV-native"), question="Native?"),
            claims=(Claim(Identifier("C-native"), statement="Native claim"),),
        )
        external, diagnostics = ExternalFARDocument.from_ir(ir)
        self.assertEqual(diagnostics, ())
        self.assertEqual(external.format_version, FORMAT_VERSION)
        self.assertEqual(external.claims[0].id, "C-native")

    def test_unsupported_version_diagnostic(self):
        data = load(VALID / "minimal-far-document.json")
        data["format_version"] = "far-ir/0.1"
        doc, diagnostics = ExternalFARDocument.from_mapping(data)
        self.assertIsNone(doc)
        self.assertEqual(diagnostics[0].code, DiagnosticCode.UNSUPPORTED_FORMAT_VERSION)

    def test_unknown_field_rejection(self):
        data = load(VALID / "minimal-far-document.json")
        data["unknown"] = True
        doc, diagnostics = ExternalFARDocument.from_mapping(data)
        self.assertIsNone(doc)
        self.assertTrue(any(d.code == DiagnosticCode.UNKNOWN_CORE_FIELD for d in diagnostics))

    def test_no_cross_reference_resolution_or_dependency_validation_occurs(self):
        data = load(VALID / "minimal-far-document.json")
        data["reasoning_steps"][0]["premises"] = [{"identifier": "DOES-NOT-EXIST", "expected_kind": "assumption"}]
        doc, diagnostics = ExternalFARDocument.from_mapping(data)
        self.assertEqual(diagnostics, ())
        _, ir_diagnostics = doc.to_ir()
        self.assertEqual(ir_diagnostics, ())

    def test_canonical_ir_remains_serialization_independent(self):
        claim = Claim(Identifier("C-native"), statement="Native", metadata={"not_json_specific": ("tuple",)})
        self.assertEqual(claim.metadata["not_json_specific"], ("tuple",))
        self.assertEqual(claim.validate(), ())

    def test_extensions_preserved_on_external_models(self):
        doc, diagnostics = ExternalFARDocument.from_mapping(load(VALID / "all-core-objects.json"))
        self.assertEqual(diagnostics, ())
        self.assertEqual(doc.extensions["far.example"]["note"], "namespaced extension")
        with self.assertRaises(TypeError):
            doc.extensions["new"] = True


if __name__ == "__main__":
    unittest.main()
