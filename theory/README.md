# Theory Index

This directory contains Project FAR's canonical shared theory. Research notes remain under `../research/`; framework-specific commitments remain under `../frameworks/`.

## Governing theory

- [Project FAR Core Theory v1.1](theorems/Project-FAR-Theory-Closure-v1.1.md) — current governed correction of the contract-relative representation, sufficiency, observational-quotient, invariance, and terminal-boundary results.
- [Machine-readable v1.1 core ledger](terminal/project-far-core-theory-v1.1.json) — current claim IDs, corrected scopes, dispositions, and assurance.
- [Permanent v1.1 regressions](evaluation/project-far-core-theory-v1.1-regressions.json) — countermodels preventing reintroduction of the FAR-CORE-004 and FAR-CORE-010 defects.
- [Historical Project FAR Core Theory v1.0](theorems/Project-FAR-Theory-Closure-v1.0.md) — immutable historical base, preserved byte-for-byte at its recorded SHA-256 and superseded only as current authority.
- [Shared definitions](definitions/definitions.md) — canonical vocabulary used by the core and frameworks.

## Supporting areas

- `axioms/` — legacy and scoped axiom records; none overrides the core theory.
- `theorems/`, `proofs/`, and `proof-objects/` — theorem and proof artifacts at their recorded assurance.
- `evaluation/` — bounded protocols, historical programs, regression fixtures, and the post-closure assurance program.
- `independence/` — historical primitive-independence criteria and research artifacts.

## Reading order

1. `theorems/Project-FAR-Theory-Closure-v1.1.md`
2. `../docs/governance/project-far-theory-closure-acceptance-v1.1.md`
3. `../docs/audits/project-far-core-theory-v1.1-correction-audit.md`
4. `definitions/definitions.md`
5. `../docs/governance/framework-boundaries.md`
6. FARA, FAR, then FARO.

For provenance, reviewers of v1.1 should also retain access to the immutable v1.0 monograph and ledger.

## Canonical boundary

Shared theory depends on foundations and precedes FARA. FARA is a selected representation target; FAR and FARO are downstream methodology and operations. Historical v1.0 and UPP artifacts remain evidence and history, not current theorem authority. `PCA-W1-INDEPENDENT-REVIEW` remains open; the hostile audit that produced the v1.1 correction does not count as independent validation.
