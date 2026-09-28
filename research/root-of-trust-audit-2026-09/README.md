# Root-of-trust audit 2026-09: reproduction evidence

Status: **Research audit evidence; not a validation gate and not theory authority.**

Findings, fixes, and residual limits are recorded in [`docs/audits/root-of-trust-audit-2026-09.md`](../../docs/audits/root-of-trust-audit-2026-09.md). This directory preserves the independent oracles and scripts that support its conclusions, so another reviewer can reproduce them.

## Contents

| Path | What it is | Independence |
|---|---|---|
| `oracle_far_ir_2_0/` | A `far-ir/2.0` oracle with its own stdlib JSON Schema evaluator (ECMA-262 `$`), plus 74 adversarial records with hand-derived expected diagnostics (`adversarial/index.json`). | Derived from the v1.1-bound specification, theory, and schema only. Its author did not read the verifier, checkers, or tests. |
| `oracle_far_ir_2_1/` | A `far-ir/2.1` oracle computing each result by two routes (brute-force and sort-sweep Pareto sets, two least-element and expected-loss computations, two triangle checks), 48 adversarial records, and a seeded random-record generator. | Same restriction for the W5 specification. It uses upstream `jsonschema` and refuses the repository-local validator. |
| `scripts/compare_verifiers.py` | Runs the errata 1 reference verifiers (`contract_v2_errata1`, `contract_v21_errata1`) against both corpora and, optionally, a random corpus. | Reads the oracle expectations; it does not generate them. |
| `scripts/schema_differential.py` | Compares upstream `jsonschema` 4.22.0 with the repository-local validator on every committed document. | Upstream `jsonschema` is independently developed. |
| `scripts/w6_independent_reproduction.py` | Recomputes the W6 result without the W6 checker or the FAR verifier, under three validators. | Uses its own mutation and its own equality (exact rationals). |

The oracles share their authors' reading of the specifications and are Project-FAR-internal. They are logically independent of the implementation. They are not external replication.

## Reproduce

```bash
python research/root-of-trust-audit-2026-09/oracle_far_ir_2_0/run_all.py        # oracle self-consistency
python -m venv /tmp/far-audit && /tmp/far-audit/bin/pip install "jsonschema==4.23.0"
/tmp/far-audit/bin/python research/root-of-trust-audit-2026-09/oracle_far_ir_2_1/run.py
/tmp/far-audit/bin/python research/root-of-trust-audit-2026-09/oracle_far_ir_2_1/gen_random_records.py /tmp/w5-random 4000
python research/root-of-trust-audit-2026-09/scripts/compare_verifiers.py /tmp/w5-random
```

`compare_verifiers.py` reports differences on exactly two `far-ir/2.0` records. Both are deliberate rule changes of `far-ir/2.0` errata 1, which amendment v1.2 binds:

- `ADV-70`: repeated quotient class ids are now rejected with `DUPLICATE_QUOTIENT_CLASS`;
- `ADV-56`: an invalid freeze time is now reported as `FREEZE_TIME_INVALID`.

For `far-ir/2.1` it requires identical verdicts and diagnostic multisets. The 1211 order-only differences on the random corpus come from the oracle's grouped reading of the metric-axiom order. The v1.1 text allowed that reading. `far-ir/2.1` errata 1 now states the reference implementation's interleaved order, which was checked against 1218 records with metric-axiom failures.
