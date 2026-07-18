# Anti-Self-Validation Standard

## Status

Proposed governance standard for all confirmatory Project FAR research.

## Purpose

Project FAR exists to investigate whether reasoning instantiates a universal and minimal structure. Because the project also defines theories, representations, software, experiments, and evaluation procedures, it faces a structural risk: the same system may define the claim, construct the evidence, choose the competitors, score the results, and interpret the outcome.

This standard prevents that arrangement from being treated as independent confirmation.

The governing rule is:

> FAR must survive tests whose rules, cases, competitors, implementations, and adjudication it does not exclusively control.

Internal tests remain valuable, but their evidential force must be classified accurately.

## Scope

This standard applies to research used to support claims concerning:

- existence of a common reasoning structure;
- representational sufficiency;
- universality;
- necessity of FAR primitives;
- minimality;
- comparative economy;
- nontrivial constraint;
- superiority over competing vocabularies;
- independent replication.

It does not prohibit exploratory research, internal implementation testing, or theory revision. It governs how those activities may be interpreted.

## 1. Claim Separation

No experiment may test “FAR is universal and minimal” as a single undifferentiated claim.

Each preregistration must identify exactly which claim is tested:

### 1.1 Existence

At least one nontrivial common structure is shared by all reasoning systems in the preregistered scope.

A disconfirming result includes a valid in-scope pair or class of systems for which no common abstraction preserves the protected commitments without collapsing into unrestricted encoding.

### 1.2 Sufficiency

A frozen FAR vocabulary can represent the target system while preserving all preregistered observables and commitments.

A disconfirming result includes required information loss, silent semantic repair, unregistered auxiliary machinery, or a change to the protected theory.

### 1.3 Universality

The sufficiency result extends to every reasoning process in the independently justified scope.

Repeated successful case studies do not establish universality unless a separate argument justifies the generalization.

### 1.4 Necessity

A FAR primitive is necessary only when every admissible ablation either loses required preservation, increases total representational commitment, or reintroduces an equivalent commitment under another name.

### 1.5 Minimality

FAR is minimal only if no admissible competitor preserves the same protected commitments with a strictly smaller total commitment profile.

### 1.6 Nontrivial Constraint

FAR must reject encodings that reproduce outputs while failing to preserve the protected reasoning commitments.

If unrestricted derived constructs, hidden state, interpreter code, metadata, or lookup tables can recover any missing structure, expressive success alone is insufficient.

## 2. Protected Theory Freeze

Every confirmatory experiment must identify a protected theory package before test cases or results are exposed.

The package must include:

- primitive categories;
- permitted relations;
- semantic commitments;
- admissible derived constructs;
- operational rules;
- preservation dimensions;
- scope criteria;
- explicit exclusions;
- version identifiers and cryptographic digests.

Any substantive change required to pass the experiment creates a new theory version. The original result remains a failure or unresolved result for the frozen version.

A later theory revision may improve the framework, but it may not erase the evidential record of the earlier version.

## 3. Exploratory and Confirmatory Separation

### 3.1 Exploratory Work

Exploratory work may be iterative, project-authored, partially unblinded, and used to develop metrics, examples, implementations, and future theory versions.

Exploratory work may generate hypotheses. It may not establish a central confirmatory claim.

### 3.2 Confirmatory Work

Confirmatory work must be:

- preregistered;
- theory-frozen;
- metric-frozen;
- scope-frozen;
- independently executed or explicitly labeled internal;
- scored under fixed rules;
- fully retained, including failures and exclusions.

A dataset, scenario family, or mapping used materially during development may not later be described as an independent holdout.

## 4. Role Separation

A decisive confirmatory experiment must distinguish the following roles:

1. theory author;
2. scenario author;
3. candidate-vocabulary advocate;
4. mapper or encoder;
5. compiler or implementation author;
6. verifier author;
7. adjudicator;
8. statistical or decision-rule auditor;
9. red-team reviewer.

No single person, agent, organization, or code path should control all roles.

When role separation is not available, the experiment must be labeled according to the strongest justified category:

- internal exploratory study;
- internal implementation replication;
- independent technical replication;
- adversarial conceptual replication.

