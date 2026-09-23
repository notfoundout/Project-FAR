# Elenchus Protocol

Status: **Accepted — bounded internal methodology extension**  
Contract: `FAR-ELENCHUS-1.0`

## Purpose

This protocol governs adaptive questioning used to elicit and test a respondent's definitions, commitments, assumptions, and warrants during a FAR investigation.

The protocol preserves what the respondent actually commits to, what follows only under an explicit reasoning rule, where commitments are in tension, where incompatibility is demonstrated, and how the respondent revises or withdraws earlier commitments.

It does not create a second FAR workflow and does not establish external factual truth from conversational consistency.

## Trigger

Elenchus may be used when an investigation materially depends on clarification that cannot be recovered from a fixed source artifact alone, including:

- an ambiguous material term;
- an unstated assumption;
- an unclear inferential warrant;
- an apparent contradiction among a respondent's commitments;
- a need to distinguish materially different interpretations;
- a respondent revision that changes the proposition under evaluation.

When no interactive respondent exists, the protocol is `NOT_APPLICABLE`.

## Core rule

A respondent's commitment must be recorded before FAR tests it.

FAR may not silently strengthen, normalize, merge, or rewrite a commitment to manufacture a cleaner argument or contradiction.

## Question purposes

Every material question must state one purpose:

- `DEFINE_TERM`;
- `FIX_SCOPE`;
- `EXPOSE_ASSUMPTION`;
- `TEST_WARRANT`;
- `TEST_CONSEQUENCE`;
- `TEST_CONSISTENCY`;
- `SEEK_COUNTEREXAMPLE`;
- `DISTINGUISH_INTERPRETATIONS`;
- `CLARIFY_REVISION`.

The purpose is provenance for why the question was asked. It does not predetermine the answer.

## Procedure

1. Record the exact proposition, definition, or commitment under examination.
2. Ask a purpose-typed question directed at one material ambiguity, assumption, warrant, consequence, or consistency condition.
3. Record the response as a separate event linked to that question.
4. Materialize any resulting commitment with exact wording, context, version, and source event.
5. Materialize any definition, assumption, warrant, or tension that affects the investigation as its own identified record linked to the commitments that support it.
6. Derive implications only through an explicitly named calculus or inferential rule, and record the context in which the implication is asserted.
7. Compare derived implications and recorded commitments only at compatible contexts. If a premise commitment has a different recorded context from the implication, record an explicit bridge for that premise before using it in the derivation.
8. Record `TENSION` when incompatibility is suspected or context-sensitive but not demonstrated.
9. Record `CONTRADICTION` only when an explicit interpretation and calculus show that the referenced commitments cannot jointly hold under the recorded context.
10. Present the missing premise, tension, or demonstrated contradiction for clarification when doing so is material to the investigation.
11. Record revisions and withdrawals as new events. Preserve the earlier commitment and link the replacement; never overwrite history.
12. Repeat until the parent FAR investigation has sufficient explicitness, the respondent declines or cannot answer, the declared stopping rule is reached, or further questioning is non-material.

## Event chronology

Every question and response event uses a parseable timezone-aware date-time. A response may not predate the question it references.

A response event used to revise or withdraw a commitment may not predate the response event that originally sourced the commitment being changed. This prevents an internally impossible lifecycle history in which a commitment is revised or withdrawn before it exists.

These chronology rules establish only that the recorded dialogue order is internally possible. They do not prove wall-clock accuracy, external event truth, or causal order beyond the provenance of the underlying transcript or event source.

## Elicited-record traceability

Definitions, assumptions, warrants, and tensions are not free-form annotation buckets.

Every such record must have a stable identifier and explicit content. Definitions record the term and the definition statement. Assumptions and warrants record the exact statement. Tensions identify at least two commitments and state the basis for unresolved incompatibility. Every record names the commitment IDs from which it was elicited or against which it is evaluated.

A reference to an unknown commitment invalidates the session record. An empty object is not a valid elicited record.

## Implication context discipline

Every derived implication records:

- its premise commitment IDs;
- the resulting statement;
- the calculus;
- the rule;
- the implication context;
- zero or more per-premise context bridges.

A premise whose commitment context equals the implication context requires no bridge. A premise with a different context requires one explicit non-empty bridge tied to that premise ID. A bridge for a commitment that is not a premise is invalid, as is more than one bridge for the same premise.

A context bridge records the analyst's explicit justification for transporting that premise into the implication context. It does not itself prove that the transport is substantively sound; that justification remains auditable under the parent investigation.

## Commitment versioning

A revision must:

