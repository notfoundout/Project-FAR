# Architecture-Neutral Research Roadmap

## Purpose

This roadmap orders the scientific work required to determine whether any genuine common structure of reasoning exists and whether FARA is universal, bounded, nonminimal, replaceable, equivalent to alternatives, or false as a universal account.

Each milestone must preserve favorable, unfavorable, and unresolved outcomes.

## Milestone 1 — Architecture-neutral reasoning domain

**Status:** complete prospectively through `docs/research/reasoning-domain-specification-v1.0.md` and `theory/evaluation/reasoning-domain-registry.json`.

**Result:** sixteen target classes, fourteen cross-cutting variation axes, unresolved boundary classes, five observability strata, revision controls, and a candidate-neutrality audit are registered.

**Cannot establish alone:** a mathematical definition of reasoning, universality, necessity, or minimality.

## Milestone 2 — Independent mathematical definition of reasoning

**Status:** complete prospectively through `docs/research/independent-reasoning-definition-v1.0.md` and `theory/evaluation/independent-reasoning-definition-registry.json`.

**Result:** IRD-001 defines a candidate-neutral process presentation and six reasoning conditions, with E0-E2 evidential grades and mandatory countermodels.

**Cannot establish alone:** that R1-R6 are sufficient, necessary, independent, minimal, or faithfully represented by FARA.

## Milestone 3 — Preservation-basis investigation

**Status:** derivation phase complete prospectively through `docs/research/preservation-basis-investigation-v1.0.md` and `theory/evaluation/preservation-basis-registry.json`.

**Result:** PB-001 registers eight candidate preservation axes:

1. configuration;
2. commitment;
3. stake and alternatives;
4. grounds and justification;
5. admissibility and dynamics;
6. consequence;
7. history and path;
8. evidential correspondence.

The inherited information-preservation dimension is reclassified as an aggregate no-relevant-loss criterion rather than an independent coordinate. Structural, operational, dependency, and historical preservation are retained in sharpened form. The inherited semantic dimension is decomposed.

**Current status:** PB-001 is derived and frozen for testing, but is not established as sufficient, necessary, independent, minimal, or complete.

**Next required work:** construct the frozen preservation-basis test suite with domain coverage, paired independence cases, axis ablations, and adversarial addition-search challenges.

## Milestone 4 — Preservation-basis test suite

**Entrance:** PB-001 derivation merged and frozen.

**Goal:** test whether P1-P8 are sufficient within declared scopes, independently discriminating, nonredundant, and resistant to uncovered distinctions.

**Required artifacts:**

- at least one discriminating pair per axis where constructible;
- explicit impossibility or dependence argument where a clean pair cannot be constructed;
- one ablation challenge per axis;
- coverage records for D1-D16, boundary classes, and mandatory IRD countermodels;
- adversarial pairs designed to match on P1-P8 while differing materially under IRD-001;
- hidden-recovery and evaluator-repair checks;
- immutable favorable, unfavorable, and unresolved classifications.

**Favorable result:** PB-001 survives the frozen test suite within a declared scope.

**Unfavorable result:** one or more axes are redundant, PB-001 is incomplete, different domain classes require different bases, or no finite basis survives.

**Cannot establish alone:** FARA compliance, universality, primitive necessity, minimality, superiority, or independent replication.

## Milestone 5 — Scoped representation theorem

Prove or refute a nontrivial faithful representation theorem from IRD-001 or a justified revision into FARA using a preservation basis that has survived its registered tests. Placeholder, label-only, lookup, hidden-interpreter, or evaluator-repaired inhabitation is excluded.

## Milestone 6 — Candidate architecture schema and compiler contracts

Create a candidate-neutral formal schema enabling multiple architectures to be specified, frozen, compiled, and evaluated uniformly. The governance registry is not a substitute for this formalism.

## Milestone 7 — Primitive ablation and lower bounds

Remove or reconstruct every FARA primitive under anti-reintroduction and full-cost accounting. Classify each as necessary within scope, derivable, replaceable, unresolved, or unnecessary.

## Milestone 8 — Strong competitor completion

Resolve the compact alternatives left unresolved by CRE-003 and successor work. Unresolved candidates remain live competitors until evidence changes their status.

## Milestone 9 — Exhaustive bounded small-system search

Define a finite universe of small reasoning systems, enumerate it completely, and test all admitted candidates or candidate families. Publish coverage limits and generation rules.

## Milestone 10 — Minimal counterexample generation

For each failure, produce or approximate the smallest counterexample and classify whether it defeats a mapping, candidate, preservation basis, domain definition, independent definition, or universal finite-architecture hypothesis.

## Milestone 11 — Equivalence and dominance analysis

Separate syntactic similarity, experimental indistinguishability, bidirectional translation, scoped Pareto dominance, and formally proved equivalence.

## Milestone 12 — Impossibility and no-go results

Search for conditions proving that no finite architecture can preserve all accepted commitments, or that incompatible reasoning classes require incompatible primitive distinctions.

## Milestone 13 — Independent replication and adversarial holdouts

Execute frozen packages at the strongest available independence level, including private holdouts and permanent publication of failures and unresolved outcomes.

## Milestone 14 — Central decision assessment

Update the central claim registry and candidate registry. Allowed conclusions include:

- FARA supported within a proven scope;
- FARA replaced within a declared scope;
- multiple candidates equivalent or incomparable;
- only bounded architectures exist;
- no finite universal architecture exists under stated assumptions;
- evidence remains insufficient.

## Dependency order

The frozen domain precedes IRD-001. IRD-001 precedes preservation-basis derivation. PB-001 derivation precedes its test suite. A preservation basis must survive registered tests before supporting representation-theorem claims. Candidate, ablation, and competitor milestones define architectural pressure. Bounded search, counterexample, equivalence, and impossibility milestones investigate the formal space. Independent replication supplies external evidential force. The final assessment records only the strongest justified conclusion.

## Paused work

Certification expansion, new dashboards, release packaging, favorable-case accumulation, generic exposition, and unrelated applications remain paused unless required to execute or verify an active milestone.

## Immediate next PR

Construct and freeze the PB-001 preservation-basis test suite. Do not begin the FARA representation theorem until P1-P8 have undergone registered coverage, independence, ablation, and adversarial addition-search tests.