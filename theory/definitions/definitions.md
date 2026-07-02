# Definitions

## Purpose

This document establishes the canonical terminology used throughout Project FAR.

Unless explicitly stated otherwise, every technical term appearing elsewhere in Project FAR refers to the definitions established here.

These definitions provide the common conceptual foundation required for specification, analysis, reasoning, proof construction, artifact auditing, and framework development.

The purpose of this document is consistency rather than finality. It records the current canonical vocabulary while remaining compatible with continued foundational investigation.

---

# Authority Notice

The definitions contained in this document are canonical for the current version of Project FAR.

Canonical status indicates required usage within the repository. It does **not** imply that a definition has been proven fundamental, necessary, complete, or irreducible.

Some definitions represent grounded foundational results. Others remain framework specifications awaiting further reduction, proof, or refinement.

Definitions may be revised only when supported by explicit evidence, including:

- grounding investigations;
- formal proofs;
- counterexamples;
- artifact audits;
- demonstrated reductions;
- methodology revisions;
- discovery of hidden assumptions;
- elimination of circular definitions;
- decomposition of previously unified concepts;
- demonstrable improvements in explanatory or expressive power.

Conceptual stability is earned through investigation rather than assumed by definition.

Grounding investigations are maintained under:

`foundations/discovery/`

Artifact audits are maintained under:

`foundations/discovery/audits/`

Knowledge objects supporting individual concepts are maintained separately within the Knowledge Layer.

---

# Foundational Concepts

## Object

An **object** is anything that is explicitly distinguishable.

Project FAR makes no ontological commitment regarding the independent existence or nature of an object beyond its explicit distinguishability.

---

## Property

A **property** is a characteristic that an object may possess.

Properties may themselves become objects of investigation when explicitly represented.

---

## Relation

A **relation** is an explicitly specified association between two or more objects.

Relations may themselves be represented as objects within a representational framework.

---

## Structure

A **structure** is an organized collection of objects together with explicitly specified relations among those objects.

A structure specifies organization independently of interpretation.

---

## Component

A **component** is an object identified as forming part of a larger structure.

Component status is always relative to a specified structure.

---

## System

A **system** is a collection of interacting objects organized according to a specified structure.

Interaction is determined by explicitly defined relations rather than assumed behavior.

---

## Class

A **class** is a collection of objects identified by explicitly specified membership criteria.

Membership criteria may depend upon properties, relations, structures, or other explicitly defined conditions.

---

## Domain

A **domain** is the explicitly specified collection of objects to which a claim, definition, investigation, framework, theorem, or proof is intended to apply.

Claims of generality or universality are meaningful only relative to an explicitly specified domain.

---

# Framework Concepts

## Model

A **model** is a representation intended to capture selected aspects of another object, relation, structure, system, process, or concept.

A model is not required to represent every aspect of its subject.

---

## Framework

A **framework** is an organized specification of concepts, definitions, relations, and procedures developed to achieve a specified objective.

A framework specifies how its concepts relate without asserting that those concepts are fundamental.

---

## Theory

A **theory** is a structured collection of definitions, axioms, propositions, conjectures, lemmas, theorems, proofs, and derived results concerning a specified domain.

A theory may remain incomplete while still providing explanatory or predictive value.

---

## Architecture

An **architecture** is a specification of the objects, relations, and organizational principles required to represent a specified class of systems.

An architecture specifies representational organization rather than operational behavior.

---

## Ontology

An **ontology** is a specification of the concepts, categories, and relations assumed to exist for the purposes of a framework.

An ontology specifies what the framework assumes exists. It does not by itself establish independent ontological existence.

---

## Syntax

**Syntax** specifies the structural organization of representations independently of interpretation.

Syntax constrains form but does not determine meaning.

---

## Semantics

**Semantics** specifies the meaning assigned to representations under an interpretation.

Semantic content depends upon interpretation rather than representational structure alone.

---

## Scope

The **scope** of a framework is the explicitly specified domain over which its claims are intended to apply.

Claims regarding completeness, universality, correctness, or expressive power are meaningful only relative to an explicitly stated scope.

---

# Formal Concepts

## Universal

A property is **universal** over a specified domain if every member of that domain possesses that property.

Universality is always relative to an explicitly specified domain.

---

## Universal Architecture

A **universal architecture** is an architecture capable of representing every member within its stated scope.

Universality does not imply uniqueness, optimality, minimality, or irreducibility.

---

## Minimal

A structure is **minimal** with respect to a specified objective if removing any required component reduces its expressive power relative to that objective.

Minimality is always relative to an explicitly specified objective and scope.

---

## Candidate Primitive

