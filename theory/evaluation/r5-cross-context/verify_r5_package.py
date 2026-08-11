#!/usr/bin/env python3
"""Verifier for the R5 cross-context replication package.

RESTRICTED: this file names the banned terms in order to detect them. It must
never be delivered to a Role A respondent.

Enforces, mechanically:
  1. blinding  - registered participant-facing text contains no registered
                 banned identifiers, paraphrases, or field seeds;
  2. structure - every required artifact exists and parses;
  3. state     - the package declares protocol-frozen, evidence-not-collected,
                 and registers no run and no result.

This is a lexical verifier, not proof of absent semantic leakage.
Exit code 0 = PASS, 1 = FAIL. Run from the repository root or anywhere.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent

# Files delivered to, or readable by, a Role A respondent. These packet bodies
# are subject to the blinding check; additional authorized strings are registered
# separately in participant-surface-v1.1.json and are also checked.
PARTICIPANT_FACING = [
    "elicitation-packet-A-v1.0.md",
    "elicitation-packet-B1-reword-v1.1.md",
    "elicitation-packet-B2-ablation-v1.1.md",
]

# The participant-facing surface is NOT only the packet bodies. Every string the
# protocol authorizes anyone to send Role A before reveal is registered in
# participant-surface-v1.1.json and is checked here. An earlier revision modelled
# only packet sections 2-3, which left the fallback clarification unchecked.
SURFACE_REGISTRY = "participant-surface-v1.1.json"

# In the packets the delivered material begins at section 2. Packet A has a
# retained-for-record section 4; B1/B2 end after their delivered section 3.
DELIVERED_START = "## 2."
DELIVERED_END = "## 4."

# Minimum plausible size of the delivered span, in characters. Guards against a
# future edit silently reducing the scanned text to nothing.
MIN_DELIVERED_CHARS = 600

# 17 frozen payload artifacts. The verifier itself is tooling, listed separately
# in TOOLING, and is hashed by the manifest but is not a payload artifact.
REQUIRED_ARTIFACTS = [
    "README.md",
    "participant-surface-v1.1.json",
    "target-pin-v1.1.json",
    "preregistration-v1.0.json",
    "elicitation-packet-A-v1.0.md",
    "elicitation-packet-B1-reword-v1.1.md",
    "elicitation-packet-B2-ablation-v1.1.md",
    "contamination-questionnaire-v1.0.json",
    "role-a-output-schema-v1.0.json",
    "freeze-procedure-v1.0.md",
    "reveal-packet-v1.0.md",
    "normalization-mapping-schema-v1.0.json",
    "adjudication-procedure-v1.0.md",
    "outcome-registry-v1.0.json",
    "evidence-tier-rules-v1.0.json",
    "provenance-manifest-v1.0.json",
    "package-audit-v1.0.md",
]

TOOLING = ["verify_r5_package.py"]
JSON_ARTIFACTS = [a for a in REQUIRED_ARTIFACTS if a.endswith(".json")]

# Literal identifiers that must not appear in delivered text.
BANNED_LITERALS = [
    "Project FAR", "CDRR", "C*", "P*", "E*", "OP-21", "LIM-031",
    "IKD-", "USD-", "TUE-", "contract frontier", "preservation basis",
    "faithful representation", "admissibility structure",
]

# Short acronyms and bare tokens. These MUST be word-boundary matched: a
# substring scan for "UPP" fires inside "supplied", and one for "FARE" fires
# inside "welfare". Substring matching on short acronyms produces false
# positives that mask real leaks by training the reader to ignore the check.
BANNED_TOKENS = [
    "far", "fara", "faro", "farm", "fare", "rccd",
    "upp", "g1", "g2", "g3",
]

# Registered semantic paraphrases of the programme's own vocabulary. These are
# banned as lexical watchlist items; the verifier does not claim that all possible
# semantic paraphrases have been enumerated.
BANNED_PARAPHRASES = [
    "commitment", "commitments",
    "admissibility", "admissible",
    "ground", "grounds", "justificatory",
    "stake", "stakes",
    "calculus",
    "candidate primitive", "primitives",
    "supersession", "superseded",
    "provenance",
    "preservation contract", "preservation requirement",
    "reasoning calculus", "investigation",
    "construct", "differentiate", "restrict", "resolve",
    "invariant architecture", "minimal architecture",
    "uniform recovery", "machinery closure", "charged machinery",
]

# Terms whose appearance would seed the respondent's literature search with the
# fields the prior internal comparison used.
BANNED_FIELD_SEEDS = [
    "blackwell", "garbling", "van glabbeek", "branching time",
    "institution", "satisfaction condition", "abstract interpretation",
    "galois connection", "nerode", "myhill", "kalman", "minimal realization",
    "coalgebra", "final coalgebra", "bisimulation", "testing equivalence",
    "full abstraction", "de nicola", "hennessy", "cousot", "rutten",
    "goguen", "burstall", "meseguer",
]


def delivered_text(path: Path) -> tuple[str, str | None]:
    """Return the delivered span of a packet, plus an error if it looks wrong."""
    text = path.read_text(encoding="utf-8")
    start = text.find(DELIVERED_START)
    if start == -1:
        return "", f"{path.name}: no delivered section found (expected {DELIVERED_START!r})"
    end = text.find(DELIVERED_END, start)
    if end == -1:
        # No retained-for-record section. Scan to end of file. Over-scanning is
        # the FAIL-SAFE direction: extra text checked can only add findings,
        # whereas under-scanning silently hides leaks.
        end = len(text)
    span = text[start:end]
    if len(span) < MIN_DELIVERED_CHARS:
        return span, (f"{path.name}: delivered span is only {len(span)} chars, "
                      f"below the {MIN_DELIVERED_CHARS}-char floor; the blinding check "
                      f"would pass vacuously")
    return span, None


def scan(text: str, needles: list[str], *, word_boundary: bool) -> list[str]:
    hits = []
    low = text.lower()
    for needle in needles:
        if word_boundary:
            if re.search(rf"\b{re.escape(needle.lower())}\b", low):
                hits.append(needle)
        elif needle.lower() in low:
            hits.append(needle)
    return hits


def main() -> int:
    failures: list[str] = []

    # 1. structure
    for name in REQUIRED_ARTIFACTS:
        if not (PKG / name).is_file():
            failures.append(f"MISSING ARTIFACT: {name}")

    for name in JSON_ARTIFACTS:
        path = PKG / name
        if path.is_file():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                failures.append(f"INVALID JSON: {name}: {exc}")

    # 2. blinding, against delivered packet text
    for name in PARTICIPANT_FACING:
        path = PKG / name
        if not path.is_file():
            continue
        text, span_error = delivered_text(path)
        if span_error:
            failures.append(f"DELIVERED-SPAN ERROR: {span_error}")
        for label, needles, wb in (
            ("BANNED LITERAL", BANNED_LITERALS, False),
            ("BANNED TOKEN", BANNED_TOKENS, True),
            ("BANNED PARAPHRASE", BANNED_PARAPHRASES, True),
            ("FIELD SEED", BANNED_FIELD_SEEDS, False),
        ):
            for hit in scan(text, needles, word_boundary=wb):
                failures.append(f"{label} in delivered text of {name}: {hit!r}")

    # 2b. participant-facing SURFACE: every registered string, fail closed
    surface_path = PKG / SURFACE_REGISTRY
    registered_strings: list[tuple[str, str]] = []
    if not surface_path.is_file():
        failures.append(f"MISSING SURFACE REGISTRY: {SURFACE_REGISTRY}")
    else:
        surface = json.loads(surface_path.read_text(encoding="utf-8"))
        for group, entries in surface["surface"].items():
            for entry in entries:
                if "exact_string" in entry:
                    registered_strings.append((entry["id"], entry["exact_string"]))
                elif "file" in entry and entry["file"] not in PARTICIPANT_FACING:
                    failures.append(
                        f"SURFACE ENTRY {entry['id']} names {entry['file']!r}, which is not in PARTICIPANT_FACING")
        for sid, text in registered_strings:
            for label, needles, wb in (
                ("BANNED LITERAL", BANNED_LITERALS, False),
                ("BANNED TOKEN", BANNED_TOKENS, True),
                ("BANNED PARAPHRASE", BANNED_PARAPHRASES, True),
                ("FIELD SEED", BANNED_FIELD_SEEDS, False),
            ):
                for hit in scan(text, needles, word_boundary=wb):
                    failures.append(f"{label} in registered surface string {sid}: {hit!r}")

        # fail closed: any quoted fallback in a packet must be registered
        for name in PARTICIPANT_FACING:
            path = PKG / name
            if not path.is_file():
                continue
            body = path.read_text(encoding="utf-8")
            for quoted in re.findall(r'reply only[^\n]*?[*>"]\s*([^*"\n][^*"\n]{20,})', body):
                cleaned = quoted.strip().strip('*">').strip()
                if cleaned and not any(cleaned in reg for _, reg in registered_strings):
                    failures.append(
                        f"UNREGISTERED PARTICIPANT-FACING STRING in {name}: {cleaned[:70]!r}")

    # 3. state: protocol frozen, nothing executed
    prereg_path = PKG / "preregistration-v1.0.json"
    if prereg_path.is_file():
        prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
        if prereg.get("status") != "PROTOCOL_FROZEN_EVIDENCE_NOT_YET_COLLECTED":
            failures.append("preregistration status is not PROTOCOL_FROZEN_EVIDENCE_NOT_YET_COLLECTED")
        if prereg.get("execution_authorized") is not False:
            failures.append("preregistration declares execution authorized")

    registry_path = PKG / "outcome-registry-v1.0.json"
    if registry_path.is_file():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        if registry.get("runs_recorded") != 0:
            failures.append("outcome registry records runs; nothing has been executed")

    if (PKG / "runs").exists():
        failures.append("a runs/ directory exists; this package must contain no executed run")

    if failures:
        print("FAIL")
        for line in failures:
            print(f"  - {line}")
        return 1

    print("PASS")
    print(f"  artifacts: {len(REQUIRED_ARTIFACTS)} present and parsing")
    n_terms = len(BANNED_LITERALS) + len(BANNED_TOKENS) + len(BANNED_PARAPHRASES) + len(BANNED_FIELD_SEEDS)
    print(f"  blinding:  {len(PARTICIPANT_FACING)} packet bodies + {len(registered_strings)} registered surface "
          f"strings clean against {n_terms} watchlist terms")
    print("             (lexical check only; absence of watchlist terms is NOT proof of no semantic leakage)")
    print("  state:     protocol frozen, no run recorded, no result registered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
