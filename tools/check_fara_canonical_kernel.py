#!/usr/bin/env python3
"""Fail-closed validator for the provisional FARA kernel Research campaign."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from theory.foundation.fara_canonical_kernel import kernel

SPEC = ROOT / "theory/formal/fara-canonical-kernel-v1.0.json"
PROOF = ROOT / "theory/evaluation/fara-canonical-kernel-proof-v1.0.json"
REPORT = ROOT / "theory/evaluation/generated-fara-canonical-kernel-report.md"

FORBIDDEN_PROMOTIONS = (
    "status: **accepted",
    "is canonical for project far v1.0",
    "uq-t11 is resolved",
)


def render(spec, proof):
    rows = []
    for candidate in proof["candidate_adjudication"]:
        rows.append(
            "| {id} | {classification} | {failed} |".format(
                id=candidate["id"],
                classification=candidate["classification"],
                failed=", ".join(candidate["failed_gates"]) or "none",
            )
        )
    return "\n".join(
        [
            "# Generated FARA Kernel Research Report",
            "",
            "Status: **Research**",
            "",
            f"Campaign: `{proof['campaign_id']}`",
            f"Kernel candidate: `{proof['kernel_version']}`",
            "",
            "## Lifecycle",
            "",
            *[f"- {stage}: `{status}`" for stage, status in proof["lifecycle"].items()],
            "",
            "## Executable adjudication",
            "",
            "| Candidate | Classification | Failed frozen gates |",
            "|---|---|---|",
            *rows,
            "",
            "Every gate result is derived by executable predicates in the kernel implementation. The specification contains no candidate-authored gate booleans.",
            "",
            "## Translation and counterexample evidence",
            "",
            f"- Typed-hypergraph exact round trip: `{proof['hypergraph_translation']['roundtrip_exact']}`.",
            f"- Algebraic/state-transition exact round trip with explicit sidecar: `{proof['algebraic_translation']['roundtrip_exact_with_sidecar']}`.",
            f"- Bare algebraic reconstruction rejected: `{proof['algebraic_translation']['bare_reconstruction_rejected']}`.",
            f"- Extensional relation-occurrence identity loss detected: `{proof['counterexamples']['extensional_relation_identity_loss']['loss_detected']}`.",
            "",
            "## Provisional finding",
            "",
            spec["finding"],
            "",
            "## Historical evidence policy",
            "",
            "The earlier Pareto comparison and expanded bounded campaign remain immutable historical Research evidence. This campaign evaluates a repaired fourth candidate and does not rewrite those results.",
            "",
            "## Nonclaims",
            "",
            *[f"- {claim}" for claim in spec["nonclaims"]],
            "",
        ]
    )


def git_blob_sha(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def validate_historical(spec, root=ROOT):
    errors = []
    for relative, record in spec.get("historical_artifacts", {}).items():
        path = root / relative
        if not path.exists():
            errors.append(f"missing historical artifact: {relative}")
            continue
        if git_blob_sha(path.read_bytes()) != record.get("git_blob_sha"):
            errors.append(f"historical artifact changed: {relative}")
    return errors


def validate(spec, stored, report=None, check_historical=True, root=ROOT):
    errors = []
    if spec.get("status") != "Research":
        errors.append("research artifact promoted without lifecycle completion")
    if spec.get("mandatory_gates") != list(kernel.MANDATORY_GATES):
        errors.append("mandatory gate registry mismatch")
    if spec.get("proposed_foundation") != "identity-bearing-many-sorted-relational":
        errors.append("unexpected provisional foundation")
    if any("gates" in candidate for candidate in spec.get("candidates", [])):
        errors.append("candidate-authored gate booleans")
    lifecycle = spec.get("lifecycle", {})
    if lifecycle.get("replication") != "pending independent implementation":
        errors.append("replication status drift")
    if lifecycle.get("acceptance") != "pending" or lifecycle.get("promotion") != "pending":
        errors.append("premature acceptance or promotion")
    if len({candidate.get("id") for candidate in spec.get("candidates", [])}) != 4:
        errors.append("missing or duplicate candidate")
    if "candidate-authored gate booleans" in errors:
        return sorted(set(errors))
    try:
        fresh = kernel.build_proof(copy.deepcopy(spec))
    except Exception as exc:
        return [f"fresh build failed: {exc}"]
    if stored != fresh:
        errors.append("stale proof object")
    if check_historical:
        errors.extend(validate_historical(spec, root=root))
    if report is not None and report != render(spec, fresh):
        errors.append("stale generated report")
    provisional = [
        row
        for row in fresh["candidate_adjudication"]
        if row["classification"] == "provisional-canonical-candidate"
    ]
    if [row["id"] for row in provisional] != [spec["proposed_foundation"]]:
        errors.append("provisional gate adjudication is not unique")
    for row in fresh["candidate_adjudication"]:
        if set(row["gate_evidence"]) != set(kernel.MANDATORY_GATES):
            errors.append(f"incomplete gate evidence: {row['id']}")
        if any(
            evidence.get("pass") not in (True, False)
            or not evidence.get("evidence")
            for evidence in row["gate_evidence"].values()
        ):
            errors.append(f"non-executable gate evidence: {row['id']}")
    if not fresh["sample_model_valid"]:
        errors.append("research sample invalid")
    if not fresh["hypergraph_translation"]["roundtrip_exact"]:
        errors.append("hypergraph round trip failed")
    if not fresh["algebraic_translation"]["roundtrip_exact_with_sidecar"]:
        errors.append("algebraic sidecar round trip failed")
    if not fresh["algebraic_translation"]["bare_reconstruction_rejected"]:
        errors.append("bare algebraic reconstruction unexpectedly accepted")
    if fresh["algebraic_translation"]["standalone_complete"]:
        errors.append("bare algebraic view promoted to complete")
    if not fresh["counterexamples"]["extensional_relation_identity_loss"][
        "loss_detected"
    ]:
        errors.append("parallel occurrence identity loss not detected")
    serialized = (report or "").lower() + json.dumps(spec).lower()
    if any(claim in serialized for claim in FORBIDDEN_PROMOTIONS):
        errors.append("research artifact masquerades as accepted theory")
    return sorted(set(errors))


def write_all(spec):
    proof = kernel.build_proof(copy.deepcopy(spec))
    PROOF.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n")
    REPORT.write_text(render(spec, proof))
    return proof


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    spec = json.loads(SPEC.read_text())
    if args.write:
        write_all(spec)
        print("wrote provisional FARA kernel Research proof and report")
        return
    proof = json.loads(PROOF.read_text())
    errors = validate(spec, proof, REPORT.read_text())
    if errors:
        print("FAIL: " + "; ".join(errors))
        raise SystemExit(1)
    print(
        "PASS: executable gate derivation, event completeness, translations, "
        "counterexamples, historical immutability, and lifecycle status verified"
    )


if __name__ == "__main__":
    main()
