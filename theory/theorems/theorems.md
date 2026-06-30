# Theorems

## Purpose

This document records the established theorems of Project FAR.

A theorem is a formal result proved from the canonical definitions, established derived concepts, axioms, and previously established propositions.

Theorems represent the highest level of the formal theory.

## Canonical Prerequisites

Theorems must reference the current canonical definitions in `../definitions/definitions.md`, current canonical axioms in `../axioms/axioms.md`, and any previously established propositions or theorems before introducing a new theorem.

---


# Theorem Lifecycle

Every theorem progresses through the following stages.

1. Proposed
2. Verified
3. Established

Only established theorems should be regarded as part of the canonical theory.

---

# Theorem Format

Every theorem should contain the following sections.

## Identifier

A unique identifier of the form:

```text
T-NAME
```

---

## Statement

The formal claim.

---

## Dependencies

Every definition, derived concept, axiom, proposition, and theorem upon which the theorem depends.

---

## Proof

A reference to the corresponding proof document located within the `theory/proofs/` directory.

---

## Status

One of:

- Proposed
- Verified
- Established

---

## Notes

Optional observations.

---

# Planned Theorems

The following theorems represent major long-term research objectives.

## T-MINIMAL-PRIMITIVE-ARCHITECTURE

**Objective**

Demonstrate that the primitive architecture of FARA is minimal by proving that no primitive concept is derivable from the remaining primitive concepts.

**Status**

Research

---

## T-SUFFICIENCY-OF-PRIMITIVE-ARCHITECTURE

**Objective**

Demonstrate that every non-primitive concept within Project FAR is derivable from the primitive architecture.

**Status**

Research

---

## T-EXPRESSIVE-SUFFICIENCY

**Objective**

Demonstrate that the primitive architecture preserves the expressive power required to represent every reasoning process within the stated scope of Project FAR.

**Status**

Research

---

## T-REPRESENTATION-THEOREM

**Objective**

Demonstrate that every reasoning process within the stated scope of Project FAR admits a representation within FARA.

**Status**

Research

---

# Established Theorems

None.

---

# Research Status

Project FAR has not yet established any formal theorems.

Current research is focused on:

- deriving non-primitive concepts;
- verifying primitive independence;
- establishing propositions; and
- developing formal proofs.

Theorems will be introduced only after a sufficient body of established propositions has been developed.
