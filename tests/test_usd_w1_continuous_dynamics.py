from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "theory/evaluation/usd-w1-continuous-dynamics-scope-v1.0.json"
FIXTURES = ROOT / "theory/evaluation/usd-w1-continuous-dynamics-fixtures-v1.0.json"
RESULT = ROOT / "theory/evaluation/usd-w1-continuous-dynamics-extension-result-v1.0.json"
CHECKER = ROOT / "tools/check_usd_w1_continuous_dynamics.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_continuous_dynamics_checker_passes() -> None:
    completed = subprocess.run(
        [sys.executable, str(CHECKER)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "PASS" in completed.stdout


def test_scope_is_candidate_independent_and_bounded() -> None:
    scope = load(SCOPE)
    admission = scope["admission_rule"]
    assert admission["candidate_independent"] is True
    assert scope["source_class"] == "S_cd_lip_eff"
    assert "nonunique flows" in admission["exclusions"]
    assert "Zeno event accumulation" in admission["exclusions"]
    assert "actual-process correspondence" in admission["exclusions"]


def test_grid_and_oracle_controls_are_rejected() -> None:
    fixtures = {item["id"]: item for item in load(FIXTURES)["fixtures"]}
    result = load(RESULT)
    assert fixtures["CD-NEG-GRID-001"]["expected"] == "rejected"
    assert fixtures["CD-NEG-ORACLE-001"]["expected"] == "rejected"
    assert result["fixture_results"]["CD-NEG-GRID-001"] == "rejected"
    assert result["fixture_results"]["CD-NEG-ORACLE-001"] == "rejected"


def test_nonunique_and_zeno_cases_remain_scope_boundaries() -> None:
    result = load(RESULT)
    assert result["fixture_results"]["CD-BOUND-NONUNIQ-001"] == "excluded"
    assert result["fixture_results"]["CD-BOUND-ZENO-001"] == "excluded"
    assert result["terminal_outcome"] == "proper_subclass_only"


def test_broader_claims_remain_unresolved() -> None:
    result = load(RESULT)
    claims = result["claim_effect"]
    assert claims["all_continuous_dynamics_representation"] == "unresolved"
    assert claims["S_IRD_representation"] == "unresolved"
    assert claims["universal_structure"] == "unresolved"
    assert claims["primitive_necessity"] == "not_established"
    assert claims["minimality"] == "not_established"
    assert claims["uniqueness"] == "not_established"
    assert result["machine_check_status"] == "not_mechanized"
    assert result["independent_review_status"] == "not_started"
