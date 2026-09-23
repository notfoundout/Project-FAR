# Elenchus Protocol

Status: **Provisional — candidate internal methodology extension**  
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
5. Derive implications only through an explicitly named calculus or inferential rule.
6. Compare derived implications and recorded commitments at compatible contexts.
7. Record `TENSION` when incompatibility is suspected or context-sensitive but not demonstrated.
8. Record `CONTRADICTION` only when an explicit interpretation and calculus show that the referenced commitments cannot jointly hold under the recorded context.
9. Present the missing premise, tension, or demonstrated contradiction for clarification when doing so is material to the investigation.
10. Record revisions and withdrawals as new events. Preserve the earlier commitment and link the replacement; never overwrite history.
11. Repeat until the parent FAR investigation has sufficient explicitness, the respondent declines or cannot answer, the declared stopping rule is reached, or further questioning is non-material.

## Commitment versioning

A revision must:

- identify the superseded commitment;
- create a distinct replacement commitment;
- use a greater version number;
- retain the superseded commitment with status `REVISED`;
- identify the response event that authorized the revision;
- state why the revision occurred.

A withdrawal must retain the withdrawn commitment with status `WITHDRAWN` and identify the response event and reason.

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

Elenchus does not authorize silent selection of one interpretation. If materially distinct interpretations survive questioning, the Contract Discovery Protocol still requires them to remain in the active family unless an explicit exclusion is justified.

## Relationship to FAR reasoning

Stage 3 may use elicited definitions or interpretations with session provenance.

Stage 6 may use elicited commitments as premises only at their recorded scope and context. Any derived implication must identify its premises, calculus, and rule.

A later revision that changes a result-relevant commitment invalidates dependent reasoning to the extent required by the canonical FAR revision rules.

## Machine-readable record

The candidate interchange contract is `socratic-epistemic-extensions/1.0` with record type `ELENCHUS_SESSION`, governed by:

- `schemas/socratic-epistemic-extensions-v1.schema.json`;
- `mechanization/far_mechanization/socratic_epistemic.py`.

The validator checks event references, revision history, version ordering, implication-premise references, and contradiction references. It does not infer semantic contradiction from natural language.

## Failure conditions

The protocol fails if:

- a material respondent statement is replaced by an analyst paraphrase without preserving the original;
- a response is not linked to the question that elicited it;
- an implication lacks explicit premises, calculus, or rule;
- a contradiction is asserted without an explicit interpretation and calculus;
- a revision overwrites the prior commitment;
- a withdrawal deletes the prior commitment;
- materially different contexts are collapsed without an explicit bridge;
- conversational consistency is treated as external factual verification.

## Boundary

Elenchus produces evidence about commitments and their relations. External factual claims still require the evidence and validation required by the parent FAR investigation.

The name records a procedural resemblance to Socratic questioning. It does not establish historical derivation of Project FAR from Socrates.
