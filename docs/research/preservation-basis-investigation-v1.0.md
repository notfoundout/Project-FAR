# Preservation Basis Investigation v1.0

## Status

Frozen prospective result of Milestone 3 of the Architecture-Neutral Research Roadmap.

This investigation derives a candidate preservation basis from the frozen reasoning domain and IRD-001. It does not prove that the basis is sufficient, necessary, independent, minimal, or uniquely correct.

## Purpose

A candidate representation cannot be evaluated rigorously until the project states what must survive translation. Earlier comparative work used six dimensions: structural, semantic, operational, dependency, information, and historical preservation. Those dimensions were useful, but they were inherited before the architecture-neutral reasoning domain and IRD-001 existed.

This investigation asks:

1. Which preservation obligations follow from IRD-001 rather than from FARA?
2. Which inherited dimensions remain justified?
3. Which are composite, redundant, underspecified, or incomplete?
4. What prospective basis should govern the next representation-theorem and candidate-comparison work?

## Inputs

This investigation depends only on:

- `docs/research/reasoning-domain-specification-v1.0.md`;
- `docs/research/independent-reasoning-definition-v1.0.md`;
- the external-observation, negative-control, cost, and anti-reintroduction standards;
- prior preservation dimensions as objects of comparison, not as authoritative conclusions.

FARA primitives, FARO implementation structure, and prior favorable mappings are not derivation inputs.

## Derivation rule

A preservation obligation is admitted only when failure to preserve it can change at least one of the following under IRD-001:

- whether R1-R6 are satisfied;
- which alternatives are live;
- what grounds bear on which commitments;
- which transitions are admissible;
- what commitment consequence occurs;
- which historical path produced the consequence;
- what evidential grade can legitimately be claimed.

A distinction is not admitted merely because FARA names it or because an existing implementation stores it.

## PB-001 candidate preservation basis

The prospective basis contains eight axes.

### P1 — Configuration preservation

Preserve the distinctions among relevant process states, participants, resources, externalized state, and relations needed to identify an episode and its evolution.

Failure example: merging two participants or two states that differ in available grounds or future actions.

IRD motivation: process states, histories, distributed and embodied cases.

### P2 — Commitment preservation

Preserve what is maintained, accepted, rejected, compared, suspended, revised, or otherwise treated as a commitment, including uncertainty or partial commitment where relevant.

Failure example: representing acceptance, rejection, and suspension as the same undifferentiated token.

IRD motivation: R2 and R5.

### P3 — Stake-and-alternative preservation

Preserve the question, objective, issue, decision, explanatory demand, or other stake relative to which alternatives are evaluated, together with the distinctions among live alternatives.

Failure example: preserving a final choice while erasing that different alternatives were available under a different question or objective.

IRD motivation: R1 and R2.

### P4 — Ground-and-justification preservation

Preserve which observations, assumptions, reasons, evidence, constraints, models, rules, or prior states bear on which commitments, and with what justificatory role when the source supports that distinction.

Failure example: retaining all facts but losing which fact supported, defeated, qualified, or was irrelevant to a conclusion.

IRD motivation: R3 and R6.

### P5 — Admissibility-and-dynamics preservation

Preserve the transformations available to the process, the conditions under which they are admissible, and material differences among fixed, defeasible, stochastic, resource-bounded, action-coupled, or self-modifying evolution.

Failure example: reproducing observed outputs with a lookup table that does not preserve the source process's allowed future transitions.

IRD motivation: R3, R4, admissible evolutions, self-modification, and counterfactual pressure.

### P6 — Consequence preservation

Preserve the material consequence of the episode for later commitment, action, inquiry, policy, proof status, explanation, or decision. Output equality alone is insufficient when downstream commitments differ.

Failure example: two systems emit the same sentence, but one treats it as a tentative hypothesis and the other as a binding decision.

IRD motivation: R5.

### P7 — Historical and path preservation

Preserve ordering, revision, retraction, provenance, supersession, and path-dependent constraints whenever different histories license different current or future states.

Failure example: representing a revised rule set as if the new rule had always been active.

IRD motivation: histories, nonmonotonicity, learning, self-revision, and distributed asynchronous reasoning.

### P8 — Evidential-correspondence preservation

Preserve the boundary between what is observed, reported, instrumented, specified, inferred, or formally linked to the process. A representation may not upgrade O0/O1 evidence into an E1/E2 internal-process claim.

Failure example: treating a fluent post hoc explanation as a verified trace of the computation that produced the answer.

IRD motivation: R6, E0-E2, O0-O4, opaque systems, human introspection, and neural reasoning claims.

## Treatment of the inherited six dimensions

### Structural preservation

**Disposition: retained but narrowed into P1.**

Structure remains necessary as a family of distinctions, but it must be tied to consequences for IRD-001 rather than preserved indiscriminately.

### Semantic preservation

**Disposition: split.**

The inherited semantic dimension conflated at least commitment content, stake, alternatives, and consequence. These are separated into P2, P3, and P6 because each can vary independently in relevant cases.

### Operational preservation

**Disposition: retained and sharpened into P5.**

Operation must include admissibility, counterfactual future transitions, resource conditions, stochasticity, and self-modification—not only the observed transition sequence.

### Dependency preservation

**Disposition: retained and sharpened into P4.**

Dependency must distinguish support, defeat, qualification, constraint, provenance, and unresolved justificatory role when source observability permits.

