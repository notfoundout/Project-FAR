# Audit — USD-W1 semantic-change extension

## Scope integrity

Admission is defined independently of the candidate vocabulary by effective versioned semantic interfaces, explicit transition maps, append-only history, and finite recoverable dependency cones. No FARA primitive appears in the admission rule.

## Construction audit

The constructor is uniform over `S_sem_eff`. It carries source-declared version and translation data without a source-specific decoder, future-semantics oracle, or new target primitive.

## Preservation audit

The proof separately checks denotation, inferential role, transition classification, commitments, grounds, dependencies, historical reasons, rejected alternatives, and unresolved translations. Shared labels are never used as evidence of semantic identity.

## Negative-control audit

The label-collapse control loses changed denotation and inference. The erase-history control loses why earlier commitments were licensed. Oracle-defined equivalence and unbounded retroactive rewriting remain explicit boundaries rather than post hoc repairs.

## Classification audit

`extension_proved` would overstate the result because major semantic-change families are excluded. `countermodel` is false because all admitted fixtures satisfy the construction. The correct terminal outcome is `proper_subclass_only`.

## Claim-boundary audit

The result advances one feature subclass only. It does not establish all semantic change, `S_IRD`, universal structure, necessity, minimality, uniqueness, actual-process correspondence, mechanization, or independent review.
