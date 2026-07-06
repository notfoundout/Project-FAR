# T-001 — Conditional Primitive Minimality

## Status

Established relative to the current Project FAR scope and axioms.

This proof is conditional. It establishes minimality for the present architecture as specified by the current definitions and axioms. It does not prove that no future lower-level reduction can replace the primitive set.

---

## Statement

Let the primitive architecture of Project FAR be:

```text
P = { Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus }
```

Let the objective be representation of every reasoning process within the stated scope of Project FAR.

For each primitive `p` in `P`, removing `p` reduces expressive power relative to that objective.

Therefore, `P` is minimal relative to the current scope, definitions, and axioms.

---

## Dependencies

- `theory/definitions/definitions.md`
- `theory/axioms/axioms.md`
- `theory/semantics/scope.md`

---

## Proof

Assume a reasoning process `R` is within the stated Project FAR scope.

By Axiom 1, `R` admits one or more explicit representations. Therefore, any architecture that omits representation cannot express the explicit objects by which `R` is made analyzable. Removing Representation eliminates the basic object of analysis. Expressive power is reduced.

By Axiom 2, every collection of representations participating in `R` possesses a representational structure. Therefore, any architecture that omits Representational Structure can at most list representations without specifying their relations. But reasoning transitions, dependencies, ordering, conflict, support, and inferential connection require explicitly specified relations among representations. Removing Representational Structure eliminates the organization required to distinguish a structured argument from an unordered inventory of marks. Expressive power is reduced.

By Axiom 3, every representation participating in `R` is interpreted within an investigation. Therefore, any architecture that omits Interpretation can express marks or tokens but cannot express what those marks mean in the investigation. Because the same representation may receive different meanings under different interpretations, meaning is not recoverable from representation alone. Removing Interpretation eliminates semantic content. Expressive power is reduced.

By Axiom 4, every reasoning process occurs within exactly one investigation. Therefore, any architecture that omits Investigation cannot specify the reasoning objective or the conditions under which representations, interpretations, candidates, admissibility, and resolutions are defined. Without that context, the same representation and calculus may serve different objectives and produce different evaluative roles. Removing Investigation eliminates objective-relative evaluation. Expressive power is reduced.

By Axiom 5, every reasoning process proceeds according to a reasoning calculus governing its admissible reasoning transitions. Therefore, any architecture that omits Reasoning Calculus cannot distinguish admissible from inadmissible transformations. Without such a rule specification, the architecture can record representational change but cannot represent reasoning as governed transition. Removing Reasoning Calculus eliminates admissibility of inference. Expressive power is reduced.

For every `p` in `P`, removing `p` reduces expressive power relative to the Project FAR objective. By the definition of minimality, `P` is minimal relative to the current scope, definitions, and axioms.

---

## Corollary

The current primitive architecture should not be compressed by deletion alone. Any successful compression must replace one primitive with a formally equivalent construction from weaker foundations.

---

## Limitation

This theorem does not prove absolute metaphysical necessity. It proves framework-relative minimality. A future discovery layer may still derive one or more primitives from deeper concepts.