A **candidate primitive** is a concept that has not yet been successfully reduced to simpler concepts within the current framework.

Candidate primitive status is provisional and remains subject to future reduction.

---

## Established Primitive

An **established primitive** is a concept for which repeated reduction attempts have failed within the current framework.

Established primitive status remains revisable if future reductions succeed.

---

## Derived Concept

A **derived concept** is a concept explicitly defined in terms of one or more other concepts within the framework.

A concept may transition between candidate primitive and derived status as the framework evolves.

---

## Reduction

A **reduction** is a demonstration that one concept can be completely defined in terms of other concepts without loss of expressive power relative to a specified scope and objective.

---

## Independence

Two concepts are **independent** if neither can be derived from the other within the current framework.

Independence claims remain provisional and may be overturned by future reductions.

---

## Equivalence

Two objects are **equivalent** if they satisfy an explicitly specified equivalence relation.

Equivalence exists only relative to the defining relation.

---

## Expressive Power

The **expressive power** of a framework is the collection of objects, relations, structures, or systems that the framework is capable of representing within its stated scope.

Expressive power should always be evaluated relative to explicitly specified objectives and scope.

---

# Representational Concepts

## Representation

A **representation** is an explicitly distinguishable object constructed or used to denote, describe, encode, or refer to another object, relation, structure, system, process, or concept.

A representation is distinct from that which it represents.

The same represented object may admit multiple representations, and the same representation may refer to different represented objects under different interpretations.

Project FAR concerns representations independently of whether the represented object exists.

---

## Represented Object

A **represented object** is the object, relation, structure, system, process, or concept to which a representation refers under a specified interpretation.

A represented object is distinct from every representation of it.

Represented objects may be concrete, abstract, hypothetical, fictional, or otherwise specified by an investigation.

---

## Representational Structure

A **representational structure** is an organized collection of representations together with explicitly specified relations among those representations.

A representational structure specifies organization independently of interpretation.

Different interpretations may assign different meanings to the same representational structure.

---

## Interpretation

An **interpretation** is a mapping that assigns semantic meaning to representations.

Interpretations operate upon representations without altering their representational structure.

The same representation may receive different meanings under different interpretations.

Different interpretations need not be equally appropriate for a given investigation.

---

## Semantic Content

**Semantic content** is the meaning assigned to a representation under a specified interpretation.

Semantic content is always relative to an interpretation.

Representations may possess structure without possessing semantic content.

---

## Structural Equivalence

Two representations are **structurally equivalent** if they satisfy an explicitly specified structural equivalence relation.

Structural equivalence concerns representational organization rather than meaning.

Structural equivalence does not imply semantic equivalence.

---

## Semantic Equivalence

Two representations are **semantically equivalent** under a specified interpretation if they possess the same semantic content under that interpretation.

Semantic equivalence is always relative to an explicitly specified interpretation.

Semantic equivalence does not imply structural equivalence.

---

## Representation Mapping

A **representation mapping** is an explicitly specified correspondence between one representational structure and another.

A representation mapping specifies how representations in one structure correspond to representations in another.

Representation mappings may preserve, modify, or discard structural or semantic properties depending upon their specification.

---

## Representation Transformation

A **representation transformation** is a representation mapping that produces a new representational structure from an existing representational structure.

Representation transformations concern representations rather than the represented objects themselves.

Whether semantic content is preserved depends upon both the transformation and the applicable interpretation.

---

## Representation Invariance

A property is **representation invariant** if it remains unchanged under a specified class of representation mappings.

Representation invariance is always relative to explicitly specified mappings.

---

## Representation Fidelity

The **fidelity** of a representation is the extent to which it preserves explicitly specified properties of its represented object under a specified interpretation.

Fidelity is always relative to:

- the represented object;
- the interpretation;
- the properties being preserved.

No representation is assumed to possess complete fidelity unless explicitly demonstrated.

---

## Representation Completeness

A representation is **complete** relative to a specified objective if it contains every representational element required to achieve that objective.

Completeness is always relative to:

- an objective;
- a scope;
- an interpretation.

Completeness is never absolute.

---

## Representation Consistency

A representational structure is **consistent** if its representations satisfy all explicitly specified structural constraints applicable to that structure.

Consistency of representation does not imply correctness of interpretation.

---

## Representational Independence

Two representations are **representationally independent** if neither representation can be completely derived from the other under the applicable representational framework.

Representational independence does not imply semantic independence.

---

# Reasoning Concepts

## Investigation

An **investigation** is an explicitly specified reasoning objective together with the conditions under which that objective is pursued.

An investigation establishes the context within which representations, interpretations, reasoning calculi, candidates, admissibility, and resolutions are defined.

An investigation is distinct from:

