# Derived Concept Registry

## Purpose

This registry lists current non-primitive Project FAR concepts and records how each derives from the primitive architecture.

The primitive architecture is:

```text
P = { Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus }
```

A concept is admissible as derived only if it can be constructed from primitives or previously registered derived concepts.

---

# Primitive Concepts

These are not derived in the current theory.

| ID | Concept |
|---|---|
| PR-001 | Investigation |
| PR-002 | Representation |
| PR-003 | Representational Structure |
| PR-004 | Interpretation |
| PR-005 | Reasoning Calculus |

---

# First-Level Derived Concepts

| ID | Concept | Derivation |
|---|---|---|
| D-001 | Semantic Content | Interpretation applied to Representation within Investigation |
| D-002 | Representation Collection | Set or ordered collection of Representations |
| D-003 | Structural Relation | Relation specified by Representational Structure over Representations |
| D-004 | Reasoning State | Representation Collection plus applicable structure and interpretation within an Investigation |
| D-005 | Transformation Rule | Rule belonging to a Reasoning Calculus |
| D-006 | Admissibility | Satisfaction of criteria supplied by a Reasoning Calculus within an Investigation |
| D-007 | Candidate | Representation evaluated under an Investigation and Reasoning Calculus |
| D-008 | Resolution Rule | Rule in a Reasoning Calculus that selects, rejects, ranks, or terminates candidates |

---

# Second-Level Derived Concepts

| ID | Concept | Derivation |
|---|---|---|
| D-009 | Transformation Execution | Application of D-005 to D-004 under PR-005 |
| D-010 | Transformation Result | Output of D-009 |
| D-011 | Transition Signature | Representation of D-009 between reasoning states |
| D-012 | Reasoning Trace | Ordered collection of D-011 |
| D-013 | Admissibility Structure | Structure over candidates and admissibility statuses |
| D-014 | Resolution Execution | Application of D-008 to D-013 |
| D-015 | Resolution | Result of D-014 |
| D-016 | Representation Mapping | Function from one Representation Collection or Structure to another |
| D-017 | Semantic Equivalence | Preservation of D-001 under mapping |
| D-018 | Structural Equivalence | Preservation of D-003 under mapping |

---

# Third-Level Derived Concepts

| ID | Concept | Derivation |
|---|---|---|
| D-019 | FAR Representation | Tuple `<I, Rep, S, Int, C, T>` using primitives plus D-012 |
| D-020 | FAR Model | FAR structure satisfying Project FAR axioms |
| D-021 | Satisfaction | Relation between FAR Model and statement under Interpretation and Calculus |
| D-022 | Validity | Satisfaction across a specified class of FAR Models |
| D-023 | Model Equivalence | Preservation of selected properties across FAR Models |
| D-024 | Canonical Representation | FAR Representation after redundancy-removal and canonical labeling |
| D-025 | Normal Form | Canonical Representation under total ordering and canonical labels |
| D-026 | Conservative Extension | Extension that adds no new primitive and preserves canonical definitions, axioms, and theorem dependencies |

---

# Registry Rule

A theorem may claim primitive sufficiency only for concepts listed in this registry or for concepts added later with an explicit derivation path.

If a term appears in Project FAR but does not appear in this registry, one of three actions is required:

1. add it as a derived concept with a valid derivation;
2. mark it as informal and non-canonical;
3. treat it as evidence that the primitive architecture may be incomplete.

---

# Current Sufficiency Result

The current registry supports T-006 for D-001 through D-026.

T-006 should not be read as covering unregistered future concepts.
