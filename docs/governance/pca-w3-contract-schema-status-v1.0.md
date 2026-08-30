# PCA-W3 contract-schema status v1.0

Status: **Complete subject to merge**

Program: `POST-CLOSURE-001`

Workstream: `PCA-W3-CONTRACT-SCHEMA`

Governing theory: `PROJECT-FAR-CORE-THEORY-1.1`

## Terminal disposition

W3 is complete when this change is merged and its exact-head validation is green.

Result: `FAR_IR_2_0_VERSIONED_CONTRACT_SCHEMA_WITH_FINITE_EXPLICIT_SEMANTIC_CHECKER_MIGRATION_AND_CONFORMANCE`

No governing core proposition is changed or reopened.

## Delivered

1. `schemas/far-contract-v2.schema.json` — JSON Schema Draft 2020-12 successor identified as `far-ir/2.0`.
2. `mechanization/far_mechanization/contract_v2.py` — semantic verifier for schema constraints, exact finite factorization, collision witnesses, exact beta-kernel quotient witnesses, typed `Unknown`, and freeze hashing.
3. `mechanization/far_mechanization/migrate_v1_to_v2.py` — loss-explicit migration that first validates `far-ir/1.0`, preserves its primitive payload, and marks absent W3 semantics `Unknown` rather than inventing them.
4. `mechanization/far_mechanization/contract_conformance.py` plus `conformance/far-ir-2.0/` — registered positive and adversarial fixtures.
5. `tests/test_far_contract_v2.py` — mutation-style regressions for decoder failure, false collision, false quotient, freeze drift, approximation overclaim, migration preservation, and Unknown/outcome coherence.
6. `docs/specification/far-ir-2.0-contract.md` — version, semantics, verification boundary, migration boundary, W4 boundary, and W5 boundary.

## Required W3 dimensions

The successor explicitly represents contract identity/version, source/case domain, required behavior, representation, decoder/factorization or collision evidence, observation contexts, typed outcomes including `Unknown`, observational-equivalence/quotient evidence, admitted transformations/equivalences, interpretation profile, target/model class, frame, provenance/freeze metadata, failure reporting, and optional approximation/loss/cost declarations.

## Legacy invariant

`far-ir/1.0` is not modified or reinterpreted. Its schema and parser remain authoritative for the legacy reasoning-document interchange format. Migration to v2 cannot certify sufficiency, collision, quotient, domain correspondence, or application correctness because v1 never encoded the complete comparison contract.

## Assurance boundary

A v2 `CHECKED_FINITE_EXPLICIT` result is recomputed from the explicit finite tables. It is evidence for the encoded finite contract only. It does not establish that the chosen domain, interpretation profile, target class, frame, or observations correctly model an external discipline.

Approximation fields are forward-compatible declarations only. W3 fixes `w5_semantics_established` to `false` and rejects checked approximate evidence. W5 remains open.

## Next workstream

`PCA-W4-DOMAIN-CONTRACTS` is next. W4 must independently motivate and instantiate v2 contracts for formal logic, Bayesian/causal reasoning, argumentation, model-based reasoning, type theory, and proof theory, then run collision/sufficiency audits without reading schema reuse as universal primitive evidence.