Multiple isolated implementations produced by one person or one agent establish implementation-path robustness only. They do not establish human, organizational, or conceptual independence.

## 5. Competitor Fairness

Project FAR authors may not define a weak competing vocabulary and treat victory over it as evidence of superiority.

For each serious comparison:

- the competitor must be specified from authoritative sources or by a knowledgeable advocate;
- the strongest defensible version must be used;
- FAR and competitors must receive equivalent opportunity for clarification;
- custom repairs must be counted as representational machinery;
- exclusions must be disclosed before scoring;
- adjudicators must be permitted to reject an unfair comparison before execution.

Comparisons designed entirely by FAR proponents must be labeled internal benchmarks.

## 6. External Observation Contract

Success criteria must be defined through an external observation contract rather than FAR-native categories.

The contract describes what must be preserved from the source reasoning system, including where applicable:

- admissible input states;
- conclusions and outputs;
- permitted and forbidden transitions;
- dependency relations;
- rule changes;
- history-sensitive behavior;
- uncertainty;
- provenance;
- counterfactual behavior;
- termination conditions;
- ontology commitments;
- information that must remain distinguishable.

Each candidate vocabulary maps independently to the same contract.

The contract must not require a candidate to resemble FAR unless the resemblance itself is the preregistered object of study.

## 7. Full-Cost Accounting

All machinery required for a successful representation must be counted.

Each mapping must report at least:

- **P** — primitive commitments;
- **D** — derived constructs;
- **O** — operations and transformation rules;
- **L** — semantic description length;
- **H** — hidden or auxiliary state;
- **A** — ambiguity policies and adjudication assumptions;
- **I** — external interpreter or executable machinery;
- **E** — exceptions, case-specific patches, and escape hatches.

No construct may be excluded from cost merely because it is called derived, implementation-level, metadata, or convenience syntax.

Comparative conclusions should use Pareto analysis unless a separate weighting rule was preregistered and justified.

Vocabulary X dominates Y only when X preserves at least as much as Y, is no worse on every registered cost dimension, and is strictly better on at least one dimension.

If neither dominates, the result is a tradeoff, not a victory.

## 8. Hidden-Reintroduction Control

Ablation tests must detect semantic equivalents, not only missing names.

After removing a primitive, the experiment must inspect whether the same commitment returns through:

- renamed fields;
- helper relations;
- metadata;
- hidden state;
- compiler behavior;
- verifier assumptions;
- interpretation policy;
- external code;
- case-specific derived constructs.

An ablation fails to establish dispensability when the removed commitment is merely reintroduced under another representation.

An ablation fails to establish necessity when the replacement succeeds with equal preservation and equal or lower total commitment.

## 9. Negative Controls and Constraint Tests

Every confirmatory sufficiency study must include negative controls designed to mimic outputs while violating protected commitments.

Required negative-control classes include, where applicable:

- lookup-table reproduction;
- dependency collapse;
- history erasure;
- rule modification hidden as ordinary state;
- semantics encoded only in labels;
- unrestricted interpreter code;
- hidden auxiliary state;
- provenance deletion;
- output-equivalent but process-distinct encodings.

A verifier that accepts these controls has not established nontrivial representational constraint.

## 10. Counterexample Search

Counterexample discovery must be treated as a primary research activity rather than a defensive afterthought.

The project should maintain hostile scenario generators targeting:

- self-modifying reasoning;
- nonmonotonic reasoning;
- inconsistent but nonexplosive systems;
- probabilistic belief revision;
- continuous-time systems;
- distributed multi-agent reasoning;
- analogical and creative reasoning;
- embodied or perceptual reasoning;
- inaccessible internal state;
- changing semantics;
- circular justification;
- creation of new representational types;
- undecidable transition conditions;
- severe resource bounds.

Automated search should maximize disagreement among the source model, FAR representation, and competitor representations.

## 11. Red-Team Authority

Confirmatory programs must assign a red-team function with authority to challenge:

- scenario selection;
- scope definitions;
- competitor strength;
- preservation metrics;
- semantic smuggling;
- hidden machinery;
- post hoc exclusions;
- favorable aggregation;
- overclaiming.

