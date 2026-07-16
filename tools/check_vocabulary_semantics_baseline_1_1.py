#!/usr/bin/env python3
"""Validate prospective Vocabulary Semantics Baseline 1.1 without altering prior evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE_JSON = ROOT / "theory/evaluation/comparative-representation/semantics/vocabulary-semantics-baseline-1.1.json"
BASELINE_MD = ROOT / "theory/evaluation/comparative-representation/semantics/vocabulary-semantics-baseline-1.1.md"
EXTENSION = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001"
ORIGINAL_RESULT = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002/execution/cre002-comparison.json"
EXPECTED_ORIGINAL_SHA256 = "d03c37e2d916923f6ca697f6f05f9fa772bb9ba23b8f725f82ef24f3617ff683"
REQUIRED_CONSTRUCTS = {
    "D_nondeterminism",
    "D_concurrency",
    "D_priority",
    "D_provenance",
    "D_rule_modification",
}
VOCABS = {
    "CRE-001-VOCAB-A-1.0",
    "CRE-001-VOCAB-B-1.0",
    "CRE-001-VOCAB-C-1.0",
}
NONCLAIMS = {
    "universal sufficiency",
    "primitive-only sufficiency",
    "necessity",
    "minimality",
    "independence",
    "superiority",
    "FAR proof",
    "universal structure of reasoning",
    "retrospective validation of CRE-002",
    "behavioral success in CRE-002-EXT-001",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    for path in [BASELINE_JSON, BASELINE_MD, EXTENSION / "README.md", EXTENSION / "execution-lock.json", ORIGINAL_RESULT]:
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        print("BASELINE 1.1 CHECK FAILED")
        print("\n".join(errors))
        return 1

    baseline = load(BASELINE_JSON)
    lock = load(EXTENSION / "execution-lock.json")
    original = load(ORIGINAL_RESULT)

    if baseline.get("artifact_id") != "VOCABULARY-SEMANTICS-BASELINE-1.1":
        errors.append("wrong Baseline 1.1 artifact identifier")
    chronology = baseline.get("chronology", {})
    if chronology.get("cannot_reclassify") != "any previously recorded CRE-002 candidate outcome":
        errors.append("Baseline 1.1 does not preserve CRE-002 outcome finality")
    if "CRE-002" not in chronology.get("not_retrospective_evidence_for", []):
        errors.append("Baseline 1.1 omits the non-retrospective CRE-002 boundary")

    constructs = {item.get("identifier") for item in baseline.get("derived_constructs", [])}
    if constructs != REQUIRED_CONSTRUCTS:
        errors.append(f"derived construct set mismatch: {sorted(constructs)}")
    for item in baseline.get("derived_constructs", []):
        if item.get("classification") != "derived":
            errors.append(f"{item.get('identifier')} is not classified as derived")
        if not item.get("formal_definition") or not item.get("required_fields"):
            errors.append(f"{item.get('identifier')} lacks a complete definition")
        if not item.get("operational_constraints") or not item.get("forbidden_imports"):
            errors.append(f"{item.get('identifier')} lacks boundary constraints")

    licensing = baseline.get("vocabulary_licensing", {})
    if set(licensing) != VOCABS:
        errors.append("vocabulary licensing coverage is incomplete")
    for vocab, record in licensing.items():
        if set(record.get("licensed_derived_constructs", [])) != REQUIRED_CONSTRUCTS:
            errors.append(f"{vocab} does not explicitly license all five derived constructs")
        if not record.get("construction_rule") or not record.get("limitation"):
            errors.append(f"{vocab} lacks construction or limitation text")

    if not NONCLAIMS.issubset(set(baseline.get("nonclaims", []))):
        errors.append("Baseline 1.1 omits required nonclaims")
    if baseline.get("scope", {}).get("primitive_only_claim") is not False:
        errors.append("Baseline 1.1 must not make a primitive-only claim")

    if lock.get("execution_permitted") is not False:
        errors.append("CRE-002-EXT-001 execution is not locked")
    if lock.get("compiler_implementation_permitted") is not False:
        errors.append("CRE-002-EXT-001 compiler implementation is not locked")
    if lock.get("official_results_present") is not False:
        errors.append("CRE-002-EXT-001 incorrectly claims results")

    if sha256(ORIGINAL_RESULT) != EXPECTED_ORIGINAL_SHA256:
        errors.append("original CRE-002 result changed after Baseline 1.1 work began")
    if original.get("aggregate", {}).get("unsupported_candidates") != 3:
        errors.append("original CRE-002 unsupported result was reclassified")
    if any(row.get("outcome") != "unsupported" for row in original.get("candidates", [])):
        errors.append("one or more original CRE-002 candidate outcomes changed")

    if errors:
        print("BASELINE 1.1 CHECK FAILED")
        print("\n".join(errors))
        return 1
    print("BASELINE 1.1 CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
