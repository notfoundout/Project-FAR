# Audit: UPP-W2 RCCD-Independent Target Class

## Dependency

PR #281 registered the proof program. PR #282 established the typed metalanguage without proving RCCD. This workstream uses that foundation only to type membership evidence and decisions.

## Independence controls

- The membership classifier receives no RCCD mapping.
- The five criteria use alternatives, standards-based appraisal, response sensitivity, finite specification, and repeatability.
- RCCD component names and direct aliases are rejected from criterion text.
- Membership cannot be revised merely because a later RCCD theorem succeeds or fails.
- Class membership and theorem satisfaction remain distinct predicates.

## Boundary discipline

Accessible failure of any criterion yields Out of Scope. Inaccessible evidence yields Unknown. Unknown is not promoted to membership, exclusion, or RCCD support.

## Adversarial checks

The suite mutates each criterion independently, injects each forbidden RCCD term, tests inaccessible evidence, and verifies neutral criterion text. Positive, negative, and Unknown cases are all required.

## Outcome

`rccd_independent_target_class_defined_with_neutral_membership_and_unknown_boundary`

This establishes a neutral target-class predicate. It does not establish maximality, P*, E*, machinery closure, RCCD necessity, or the terminal theorem.
