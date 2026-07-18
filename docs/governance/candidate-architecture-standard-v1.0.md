# Candidate Architecture Standard v1.0

## Purpose

This standard governs how Project FAR registers, compares, revises, supersedes, rejects, and retires candidate reasoning architectures. It applies equally to FARA and every alternative candidate.

## Candidate lifecycle

Allowed statuses are:

- `proposed`
- `exploratory-admissible`
- `frozen-for-experiment`
- `actively-evaluated`
- `boundedly-supported`
- `unresolved`
- `dominated-within-declared-space`
- `superseded`
- `rejected-within-declared-scope`
- `retired`

No status implies global disproof unless a separately registered theorem or decisive evidence supports that conclusion.

## Required identity fields

Every candidate record must include:

- stable identifier;
- human-readable name;
- version;
- provenance;
- canonical specification links;
- primitive commitments;
- derived machinery;
- admissibility assumptions;
- intended scope;
- known limitations;
- current evidence status;
- related experiments;
- status history;
- confirmatory-comparison eligibility;
- unresolved questions;
- supersession links when applicable.

## Admission

A candidate is admissible for comparison only when:

1. its specification is sufficiently explicit to permit implementation or mapping;
2. primitive, derived, interpreter, hidden-state, exception, and adjudication costs can be counted;
3. it receives no candidate-specific preservation criteria;
4. assumptions and repair policies are explicit;
5. failures and unresolved mappings will be preserved; and
6. required evaluator blinding can be maintained.

## Revision and freeze

A material change after exposure to a frozen case creates a new candidate version. A frozen candidate may not be silently repaired. Historical versions, failed mappings, and unfavorable results remain preserved.

## Replacement

A candidate may replace FARA only within an explicitly declared scope and comparison space. Replacement requires evidence that the replacement:

- preserves at least the same registered commitments;
- contains no disallowed hidden reintroduction;
- has lower or equal full cost with at least one strict advantage, or satisfies another preregistered formal replacement relation;
- survives applicable negative controls;
- satisfies the required independence and replication standard; and
- does not depend on post hoc evaluation changes.

Bounded dominance does not establish global replacement.

## Equivalence

Two candidates may be marked `equivalence-conjectured` only when bidirectional admissible translations preserve the same registered commitments without ignoring hidden machinery or unequal cost. Formal equivalence requires a separately accepted theorem. Experimental indistinguishability alone is not formal equivalence.

## Rejection

A rejection record must identify:

- declared scope;
- failed commitments;
- evidence links;
- whether the failure concerns the architecture or only a mapping;
- whether repair creates a new version; and
- remaining uncertainty.

## Dominance

Dominance claims must use the frozen comparative cost model and preservation criteria. They must state the tested candidate set and scope. An unresolved competitor may not be described as defeated.

## FARA status

FARA is the current principal candidate, not the default winner. Its accepted evidence supports coherence, executability, and bounded successful representation at registered scopes. Universality, necessity, minimality, comparative economy, unique optimality, and general independent replication remain unestablished.

## CRE-004 separation

This registry must not expose the private identity mapping for blinded CRE-004 candidate labels. Coordinator-only keys remain governed by the frozen CRE-004 artifacts merged before this standard.
