# AA-002 — Research Doctrine Artifact Audit

## Status

Research Audit

## Artifact Audited

`methodology/research-doctrine.md`

## Audit Objective

Test whether the Research Doctrine is coherent as canonical methodology, whether it conflates research status with governance status, and whether it has enough operational detail to guide discovery without pretending to prove theory.

This audit does not revise the doctrine.

## Summary Result

The Research Doctrine is structurally sound as high-level canonical methodology.

It correctly refuses framework preservation, requires explicit assumptions, preserves revisability, and applies standards to itself.

Its main defect is that it still treats `acceptance` and `promotion` too broadly. Later discovery work has shown that research state, logical status, authority level, and governance action must remain separate.

## Major Findings

### AA-002-F1 — Doctrine Correctly Rejects Framework Preservation

The doctrine states that Project FAR does not exist to defend FAR, FARA, FARO, or any previously proposed architecture.

This is a strong methodological constraint.

It prevents framework-first confirmation and supports discovery-first grounding.

Disposition: retain.

### AA-002-F2 — Explicitness Principle Needs a Relevance Limit

The doctrine requires every definition, assumption, scope boundary, dependency, inference, proof obligation, uncertainty, and limitation to be explicit.

Issue:

Unlimited explicitness is impossible and may create irrelevant noise.

Recent investigation suggests the stronger formulation is:

> Methodologically relevant implicit structure must be made explicit because only explicit structure can be independently evaluated.

Required action:

Future revision should distinguish relevant explicitness from total explicitness.

### AA-002-F3 — Promotion Hierarchy Collapses Artifact Kinds

The promotion hierarchy lists:

1. Observation
2. Question
3. Candidate
4. Hypothesis
5. Conjecture
6. Research Result
7. Lemma
8. Corollary
9. Theorem
10. Principle
11. Framework Component

Issue:

This sequence mixes different artifact kinds and research states.

A question does not become a theorem.

A definition does not become a lemma.

A methodology rule does not mature through the same path as a theorem.

Required action:

Replace or supplement the single promotion ladder with artifact-specific lifecycle models.

### AA-002-F4 — Acceptance Is Underspecified

The doctrine uses acceptance as a general endpoint.

Issue:

Recent discovery work separates:

- research state;
- logical status;
- authority level;
- governance action.

A claim may be provisionally stable as research, proven under assumptions as logic, and not yet canonical as governance.

Required action:

Future revision should replace broad acceptance language with explicit state dimensions.

### AA-002-F5 — Primitive Treatment Is Correctly Revisable but Not Basis-Relative

The doctrine states that every primitive remains open to reduction and replacement unless proven otherwise.

Issue:

It does not yet state that primitive status is basis-relative and methodology-relative.

Required action:

Future doctrine revision should define primitives operationally as current irreducible residuals relative to a specified basis, scope, and methodology.

### AA-002-F6 — Self-Application Is Strong but Needs an Audit Mechanism

The doctrine states that the research process is subject to the same standards of explicitness, traceability, falsification, and revision.

This is correct.

The later `methodology/methodology-audit-protocol.md` operationalizes this principle.

Disposition: retain and link to audit protocol in future revision.

### AA-002-F7 — Rejection Requirements Are Strong but Claim-Centered

The rejection requirements focus on claims.

Issue:

Not all artifacts are claims.

Definitions, questions, methodology rules, audits, architecture decisions, and repository decisions require distinct evaluation relations.

Required action:

Future revision should define rejection, revision, or demotion criteria by artifact kind.

## Cross-Cutting Findings

### 1. Doctrine Is Strong as Philosophy, Weaker as Operational System

The doctrine succeeds as a governing research ethic.

It is less complete as a workflow specification.

This is acceptable because later protocol documents provide operational detail.

### 2. The Doctrine Needs Artifact Profiles

The doctrine predates the artifact profile model.

Future revision should refer to artifact profiles rather than treating all research objects as claims.

### 3. No Immediate Rewrite Required

The doctrine is not misleading enough to require immediate replacement.

The correct next move is to keep auditing artifacts and then revise the doctrine once multiple audits confirm the same pressure points.

## Recommended Next Actions

1. Do not rewrite the doctrine immediately.
2. Record this audit as evidence that the doctrine is useful but not fully operational.
3. Audit the Foundational Discovery Protocol next.
4. After at least three methodology audits, produce one consolidated methodology revision instead of piecemeal edits.

## Methodology Audit

### Did the audit expose hidden assumptions?

Yes.

It exposed that the doctrine assumes a mostly claim-centered promotion model.

### Did it distinguish evaluation from governance?

Yes.

It identified that acceptance, proof status, research stability, and canonical authority are separate dimensions.

### Did it require immediate revision?

No.

The defects are real but not urgent enough to justify piecemeal doctrine edits.

### Did the methodology prove useful on a second artifact?

Yes.

The audit identified concrete structural pressure without destabilizing the repository.
