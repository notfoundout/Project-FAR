# Backburner

## Purpose

This document records ideas that may strengthen Project FAR but are not currently required for the core framework.

Items remain here until there is sufficient theoretical justification or practical need to incorporate them into the architecture, methodology, or formal theory.

Unlike the active research questions, these items are intentionally deferred.

---

# Medium Priority

## Transformation Taxonomy

Develop a formal classification of transformation types.

Possible categories include:

- Addition
- Removal
- Modification
- Reorganization
- Interpretation Transformation
- Investigation Transformation

---

## Confidence, Uncertainty, and Degrees of Support

Investigate whether these concepts deserve formal treatment within Project FAR after the core theory has matured.

Questions include:

- Are they architectural concepts or properties?
- Can they be represented independently of probability?
- Should they be associated with representations, candidates, reasoning states, or admissibility classifications?
- Do they increase expressive power if formalized?

Current hypothesis:

These concepts are properties of existing architectural objects rather than new primitives.

Architectural changes should not be considered until additional validation studies have been completed.

---

## Additional Validation Frameworks

Extend validation to additional reasoning frameworks, including:

- Machine Learning
- Engineering Design
- Medical Diagnosis
- Intelligence Analysis
- Economic Reasoning
- Ethical Reasoning
- Strategic Planning

---

# Low Priority

## Repository Dependency Graph

Represent document-level dependencies across the repository.

Ensure dependencies remain acyclic.

---

## Proof Organization

Determine whether proofs should remain in a single file or move into a dedicated `theory/proofs/` directory.

---

## Theorem Organization

Determine whether theorems should eventually move into a dedicated `theory/theorems/` directory.

---

## Contributor Workflow

Develop contributor guidelines for:

- introducing new concepts,
- establishing canonical locations,
- maintaining dependency consistency,
- preserving repository minimality.
