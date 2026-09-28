"""Frozen EFR-U2 three-arm allocation and numerical gates; no site data bundled.

EFR-U2 supersedes EFR-U1 with an active comparator arm (``checker``: native evidence and SOP plus
the neutral case tables and the generic table-consistency report). The primary contrast is the
comparator-arm minus FAR-arm escaped-defect proportion. A missing FAR output counts as an escaped
defect; a missing comparator or standard output counts as not escaped, so missing FAR data can
never manufacture a FAR-specific benefit. Harm and protocol-validity gates remain separate
adjudicated findings.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

SITES = ("S01", "S02", "S03")
ARMS = ("far", "checker", "standard")
PER_ARM = 20
PER_SITE = PER_ARM * len(ARMS)


def _digest(data: bytes, expected: str, label: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError(f"{label} SHA-256 must be 64 lowercase hexadecimal digits")
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f"sealed {label} digest mismatch")


def allocate(roster_bytes: bytes, roster_sha256: str) -> dict:
    _digest(roster_bytes, roster_sha256, "site-roster manifest")
    data = json.loads(roster_bytes)
    if data.get("test_id") != "EFR-U2":
        raise ValueError("site-roster manifest must declare test_id EFR-U2; EFR-U1 inputs are not accepted")
    rng = random.Random(int(roster_sha256[:16], 16))
    allocation = {}
    for site in SITES:
        record = data["sites"][site]
        workers = record["workers"]
        if not workers or len(set(workers)) != len(workers) or len(workers) > 40:
            raise ValueError(f"{site}: between 1 and 40 distinct workers required")
        expected = [f"{site}-{index:03d}" for index in range(1, PER_SITE + 1)]
        assignments = record["assignments"]
        if sorted(assignments) != expected:
            raise ValueError(f"{site}: exactly {PER_SITE} consecutive investigation assignments required")
        for index, investigation in enumerate(expected):
            if assignments[investigation] != workers[index % len(workers)]:
                raise ValueError(f"{site}: assignment of {investigation} violates the cyclic worker rule")
        slots = [arm for arm in ARMS for _ in range(PER_ARM)]
        rng.shuffle(slots)
        allocation[site] = dict(zip(expected, slots))
    return {"test_id": "EFR-U2", "roster_manifest_sha256": roster_sha256, "allocation": allocation}


def _rate(ids, escaped, weights, assigned):
    numerator = denominator = 0
    for case_id in ids:
        weight = weights[assigned[case_id]]
        numerator += weight * escaped[case_id]
        denominator += weight
    if not denominator:
        return None
    return Fraction(numerator, denominator)


def _conservative(rate, arm):
    """Zero-weight resample: worst case for FAR, best case for every comparison arm.

    v1.0 invalidated the whole test on any zero denominator; with realistic rosters that makes a
    correctly run study INVALID by resampling chance alone (about half the time at ten workers
    per site). This preregistered rule instead resolves the resample against FAR, so chance can
    only make a FAR-specific pass harder. No resample is discarded or redrawn.
    """
    if rate is not None:
        return rate
    return Fraction(1) if arm == "far" else Fraction(0)


def analyze(roster_bytes, roster_sha256, outcomes_bytes, outcomes_sha256):
    allocation = allocate(roster_bytes, roster_sha256)["allocation"]
    _digest(outcomes_bytes, outcomes_sha256, "outcomes")
    data = json.loads(roster_bytes)
    outcomes = json.loads(outcomes_bytes)
    if outcomes.get("roster_manifest_sha256") != roster_sha256:
        raise ValueError("outcomes refer to another site-roster manifest")
    recorded = {}
    for row in outcomes["investigations"]:
        if row["id"] in recorded or row["escaped_defect"] not in (True, False, None):
            raise ValueError("duplicate investigation or invalid escaped_defect value")
        recorded[row["id"]] = row["escaped_defect"]
    expected = {case for site in SITES for case in allocation[site]}
    if set(recorded) != expected:
        raise ValueError("every allocated investigation requires a row, including missing outputs")
    arm_of = {case: arm for site in SITES for case, arm in allocation[site].items()}
    escaped = {case: int(value if value is not None else arm_of[case] == "far")
               for case, value in recorded.items()}
    assigned = {case: worker for site in SITES
                for case, worker in data["sites"][site]["assignments"].items()}
    ids = {(site, arm): sorted(c for c, a in allocation[site].items() if a == arm)
           for site in SITES for arm in ARMS}
    unit = Counter({worker: 1 for worker in assigned.values()})
    observed = {(s, a): _rate(ids[s, a], escaped, unit, assigned) for s in SITES for a in ARMS}
    if any(value is None for value in observed.values()):
        raise ValueError("observed arm has no investigations")
    primary = sum(observed[s, "checker"] - observed[s, "far"] for s in SITES) / 3
    checker_rate = sum(observed[s, "checker"] for s in SITES) / 3
    site_reductions = {s: observed[s, "checker"] - observed[s, "far"] for s in SITES}
    rng = random.Random(int(roster_sha256[:16], 16))
    samples = {"primary": [], "checker_vs_standard": [], "far_vs_standard": []}
    zero_denominator_resamples = 0
    for resample in range(10000):
        degenerate = False
        rates = {}
        for site in SITES:
            workers = sorted(data["sites"][site]["workers"])
            weights = Counter(workers[rng.randrange(len(workers))] for draw in range(len(workers)))
            for arm in ARMS:
                drawn = [ids[site, arm][rng.randrange(PER_ARM)] for draw in range(PER_ARM)]
                rate = _rate(drawn, escaped, weights, assigned)
                degenerate = degenerate or rate is None
                rates[site, arm] = _conservative(rate, arm)
        zero_denominator_resamples += degenerate
        samples["primary"].append(sum(rates[s, "checker"] - rates[s, "far"] for s in SITES) / 3)
        samples["checker_vs_standard"].append(sum(rates[s, "standard"] - rates[s, "checker"] for s in SITES) / 3)
        samples["far_vs_standard"].append(sum(rates[s, "standard"] - rates[s, "far"] for s in SITES) / 3)
    bounds = {}
    for name, bucket in samples.items():
        bucket.sort()
        bounds[name] = [bucket[249], bucket[9749]]
    relative_ok = checker_rate > 0 and primary / checker_rate >= Fraction(1, 5)
    passed = (primary >= Fraction(1, 20) and relative_ok and bounds["primary"][0] > 0
              and all(value >= -Fraction(1, 20) for value in site_reductions.values()))
    return {
        "test_id": "EFR-U2",
        "roster_manifest_sha256": roster_sha256,
        "outcomes_sha256": outcomes_sha256,
        "numerical_disposition": "NUMERICAL_GATES_PASS" if passed else "NUMERICAL_GATES_FAIL",
        "harm_and_protocol_validity_still_required": True,
        "primary": {"far_specific_escaped_defect_reduction": str(primary),
                    "relative_to_checker": str(primary / checker_rate) if checker_rate else None,
                    "percentile_bounds": [str(x) for x in bounds["primary"]],
                    "site_reductions": {s: str(v) for s, v in site_reductions.items()}},
        "secondary_descriptive": {name: [str(x) for x in bounds[name]]
                                  for name in ("checker_vs_standard", "far_vs_standard")},
        "resamples": 10000,
        "zero_denominator_resamples": zero_denominator_resamples,
        "zero_denominator_rule": "far rate 1, checker/standard rate 0 (conservative against FAR); never discarded or redrawn",
        "interval": "nominal crossed site-worker/investigation perturbation; no exact coverage claim",
    }


def main():
    if sys.version_info[:2] != (3, 12) or len(sys.argv) != 5:
        raise SystemExit("Python 3.12 required: efr_u2_analysis.py ROSTER ROSTER_SHA256 OUTCOMES OUTCOMES_SHA256")
    result = analyze(Path(sys.argv[1]).read_bytes(), sys.argv[2], Path(sys.argv[3]).read_bytes(), sys.argv[4])
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
