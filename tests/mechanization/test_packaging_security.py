from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

from mechanization.far_mechanization import __version__
from mechanization.far_mechanization.cli import CLI_VERSION
from mechanization.far_mechanization.external_models import FORMAT_VERSION
from mechanization.far_mechanization.parser import _load_schema, parse_yaml_text
from mechanization.far_mechanization.serialization import serialize_yaml
from mechanization.far_mechanization.parser import parse_file
from mechanization.far_mechanization.graph_engine import build_graph

ROOT = Path(__file__).resolve().parents[2]


def test_package_import_and_version_consistency():
    assert __version__ == "0.6.0"
    assert CLI_VERSION == "0.6.0"
    assert FORMAT_VERSION == "far-ir/1.0"
    completed = subprocess.run([sys.executable, "-c", "import mechanization.far_mechanization as m; print(m.__version__)"], cwd=ROOT, text=True, capture_output=True, check=False)
    assert completed.returncode == 0
    assert completed.stdout.strip() == __version__


def test_cli_entrypoint_smoke_version_and_help():
    for args in ([str(ROOT / "far"), "version"], [str(ROOT / "far"), "help"]):
        completed = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
        assert completed.returncode == 0
        assert completed.stdout


def test_safe_yaml_and_no_python_object_construction():
    malicious = "!!python/object/apply:os.system ['echo unsafe']\n"
    result = parse_yaml_text(malicious, "malicious.yaml")
    assert not result.success
    assert result.diagnostics[0].code.value == "FAR-PARSE-004"
    valid = parse_file(ROOT / "conformance" / "far-ir-1.0" / "valid" / "minimal.json")
    dumped = serialize_yaml(valid.document).text
    assert "!!python" not in dumped
    assert yaml.safe_load(dumped)["format_version"] == "far-ir/1.0"


def test_schema_references_are_local_only_for_mvp():
    schema = _load_schema()
    refs = []
    def walk(value):
        if isinstance(value, dict):
            if "$ref" in value:
                refs.append(value["$ref"])
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(schema)
    assert refs
    assert all(ref.startswith("#/") for ref in refs)


def test_graph_export_is_json_serializable_without_content_execution():
    valid = parse_file(ROOT / "conformance" / "far-ir-1.0" / "valid" / "complete.json")
    graph = build_graph(valid.document).graph
    payload = {"nodes": [str(n.identifier) for n in graph.nodes], "edges": [str(e.identifier) for e in graph.edges]}
    assert json.loads(json.dumps(payload, sort_keys=True))["nodes"]
