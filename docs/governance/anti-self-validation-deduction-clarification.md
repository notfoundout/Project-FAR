# Anti-Self-Validation Deduction Clarification

## Status

Prospective governance clarification effective upon merge.

## Purpose

The Anti-Self-Validation Standard was written primarily for confirmatory experiments. Its controls remain binding for empirical evaluation, comparative claims, implementation replication, external validation, and claims of independent confirmation.

Project FAR now uses a deduction-first central program. This clarification defines how the Anti-Self-Validation Standard applies to theorem construction, proof checking, and independent proof review.

## Controlling interpretation

The Anti-Self-Validation Standard does not prohibit Project FAR authors from:

- defining a formal source class;
- stating axioms and theorem targets;
- constructing proofs;
- constructing countermodels;
- proving lower bounds or impossibility results;
- mechanizing proofs;
- revising a failed theorem through an explicit versioned process.

A project-authored proof is not independent verification. It may nevertheless be a mathematical proof if the conclusion follows from the declared assumptions under the stated formal system.

## Separate claim dimensions

The repository must distinguish:

1. **theorem status** — whether the proposition is proved, refuted, bounded, or unresolved;
2. **mechanization status** — whether the formal derivation is machine checked and under which trusted assumptions;
3. **independent proof-review status** — whether external reviewers reconstructed, verified, or challenged the proof;
4. **empirical replication status** — whether a frozen evaluation was independently reproduced;
5. **application status** — whether implementations and domains satisfy a bounded formal contract.

A result in one dimension may affect another, but the statuses may not be silently merged.

## Scope of the original confirmatory gates

The staged gates in Section 17 of the Anti-Self-Validation Standard govern empirical and comparative conclusions produced from confirmatory experiments.

They do not impose the following dependency:

> independent empirical replication must occur before a representation theorem may be attempted.

Instead:

- independent replication is required before claiming independent empirical confirmation;
- formal theorem gates are required before claiming a theorem;
- mechanized verification is required before claiming a machine-checked theorem;
- independent proof review is required before claiming independent proof verification.

The applicable formal theorem gates are registered in `theory/evaluation/research-gates.json` and governed by `docs/governance/deduction-first-research-standard.md`.

## Universality and minimality

Experiments, case studies, and replication may provide bounded evidence, discover counterexamples, or expose ambiguous definitions. They do not by themselves establish mathematical universality or global minimality.

A formal universality claim requires a theorem quantified over an independently defined source class.

A formal minimality claim requires a declared candidate universe and an appropriate lower-bound, equivalence, uniqueness, or no-minimum result.

The original Anti-Self-Validation controls continue to govern any empirical universality, local-necessity, comparative-economy, or superiority claim.

## Independent review

Independent reviewers may discover a valid defect in a project-authored proof. If so, the theorem claim must be withdrawn, weakened, or revised.

Reviewer agreement does not substitute for a derivation. Reviewer disagreement does not automatically refute a valid derivation. The decisive issue is whether the formal conclusion follows from the declared assumptions and whether those assumptions and definitions support the stated scope.

Independent proof review remains required before using terms such as:

- independently verified proof;
- externally checked theorem;
- independently reproduced formal derivation.

## Mechanization

A proof assistant may verify a derivation relative to:

- its trusted kernel;
- imported libraries;
- Project FAR definitions;
- explicitly introduced axioms.

Mechanization does not establish that an axiom is true, that a source class captures every real reasoning process, or that a formalization matches an intended informal interpretation. Those remain separate obligations.

## Immutable failures and revisions

The original rules for immutable failures, scope changes, and versioned revisions apply fully to deductive work.

The repository must preserve:

- failed theorem versions;
- countermodels;
- proof gaps;
- assumptions introduced to repair a proof;
- scope restrictions introduced after a counterexample;
- mechanization failures;
- independent-review objections;
- superseded statements and their prior status.

A repaired theorem is a new version. It does not erase the earlier failure.

## Precedence

Where the original Anti-Self-Validation Standard uses experiment-specific language that could be read as making independent empirical replication a prerequisite for proof construction, this clarification and the Deduction-First Research Standard control that dependency question.

All stricter controls concerning experimental independence, competitor fairness, role separation, frozen packages, negative controls, hidden reintroduction, failure retention, and overclaim prevention remain unchanged.

## Nonclaims

This clarification does not establish:

- a valid representation theorem;
- the truth of Project FAR's axioms or definitions;
- FARA universality;
- primitive necessity;
- minimality or uniqueness;
- mechanized proof verification;
- independent proof review;
- independent empirical replication.

It prevents two distinct standards of justification from being conflated: deduction establishes what follows formally, while independent validation checks and challenges the work from outside the original construction path.