# Primitive Independence W1 Investigation

## Status

Research — execution complete; all seven outcomes unresolved

## Question

Is every proposed FARA primitive logically independent of the others?

## Objective

Determine whether each proposed primitive is indispensable or derivable from the remaining primitives.

## Motivation

A primitive set is justified only if no primitive can be derived from the others. If a proposed primitive is derivable, it should not remain primitive.

## Proof Obligations

1. Formally define logical independence.
2. For each proposed primitive, remove it from the system.
3. Attempt to reconstruct it from the remaining primitives.
4. If reconstruction succeeds, classify it as derived.
5. If reconstruction fails, justify its independence.

## Success Criteria

A complete independence matrix identifying which primitives are independent, derived, equivalent, or require further investigation.

## Execution result

The canonical authority fixes seven **candidate** primitives: Object, Property, Relation, Representation, Interpretation, Investigation, and Reasoning Calculus. It defines Independence only pairwise and defines Reduction relative to a specified scope and objective. It does not provide the formal signature, axioms, inference rules, model class, scope, objective, or equivalence relation needed for independence-from-the-other-six countermodels or lossless derivations.

W1 therefore tested every primitive and failed closed in every case. The complete machine-checkable record is `theory/evaluation/fara-w1-primitive-independence.json`; the generated human-readable result is `primitive-independence-w1-result.md`. Every outcome is **unresolved**. No independence theorem is claimed.

The execution also records circular dependency hazards (Object/Representation, Representation/Interpretation, and Investigation/Reasoning Calculus), possible but unproved hidden equivalences (including Property/Relation encodings), absence of exact normalized renamed duplicates, and exclusion of downstream FAR/FARO methodology.

## Consequence and blocker

All seven concepts remain candidate primitives. Independence, derivability, equivalence, irreducibility, and minimality are not established. A positive rerun requires canonical authority for a formal signature, axioms or inference rules, model class, scope, objective, and equivalence relation; inventing any of these inside this investigation would violate the fail-closed rule.
