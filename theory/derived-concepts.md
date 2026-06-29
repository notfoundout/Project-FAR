# Derived Concepts

## Purpose

This document records the concepts of Project FAR that are regarded as derived rather than primitive.

The objective is to demonstrate that each derived concept can be completely characterized in terms of the primitive architecture of FARA.

Successful derivations strengthen the claim that the primitive architecture is both minimal and sufficient.

---

# Primitive Architecture

The current candidate primitive concepts are:

- Investigation
- Representation
- Representational Structure
- Interpretation
- Reasoning Calculus

Every derived concept should ultimately depend only upon these primitives.

---

# Derivation Standards

A derived concept is considered formally established only if:

- Its derivation is complete.
- Its derivation is non-circular.
- Every dependency is explicitly identified.
- Every dependency ultimately terminates at the primitive architecture.
- The derivation preserves the expressive power of Project FAR.

---

# DC-REASONING-STATE

## Status

Pending

## Primitive Dependencies

- Investigation
- Representation
- Representational Structure
- Interpretation
- Reasoning Calculus

## Derived Dependencies

None

## Objective

Demonstrate that a reasoning state can be completely characterized using only the primitive architecture.

## Proposed Derivation

Pending.

## Formal Derivation

Pending.

## Notes

None.

---

# DC-TRANSITION-SIGNATURE

## Status

Pending

## Primitive Dependencies

- Investigation
- Representation
- Representational Structure
- Interpretation
- Reasoning Calculus

## Derived Dependencies

- DC-REASONING-STATE

## Objective

Demonstrate that a transition signature can be completely characterized using the primitive architecture together with the derived concept of a reasoning state.

## Proposed Derivation

Pending.

## Formal Derivation

Pending.

## Notes

None.

---

# DC-CANDIDATE

## Status

Pending

## Primitive Dependencies

- Investigation
- Representation
- Interpretation

## Derived Dependencies

None

## Objective

Demonstrate that a candidate can be completely characterized using the primitive architecture.

## Proposed Derivation

Pending.

## Formal Derivation

Pending.

## Notes

None.

---

# DC-ADMISSIBILITY-STRUCTURE

## Status

Pending

## Primitive Dependencies

- Reasoning Calculus

## Derived Dependencies

- DC-CANDIDATE

## Objective

Demonstrate that the Admissibility Structure (Ω) can be completely characterized from the primitive architecture.

## Proposed Derivation

Pending.

## Formal Derivation

Pending.

## Notes

None.

---

# DC-RESOLUTION-RULE

## Status

Pending

## Primitive Dependencies

None

## Derived Dependencies

- DC-ADMISSIBILITY-STRUCTURE

## Objective

Demonstrate that a resolution rule can be completely characterized from the Admissibility Structure.

## Proposed Derivation

Pending.

## Formal Derivation

Pending.

## Notes

None.

---

# DC-RESOLUTION

## Status

Pending

## Primitive Dependencies

None

## Derived Dependencies

- DC-ADMISSIBILITY-STRUCTURE
- DC-RESOLUTION-RULE

## Objective

Demonstrate that a resolution can be completely characterized from previously established concepts.

## Proposed Derivation

Pending.

## Formal Derivation

Pending.

## Notes

None.

---

# Dependency Graph

The intended dependency structure is:

```text
Primitive Architecture
        │
        ├── DC-REASONING-STATE
        │         │
        │         └── DC-TRANSITION-SIGNATURE
        │
        ├── DC-CANDIDATE
        │         │
        │         └── DC-ADMISSIBILITY-STRUCTURE
        │                     │
        │                     └── DC-RESOLUTION-RULE
        │                                 │
        │                                 └── DC-RESOLUTION
```

---

# Research Status

No formal derivations have yet been completed.

This document serves as the canonical record of Project FAR's derived concepts and will be updated as formal derivations are established.
