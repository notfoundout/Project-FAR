# AA-003 — Foundational Discovery Protocol Artifact Audit

## Status

Active Artifact Audit

## Artifact

Foundational Discovery Protocol

## Objective

Evaluate whether the protocol cleanly separates discovery, investigation, evaluation, governance, and repository management under Phase II standards.

This audit does not revise the protocol directly.

## Audit Criteria

- hidden assumptions;
- circularity;
- dependency clarity;
- scope clarity;
- explicitness;
- category collapse under MI-001;
- evidence traceability;
- revision justification.

## Findings

### AA-003-F1 — Research Process and Repository Action Are Mixed

The protocol mixes the intellectual process of investigation with repository-level actions such as recording, revising, preserving, or canonizing artifacts.

This is a category collapse.

A discovery process may produce a result without immediately requiring a repository action.

A repository action may record or govern a result without being identical to the investigation itself.

Recommendation: distinguish investigation process from artifact lifecycle in future protocol revisions.

### AA-003-F2 — Discovery and Governance Remain Too Close

Discovery and governance remain adjacent in several workflows.

This risks allowing a research result to become repository authority without an explicit evaluation stage.

Recommendation: require an explicit evaluation stage before any governance action.

### AA-003-F3 — Investigation Termination Is Too Linear

The protocol assumes investigations terminate in a relatively linear way.

Phase II grounding suggests investigations may reopen after:

- new evidence;
- counterexamples;
- dependency revisions;
- methodology revisions;
- downstream failures;
- compression results.

Recommendation: define reopening conditions explicitly.

### AA-003-F4 — Negative Results Are Not Fully First-Class

Negative results are not consistently treated as permanent research outputs.

Failed reductions, rejected hypotheses, unsuccessful counterexample searches, and unresolved attacks are epistemically valuable.

Recommendation: preserve negative results as first-class research artifacts.

### AA-003-F5 — Investigation Process and Investigation Record Are Collapsed

The protocol does not consistently distinguish:

```text
Investigation Process
Investigation Record
Investigation Artifact
Investigation Outcome
```

This confirms the relevance of GP-007.

Recommendation: adopt the GP-007 decomposition during future revision.

### AA-003-F6 — Category Collapse Is Reproducibly Detected

Using MI-001 as a test criterion, this audit detected multiple category collapses in the protocol:

- process vs record;
- discovery vs governance;
- evaluation vs decision;
- negative result vs failed investigation;
- investigation closure vs repository action.

This supports MI-001 beyond the Grounding Pass family.

However, this is one artifact audit and does not yet justify methodological canonization.

## Overall Assessment

The protocol remains structurally sound but contains several concept collapses identified during Phase II grounding.

No immediate canonical revision is recommended.

The audit supports preserving the protocol until GP-006, GP-007, MI-001, and related validation work stabilize.

## Methodology Result

This audit strengthens MI-001 by showing that category-collapse analysis improves an Artifact Audit, not only Grounding Passes.

Current MI-001 status should remain under investigation, but the evidence base now includes:

- Grounding Pass evidence;
- Dependency Graph Audit evidence;
- Artifact Audit evidence.

## Research Debt

- Audit additional canonical methodology documents using MI-001.
- Determine whether category collapse is derivable from Explicitness and Orthogonality.
- Decide whether the protocol should be revised only after multiple audits converge.
