"""Generate seeded random far-ir/2.1 records and this oracle's expected diagnostics.

Run under a Python with upstream jsonschema (the oracle refuses the repository-local validator):
    python gen_random_records.py OUT_DIR 4000
Each record r#####.json is written with r#####.oracle holding the oracle's code sequence. Claims are
either the oracle-recomputed sets (70%) or random subsets, so claim-set mismatch checks are exercised.
"""
import copy, json, random, sys, pathlib
from fractions import Fraction
sys.path.insert(0, pathlib.Path(__file__).resolve().parent.as_posix())
from oracle import ROOT, contract_sha256, verify  # noqa: E402

out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); N = int(sys.argv[2])
BASE = json.loads((ROOT / "conformance/far-ir-2.1/valid-frontier.json").read_text())
rng = random.Random(777)


def rd(k):
    den = rng.choice([1, 2, 3, 4, 6, 10]); cuts = sorted(rng.randint(0, den) for _ in range(k - 1))
    return [Fraction(b - a, den) for a, b in zip([0] + cuts, cuts + [den])]


def s(q):
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


for i in range(N):
    r = copy.deepcopy(BASE); a = r["contract"]["approximation"]
    w = rd(2); a["reference"]["weights"][0]["weight"], a["reference"]["weights"][1]["weight"] = s(w[0]), s(w[1])
    a["aggregation"] = rng.choice(["expected", "maximum"]); a["tolerance"] = rng.choice(["0", "1/4", "1/3", "1/2", "2/3", "1"])
    if rng.random() < 0.3:
        vals = [False, True, "x", "y"]; d = {}
        for left in vals:
            for right in vals:
                same = left is right or (left == right and type(left) is type(right))
                d[(left, right)] = "0" if same else ("1" if {left, right} == {False, True} else rng.choice(["0", "1/4", "1/2", "1", "2"]))
        a["metric"] = {"kind": "finite_table_metric", "values": vals, "entries": [{"left": l, "right": rr, "distance": d[(l, rr)]} for l in vals for rr in vals]}
    ev = r["report"]["evidence"]; ev["candidates"] = []
    for j in range(rng.randint(1, 6)):
        rows = []
        for rv in ("r0", "r1"):
            p = rd(2); rows.append({"representation_value": rv, "distribution": [{"action": False, "probability": s(p[0])}, {"action": True, "probability": s(p[1])}]})
        ev["candidates"].append({"id": f"c{j}", "decoder_table": rows, "costs": [{"dimension_id": "storage", "value": str(rng.randint(0, 3))}, {"dimension_id": "evaluation", "value": str(rng.randint(0, 3))}]})
    r["freeze"]["contract_sha256"] = contract_sha256(r["contract"])
    res = verify(r)
    if not any(c.startswith("METRIC_") for c in res.codes):
        det = res.detail; ids = [c["id"] for c in ev["candidates"]]
        for field, key in (("claimed_feasible", "feasible"), ("claimed_pareto_minimal", "pareto"), ("claimed_least_elements", "least"), ("exact_recovery_claims", "exact_recovery")):
            ev[field] = det[key] if rng.random() < 0.7 else sorted(rng.sample(ids, rng.randint(0, len(ids))))
    (out / f"r{i:05d}.json").write_text(json.dumps(r))
    (out / f"r{i:05d}.oracle").write_text(json.dumps(verify(r).codes))
