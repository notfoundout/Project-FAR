# CRE-001 Semantic Regression


## Status Vocabulary

- **Supported**: established for frozen CRE-001 vocabulary-semantics scope by explicit source definitions and this specification.
- **Unsupported**: not established and not licensed by this specification.
- **Unknown**: not determined by available repository evidence.
- **Assumed**: required CRE-001-scoped assumption recorded explicitly.
- **Implementation-specific**: property of the deterministic compiler/verifier artifacts, not primitive semantics.


## Regression Authority

`semantic-specification.json` and `semantic-regression-lock.json` are checked by `tools/check_cre001_semantics.py`.

## Must Fail If

- Primitive definitions change without updating the frozen semantics and lock.

- Semantic commitments drift.

- Derived machinery silently grows.

- Primitive licensing changes.

- Semantic documents disagree with the machine-readable specification.

- Hidden assumptions are introduced in generated native artifacts.
