# Primitive Independence Framework

## Status

Research protocol. This document defines a falsifiable framework for evaluating whether the five current Project FAR primitives are independent. It does not establish that any primitive is independent.

## Purpose

Project FAR currently uses five primitive concepts:

1. Investigation
2. Representation
3. Representational Structure
4. Interpretation
5. Reasoning Calculus

The framework must not infer independence merely because each primitive has a distinct name or definition. Independence is instead treated as resistance to explicit reduction attempts under preserved representational commitments.

## Claim boundary

A successful evaluation under this framework may establish only one of the following bounded claims:

- **local independence:** a primitive cannot be eliminated, defined, merged, substituted, or recovered within the preregistered candidate transformations and target vocabulary;
- **tested-space independence:** no admissible reduction succeeds within the preregistered alternative-vocabulary search space;
- **failure of independence:** at least one admissible reduction preserves all required commitments at acceptable or lower cost.

No finite execution establishes absolute or universal independence over every possible vocabulary.

## Evaluation object

Let the target vocabulary be

\[
V_F = \{I, R, S, M, C\}
\]

where:

- \(I\) = Investigation;
- \(R\) = Representation;
- \(S\) = Representational Structure;
- \(M\) = Interpretation;
- \(C\) = Reasoning Calculus.

For each primitive \(p \in V_F\), an independence evaluation constructs one or more candidate reduced vocabularies \(V'\) and attempts to represent the same frozen benchmark systems.

## Required preservation commitments

A reduction is admissible only if it preserves the commitments required by the frozen benchmark specification. Preservation is assessed separately across:

- structural preservation;
- semantic preservation;
- operational preservation;
- dependency preservation;
- information preservation;
- historical preservation.

Each dimension is recorded as `Pass`, `Partial`, `Fail`, or `Unknown`. `Unknown` is unresolved and is not ordered between `Partial` and `Fail`.

A candidate reduction succeeds only when every required dimension is `Pass`. A `Partial`, `Fail`, or `Unknown` result prevents an independence failure conclusion for that candidate.

## Five mandatory reduction tests

Every primitive must be subjected to all five tests. No test may be omitted because it is difficult or produces an inconvenient result.

### 1. Elimination test

Remove primitive \(p\) without adding a replacement primitive.

The evaluator may reorganize declarations and relations, but may not introduce hidden machinery that is commitment-equivalent to \(p\).

The test succeeds when the reduced vocabulary preserves all required commitments.

### 2. Derivability test

Attempt to define \(p\) entirely from the remaining primitives and permitted general logical or set-theoretic resources.

A derivation is valid only when:

- it is total over the frozen benchmark domain;
- it is non-circular;
- it does not reference \(p\) or a synonym of \(p\);
- it is invariant under irrelevant renaming;
- it reproduces the operational consequences attributed to \(p\), not merely its label.

### 3. Merger test

Merge \(p\) with another primitive \(q\) into a single primitive \(m_{pq}\).

The merged primitive must have one unified identity condition. Merely packaging two independent fields into a tuple does not count as a merger.

The merger succeeds only if the model preserves cases in which \(p\) and \(q\) vary independently without reconstructing their distinction through hidden state or derived tags.

### 4. Substitution test

Replace \(p\) with a non-equivalent alternative primitive drawn from a preregistered candidate vocabulary.

The substitute must not be defined as \(p\) under another name. The evaluation must state the substitute's independent semantics and identity conditions before mapping begins.

### 5. Recovery test

Remove \(p\), then permit derived machinery under a fixed complexity budget.

This test detects pseudo-independence caused by prohibiting all derivation. It also detects pseudo-reduction caused by recreating the deleted primitive through unrestricted machinery.

A recovery succeeds only when the derived construction:

- remains within the preregistered complexity budget;
- is not commitment-equivalent to reintroducing \(p\) as a hidden primitive;
- preserves every required commitment;
- remains stable across all frozen benchmark cases.

## Hidden reintroduction rule

A candidate reduction fails as a reduction when it introduces any object, field, relation, state variable, transition schema, admissibility condition, or historical constraint that has the same identity and operational role as the removed primitive.

Commitment-equivalence is assessed by whether two constructions:

1. distinguish the same admissible states;
2. permit and prohibit the same transitions;
3. preserve the same dependencies and histories;
4. support the same counterfactual variations;
5. differ only by naming, formatting, or packaging.

Commitment-equivalent machinery is counted as the original primitive for vocabulary-cost purposes.

## Complexity accounting

Vocabulary cost and representation cost remain separate.

### Vocabulary cost

Record:

- `A_used`: primitive categories actually used;
- `A_required`: primitive categories shown necessary for the mapping.

### Representation cost

Record:

- `D`: derived machinery;
- `O`: operations or transition rules;
- `L`: semantic description length after canonicalization.

A reduction does not succeed merely by lowering `A_used` while increasing hidden or derived machinery without bound.

## Comparison rule

Use Pareto comparison after canonicalization.

Candidate \(X\) dominates candidate \(Y\) only when:

- preservation in \(X\) is no worse than preservation in \(Y\) on every required dimension;
- vocabulary cost in \(X\) is no greater than in \(Y\);
- `D`, `O`, and `L` in \(X\) are each no greater than in \(Y\);
- at least one comparison is strict.

If neither candidate dominates, report a tradeoff. Do not collapse preservation and complexity into one unregistered scalar score.

## Per-primitive decision rule

For primitive \(p\):

- **Independence failed:** at least one admissible reduction passes every required preservation dimension and Pareto-dominates or equals the unreduced vocabulary while using fewer commitment-distinct primitives.
- **Locally independent:** every mandatory reduction attempted within the frozen local transformation set fails, becomes commitment-equivalent to reintroducing \(p\), or is Pareto-inferior.
- **Tested-space independent:** the local criterion is met and every preregistered external substitute or alternative vocabulary also fails.
- **Unresolved:** any mandatory test is unexecuted, materially `Unknown`, or blocked by an unresolved equivalence judgment.

## Architecture-level decision rule

The five-primitive architecture may be described as independent relative to the protocol only when every primitive is at least locally independent.

It may be described as independent over the tested search space only when every primitive is tested-space independent.

One failed primitive is sufficient to reject independence of the current five-primitive architecture.

## Required artifacts for execution

A future execution must freeze:

- benchmark system descriptions;
- required preservation dimensions per system;
- candidate transformations;
- alternative vocabularies and substitute semantics;
- canonical intermediate representation;
- commitment-equivalence criteria;
- complexity budgets and counting rules;
- evaluator eligibility and calibration;
- adjudication procedure;
- deterministic aggregation rules.

Every attempted mapping must be retained, including divergent and failed mappings.

## Evaluator requirements

Evaluators must:

- be able to read formal specifications;
- be familiar with state-transition systems or formal reasoning;
- have no involvement in constructing the candidate vocabulary under evaluation;
- have no access to previous evaluators' mappings before submission freeze;
- complete a standardized calibration exercise unrelated to the experiment.

## Statistical philosophy

This framework is decision-theoretic, not inferential. It does not estimate population parameters or test null hypotheses. Conclusions follow from preregistered decision rules applied to observed mappings. Confidence intervals, significance tests, or population claims require a separately preregistered replication design.

## Falsification conditions

The current primitive-independence hypothesis is falsified if any one of the following occurs:

- a primitive is eliminated while all required commitments are preserved;
- a primitive is non-circularly derived from the remaining vocabulary;
- two primitives are genuinely merged while preserving their independent variations;
- a non-equivalent substitute preserves all commitments at equal or lower cost;
- a reduced vocabulary Pareto-dominates the five-primitive vocabulary without hidden reintroduction.

## Relationship to minimality

Independence and minimality are distinct.

- Independence asks whether each primitive can be reduced to or replaced by the others.
- Local minimality asks whether deletion from the current vocabulary causes failure.
- Global minimality asks whether any alternative vocabulary with lower commitment-distinct cost performs as well.

This framework contributes to independence and local minimality. Global minimality requires a broader alternative-vocabulary competition.

## Current result

No primitive-independence result is established by this document. The status of every primitive remains `Open` until the mandatory tests are executed and adjudicated.