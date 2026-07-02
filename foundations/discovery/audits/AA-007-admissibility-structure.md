# AA-007 — Admissibility Structure Artifact Audit

## Status

Active Artifact Audit

## Target

`frameworks/FARA/admissibility-structure.md`

## Objective

Audit the FARA Admissibility Structure document against Phase II standards using only the fetched repository contents.

This audit does not revise the target document directly.

## Source Evidence

The document defines the Admissibility Structure within FARA.

It says the Admissibility Structure represents the classification of candidates according to a reasoning calculus within an investigation.

It also says the structure does not perform reasoning or determine how candidates are generated.

The definition states that Ω classifies candidates admitted for consideration within an investigation according to the applicable reasoning calculus.

## Audit Criteria

- hidden assumptions;
- dependency clarity;
- scope clarity;
- explicitness;
- category collapse under MI-001;
- grounding consistency with GP-005, GP-006, GP-007, and GP-008;
- knowledge traceability;
- revision justification.

## Findings

### AA-007-F1 — Strong Separation of Representation and Procedure

The document explicitly says the Admissibility Structure provides a representation of admissibility rather than a procedure for determining admissibility.

This is a strength.

It avoids collapsing record, procedure, and execution.

### AA-007-F2 — Classification and Record Are Mostly Clear but Still Need Typing

The document says Ω classifies candidates and also records admissibility determinations.

This is coherent if Ω is treated as a structured representation of classification results.

However, future revision should clarify whether Ω is:

- the classification relation;
- the representation of the classification relation;
- the current classification state;
- or the artifact recording the classification state.

### AA-007-F3 — Candidate Is Ungrounded in This Document

The document depends heavily on candidates but does not define candidate here.

The dependency is expected because definitions are delegated to `theory/definitions/definitions.md`.

However, admissibility cannot be fully grounded until candidate status, candidate generation, and candidate representation are distinguished.

Recommendation: future audits should inspect candidate-related definitions.

### AA-007-F4 — Reasoning Calculus Carries Most Determinative Load

The document states that admissibility is determined solely by the applicable reasoning calculus operating within the investigation.

This cleanly separates Ω from the determining procedure.

However, it also means Ω depends heavily on an explicitly defined reasoning calculus.

Recommendation: audit the reasoning calculus definition and its relation to admissibility before revising Ω.

### AA-007-F5 — Resolution Is Properly Separated

The document says Ω does not itself produce a resolution and that resolution is obtained by applying a resolution rule to classified candidates.

This is a strong category separation.

It keeps admissibility classification distinct from final resolution.

### AA-007-F6 — Traceability Language Requires Clarification

The document says every admissibility classification can be traced to the reasoning process that produced it.

This may conflict slightly with the earlier separation between Ω as a record and reasoning calculus as the determining mechanism.

Recommendation: specify whether traceability points to reasoning process, reasoning calculus, transition history, or evidence record.

### AA-007-F7 — Knowledge Traceability Is Absent

The document delegates formal definitions to `theory/definitions/definitions.md`, but it does not link to grounding investigations or Knowledge Layer objects.

Relevant knowledge objects include C-002 and H-001, because Ω depends on separations among rule, execution, representation, and classification.

Recommendation: after Knowledge Layer validation, link Ω claims to supporting investigations and claim objects.

## Overall Assessment

This is the strongest of the three audited FARA subdocuments so far.

It explicitly separates admissibility representation from procedure, reasoning, candidate generation, and resolution.

The main remaining instability concerns the typing of Ω itself and its dependence on candidate and reasoning calculus definitions.

## Revision Recommendation

A future revision is useful but not urgent.

Recommended future distinctions:

- Admissibility Status;
- Admissibility Classification;
- Admissibility Structure;
- Representation of Admissibility Structure;
- Reasoning Calculus;
- Resolution Rule;
- Candidate Generation.

## Audit Outcome

Status: Provisionally strong.

Requires follow-up audits of candidate, reasoning calculus, and resolution rule definitions before major revision.
