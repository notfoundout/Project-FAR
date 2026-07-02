# AA-001 — Core Definitions Artifact Audit

## Status

Research Audit

## Artifact Audited

`theory/definitions/definitions.md`

## Audit Objective

Test whether the canonical definitions file collapses independent dimensions, hides relational arguments, assumes framework structure before grounding it, or mixes design choices with discovered necessities.

This audit does not revise the definitions.

It identifies grounding defects and revision targets.

## Summary Result

The definitions file is usable as a framework specification, but it is not yet grounded as first-principles theory.

Several definitions presuppose concepts that the current foundational investigation has not yet justified.

The main issue is not wording quality.

The main issue is authority level: many definitions are written canonically even though they currently function as framework-first design definitions rather than derived or independently grounded results.

## Major Findings

### AA-001-F1 — Object Depends on Distinguishability

Current definition:

> An object is any entity that can be explicitly distinguished.

Issue:

This definition depends on `entity`, `explicitly`, and `distinguished`, none of which are grounded here.

It also makes objecthood dependent on distinguishability, which aligns with current discovery work but has not yet been proven.

Required action:

Treat this as a provisional framework definition until distinguishability is investigated and either accepted, revised, or replaced.

### AA-001-F2 — Relation Assumes Objects

Current definition:

> A relation is an explicitly defined association between two or more objects.

Issue:

The definition assumes objects are prior to relations.

Current foundational investigation has not established whether relations depend on objects, positions, roles, relation types, or satisfaction conditions.

Required action:

Mark relation as ungrounded pending relation-type / relation-instance analysis.

### AA-001-F3 — Representation Mixes Object, Function, and Investigation Role

Current definition:

> A representation is an explicitly distinguishable object used to represent information within an investigation.

Issue:

This collapses independent dimensions:

- artifact ontology: object;
- function: represents information;
- research role: used within an investigation;
- dependency: distinguishability;
- scope: investigation-relative.

It also assumes `information` and `investigation` before both are independently grounded.

Required action:

Split representation into independent dimensions before canonization:

- representational artifact;
- represented content;
- representation relation;
- interpretation context;
- investigation role.

### AA-001-F4 — Investigation Assumes Criteria

Current definition:

> An investigation specifies the object of analysis together with the criteria by which reasoning is organized.

Issue:

This definition assumes that every investigation has an object and criteria.

Recent analysis suggests investigations may instead target relations, questions, or candidate structures rather than objects alone.

Required action:

Revise after FI-000 determines the correct foundational research question and after target-object / target-relation analysis is completed.

### AA-001-F5 — Reasoning Is Defined Too Far Downstream

Current definition:

> Reasoning is the process of producing, transforming, or evaluating representations according to a reasoning calculus within the context of an investigation.

Issue:

This definition presupposes nearly the entire current framework:

- process;
- representation;
- transformation;
- evaluation;
- reasoning calculus;
- investigation.

It therefore cannot ground the framework.

It is a framework-internal operational definition, not a first-principles definition.

Required action:

Demote this definition's authority for foundational work until explicit reasoning is independently characterized.

### AA-001-F6 — Evaluation and Execution Are Conflated in Reasoning

The reasoning definition includes producing, transforming, and evaluating representations in one definition.

Issue:

Current discovery work has separated execution from evaluation.

A system may execute rule-governed transformations without evaluating those transformations.

Required action:

Separate:

- reasoning execution;
- reasoning trace;
- reasoning evaluation;
- investigation of reasoning.

### AA-001-F7 — Primitive Definition Is Too Absolute

Current definition:

> A primitive is a concept that is not derived from simpler concepts within the framework.

Issue:

This treats primitiveness as a property of an individual concept.

Current methodology suggests primitive status should be basis-relative and methodology-relative.

Required action:

Revise to something closer to:

> A primitive is a concept currently treated as an irreducible residual relative to a specified basis, scope, and accepted reduction methodology.

### AA-001-F8 — Reduction Definition Is Too Weak

Current definition:

> A reduction is the demonstration that one concept can be completely represented in terms of other concepts.

Issue:

This does not distinguish genuine reduction from paraphrase.

It ignores preservation of explanatory scope and reduction of independent explanatory commitments.

Required action:

Revise after methodology validates commitment-minimization criteria.

### AA-001-F9 — Admissibility Collapses Property, Criteria, Calculus, and Investigation

Current definition:

> Admissibility is the property of satisfying the criteria established by a reasoning calculus within an investigation.

Issue:

This is structurally useful, but it is not decomposed.

It combines:

- property;
- criterion satisfaction;
- source of criteria;
- calculus;
- investigation context.

Required action:

Represent admissibility as a typed relation:

```text
candidate X
satisfies criterion C
under calculus K
within investigation I
relative to scope S
```

### AA-001-F10 — Resolution Depends on an Unjustified Decision Procedure

Current definition:

> A resolution is the candidate, or collection of candidates, selected from the Admissibility Structure according to the applicable resolution rule.

Issue:

This is downstream of candidate, admissibility, admissibility structure, and resolution rule.

It also assumes selection is the correct form of investigative closure.

Required action:

Keep as framework-internal definition, not foundational result.

## Cross-Cutting Defects

### 1. Canonical Status Exceeds Grounding Status

Many definitions are canonical in repository role but not grounded as first-principles results.

This is not fatal if the repository explicitly distinguishes canonical framework specification from grounded foundational theory.

### 2. Hidden Relational Arguments

Several definitions should be rewritten as typed relations rather than unary concepts.

Examples:

- admissibility;
- equivalence;
- reduction;
- primitive status;
- resolution;
- representation.

### 3. Framework-First Bias

The file defines concepts in a way that makes FAR/FARA/FARO usable, but not in a way that derives them.

This confirms the need for the discovery track.

### 4. Independent Dimensions Are Collapsed

Definitions often combine ontology, repository role, investigation role, logical status, and framework function.

This confirms the Orthogonality Rule as a useful audit tool.

## Recommended Next Actions

1. Do not rewrite the entire definitions file immediately.
2. Add an authority notice to `theory/definitions/definitions.md` distinguishing framework-internal definitions from first-principles grounded definitions.
3. Create a separate `foundations/discovery/audits/` index if more audits are added.
4. Begin a targeted rewrite only after FI-000 and FI-002 clarify the target object and explicit reasoning.
5. Use this audit as evidence that the methodology exposes real repository defects.

## Methodology Audit

### Did the methodology expose hidden assumptions?

Yes.

It exposed that multiple canonical definitions depend on ungrounded concepts such as distinguishability, information, investigation, calculus, criteria, and process.

### Did it prevent premature conclusion?

Yes.

The audit does not claim the definitions are false.

It classifies them as useful but not yet grounded.

### Did it expose collapsed dimensions?

Yes.

Representation, admissibility, resolution, and primitive status collapse independent dimensions.

### Did it require revision to methodology?

Not yet.

The current methodology was sufficient to identify concrete defects.

### Current Methodology Result

The audit provides evidence that the methodology is useful: it exposed actionable structural defects in an existing canonical artifact without requiring speculative theory expansion.
