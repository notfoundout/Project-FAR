# Proof Verification Checklist

## Purpose

This checklist defines the minimum verification standard for Project FAR proofs.

A theorem may not be marked Established unless it passes every required check below or explicitly records an approved exception.

---

# Required Checks

## 1. Dependency Check

A proof must list every dependency it uses.

Required items:

- primitive definitions;
- derived concepts;
- axioms;
- propositions;
- lemmas;
- prior theorems;
- notation files;
- model-theory files;
- scope files.

Pass condition: every dependency appears in `theory/dependencies/dependency-graph.md` or is added there in the same change.

Failure condition: the proof relies on an unstated or unavailable dependency.

---

## 2. Notation Check

A proof must use canonical notation from:

`theory/notation/canonical-notation.md`

Pass condition: symbols such as `I`, `Rep`, `S`, `Int`, `C`, `T`, `⊨`, `≡sem`, `≡str`, `≡Q`, and `NF` are used consistently.

Failure condition: the proof gives a canonical symbol a conflicting meaning without declaring a local override.

---

## 3. Scope Check

A proof must state its scope.

Required scope labels include, when applicable:

- scoped explicit reasoning processes;
- finite FAR representations;
- canonical FAR representations;
- registered derived concepts;
- specified preservation profiles;
- supplied reasoning calculi;
- explicit transition domains.

Pass condition: the theorem's scope is stated clearly and does not exceed what the proof establishes.

Failure condition: the statement is broader than the proof.

---

## 4. Circularity Check

A proof must not depend on itself directly or indirectly.

Pass condition: the proof passes the current circularity audit or includes a new audit update.

Failure condition: the proof depends on itself, a later theorem that depends on it, or a definition justified by it.

---

## 5. Registry Check

A proof using non-primitive concepts must verify that those concepts appear in:

`theory/derivations/derived-concept-registry.md`

Pass condition: every non-primitive technical concept is registered or explicitly marked informal.

Failure condition: the proof depends on an unregistered technical concept.

---

## 6. Lemma Check

A proof should not make large inferential jumps when a reusable lemma would isolate the step.

Pass condition: every major inference is either immediate from a definition, axiom, proposition, lemma, or prior theorem.

Failure condition: a key inferential step is asserted without a supporting lemma or explicit derivation.

---

## 7. Limitation Check

A proof must state its limitations.

Pass condition: the proof identifies what it does not establish.

Failure condition: the proof implies absolute or universal force when it is only conditional, relative, finite, registry-bound, or scope-bound.

---

# Verification Decision

A verifier must assign one of the following outcomes:

- Pass;
- Pass with limitation;
- Needs revision;
- Reject;
- Deprecated.

A theorem may be marked Established only after receiving Pass or Pass with limitation.

---

# Minimum Theorem Header

Every theorem proof file should include:

```text
# T-XXX — Title

## Status

## Statement

## Scope

## Dependencies

## Proof

## Corollaries

## Limitations

## Verification Notes
```

---

# Verification Rule

If a theorem cannot pass this checklist, it must remain Draft or Proposed. It must not be marked Established.
