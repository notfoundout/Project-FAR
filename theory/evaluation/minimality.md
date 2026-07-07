# Primitive Minimality Analysis

Status: Provisional v0.3.0 evaluation artifact.

## Purpose

This analysis evaluates whether the current five-primitive set appears minimal under repository evidence. It does not claim a final proof of minimality.

## Sufficiency Versus Minimality

Sufficiency asks whether the five primitives can represent the evaluated reasoning systems without adding a sixth primitive. Minimality asks whether any of the five can be removed or derived from the others without losing explanatory or evaluative power. Current v0.3.0 evidence is stronger for provisional sufficiency than for formal minimality.

## Can Any Primitive Be Derived From the Others?

Current evidence does not show that any primitive can be derived from the other four. Each primitive has a distinct failure mode in the independence analysis:

- Investigation: scope and provenance boundary;
- Representation: explicit content;
- Representational Structure: relations among content;
- Interpretation: domain meaning and satisfaction;
- Reasoning Calculus: admissible transformation.

These roles interact, but the repository has no accepted derivation that eliminates one role.

## Can Any Pair Be Merged?

Potential pair mergers weaken the analysis:

- Merging Representation and Representational Structure obscures the difference between content and relations among content.
- Merging Structure and Interpretation obscures the difference between a relation and the meaning assigned to that relation.
- Merging Interpretation and Reasoning Calculus obscures the difference between semantic assignment and admissible transformation.
- Merging Investigation with any content primitive erases scope, provenance, and boundary discipline.
- Merging Representation and Reasoning Calculus collapses states and transformations, weakening proof-trace and transition analysis.

## Why Merging Would Weaken Explanatory or Evaluative Power

The v0.3.0 evaluations repeatedly separate what is represented, how represented items are related, how they are interpreted, and which transformations are admissible. That separation is what allows the repository to classify cases as `fits FAR`, `conservative extension`, `unresolved pressure`, `outside scope`, or `candidate counterexample` without silently changing primitives. Merging primitives would reduce auditability and make pressure localization less precise.

## Reduction Table

| Primitive | Candidate Reduction | Result | Reason |
|---|---|---|---|
| Investigation | Reduce to Representation plus metadata | currently necessary | Scope and provenance boundaries are not merely represented objects; they identify the reasoning episode under evaluation. |
| Representation | Reduce to Structure or Interpretation | currently necessary | Structures and interpretations require explicit relata or content. |
| Representational Structure | Reduce to collections of Representations | currently necessary | Relations such as accessibility, dependency, attack, typing, ordering, and composition are not captured by bare content lists. |
| Interpretation | Reduce to Structure plus Calculus | currently necessary | Semantic, normative, probabilistic, indexed, or satisfaction assignments are distinct from relations and transitions. |
| Reasoning Calculus | Reduce to interpreted structures | currently necessary | Admissible transformation and inference rules are distinct from static meaning assignments. |

## Current Minimality Status

The current evidence supports provisional non-redundancy, not a final proof of minimality. Each primitive is currently classified as `currently necessary`. No primitive is currently classified as `possibly redundant`, and no reduction is accepted as proven. Future falsification may still show that a primitive can be derived, merged, or replaced.