- the reasoning process conducted within it;
- the representations used during it;
- the records produced by it;
- the conclusions ultimately reached.

---

## Investigation State

An **investigation state** is the condition of an investigation at a particular stage of a reasoning process.

An investigation state exists independently of any representation of that state.

Multiple representations may describe the same investigation state.

---

## Investigation Record

An **investigation record** is the persistent representation of an investigation.

An investigation record documents an investigation.

It is not the investigation itself.

---

## Reasoning

**Reasoning** is the activity of generating, transforming, evaluating, classifying, or selecting representations according to a reasoning calculus within an investigation.

Reasoning is an activity rather than an object.

Reasoning is distinct from representations of reasoning.

---

## Reasoning Process

A **reasoning process** is an ordered sequence of reasoning activities performed within an investigation.

A reasoning process may produce:

- representations;
- reasoning state representations;
- transition signatures;
- admissibility classifications;
- resolutions.

A reasoning process is distinct from every representation that documents it.

---

## Reasoning Calculus

A **reasoning calculus** is a specification of the rules governing admissible reasoning within an investigation.

A reasoning calculus specifies:

- admissible transformations;
- admissible inference rules;
- admissibility criteria;
- resolution procedures.

Project FAR remains independent of any particular reasoning calculus.

---

## State

A **state** is the specification of the relevant properties of an object relative to explicitly specified criteria.

State descriptions are always relative to:

- the object;
- the analysis criteria;
- the scope of the investigation.

---

## Reasoning State

A **reasoning state** is the state of an investigation at a particular stage of a reasoning process.

A reasoning state is not itself a representation.

---

## Reasoning State Representation

A **reasoning state representation** is a representation describing a reasoning state.

Different reasoning state representations may describe the same reasoning state.

---

## Reasoning State Record

A **reasoning state record** is a persistent representation of one or more reasoning state representations maintained for documentation, auditing, verification, or reproduction.

A reasoning state record is a repository artifact rather than a reasoning state.

---

## Transformation Rule

A **transformation rule** specifies the conditions under which one representation may be transformed into another.

A transformation rule does not itself perform a transformation.

---

## Transformation Execution

A **transformation execution** is the application of a transformation rule during a reasoning process.

Executions are events.

Rules are specifications.

The two are distinct.

---

## Transformation Result

A **transformation result** is the representation produced by a transformation execution.

Transformation results may preserve, modify, or discard structural or semantic properties depending upon the applicable rule and interpretation.

---

## Transition Signature

A **transition signature** is a representation describing a transformation execution between reasoning state representations.

A transition signature documents a transition.

It is not itself the transition.

---

## Reasoning Trace

A **reasoning trace** is an ordered collection of transition signatures representing the progression of a reasoning process.

A reasoning trace represents reasoning.

It is not the reasoning process itself.

---

# Decision Concepts

## Candidate

A **candidate** is an explicitly represented object admitted for consideration within an investigation.

Candidate status does not imply admissibility or eventual selection.

---

## Criterion

A **criterion** is an explicitly specified condition used for evaluation, classification, admissibility, or selection.

---

## Classification

A **classification** is the assignment of one or more objects to categories according to explicitly specified criteria.

---

## Admissibility

**Admissibility** is the property of satisfying the criteria established by the applicable reasoning calculus within an investigation.

Admissibility is determined by the reasoning calculus.

It is not determined by the admissibility structure.

---

## Admissibility Classification

An **admissibility classification** is the explicit assignment of admissibility status to a candidate.

Classification is distinct from both the criterion used to produce it and the representation that records it.

---

## Admissibility Structure (Ω)

The **Admissibility Structure**, denoted **Ω**, is the representation of the admissibility classifications of candidates within an investigation.

Ω records admissibility classifications.

Ω does not:

- perform reasoning;
- determine admissibility;
- generate candidates;
- perform candidate selection;
- produce resolutions.

---

## Resolution Rule

A **resolution rule** specifies how one or more admissible candidates are selected from Ω.

A resolution rule specifies selection.

It is not the act of selection.

---

## Resolution Execution

A **resolution execution** is the application of a resolution rule to an admissibility structure.

---

## Resolution

A **resolution** is the candidate or collection of candidates produced by a resolution execution.

A resolution is distinct from:

- the admissibility structure;
- the resolution rule;
- the execution that produced it.

---

# Meta Concepts

## Definition

A **definition** is an explicit specification that assigns meaning to a term within a framework.

Definitions establish how terms are used within the framework but do not, by themselves, establish the truth, necessity, or existence of the concepts they define.

Definitions may be revised only through explicit justification.

---

## Principle

A **principle** is a general rule adopted to guide the design, development, or evaluation of a framework.

