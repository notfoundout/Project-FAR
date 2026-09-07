# EFR-001 R2 input-specification amendment v1.1

Amendment ID: `EFR-001-R2-INPUT-AMENDMENT-1.1`

Program: `EXTERNAL-FALSIFICATION-AND-REPLICATION-001` (`EFR-001`)

Status: **PREREGISTERED AMENDMENT — NOT EXECUTED**

Date: 2026-09-07

Machine authority: [`external-falsification-and-replication-r2-input-amendment-v1.1.json`](../../theory/evaluation/external-falsification-and-replication-r2-input-amendment-v1.1.json)

Amends: the **`EFR-R2` input specification only** in [External Falsification and Replication Program v1.0](external-falsification-and-replication-program-v1.0.md).

## 1. What this amendment does and does not touch

The frozen EFR v1.0 program is **preserved byte-for-byte**. This amendment modifies no frozen artifact, no endpoint, no threshold, no sample or stratum count, no inclusion/exclusion rule, no allocation, no missing-data rule, and no analysis. It supersedes exactly one thing: **which specification bytes constitute the permitted `EFR-R2` input package**.

Every other registered test — `EFR-R1`, `H1`, `A1`, `HD1`, `U1`, `C1`, `N1` — is untouched, as are the program decision rule and the aggregate label.

The nine content-addressed v1.0 artifact objects are verified unmodified by `tests/test_efr_r2_input_amendment.py`, which fails closed if any frozen blob drifts.

## 2. The preregistration defect

`EFR-R2` requires two clean-room implementations to agree with each other and the frozen expected result on **every required item**, comparing outcome, **error category**, and recomputed evidence, using only the published W3/W5 specifications.

At registration those specifications did not determine error category:

- the `far-ir/2.0` verifier emits 26 diagnostic codes and the `far-ir/2.1` verifier emits 41; the published specifications named exactly one of them (`W5_SEMANTICS_NOT_ESTABLISHED`);
- two `far-ir/2.1` codes are composed at runtime as `DUPLICATE_{label}` and appear as no source literal anywhere;
- diagnostics are an ordered sequence with multiplicity, which the specifications did not state;
- **suppression was unstated**: both verifiers accumulate into one shared diagnostic sequence and abandon later checks when that sequence is non-empty for any reason, so an unrelated cross-field defect suppresses the claim-specific check entirely.

The last item is decisive. A record carrying both a `FREEZE_HASH_MISMATCH` and a genuine decoder error yields exactly `[FREEZE_HASH_MISMATCH]` under the canonical verifier. An implementer following the previously published prose would reasonably emit both codes and mismatch.

`EFR-R2` was therefore **unsatisfiable for specification reasons unrelated to `far-ir` semantics**. Two correct clean-room implementations could not have converged. This is a defect in the registered input, not a finding about Project FAR's comparison semantics.

## 3. Mandatory consequence

`EFR-001` v1.0 states that later intake may supply only identities, dates, sources, and observations, and permits **no later scientific design choices**. Which specification bytes a clean-room team receives is such a design choice.

Therefore:

> **`EFR-R2` MUST NOT execute against the corrected specifications under the unamended v1.0 freeze.** Executing R2 under v1.0 while handing teams the corrected specifications would make the test retrospectively specified and forfeits its confirmatory status.

`EFR-R2` may execute only under this amendment, whose bound bytes are fixed in §5 before any team is enrolled. This is a determinate requirement, not a discretionary judgement for the program owner.

The amendment must be promoted to protected `main` before any R2 team is enrolled or any R2 input is sealed; the promotion event supplies its authoritative freeze timestamp, exactly as for v1.0.

## 4. Canonical R2 state before this correction

The correction is prospective with respect to the **canonical EFR authorities**. At the time of amendment those authorities machine-record all of the following:

| Evidence | Recorded value |
|---|---|
| `EFR-R2` status in the program ledger | `PREREGISTERED_NOT_EXECUTED` |
| All eight registered test statuses | `PREREGISTERED_NOT_EXECUTED` |
| `EFR-R2` input slot in the v1.0 input freeze | `EMPTY_AWAITING_INDEPENDENT_CUSTODIAN_SEAL` |
| `current_results.tests_executed` | `0` |
| `current_results.external_cases` | `0` |

`tests/test_efr_r2_input_amendment.py` checks those five facts directly against the frozen program and input-freeze records and fails closed if they cease to match while this amendment still describes the pre-execution state.

These checks prove what the repository can prove: **the canonical EFR state contained no sealed R2 input, executed R2 test, or recorded external case before the specification correction.** They do not prove the global nonexistence of unregistered external files, communications, private experiments, or other activity outside the canonical EFR intake. This amendment therefore makes no such claim. Any such undisclosed activity, if it existed, would be evaluated under the v1.0 exposure/protocol-breach rules rather than silently treated as absent.

## 5. Bound corrected input specification

The permitted `EFR-R2` specification package is exactly these bytes, bound by git blob object identity under the same semantics v1.0 uses (blob IDs bind exact bytes including the blob header):

| Path | Role |
|---|---|
| `docs/specification/far-ir-2.0-contract.md` | W3 comparison-contract specification, including the §9 diagnostic vocabulary and §9.7–§9.8 sequence/suppression semantics |
| `docs/specification/far-ir-2.1-approximation-cost.md` | W5 approximation/cost specification, including its diagnostic vocabulary and gate semantics |
| `schemas/far-contract-v2.schema.json` | `far-ir/2.0` schema, unchanged from the v1.0 baseline |
| `schemas/far-contract-v2.1.schema.json` | `far-ir/2.1` schema, unchanged from the v1.0 baseline |

Exact blob identities are recorded in the machine authority. Both schema blobs are **identical to the v1.0 baseline**; only the two specification documents differ.

The permitted package is specification-and-schema only. The v1.0 prohibition is unchanged and still binding: clean-room teams may not use Project FAR verifier, checker, test, oracle, or other implementation source, generated expected outputs, or another team's code. `mechanization/far_mechanization/diagnostic_vocabulary.py` remains an internal repository consistency declaration referenced by the specifications, but it is **not** part of the R2 clean-room input package because the specifications already publish the complete diagnostic tables.

## 6. What this amendment does not establish

Correcting an input specification is not evidence about Project FAR. This amendment does not execute `EFR-R2`, does not make its acceptance more likely, and does not establish external independence, replication, novelty, empirical utility, or any assurance upgrade. `EFR-R2` remains `PREREGISTERED_NOT_EXECUTED`, and `OP-28` remains open.

Whether the corrected specification is in fact sufficient for two independent implementations to converge is exactly what `EFR-R2` tests. That question is open, and this amendment must not be read as answering it.
