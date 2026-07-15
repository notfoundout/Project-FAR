# Proof Assurance Taxonomy

This taxonomy records proof-assurance method separately from theorem truth status.

| Assurance level | Meaning |
|---|---|
| narrative_argument | A prose proof or argument is present. |
| structurally_checked_proof_object | A YAML proof object is structurally valid: references, required fields, rule labels, and local lineage constraints are checked. This is not a machine-verified formal proof. |
| semantically_constrained_proof_object | Structural checks plus repository-defined semantic rule-pattern constraints are checked. This is still not a proof-assistant verification. |
| machine_verified_formal_proof | A proof assistant or formal verifier checks the theorem in a formal system. No current Project FAR theorem has this assurance level. |
| independently_reviewed_proof | Independent reviewers have reviewed the proof under a documented protocol. Unknown unless explicitly recorded. |

Theorem metadata must separately record theorem status, scope, theorem category, assumptions, counterexample or falsifiability condition where applicable, proof-assurance level, and review status.
