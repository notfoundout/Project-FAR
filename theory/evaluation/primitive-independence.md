# Primitive Independence Analysis

Status: Provisional v0.3.0 evaluation artifact.

## Purpose

This analysis asks what breaks if each FAR primitive is removed. It is not a mathematical independence proof. It is the strongest current repository-grounded argument from fixtures, registries, reports, and adversarial evaluations.

## Investigation

### Role

Investigation scopes an explicit reasoning episode and separates the object of inquiry from surrounding activity.

### Hypothetical Removal

Without Investigation, the repository loses the unit that distinguishes an explicit reasoning process from background context, external intervention, or another agent's reasoning episode.

### Systems Affected

Multi-agent reasoning, interactive theorem proving, scientific reasoning, legal reasoning, and all fixture-level evaluations that require an identified reasoning episode.

### Why Other Primitives Cannot Fully Replace It

Representation can encode objects, structure can relate them, interpretation can assign meaning, and calculus can govern transformations, but none of those primitives alone supplies the boundary and provenance role of an investigation.

### Current Independence Status

`independent`

## Representation

### Role

Representation supplies the objects, statements, rules, claims, traces, terms, worlds, assignments, and artifacts that reasoning operates on.

### Hypothetical Removal

Without Representation, there is no explicit content for structure, interpretation, or calculus to relate, interpret, or transform.

### Systems Affected

Higher-order logic, description logic, SAT solving, theorem provers, type theory, modal logic, temporal logic, paradox, and every fixture with explicit content.

### Why Other Primitives Cannot Fully Replace It

Structure presupposes relata, interpretation presupposes something interpreted, and calculus presupposes states or expressions to transform. Investigation scopes work but does not provide content.

### Current Independence Status

`independent`

## Representational Structure

### Role

Representational Structure records relations among representations: accessibility, ordering, attack-defense, dependency, causal, categorical, typing, clause, or proof-state relations.

### Hypothetical Removal

Without Representational Structure, representations collapse into an unorganized collection; many systems lose the relations that make their reasoning possible.

### Systems Affected

Modal logic, temporal logic, causal reasoning, category-theoretic reasoning, probabilistic programming, argumentation frameworks, quantum logic, SAT solving, theorem provers, and type theory.

### Why Other Primitives Cannot Fully Replace It

Representation can list items but not the relations among them. Interpretation can assign meaning to structures but cannot replace the existence of the structure. Calculus can transform structures but cannot supply static dependency, accessibility, ordering, or compositional relations by itself.

### Current Independence Status

`independent`

## Interpretation

### Role

Interpretation assigns semantic, normative, probabilistic, indexed, constructive, or model-theoretic meaning to representations and structures.

### Hypothetical Removal

Without Interpretation, represented artifacts and transitions can be syntactically manipulated but not evaluated as true, valid, satisfied, obligatory, probable, constructive, or meaningful in a domain.

### Systems Affected

Modal logic, temporal logic, deontic logic, fuzzy logic, intuitionistic logic, paradoxical reasoning, reflective reasoning, meta-reasoning, hybrid logic, causal reasoning, and category-theoretic reasoning.

### Why Other Primitives Cannot Fully Replace It

Structure can organize content and calculus can transform it, but neither supplies domain meaning. A calculus may preserve a semantic property, but the semantic assignment remains an interpretation pressure.

### Current Independence Status

`independent`

## Reasoning Calculus

### Role

Reasoning Calculus supplies admissible transformations, inference rules, proof steps, update policies, transition rules, and revision or conflict-handling procedures.

### Hypothetical Removal

Without Reasoning Calculus, FAR can store and interpret static representations, but cannot account for inferential movement or admissible reasoning steps.

### Systems Affected

Theorem provers, SAT solving, type theory, intuitionistic logic, belief revision, learning systems, dynamic logic, non-monotonic reasoning, inconsistent calculus, self-modifying reasoning, and all proof-like fixtures.

### Why Other Primitives Cannot Fully Replace It

Representation and structure describe states, and interpretation assigns meanings, but none of them specifies which transformations are allowed. Investigation scopes the activity but does not govern its inference rules.

### Current Independence Status

`independent`

## Independence Matrix

| Primitive Removed | Systems Affected | Failure Mode | Independence Status |
|---|---|---|---|
| Investigation | Multi-agent reasoning; interactive theorem proving; scientific and legal reasoning; all scoped fixture evaluations | Loss of reasoning-episode boundary, provenance, and explicit scope | independent |
| Representation | Higher-order logic; description logic; SAT solving; theorem provers; type theory; modal, temporal, paradoxical, and fixture-level reasoning | No explicit content for structure, interpretation, or calculus | independent |
| Representational Structure | Modal, temporal, causal, categorical, probabilistic, argumentation, quantum, SAT, theorem-prover, and type-theoretic cases | Loss of accessibility, order, dependency, typing, attack-defense, clause, proof-state, and compositional relations | independent |
| Interpretation | Modal, temporal, deontic, fuzzy, intuitionistic, paradoxical, reflective, meta, hybrid, causal, and categorical cases | Loss of semantic, normative, probabilistic, indexed, constructive, or satisfaction meaning | independent |
| Reasoning Calculus | Theorem provers; SAT solving; type theory; intuitionistic logic; belief revision; learning; dynamic; non-monotonic; inconsistent; self-modifying reasoning | Loss of admissible transformation, inference, update, revision, and transition rules | independent |

## Current Conclusion

Current repository evidence supports provisional independence for all five primitives. This is not a formal model-theoretic independence proof. It is a repository-grounded failure analysis: removing any primitive creates a recurring failure mode not fully supplied by the remaining four primitives.
