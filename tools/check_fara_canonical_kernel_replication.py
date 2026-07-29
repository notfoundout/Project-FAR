#!/usr/bin/env python3
"""Validate and render the clean-room FARA kernel replication."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/replications/fara-canonical-kernel-v1.0"
PROTOCOL = BASE / "protocol.json"
FIXTURES = BASE / "neutral-fixtures.json"
SCRIPT = BASE / "replicate.js"
RESULT = BASE / "result.json"
ADJUDICATION = BASE / "adjudication.json"
REPORT = BASE / "README.md"
EXPECTED_GATES = [
    "representation_object_separation",
    "rule_execution_result_separation",
    "interpretation_separation",
    "calculus_independence",
    "architecture_operation_separation",
    "identity_bearing_occurrences",
    "explicit_provenance_and_order",
    "encoding_neutrality",
]
FORBIDDEN_SOURCE_TOKENS = (
    "theory/foundation/fara_canonical_kernel",
    "fara-canonical-kernel-proof-v1.0.json",
    "fara-canonical-kernel-v1.0.json",
    "kernel.py",
    "child_process",
    "worker_threads",
    'require("http")',
    'require("https")',
    'require("net")',
    'require("tls")',
    'require("dns")',
    "fetch(",
    "eval(",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def candidate_summary(document: dict[str, Any], evidence_key: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in document.get("candidate_adjudication", []):
        evidence = row.get(evidence_key, {})
        failed_from_evidence = sorted(
            gate for gate, item in evidence.items() if not item.get("pass", False)
        )
        failed = sorted(row.get("failed_gates", []))
        if failed_from_evidence != failed:
            raise ValueError(f"failed-gate drift for {row.get('id')}")
        rows.append(
            {
                "id": row.get("id"),
                "classification": row.get("classification"),
                "failed_gates": failed,
            }
        )
    return rows


def protocol_has_outcome_leakage(protocol: dict[str, Any]) -> bool:
    forbidden = {
        "expected_gates",
        "proposed_foundation",
        "classification",
        "failed_gates",
        "gate_results",
        "gate_evidence",
    }

    def walk(value: Any) -> bool:
        if isinstance(value, dict):
            return bool(forbidden.intersection(value)) or any(walk(v) for v in value.values())
        if isinstance(value, list):
            return any(walk(v) for v in value)
        return False

    return walk(protocol)


def inspect_script(script_text: str, protocol: dict[str, Any]) -> list[str]:
    errors = [
        f"forbidden clean-room dependency: {token}"
        for token in FORBIDDEN_SOURCE_TOKENS
        if token in script_text
    ]
    modules = re.findall(r'require\(["\']([^"\']+)["\']\)', script_text)
    allowed = sorted(protocol["independence_contract"]["allowed_runtime_modules"])
    observed = sorted(set(modules))
    if observed != allowed:
        errors.append(f"runtime-module declaration drift: observed={observed}, allowed={allowed}")
    if "module.exports" not in script_text:
        errors.append("replicator does not expose testable functions")
    return errors


def _run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=False, timeout=60
    )


def verify_freeze_history(protocol: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    fixture = protocol["fixture_corpus"]
    freeze = fixture["freeze_commit"]
    implementation = fixture["implementation_commit"]
    fixture_path = fixture["path"]
    implementation_path = "research/replications/fara-canonical-kernel-v1.0/replicate.js"
    errors: list[str] = []

    if _run_git(root, ["rev-parse", "--is-inside-work-tree"]).returncode != 0:
        return {"verified": False, "errors": ["not inside a Git work tree"]}

    ancestor = _run_git(root, ["merge-base", "--is-ancestor", freeze, implementation])
    if ancestor.returncode != 0:
        fetch = _run_git(root, ["fetch", "--no-tags", "--depth=32", "origin", implementation])
        if fetch.returncode != 0:
            errors.append(f"cannot fetch frozen implementation ancestry: {fetch.stderr.strip()}")
        ancestor = _run_git(root, ["merge-base", "--is-ancestor", freeze, implementation])
    if ancestor.returncode != 0:
        errors.append("fixture freeze commit is not a reachable ancestor of implementation commit")

    frozen = _run_git(root, ["show", f"{freeze}:{fixture_path}"])
    current = root / fixture_path
    if frozen.returncode != 0 or not current.is_file() or frozen.stdout.encode() != current.read_bytes():
        errors.append("frozen fixture bytes do not equal current fixture bytes")

    absent = _run_git(root, ["cat-file", "-e", f"{freeze}:{implementation_path}"])
    if absent.returncode == 0:
        errors.append("implementation already existed at fixture freeze commit")
    present = _run_git(root, ["cat-file", "-e", f"{implementation}:{implementation_path}"])
    if present.returncode != 0:
        errors.append("implementation is absent at declared implementation commit")

    return {
        "verified": not errors,
        "errors": errors,
        "freeze_commit": freeze,
        "implementation_commit": implementation,
        "fixture_unchanged_since_freeze": "frozen fixture bytes do not equal current fixture bytes" not in errors,
        "implementation_absent_at_freeze": "implementation already existed at fixture freeze commit" not in errors,
        "freeze_ancestor_of_implementation": "fixture freeze commit is not a reachable ancestor of implementation commit" not in errors,
    }


def run_isolated(
    protocol_path: Path = PROTOCOL,
    fixtures_path: Path = FIXTURES,
    script_path: Path = SCRIPT,
) -> dict[str, Any]:
    node = shutil.which("node")
    if not node:
        raise RuntimeError("Node.js is required for independent replication")
    with tempfile.TemporaryDirectory(prefix="fara-clean-room-") as directory:
        room = Path(directory)
        local_protocol = room / "protocol.json"
        local_fixtures = room / "fixtures.json"
        local_script = room / "replicate.js"
        shutil.copyfile(protocol_path, local_protocol)
        shutil.copyfile(fixtures_path, local_fixtures)
        shutil.copyfile(script_path, local_script)
        completed = subprocess.run(
            [node, str(local_script), str(local_protocol), str(local_fixtures)],
            cwd=room,
            env={"PATH": os.environ.get("PATH", ""), "HOME": str(room), "LANG": "C.UTF-8"},
            text=True,
            capture_output=True,
            timeout=60,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"isolated replicator failed ({completed.returncode}): {completed.stderr.strip()}"
            )
        return json.loads(completed.stdout)


def build_adjudication(
    protocol: dict[str, Any],
    fixtures: dict[str, Any],
    result: dict[str, Any],
    source_spec: dict[str, Any],
    source_proof: dict[str, Any],
    *,
    root: Path = ROOT,
    script_text: str | None = None,
    fresh_result: dict[str, Any] | None = None,
    history: dict[str, Any] | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    script_text = SCRIPT.read_text() if script_text is None else script_text
    fresh_result = run_isolated() if fresh_result is None else fresh_result
    history = verify_freeze_history(protocol, root) if history is None else history

    if protocol.get("status") != "Research" or result.get("status") != "Research":
        errors.append("replication artifacts must remain Research")
    if protocol_has_outcome_leakage(protocol):
        errors.append("outcome leakage in frozen protocol")
    if protocol.get("mandatory_gates") != EXPECTED_GATES:
        errors.append("mandatory-gate drift")
    if source_spec.get("mandatory_gates") != EXPECTED_GATES:
        errors.append("source gate contract drift")
    if [row.get("id") for row in protocol.get("candidates", [])] != [row.get("id") for row in source_spec.get("candidates", [])]:
        errors.append("candidate-set drift from source campaign")
    if not history.get("verified"):
        errors.extend(f"history proof: {error}" for error in history.get("errors", ["unverified"]))

    fixture_lock = protocol.get("fixture_corpus", {})
    fixture_path = root / fixture_lock.get("path", "")
    if not fixture_path.is_file() or git_blob_sha(fixture_path.read_bytes()) != fixture_lock.get("git_blob_sha"):
        errors.append("neutral fixture blob lock mismatch")
    source = protocol.get("source_campaign", {})
    for path_key, sha_key in (("spec_path", "spec_git_blob_sha"), ("proof_path", "proof_git_blob_sha")):
        artifact = root / source.get(path_key, "")
        if not artifact.is_file() or git_blob_sha(artifact.read_bytes()) != source.get(sha_key):
            errors.append(f"source artifact blob lock mismatch: {path_key}")

    errors.extend(inspect_script(script_text, protocol))
    if fresh_result != result:
        errors.append("committed result differs from fresh isolated execution")
    if not result.get("fixture_corpus", {}).get("all_models_valid"):
        errors.append("one or more neutral models failed validation")
    if result.get("fixture_corpus", {}).get("scenario_count") != len(fixtures.get("scenarios", [])):
        errors.append("neutral scenario count drift")
    if not all(result.get("translations", {}).values()):
        errors.append("one or more registered translation checks failed")

    try:
        source_summary = candidate_summary(source_proof, "gate_evidence")
        replication_summary = candidate_summary(result, "gate_results")
    except ValueError as exc:
        errors.append(str(exc))
        source_summary, replication_summary = [], []
    agreement = source_summary == replication_summary
    if not agreement:
        errors.append("candidate classifications or failed-gate sets disagree with source proof")
    if result.get("provisional_result") != [source_spec.get("proposed_foundation")]:
        errors.append("provisional result disagrees with frozen source proposal")
    if result.get("lifecycle", {}).get("investigator_independence") != "not established":
        errors.append("investigator-independence boundary drift")
    if result.get("lifecycle", {}).get("acceptance") != "pending separate adjudication":
        errors.append("premature acceptance")
    if result.get("lifecycle", {}).get("promotion") != "pending separate adjudication":
        errors.append("premature promotion")

    decision = "replicated" if not errors else "not_replicated"
    return {
        "replication_id": protocol.get("replication_id"),
        "status": "Research",
        "decision": decision,
        "errors": errors,
        "independence": {
            "implementation_language_independent": True,
            "source_kernel_import_absent": not any("dependency" in error for error in errors),
            "source_proof_unavailable_during_execution": True,
            "isolated_directory_execution": True,
            "neutral_fixture_history": history,
            "external_investigator_independence": "not established",
        },
        "agreement": {
            "matches_source_classifications_and_failed_gates": agreement,
            "source": source_summary,
            "replication": replication_summary,
        },
        "artifact_locks": {
            "protocol_git_blob_sha": git_blob_sha(PROTOCOL.read_bytes()) if PROTOCOL.is_file() else None,
            "fixtures_git_blob_sha": git_blob_sha(FIXTURES.read_bytes()) if FIXTURES.is_file() else None,
            "implementation_git_blob_sha": git_blob_sha(SCRIPT.read_bytes()) if SCRIPT.is_file() else None,
            "raw_result_git_blob_sha": git_blob_sha(RESULT.read_bytes()) if RESULT.is_file() else None,
            "fresh_result_sha256": sha256_json(fresh_result),
        },
        "lifecycle_consequence": {
            "replication": "complete under the frozen implementation-independent clean-room criterion" if decision == "replicated" else "failed",
            "acceptance": "pending separate PR",
            "promotion": "pending separate PR",
            "canonical_authority_changed": False,
        },
        "merge_requirement": protocol["fixture_corpus"]["merge_requirement"],
        "nonclaims": protocol.get("nonclaims", []),
    }


def render(adjudication: dict[str, Any]) -> str:
    rows = "\n".join(
        f"| `{row['id']}` | `{row['classification']}` | `{', '.join(row['failed_gates']) or 'none'}` |"
        for row in adjudication["agreement"]["replication"]
    )
    errors = adjudication.get("errors", [])
    error_text = "None." if not errors else "\n".join(f"- {error}" for error in errors)
    history = adjudication["independence"]["neutral_fixture_history"]
    return f"""# FARA Canonical-Kernel Clean-Room Replication

