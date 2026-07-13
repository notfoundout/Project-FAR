# Central Research Program

## Purpose

Project FAR exists to determine whether there is a universal and minimal structure underlying reasoning.

This document defines the primary research program governing the long-term direction of the project. It establishes the central question under investigation, the standards by which evidence is evaluated, and the criteria by which the project's success is judged.

Every theoretical development, mechanization effort, external validation, proof, implementation, and supporting framework should contribute directly or indirectly to this research program.

## Why?

The purpose of Project FAR is not merely to construct a reasoning framework. Its purpose is to answer a foundational question about reasoning itself.

Without an explicit central research program, the project risks improving FAR as an artifact without determining whether FAR accurately represents the phenomenon it was created to investigate. This document prevents infrastructure, implementation, and maintenance work from replacing the research objective.

## Scope

This document governs the project's primary research direction.

It does not define new mathematics, introduce new primitives, revise accepted proofs, or modify Foundation v1.0. It defines the research program through which the existing theory and any future revisions are evaluated.

## Role in Project FAR

The Central Research Program is the authoritative statement of Project FAR's research objective. It governs:

- theory development;
- research investigations;
- external validation;
- mechanization used for research;
- future Foundation or theory revision proposals;
- roadmap planning;
- admission of work into the theoretical core.

When uncertainty exists about whether proposed work belongs in the project's core, this document provides the governing criterion.

## Dependencies

This document depends on:

- Foundation v1.0;
- the canonical Project FAR definitions;
- repository governance;
- completed v0.4.0 preliminary external-validation evidence;
- the mechanization MVP;
- repository certification.

## Dependents

This document governs:

- future research programs;
- counterexample investigations;
- universality and minimality studies;
- theory-revision proposals;
- research-oriented roadmap decisions;
- criteria for core research contributions.

## Design Rationale

Project FAR is fundamentally a research project. The framework exists because of the question, not the other way around. The research objective therefore governs subsequent theory and engineering rather than emerging implicitly from them.

The program is framed as hypothesis evaluation rather than confirmation or falsification alone. This preserves neutrality: supporting evidence, counterexamples, bounded applicability, and failure of the hypothesis are all valid outcomes.

## Central Research Question

> Does every reasoning process necessarily instantiate a common underlying structure, and if so, is that structure both universal and minimal?

This question includes three distinct issues:

1. whether a common structure exists;
2. whether it applies to every reasoning process within the justified scope;
3. whether it is irreducible or can be replaced by a simpler structure with equal expressive power.

The repository, theory, mechanization, and supporting artifacts exist to investigate this question rather than to presuppose its answer.

## Research Position

Project FAR treats the existence of a universal structure of reasoning as a hypothesis.

The project does not assume that such a structure exists. It does not assume that FAR is that structure. A result against FAR is a valid research result when supported by rigorous analysis.

Evidence may strengthen or weaken the central hypothesis. Existing accepted theory remains subject to scrutiny through the established theory-revision and Foundation-revision processes. No accepted artifact is protected from criticism merely because it supports the current framework.

## Primary Research Objectives

### Objective I — Existence

Determine whether any universal structure of reasoning exists.

If no such structure exists, identify the strongest counterexamples, boundaries, or incompatibilities supporting that conclusion.

### Objective II — Universality

If a candidate structure exists, determine whether every reasoning process can be faithfully represented within it without ad hoc modification or loss of relevant structure.

A failed representation must be analyzed to determine whether it indicates:

- a limitation of FAR;
- a defective reconstruction;
- an interpretation dispute;
- a justified scope boundary;
- or a process that does not meet the project's independently stated criteria for reasoning.

### Objective III — Necessity

Determine whether every component of the candidate structure is required.

A component is necessary only if removing it reduces the framework's ability to represent or evaluate reasoning within the justified scope. Components that do not satisfy this test should not remain in the minimal core.

### Objective IV — Minimality

Determine whether the structure is irreducible.

If a competing structure with fewer primitives, assumptions, or relations has equal expressive and explanatory power, the simpler structure is preferred. Necessity asks whether each current component is required; minimality asks whether the entire structure is the smallest adequate structure among alternatives.

## Research Method

Research governed by this program should use the following pattern where applicable:

1. formulate the tested claim precisely;
2. identify all material assumptions;
3. identify the relevant scope and interpretation;
4. construct plausible counterexamples and competing structures;
5. reconstruct the candidate reasoning process faithfully;
6. represent it using FAR without silent repair or redefinition;
7. test alternative interpretations and adversarial objections;
8. mechanize the representation where doing so adds reproducibility;
9. classify failures explicitly;
10. record implications for existence, universality, necessity, and minimality;
11. preserve unresolved uncertainty rather than forcing a conclusion.

Research should be reproducible, traceable, and open to independent scrutiny.

## Evidence and Evaluation Standard