### Historical preservation

**Disposition: retained as P7.**

History remains separately required because current-state equivalence does not preserve revision, provenance, or path-dependent admissibility.

### Information preservation

**Disposition: reclassified as an aggregate adequacy criterion, not a coordinate.**

“Information preservation” is true exactly to the extent that all claim-relevant distinctions are retained. Used as a separate axis, it either duplicates the other dimensions or becomes an unconstrained catch-all that cannot be independently scored.

Future work may report an aggregate no-relevant-loss judgment derived from P1-P8, but it must not count that aggregate as additional evidence of independence or dimensional coverage.

## Why P3, P6, and P8 are added

### Stake and alternatives

Two episodes may preserve identical propositions, operations, and dependency graphs while answering different questions or evaluating different alternative sets. IRD-001 makes the situated stake and alternative-sensitive commitment space constitutive, so they cannot remain implicit.

### Consequence

A final output is not equivalent to the commitment consequence attached to it. Tentative belief, proof acceptance, action authorization, policy adoption, and public strategic assertion may share content while differing materially.

### Evidential correspondence

The same represented trace can support different claims depending on whether it is self-report, instrumentation, white-box specification, or proved correspondence. This is not ordinary process history or dependency; it governs what the representation is evidence of.

## Candidate-neutrality audit

PB-001 does not require:

- FARA's five primitives;
- symbolic or propositional representations;
- centralized agency;
- deterministic transitions;
- fixed goals, rules, or representational types;
- complete internal observability;
- a single implementation formalism.

Each axis is motivated by IRD-001 or the frozen domain. Alternative candidate architectures may satisfy the basis using entirely different primitive decompositions.

## Nontriviality and anti-collapse requirements

A mapping fails preservation when it relies on any of the following without counting and exposing the machinery:

- output-only lookup;
- unrestricted metadata smuggling;
- hidden interpreter or operator;
- post hoc semantic labels with no operational commitment;
- collapsed alternatives reconstructed only by the evaluator;
- history erased from the representation but recovered from external narrative;
- evidential grade upgraded without a correspondence argument;
- one universal opaque state whose decoder contains the entire source system.

## Scoring status

Each axis may receive:

- `pass` — all preregistered distinctions for that axis are demonstrably retained;
- `partial` — some required distinctions are retained and the loss is bounded explicitly;
- `fail` — a required distinction is demonstrably collapsed, invented, or contradicted;
- `unknown` — the available observation contract does not resolve the judgment.

`unknown` is not ordered between `partial` and `fail`.

A basis-level result must report the full vector. It may not replace the vector with an unregistered scalar score.

## Sufficiency, independence, and minimality test program

PB-001 is only a derived candidate basis. It must undergo four separate tests.

### Coverage test

For D1-D16, boundary cases, mandatory countermodels, and cross-cutting axes, identify whether every claim-relevant distinction is assigned to at least one preservation axis.

### Independence test

For each Pi, construct paired source systems that differ only in Pi while matching on the other seven as far as the frozen construction permits. If no such pair can exist, Pi may be derivable or redundant.

### Ablation test

Remove Pi from the evaluation basis and determine whether a candidate can pass while collapsing a distinction required by IRD-001.

### Addition search

Adversarially search for paired reasoning systems that match on P1-P8 but remain materially different under IRD-001. A successful pair indicates incompleteness.

## Prospective decision rules

- An axis is **retained provisionally** when it has direct IRD motivation and at least one planned discriminating pair.
- An axis is **redundant within the tested space** only if its distinctions are derivable from the remaining axes under explicit assumptions.
- The basis is **incomplete** if a materially different IRD-001 episode pair matches on all registered axes.
- The basis is **sufficient within a declared scope** only after all registered coverage and addition-search cases are resolved without an uncovered distinction.
- The basis is **minimal within a declared search space** only after every axis survives ablation and no lower-cost alternative basis matches its coverage.

## Current result

The inherited six-dimensional vector should not be treated as the final preservation basis.

The strongest justified prospective position is:

- structural, operational, dependency, and historical preservation remain justified but require sharper definitions;
- semantic preservation must be decomposed;
- information preservation is an aggregate no-loss criterion rather than an independent dimension;
- stake/alternatives, commitment consequences, and evidential correspondence must be tested explicitly;
- PB-001 with P1-P8 is the frozen candidate basis for the next test program.

## Allowed unfavorable outcomes

Later work may establish that:

- one or more P1-P8 axes are redundant;
- P1-P8 is incomplete;
- different reasoning classes require different preservation bases;
- no finite preservation basis captures the full frozen domain;
- IRD-001 itself requires revision;
- the evidence remains insufficient.

## Revision policy

Material changes create a new PB version. Earlier versions and failed tests remain preserved. No axis may be added, removed, merged, or redefined after benchmark exposure without an explicit supersession record and scope-impact statement.

## Nonclaims

This investigation does not establish:

- PB-001 sufficiency, necessity, independence, or minimality;
- a representation theorem;
- FARA compliance with PB-001;
- FARA universality, necessity, minimality, superiority, or economy;
- closure of the preservation search space;
- independent replication.

## Next required milestone

Construct a frozen preservation-basis test suite containing discriminating pairs, ablations, addition-search challenges, and domain-coverage records for P1-P8 before using PB-001 in a representation theorem.