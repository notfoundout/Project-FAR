# FAR-SAT-v0.4 Falsification Record

Status: Complete

## Null hypothesis

No new contract is necessary. All v0.4 saturation capabilities reduce to existing canonical FAR primitives.

## Elimination tests

### Translation provenance
Result: null sustained. Existing interpretation and provenance mechanisms can carry translated representations and their derivation. No translation-specific primitive is necessary yet.

### Search stopping / saturation
Result: null sustained. `far-intake-v1` already requires a stopping rule and supports saturation rounds, exclusions, completeness claims, and manual review for nontrivial completeness claims.

### Generic assurance graph vocabulary
Result: null sustained. Existing knowledge-graph claim, premise, assumption, evidence, relation, assessment, rebuttal, and caveat objects are sufficient to express the graph itself. Only a required audit-assurance profile remains missing.

### Source dependence
Counterexample: three documents can cite or copy one originating report. Current source/evidence records can list all three but do not require a machine-readable common-lineage or independence key. Counting records can therefore be mistaken for independent corroboration.
Result: null fails.

### Bitemporal state
Counterexample: an evidence source publishes statement P on day 1, retracts it on day 10, and FAR learns of the retraction on day 12. A single timestamp cannot answer both "what was asserted/valid on day 5?" and "what did FAR know on day 11?".
Result: null fails.

### Explicit abstention
Counterexample: a verifier cannot safely interpret a source because the material is inaccessible or semantically ambiguous. `unresolved` can record a dispute result but cannot distinguish deliberate non-adjudication from an adjudicated tie without a reasoned abstention record.
Result: null fails.

### Audit self-assurance profile
Counterexample: two audit reports may expose identical final claim statuses while only one performed falsification search, inference checking, or hostile-source isolation. Existing graph vocabulary can encode these facts if supplied, but no bounded contract requires them.
Result: null fails.

### Hostile-source control boundary
Counterexample: a document under audit contains instructions addressed to an AI reviewer. If source text can influence control policy rather than remain quoted evidence, the audited object can alter the auditor.
Result: null fails.

## Result

The null hypothesis is rejected only for the bounded surviving gaps. Expansion beyond those gaps remains unsupported.