The central hypothesis may be evaluated using:

- formal proof;
- formal derivation;
- empirical evidence;
- mechanized conformance;
- reproducible case studies;
- comparative analysis;
- successful representation;
- identified limitations;
- genuine counterexamples.

These forms of evidence do not have identical force. Formal proof supports only the propositions and assumptions it actually establishes. Mechanized conformance demonstrates executability and contract satisfaction, not universal truth. Case studies provide bounded evidence. Failure to discover a counterexample does not prove universality.

Every conclusion must state the evidence type, assumptions, scope, and remaining uncertainty.

## Counterexample Policy

Potential counterexamples are primary research objects and must not be dismissed merely because they pressure the current theory.

Each candidate must be classified as exactly one of:

- **Genuine Counterexample** — a reasoning process within the justified scope cannot be faithfully represented by FAR;
- **Representation Failure** — the attempted mapping is defective or incomplete, but the case has not shown FAR itself to fail;
- **Interpretation Dispute** — the outcome depends on unresolved meanings or reconstructions;
- **Scope-Boundary Case** — the case lies outside a previously and independently justified scope;
- **Non-Reasoning Process** — the case fails independently established criteria for reasoning;
- **Inconclusive** — the available evidence does not support a stable classification;
- **Successfully Represented** — the relevant reasoning structure is represented without changing the protected theory.

Every classification requires explicit justification. A candidate may not be excluded by redefining reasoning after the fact. Any scope restriction must be stated independently of the challenged case and defended on its own merits.

## Theory Revision Policy

The central research program may reveal defects, limitations, or unnecessary structure in FAR.

Protected Foundation artifacts must not be modified silently. If research requires a mathematical change, it must enter an explicit Foundation Revision, Theory Revision, or Research Investigation process under the repository's governance rules.

Documentation, repository restructuring, terminology cleanup, or mechanization changes may not be used to conceal substantive theoretical revision.

## Relationship to Mechanization

Mechanization operationalizes FAR, tests whether its concepts can be represented precisely, enables reproducible validation, and supports systematic counterexample analysis.

Mechanization strengthens confidence in internal coherence and executability. It does not by itself establish universality, necessity, minimality, or truth.

## Relationship to External Validation

External validation tests FAR against reasoning systems, arguments, and practices not constructed for FAR. It provides bounded evidence concerning representational reach, domain-specific assumptions, recurring pressure points, and possible limitations.

External validation does not prove universal applicability. Each case remains conditional on its reconstruction, evidence, and scope. As of v0.4.0, CRP v1.0 governs future blinded comparative claims about representational vocabularies; CRE-001 is registered but unexecuted.

## Work Admission Standard

A proposed contribution belongs in the core research program only if it materially advances at least one of the following:

- counterexample discovery;
- faithful representation;
- limitation identification;
- assumption reduction;
- primitive reduction;
- proof strengthening;
- boundary clarification;
- mechanized testability;
- explanatory power;
- comparison with a simpler competing structure.

Work that does not advance the central question should be classified accurately as infrastructure, maintenance, application, future enhancement, or outside core research scope. Such work may still be valuable, but it must not be confused with evidence resolving the central hypothesis.

## Possible Outcomes

The program recognizes at least the following legitimate outcomes:

1. no universal structure of reasoning exists;
2. a universal structure exists, but FAR is not that structure;
3. FAR is universal only within an explicitly bounded domain;
4. FAR is universal under stated assumptions but is not minimal;
5. FAR is universal and minimal under stated assumptions;
6. the evidence remains insufficient for a justified conclusion.

Project success does not require a favorable conclusion about FAR. It requires the strongest conclusion justified by the evidence.

## Completion Standard

The Central Research Program is complete only when the strongest justified conclusion has been established regarding:

- existence;
- universality;
- necessity;
- minimality;
- boundaries of applicability;
- unresolved uncertainty.

The project must distinguish proof from bounded evidence, and justified conclusion from absence of disconfirmation. Completion does not require certainty beyond what the evidence can support.

## Current Research Boundary

The current repository establishes that:

- Foundation v1.0 is frozen;
- initial cross-domain external validation is complete;
- the mechanization MVP is complete;
- repository governance and certification are complete.

These results establish readiness for systematic investigation. They do not answer the central research question.

Future major work should therefore be evaluated by its contribution to determining whether FAR captures a universal and minimal structure of reasoning, where its boundaries lie, and whether a simpler competing structure can account for the same phenomena.
## Comparative Representation Evaluation Governance

The central research program distinguishes preliminary external validation from blinded comparative representation evaluation. Preliminary external validation may describe systems, map FAR/FARA roles, and identify pressure points. Comparative Representation Protocol v1.0 governs claims about comparative distinctiveness, reproducibility, local necessity, relative economy, and Pareto interpretation. CRE-001 is registered but not executed.
