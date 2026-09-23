# far-ir/2.0 Current Verification Rule

Status: **Accepted current verification surface; additive to the frozen `far-ir/2.0` specification**

Current verifier: [`mechanization/far_mechanization/contract_v2_strict.py`](../../mechanization/far_mechanization/contract_v2_strict.py)

Frozen baseline: [`mechanization/far_mechanization/contract_v2.py`](../../mechanization/far_mechanization/contract_v2.py), specified by [`far-ir-2.0-contract.md`](far-ir-2.0-contract.md)

## Why this page exists

The [`far-ir/2.0` specification](far-ir-2.0-contract.md) section 9, Stage 3 runs a claim-specific check only when `report.evidence.status` is `CHECKED_FINITE_EXPLICIT`. A record with `DECLARED_UNCHECKED` evidence therefore passes the baseline verifier with outcome `PROVED` or `REFUTED` even when its own explicit tables contradict that outcome. Baseline `success` means well-formed, not verified (`LIM-047`).

The baseline specification and verifier are not edited. The specification is git-blob bound by `EFR-001-R2-INPUT-AMENDMENT-1.1`, and the verifier is git-blob pinned as the `PCA-W6` protocol base and named as the `EFR-001` v1.0 baseline command.

## Rule

Current far-ir/2.0 verification is the baseline verifier followed by one additional rule, applied to the same parsed document:

> A report whose `outcome` is `PROVED` or `REFUTED` is accepted only when `report.evidence.status` is `CHECKED_FINITE_EXPLICIT`.

Records with any other outcome (`OPEN`, `BLOCKED`, `UNDERDETERMINED`, `NOT_APPLICABLE`, `HISTORICAL_SUPERSEDED`, `Unknown`) are unaffected. For every record whose determinate outcome is backed by checked evidence, current and baseline verification return identical diagnostics.

A file is read and parsed exactly once, and both the baseline and the additional rule see that same in-memory document. An unreadable file (missing, not UTF-8, or not JSON) yields only `UNREADABLE_CONTRACT`.

## Additional diagnostic

| Code | Condition |
|---|---|
| `DETERMINATE_OUTCOME_UNCHECKED` | `report.outcome` is `PROVED` or `REFUTED` and `report.evidence.status` is not `CHECKED_FINITE_EXPLICIT`. |

The declaration authority is `FAR_IR_2_0_STRICT_DIAGNOSTIC_CODES` in [`diagnostic_vocabulary.py`](../../mechanization/far_mechanization/diagnostic_vocabulary.py).

## Current versus historical use

Every current surface uses the current verifier: the `far-ir/2.0` conformance runner, v1→v2 migration, the `PCA-W4` recomputation checker, the commercial semantic audit, and any campaign registered after this rule, including `EFR-002`.

Direct use of the baseline is limited to reproducing records whose provenance names it: the `PCA-W6` protocol, the `EFR-001` v1.0 frozen baseline command, baseline regression tests, and diagnostic-vocabulary publication. The registry in [`verifier_authority.py`](../../mechanization/far_mechanization/verifier_authority.py) lists each permitted baseline consumer with its reason, and `tests/test_contract_v2_verifier_authority.py` fails if any other tracked file imports or invokes the baseline.

Command:

```bash
python -m mechanization.far_mechanization.contract_v2_strict RECORD --json
```

## Nonclaims

This rule does not change the `far-ir/2.0` schema, any frozen record, any recorded campaign result, or any claim status. It is not a claim that checked records correspond to a real application domain.
