import json
import tempfile
from pathlib import Path
import unittest
import yaml
import jsonschema

from mechanization.far_mechanization import DiagnosticCode
from mechanization.far_mechanization.parser import (
    detect_format, parse_document, parse_file, parse_json_file, parse_json_text,
    parse_yaml_file, parse_yaml_text,
)

ROOT = Path(__file__).resolve().parents[2]
VALID = ROOT / "tests" / "fixtures" / "mechanization" / "parser" / "valid"
INVALID = ROOT / "tests" / "fixtures" / "mechanization" / "parser" / "invalid"
EXAMPLE_JSON = ROOT / "examples" / "mechanization" / "minimal-investigation.json"
EXAMPLE_YAML = ROOT / "examples" / "mechanization" / "minimal-investigation.yaml"

class ParserTests(unittest.TestCase):
    def test_declared_schema_dependency_imports(self):
        self.assertEqual(jsonschema.__version__, "4.22.0")

    def test_json_text_and_yaml_text_parse_to_equal_ir(self):
        j = parse_json_text(EXAMPLE_JSON.read_text(), "example.json")
        y = parse_yaml_text(EXAMPLE_YAML.read_text(), "example.yaml")
        self.assertTrue(j.success, j.diagnostics)
        self.assertTrue(y.success, y.diagnostics)
        self.assertEqual(j.document, y.document)
        self.assertEqual(j.format_version, "far-ir/1.0")

    def test_json_file_and_yaml_file_parse(self):
        self.assertTrue(parse_json_file(EXAMPLE_JSON).success)
        result = parse_yaml_file(EXAMPLE_YAML)
        self.assertTrue(result.success, result.diagnostics)
        self.assertEqual(result.source, str(EXAMPLE_YAML))

    def test_explicit_format_overrides_extension(self):
        result = parse_document(EXAMPLE_JSON.read_text(), "misleading.yaml", explicit_format="json")
        self.assertTrue(result.success, result.diagnostics)
        self.assertEqual(result.detected_format, "json")

    def test_extension_detection_and_unknown_extension(self):
        self.assertEqual(detect_format("x.json")[0], "json")
        self.assertEqual(detect_format("x.yaml")[0], "yaml")
        fmt, diagnostics = detect_format("x.unknown")
        self.assertIsNone(fmt)
        self.assertEqual(diagnostics[0].code, DiagnosticCode.UNKNOWN_FILE_EXTENSION)

    def test_malformed_json_and_yaml_diagnostics_include_location(self):
        j = parse_json_text((INVALID / "malformed.json").read_text(), "bad.json")
        self.assertEqual(j.diagnostics[0].code, DiagnosticCode.MALFORMED_JSON)
        self.assertIsNotNone(j.diagnostics[0].source.line)
        y = parse_yaml_text((INVALID / "malformed.yaml").read_text(), "bad.yaml")
        self.assertEqual(y.diagnostics[0].code, DiagnosticCode.MALFORMED_YAML)
        self.assertIsNotNone(y.diagnostics[0].source.line)

    def test_non_object_roots(self):
        self.assertEqual(parse_json_text((INVALID / "root-scalar.json").read_text()).diagnostics[0].code, DiagnosticCode.NON_OBJECT_ROOT)
        self.assertEqual(parse_yaml_text((INVALID / "root-sequence.yaml").read_text()).diagnostics[0].code, DiagnosticCode.NON_OBJECT_ROOT)

    def test_actual_jsonschema_enforcement(self):
        result = parse_yaml_text((INVALID / "schema-invalid.yaml").read_text(), "schema-invalid.yaml")
        self.assertFalse(result.success)
        self.assertEqual(result.diagnostics[0].code, DiagnosticCode.SCHEMA_CONSTRAINT_VIOLATION)
        self.assertIn("path", result.diagnostics[0].details)

    def test_unsupported_format_version_schema_diagnostic(self):
        result = parse_yaml_text((INVALID / "unsupported-version.yaml").read_text(), "bad-version.yaml")
        self.assertFalse(result.success)
        self.assertEqual(result.diagnostics[0].code, DiagnosticCode.SCHEMA_CONSTRAINT_VIOLATION)

    def test_local_ir_validation_executes_after_schema(self):
        data = json.loads(EXAMPLE_JSON.read_text())
        data["claims"].append({"id":"C-min", "kind":"claim", "statement":"duplicate"})
        result = parse_json_text(json.dumps(data), "duplicate.json")
        self.assertFalse(result.success)
        self.assertTrue(any(d.code == DiagnosticCode.DUPLICATE_LOCAL_IDENTIFIER for d in result.diagnostics))

    def test_file_io_errors_return_diagnostics(self):
        result = parse_file(ROOT / "missing-file.far.json")
        self.assertFalse(result.success)
        self.assertEqual(result.diagnostics[0].code, DiagnosticCode.UNREADABLE_FILE)

    def test_ambiguous_detection(self):
        fmt, diagnostics = detect_format(text="not clearly either")
        self.assertIsNone(fmt)
        self.assertEqual(diagnostics[0].code, DiagnosticCode.AMBIGUOUS_FORMAT_DETECTION)

if __name__ == "__main__":
    unittest.main()
