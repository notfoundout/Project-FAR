# Validation Investigation

## Investigation ID

VI-003

---

## Title

Primitive Independence

---

## Status

Research

---

# Purpose

This investigation evaluates whether each current candidate primitive contributes unique expressive capability to the Foundational Architecture of Reasoning Analysis (FARA).

Unlike Validation Investigation VI-002, which attempted explicit reductions, this investigation seeks evidence that each candidate primitive is logically indispensable to the current architecture.

---

# Research Question

Does each current candidate primitive contribute expressive capability that cannot be reconstructed from the remaining candidate primitives?

---

# Hypothesis

Every current candidate primitive contributes unique expressive capability.

Removing any candidate primitive should produce at least one representational capability that cannot be recovered using the remaining candidate primitives.

---

# Relationship to VI-002

Validation Investigation VI-002 asked:

> Can a primitive be reduced?

Validation Investigation VI-003 asks:

> If reduction fails, can independence be positively demonstrated?

Failure to reduce does not establish independence.

Independent evidence must therefore be produced.

---



## Relationship to T-002

T-002 establishes a conditional deletion-independence result under its stated assumptions. VI-003 remains incomplete because its broader reconstruction, re-execution, counterexample-minimization, and equivalent-reconstruction criteria have not all been satisfied.

---

# Candidate Primitive Basis

- Object
- Property
- Relation
- Representation
- Interpretation
- Investigation
- Reasoning Calculus

---

# Independence Criterion

A candidate primitive is provisionally independent if removing it necessarily prevents the architecture from representing at least one reasoning situation that was previously representable.

Evidence must identify a minimal counterexample.

---

# Methodology

For each candidate primitive:

1. Remove the primitive.
2. Replace every occurrence using only the remaining candidate primitives.
3. Reconstruct the affected architectural definitions.
4. Execute Validation Investigation VI-001.
5. Execute Validation Investigation VI-002.
6. Search for a reasoning situation that can no longer be represented.
7. Minimize the counterexample.
8. Verify that no equivalent reconstruction exists.

---

# Required Evidence

An independence claim should identify:

- the primitive removed;
- the representational capability lost;
- the smallest counterexample;
- the failed reconstruction;
- the reason reconstruction fails.

---

# Evaluation Criteria

Each candidate primitive shall receive one of the following classifications.

**Independent**

The primitive contributes unique expressive capability that cannot be reconstructed.

**Dependent**

The primitive's expressive capability can be completely reconstructed from the remaining candidate primitives.

**Undetermined**

Current evidence is insufficient to justify either conclusion.

---

# Primitive Evaluation Matrix

| Primitive | Status | Classification |
|-----------|:------:|----------------|
| Object | Pending | — |
| Property | Pending | — |
| Relation | Pending | — |
| Representation | Pending | — |
| Interpretation | Pending | — |
| Investigation | Pending | — |
| Reasoning Calculus | Pending | — |

---

# Research Status

Research

No primitive evaluations have yet been completed.
