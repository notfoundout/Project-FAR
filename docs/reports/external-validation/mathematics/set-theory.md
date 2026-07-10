# External Validation: Elementary Set Theory

## Target System

Elementary set theory reasons about membership, subsets, unions, intersections, functions, relations, and cardinal constructions under a specified axiom system.

## FAR Mapping

| FAR role | Target-system realization |
| --- | --- |
| Representation | set symbol, element, membership claim, subset claim, ordered pair, function |
| Representational structure | membership relation, inclusion relation, set-builder condition, proof sequence |
| Interpretation | a specified set-theoretic universe or model |
| Investigation | prove equality, inclusion, existence, or non-existence |
| Reasoning calculus | selected set axioms, definitions, and logical rules |
| Operation | element selection, membership substitution, comprehension under permitted scope, extensional comparison |

## Valid Case

Claim: A ∩ B ⊆ A.

Let x be arbitrary and assume x ∈ A ∩ B. By the definition of intersection, x ∈ A and x ∈ B. Therefore x ∈ A. Since x was arbitrary, A ∩ B ⊆ A.

FAR can represent the arbitrary element, membership assumptions, definitional unpacking, and universal conclusion.

Result: PASS.

## Invalid Case

Claim: If A ∈ B, then A ⊆ B.

Membership and subset are distinct relations. A counterexample can be constructed where A is an element of B but some element of A is not an element of B. FAR preserves the relational distinction and rejects the inference.

Result: PASS.

## Malformed or Scope-Violating Case

A proof forms the unrestricted set of all sets that do not contain themselves while claiming to remain inside an axiom system that restricts comprehension.

FAR can represent the attempted construction but classify it as unavailable under the supplied set-theoretic calculus.

Result: PASS.

## Limitations

FAR does not choose among ZF, ZFC, type theory, or other foundations, and it does not establish consistency or independence results for them. The chosen axioms and model assumptions must be supplied.

## Final Outcome

CONDITIONAL PASS

Condition: the set-theoretic universe, axiom system, definitions, and admissible comprehension principles must be explicit.
