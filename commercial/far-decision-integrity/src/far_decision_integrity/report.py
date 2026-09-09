from __future__ import annotations

import json
from pathlib import Path

from .adjudicate import Adjudication


def report_payload(result: Adjudication) -> dict:
    payload = {
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
    if result.semantic_audits:
        payload["semantic_audits"] = [
            {
                "binding_id": audit.binding_id,
                "target_node_id": audit.target_node_id,
                "purpose": audit.purpose,
                "selected_candidate_id": audit.selected_candidate_id,
                "document_id": audit.document_id,
                "contract_id": audit.contract_id,
                "format_version": audit.format_version,
                "outcome": audit.outcome,
                "disposition": audit.disposition.value,
                "verifier_success": audit.verifier_success,
                "diagnostics": [
                    {
                        "code": diagnostic.code,
                        "message": diagnostic.message,
                        "path": list(diagnostic.path),
                    }
                    for diagnostic in audit.diagnostics
                ],
                "verifier_artifacts": [
                    {
                        "role": artifact.role,
                        "path": artifact.path,
                        "sha256": artifact.sha256,
                    }
                    for artifact in audit.verifier_artifacts
                ],
            }
            for audit in result.semantic_audits
        ]
    return payload


def write_report(result: Adjudication, output: str | Path) -> Path:
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(report_payload(result), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return target
