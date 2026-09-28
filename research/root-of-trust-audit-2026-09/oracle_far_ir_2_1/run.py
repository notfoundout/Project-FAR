"""Run the independent W5 oracle over the registered fixtures and the adversarial corpus.

Usage (from the repository root):  python3 audit_oracle_w5/run.py [-v]
Exit status 0 iff every expectation (default reading and every declared alternative
reading) matches the oracle.
"""
from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from oracle import ROOT, Interp, verify  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
VERBOSE = "-v" in sys.argv

FIXTURES = {
    "conformance/far-ir-2.1/valid-frontier.json": [],
    "conformance/far-ir-2.1/valid-zero-boundary.json": [],
    "research/results/pca-w5-approximation-and-cost/frontier.json": [],
}

failures = 0


def show(label, res):
    det = res.detail
    print(f"  {label}: codes={res.codes}")
    if "candidates" in det:
        for cid, v in det["candidates"].items():
            print(f"    {cid:13s} L={v['case_loss']} agg={v['aggregate']} feasible={v['feasible']} "
                  f"exact={v['exact']} cost={v['cost']}")
        print(f"    feasible={det['feasible']} pareto={det['pareto']} least={det['least']} "
              f"exact_recovery={det['exact_recovery']}")


print("== Registered W5 records ==")
for rel, want in FIXTURES.items():
    res = verify(json.loads((ROOT / rel).read_text()))
    ok = res.codes == want
    failures += not ok
    print(f"[{'PASS' if ok else 'FAIL'}] {rel}")
    show("oracle", res)

print("\n== Adversarial corpus ==")
index = json.loads((HERE / "adversarial/expected.json").read_text())
for item in index:
    rec = json.loads((HERE / item["file"]).read_text())
    res = verify(rec)
    ok = res.codes == item["expected"]
    alt_results = []
    for alt in item["alternatives"]:
        ares = verify(rec, Interp(**alt["interp"]))
        a_ok = ares.codes == alt["codes"]
        ok = ok and a_ok
        alt_results.append((alt["interp"], ares.codes, a_ok))
    failures += not ok
    print(f"[{'PASS' if ok else 'FAIL'}] {item['name']}: expected={item['expected']} got={res.codes}")
    for interp, codes, a_ok in alt_results:
        print(f"         alt {interp} -> {codes} {'ok' if a_ok else 'MISMATCH'}")
    if VERBOSE or not ok:
        show("detail", res)

# Float shadow of the tolerance boundary trap (demonstrates why exact arithmetic matters).
f_agg = 0.5 * (4 / 5 * 0 + 1 / 5 * 1) + 0.5 * (2 / 5 * 1 + 3 / 5 * 0)
print(f"\nbinary64 shadow of tolerance_boundary_float_trap: {f_agg!r} <= 0.3 is {f_agg <= 0.3}")
print(f"binary64 shadow of 99999999999999999/10^17: {99999999999999999 / 10**17!r}")

print(f"\n{len(index)} adversarial records, {len(FIXTURES)} registered records, failures={failures}")
sys.exit(1 if failures else 0)
