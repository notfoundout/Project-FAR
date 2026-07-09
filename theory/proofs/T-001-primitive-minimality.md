# T-001 — Conditional Primitive Minimality

## Status

Established relative to the current Project FAR scope, definitions, axioms, and deletion-only compression standard.

This proof is conditional. It establishes minimality for the present architecture as specified by the current definitions and axioms. It does not prove that no future lower-level reduction can replace the primitive set.

---

## Statement

Let the current primitive architecture of Project FAR be:

```text
P = { Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus }
```

Let the objective be representation of reasoning processes within the stated scope of Project FAR evaluation.

For each primitive `p` in `P`, removing `p` without supplying an accepted replacement reduces expressive power relative to that objective.

Therefore, `P` is minimal relative to the current Project FAR scope, definitions, axioms, and deletion-only compression standard.

---

## Dependencies

- `theory/definitions/definitions.md`
- `theory/axioms/axioms.md`
- `theory/semantics/scope.md`
- `theory/lemmas/core-lemmas.md`

---

## Proof

Assume a reasoning process `R` is within the stated Project FAR scope.

By the validated Axiom 1 consequence recorded in L-001 and P-001, `R` admits, for Project FAR evaluation, at least one explicit representation. Therefore, any architecture that removes Representation without supplying an accepted replacement cannot express the explicit objects by which `R` is made analyzable. Expressive power is reduced.

By the validated Axiom 2 consequence recorded in L-002, a participating collection of representations satisfies Project FAR Axiom 2 only if it possesses representational structure. Therefore, any architecture that removes Representational Structure without supplying an accepted replacement can at most list representations without specifying their relations. It cannot represent the organization required to distinguish a structured argument from an unordered inventory of marks. Expressive power is reduced.

By the validated Axiom 3 consequence recorded in L-003, a participating representation satisfies Project FAR Axiom 3 only if it is interpreted within an investigation. Therefore, any architecture that removes Interpretation without supplying an accepted replacement can express marks or tokens but cannot express their meaning under the relevant investigation. Expressive power is reduced.

By the validated Axiom 4 consequence recorded in L-004, a scoped reasoning process satisfies Project FAR Axiom 4 only if it occurs within exactly one investigation. Therefore, any architecture that removes Investigation without supplying an accepted replacement cannot specify the reasoning objective or the conditions under which representations, interpretations, candidates, admissibility, and resolutions are defined. Expressive power is reduced.

By the validated Axiom 5 consequence recorded in L-005, a scoped reasoning process satisfies Project FAR Axiom 5 only if it proceeds according to a reasoning calculus governing its admissible reasoning transitions. Therefore, any architecture that removes Reasoning Calculus without supplying an accepted replacement cannot distinguish admissible from inadmissible transformations. Expressive power is reduced.

For every `p` in `P`, removing `p` without supplying an accepted replacement reduces expressive power relative to the Project FAR objective. By the stated deletion-only minimality standard, `P` is minimal relative to the current Project FAR scope, definitions, axioms, and deletion-only compression standard.

---

## Corollary

The current primitive architecture should not be compressed by deletion alone. Any successful compression must replace one primitive with a formally equivalent construction from weaker accepted foundations.

---

## Limitation

This theorem does not prove absolute metaphysical necessity. It proves framework-relative, deletion-only minimality. A future discovery layer may still derive or replace one or more primitives from deeper accepted concepts.
