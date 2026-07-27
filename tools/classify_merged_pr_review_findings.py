#!/usr/bin/env python3
"""Classify frozen merged-PR review threads without claiming unsupported resolution.

The classifier is deliberately conservative. GitHub's resolved/outdated metadata is
not treated as proof that a reviewer concern was correctly addressed. Definite
claims require a separately recorded evidence decision in an overrides file.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ALLOWED = {
    "resolved_correctly",
    "resolved_incorrectly",
    "unresolved",
    "obsolete_after_later_changes",
    "non_actionable",
    "uncertain_manual_review_required",
}


@dataclass(frozen=True)
class Finding:
    finding_id: str
    pr_number: int
    thread_id: str
    comment_id: str | None
    path: str | None
    line: int | None
    url: str | None
    reviewer_claim: str
    github_is_resolved: bool
    github_is_outdated: bool
    disposition: str
    confidence: str
    evidence: list[str]
    rationale: str


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing required input: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc


def load_overrides(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    data = load_json(path)
    if data.get("schema_version") != 1 or not isinstance(data.get("decisions"), list):
        raise SystemExit("override file must contain schema_version=1 and a decisions list")
    result: dict[str, dict[str, Any]] = {}
    for decision in data["decisions"]:
        finding_id = decision.get("finding_id")
        disposition = decision.get("disposition")
        evidence = decision.get("evidence")
        rationale = decision.get("rationale")
        if not finding_id or disposition not in ALLOWED:
            raise SystemExit(f"invalid override decision: {decision!r}")
        if disposition in {"resolved_correctly", "resolved_incorrectly", "obsolete_after_later_changes"}:
            if not isinstance(evidence, list) or not evidence or not rationale:
                raise SystemExit(f"evidence and rationale required for definitive override {finding_id}")
        if finding_id in result:
            raise SystemExit(f"duplicate override for {finding_id}")
        result[finding_id] = decision
    return result


def first_comment(thread: dict[str, Any]) -> dict[str, Any]:
    comments = thread.get("comments")
    if not isinstance(comments, list) or not comments:
        return {}
    return comments[0] if isinstance(comments[0], dict) else {}


def default_disposition(thread: dict[str, Any], comment: dict[str, Any]) -> tuple[str, str, list[str], str]:
    body = str(comment.get("body") or "").strip()
    if not body:
        return (
            "non_actionable",
            "high",
            ["The frozen comment body is empty."],
            "There is no reviewer claim to evaluate.",
        )
    if not bool(thread.get("is_resolved")):
        return (
            "unresolved",
            "high",
            ["GitHub review-thread metadata records is_resolved=false."],
            "The frozen evidence directly establishes that the thread remained unresolved at export time.",
        )
    evidence = ["GitHub review-thread metadata records is_resolved=true."]
    if bool(thread.get("is_outdated")):
        evidence.append("GitHub records the diff location as outdated.")
    return (
        "uncertain_manual_review_required",
        "high",
        evidence,
        "Thread resolution or an outdated diff location does not prove that the underlying claim was correctly addressed.",
    )


def classify(threads: list[dict[str, Any]], overrides: dict[str, dict[str, Any]]) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[str] = set()
    for index, thread in enumerate(threads, start=1):
        if not isinstance(thread, dict):
            raise SystemExit(f"thread {index} is not an object")
        thread_id = str(thread.get("id") or "")
        pr_number = thread.get("pr_number")
        if not thread_id or not isinstance(pr_number, int):
            raise SystemExit(f"thread {index} lacks stable id or pr_number")
        comment = first_comment(thread)
        comment_id = comment.get("id")
        finding_id = f"PR{pr_number}:{thread_id}"
        if finding_id in seen:
            raise SystemExit(f"duplicate finding id {finding_id}")
        seen.add(finding_id)
        disposition, confidence, evidence, rationale = default_disposition(thread, comment)
        override = overrides.get(finding_id)
        if override:
            disposition = override["disposition"]
            confidence = str(override.get("confidence") or "manual")
            evidence = [str(item) for item in override.get("evidence", [])]
            rationale = str(override.get("rationale") or "Manual decision recorded.")
        if disposition not in ALLOWED:
            raise SystemExit(f"unsupported disposition {disposition}")
        findings.append(
            Finding(
                finding_id=finding_id,
                pr_number=pr_number,
                thread_id=thread_id,
                comment_id=str(comment_id) if comment_id else None,
                path=thread.get("path"),
                line=thread.get("line") or thread.get("original_line"),
                url=comment.get("url"),
                reviewer_claim=str(comment.get("body") or "").strip(),
                github_is_resolved=bool(thread.get("is_resolved")),
                github_is_outdated=bool(thread.get("is_outdated")),
                disposition=disposition,
                confidence=confidence,
                evidence=evidence,
                rationale=rationale,
            )
        )
    unused = sorted(set(overrides) - seen)
    if unused:
        raise SystemExit(f"overrides reference missing findings: {unused}")
    return findings


def markdown_plain_text(value: str) -> str:
    """Render untrusted review Markdown as inert single-line report text."""
    value = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"</?[^>]+>", "", value)
    value = value.replace("`", "'")
    return " ".join(value.split())


def render_markdown(findings: list[Finding], source: Path) -> str:
    counts = Counter(item.disposition for item in findings)
    lines = [
        "# Frozen merged-PR review findings",
        "",
        f"Source: `{source.as_posix()}`",
        "",
        "This report is fail-closed. A resolved GitHub thread is not labeled correctly resolved unless a manual evidence decision proves it.",
        "",
        "## Summary",
        "",
        f"- Total review threads: {len(findings)}",
    ]
    for name in sorted(ALLOWED):
        lines.append(f"- `{name}`: {counts.get(name, 0)}")
    lines.extend(["", "## Findings", ""])
    for item in findings:
        location = item.path or "no file"
        if item.line:
            location += f":{item.line}"
        claim = markdown_plain_text(item.reviewer_claim)
        if len(claim) > 240:
            claim = claim[:237] + "..."
        lines.extend(
            [
                f"### {item.finding_id}",
                "",
                f"- Disposition: `{item.disposition}`",
                f"- Confidence: `{item.confidence}`",
                f"- Location: `{location}`",
                f"- GitHub resolved/outdated: `{item.github_is_resolved}` / `{item.github_is_outdated}`",
                f"- Review URL: {item.url or 'unavailable'}",
                f"- Claim: {claim or '[empty]'}",
                f"- Rationale: {item.rationale}",
                "- Evidence:",
            ]
        )
        lines.extend(f"  - {entry}" for entry in item.evidence)
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threads", type=Path, required=True)
    parser.add_argument("--overrides", type=Path)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    args = parser.parse_args()

    payload = load_json(args.threads)
    if payload.get("schema_version") != 2 or not isinstance(payload.get("threads"), list):
        raise SystemExit("thread inventory must use schema_version=2 and contain a threads list")
    overrides = load_overrides(args.overrides)
    findings = classify(payload["threads"], overrides)
    output = {
        "schema_version": 1,
        "source": args.threads.as_posix(),
        "classification_policy": "fail_closed_v1",
        "counts": dict(sorted(Counter(item.disposition for item in findings).items())),
        "findings": [asdict(item) for item in findings],
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(findings, args.threads) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