Principles guide methodology but do not themselves constitute proofs.

---

## Axiom

An **axiom** is a proposition accepted without proof within a specified formal system.

The validity of conclusions derived from an axiom is always relative to that formal system.

---

## Proposition

A **proposition** is a statement capable of possessing a truth value.

Truth, falsity, or undecidability are determined relative to explicitly specified definitions, assumptions, and reasoning calculi.

---

## Conjecture

A **conjecture** is a proposition believed to be true but not yet established by proof or counterexample.

---

## Lemma

A **lemma** is a proposition proved primarily for use in establishing another proposition.

---

## Theorem

A **theorem** is a proposition established by proof from explicitly specified premises under an explicitly specified reasoning calculus.

---

## Corollary

A **corollary** is a proposition that follows directly from one or more established theorems.

---

## Proof

A **proof** is a finite sequence of justified reasoning steps demonstrating that a proposition follows from specified premises under an explicitly stated reasoning calculus.

A proof establishes derivability within a formal system.

It does not establish the truth of its premises.

---

## Refutation

A **refutation** is a demonstration that a proposition cannot be derived under the stated premises, or that it is contradicted by a valid counterexample.

---

# Evidence Concepts

## Claim

A **claim** is a proposition asserted within an investigation.

Claims may be classified according to explicitly specified claim types.

---

## Claim Type

A **claim type** classifies a claim according to its role within an investigation.

Examples include:

- definitional;
- logical;
- mathematical;
- empirical;
- causal;
- interpretive;
- probabilistic;
- normative;
- predictive.

Claim types determine appropriate evaluation methods.

---

## Evidence

**Evidence** is a representation used to support, weaken, or evaluate a claim within an investigation.

Evidence is distinct from:

- the claim it concerns;
- the reasoning process that evaluates it;
- the conclusions ultimately reached.

Evidence does not establish a claim independently of an applicable reasoning calculus.

---

## Observation

An **observation** is a representation describing something obtained through an explicitly specified observation procedure.

Observation does not imply correctness or interpretation.

---

## Assumption

An **assumption** is a claim treated as accepted for the purposes of an investigation.

Acceptance within an investigation does not imply objective truth.

---

## Hypothesis

A **hypothesis** is a claim proposed for evaluation whose status has not yet been determined.

---

## Explanation

An **explanation** is a representation intended to account for one or more observations, claims, or phenomena under explicitly specified assumptions.

---

## Prediction

A **prediction** is a claim concerning observations expected under specified conditions.

---

## Counterexample

A **counterexample** is an object demonstrating that a universal claim fails within its stated domain.

A valid counterexample is sufficient to refute a universal claim within that domain.

---

# Methodology Concepts

## Artifact

An **artifact** is a persistent representation produced during the development, investigation, or documentation of Project FAR.

Artifacts include, but are not limited to:

- definitions;
- specifications;
- audits;
- investigations;
- proofs;
- reports;
- diagrams;
- datasets;
- knowledge objects.

---

## Audit

An **audit** is a systematic evaluation of an artifact against explicitly specified evaluation criteria.

Every audit shall record:

- evaluation criteria;
- findings;
- supporting evidence;
- recommendations;
- overall assessment.

Audit conclusions require explicit justification.

---

## Grounding Investigation

A **grounding investigation** is an investigation whose objective is to determine whether a concept can be justified from more fundamental concepts.

Grounding investigations may:

- establish reductions;
- identify hidden assumptions;
- expose category collapses;
- demonstrate independence;
- justify candidate primitives;
- reject previously accepted concepts.

---

## Knowledge Object

A **knowledge object** is a persistent artifact representing an explicitly identified unit of organized knowledge within Project FAR.

Knowledge objects include:

- claims;
- evidence;
- hypotheses;
- questions;
- investigations;
- audit findings;
- proof results;
- derived conclusions.

Knowledge objects improve traceability but do not themselves establish correctness.

---

## Traceability

**Traceability** is the property that every claim, definition, conclusion, audit finding, or architectural decision can be explicitly connected to the supporting artifacts from which it was derived.

---

## Revision

A **revision** is an explicitly justified modification to an existing artifact.

Every revision should identify:

- the artifact being revised;
- the motivating evidence;
- the specific changes;
- the rationale for those changes;
- any affected dependent artifacts.

---

# Closing Statement

This document defines the canonical terminology of Project FAR.

Its purpose is to provide a stable conceptual vocabulary for reasoning, analysis, framework development, and foundational investigation.

Canonical status reflects current repository usage rather than permanent finality.

All definitions remain subject to revision when justified by explicit evidence arising from grounding investigations, formal proofs, artifact audits, or methodological improvements.
