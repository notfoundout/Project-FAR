from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable

from .trust import HMACTrust, TrustError, canonical_json, read_attestation, write_attestation

CERTIFICATE_KIND = "validation-certificate"
CERTIFICATE_SCHEMA = "project-far-validation-certificate-v1"


class CertificateError(ValueError):
    pass


def _result_digest(run_payload: dict[str, Any]) -> str:
    material = {
        "profile": run_payload.get("profile"),
        "selected_checks": run_payload.get("selected_checks", []),
        "results": run_payload.get("results", []),
        "manifest_hash": run_payload.get("manifest_hash"),
    }
    return hashlib.sha256(canonical_json(material)).hexdigest()


def certificate_payload(
    run_payload: dict[str, Any],
    *,
    event_name: str | None = None,
    repository: str | None = None,
) -> dict[str, Any]:
    return {
        "schema": CERTIFICATE_SCHEMA,
        "run_id": run_payload.get("run_id"),
        "profile": run_payload.get("profile"),
        "commit_sha": run_payload.get("commit_sha"),
        "tree_sha": run_payload.get("tree_sha"),
        "base_sha": run_payload.get("base_sha"),
        "manifest_hash": run_payload.get("manifest_hash"),
        "successful": bool(run_payload.get("successful")),
        "root_failures": list(run_payload.get("root_failures", [])),
        "selected_checks": list(run_payload.get("selected_checks", [])),
        "result_digest": _result_digest(run_payload),
        "assurance": dict(run_payload.get("assurance", {})),
        "event_name": event_name if event_name is not None else os.environ.get("GITHUB_EVENT_NAME", "local"),
        "repository": repository if repository is not None else os.environ.get("GITHUB_REPOSITORY", "local"),
        "workflow": os.environ.get("GITHUB_WORKFLOW", ""),
        "run_id_external": os.environ.get("GITHUB_RUN_ID", ""),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", ""),
    }


def write_certificate(path: Path, run_payload: dict[str, Any], *, trust: HMACTrust) -> dict[str, Any]:
    payload = certificate_payload(run_payload)
    write_attestation(
        path,
        trust=trust,
        kind=CERTIFICATE_KIND,
        payload=payload,
        metadata={"commit_sha": payload["commit_sha"], "tree_sha": payload["tree_sha"]},
    )
    return payload


def verify_certificate(
    path: Path,
    *,
    trust: HMACTrust,
    expected_commit: str,
    expected_tree: str,
    required_checks: Iterable[str] = (),
    required_evidence: Iterable[str] = (),
    allowed_events: Iterable[str] = ("pull_request", "merge_group", "push", "workflow_dispatch", "local"),
) -> dict[str, Any]:
    try:
        payload = read_attestation(path, trust=trust, kind=CERTIFICATE_KIND)
    except TrustError as exc:
        raise CertificateError(str(exc)) from exc
    if payload.get("schema") != CERTIFICATE_SCHEMA:
        raise CertificateError("unsupported certificate schema")
    if payload.get("commit_sha") != expected_commit:
        raise CertificateError("certificate commit does not match checked commit")
    if payload.get("tree_sha") != expected_tree:
        raise CertificateError("certificate tree does not match checked tree")
    if payload.get("event_name") not in set(allowed_events):
        raise CertificateError(f"certificate event is not authorized: {payload.get('event_name')}")
    if payload.get("successful") is not True or payload.get("root_failures"):
        raise CertificateError("certificate records a failed validation run")
    selected = set(payload.get("selected_checks", []))
    missing = sorted(set(required_checks) - selected)
    if missing:
        raise CertificateError(f"certificate omitted required checks: {missing}")
    assurance = payload.get("assurance", {})
    evidence = assurance.get("evidence", {}) if isinstance(assurance, dict) else {}
    missing_evidence = sorted(set(required_evidence) - set(evidence))
    if missing_evidence:
        raise CertificateError(f"certificate omitted required assurance evidence: {missing_evidence}")
    for evidence_id in required_evidence:
        item = evidence[evidence_id]
        if not isinstance(item, dict) or item.get("successful") is not True or not isinstance(item.get("sha256"), str):
            raise CertificateError(f"assurance evidence is not successful or attested: {evidence_id}")
    if not isinstance(payload.get("result_digest"), str) or len(payload["result_digest"]) != 64:
        raise CertificateError("certificate result digest is malformed")
    return payload


def main(argv: list[str] | None = None) -> int:
    import argparse
    import subprocess

    parser = argparse.ArgumentParser(description="Create or verify signed Project FAR validation certificates")
    parser.add_argument("action", choices=("create", "verify"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--run", type=Path, default=None)
    parser.add_argument("--certificate", type=Path, default=None)
    parser.add_argument("--expected-commit")
    parser.add_argument("--expected-tree")
    parser.add_argument("--require-signed", action="store_true")
    parser.add_argument("--required-check", action="append", default=[])
    parser.add_argument("--required-evidence", action="append", default=[])
    args = parser.parse_args(argv)
    root = args.root.resolve()
    run_path = args.run or root / ".far" / "runs" / "latest.json"
    certificate_path = args.certificate or root / ".far" / "artifacts" / "validation" / "certificate.json"
    try:
        trust = HMACTrust.from_environment(require_signature=args.require_signed)
        if args.action == "create":
            payload = json.loads(run_path.read_text(encoding="utf-8"))
            write_certificate(certificate_path, payload, trust=trust)
            print(f"signed validation certificate: {certificate_path}")
            return 0
        expected_commit = args.expected_commit or subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip()
        expected_tree = args.expected_tree or subprocess.check_output(
            ["git", "rev-parse", "HEAD^{tree}"], cwd=root, text=True
        ).strip()
        payload = verify_certificate(
            certificate_path,
            trust=trust,
            expected_commit=expected_commit,
            expected_tree=expected_tree,
            required_checks=args.required_check,
            required_evidence=args.required_evidence,
        )
        print(
            "validation certificate verified: "
            f"commit={payload['commit_sha']} tree={payload['tree_sha']} event={payload['event_name']}"
        )
        return 0
    except (OSError, json.JSONDecodeError, TrustError, CertificateError, subprocess.CalledProcessError) as exc:
        print(f"FAR-VAL-CERT-001: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
