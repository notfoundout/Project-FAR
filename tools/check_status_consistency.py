#!/usr/bin/env python3
"""Detect cross-document status contradictions without modifying sources."""
from __future__ import annotations

import argparse
import math
import re
import string
from dataclasses import dataclass
from pathlib import Path
from itertools import combinations

ROOT = Path(__file__).resolve().parents[1]

RESOLVED = {"established", "established conditional", "completed", "supported", "not supported"}
UNRESOLVED = {"research", "active", "pending", "undetermined", "open"}
STOPWORDS = {"a", "an", "and", "are", "be", "can", "current", "does", "is", "of", "one", "or", "the", "to", "under", "within", "without", "with"}
SIMILARITY_THRESHOLD = 0.60

@dataclass(frozen=True)
class StatusRecord:
    source_path: str
    source_class: str
    line_start: int
    line_end: int
    explicit_id: str | None
    title: str
    raw_status: str | None
    normalized_status: str

    @property
    def category(self) -> str:
        return status_category(self.normalized_status)


def normalize_status(raw: str | None) -> str:
    text = re.sub(r"[,.]", "", (raw or "missing").strip().lower())
    text = re.sub(r"\s+", " ", text)
    if "established" in text and "conditional" in text:
        return "established conditional"
    if "established" in text:
        return "established"
    for status in ["completed", "supported", "not supported", "research", "active", "pending", "undetermined", "open"]:
        if status in text:
            return status
    return text or "missing"


def status_category(normalized: str) -> str:
    if normalized in RESOLVED:
        return "resolved"
    if normalized in UNRESOLVED:
        return "unresolved"
    return "unknown"


def title_tokens(title: str) -> set[str]:
    table = str.maketrans({c: " " for c in string.punctuation})
    words = title.lower().translate(table).split()
    out = set()
    for word in words:
        if word in STOPWORDS:
            continue
        if len(word) > 3 and word.endswith("ies"):
            word = word[:-3] + "y"
        elif len(word) > 3 and word.endswith("s"):
            word = word[:-1]
        if word not in STOPWORDS:
            out.add(word)
    return out


def title_similarity(a: str, b: str) -> float:
    ta, tb = title_tokens(a), title_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / math.sqrt(len(ta) * len(tb))



def title_scope(title: str) -> str:
    tokens = title_tokens(title)
    if "global" in tokens:
        return "global"
    if "conditional" in tokens:
        return "conditional"
    return "broad"


def scope_compatible_for_fallback(a: StatusRecord, b: StatusRecord) -> bool:
    scopes = {title_scope(a.title), title_scope(b.title)}
    if "conditional" in scopes and scopes != {"conditional"}:
        return False
    if "global" in scopes and scopes != {"global"}:
        return False
    return True

def _record(path: Path, cls: str, line: int, title: str, status: str | None, explicit_id: str | None = None) -> StatusRecord:
    return StatusRecord(str(path.relative_to(ROOT)) if path.is_absolute() and path.is_relative_to(ROOT) else str(path), cls, line, line, explicit_id, title.strip(), status.strip() if status else None, normalize_status(status))


def parse_theorem_registry(path: Path = ROOT / "theory/theorems/theorems.md") -> list[StatusRecord]:
    lines = path.read_text(encoding="utf-8").splitlines()
    records = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"##\s+(T-\d+)\s+[—-]\s+(.+)", line)
        if not m:
            continue
        explicit_id, title = m.groups()
        status = None
        for j in range(i, min(len(lines), i + 25)):
            sm = re.match(r"Status:\s*(.+)", lines[j])
            if sm:
                status = sm.group(1)
                break
        records.append(_record(path, "theorem", i, title, status, explicit_id))
    return records