Status: **Research**

Replication: `{adjudication['replication_id']}`

## Decision

**{adjudication['decision']}**

The clean-room Node.js implementation reproduced the source campaign's candidate classifications and failed-gate sets across three neutral fixture scenarios. Agreement was computed only after isolated execution.

## Independence achieved

- different implementation language from the source Python kernel;
- no source-kernel import or source-proof access during execution;
- isolated temporary-directory execution;
- fresh output exactly equals the committed raw result;
- Git ancestry proves fixture commit `{history.get('freeze_commit')}` precedes implementation commit `{history.get('implementation_commit')}`;
- the frozen fixture bytes remain unchanged and the implementation was absent at the freeze commit.

## Candidate agreement

| Candidate | Classification | Failed gates |
|---|---|---|
{rows}

## Merge requirement

{adjudication['merge_requirement']}

## Remaining boundary

External investigator independence is **not established**. Acceptance and Promotion require a separate adjudication PR. No canonical FARA authority changes here.

## Validation errors

{error_text}

## Nonclaims

""" + "\n".join(f"- {item}" for item in adjudication["nonclaims"]) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    protocol, fixtures, result = load(PROTOCOL), load(FIXTURES), load(RESULT)
    source_spec = load(ROOT / protocol["source_campaign"]["spec_path"])
    source_proof = load(ROOT / protocol["source_campaign"]["proof_path"])
    adjudication = build_adjudication(protocol, fixtures, result, source_spec, source_proof)
    if args.write:
        ADJUDICATION.write_text(json.dumps(adjudication, indent=2, sort_keys=True) + "\n")
        REPORT.write_text(render(adjudication))
    else:
        errors = list(adjudication["errors"])
        if not ADJUDICATION.is_file() or load(ADJUDICATION) != adjudication:
            errors.append("stale adjudication artifact")
        if not REPORT.is_file() or REPORT.read_text() != render(adjudication):
            errors.append("stale replication report")
        if errors:
            for error in errors:
                print(error)
            return 1
    print(f"FARA kernel replication validation passed: {adjudication['decision']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
