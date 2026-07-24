from __future__ import annotations

import json
from pathlib import Path

from .adjudicate import Adjudication


def report_payload(result: Adjudication) -> dict:
    return {
        "decision_id": result.decision_id,
        "status": result.status.value,
        "findings": [
            {
                "rule_id": finding.rule_id,
                "severity": finding.severity,
                "message": finding.message,
                "node_id": finding.node_id,
            }
            for finding in result.findings
        ],
    }


def write_report(result: Adjudication, output: str | Path) -> Path:
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(report_payload(result), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return target
