# AVC-001 — Alternative Vocabulary Competition

## Status

Completed bounded internal comparison. Scientific conclusion: **inconclusive**.

## Purpose

AVC-001 tests whether the current five-primitive FAR vocabulary is uniquely favored when compared with independently specified alternative vocabularies on the frozen `CRE-001-REFERENCE-V1` rule-modifying state-transition benchmark.

The competition includes FAR as the control and nine alternatives drawn from merged-primitive, graph, operational, categorical, information-theoretic, semantic-first, and event-process families.

## Freeze rule

All vocabulary names, primitive semantics, and identity conditions are recorded in `vocabularies.json` with status `frozen-before-evaluation`. A vocabulary may not be repaired after comparison by silently changing primitive meaning.

The benchmark is the existing deterministic CRE-001 reference model:

`theory/evaluation/comparative-representation/experiments/CRE-001/deterministic-verifier/reference-model.json`

The required preservation dimensions are:

- structural;
- semantic;
- operational;
- dependency;
- information;
- historical.

The comparison uses the Pareto and hidden-reintroduction rules from the Primitive Independence Framework.

## Candidate set

| ID | Vocabulary | Family | Primitive count |
|---|---|---|---:|
| AV-001 | FAR five-primitive control | FAR | 5 |
| AV-002 | Sign system | merged representation/semantics | 4 |
| AV-003 | Goal-governed process | merged investigation/calculus | 4 |
| AV-004 | Object-relation-transformation | graph/ontology | 3 |
| AV-005 | State-transition system | operational | 3 |
| AV-006 | Category-process vocabulary | categorical | 3 |
| AV-007 | Information-channel vocabulary | information-theoretic | 3 |
| AV-008 | Semantic-commitment vocabulary | semantic-first | 3 |
| AV-009 | Event-process vocabulary | event calculus | 3 |
| AV-010 | Typed dependency graph | graph-only | 3 |

## Results

The FAR control passed all six preservation dimensions on the frozen benchmark.

Two merged vocabularies failed as genuine reductions:

- AV-002 could not preserve independent variation between representational bearer and semantic assignment without recreating Representation and Interpretation.
- AV-003 could not preserve independent variation between objective conditions and governing rules without recreating Investigation and Reasoning Calculus.

Three alternatives were not admissible because at least one preservation dimension was Partial:

- AV-007 information-channel vocabulary;
- AV-008 semantic-commitment vocabulary;
- the merged alternatives above.

The state-transition, object-relation-transformation, event-process, and typed-graph vocabularies remain unresolved tradeoffs. They compactly preserve major structural or operational commitments, but their primitive semantics do not by themselves settle all semantic and information-preservation judgments.

The categorical vocabulary is representation-cost inferior on this benchmark and still leaves semantic judgments unresolved.

## Decision

AVC-001 does **not** establish that FAR is globally minimal, uniquely best, or universal.

The correct bounded conclusion is:

> On CRE-001, FAR supplied the only fully resolved all-Pass mapping in this internal comparison. Several lower-primitive alternatives remained unresolved rather than defeated because semantic or hidden-reintroduction judgments could not be conclusively adjudicated.

Therefore:

- FAR dominance: not established;
- competitor dominance: not established;
- global minimality: not established;
- alternative-vocabulary competition result: inconclusive.

## Internal-execution boundary

This comparison was constructed and evaluated within the Project FAR development process. It is not an independent external replication and does not satisfy the evaluator-independence requirement for a strong tested-space independence claim.

The numeric `D`, `O`, and `L` values are canonicalized internal counts for this bounded comparison. They are useful for deterministic comparison within AVC-001 but are not population estimates or universal complexity measures.

## Scientific value

AVC-001 establishes three useful results without overclaiming:

1. simple mergers of Representation with Interpretation and Investigation with Reasoning Calculus do not survive the frozen benchmark without hidden reconstruction;
2. compact operational and graph vocabularies remain serious competitors rather than being dismissed by definition;
3. the current benchmark is insufficient to resolve semantic adequacy among several structurally successful alternatives.

The third result directly motivates broader benchmarks designed to vary interpretation, investigation, and calculus independently.

## Artifacts

- `vocabularies.json` — frozen definitions and identity conditions for all ten vocabularies;
- `results.csv` — preservation, complexity, hidden-reintroduction, and decision records;
- `tests/test_alternative_vocabulary_competition.py` — deterministic integrity and claim-boundary checks.
