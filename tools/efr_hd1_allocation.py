"""Frozen EFR-HD1 allocation; no observations or participant data are bundled."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import random
import re
import sys

DOMAINS = (
    "argumentation", "bayesian_causal", "formal_logic",
    "model_based_reasoning", "proof_theory", "type_theory",
)
CLASSES = ("material_loss", "preservation")
ARMS = ("far", "standard")


def allocate(manifest_sha256: str, reviewers: list[str], cases: list[dict]) -> dict:
    if not re.fullmatch(r"[0-9a-f]{64}", manifest_sha256):
        raise ValueError("manifest SHA-256 must be 64 lowercase hexadecimal digits")
    ids = [case["id"] for case in cases]
    if len(reviewers) != 24 or len(set(reviewers)) != 24:
        raise ValueError("exactly 24 distinct reviewers required")
    if len(ids) != 120 or len(set(ids)) != 120:
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
             "arm_order": list(ARMS if position % 2 == 0 else reversed(ARMS)),
             "tasks": {arm: [] for arm in ARMS}}
            for position, reviewer in enumerate(roster)]
    for index, case_id in enumerate(ordered_cases):
        for offset in range(6):
            rows[(index + offset) % 24]["tasks"]["far"].append(case_id)
            rows[(index + 12 + offset) % 24]["tasks"]["standard"].append(case_id)
    for row in rows:
        for arm in ARMS:
            seed_bytes = f"{manifest_sha256}\nEFR-HD1\n{row['reviewer_id']}\n{arm}\n".encode("ascii")
            seed = int(hashlib.sha256(seed_bytes).hexdigest()[:16], 16)
            tasks = sorted(row["tasks"][arm])
            random.Random(seed).shuffle(tasks)
            row["tasks"][arm] = tasks
    return {"test_id": "EFR-HD1", "input_manifest_sha256": manifest_sha256,
            "allocation": rows}


def main() -> int:
    if sys.version_info[:2] != (3, 12):
        raise SystemExit("EFR-HD1 allocation requires the frozen Python 3.12 runtime")
    if len(sys.argv) != 2:
        raise SystemExit("usage: python tools/efr_hd1_allocation.py sealed-input.json")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = allocate(data["manifest_sha256"], data["reviewers"], data["cases"])
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
