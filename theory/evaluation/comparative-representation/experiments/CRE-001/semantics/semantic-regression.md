# Vocabulary Semantics Baseline 1.0 — Semantic Regression


## Status Vocabulary

- **Supported**: prospectively frozen for CRE-002 and later experiments by explicit baseline definitions and this specification.
- **Unsupported**: not established and not licensed by this specification.
- **Unknown**: not determined by available repository evidence.
- **Assumed**: required CRE-001-scoped assumption recorded explicitly.
- **Implementation-specific**: property of the deterministic compiler/verifier artifacts, not primitive semantics.

## Chronology and Prospective Authority

- Vocabulary Semantics Baseline 1.0 was formalized after completion of deterministic CRE-001.
- It was informed by lessons learned during CRE-001.
- It is frozen for future experiments beginning with CRE-002.
- It is not independent evidence supporting CRE-001.
- It cannot be used as retrospective validation of CRE-001.
- CRE-001 demonstrates only that compiler-authored declared interpretations successfully compiled, lowered, and verified under the registered deterministic reference.


## Regression Authority

`semantic-specification.json` and `semantic-regression-lock.json` are checked by `tools/check_cre001_semantics.py`.

## Must Fail If

- Primitive definitions change without updating the frozen semantics and lock.

- Semantic commitments drift.

- Derived machinery silently grows.

- Primitive licensing changes.

- Semantic documents disagree with the machine-readable specification.

- Hidden assumptions are introduced in generated native artifacts.
