"""Frozen EFR-HD2 three-arm allocation; no observations or participant data are bundled.

EFR-HD2 supersedes EFR-HD1 by adding an active comparator arm (``checker``) that receives the
generic table-consistency report instead of the FAR verifier report. For case index c (0-119)
and arm index k (far=0, checker=1, standard=2), reviewers occupy roster positions
(c + 20k + j) mod 60 for j = 0..5. Because 120 is a multiple of 60, every case gets exactly six
ratings per arm, every reviewer makes exactly 12 decisions per arm on 36 distinct cases, no
reviewer sees a case in two arms, and each of the six arm orders is used by exactly ten reviewers.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from itertools import permutations
from pathlib import Path

DOMAINS = (
    "argumentation", "bayesian_causal", "formal_logic",
    "model_based_reasoning", "proof_theory", "type_theory",
)
CLASSES = ("material_loss", "preservation")
ARMS = ("far", "checker", "standard")
REVIEWERS = 60
ARM_OFFSET = 20
CASES = 120
RATINGS_PER_CASE_PER_ARM = 6
ARM_ORDERS = tuple(permutations(ARMS))  # six orders, counterbalanced by position mod 6


def allocate(manifest_bytes: bytes, manifest_sha256: str) -> dict:
    if not re.fullmatch(r"[0-9a-f]{64}", manifest_sha256):
        raise ValueError("manifest SHA-256 must be 64 lowercase hexadecimal digits")
    if hashlib.sha256(manifest_bytes).hexdigest() != manifest_sha256:
        raise ValueError("sealed input manifest digest mismatch")
    data = json.loads(manifest_bytes)
    if data.get("test_id") != "EFR-HD2":
        raise ValueError("input manifest must declare test_id EFR-HD2; EFR-HD1 inputs are not accepted")
    reviewers = data["reviewers"]
    cases = data["cases"]
    ids = [case["id"] for case in cases]
    if len(reviewers) != REVIEWERS or len(set(reviewers)) != REVIEWERS:
        raise ValueError("exactly 60 distinct reviewers required")
    if len(ids) != CASES or len(set(ids)) != CASES:
        raise ValueError("exactly 120 distinct case IDs required")
    if any(not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9._-]+", value)
           for value in reviewers + ids):
        raise ValueError("IDs must use only ASCII letters, digits, dot, underscore, or dash")
    if any(case["domain"] not in DOMAINS or case["class"] not in CLASSES for case in cases):
        raise ValueError("unregistered domain or class")
    rng = random.Random(int(manifest_sha256[:16], 16))
    ordered_cases = []
    for domain in DOMAINS:
        for label in CLASSES:
            stratum = sorted(case["id"] for case in cases
                             if case["domain"] == domain and case["class"] == label)
            if len(stratum) != 10:
                raise ValueError("each domain/class stratum must contain exactly ten cases")
            rng.shuffle(stratum)
            ordered_cases.extend(stratum)
    roster = sorted(reviewers)
    rng.shuffle(roster)
    rows = [{"reviewer_id": reviewer, "position": position,
             "arm_order": list(ARM_ORDERS[position % len(ARM_ORDERS)]),
             "tasks": {arm: [] for arm in ARMS}}
            for position, reviewer in enumerate(roster)]
    for index, case_id in enumerate(ordered_cases):
        for arm_index, arm in enumerate(ARMS):
            for offset in range(RATINGS_PER_CASE_PER_ARM):
                rows[(index + ARM_OFFSET * arm_index + offset) % REVIEWERS]["tasks"][arm].append(case_id)
    for row in rows:
        for arm in ARMS:
            seed_bytes = f"{manifest_sha256}\nEFR-HD2\n{row['reviewer_id']}\n{arm}\n".encode("ascii")
            seed = int(hashlib.sha256(seed_bytes).hexdigest()[:16], 16)
            tasks = sorted(row["tasks"][arm])
            random.Random(seed).shuffle(tasks)
            row["tasks"][arm] = tasks
    return {"test_id": "EFR-HD2", "input_manifest_sha256": manifest_sha256,
            "allocation": rows}


def main() -> int:
    if sys.version_info[:2] != (3, 12):
        raise SystemExit("EFR-HD2 allocation requires the frozen Python 3.12 runtime")
    if len(sys.argv) != 3:
        raise SystemExit("usage: python tools/efr_hd2_allocation.py sealed-input.json EXPECTED_SHA256")
    manifest_bytes = Path(sys.argv[1]).read_bytes()
    result = allocate(manifest_bytes, sys.argv[2])
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
