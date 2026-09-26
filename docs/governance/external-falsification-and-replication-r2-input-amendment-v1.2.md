# EFR-001 R2 input-specification amendment v1.2

Amendment ID: `EFR-001-R2-INPUT-AMENDMENT-1.2`

Program: `EXTERNAL-FALSIFICATION-AND-REPLICATION-001` (`EFR-001`)

Status: **PREREGISTERED AMENDMENT — NOT EXECUTED (candidate until promoted to protected `main`)**

Date: 2026-09-26

Machine authority: [`external-falsification-and-replication-r2-input-amendment-v1.2.json`](../../theory/evaluation/external-falsification-and-replication-r2-input-amendment-v1.2.json)

Supersedes: the bound specification package of [amendment v1.1](external-falsification-and-replication-r2-input-amendment-v1.1.md). The v1.1 amendment and every byte it binds are preserved unmodified, and those bytes stay in the v1.2 package.

Layered on: [comparator amendment v2.0](external-falsification-and-replication-comparator-amendment-v2.0.md), preserved unmodified.

Amends: the **`EFR-R2` input specification only** in [External Falsification and Replication Program v1.0](external-falsification-and-replication-program-v1.0.md).

## 1. What this amendment does and does not touch

Every earlier object is **preserved byte-for-byte**: the frozen EFR v1.0 program, amendment v1.1 and its bound package, comparator amendment v2.0, and the verifiers they name. The machine authority binds each by git blob.

This amendment modifies no frozen artifact, endpoint, threshold, sample or stratum count, inclusion/exclusion rule, allocation, missing-data rule, or analysis. It supersedes exactly one thing: **which specification bytes constitute the permitted `EFR-R2` input package**. It does so by adding two versioned errata documents to the unchanged v1.1-bound bytes.

The registered tests after comparator amendment v2.0 are `EFR-R1`, `EFR-H1`, `EFR-A1`, `EFR-HD2`, `EFR-U2`, `EFR-C2`, and `EFR-N1`. None of them is amended, and neither is the aggregate rule or the v2.0 H1/A1 execution binding. The v2.0 aggregate rule names `EFR-R2 (v1.1)`; under this amendment `EFR-R2` is evaluated against the v1.2 package, and no other term of that rule changes. `EFR-HD1`, `EFR-U1`, and `EFR-C1` remain `SUPERSEDED_NOT_EXECUTABLE` under v2.0.

## 2. The defect in the v1.1-bound input

`EFR-R2` requires two clean-room implementations to agree with each other and with the frozen expected result on every required item. The 2026-09 [root-of-trust audit](../audits/root-of-trust-audit-2026-09.md) compared the reference verifiers with oracles derived only from the v1.1-bound specifications. It found that the reference itself was defective or nondeterministic on some records, and that the bound text still left some reference outputs undetermined:

- the `far-ir/2.0` reference identified quotient classes by id, so a repeated class id merged two declared classes: a split partition was certified `PROVED` as the exact observational quotient, and an exact partition with a repeated id was rejected, contrary to §3.3;
- overlapping classes produced class-relation diagnostics computed from an arbitrary assignment instead of `QUOTIENT_NOT_PARTITION`, contrary to that code's published definition;
- the reference intake accepted `NaN`/`Infinity` and resolved duplicate object keys last-wins, so a record that a first-wins JSON parser reads as `REFUTED` was certified `PROVED`;
- a `FROZEN` record with a null or non-RFC3339 `frozen_at` was accepted, although §5 requires an RFC3339 time;
- the `far-ir/2.1` reference ordered `METRIC_LOSS_DOMAIN_MISMATCH` and `LOSS_METRIC_MISMATCH` by Python set iteration, so its normative sequence varied with `PYTHONHASHSEED`;
- the `far-ir/2.1` text read as grouping metric-axiom codes, while the reference interleaves them; a specification-derived oracle disagreed with the reference on order for 1211 of 4000 random records;
- canonical JSON for `contract_sha256`, table-value equality, and quotient pair iteration order were unspecified.

