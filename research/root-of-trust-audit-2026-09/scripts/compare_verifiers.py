"""Compare the errata reference verifiers with the specification-derived oracles' expectations.

    python research/root-of-trust-audit-2026-09/scripts/compare_verifiers.py [W5_RANDOM_DIR]

Reports, for the far-ir/2.0 corpus (expectations derived from the v1.1-bound specification before
the repairs), every verdict or code difference; the deliberate v1.2 rule changes are listed in the
audit report. For the far-ir/2.1 corpus and an optional random corpus from
oracle_far_ir_2_1/gen_random_records.py, it requires identical verdicts and code multisets.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

# The frozen far-ir/2.0 and far-ir/2.1 verifiers are unchanged; errata 1 is implemented by these successors.
from mechanization.far_mechanization import contract_v2_errata1, contract_v21_errata1  # noqa: E402

V12_RULE_CHANGES = {"ADV-27", "ADV-56", "ADV-70"}


def codes(module, path: Path) -> list[str]:
    return [diagnostic.code for diagnostic in module.load_and_validate(path).diagnostics]


def main() -> int:
    failures = 0
    index = json.loads((HERE / "oracle_far_ir_2_0/adversarial/index.json").read_text())["cases"]
    for case in index:
        actual = codes(contract_v2_errata1, HERE / "oracle_far_ir_2_0/adversarial" / case["file"])
        options = [case["expected_codes"]] + [a.get("expected_codes", a) if isinstance(a, dict) else a for a in case.get("alternatives", [])]
        if actual in options:
            continue
        verdict_differs = all((not actual) != (not option) for option in options)
        tag = "v1.2-rule-change" if case["id"] in V12_RULE_CHANGES else ("VERDICT" if verdict_differs else "codes")
        failures += tag == "VERDICT" and case["id"] not in V12_RULE_CHANGES
        print(f"far-ir/2.0 {case['id']} [{tag}] {case['defect_class']}: actual={actual} spec-v1.1-oracle={case['expected_codes']}")
    expected21 = json.loads((HERE / "oracle_far_ir_2_1/adversarial/expected.json").read_text())
    items = expected21
    for item in items:
        actual = codes(contract_v21_errata1, HERE / "oracle_far_ir_2_1" / item["file"])
        if actual != item["expected"]:
            alternative = any(actual == option["codes"] for option in item.get("alternatives", []))
            failures += not alternative
            print(f"far-ir/2.1 {item['name']} [{'alternative-reading' if alternative else 'MISMATCH'}]: actual={actual} oracle={item['expected']}")
    print(f"far-ir/2.0 corpus: {len(index)} records; far-ir/2.1 corpus: {len(items)} records")
    if len(sys.argv) > 1:
        verdicts = multisets = orders = total = 0
        for path in sorted(Path(sys.argv[1]).glob("*.json")):
            actual = codes(contract_v21_errata1, path)
            oracle = json.loads(path.with_suffix(".oracle").read_text())
            total += 1
            verdicts += (not actual) != (not oracle)
            multisets += Counter(actual) != Counter(oracle)
            orders += actual != oracle
        failures += verdicts + multisets
        print(f"far-ir/2.1 random: {total} records; verdict differences {verdicts}; multiset differences {multisets}; "
              f"order-only differences {orders - multisets} (the oracle groups metric-axiom codes; see audit report)")
    print("RESULT:", "FAIL" if failures else "PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
