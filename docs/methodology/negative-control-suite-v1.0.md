# Negative Control Suite v1.0

## Purpose

This standard tests whether Project FAR's evaluation machinery can reject invalid representations rather than merely accepting any encoding that reproduces selected outputs.

A confirmatory experiment cannot support a nontrivial-constraint claim unless its registered negative controls fail for the registered reasons.

## Core rule

Negative controls must be designed and frozen before confirmatory execution. They must be processed through the same compilation, lowering, verification, scoring, and adjudication paths as candidate mappings.

A verifier that accepts every negative control is not evidence of expressive adequacy; it is evidence that the evaluation contract is underconstrained.

## Mandatory control families

### NC-01 — Lookup-table substitution

Reproduce registered outputs without preserving transition structure, dependencies, or historical commitments.

Expected result: rejection for process and commitment loss.

### NC-02 — Dependency collapse

Merge distinct premises, rules, authorities, or causal dependencies into an undifferentiated support relation.

Expected result: rejection or explicit preservation failure.

### NC-03 — History erasure

Preserve final state while deleting the sequence and timing of rule changes, accepted and rejected modifications, or prior dependencies.

Expected result: historical-preservation failure.

### NC-04 — Hidden rule modification

Implement a rule change inside compiler behavior or external code while leaving the explicit representation unchanged.

Expected result: rejection for hidden operational machinery.

### NC-05 — Label-only semantics

Attach vocabulary labels to objects without encoding the semantic or operational distinctions those labels claim.

Expected result: semantic- or operational-preservation failure.

### NC-06 — Unrestricted interpreter

Use a general external interpreter that supplies any missing behavior without charging the interpreter as representational machinery.

Expected result: rejection or full interpreter cost attribution.

### NC-07 — Hidden auxiliary state

Store protected distinctions outside the declared candidate representation.

Expected result: rejection for undeclared state or information relocation.

### NC-08 — Provenance deletion

Reproduce conclusions while removing source, justification, revision, or adjudication provenance.

Expected result: information- or historical-preservation failure.

### NC-09 — Output-equivalent process substitution

Replace the registered reasoning process with a different process that happens to produce the tested outputs.

Expected result: failure of commitment equivalence.

### NC-10 — Primitive smuggling

Remove a tested primitive by renaming or relocating its function into metadata, derived constructs, verifier assumptions, or compiler code.

Expected result: rejection by the anti-reintroduction audit.

## Control manifest

Every control must declare:

- identifier;
- protected distinction violated;
- construction procedure;
- expected diagnostic;
- expected preservation-vector effect;
- expected cost treatment;
- whether detection is syntactic, semantic, operational, or manual;
- false-positive risk;
- false-negative risk.

## Execution requirements

1. Controls are frozen before candidate results are visible.
2. Controls use the same software versions and execution environment as candidates.
3. Control identity may be blinded where practical.
4. All outputs and diagnostics are preserved.
5. Unexpected passes and unexpected failure reasons are adjudicated and retained.
6. Controls may not be removed because they are inconvenient or difficult to detect.

## Decision rules

- Any mandatory control that unexpectedly passes blocks a general nontrivial-constraint claim.
- A control rejected for the wrong reason is unresolved, not passed.
- A control that cannot be constructed because the contract is underspecified exposes a contract defect.
- Candidate success cannot offset control failure.
- Post hoc verifier changes create a new experiment version and leave the original result intact.

## Minimum suite for a pilot

The first prospective pilot must include at least NC-01 through NC-10. Later experiments may add domain-specific controls but may not silently remove mandatory families.

## Reporting

Report the full control distribution, including passes, failures, unknowns, adjudications, and implementation defects. Do not summarize only the controls that behaved as expected.

## Permitted conclusion

Successful rejection supports only the claim that the tested evaluation machinery imposes the registered constraints within the tested scope. It does not establish that all invalid representations will be rejected.