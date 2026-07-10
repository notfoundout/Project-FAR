# External Validation: Euclidean Geometry

## Target System

Euclidean geometry reasons from definitions, common notions, postulates, constructed figures, and diagram-independent proofs.

## FAR Mapping

| FAR role | Target-system realization |
| --- | --- |
| Representation | point, line, angle, triangle, equality claim, construction step |
| Representational structure | incidence, betweenness, congruence, proof order, diagram relations |
| Interpretation | Euclidean plane or specified geometric model |
| Investigation | prove a target geometric relation |
| Reasoning calculus | accepted definitions, postulates, common notions, and proved results |
| Operation | construction, comparison, substitution, congruence inference, deduction |

## Valid Case

Claim: Base angles of an isosceles triangle are equal.

Given triangle ABC with AB = AC, compare the triangle with the correspondence B ↔ C. Using accepted congruence conditions and equality preservation, infer ∠ABC = ∠BCA.

FAR can represent the objects, equality premise, correspondence, permitted congruence reasoning, and final proof trace.

Result: PASS.

## Invalid Case

Claim: Every triangle with two visually similar sides is isosceles.

A drawing is not a proof that the side lengths are equal. FAR can distinguish the diagram as a representation from the interpreted metric relation required by the claim.

Result: PASS.

## Malformed or Scope-Violating Case

A proof uses the parallel postulate while claiming to operate in a neutral geometry that has not assumed it.

FAR can represent the step but classify it as outside the supplied calculus and investigation scope.

Result: PASS.

## Limitations

FAR does not supply Euclidean postulates, congruence theorems, construction rules, or a geometric model. Those must be supplied by the target theory.

## Final Outcome

CONDITIONAL PASS

Condition: the geometric definitions, model assumptions, postulates, and admissible proof rules must be explicit.
