# far-ir/2.1 Specification Errata 1

Status: **Accepted successor corrections to the frozen `far-ir/2.1` specification; additive, no frozen byte changed**

Corrects: [`far-ir-2.1-approximation-cost.md`](far-ir-2.1-approximation-cost.md) (git blob `cec3368e426c4220010fe25f7058710dc9bb5017`, bound by `EFR-001-R2-INPUT-AMENDMENT-1.1`), which is unchanged

Reference and current verifier: [`mechanization/far_mechanization/contract_v21_errata1.py`](../../mechanization/far_mechanization/contract_v21_errata1.py)

Source: [root-of-trust audit 2026-09](../audits/root-of-trust-audit-2026-09.md)

## Why this page exists

The diagnostic sequence is normative: an independent implementation must reproduce code, multiplicity, and order. The 2026-09 root-of-trust audit found two ways in which the `far-ir/2.1` reference and text failed to fix that sequence:

- The executed verifier iterates required-behavior values as a Python set in the loss checks. A record with more than one `METRIC_LOSS_DOMAIN_MISMATCH` or `LOSS_METRIC_MISMATCH` therefore reports them in an order that varies with `PYTHONHASHSEED`.
- The Stage 2 text reads as grouping the metric-axiom codes by code, but the reference interleaves them. An oracle written only from the specification disagreed with the reference on order for 1211 of 4000 random records.

Neither the text nor the verifier can be edited in place. `EFR-001-R2-INPUT-AMENDMENT-1.1` binds the specification by git blob. The completed `PCA-W5` manifest pins the executed verifier [`contract_v21.py`](../../mechanization/far_mechanization/contract_v21.py) by SHA-256, and W5 is recomputed from those bytes. This page records the corrections as successor material. Read together with the frozen specification, they define `far-ir/2.1` as corrected by errata 1.

## E1. Evaluation order, Stage 2

Replace the Stage 2 paragraph. Values are identified by canonical JSON as defined in [`far-ir/2.0` errata 1](far-ir-2.0-errata-1.md), E3.

**Stage 2 — reference, metric, loss, cost dimensions.** Codes are appended in this order:

1. `DUPLICATE_REFERENCE_CASE`, `REFERENCE_COVERAGE_MISMATCH`, `REFERENCE_NOT_PROBABILITY`, `DUPLICATE_METRIC_VALUE`, `DUPLICATE_METRIC_ENTRY`.
2. Either `METRIC_NOT_TOTAL`, which suppresses all four metric-axiom checks, or the metric-axiom checks. These are interleaved, not grouped by code. For each distinct declared metric value `l` in first-occurrence order:
   - `METRIC_IDENTITY_FAILURE` if `d(l, l) != 0`;
   - then, for each distinct value `r` in the same order, `METRIC_SYMMETRY_FAILURE` if `d(l, r) != d(r, l)`, and `METRIC_SEPARATION_FAILURE` if `l != r` and `d(l, r) == 0`;
   - each followed, for each distinct value `m` in the same order, by `METRIC_TRIANGLE_FAILURE` if `d(l, r) > d(l, m) + d(m, r)`.

   An asymmetric pair is therefore reported once from each side.
3. `DUPLICATE_LOSS_ACTION`, `DUPLICATE_LOSS_ENTRY`, `LOSS_NOT_TOTAL`.
4. The loss checks. For each distinct required-behavior value in first-occurrence order of `required_behavior.table` rows, and within it each distinct declared action in first-occurrence order: `METRIC_LOSS_DOMAIN_MISMATCH` if that (truth, action) pair is not a metric pair, otherwise `LOSS_METRIC_MISMATCH` if its loss entry differs from the metric distance.
5. Finally, `DUPLICATE_COST_DIMENSION`.

The metric-axiom order in step 2 is what the executed verifier already does, so it is a clarification of the text. The loss-check order in step 4 is a correction: the reference verifier `contract_v21_errata1` runs the executed verifier unchanged and puts only those loss-check diagnostics into this order. Every other diagnostic and every success or failure outcome is the executed verifier's.

## Effect on existing records

The executed and corrected verifiers can differ only in the relative order of two or more loss-check diagnostics in one record. No governed `PCA-W5` record has such diagnostics: the W5 checker requires the corrected verifier to reproduce every governed record's executed diagnostic sequence. `tests/test_far_contract_v21_determinism.py` shows that the executed order varies with `PYTHONHASHSEED` and the corrected order does not.

## Nonclaims

These errata add no diagnostic code. They do not change the `far-ir/2.1` schema, the frozen specification or verifier bytes, any frozen record, any recorded campaign result, or any claim status. They do not establish that the corrected text is sufficient for independent convergence, which is what `EFR-R2` tests.