- identify the superseded commitment;
- create a distinct replacement commitment;
- use a greater version number;
- retain the superseded commitment with status `REVISED`;
- identify the response event that authorized the revision;
- use that same response event as the source event of the replacement commitment;
- occur no earlier than the source response of the superseded commitment;
- state why the revision occurred.

Each `REVISED` commitment must be the source of exactly one revision event. A revision source may not fork silently into multiple replacement commitments, and one replacement commitment may not be reused as the target of multiple revision events.

A withdrawal must retain the withdrawn commitment with status `WITHDRAWN`, identify the response event and reason, occur exactly once for that commitment, and occur no earlier than the response event that sourced the commitment. Every commitment marked `WITHDRAWN` must have a corresponding withdrawal event.

No revision or withdrawal deletes history.

## Contradiction discipline

Two statements are not contradictory merely because they differ.

A contradiction record must identify:

- at least two recorded commitment IDs;
- the interpretation under which they are compared;
- the reasoning calculus;
- the basis for incompatibility.

Different scopes, definitions, times, modalities, or contexts must be tested before incompatibility is asserted.

If those dimensions are unresolved, preserve `TENSION` or `Unknown` rather than promoting to contradiction.

## Relationship to contract discovery

When an interactive respondent is available, Contract Discovery may use elenchus evidence to clarify a material parse or interpretation before freeze.

When elenchus materially affects pre-freeze discovery, the exact session or transcript artifact must enter the governed intake as a hash-bound `far-intake/1.0` source with its locator, retrieval time, scope, and appropriate source type. Any parse, interpretation, materiality decision, assumption, or exclusion derived from that dialogue remains subject to the ordinary intake provenance rules, and the registered source remains subject to the terminal query/source saturation recheck before freeze. Elenchus is not a bypass around Contract Discovery search coverage, exclusion discipline, or freeze binding.

Elenchus does not authorize silent selection of one interpretation. If materially distinct interpretations survive questioning, the Contract Discovery Protocol still requires them to remain in the active family unless an explicit exclusion is justified.

## Relationship to FAR reasoning

Stage 3 may use elicited definitions or interpretations with session provenance.

Stage 6 may use elicited commitments as premises only at their recorded scope and context. Any derived implication must identify its premises, calculus, rule, and implication context. A premise from a different recorded context requires an explicit per-premise bridge before it is used.

A later revision that changes a result-relevant commitment invalidates dependent reasoning to the extent required by the canonical FAR revision rules.

## Machine-readable record

The accepted internal interchange contract is `socratic-epistemic-extensions/1.0` with record type `ELENCHUS_SESSION`, governed by:

- `schemas/socratic-epistemic-extensions-v1.schema.json`;
- `mechanization/far_mechanization/socratic_epistemic.py`.

The validator checks event references, timezone-aware event timestamps, response-to-question chronology, lifecycle-event chronology relative to the commitments they modify, elicited-record commitment references, revision and withdrawal completeness, revision source/target uniqueness, revision response provenance, version ordering, implication-premise references, implication-context compatibility and per-premise bridges, and contradiction references. It does not infer semantic contradiction from natural language or prove that a recorded context bridge is substantively valid.

## Failure conditions

The protocol fails if:

- a material respondent statement is replaced by an analyst paraphrase without preserving the original;
- a question or response timestamp is not a parseable timezone-aware date-time;
- a response predates the question it references;
- a revision response predates the response that sourced the superseded commitment;
- a withdrawal response predates the response that sourced the withdrawn commitment;
- a response is not linked to the question that elicited it;
- a material definition, assumption, warrant, or tension is stored without typed content and commitment provenance;
- an elicited record references a nonexistent commitment;
- pre-freeze elenchus evidence affects contract discovery without entering the governed intake as hash-bound source provenance and remaining subject to the existing search/saturation/freeze rules;
- an implication lacks explicit premises, calculus, rule, or context;
- an implication uses a premise from a different recorded context without an explicit bridge tied to that premise;
- an implication supplies a context bridge for a non-premise or duplicates a bridge for one premise;
- a contradiction is asserted without an explicit interpretation and calculus;
- a revision overwrites the prior commitment;
- a commitment is marked `REVISED` without a corresponding revision event;
- a revision source forks to multiple targets or a target is reused by multiple revisions;
- the response event authorizing a revision is not the source event of the replacement commitment;
- a commitment is marked `WITHDRAWN` without a corresponding withdrawal event, or is withdrawn more than once;
- a withdrawal deletes the prior commitment;
- materially different contexts are collapsed without an explicit bridge;
- conversational consistency is treated as external factual verification.

## Boundary

Elenchus produces evidence about commitments and their relations. External factual claims still require the evidence and validation required by the parent FAR investigation.

The name records a procedural resemblance to Socratic questioning. It does not establish historical derivation of Project FAR from Socrates.
