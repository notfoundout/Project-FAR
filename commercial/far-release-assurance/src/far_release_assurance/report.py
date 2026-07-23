"""Deterministic release-assurance reports and evidence manifests."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from .compare import ComparisonSummary, comparison_to_dict
from .io import canonical_json, package_digest
from .model import ReleasePackage

REPORT_SCHEMA = "far-release-report/0.1"
MANIFEST_SCHEMA = "far-evidence-manifest/0.1"


@dataclass(frozen=True, slots=True)
class ReportBundle:
    report_json: str
    report_markdown: str
    manifest_json: str


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def report_payload(
    baseline: ReleasePackage,
    candidate: ReleasePackage,
    summary: ComparisonSummary,
) -> dict[str, object]:
    comparison = comparison_to_dict(summary)
    findings = comparison["findings"]
    assert isinstance(findings, list)
    return {
        "schema_version": REPORT_SCHEMA,
        "decision": summary.comparison.decision.value,
        "rationale": summary.comparison.rationale,
        "baseline": {
            "release_id": baseline.release_id,
            "source_commit": baseline.source_commit,
            "package_digest": package_digest(baseline),
            "closure_status": summary.comparison.baseline_closure.status.value,
        },
        "candidate": {
            "release_id": candidate.release_id,
            "source_commit": candidate.source_commit,
            "package_digest": package_digest(candidate),
            "closure_status": summary.comparison.candidate_closure.status.value,
        },
        "summary": {
            "finding_count": len(findings),
            "blocking_finding_count": sum(bool(item["blocking"]) for item in findings),
            "unknown_finding_count": sum(item["disposition"] == "unknown" for item in findings),
            "machinery_added": len(summary.machinery.added),
            "machinery_removed": len(summary.machinery.removed),
            "machinery_changed": len(summary.machinery.changed),
            "newly_unresolved": len(summary.machinery.newly_unresolved),
            "replay_delta": summary.replay_delta,
        },
        "comparison": comparison,
        "claim_boundary": (
            "This report evaluates disclosed, instrumented release packages. "
            "It does not prove hidden cognition, telemetry completeness, causal truth, "
            "safety, or legal compliance."
        ),
    }


def canonical_report_json(payload: dict[str, object]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"


def render_markdown(payload: dict[str, object]) -> str:
    baseline = payload["baseline"]
    candidate = payload["candidate"]
    summary = payload["summary"]
    comparison = payload["comparison"]
    assert isinstance(baseline, dict)
    assert isinstance(candidate, dict)
    assert isinstance(summary, dict)
    assert isinstance(comparison, dict)
    findings = comparison["findings"]
    assert isinstance(findings, list)

    lines = [
        "# FAR Release Assurance Report",
        "",
        f"**Decision:** {str(payload['decision']).replace('_', ' ').title()}",
        "",
        str(payload["rationale"]),
        "",
        "## Releases",
        "",
        f"- Baseline: `{baseline['release_id']}` at `{baseline['source_commit']}`",
        f"- Candidate: `{candidate['release_id']}` at `{candidate['source_commit']}`",
        f"- Baseline package digest: `{baseline['package_digest']}`",
        f"- Candidate package digest: `{candidate['package_digest']}`",
        "",
        "## Integrity Summary",
        "",
        f"- Findings: {summary['finding_count']}",
        f"- Blocking findings: {summary['blocking_finding_count']}",
        f"- Unknown findings: {summary['unknown_finding_count']}",
        f"- Machinery added / removed / changed: {summary['machinery_added']} / {summary['machinery_removed']} / {summary['machinery_changed']}",
        f"- Newly unresolved machinery: {summary['newly_unresolved']}",
        f"- Replay completeness delta: {summary['replay_delta']}",
        "",
        "## Findings",
        "",
    ]
    if not findings:
        lines.append("No findings.")
    else:
        for finding in findings:
            assert isinstance(finding, dict)
            lines.extend(
                [
                    f"### {finding['rule_id']}",
                    "",
                    f"- Severity: {finding['severity']}",
                    f"- Disposition: {finding['disposition']}",
                    f"- Blocking: {str(finding['blocking']).lower()}",
                    f"- Affected IDs: {', '.join(finding['affected_ids']) or 'none'}",
                    "",
                    str(finding["rationale"]),
                    "",
                ]
            )
    lines.extend(["## Claim Boundary", "", str(payload["claim_boundary"]), ""])
    return "\n".join(lines)


def build_report_bundle(
    baseline: ReleasePackage,
    candidate: ReleasePackage,
    summary: ComparisonSummary,
) -> ReportBundle:
    payload = report_payload(baseline, candidate, summary)
    report_json = canonical_report_json(payload)
    report_markdown = render_markdown(payload)
    manifest = {
        "schema_version": MANIFEST_SCHEMA,
        "baseline_package_digest": package_digest(baseline),
        "candidate_package_digest": package_digest(candidate),
        "baseline_canonical_digest": _sha256_text(canonical_json(baseline)),
        "candidate_canonical_digest": _sha256_text(canonical_json(candidate)),
        "report_json_digest": _sha256_text(report_json),
        "report_markdown_digest": _sha256_text(report_markdown),
        "decision": summary.comparison.decision.value,
    }
    manifest_json = json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n"
    return ReportBundle(report_json, report_markdown, manifest_json)


def write_report_bundle(bundle: ReportBundle, output_directory: str | Path) -> None:
    directory = Path(output_directory)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "report.json").write_text(bundle.report_json, encoding="utf-8")
    (directory / "report.md").write_text(bundle.report_markdown, encoding="utf-8")
    (directory / "manifest.json").write_text(bundle.manifest_json, encoding="utf-8")
