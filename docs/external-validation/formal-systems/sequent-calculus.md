# Sequent Calculus Validation

## Test Case

Target sequent:

`P ∧ Q ⊢ P`

Representative derivation:

1. Begin with the identity sequent `P ⊢ P`.
2. Apply left weakening or the relevant conjunction-left rule to obtain `P ∧ Q ⊢ P`, depending on the selected sequent calculus presentation.

## FAR Mapping

| FAR role | Target-system counterpart |
| --- | --- |
| Investigation | Derive the target sequent under the selected sequent calculus. |
| Representation | Formula occurrences, contexts, turnstile, and proof-tree nodes. |
| Representational structure | Ordered or multiset contexts, antecedent/succedent position, and proof-tree parent/child relations. |
| Interpretation | Semantic structures used when proving soundness or completeness. |
| Reasoning calculus | Structural and logical sequent rules. |
| Operation | Application of a sequent rule. |
| Admissibility | Satisfaction of the selected rule schema and side conditions. |
| Reasoning state | Current open sequents in the proof search. |
| Transition | Replacement of an open goal by its rule premises, or construction of a conclusion from proven premises. |
| Resolution | A closed proof tree with no unresolved leaves. |

## Structural Test

Sequent calculus tests FAR against branching rather than linear reasoning. A proof is naturally represented as a tree. Reasoning state may contain multiple open sequents, and one rule application can replace one goal with several subgoals.

This shows that FAR operations and transitions cannot be restricted to single-input, single-output linear changes. The frozen framework permits structured states and mappings, so no revision is required.

## Pressure Findings

1. Reasoning processes may branch and later reconverge; chronological sequence alone is not enough to represent dependency.
2. The antecedent and succedent are structural positions, not semantic meanings by themselves.
3. Structural rules differ across calculi. FAR must remain neutral as to whether weakening, contraction, or exchange is permitted.
4. Proof search direction and proof-justification direction can be opposite while describing the same proof object.

## Counterexample Search

No structural counterexample was found. Branching proof states fit FAR if representational structure includes graph or tree relations rather than only linear order.

## Result

**PASS WITH LIMITATION**

Foundation v1.0 covers the tested sequent-calculus proof. The limitation is that a concrete FAR implementation must support branching proof states and must not assume every reasoning trace is a simple list.
