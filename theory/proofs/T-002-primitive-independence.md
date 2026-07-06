# T-002 — Conditional Primitive Independence

## Status

Established relative to the current Project FAR definitions and reduction standard.

---

## Statement

Within the current framework, none of the five primitives is derivable from the other four without loss of expressive power:

```text
Investigation
Representation
Representational Structure
Interpretation
Reasoning Calculus
```

Therefore, the current primitive architecture is mutually independent relative to the present reduction standard.

---

## Dependencies

- `theory/definitions/definitions.md`
- `theory/axioms/axioms.md`
- `theory/proofs/T-001-primitive-minimality.md`

---

## Proof Method

For each primitive `p`, construct a countermodel containing the other four primitives but lacking `p`. If the countermodel fails to express a scoped reasoning process, then `p` is not derivable from the others under the current framework.

---

## Countermodels

### 1. No Representation

Let a structure contain an investigation, a representational structure schema, an interpretation function schema, and a reasoning calculus, but no representations.

There are no explicit distinguishable objects for the interpretation to assign meaning to, no elements for the structure to organize, and no states for the calculus to transform.

Therefore Representation is not derivable from the other four.

### 2. No Representational Structure

Let a structure contain representations, an investigation, an interpretation, and a reasoning calculus, but no explicitly specified relations among the representations.

The framework can identify tokens and meanings but cannot specify dependency, ordering, contradiction, support, transition, or inferential connection among them. Any attempted recovery of such organization must introduce relations among representations, which is exactly representational structure.

Therefore Representational Structure is not derivable from the other four.

### 3. No Interpretation

Let a structure contain representations, a representational structure, an investigation, and a reasoning calculus, but no mapping from representations to meanings.

The framework can describe formal marks and their relations but cannot determine whether a representation denotes a premise, candidate, observation, rule, objection, or conclusion. Since the same representation may have different semantic content under different interpretations, semantic content is underdetermined by structure alone.

Therefore Interpretation is not derivable from the other four.

### 4. No Investigation

Let a structure contain representations, a representational structure, an interpretation, and a reasoning calculus, but no specified reasoning objective or governing conditions.

The framework can express interpreted rule-governed transitions, but it cannot determine what objective the process is pursuing, which candidates are under consideration, which criteria are relevant, or what counts as resolution. The same interpreted calculus may serve proof, diagnosis, classification, or decision under different investigations.

Therefore Investigation is not derivable from the other four.

### 5. No Reasoning Calculus

Let a structure contain an investigation, representations, a representational structure, and an interpretation, but no rules governing admissible transitions.

The framework can express meaningful structured content in context, but it cannot distinguish valid inference, invalid inference, admissible transformation, inadmissible transformation, or resolution procedure. Any attempt to recover those distinctions must introduce rules of admissible reasoning, which is a reasoning calculus.

Therefore Reasoning Calculus is not derivable from the other four.

---

## Conclusion

Each primitive admits a countermodel in which the other four are present but the target primitive is absent and the architecture fails to represent scoped reasoning adequately.

Therefore the primitives are mutually independent relative to the current framework.

---

## Limitation

This is not a final proof of absolute irreducibility. It is an independence result under the present definitions. A future lower-level theory may still replace these primitives with deeper constructions.
