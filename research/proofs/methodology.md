# Proof Research Methodology

Status: Research; non-canonical

## Purpose

This document records working standards for constructing and evaluating proof attempts inside `research/proofs/`.

It does not govern Project FAR accepted proof status and cannot promote a research argument into an accepted result. Current theorem/proof status is controlled by the [Theorem and Proof-Status Register](../../docs/governance/theorem-proof-status-register.md), and canonical locations are resolved through the [Canonical Map](../../docs/CANONICAL_MAP.md).

When a research proof attempt uses canonical terminology, the current theory definitions are available at [`../../theory/definitions/definitions.md`](../../theory/definitions/definitions.md). This research document does not redefine them.

---

## Objective

A proof attempt should demonstrate that a stated conclusion follows from explicit premises by identified rules of inference. The intended result is logical necessity relative to those premises, not plausibility or empirical frequency.

---

## Scope

This guidance applies only to research-stage:

- lemmas;
- propositions;
- theorems;
- corollaries;
- proof attempts;
- proof revisions.

It does not replace canonical governance, accepted theory, or validation protocols.

---

## Recommended structure

A research proof attempt should identify:

- research identifier and title;
- research status;
- statement and scope;
- purpose;
- dependencies;
- assumptions;
- proof strategy;
- numbered inference steps;
- conclusion;
- consequences;
- limitations;
- related results.

Every dependency or assumption material to the conclusion should be explicit. A research attempt must not treat a later or unestablished result as an accepted premise without identifying that status.

---

## Proof strategies

Strategies may include direct proof, contradiction, contrapositive, construction, case analysis, or induction when the chosen strategy is justified by the stated premises and domain.

Each numbered step should state the claim established and identify the dependency, assumption, or inference rule used. Hidden inference is a defect to be exposed, not silently filled in.

---

## Completion and failure

A research attempt may use **Q.E.D.** only to mark that its own argument is intended as complete. That marker does not create accepted theorem status.

An incomplete proof, counterexample, contradiction, failed construction, or unresolved obligation remains a valid research result and should retain its actual status rather than be promoted by terminology.

---

## Quality checks

Research proof attempts should be checked for:

- explicitness;
- traceability;
- dependency discipline;
- hidden assumptions;
- undefined or equivocal terminology;
- circularity;
- unsupported generalization;
- justified scope;
- reproducibility.

Examples alone do not prove universal claims. Validation evidence alone does not constitute a formal proof. A failed validation result does not automatically refute a theorem unless the theorem's premises and falsification conditions make that inference valid.

---

## Revision and preservation

Research proof material may be revised when an error, stronger argument, dependency change, reduced assumption set, counterexample, or clearer reconstruction is established. Superseded or failed material should be preserved when it contains unique provenance or evidentiary value.

Any move from research status to accepted proof status must occur through the governed acceptance and promotion path and be recorded by the applicable canonical authority. This file cannot authorize that transition.