The red team should control at least one private holdout set when practical.

The protected theory, metrics, and failure rules must be frozen before holdout exposure.

## 12. Evidence Classification

Every result must be labeled with its maximum justified evidential class:

1. internal coherence;
2. internal implementation robustness;
3. bounded representational sufficiency;
4. nontrivial constraint;
5. local necessity;
6. comparative economy;
7. independent technical replication;
8. adversarial conceptual replication;
9. generalized universality argument;
10. bounded or universal conclusion.

Evidence at one level must not be described as evidence at a higher level without an explicit bridging argument.

## 13. Immutable Failure Record

The repository must preserve:

- failed frozen experiments;
- unresolved mappings;
- excluded cases;
- discarded evaluator responses;
- adjudication disputes;
- scope changes;
- theory revisions prompted by failures;
- negative controls that passed unexpectedly.

A failure may be superseded by a later version but must not be deleted or rewritten as though the original version succeeded.

## 14. Scope-Change Rule

A scope restriction introduced after exposure to a counterexample is post hoc.

It may define a new bounded hypothesis, but it may not rescue the original claim.

Every scope change must state:

- the triggering evidence;
- whether the restriction was preregistered;
- the prior claim affected;
- the new bounded claim;
- the theoretical justification independent of convenience.

## 15. Claim Ledger

Every central claim must have a maintained ledger entry containing:

- exact proposition;
- theory version;
- evidence for;
- evidence against;
- current scope;
- assumptions;
- dependencies;
- evidential class;
- unresolved objections;
- conditions that would raise confidence;
- conditions that would lower confidence;
- falsification conditions;
- current status.

No dashboard count may substitute for a claim ledger.

## 16. Infrastructure Discipline

Repository engineering, certification, dashboards, audits, and governance are enabling work, not evidence for FAR’s central theory.

A proposed infrastructure task must identify the active research dependency it serves.

If it does not materially improve counterexample discovery, faithful representation, comparison, verification, replication, or claim control, it must be classified as maintenance or deferred.

The project should periodically compare infrastructure effort with completed confirmatory research outputs.

## 17. Staged Research Gates

Claims must progress through the following gates:

### Gate 1 — Internal Coherence

The theory can be specified and implemented deterministically.

### Gate 2 — Bounded Sufficiency

The frozen vocabulary preserves preregistered observables across diverse frozen systems.

### Gate 3 — Nontrivial Constraint

The verifier rejects output-equivalent but commitment-invalid encodings.

### Gate 4 — Local Necessity

Primitive ablations fail under hidden-reintroduction controls.

### Gate 5 — Comparative Economy

FAR is not Pareto-dominated by strong competitors.

### Gate 6 — Independent Replication

Independent implementers reproduce the result from the frozen specification.

### Gate 7 — Boundary Discovery

The project states where FAR fails, becomes unresolved, or requires scope restrictions.

### Gate 8 — General Conclusion

Only after the prior gates may the project make a universality or minimality judgment.

A gate may remain unresolved. Progress does not require a favorable result.

## 18. Minimum Confirmatory Package

A confirmatory research package is incomplete without:

- claim-specific preregistration;
- protected theory manifest;
- external observation contract;
- role and independence declaration;
- competitor provenance statement;
- mapping artifacts;
- full-cost accounting;
- negative controls;
- hidden-reintroduction audit where applicable;
- deterministic verifier output;
- adjudication log;
- red-team report;
- immutable failure record;
- claim-ledger update;
- nonclaim and overstatement audit.

## 19. Decision Rule

Project success is not defined as proving FAR correct.

Project success is defined as establishing the strongest conclusion justified by evidence gathered under procedures that could have produced an unfavorable result.

Valid final outcomes include:

- no universal structure exists;
- a universal structure exists but FAR is not it;
- FAR is useful but nonminimal;
- FAR applies only within a bounded domain;
- FAR is universal under stated assumptions;
- evidence remains insufficient.

## Adoption

Upon adoption, this standard governs all newly registered confirmatory experiments. Existing experiments must state which controls were absent and must not be retroactively upgraded to a stronger evidential class.