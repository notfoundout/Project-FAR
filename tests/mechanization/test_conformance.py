from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mechanization.far_mechanization.conformance import MANIFEST_PATH, load_manifest, run_conformance, validate_manifest
from mechanization.far_mechanization.parser import parse_file
from mechanization.far_mechanization.serialization import serialize_json, serialize_yaml
from mechanization.far_mechanization.cli import _graph_data, _diagnostic_to_dict, _sort_diagnostics

ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT / "conformance" / "far-ir-1.0"


def test_conformance_manifest_is_valid_and_covers_mandatory_categories():
    manifest = load_manifest(MANIFEST_PATH)
    assert validate_manifest(manifest) == ()
    categories = {case["feature_category"] for case in manifest["cases"]}
    assert {"document-structure", "parsing", "references", "graph-construction", "dependencies", "normalization", "serialization", "cli"} <= categories
    assert len(manifest["cases"]) >= 50


def test_every_conformance_case_passes():
    result = run_conformance(MANIFEST_PATH)
    assert result.success
    assert result.total == 58
    assert result.passed == 58
    assert result.failed == 0


def test_conformance_runner_human_and_json_modes():
    human = subprocess.run([sys.executable, "-m", "mechanization.far_mechanization.conformance"], cwd=ROOT, text=True, capture_output=True, check=False)
    assert human.returncode == 0
    assert "58/58 passed" in human.stdout
    machine = subprocess.run([sys.executable, "-m", "mechanization.far_mechanization.conformance", "--output", "json"], cwd=ROOT, text=True, capture_output=True, check=False)
    assert machine.returncode == 0
    payload = json.loads(machine.stdout)
    assert payload["success"] is True
    assert payload["total"] == 58


def test_golden_outputs_match_current_pipeline():
    doc = parse_file(SUITE / "valid" / "complete.json").document
    assert serialize_json(doc).text == (SUITE / "expected" / "complete.normalized.json").read_text(encoding="utf-8")
    assert serialize_yaml(doc).text == (SUITE / "expected" / "complete.normalized.yaml").read_text(encoding="utf-8")
    graph_data, _ = _graph_data(doc)
    assert json.dumps(graph_data, indent=2, sort_keys=True) + "\n" == (SUITE / "expected" / "complete.graph.json").read_text(encoding="utf-8")
    invalid = parse_file(SUITE / "invalid" / "invalid-identifier.json")
    diagnostics = [_diagnostic_to_dict(d) for d in _sort_diagnostics(invalid.diagnostics)]
    assert json.dumps(diagnostics, indent=2, sort_keys=True) + "\n" == (SUITE / "expected" / "invalid-identifier.diagnostics.json").read_text(encoding="utf-8")


def test_cli_conformance_command():
    completed = subprocess.run([str(ROOT / "far"), "conformance", "--output", "json"], cwd=ROOT, text=True, capture_output=True, check=False)
    assert completed.returncode == 0
    assert json.loads(completed.stdout)["passed"] == 58
