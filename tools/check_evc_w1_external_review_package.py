#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "theory/evaluation/evc-w1-external-proof-review-protocol-v1.0.json"
MANIFEST = ROOT / "theory/evaluation/evc-w1-external-review-package-manifest-v1.0.json"
TEMPLATE = ROOT / "theory/evaluation/evc-w1-external-review-result-template-v1.0.json"
GUIDE = ROOT / "docs/research/evc-w1-external-reviewer-guide-v1.0.md"
AUDIT = ROOT / "docs/audits/evc-w1-external-review-package-audit.md"
PARENT = ROOT / "theory/evaluation/post-w5-usd-next-program-v1.0.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for path in (PROTOCOL, MANIFEST, TEMPLATE, GUIDE, AUDIT, PARENT):
        assert path.is_file(), path

    protocol, manifest, template, parent = map(load, (PROTOCOL, MANIFEST, TEMPLATE, PARENT))
    guide = GUIDE.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    assert parent["program_id"] == "POST-USD-EVC-001"
    assert protocol["protocol_id"] == "EVC-W1-EXTERNAL-PROOF-REVIEW-001"
    assert protocol["status"] == "frozen_unexecuted"
    assert protocol["parent_program"] == parent["program_id"]
    assert protocol["workstream"] == "EVC-W1-EXTERNAL-PROOF-REVIEW"
    assert len(protocol["mandatory_review_questions"]) == 10
    assert set(protocol["required_outputs"]["verdict"]) == {
        "confirmed", "confirmed_with_nonblocking_qualifications", "blocking_objection", "unresolved"
    }
    assert protocol["freeze_and_access"]["post_access_rule"].startswith("no reviewed artifact may be repaired")
    assert protocol["author_response_boundary"]["initial_verdict_before_response"] is True
    assert protocol["claim_effect"] == {
        "protocol_frozen": True,
        "external_review_completed": False,
        "independent_verification_established": False,
        "universal_structure_established": False,
    }

    assert manifest["manifest_id"] == "EVC-W1-REVIEW-PACKAGE-001"
    assert manifest["status"] == "frozen_unreleased"
    assert manifest["protocol"] == protocol["protocol_id"]
    release = manifest["release_state"]
    assert release["reviewer_accessed"] is False
    assert release["release_commit"] is None
    assert release["external_review_started"] is False
    assert release["external_review_completed"] is False
    prohibited = set(manifest["prohibited_omissions"])
    assert "failed or scope-limiting controls" in prohibited
    assert "unresolved theorem gates" in prohibited
    assert "internal-only independence classification" in prohibited

    assert template["result_template_id"] == "EVC-W1-REVIEW-RESULT-TEMPLATE-001"
    assert template["protocol"] == protocol["protocol_id"]
    assert template["package_manifest"] == manifest["manifest_id"]
    assert len(template["obligation_matrix"]) == 10
    assert {item["id"] for item in template["obligation_matrix"]} == {f"W1-Q{i:02d}" for i in range(1, 11)}
    assert template["initial_verdict"] is None
    assert template["reviewer_declaration"]["substantive_author_contact_before_initial_verdict"] is False
    assert set(template["allowed_verdicts"]) == set(protocol["required_outputs"]["verdict"])

    assert "does not ask the reviewer to endorse Project FAR" in guide
    assert "initial report must be preserved before author response" in guide
    assert "External validation occurs only after an eligible reviewer" in guide
    assert "This is an internal package-design audit" in audit
    assert "No eligible reviewer has been recruited" in audit
    assert "frozen_unexecuted" in audit

    print("EVC-W1 external review package: PASS (frozen and procedurally ready; external review not executed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
