#!/usr/bin/env python3
"""Run the independent far-ir/2.0 oracle over:
  A. the registered conformance suite (conformance/far-ir-2.0/manifest.json);
  B. supplementary far-ir/2.0 records under research/results/pca-w4-domain-contracts/;
  C. the hand-derived adversarial corpus (audit_oracle_v2/adversarial/index.json),
     under the default reading and every recorded alternative reading.
Also cross-checks each accepted/rejected claim against the partition-lattice layer.
Exit status is non-zero if any oracle output differs from a hand-derived expectation.
"""
import dataclasses
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import oracle  # noqa: E402

ROOT = oracle.ROOT
HERE = pathlib.Path(__file__).resolve().parent


def run(path, opts=oracle.DEFAULT):
    codes = oracle.diagnose_path(path, opts)
    problems = []
    if codes not in (["UNREADABLE_CONTRACT"],) and "SCHEMA_CONSTRAINT_VIOLATION" not in codes:
        doc = oracle.parse_json_text(path.read_text("utf-8"), opts)
        problems = oracle.cross_check(doc, codes, opts)
    return codes, problems


def fmt(codes):
    return "[]" if not codes else "[" + ", ".join(codes) + "]"


def main():
    failures = 0

    print("== A. Registered conformance suite conformance/far-ir-2.0 ==")
    man = json.loads((ROOT / "conformance/far-ir-2.0/manifest.json").read_text("utf-8"))
    for case in man["cases"]:
        codes, probs = run(ROOT / "conformance/far-ir-2.0" / case["path"])
        ok = codes == case["expected_codes"] and (not codes) == case["expected_valid"]
        failures += (not ok) + len(probs)
        print(f"{case['id']} {case['path']}: oracle={'accept' if not codes else 'reject'} {fmt(codes)} "
              f"declared={'accept' if case['expected_valid'] else 'reject'} {fmt(case['expected_codes'])} "
              f"{'AGREE' if ok else 'DISAGREE'}{' XCHECK:' + str(probs) if probs else ''}")

    print("\n== B. Supplementary far-ir/2.0 records (PCA-W4 domain contracts; not conformance fixtures) ==")
    wdir = ROOT / "research/results/pca-w4-domain-contracts"
    wman = json.loads((wdir / "manifest.json").read_text("utf-8"))
    for rec in wman["records"]:
        p = ROOT / rec["path"]
        codes, probs = run(p)
        doc = json.loads(p.read_text("utf-8"))
        rep = doc["report"]
        file_hash_ok = hashlib.sha256(p.read_bytes()).hexdigest() == rec["sha256"]
        decl_ok = rep["outcome"] == rec["expected_outcome"] and rep["evidence"]["kind"] == rec["expected_evidence"]
        m = oracle.mathematics(doc) if not codes else {}
        extra = ""
        if m.get("applicable"):
            extra = f" factorizable={m['factorizable']} collisions={len(m['collisions'])} beta_blocks={m['beta_blocks']}"
        failures += bool(codes) + len(probs)
        print(f"{p.name}: oracle={'accept' if not codes else 'reject'} {fmt(codes)} "
              f"record={rep['outcome']}/{rep['evidence']['kind']}/{rep['evidence'].get('status')} "
              f"manifest_match={decl_ok} file_sha256_match={file_hash_ok}{extra}"
              f"{' XCHECK:' + str(probs) if probs else ''}")

    print("\n== C. Adversarial corpus audit_oracle_v2/adversarial ==")
    idx = json.loads((HERE / "adversarial/index.json").read_text("utf-8"))
    for case in idx["cases"]:
        p = HERE / "adversarial" / case["file"]
        codes, probs = run(p)
        ok = codes == case["expected_codes"]
        alt_notes = []
        for alt in case["alternatives"]:
            aopts = dataclasses.replace(oracle.DEFAULT, **alt["options"])
            acodes, aprobs = run(p, aopts)
            aok = acodes == alt["expected_codes"]
            failures += (not aok) + len(aprobs)
            alt_notes.append(f"{alt['options']}->{fmt(acodes)}{'' if aok else ' MISMATCH'}")
        failures += (not ok) + len(probs)
        flag = " [verdict ambiguous]" if case["verdict_interpretation_dependent"] else (
            " [count/order ambiguous]" if case["codes_interpretation_dependent"] else "")
        print(f"{case['id']} {'accept' if not codes else 'reject'} {fmt(codes)} expected={fmt(case['expected_codes'])} "
              f"{'OK' if ok else 'MISMATCH'}{flag}{' alts: ' + '; '.join(alt_notes) if alt_notes else ''}"
              f"{' XCHECK:' + str(probs) if probs else ''}")

    print(f"\nTOTAL MISMATCHES/INCONSISTENCIES: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