def parse_investigation(path: Path) -> list[StatusRecord]:
    lines = path.read_text(encoding="utf-8").splitlines()
    inv_id = None; title = None; status = None; line_no = 1
    for i, line in enumerate(lines, 1):
        if line.strip() == "## Investigation ID" and i < len(lines):
            inv_id = next((l.strip() for l in lines[i:] if l.strip() and not l.startswith("---")), None)
        if line.strip() == "## Title" and i < len(lines):
            title = next((l.strip() for l in lines[i:] if l.strip() and not l.startswith("---")), None); line_no = i
        if line.strip() == "## Status" and i < len(lines):
            status = next((l.strip() for l in lines[i:] if l.strip() and not l.startswith("---")), None)
    if title or status or inv_id:
        return [_record(path, "investigation", line_no, title or path.stem, status, inv_id)]
    return []


def parse_open_questions(path: Path = ROOT / "research/open-problems/open-questions.md") -> list[StatusRecord]:
    lines = path.read_text(encoding="utf-8").splitlines()
    records = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"##\s+(.+)", line)
        if not m or m.group(1).lower() == "purpose":
            continue
        title = m.group(1).strip()
        status = None
        for j in range(i, min(len(lines), i + 20)):
            sm = re.match(r"\*\*Status:\*\*\s*(.+)", lines[j])
            if sm:
                status = sm.group(1); break
            if j > i and lines[j].startswith("## "):
                break
        records.append(_record(path, "open_question", i, title, status))
    return records


def parse_records(root: Path = ROOT) -> list[StatusRecord]:
    records = parse_theorem_registry(root / "theory/theorems/theorems.md")
    inv_dir = root / "research/validation/investigations"
    for path in sorted(inv_dir.glob("*.md")):
        records.extend(parse_investigation(path))
    records.extend(parse_open_questions(root / "research/open-problems/open-questions.md"))
    return records


def match_reason(a: StatusRecord, b: StatusRecord) -> tuple[str, float] | None:
    if a.source_class == b.source_class:
        return None
    if a.explicit_id and b.explicit_id and a.explicit_id == b.explicit_id:
        return ("explicit-id", 1.0)
    # explicit cross-reference by ID in title/status text
    blob_a = f"{a.title} {a.raw_status or ''}".lower(); blob_b = f"{b.title} {b.raw_status or ''}".lower()
    if a.explicit_id and a.explicit_id.lower() in blob_b:
        return ("explicit-cross-reference", 1.0)
    if b.explicit_id and b.explicit_id.lower() in blob_a:
        return ("explicit-cross-reference", 1.0)
    if re.sub(r"\s+", " ", a.title.lower()).strip() == re.sub(r"\s+", " ", b.title.lower()).strip():
        return ("exact-title", 1.0)
    score = title_similarity(a.title, b.title)
    if score >= SIMILARITY_THRESHOLD and scope_compatible_for_fallback(a, b):
        return ("fallback-title-similarity", score)
    return None


def find_contradictions(records: list[StatusRecord]) -> list[dict[str, object]]:
    findings = []
    for a, b in combinations(records, 2):
        reason = match_reason(a, b)
        if not reason:
            continue
        if {a.category, b.category} == {"resolved", "unresolved"}:
            findings.append({"a": a, "b": b, "reason": reason[0], "score": reason[1]})
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-only", "--allow-findings", action="store_true", dest="report_only")
    args = ap.parse_args()
    records = parse_records()
    findings = find_contradictions(records)
    print("Status Consistency Report")
    print(f"Records parsed: {len(records)}")
    print(f"Contradictions: {len(findings)}")
    for f in findings:
        a = f["a"]; b = f["b"]
        print(f"- {a.title} <-> {b.title}")
        print(f"  match: {f['reason']} score={f['score']:.2f}")
        print(f"  {a.source_class}: {a.normalized_status} (raw: {a.raw_status}) at {a.source_path}:{a.line_start}")
        print(f"  {b.source_class}: {b.normalized_status} (raw: {b.raw_status}) at {b.source_path}:{b.line_start}")
    return 0 if args.report_only or not findings else 1

if __name__ == "__main__":
    raise SystemExit(main())
