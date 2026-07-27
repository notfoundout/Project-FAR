#!/usr/bin/env python3
"""Fail-closed reconciliation of frozen merged-PR review findings."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

BASELINE_DISPOSITION = "resolved_incorrectly"
DISPOSITIONS = {
    "fixed_on_current_main", "still_reproducible", "obsolete_after_later_changes",
    "superseded_by_canonical_change", "cannot_verify",
}
RESIDUAL = {"still_reproducible", "cannot_verify"}
DEFINITIVE = DISPOSITIONS - {"cannot_verify"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def subsystem(path: str | None) -> str:
    path = path or ""
    rules = (
        ("commercial/far-release-assurance/external-validation", "external-validation"),
        ("theory/evaluation/comparative-representation", "comparative-experiments"),
        (".github/workflows", "ci-and-automation"), ("tools/", "validators-and-tooling"),
        ("tests/", "test-infrastructure"), ("mechanization/", "mechanization"),
        ("far_validation/", "validation-engine"), ("theory/", "canonical-theory"),
        ("research/", "research-records"), ("frameworks/", "frameworks"),
        ("commercial/", "commercial-validation"), ("docs/", "documentation-and-governance"),
    )
    return next((name for prefix, name in rules if path.startswith(prefix)), "repository-metadata")


def blocking(path: str | None, claim: str) -> bool:
    text = f"{path or ''} {claim}".lower()
    return any(token in text for token in (
        "reconstruct", "reproduc", "execution", "experiment", "manifest", "checksum",
        "frozen", "swe-agent", "cre-00", "preregistration", "trace",
    ))


def plain(value: str) -> str:
    value = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", str(value))
    value = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"</?[^>]+>", "", value)
    return " ".join(value.split())


def title(claim: str) -> str:
    return re.sub(r"[*_`]", "", plain(claim)).strip()[:180] or "Unlabeled review defect"


def locate(root: Path, item: dict[str, Any], override: dict[str, Any]) -> tuple[str | None, list[int]]:
    path = override.get("current_path", item.get("path"))
    if not path or not (root / path).is_file():
        return path, []
    if override.get("current_lines"):
        return path, list(override["current_lines"])
    lines = (root / path).read_text(encoding="utf-8", errors="replace").splitlines()
    original = int(item.get("line") or 1)
    return path, [min(max(original, 1), max(len(lines), 1))]


def reconcile(root: Path, baseline: dict[str, Any], decisions: dict[str, Any]) -> dict[str, Any]:
    original = [x for x in baseline.get("findings", []) if x.get("disposition") == BASELINE_DISPOSITION]
    overrides = {x["finding_id"]: x for x in decisions.get("decisions", [])}
    if len(overrides) != len(decisions.get("decisions", [])):
        raise ValueError("duplicate reconciliation decision")
    unknown = sorted(set(overrides) - {x["finding_id"] for x in original})
    if unknown:
        raise ValueError(f"decisions reference non-baseline findings: {unknown}")

    records = []
    for item in original:
        override = overrides.get(item["finding_id"])
        disposition = override.get("disposition") if override else "cannot_verify"
        if disposition not in DISPOSITIONS:
            raise ValueError(f"invalid disposition for {item['finding_id']}")
        if disposition in DEFINITIVE and (not override or not override.get("evidence")):
            raise ValueError(
                f"finding {item['finding_id']} requires explicit disposition-specific evidence for {disposition}"
            )
        current_path, current_lines = locate(root, item, override or {})
        explicit_root = (override or {}).get("root_cause_id")
        records.append({
            "finding_id": item["finding_id"], "pr_number": item["pr_number"],
            "thread_id": item["thread_id"], "comment_id": item.get("comment_id"),
            "review_url": item.get("url"), "original_path": item.get("path"),
            "original_line": item.get("line"), "reviewer_claim": item["reviewer_claim"],
            "disposition": disposition, "risk": item["risk"],
            "subsystem": subsystem(current_path),
            "root_cause_id": explicit_root or f"unverified:{item['finding_id']}",
            "root_cause_verified": bool(explicit_root),
            "current_path": current_path, "current_lines": current_lines,
            "failure_mechanism": (override or {}).get("failure_mechanism") or item.get("rationale") or item["reviewer_claim"],
            "blocks_experiment_reconstruction": bool((override or {}).get(
                "blocks_experiment_reconstruction", blocking(current_path, item["reviewer_claim"])
            )),
            "smallest_complete_remediation_boundary": (override or {}).get(
                "smallest_complete_remediation_boundary",
                f"Verify the current-main status of {title(item['reviewer_claim'])!r}; if reproducible, repair the authoritative source and add a focused regression test; otherwise record concrete fix, obsolescence, or supersession evidence."
            ),
            "evidence": list((override or {}).get("evidence", [
                "No disposition-specific current-main reproduction, mechanical comparison, or supersession evidence has been recorded."
            ])),
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
    return {
        "schema_version": 2, "policy": "current_main_residual_v2_fail_closed",
        "source": decisions["source"], "baseline_commit": decisions["baseline_commit"],
        "audited_main_commit": decisions["audited_main_commit"], "counts": counts,
        "findings": records,
    }


def validate(data: dict[str, Any], baseline: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_ids = [x["finding_id"] for x in baseline["findings"] if x["disposition"] == BASELINE_DISPOSITION]
    ids = [x.get("finding_id") for x in data.get("findings", [])]
    if Counter(ids) != Counter(source_ids):
        errors.append("original finding set is not preserved exactly once")
    for x in data.get("findings", []):
        if x.get("disposition") not in DISPOSITIONS:
            errors.append(f"{x.get('finding_id')}: invalid disposition")
        if x.get("disposition") in DEFINITIVE and not x.get("evidence"):
            errors.append(f"{x.get('finding_id')}: definitive disposition lacks evidence")
        if x.get("disposition") == "still_reproducible" and not x.get("root_cause_verified"):
            errors.append(f"{x.get('finding_id')}: reproducible disposition lacks verified mechanism")
    if data["counts"]["residual"] != sum(x["disposition"] in RESIDUAL for x in data["findings"]):
        errors.append("residual count mismatch")
    return errors


def compact_ledger(data: dict[str, Any]) -> dict[str, Any]:
    explicit = [x for x in data["findings"] if x["disposition"] != "cannot_verify"]
    return {
        "schema_version": 2,
        "policy": data["policy"],
        "source": data["source"],
        "baseline_commit": data["baseline_commit"],
        "audited_main_commit": data["audited_main_commit"],
        "default_disposition": "cannot_verify",
        "default_evidence": "No disposition-specific current-main evidence is recorded.",
        "source_finding_count": data["counts"]["total"],
        "counts": data["counts"],
        "explicit_findings": explicit,
        "composition_rule": "Apply explicit_findings by finding_id; every remaining resolved_incorrectly source finding is cannot_verify and retains its source traceability and remediation boundary until audited.",
    }


def render_report(data: dict[str, Any]) -> str:
    c = data["counts"]
    p1 = sum(x["risk"] in {"critical", "high"} and x["disposition"] in RESIDUAL for x in data["findings"])
    return "\n".join([
        "# Merged-PR finding reconciliation", "",
        f"Audited main: `{data['audited_main_commit']}`", "",
        "## Result", "",
        f"- Source findings: {c['total']}", f"- Residual findings: {c['residual']}",
        *[f"- `{k}`: {v}" for k, v in c["by_disposition"].items()], "",
        "Unaudited findings fail closed to `cannot_verify`; they are not claimed reproducible.", "",
        "## Residual counts", "",
        f"- By risk: `{json.dumps(c['by_risk'], sort_keys=True)}`",
        f"- By subsystem: `{json.dumps(c['by_subsystem'], sort_keys=True)}`",
        f"- By experiment-blocking status: `{json.dumps(c['by_experiment_blocking'], sort_keys=True)}`", "",
        f"**{p1} unresolved P1 findings require verification or remediation.**", "",
        "The compact authoritative ledger composes this result with the immutable source findings; only disposition-specific overrides are duplicated here.",
    ])


def render_queue(data: dict[str, Any]) -> str:
    c = data["counts"]
    return "\n".join([
        "# Authoritative residual verification and remediation queue", "",
        f"Residual count: {c['residual']}", "",
        f"- `cannot_verify`: {c['by_disposition'].get('cannot_verify', 0)}",
        f"- `still_reproducible`: {c['by_disposition'].get('still_reproducible', 0)}", "",
        "All unaudited source findings remain active through the ledger composition rule. They must be verified before remediation batching; none is represented as reproduced merely because it appeared in the historical queue.", "",
        f"- Risk counts: `{json.dumps(c['by_risk'], sort_keys=True)}`",
        f"- Experiment-blocking counts: `{json.dumps(c['by_experiment_blocking'], sort_keys=True)}`",
    ])


def render_batches(data: dict[str, Any]) -> str:
    verified = [x for x in data["findings"] if x["disposition"] in RESIDUAL and x["root_cause_verified"]]
    lines = [
        "# Residual remediation batches", "",
        "Only findings with an explicitly demonstrated shared root-cause mechanism may be batched.", "",
    ]
    if not verified:
        lines += [
            "No residual finding currently has a verified root-cause batch.", "",
            "The 400 unaudited findings remain `cannot_verify` and must retain distinct source traceability and remediation boundaries until individually audited or mechanically reproduced.",
        ]
    else:
        for x in verified:
            lines += [
                f"## `{x['root_cause_id']}`", "",
                f"- Finding: `{x['finding_id']}`",
                f"- Trace: PR `{x['pr_number']}`, thread `{x['thread_id']}`, comment `{x.get('comment_id')}`",
                f"- Boundary: {plain(x['smallest_complete_remediation_boundary'])}", "",
            ]
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--baseline", type=Path, required=True)
    p.add_argument("--decisions", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    baseline, decisions = load(a.baseline), load(a.decisions)
    data = reconcile(Path.cwd(), baseline, decisions)
    errors = validate(data, baseline)
    if errors:
        raise SystemExit("\n".join(errors))
    outputs = {
        "disposition-ledger.json": json.dumps(compact_ledger(data), indent=2, sort_keys=True) + "\n",
        "RECONCILIATION_REPORT.md": render_report(data) + "\n",
        "RESIDUAL_REMEDIATION_QUEUE.md": render_queue(data) + "\n",
        "REMEDIATION_BATCHES.md": render_batches(data) + "\n",
    }
    if a.check:
        stale = [name for name, text in outputs.items() if not (a.output_dir / name).is_file() or (a.output_dir / name).read_text(encoding="utf-8") != text]
        if stale:
            raise SystemExit(f"stale reconciliation outputs: {', '.join(stale)}")
    else:
        a.output_dir.mkdir(parents=True, exist_ok=True)
        for name, text in outputs.items():
            (a.output_dir / name).write_text(text, encoding="utf-8")
    print(f"validated {len(data['findings'])} findings; residual={data['counts']['residual']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
