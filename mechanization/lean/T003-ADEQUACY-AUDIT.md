# T-003 Assumption-Minimality and Adequacy Audit

## Result

The Lean encoding now distinguishes two claims that were previously easy to conflate:

1. **Structural existence**: the type `FARRepresentation R` has an inhabitant.
2. **Faithful representation**: a FAR tuple preserves an independently specified process's investigation, representations, structure, semantics, admissible transitions, and trace.

These are not equivalent.

## Minimality finding

Under the current Lean data types, A1-A5 are not necessary for bare structural existence. `defaultFARRepresentation` constructs a placeholder tuple for every `ReasoningProcess`, and `unconditional_structural_existence` proves:

```text
∀ R, Nonempty (FARRepresentation R)
```

without A1-A5.

This does not refute A1-A5. It shows that T-003's bare existence conclusion is too weak to establish their necessity. The premises select process-relative content; they are not needed merely to inhabit the tuple type.

## Non-circularity finding

The theorem `t003_representation_theorem` is a valid constructor theorem, but its conclusion is close to its premises:

- A4 supplies the investigation.
- A1 supplies a nonempty representation collection.
- A2 supplies the structure over that collection.
- A3 supplies the interpretation for that investigation and collection.
- A5 supplies the calculus.
- The trace is copied from the process.

Lean verifies that these components can be assembled consistently. It does not independently derive their existence from a weaker description of reasoning.

## Preservation layer

`ProcessSpecification` provides an independent target containing:

- a process;
- its investigation;
- its representations;
- required structural relations;
- semantic assignments;
- admissible transitions.

The audit defines:

- `StructuralPreservation`;
- `SemanticPreservation`;
- `OperationalPreservation`;
- `TracePreservation`;
- `FaithfulRepresentation`.

`canonical_representation_is_faithful` proves that the canonical compiler from a valid process specification preserves all four dimensions.

## Concrete instantiations

The preservation theorem is instantiated for three distinct process classes:

1. propositional modus ponens;
2. clinical triage;
3. contract-rule analysis.

These examples establish that the preservation layer is executable across different domains. They do not establish universal domain coverage.

## Negative result

`corruptedModusPonensRepresentation` is a valid inhabitant of the six-component FAR type but intentionally has:

- the wrong investigation;
- corrupted meanings;
- a calculus that permits no transition.

Lean proves that it fails structural, semantic, and operational preservation and therefore is not faithful.

The theorem `structural_existence_does_not_imply_faithfulness` records the exact result:

```text
Nonempty (FARRepresentation R) ∧
∃ F : FARRepresentation R, ¬ FaithfulRepresentation spec F
```

for the modus-ponens specification.

## Independence boundary

This audit does **not** prove model-theoretic independence of A1-A5. Because the current component types have trivial inhabitants, removal of any premise does not block bare tuple construction. What the negative examples establish is that structural typing alone does not imply the corresponding preservation obligations.

A genuine axiom-independence result would require a semantic theory in which each axiom is represented as a proposition over models and countermodels are constructed for every omitted axiom.

## Licensed conclusions

The mechanization now supports these conclusions:

- T-003 is a valid conditional construction theorem.
- A1-A5 are not minimal for bare tuple inhabitation in the current encoding.
- Bare tuple inhabitation does not imply faithful representation.
- Faithfulness requires explicit preservation obligations.
- A canonical representation built from a valid independent process specification satisfies those obligations.

It does not support these conclusions:

- A1-A5 are logically necessary for all reasoning.
- A1-A5 are mutually independent.
- every cognitive process admits an independently recoverable process specification;
- FAR is unique, minimal, or universally adequate;
- the three examples establish universal scope.
