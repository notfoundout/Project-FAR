# Architecture-Neutral Research Roadmap

## Purpose

This roadmap orders the scientific work required to determine whether any genuine common structure of reasoning exists and whether FARA is universal, bounded, nonminimal, replaceable, equivalent to alternatives, or false as a universal account.

Each milestone must preserve favorable, unfavorable, and unresolved outcomes.

## Milestone 1 — Architecture-neutral reasoning domain

**Status:** complete prospectively through `docs/research/reasoning-domain-specification-v1.0.md` and `theory/evaluation/reasoning-domain-registry.json`.

**Goal:** freeze independently justified target classes, boundary cases, observability limits, exclusion rules, and admission controls without defining reasoning through FARA-native primitives.

**Result:** sixteen target classes, fourteen cross-cutting variation axes, unresolved boundary classes, five observability strata, revision controls, and a candidate-neutrality audit are registered.

**Cannot establish alone:** a mathematical definition of reasoning, universality, necessity, or minimality.

## Milestone 2 — Independent mathematical definition of reasoning

**Entrance:** Milestone 1 domain specification merged and frozen.

**Goal:** propose one or more mathematical classes that address the frozen target domain without deriving their required structure from FARA.

**Required artifacts:** formal definitions, axioms or admissibility conditions, mappings from target classes to the proposed abstraction, exclusions and counterexamples, clause-level candidate-neutrality audit, and unresolved-case ledger.

**Favorable result:** a nontrivial architecture-neutral class covers the justified domain under explicit assumptions.

**Unfavorable result:** no single nontrivial class covers the domain without embedding a candidate ontology or collapsing relevant distinctions.

**Unresolved result:** multiple defensible classes remain, or some target classes cannot yet be classified.

**May update:** scope, existence research design, and the domain-definition dependency.

**Cannot establish alone:** FARA universality, necessity, minimality, or comparative superiority.

## Milestone 3 — Preservation-basis investigation

Determine whether the current preservation dimensions are sufficient, independent, redundant, or incomplete. The number six is a hypothesis, not a protected result.

## Milestone 4 — Scoped representation theorem

Prove or refute a nontrivial faithful representation theorem from an independent reasoning class into FARA. Placeholder or label-only inhabitation is excluded.

## Milestone 5 — Candidate architecture schema and compiler contracts

Create a candidate-neutral formal schema enabling multiple architectures to be specified, frozen, compiled, and evaluated uniformly. The governance registry is not a substitute for this formalism.

## Milestone 6 — Primitive ablation and lower bounds

Remove or reconstruct every FARA primitive under anti-reintroduction and full-cost accounting. Classify each as necessary within scope, derivable, replaceable, unresolved, or unnecessary.

## Milestone 7 — Strong competitor completion

Resolve the compact alternatives left unresolved by CRE-003 and successor work. Unresolved candidates remain live competitors until evidence changes their status.

## Milestone 8 — Exhaustive bounded small-system search

Define a finite universe of small reasoning systems, enumerate it completely, and test all admitted candidates or candidate families. Publish coverage limits and generation rules.

## Milestone 9 — Minimal counterexample generation

For each failure, produce or approximate the smallest counterexample and classify whether it defeats a mapping, candidate, preservation basis, domain definition, or universal finite-architecture hypothesis.

## Milestone 10 — Equivalence and dominance analysis

Separate syntactic similarity, experimental indistinguishability, bidirectional translation, scoped Pareto dominance, and formally proved equivalence.

## Milestone 11 — Impossibility and no-go results

Search for conditions proving that no finite architecture can preserve all accepted commitments, or that incompatible reasoning classes require incompatible primitive distinctions.

## Milestone 12 — Independent replication and adversarial holdouts

Execute frozen packages at the strongest available independence level, including private holdouts and permanent publication of failures and unresolved outcomes.

## Milestone 13 — Central decision assessment

Update the central claim registry and candidate registry. Allowed conclusions include:

- FARA supported within a proven scope;
- FARA replaced within a declared scope;
- multiple candidates equivalent or incomparable;
- only bounded architectures exist;
- no finite universal architecture exists under stated assumptions;
- evidence remains insufficient.

## Dependency order

The frozen domain precedes the mathematical definition. The independent definition precedes representation-theorem and exhaustive-search claims. Preservation-basis work precedes final preservation claims. Candidate, ablation, and competitor milestones define architectural pressure. Bounded search, counterexample, equivalence, and impossibility milestones investigate the formal space. Independent replication supplies external evidential force. The final assessment records only the strongest justified conclusion.

## Paused work

Certification expansion, new dashboards, release packaging, favorable-case accumulation, generic exposition, and unrelated applications remain paused unless required to execute or verify an active milestone.

## Immediate next PR

Construct and freeze one or more architecture-neutral mathematical definitions of reasoning. Every clause must be justified against the frozen domain specification, audited for candidate bias, and accompanied by counterexamples showing how it could be too weak or too strong.
