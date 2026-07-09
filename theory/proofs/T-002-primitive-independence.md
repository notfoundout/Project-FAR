# T-002 — Conditional Primitive Independence

## Status

Established relative to the current Project FAR definitions and reduction standard.

---

## Statement

Within the current framework and deletion-only reduction standard, none of the five primitives is eliminable in favor of the other four without loss of expressive power:

```text
Investigation
Representation
Representational Structure
Interpretation
Reasoning Calculus
```

Therefore, the current primitive architecture is deletion-independent relative to the present reduction standard. This does not prove absolute underivability from every possible future lower-level replacement theory.

---

## Dependencies

- `theory/definitions/definitions.md`
- `theory/axioms/axioms.md`
- `theory/proofs/T-001-primitive-minimality.md`

---

## Proof Method

For each primitive `p`, construct a deletion test case containing the other four primitives but lacking `p`. If the test case fails to express a scoped reasoning process and any attempted repair must reintroduce `p` or an accepted replacement for `p`, then `p` is not eliminable in favor of the other four under the current deletion-only reduction standard.

---

## Countermodels

### 1. No Representation

Let a structure contain an investigation, a representational structure schema, an interpretation function schema, and a reasoning calculus, but no representations.

There are no explicit distinguishable objects for the interpretation to assign meaning to, no elements for the structure to organize, and no states for the calculus to transform.

Therefore Representation is not eliminable in favor of the other four under the deletion-only reduction standard.

### 2. No Representational Structure

Let a structure contain representations, an investigation, an interpretation, and a reasoning calculus, but no explicitly specified relations among the representations.

The framework can identify tokens and meanings but cannot specify dependency, ordering, contradiction, support, transition, or inferential connection among them. Any attempted recovery of such organization must introduce relations among representations, which is exactly representational structure.

Therefore Representational Structure is not eliminable in favor of the other four under the deletion-only reduction standard.

### 3. No Interpretation

Let a structure contain representations, a representational structure, an investigation, and a reasoning calculus, but no mapping from representations to meanings.

The framework can describe formal marks and their relations but cannot determine whether a representation denotes a premise, candidate, observation, rule, objection, or conclusion. Since the same representation may have different semantic content under different interpretations, semantic content is underdetermined by structure alone.

Therefore Interpretation is not eliminable in favor of the other four under the deletion-only reduction standard.

### 4. No Investigation

Let a structure contain representations, a representational structure, an interpretation, and a reasoning calculus, but no specified reasoning objective or governing conditions.

The framework can express interpreted rule-governed transitions, but it cannot determine what objective the process is pursuing, which candidates are under consideration, which criteria are relevant, or what counts as resolution. The same interpreted calculus may serve proof, diagnosis, classification, or decision under different investigations.

Therefore Investigation is not eliminable in favor of the other four under the deletion-only reduction standard.

### 5. No Reasoning Calculus

Let a structure contain an investigation, representations, a representational structure, and an interpretation, but no rules governing admissible transitions.

The framework can express meaningful structured content in context, but it cannot distinguish valid inference, invalid inference, admissible transformation, inadmissible transformation, or resolution procedure. Any attempt to recover those distinctions must introduce rules of admissible reasoning, which is a reasoning calculus.

Therefore Reasoning Calculus is not eliminable in favor of the other four under the deletion-only reduction standard.

---

## Conclusion

Each primitive admits a countermodel in which the other four are present but the target primitive is absent and the architecture fails to represent scoped reasoning adequately.

Therefore the primitives are deletion-independent relative to the current framework and current reduction standard.

---

## Limitation

This is not a final proof of absolute irreducibility or absolute underivability. It is a deletion-independence result under the present definitions and current reduction standard. A future lower-level theory may still replace these primitives with deeper constructions if independently accepted.
