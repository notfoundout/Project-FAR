# far-ir/2.0 Specification Errata 1

Status: **Accepted successor corrections to the frozen `far-ir/2.0` specification; additive, no frozen byte changed**

Corrects: [`far-ir-2.0-contract.md`](far-ir-2.0-contract.md) (git blob `4dbc3d8e5fa42d0397c58b6719b764f1ce003d7e`, bound by `EFR-001-R2-INPUT-AMENDMENT-1.1`), which is unchanged

Reference verifier: [`mechanization/far_mechanization/contract_v2_errata1.py`](../../mechanization/far_mechanization/contract_v2_errata1.py)

Current verifier: [`contract_v2_strict_v11.py`](../../mechanization/far_mechanization/contract_v2_strict_v11.py), under the [current verification rule](far-ir-2.0-current-verification.md)

Source: [root-of-trust audit 2026-09](../audits/root-of-trust-audit-2026-09.md)

## Why this page exists

The 2026-09 root-of-trust audit compared the `far-ir/2.0` reference verifier with an oracle written only from the specification. The reference verifier certified a split partition as the exact quotient, accepted non-JSON input, and accepted a non-RFC3339 freeze time. The text also left canonical JSON, value equality, and quotient pair order undetermined.

The specification and its verifier cannot be edited in place. `EFR-001-R2-INPUT-AMENDMENT-1.1` binds the specification by git blob. The verifier [`contract_v2.py`](../../mechanization/far_mechanization/contract_v2.py) is git-blob pinned as the preregistered `PCA-W6` protocol base and is named as the `EFR-001` v1.0 baseline command. This page records the corrections as successor material instead. Read together with the frozen specification, they define `far-ir/2.0` as corrected by errata 1.

A section below replaces or extends only the part it names. Everything else in the frozen specification is unchanged.

## E1. §3 — unchecked evidence and value equality

Add to §3:

Evidence declared `DECLARED_UNCHECKED` is not recomputed. Validation success for such a record certifies only that the record is well formed; its `outcome` remains an unverified declaration, not a checked result.

Two table values are equal exactly when their canonical JSON serializations (E3) are identical. Equality is therefore typed and textual: `1`, `1.0`, `true`, and `"1"` are four distinct values, and strings are compared by code point without Unicode normalization.

## E2. §3.3 — quotient class identity

Add to §3.3:

The classes are the declared `classes` entries, identified by position. Class identifiers must be unique. A repeated identifier is rejected rather than read as one merged class, because merging would let a split partition be certified as the exact quotient. Overlapping classes are not a partition.

## E3. §5 — canonical JSON

Canonical JSON in §5 is exactly the UTF-8 encoding of Python `json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)` applied to the parsed value. That means:

- object keys are sorted by code point;
- there is no insignificant whitespace;
- non-ASCII characters are emitted literally, not `\u`-escaped;
- numbers written without a fraction or exponent are kept as exact decimal integers;
- numbers written with a fraction or exponent are parsed as IEEE-754 doubles and emitted in Python's shortest round-trip `repr` form, so `1.0` stays `1.0` and `1e2` becomes `100.0`.

It is not RFC 8785 (JCS), whose number and escaping rules differ.

The §5 requirement that a `FROZEN` record carries an RFC3339 freeze time is now checked; see E5.

## E4. §9.1 — document intake

Replace the two §9.1 rows:

| Code | Emitted when |
|---|---|
| `UNREADABLE_CONTRACT` | The file cannot be read or is not RFC 8259 JSON. This includes the non-JSON constants `NaN`, `Infinity`, and `-Infinity`, and any object with a repeated member name, whose meaning RFC 8259 leaves parser-dependent. |
| `SCHEMA_CONSTRAINT_VIOLATION` | The document violates `far-contract-v2.schema.json`, or an in-memory document contains a non-finite number, which no JSON document can contain. An in-memory non-finite number yields exactly one such diagnostic and nothing else. Otherwise it is emitted once per schema error, ordered by JSON path then message. |

## E5. §9.5 and §9.6 — additional codes

Add to §9.5:

| Code | Emitted when |
|---|---|
| `DUPLICATE_QUOTIENT_CLASS` | A declared class reuses the identifier of an earlier declared class. |

In §9.5, `QUOTIENT_NOT_PARTITION` is emitted when the declared classes do not partition `source_domain`: some case is missing, some listed case is not in the domain, or classes overlap.

Add to §9.6, immediately before `FREEZE_HASH_MISMATCH`:

| Code | Emitted when |
|---|---|
| `FREEZE_TIME_INVALID` | Freeze status is `FROZEN` and `frozen_at` is not an RFC3339 date-time (§5). JSON Schema `format` is an annotation, so this is checked here. |

The declaration authority for these two codes is `FAR_IR_2_0_ERRATA_1_DIAGNOSTIC_CODES` in [`diagnostic_vocabulary.py`](../../mechanization/far_mechanization/diagnostic_vocabulary.py).

## E6. §9.8 — evaluation order

**Stage 2.** `FREEZE_TIME_INVALID` is appended after `DUPLICATE_TRANSFORMATION` and before `FREEZE_HASH_MISMATCH`, which becomes step 9 of the Stage 2 order.

**Within §9.5 quotient**, replacing the frozen rule:

1. For each declared class in order, append `DUPLICATE_QUOTIENT_CLASS` if its identifier repeats an earlier class identifier.
2. Then, for the same class, append `QUOTIENT_OVERLAP` for each of its cases already listed in an earlier class.
3. After all classes, append `QUOTIENT_NOT_PARTITION` if coverage differs from `source_domain` or any overlap occurred. This stops the check immediately.
4. Otherwise, visit every ordered pair `(x, y)`, with `x` iterating over `source_domain.cases` in order as the outer loop and `y` likewise as the inner loop. Each offending unordered pair is therefore visited twice. For each pair, append `QUOTIENT_CLASS_NOT_BEHAVIOR_CONSTANT` and then `QUOTIENT_NOT_EXACT_BEHAVIOR_KERNEL` if they apply.

## Effect on existing records

`tests/test_far_contract_v2_errata1.py` compares the corrected and baseline verifiers on every tracked `far-ir/2.0` record. They agree on every record except the four root-of-trust audit adversarial records built to trigger these defects. No `PCA-W4` or `PCA-W6` recorded outcome changes. The W6 checker additionally requires the corrected verifier to reproduce every W6 item outcome of the executed baseline.

## Nonclaims

These errata do not change the `far-ir/2.0` schema, the frozen specification or verifier bytes, any frozen record, any recorded campaign result, or any claim status. They do not establish that the corrected verifier is correct beyond the audited defects, or that the corrected text is sufficient for independent convergence, which is what `EFR-R2` tests.
