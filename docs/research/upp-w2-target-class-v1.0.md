# UPP-W2 Target Class C*

## Purpose

Define the domain of the universal theorem without selecting systems by RCCD structure.

## Membership rule

A system belongs to C* when accessible evidence establishes all five conditions:

1. It presents distinguishable response alternatives in an assessment context.
2. At least one alternative admits appraisal as permitted, prohibited, better supported, or worse supported under an explicitly supplied standard.
3. Altering the supplied grounds or standard can alter which response is permitted or warranted.
4. The facts needed for one membership decision are finitely specifiable.
5. Repeating the same stated assessment determines the same membership result in principle.

These conditions refer to assessment behavior, not to commitments, transition constraints, dependencies, histories, recovery procedures, or RCCD labels.

## Three-valued disposition

- `in_scope`: all five criteria are established.
- `out_of_scope`: accessible evidence defeats at least one criterion.
- `unknown`: evidence required to adjudicate a criterion is inaccessible.

Unknown is not treated as membership and is not treated as exclusion.

## Neutrality tests

The executable classifier does not accept an RCCD mapping as input. Renaming symbols and changing implementation medium do not change membership. Failure of a later RCCD lemma cannot remove a system from C*. Membership and theorem satisfaction are separate predicates.

## Boundary results

Finite rule adjudicators, Bayesian choice updaters, legal permission evaluators, and self-modifying planners can satisfy the criteria. A thermostat without an appraisal standard, a random symbol generator, a fixed lookup response with no alternatives, and an uninterpreted state machine do not. Opaque learned systems and tacit human judgments remain Unknown when the required facts cannot be discriminated.

## Claim boundary

This workstream defines C*. It does not prove RCCD, establish class maximality, define P* or E*, or authorize public evaluation.