Under v1.1, correct clean-room implementations could therefore disagree with the frozen expected result. The reasons would be defects of the reference or ambiguities of the bound text, not properties of `far-ir` semantics.

## 3. Mandatory consequence

> **`EFR-R2` MUST NOT execute against the v1.2-corrected specifications under amendment v1.1 or the unamended v1.0 freeze.** Which specification bytes a clean-room team receives is a scientific design choice that `EFR-001` v1.0 does not permit later intake to make.

This amendment must be promoted to protected `main` before any R2 team is enrolled or any R2 input is sealed; the promotion event supplies its authoritative freeze timestamp. This is a determinate requirement, not a discretionary judgement for the program owner.

## 4. Canonical R2 state before this correction

At the time of amendment the canonical EFR authorities still record:

- `EFR-R2` and every other registered test as `PREREGISTERED_NOT_EXECUTED`;
- the `EFR-R2` input slot as `EMPTY_AWAITING_INDEPENDENT_CUSTODIAN_SEAL`;
- zero executed tests and zero external cases.

`tests/test_efr_r2_input_amendment_v12.py` checks these facts against the frozen program and input-freeze records.

These checks prove what the repository can prove. They do not prove the global nonexistence of unregistered external files, communications, private experiments, or other activity outside the canonical EFR intake, and this amendment makes no such claim.

## 5. Bound corrected input specification

The permitted `EFR-R2` specification package is exactly these bytes, bound by git blob object identity in the machine authority:

| Path | Role | Provenance |
|---|---|---|
| `docs/specification/far-ir-2.0-contract.md` | W3 comparison-contract specification, including the §9 diagnostic vocabulary and sequence/suppression semantics | unchanged from v1.1 |
| `docs/specification/far-ir-2.0-errata-1.md` | `far-ir/2.0` errata 1: class identity, value equality, RFC 8259 intake, canonical JSON, freeze-time check, and the corrected quotient and Stage 2 order | added by v1.2 |
| `docs/specification/far-ir-2.1-approximation-cost.md` | W5 approximation/cost specification, including its diagnostic vocabulary and gate semantics | unchanged from v1.1 |
| `docs/specification/far-ir-2.1-errata-1.md` | `far-ir/2.1` errata 1: exact metric-axiom and loss-check order | added by v1.2 |
| `schemas/far-contract-v2.schema.json` | `far-ir/2.0` schema | unchanged from the v1.0 baseline |
| `schemas/far-contract-v2.1.schema.json` | `far-ir/2.1` schema | unchanged from the v1.0 baseline |

The permitted package is specification-and-schema only. The v1.0 prohibition is unchanged and still binding: clean-room teams may not use Project FAR verifier, checker, test, oracle, or other implementation source, generated expected outputs, or another team's code.

## 6. Reference verifiers for the frozen expected result

Any `EFR-R2` frozen expected result must be generated by the reference verifiers that implement the v1.2 package. The machine authority binds them by git blob:

- [`contract_v2_errata1.py`](../../mechanization/far_mechanization/contract_v2_errata1.py) for `far-ir/2.0`. It wraps the unchanged frozen baseline `contract_v2.py`.
- [`contract_v21_errata1.py`](../../mechanization/far_mechanization/contract_v21_errata1.py) for `far-ir/2.1`. It wraps the unchanged executed `PCA-W5` verifier `contract_v21.py`.

They are implementation source and are never supplied to clean-room teams.

Current verification rule v1.1 ([`contract_v2_strict_v11`](../specification/far-ir-2.0-current-verification.md)) adds a determinate-outcome rule. That rule is not part of the `far-ir/2.0` specification or its errata, so it is not an `EFR-R2` input.

## 7. What this amendment does not establish

Correcting an input specification is not evidence about Project FAR. This amendment does not:

- execute `EFR-R2` or make its acceptance more likely;
- establish that the errata reference verifiers are correct beyond the audited defects;
- establish external independence, replication, novelty, empirical utility, or any assurance upgrade;
- move the comparator amendment v2.0 execution binding off current verification rule v1.0.

`EFR-R2` remains `PREREGISTERED_NOT_EXECUTED`, and `OP-28` remains open.
