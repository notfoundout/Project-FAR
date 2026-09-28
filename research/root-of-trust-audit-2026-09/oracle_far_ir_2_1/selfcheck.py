"""Deterministic randomized self-check of the oracle's dual computational routes.

For N random schema-valid records derived from the frontier fixture (random reference
weights incl. zero mass, aggregation, tolerance incl. 0, decoders, tied/incomparable
costs, random metrics on extra values) this:
  * runs verify(), whose internal asserts compare brute-force vs sweep Pareto,
    brute-force vs meet-based least, case-wise vs representation-grouped expected loss,
    L==0 vs all-mass-on-beta exactness, and exhaustive-triple vs relaxation triangle;
  * re-verifies with claims set to the recomputed sets and requires [] (claim closure);
  * requires ZERO_TOLERANCE_EXACT_BOUNDARY_FAILURE never fires (it is provably dead).
"""
from __future__ import annotations

import copy
import json
import random
import sys
from fractions import Fraction

sys.path.insert(0, __import__("pathlib").Path(__file__).resolve().parent.as_posix())
from oracle import ROOT, contract_sha256, verify  # noqa: E402

BASE = json.loads((ROOT / "conformance/far-ir-2.1/valid-frontier.json").read_text())
rng = random.Random(20260925)


def rand_dist(k):
    """Random exact distribution over k items with small denominators (some zeros)."""
    den = rng.choice([1, 2, 3, 4, 6, 10])
    cuts = sorted(rng.randint(0, den) for _ in range(k - 1))
    parts = [b - a for a, b in zip([0] + cuts, cuts + [den])]
    return [Fraction(p, den) for p in parts]


def s(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


N = 3000
stats = dict(records=0, accepted=0, metric_rejects=0, tol0=0, tol0_zero_mass=0, no_least_with_pareto=0)
for i in range(N):
    r = copy.deepcopy(BASE)
    a = r["contract"]["approximation"]
    w = rand_dist(2)
    a["reference"]["weights"][0]["weight"], a["reference"]["weights"][1]["weight"] = s(w[0]), s(w[1])
    a["aggregation"] = rng.choice(["expected", "maximum"])
    a["tolerance"] = rng.choice(["0", "0", "1/4", "1/3", "1/2", "2/3", "1"])
    if rng.random() < 0.3:  # random metric on extra values (may violate axioms)
        vals = [False, True, "x", "y"]
        d = {}
        for l in vals:
            for rr in vals:
                if (l, rr) in {(False, False), (True, True)}:
                    d[(l, rr)] = "0"
                elif {l, rr} == {False, True}:
                    d[(l, rr)] = "1"
                else:
                    d[(l, rr)] = rng.choice(["0", "1/4", "1/2", "1", "2"])
        a["metric"] = {"kind": "finite_table_metric", "values": vals,
                       "entries": [{"left": l, "right": rr, "distance": d[(l, rr)]} for l in vals for rr in vals]}
    ev = r["report"]["evidence"]
    ev["candidates"] = []
    for j in range(rng.randint(1, 6)):
        rows = []
        for rv in ("r0", "r1"):
            p = rand_dist(2)
            rows.append({"representation_value": rv, "distribution": [
                {"action": False, "probability": s(p[0])}, {"action": True, "probability": s(p[1])}]})
        ev["candidates"].append({"id": f"c{j}", "decoder_table": rows, "costs": [
            {"dimension_id": "storage", "value": str(rng.randint(0, 3))},
            {"dimension_id": "evaluation", "value": str(rng.randint(0, 3))}]})
    r["freeze"]["contract_sha256"] = contract_sha256(r["contract"])
    res = verify(r)  # internal dual-route asserts run here
    stats["records"] += 1
    assert "ZERO_TOLERANCE_EXACT_BOUNDARY_FAILURE" not in res.codes
    if any(c.startswith("METRIC_") for c in res.codes):
        stats["metric_rejects"] += 1
        continue
    det = res.detail
    ev["claimed_feasible"], ev["claimed_pareto_minimal"] = det["feasible"], det["pareto"]
    ev["claimed_least_elements"], ev["exact_recovery_claims"] = det["least"], det["exact_recovery"]
    again = verify(r)
    assert again.codes == [], (i, again.codes)
    stats["accepted"] += 1
    if a["tolerance"] == "0":
        stats["tol0"] += 1
        stats["tol0_zero_mass"] += "0" in (a["reference"]["weights"][0]["weight"], a["reference"]["weights"][1]["weight"])
    stats["no_least_with_pareto"] += bool(det["pareto"]) and not det["least"]
print(json.dumps(stats))
