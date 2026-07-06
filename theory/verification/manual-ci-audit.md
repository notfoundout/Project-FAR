# Manual CI Audit

## Purpose

This document defines the manual checks that must be run before accepting new theory work into Project FAR.

The checks are written as CI-style gates so they can later be converted into scripts.

---

# Gate 1 — File Placement

## Check

Each new file must be located in the correct directory:

- definitions in `theory/definitions/`
- axioms in `theory/axioms/`
- propositions and theorem catalogs in `theory/theorems/`
- proofs in `theory/proofs/`
- lemmas in `theory/lemmas/`
- derivations in `theory/derivations/`
- notation in `theory/notation/`
- audits in `theory/audits/`
- tests in `theory/tests/`
- examples in `theory/examples/`

## Fail If

A canonical theory artifact is placed in an unrelated or ambiguous directory.

---

# Gate 2 — Identifier Consistency

## Check

Every theorem, proposition, lemma, and audit must have a stable identifier.

Examples:

- `T-006`
- `P-001`
- `L-004`
- `AUDIT-001`

## Fail If

An artifact has no identifier, duplicates an existing identifier, or changes an identifier without a migration note.

---

# Gate 3 — Dependency Declaration

## Check

Every proof file must list dependencies.

## Fail If

The proof cites unstated concepts, axioms, lemmas, propositions, or theorems.

---

# Gate 4 — Dependency Graph Update

## Check

If a new proof is added, `theory/dependencies/dependency-graph.md` must be updated.

## Fail If

The proof exists but the graph does not include it.

---

# Gate 5 — Registry Compliance

## Check

Every non-primitive technical concept used by a proof must appear in `theory/derivations/derived-concept-registry.md` unless explicitly marked informal.

## Fail If

A proof relies on an unregistered technical concept.

---

# Gate 6 — Notation Compliance

## Check

Every proof must use `theory/notation/canonical-notation.md` unless declaring a local override.

## Fail If

A canonical symbol is used inconsistently.

---

# Gate 7 — Scope Control

## Check

Every theorem must state its scope and limitations.

## Fail If

A theorem claims universal force while the proof establishes only a conditional, finite, relative, or registry-bound result.

---

# Gate 8 — Circularity Audit

## Check

Every new theorem must be checked for direct and indirect circularity.

## Fail If

The theorem depends on itself, a later theorem that depends on it, or a definition justified by it.

---

# Gate 9 — Falsification Pressure

## Check

Major new generality claims must be tested against a counterexample or boundary case.

## Fail If

A generality claim is accepted without any falsification attempt.

---

# Gate 10 — Catalog Update

## Check

Established theorems must appear in `theory/theorems/theorems.md`.

Established propositions must appear in `theory/theorems/propositions.md`.

## Fail If

The proof exists but the canonical catalog is stale.

---

# Manual CI Result Format

Every audit run should record:

```text
Date:
Scope:
Files checked:
Gates passed:
Gates failed:
Required fixes:
Decision:
```

---

# Decision Values

- Pass
- Pass with limitation
- Block merge
- Require downgrade
- Require deprecation

---

# Current Status

Manual CI rules established. No automated script currently enforces them.
