import json
import tempfile
from pathlib import Path
import unittest
import yaml

from mechanization.far_mechanization import DiagnosticCode
from mechanization.far_mechanization.normalization import normalize_ir_document
from mechanization.far_mechanization.parser import parse_json_file, parse_json_text, parse_yaml_file, parse_yaml_text
from mechanization.far_mechanization.serialization import serialize_json, serialize_yaml, write_json_file, write_yaml_file

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_JSON = ROOT / "examples" / "mechanization" / "minimal-investigation.json"
EXAMPLE_YAML = ROOT / "examples" / "mechanization" / "minimal-investigation.yaml"
ALL = ROOT / "tests" / "fixtures" / "mechanization" / "valid" / "all-core-objects.json"

class SerializationTests(unittest.TestCase):
    def doc(self):
        result = parse_json_file(ALL)
        self.assertTrue(result.success, result.diagnostics)
        return result.document

    def test_normalization_idempotence_order_and_identifier_preservation(self):
        doc = self.doc()
        once = normalize_ir_document(doc)
        twice = normalize_ir_document(once.document.to_ir()[0])
        self.assertTrue(once.success)
        self.assertTrue(twice.success)
        self.assertEqual(once.document, twice.document)
        self.assertEqual([s.order for s in once.document.reasoning_steps], [1])
        self.assertEqual(once.document.claims[0].id, "C-all")

    def test_json_deterministic_output(self):
        doc = self.doc()
        a = serialize_json(doc)
        b = serialize_json(doc)
        self.assertTrue(a.success, a.diagnostics)
        self.assertEqual(a.text, b.text)
        self.assertTrue(a.text.endswith("\n"))
        self.assertIn("π", serialize_json(parse_json_file(ROOT / "tests" / "fixtures" / "mechanization" / "parser" / "valid" / "unicode.json").document).text)
        self.assertIsInstance(json.loads(a.text), dict)

    def test_yaml_deterministic_safe_output(self):
        doc = self.doc()
        a = serialize_yaml(doc)
        b = serialize_yaml(doc)
        self.assertTrue(a.success, a.diagnostics)
        self.assertEqual(a.text, b.text)
        self.assertNotIn("!!python", a.text)
        self.assertTrue(a.text.endswith("\n"))
        self.assertIsInstance(yaml.safe_load(a.text), dict)

    def test_cross_format_round_trips(self):
        json_ir = parse_json_text(EXAMPLE_JSON.read_text(), "example.json").document
        yaml_ir = parse_yaml_text(EXAMPLE_YAML.read_text(), "example.yaml").document
        self.assertEqual(json_ir, yaml_ir)
        jj = parse_json_text(serialize_json(json_ir).text, "jj.json")
        yy = parse_yaml_text(serialize_yaml(yaml_ir).text, "yy.yaml")
        jy = parse_yaml_text(serialize_yaml(json_ir).text, "jy.yaml")
        yj = parse_json_text(serialize_json(yaml_ir).text, "yj.json")
        for result in (jj, yy, jy, yj):
            self.assertTrue(result.success, result.diagnostics)
            self.assertEqual(result.document, json_ir)

    def test_file_round_trips(self):
        with tempfile.TemporaryDirectory() as tmp:
            doc = parse_json_file(EXAMPLE_JSON).document
            jp = Path(tmp) / "out.json"
            yp = Path(tmp) / "out.yaml"
            self.assertTrue(write_json_file(doc, jp).success)
            self.assertTrue(write_yaml_file(doc, yp).success)
            self.assertEqual(parse_json_file(jp).document, doc)
            self.assertEqual(parse_yaml_file(yp).document, doc)

    def test_write_errors_return_diagnostics(self):
        doc = self.doc()
        result = write_json_file(doc, Path("/no/such/directory/out.json"))
        self.assertFalse(result.success)
        self.assertEqual(result.diagnostics[0].code, DiagnosticCode.FILE_WRITE_ERROR)

if __name__ == "__main__":
    unittest.main()
