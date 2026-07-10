from __future__ import annotations

import json
import subprocess
from pathlib import Path

from mechanization.far_mechanization.graph_engine import build_graph, validate_dependencies, validate_graph
from mechanization.far_mechanization.parser import parse_file, parse_json_text, parse_yaml_text
from mechanization.far_mechanization.serialization import serialize_json, serialize_yaml

ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT / "conformance" / "far-ir-1.0"


def test_json_complete_end_to_end_pipeline():
    parsed = parse_file(SUITE / "valid" / "complete.json")
    assert parsed.success
    graph = build_graph(parsed.document).graph
    assert graph is not None
    assert validate_graph(graph, parsed.document).diagnostics == ()
    assert validate_dependencies(parsed.document, graph) == ()
    exported = serialize_json(parsed.document)
    assert exported.success
    assert parse_json_text(exported.text, "<json-export>").document == parsed.document


def test_yaml_complete_end_to_end_pipeline():
    parsed = parse_file(SUITE / "valid" / "complete.yaml")
    assert parsed.success
    graph = build_graph(parsed.document).graph
    assert graph is not None
    assert validate_graph(graph, parsed.document).diagnostics == ()
    exported = serialize_yaml(parsed.document)
    assert exported.success
    assert parse_yaml_text(exported.text, "<yaml-export>").document == parsed.document


def test_invalid_document_cli_json_diagnostics_nonzero():
    completed = subprocess.run([str(ROOT / "far"), "validate", "--output", "json", str(SUITE / "invalid" / "invalid-identifier.json")], cwd=ROOT, text=True, capture_output=True, check=False)
    assert completed.returncode != 0
    payload = json.loads(completed.stdout)
    assert payload["valid"] is False
    assert payload["diagnostics"][0]["code"] == "FAR-EXT-006"


def test_cross_format_round_trip_equality():
    parsed = parse_file(SUITE / "valid" / "complete.json")
    yaml_text = serialize_yaml(parsed.document).text
    reparsed = parse_yaml_text(yaml_text, "<cross-format>")
    assert reparsed.success
    assert reparsed.document == parsed.document


def test_cli_end_to_end_commands_on_real_fixture():
    fixture = SUITE / "valid" / "complete.json"
    for command in ("validate", "parse", "normalize", "graph", "stats", "diagnostics"):
        completed = subprocess.run([str(ROOT / "far"), command, str(fixture)], cwd=ROOT, text=True, capture_output=True, check=False)
        assert completed.returncode == 0, (command, completed.stdout, completed.stderr)
        assert completed.stdout
