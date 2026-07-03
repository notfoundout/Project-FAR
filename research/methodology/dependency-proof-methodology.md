# Dependency Proof Methodology

## Purpose

Establish the methodology by which dependency claims are proven within Project FAR.

The objective is to distinguish demonstrated dependencies from proposed dependencies.

---

# Motivation

Previous investigations introduced dependency graphs and dependency classes.

Every edge within those graphs represents a substantive claim.

Those claims require explicit proof procedures.

---

# Central Question

What constitutes sufficient evidence that one concept depends upon another?

---

# Dependency Claim

A dependency claim has the form:

Concept A depends upon Concept B.

The burden of proof rests upon the claimant.

---

# Proof Strategy 1

Removal Test.

Procedure:

Temporarily remove Concept B.

Question:

Can Concept A still be coherently defined, exist, or operate according to the claimed dependency?

Evaluation:

If A survives unchanged, the dependency is rejected.

If A necessarily fails, the dependency is supported.

---

# Proof Strategy 2

Reduction Test.

Procedure:

Attempt to define Concept A without reference to Concept B.

Evaluation:

If a complete definition exists, the dependency is rejected.

If every successful definition requires Concept B, the dependency is supported.

---

# Proof Strategy 3

Construction Test.

Procedure:

Attempt to reconstruct Concept A beginning only from previously established concepts.

Evaluation:

If Concept B is required during every successful reconstruction, the dependency is supported.

---

# Proof Strategy 4

Counterexample Test.

Procedure:

Produce a valid instance of Concept A that does not require Concept B.

Evaluation:

A single valid counterexample rejects the proposed dependency.

---

# Proof Strategy 5

Circularity Test.

Procedure:

Determine whether the proposed dependency presupposes the conclusion it seeks to establish.

Evaluation:

Circular dependency arguments are rejected.

---

# Evidence Classification

Dependency claims shall be classified as:

## Proposed

A dependency has been hypothesized.

---

## Supported

Multiple proof strategies support the dependency.

No counterexample has been identified.

---

## Established

Every applicable proof strategy supports the dependency.

Repeated attempts at falsification have failed.

---

## Rejected

At least one successful counterexample or reduction disproves the dependency.

---

# Observation

Different dependency classes may require different forms of evidence.

The methodology determines how dependency claims are evaluated.

It does not determine in advance which dependency claims are true.

---

# Consequences

Every edge in the Project FAR dependency graph shall reference the investigation establishing that dependency.

Dependencies are therefore traceable, reproducible, and independently reviewable.

---

# Current Status

This methodology is proposed.

Future investigations shall apply it to every dependency introduced within Project FAR.