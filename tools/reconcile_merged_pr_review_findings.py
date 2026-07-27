#!/usr/bin/env python3
"""Generate the residual state of the frozen merged-PR review audit."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
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
        (".github/workflows", "ci-and-automation"),
        ("tools/", "validators-and-tooling"), ("tests/", "test-infrastructure"),
        ("mechanization/", "mechanization"), ("far_validation/", "validation-engine"),
        ("theory/", "canonical-theory"), ("research/", "research-records"),
        ("frameworks/", "frameworks"), ("commercial/", "commercial-validation"),
        ("docs/", "documentation-and-governance"),
    )
    return next((name for prefix, name in rules if path.startswith(prefix)), "repository-metadata")


def blocking(path: str | None, claim: str) -> bool:
    text = f"{path or ''} {claim}".lower()
    return any(token in text for token in (
        "reconstruct", "reproduc", "execution", "experiment", "manifest", "checksum",
        "frozen", "swe-agent", "cre-00", "preregistration", "trace",
    ))


def title(claim: str) -> str:
    clean = plain(claim)
    clean = re.sub(r"[*_`]", "", clean).strip()
    return (clean.splitlines()[0] or "Unlabeled review defect")[:180]


def plain(value: str) -> str:
    """Render frozen review text without activating its Markdown or HTML."""
    value = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", str(value))
    value = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"</?[^>]+>", "", value)
    return " ".join(value.split())


def locate(root: Path, item: dict[str, Any], override: dict[str, Any]) -> tuple[str | None, list[int]]:
    path = override.get("current_path", item.get("path"))
    if not path or not (root / path).is_file():
        return path, []
    if override.get("current_lines"):
        return path, list(override["current_lines"])
    lines = (root / path).read_text(encoding="utf-8", errors="replace").splitlines()
    original = item.get("line")
    return path, [min(max(int(original or 1), 1), max(len(lines), 1))]


def _explicit_override_evidence(item: dict[str, Any], override: dict[str, Any], disposition: str) -> list[str]:
    """Return evidence that supports the new disposition, never inherited baseline evidence."""
    if disposition == "cannot_verify":
        return list(override.get("evidence", []))
    if "evidence" not in override or not override.get("evidence"):
        raise ValueError(
            f"finding {item['finding_id']} requires explicit disposition-specific evidence for {disposition}"
        )
    return list(override["evidence"])


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
        current_path, current_lines = locate(root, item, override or {})
        evidence = _explicit_override_evidence(item, override or {}, disposition)
        if disposition == "cannot_verify" and not evidence:
            evidence = [
                "No disposition-specific current-main reproduction, mechanical comparison, or supersession evidence has been recorded."
            ]
        mechanism = (override or {}).get("failure_mechanism") or item.get("rationale") or item["reviewer_claim"]
        scope = subsystem(current_path)
        is_blocking = bool((override or {}).get(
            "blocks_experiment_reconstruction", blocking(current_path, item["reviewer_claim"])
        ))
        explicit_root_cause = (override or {}).get("root_cause_id")
        root_cause_id = explicit_root_cause or f"unverified:{item['finding_id']}"
        records.append({
            "finding_id": item["finding_id"], "pr_number": item["pr_number"],
            "thread_id": item["thread_id"], "comment_id": item.get("comment_id"),
            "review_url": item.get("url"), "original_path": item.get("path"),
            "original_line": item.get("line"), "reviewer_claim": item["reviewer_claim"],
            "disposition": disposition, "risk": item["risk"], "subsystem": scope,
            "root_cause_id": root_cause_id,
            "root_cause_verified": bool(explicit_root_cause),
            "current_path": current_path, "current_lines": current_lines,
            "failure_mechanism": mechanism,
            "blocks_experiment_reconstruction": is_blocking,
            "smallest_complete_remediation_boundary": (override or {}).get(
                "smallest_complete_remediation_boundary",
                f"Verify the current-main status of {title(item['reviewer_claim'])!r}; if reproducible, correct the authoritative source and add a focused regression test, otherwise record concrete fix, obsolescence, or supersession evidence."
            ),
            "evidence": evidence,
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
    return {"schema_version": 2, "policy": "current_main_residual_v2_fail_closed",
            "source": decisions["source"], "baseline_commit": decisions["baseline_commit"],
            "audited_main_commit": decisions["audited_main_commit"], "counts": counts,
            "findings": records}


def render_report(data: dict[str, Any]) -> str:
    c = data["counts"]
    lines = ["# Merged-PR finding reconciliation", "", f"Audited main: `{data['audited_main_commit']}`",
             f"Frozen input disposition: `{BASELINE_DISPOSITION}`", "", "## Result", "",
             f"- Original findings reconciled: {c['total']}", f"- Residual findings: {c['residual']}"]
    lines += [f"- `{k}`: {v}" for k, v in c["by_disposition"].items()]
    lines += ["", "## Residual counts", "", f"- By risk: `{json.dumps(c['by_risk'], sort_keys=True)}`",
              f"- By subsystem: `{json.dumps(c['by_subsystem'], sort_keys=True)}`",
              f"- By experiment-blocking status: `{json.dumps(c['by_experiment_blocking'], sort_keys=True)}`", ""]
    p1 = [x for x in data["findings"] if x["disposition"] in RESIDUAL and x["risk"] in {"critical", "high"}]
    lines += ["## Unresolved P1 findings", "", f"**{len(p1)} unresolved P1 findings require verification or remediation.**", ""]
    lines += [f"- `{x['finding_id']}` — `{x['disposition']}` — `{x['current_path']}` — {title(x['reviewer_claim'])}" for x in p1]
    lines += ["", "## Complete dispositions", ""]
    for x in data["findings"]:
        loc = x["current_path"] or "missing path"
        if x["current_lines"]:
            loc += ":" + "-".join(map(str, x["current_lines"]))
        lines += [f"### {x['finding_id']}", "", f"- Disposition: `{x['disposition']}`", f"- Risk/subsystem: `{x['risk']}` / `{x['subsystem']}`",
                  f"- Current location: `{loc}`", f"- Blocks experiment reconstruction: `{str(x['blocks_experiment_reconstruction']).lower()}`",
                  f"- Root cause: `{x['root_cause_id']}`", f"- Root cause verified: `{str(x['root_cause_verified']).lower()}`",
                  f"- Failure mechanism: {plain(x['failure_mechanism'])}",
                  f"- Remediation boundary: {plain(x['smallest_complete_remediation_boundary'])}", "- Evidence:"]
        lines += [f"  - {plain(e)}" for e in x["evidence"]]
        lines.append("")
    return "\n".join(lines)


def render_queue(data: dict[str, Any]) -> str:
    residual = [x for x in data["findings"] if x["disposition"] in RESIDUAL]
    lines = ["# Authoritative residual remediation queue", "",
             "Only `still_reproducible` and `cannot_verify` findings are active.", "",
             f"Residual count: {len(residual)}", ""]
    for risk in ("critical", "high", "medium", "low"):
        items = [x for x in residual if x["risk"] == risk]
        lines += [f"## {risk.title()} ({len(items)})", ""]
        lines += [f"- `{x['finding_id']}` — `{x['disposition']}` — `{x['current_path']}` — {title(x['reviewer_claim'])}" for x in items]
        lines.append("")
    return "\n".join(lines)


def render_batches(data: dict[str, Any]) -> str:
    groups: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for x in data["findings"]:
        if x["disposition"] in RESIDUAL:
            groups[x["subsystem"]][x["root_cause_id"]].append(x)
    lines = [
        "# Residual remediation batches", "",
        "Findings are grouped only when an explicit shared root-cause identifier exists. Unverified findings retain unique groups.", "",
    ]
    for scope in sorted(groups):
        lines += [f"## {scope}", ""]
        for cause, items in sorted(groups[scope].items()):
            lines += [f"### `{cause}`", "", f"- Findings ({len(items)}):"]
            for x in items:
                lines += [
                    f"  - `{x['finding_id']}` — `{x['disposition']}` — risk `{x['risk']}` — experiment-blocking `{str(x['blocks_experiment_reconstruction']).lower()}`",
                    f"    - Trace: PR `{x['pr_number']}`, thread `{x['thread_id']}`, comment `{x.get('comment_id')}`",
                    f"    - Boundary: {plain(x['smallest_complete_remediation_boundary'])}",
                ]
            lines.append("")
    return "\n".join(lines)


def validate(data: dict[str, Any], baseline: dict[str, Any], queue: str) -> list[str]:
    errors = []
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
        active = x.get("disposition") in RESIDUAL
        present = f"`{x.get('finding_id')}`" in queue
        if active != present:
            errors.append(f"{x.get('finding_id')}: queue/ledger mismatch")
    expected = sum(x["disposition"] in RESIDUAL for x in data["findings"])
    if data["counts"]["residual"] != expected:
        errors.append("residual count mismatch")
    return errors


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--baseline", type=Path, required=True)
    p.add_argument("--decisions", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    root = Path.cwd()
    baseline = load(a.baseline)
    decisions = load(a.decisions)
    data = reconcile(root, baseline, decisions)
    report = render_report(data) + "\n"
    queue = render_queue(data) + "\n"
    batches = render_batches(data) + "\n"
    errors = validate(data, baseline, queue)
    if errors:
        raise SystemExit("\n".join(errors))
    outputs = {
        "disposition-ledger.json": json.dumps(data, indent=2, sort_keys=True) + "\n",
        "RECONCILIATION_REPORT.md": report,
        "RESIDUAL_REMEDIATION_QUEUE.md": queue,
        "REMEDIATION_BATCHES.md": batches,
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
