# Deduction-First Research Shift Audit

## Scope

This audit reviews the governance change that makes deduction the primary route to Project FAR's central answer while retaining empirical evaluation, independent replication, and external review as separate supporting dimensions.

## Question audited

Does the repository now distinguish correctly between:

1. establishing a mathematical result from definitions and assumptions; and
2. independently checking, replicating, applying, or challenging that result?

## Result

**PASS for prospective governance and dependency restructuring.**

The change does not establish any theorem. It establishes the order and claim boundaries under which theorem work may proceed.

## Primary dependency audit

The repository now registers the central dependency chain as:

`formal domain → source definition → theorem target and premise ledger → faithful-representation definition → construction and obstruction lemmas → theorem or refutation → lower bounds → minimality/equivalence/impossibility → mechanization → independent proof review`.

PBTS-001 replication is recorded as a parallel supporting track rather than a parent dependency of theorem construction.

This resolves the prior roadmap dependency under which three independent PBTS submissions were required before representation-theorem work could begin.

## Evidence-role audit

The deduction-first standard separates:

- proof and refutation;
- mechanized proof verification;
- independent proof review;
- empirical replication;
- implementation and application validation.

These are no longer collapsed into one evidence status.

Formal proof may establish only what follows from its declared assumptions and scope. Replication may establish reproducibility of a frozen evaluation. Mechanization may establish correctness of an encoding relative to its trusted kernel and axioms. Independent review may strengthen confidence or expose an error.

None is silently substituted for another.

## Replication-preservation audit

The following artifacts remain unchanged and valid within their original scope:

- PBTS-001;
- PBTS-001 internal RUN-001;
- `PBTS-001-REP-001` independent replication package;
- `PBTS-001-REP-001-RUN-001` coordinator controls;
- empty append-only participant and result channels;
- all replication nonclaims and false gates.

The shift does not claim that independent replication occurred. It does not weaken the requirements for an R3, R4, or R5 claim.

It changes only the proposition gated by replication: independent empirical confirmation remains blocked, while proof construction is authorized.

## Anti-self-validation audit

The Anti-Self-Validation Standard remains applicable to empirical confirmation and independent-review claims.

The shift does not permit:

- one agent to simulate multiple independent replicators;
- project-authored implementations to be relabeled as external confirmation;
- agreement among internally generated evaluators to establish universality;
- the project to claim independent proof verification without external review.

The project may author a proof, as mathematical research ordinarily requires. Whether that artifact is valid depends on the derivation, assumptions, and definitions. Independent review remains a separate status.

## Theorem-gate audit

The research gate registry now contains separate gates for:

- formal theorem target;
- premise ledger and semantics;
- faithful-representation definition;
- scoped representation proof;
- primitive lower bounds;
- minimality universe and proof;
- mechanized proof verification;
- independent proof review.

All remain unsatisfied.

The independent-replication gate now gates only `independent_empirical_confirmation_claim`.

No theorem gate has been opened by this PR.

## Central-claim audit

The central claim registry now records, for every major claim:

- a primary resolution mode;
- the next formal task;
- supporting validation;
- a falsification condition;
- nonclaims.

It also separates:

- theorem status;
- mechanization status;
- independent proof-review status;
- empirical replication status;
- application status.

Existence, universality, necessity, and minimality remain unresolved or not established.

## PB-001 and P8 audit

PB-001 remains a candidate preservation basis, not a proved basis.

The theorem program must determine whether PB-001, a versioned revision, or another basis supplies the required preservation obligations.

P8 remains unresolved. A completed theorem must classify it as one of:

- an ordinary preservation coordinate;
- a cross-cutting theorem side condition;
- a separate evidential-correspondence theorem;
- a revision requirement;
- an explicit blocker preventing theorem completion.

The governance shift does not resolve P8 by declaration.

## Machine-enforcement audit

`tools/check_research_gates.py` now validates:

- all original empirical gates;
- all deduction-first theorem gates;
- the separation of theorem and validation claim dimensions;
- the policy that proof construction is not blocked by empirical replication;
- the policy that independent replication gates only independent empirical confirmation;
- explicit primary-resolution and supporting-validation fields for central claims.

`tools/check_deduction_first_program.py` additionally validates:

- canonical deduction-first documents exist;
- the central program, priority reset, proof roadmap, architecture-neutral roadmap, and README state the same dependency structure;
- the obsolete replication-before-theorem wording is absent;
- `THM-TARGET-001` is the immediate central artifact;
- theorem gates remain unsatisfied;
- no central theorem claim is promoted.

Both validators are wired into `make research-check`, `make health-fast`, and `make health`.

## Preserved baseline

This change does not modify:

- Foundation v1.0 mathematics;
- FARA or FARO primitives;
- IRD-001;
- PB-001;
- PBTS-001 cases or results;
- CRE results;
- prior failures, unknowns, partial results, countermodels, or nonclaims;
- replication participant records, which remain empty.

No earlier evidence is deleted or reclassified as proof.

## Immediate next artifact

The next central scientific artifact is `THM-TARGET-001`.

It must freeze:

- the exact theorem family;
- source scope;
- target structure;
- representation relation;
- preservation obligations;
- premise classifications;
- P8 alternatives;
- nontriviality exclusions;
- failure conditions;
- nonclaims.

It must not claim that the theorem is proved.

## Nonclaims

This governance shift does not establish:

- a common structure of reasoning;
- FARA faithful representability;
- universality;
- primitive necessity or independence;
- minimality or uniqueness;
- P8 resolution;
- mechanized proof verification;
- independent proof review;
- independent empirical replication.

It authorizes the correct next kind of work: deduction directed at a precisely frozen question.