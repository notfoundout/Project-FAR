#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROTOCOL = ROOT / "theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json"
CORPUS = ROOT / "theory/evaluation/evc-w3-r4-adversarial-challenge-corpus-v1.0.json"
MANIFEST = ROOT / "theory/evaluation/evc-w3-r4-adversarial-package-manifest-v1.0.json"
TEMPLATE = ROOT / "theory/evaluation/evc-w3-r4-adversarial-result-template-v1.0.json"
GUIDE = ROOT / "docs/research/evc-w3-r4-adversarial-team-guide-v1.0.md"
AUDIT = ROOT / "docs/audits/evc-w3-r4-adversarial-package-audit.md"
PARENT = ROOT / "theory/evaluation/post-w5-usd-next-program-v1.0.json"


def load(path: Path):
    assert path.exists(), f"missing required artifact: {path.relative_to(ROOT)}"
    return json.loads(path.read_text())


def main() -> None:
    protocol = load(PROTOCOL)
    corpus = load(CORPUS)
    manifest = load(MANIFEST)
    template = load(TEMPLATE)
    parent = load(PARENT)
    guide = GUIDE.read_text()
    audit = AUDIT.read_text()

    assert protocol["protocol_id"] == "EVC-W3-R4-ADVERSARIAL-REPLICATION-001"
    assert protocol["status"] == "frozen_unexecuted"
    assert protocol["parent_program"] == "POST-USD-EVC-001"
    assert set(protocol["terminal_outcomes"]) == {"survived", "scope_limited", "refuted", "unresolved"}
    assert len(protocol["mandatory_attack_domains"]) == 10
    assert "weakest_gate" in protocol["decision_rules"]

    workstreams = {w["id"] for w in parent["workstreams"]}
    assert "EVC-W3-R4-ADVERSARIAL-REPLICATION" in workstreams

    challenges = corpus["challenges"]
    assert len(challenges) == 12
    challenge_ids = [c["id"] for c in challenges]
    assert len(set(challenge_ids)) == 12
    assert challenge_ids[0] == "R4-C01-SCOPE-LEAK"
    assert challenge_ids[-1] == "R4-C12-ACTUAL-PROCESS-CONFLATION"

    groups = {g["group"]: g for g in manifest["required_artifact_groups"]}
    program_artifacts = groups["program_and_terminal_synthesis"]["artifacts"]
    instruments = groups["adversarial_instruments"]["artifacts"]
    assert "theory/evaluation/post-w5-usd-next-program-v1.0.json" in program_artifacts
    assert "theory/evaluation/evc-w3-r4-adversarial-challenge-corpus-v1.0.json" in instruments
    assert manifest["status"] == "frozen_unreleased"
    assert all(value in (False, None) for value in manifest["release_state"].values())

    template_ids = [item["challenge_id"] for item in template["challenge_results"]]
    assert template_ids == challenge_ids
    assert set(template["allowed_verdicts"]) == set(protocol["terminal_outcomes"])
    assert template["initial_verdict"] is None and template["final_verdict"] is None

    assert "No adversarial team has been recruited" in audit
    assert "Failure to find an attack does not establish universality" in guide
    for text in (guide, audit):
        lowered = text.lower()
        assert "universal" in lowered
        assert "actual-process" in lowered
        assert "r4" in lowered

    print("EVC-W3 R4 adversarial replication package: PASS")


if __name__ == "__main__":
    main()
