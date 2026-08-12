#!/usr/bin/env python3
"""Fail-closed reconciliation of frozen merged-PR review findings."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

BASELINE_DISPOSITION = "resolved_incorrectly"
DISPOSITIONS = {"fixed_on_current_main", "still_reproducible", "obsolete_after_later_changes", "superseded_by_canonical_change", "cannot_verify"}
RESIDUAL = {"still_reproducible", "cannot_verify"}
DEFINITIVE = DISPOSITIONS - {"cannot_verify"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(raw: bytes) -> str:
    """Return the Git object ID for exact file bytes."""
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def verify_frozen_baseline(raw: bytes, decisions: dict[str, Any]) -> None:
    expected = decisions.get("baseline_git_blob_sha")
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{40}", expected):
        raise ValueError("reconciliation decisions must pin baseline_git_blob_sha")
    actual = git_blob_sha(raw)
    if actual != expected:
        raise ValueError(f"frozen baseline digest mismatch: expected {expected}, actual {actual}")


def plain(value: str) -> str:
    value = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", str(value))
    value = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", value)
    return " ".join(re.sub(r"</?[^>]+>", "", value).split())


def subsystem(path: str | None) -> str:
    path = path or ""
    for prefix, name in (
        ("commercial/far-release-assurance/external-validation", "external-validation"),
        ("theory/evaluation/comparative-representation", "comparative-experiments"),
        (".github/workflows", "ci-and-automation"), ("tools/", "validators-and-tooling"),
        ("tests/", "test-infrastructure"), ("mechanization/", "mechanization"),
        ("far_validation/", "validation-engine"), ("theory/", "canonical-theory"),
        ("research/", "research-records"), ("frameworks/", "frameworks"),
        ("commercial/", "commercial-validation"), ("docs/", "documentation-and-governance"),
    ):
        if path.startswith(prefix):
            return name
    return "repository-metadata"


def reconcile(root: Path, baseline: dict[str, Any], decisions: dict[str, Any]) -> dict[str, Any]:
    source = [x for x in baseline.get("findings", []) if x.get("disposition") == BASELINE_DISPOSITION]
    overrides = {x["finding_id"]: x for x in decisions.get("decisions", [])}
    if len(overrides) != len(decisions.get("decisions", [])):
        raise ValueError("duplicate reconciliation decision")
    unknown = sorted(set(overrides) - {x["finding_id"] for x in source})
    if unknown:
        raise ValueError(f"decisions reference non-baseline findings: {unknown}")
    records = []
    for item in source:
        override = overrides.get(item["finding_id"])
        disposition = override.get("disposition") if override else "cannot_verify"
        if disposition not in DISPOSITIONS:
            raise ValueError(f"invalid disposition for {item['finding_id']}")
        if disposition in DEFINITIVE:
            if not override or not override.get("evidence"):
                raise ValueError(f"finding {item['finding_id']} requires explicit disposition-specific evidence for {disposition}")
            if not override.get("failure_mechanism"):
                raise ValueError(f"finding {item['finding_id']} requires explicit disposition-specific rationale for {disposition}")
        path = (override or {}).get("current_path", item.get("path"))
        explicit_root = (override or {}).get("root_cause_id")
        blocking_status = (override or {}).get("blocks_experiment_reconstruction", "unknown")
        if not (type(blocking_status) is bool or blocking_status == "unknown"):
            raise ValueError(f"finding {item['finding_id']} has invalid experiment-blocking status")
        root_cause_verified = bool(explicit_root) and disposition != "cannot_verify"
        records.append({
            "finding_id": item["finding_id"], "pr_number": item["pr_number"], "thread_id": item["thread_id"],
            "comment_id": item.get("comment_id"), "disposition": disposition, "risk": item["risk"],
            "subsystem": subsystem(path), "current_path": path,
            "root_cause_id": explicit_root or f"unverified:{item['finding_id']}",
            "root_cause_verified": root_cause_verified,
            "blocks_experiment_reconstruction": blocking_status,
            "failure_mechanism": (override or {}).get("failure_mechanism", "No current-main failure mechanism has been verified."),
            "smallest_complete_remediation_boundary": (override or {}).get("smallest_complete_remediation_boundary", f"Verify `{item['finding_id']}` against current main before assigning a remediation batch."),
            "evidence": list((override or {}).get("evidence", ["No disposition-specific current-main evidence is recorded."])),
        })
    records.sort(key=lambda x: x["finding_id"])
    counts = {
        "total": len(records),
        "by_disposition": dict(sorted(Counter(x["disposition"] for x in records).items())),
        "by_risk": dict(sorted(Counter(x["risk"] for x in records if x["disposition"] in RESIDUAL).items())),
        "by_subsystem": dict(sorted(Counter(x["subsystem"] for x in records if x["disposition"] in RESIDUAL).items())),
        "by_experiment_blocking": dict(sorted(Counter(str(x["blocks_experiment_reconstruction"]).lower() for x in records if x["disposition"] in RESIDUAL).items())),
        "residual": sum(x["disposition"] in RESIDUAL for x in records),
    }
    return {"schema_version": 4, "policy": "current_main_residual_v4_pinned_fail_closed", "source": decisions["source"], "baseline_commit": decisions["baseline_commit"], "baseline_git_blob_sha": decisions["baseline_git_blob_sha"], "audited_main_commit": decisions["audited_main_commit"], "counts": counts, "findings": records}


def validate(data: dict[str, Any], baseline: dict[str, Any]) -> list[str]:
    errors = []
    source_ids = [x["finding_id"] for x in baseline["findings"] if x["disposition"] == BASELINE_DISPOSITION]
    ids = [x["finding_id"] for x in data["findings"]]
    if Counter(ids) != Counter(source_ids):
        errors.append("original finding set is not preserved exactly once")
    for x in data["findings"]:
        if x["disposition"] == "still_reproducible" and not x["root_cause_verified"]:
            errors.append(f"{x['finding_id']}: reproducible disposition lacks verified mechanism")
        if x["disposition"] == "cannot_verify" and x["root_cause_verified"]:
            errors.append(f"{x['finding_id']}: cannot_verify disposition cannot have a verified root cause")
    return errors


def compact_ledger(data: dict[str, Any]) -> dict[str, Any]:
    explicit = [{"finding_id": x["finding_id"], "disposition": x["disposition"], "evidence": x["evidence"], "failure_mechanism": x["failure_mechanism"], "root_cause_id": x["root_cause_id"], "blocks_experiment_reconstruction": x["blocks_experiment_reconstruction"]} for x in data["findings"] if x["disposition"] != "cannot_verify"]
    return {"schema_version": 4, "policy": data["policy"], "source": data["source"], "baseline_commit": data["baseline_commit"], "baseline_git_blob_sha": data["baseline_git_blob_sha"], "audited_main_commit": data["audited_main_commit"], "default_disposition": "cannot_verify", "default_evidence": "No disposition-specific current-main evidence is recorded.", "default_experiment_blocking_status": "unknown", "source_finding_count": data["counts"]["total"], "counts": data["counts"], "explicit_findings": explicit, "composition_rule": "Apply explicit_findings by finding_id; every remaining resolved_incorrectly source finding is cannot_verify, has unknown experiment-blocking status, and retains source traceability until audited."}


def render_report(data: dict[str, Any]) -> str:
    c = data["counts"]
    p1 = sum(x["risk"] in {"critical", "high"} and x["disposition"] in RESIDUAL for x in data["findings"])
    return "\n".join(["# Merged-PR finding reconciliation", "", f"Audited main: `{data['audited_main_commit']}`", f"Frozen baseline Git blob: `{data['baseline_git_blob_sha']}`", "", "## Result", "", f"- Source findings: {c['total']}", f"- Residual findings: {c['residual']}", *[f"- `{k}`: {v}" for k, v in c["by_disposition"].items()], "", "Unaudited findings fail closed to `cannot_verify`; they are not claimed reproducible.", "Unaudited experiment-blocking status remains `unknown`; no keyword heuristic is treated as authoritative.", "", "## Residual counts", "", f"- By risk: `{json.dumps(c['by_risk'], sort_keys=True)}`", f"- By subsystem: `{json.dumps(c['by_subsystem'], sort_keys=True)}`", f"- By experiment-blocking status: `{json.dumps(c['by_experiment_blocking'], sort_keys=True)}`", "", f"**{p1} unresolved P1 findings require verification or remediation.**"])


def render_queue(data: dict[str, Any]) -> str:
    c = data["counts"]
    return "\n".join(["# Authoritative residual verification and remediation queue", "", f"Residual count: {c['residual']}", "", f"- `cannot_verify`: {c['by_disposition'].get('cannot_verify', 0)}", f"- `still_reproducible`: {c['by_disposition'].get('still_reproducible', 0)}", "", "All unaudited source findings remain active through the ledger composition rule. They must be verified before remediation batching or experiment-blocking classification.", "", f"- Risk counts: `{json.dumps(c['by_risk'], sort_keys=True)}`", f"- Experiment-blocking counts: `{json.dumps(c['by_experiment_blocking'], sort_keys=True)}`"])


def render_batches(data: dict[str, Any]) -> str:
    verified = [x for x in data["findings"] if x["disposition"] in RESIDUAL and x["root_cause_verified"]]
    unaudited = sum(x["disposition"] == "cannot_verify" and not x["root_cause_verified"] for x in data["findings"])
    if not verified:
        return "\n".join(["# Residual remediation batches", "", "Only findings with an explicitly demonstrated shared root-cause mechanism may be batched.", "", "No residual finding currently has a verified root-cause batch.", "", f"The {unaudited} unaudited findings remain `cannot_verify` and retain distinct source traceability and remediation boundaries until audited."])
    lines = ["# Residual remediation batches", ""]
    for x in verified:
        lines += [f"## `{x['root_cause_id']}`", "", f"- Finding: `{x['finding_id']}`", f"- Trace: PR `{x['pr_number']}`, thread `{x['thread_id']}`, comment `{x['comment_id']}`", f"- Risk: `{x['risk']}`", f"- Experiment blocking: `{str(x['blocks_experiment_reconstruction']).lower()}`", f"- Boundary: {plain(x['smallest_complete_remediation_boundary'])}", ""]
    return "\n".join(lines).rstrip()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--baseline", type=Path, required=True); p.add_argument("--decisions", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True); p.add_argument("--check", action="store_true")
    a = p.parse_args()
    decisions = load(a.decisions)
    baseline_raw = a.baseline.read_bytes()
    verify_frozen_baseline(baseline_raw, decisions)
    baseline = json.loads(baseline_raw.decode("utf-8"))
    data = reconcile(Path.cwd(), baseline, decisions)
    errors = validate(data, baseline)
    if errors: raise SystemExit("\n".join(errors))
    outputs = {"disposition-ledger.json": json.dumps(compact_ledger(data), indent=2, sort_keys=True) + "\n", "RECONCILIATION_REPORT.md": render_report(data).rstrip() + "\n", "RESIDUAL_REMEDIATION_QUEUE.md": render_queue(data).rstrip() + "\n", "REMEDIATION_BATCHES.md": render_batches(data).rstrip() + "\n"}
    if a.check:
        stale = [n for n, t in outputs.items() if not (a.output_dir / n).is_file() or (a.output_dir / n).read_text(encoding="utf-8") != t]
        if stale: raise SystemExit(f"stale reconciliation outputs: {', '.join(stale)}")
    else:
        a.output_dir.mkdir(parents=True, exist_ok=True)
        for n, t in outputs.items(): (a.output_dir / n).write_text(t, encoding="utf-8")
    print(f"validated {len(data['findings'])} findings; residual={data['counts']['residual']}")
    return 0


if __name__ == "__main__": raise SystemExit(main())
