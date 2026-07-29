#!/usr/bin/env python3
"""Fail-closed validator for the canonical FARA v1.0 formal kernel."""
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

FORBIDDEN_CLAIMS = (
    "universality",
    "globally unique",
    "global necessity",
    "global minimality",
    "completeness proved",
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
            "# Generated FARA Canonical Kernel Report",
            "",
            "Status: **Accepted for Project FAR v1.0**",
            "",
            f"Campaign: `{proof['campaign_id']}`",
            f"Kernel: `{proof['kernel_version']}`",
            "",
            "## Adjudication",
            "",
            "| Candidate | Classification | Failed canonical gates |",
            "|---|---|---|",
            *rows,
            "",
            "## Executable translation evidence",
            "",
            f"- Typed-hypergraph exact round trip: `{proof['hypergraph_translation']['roundtrip_exact']}`.",
            f"- Algebraic/state-transition exact round trip with explicit sidecar: `{proof['algebraic_translation']['roundtrip_exact_with_sidecar']}`.",
            f"- Algebraic/state-transition standalone completeness: `{proof['algebraic_translation']['standalone_complete']}`.",
            f"- Extensional relation-occurrence identity loss detected: `{proof['counterexamples']['extensional_relation_identity_loss']['loss_detected']}`.",
            "",
            "## Canonical decision",
            "",
            spec["conclusion"],
            "",
            "## Historical evidence policy",
            "",
            "The earlier Pareto comparison remains valid for its three frozen implementations. This decision does not rewrite that result; it applies FARA's mandatory architectural gates to select the Project FAR v1.0 kernel after repairing occurrence identity.",
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
    if spec.get("mandatory_gates") != list(kernel.MANDATORY_GATES):
        errors.append("mandatory gate registry mismatch")
    if spec.get("selected_foundation") != "identity-bearing-many-sorted-relational":
        errors.append("unexpected canonical foundation")
    if len({candidate.get("id") for candidate in spec.get("candidates", [])}) != 4:
        errors.append("missing or duplicate candidate")
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
    canonical = [
        row
        for row in fresh["candidate_adjudication"]
        if row["classification"] == "canonical-candidate"
    ]
    if [row["id"] for row in canonical] != [spec["selected_foundation"]]:
        errors.append("canonical gate adjudication is not unique")
    if not fresh["sample_model_valid"]:
        errors.append("canonical sample invalid")
    if not fresh["hypergraph_translation"]["roundtrip_exact"]:
        errors.append("hypergraph round trip failed")
    if not fresh["algebraic_translation"]["roundtrip_exact_with_sidecar"]:
        errors.append("algebraic sidecar round trip failed")
    if fresh["algebraic_translation"]["standalone_complete"]:
        errors.append("bare algebraic view promoted to complete")
    if not fresh["counterexamples"]["extensional_relation_identity_loss"][
        "loss_detected"
    ]:
        errors.append("parallel occurrence identity loss not detected")
    if any(
        forbidden in spec["conclusion"].lower() for forbidden in FORBIDDEN_CLAIMS
    ):
        errors.append("overclaimed conclusion")
    if "multiple foundations remain Pareto-incomparable" not in json.dumps(
        spec["historical_result_policy"]
    ) and "Pareto" not in json.dumps(spec["historical_result_policy"]):
        errors.append("historical comparison not preserved")
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
        print("wrote canonical FARA kernel proof and report")
        return
    proof = json.loads(PROOF.read_text())
    errors = validate(spec, proof, REPORT.read_text())
    if errors:
        print("FAIL: " + "; ".join(errors))
        raise SystemExit(1)
    print(
        "PASS: canonical kernel gates, identity-bearing model, derived views, "
        "counterexamples, and bounded nonclaims verified"
    )


if __name__ == "__main__":
    main()
