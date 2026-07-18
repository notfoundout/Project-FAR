# Confirmatory Research Package

## Purpose

This document is the required preregistration and execution template for any Project FAR study intended to support a confirmatory claim.

A completed package must be copied into the experiment directory and frozen before protected test data or results are exposed.

## 1. Registration Metadata

- Experiment identifier:
- Registration version:
- Registration timestamp:
- Theory version:
- Theory digest:
- Protocol version:
- Protocol digest:
- Repository commit:
- Exploratory or confirmatory:
- Planned execution date:

## 2. Tested Claim

Select exactly one primary claim:

- [ ] existence
- [ ] bounded sufficiency
- [ ] universality
- [ ] necessity
- [ ] minimality
- [ ] nontrivial constraint
- [ ] comparative economy
- [ ] independent replication

### Exact proposition

State the proposition in a form that can be false.

### Scope

Define the reasoning-process class, exclusions, and boundary criteria independently of the test cases.

### Supporting result

State the exact observed result that would support the proposition.

### Disconfirming result

State the exact observed result that would count against the proposition.

### Unresolved result

State which failures of measurement, reconstruction, comparison, or adjudication produce Unknown rather than support or disconfirmation.

## 3. Protected Theory Manifest

List all frozen theory commitments:

- primitives;
- relations;
- semantic commitments;
- admissible derived constructs;
- operations;
- preservation dimensions;
- scope rules;
- exclusions;
- termination rules;
- allowed auxiliary machinery.

Any substantive post-freeze change creates a new experiment version. The original result remains preserved.

## 4. Role and Independence Declaration

| Role | Person, team, or agent | Prior FAR involvement | Access restrictions | Independence class |
|---|---|---|---|---|
| Theory author | | | | |
| Scenario author | | | | |
| FAR mapper | | | | |
| Competitor advocate | | | | |
| Competitor mapper | | | | |
| Compiler author | | | | |
| Verifier author | | | | |
| Adjudicator | | | | |
| Red team | | | | |
| Nonclaim auditor | | | | |

Allowed independence labels:

- internal exploratory;
- internal isolated implementation;
- independent technical replication;
- adversarial conceptual replication.

Do not describe multiple implementations produced by one person or agent as independent external replication.

## 5. External Observation Contract

Define source-system observables without using FAR-native categories unless those categories are independently required by the source.

For each observable, specify:

| ID | Observable | Source evidence | Required distinction | Comparison rule | Failure effect |
|---|---|---|---|---|---|
| O-001 | | | | | |

Consider:

- admissible inputs;
- outputs;
- permitted transitions;
- forbidden transitions;
- dependencies;
- history;
- rule changes;
- uncertainty;
- provenance;
- ontology;
- counterfactual behavior;
- termination;
- information that must remain distinguishable.

## 6. Candidate and Competitor Provenance

For every vocabulary:

- authoritative source;
- version;
- advocate or reviewer;
- permitted clarification process;
- exclusions;
- known limitations;
- whether Project FAR authors designed or modified it.

A competitor designed only by FAR proponents must be labeled an internal benchmark.

## 7. Mapping Rules

Specify:

- mapper instructions;
- allowed source materials;
- forbidden access to other mappings;
- ambiguity procedure;
- mapping deadline;
- whether multiple mappings are required;
- how divergent mappings are retained;
- whether any mapping may be discarded and under what preregistered rule.

No inconvenient or unfavorable mapping may be silently removed.

## 8. Preservation Vector

Register the preservation dimensions and scoring rules.

Recommended vector:

\[
P=(p_s,p_m,p_o,p_d,p_i,p_h)
\]

Where:

- structural preservation;
- semantic preservation;
- operational preservation;
- dependency preservation;
- information preservation;
- historical preservation.

Allowed values:

- Pass;
- Partial;
- Fail;
- Unknown.

Unknown is unresolved, not an intermediate score between Partial and Fail.

## 9. Full-Cost Accounting

Each mapping must report:

| Dimension | Meaning | Counting rule | Tolerance |
|---|---|---|---|
| P | primitive commitments | | |
| D | derived constructs | | |
| O | operations and transformation rules | | |
| L | semantic description length | | |
| H | hidden or auxiliary state | | |
| A | ambiguity and adjudication policy | | |
| I | external interpreter or executable machinery | | |
| E | exceptions and case-specific patches | | |

Formatting and naming differences may be normalized only under a frozen canonicalization procedure.

## 10. Comparative Decision Rule

Default rule: Pareto comparison.

X dominates Y only if:

- preservation by X is no worse than preservation by Y;
- every registered cost of X is no greater than the corresponding cost of Y;
- at least one preservation or cost dimension is strictly better for X.

If neither dominates, report a tradeoff.

Do not create a weighted winner after results are visible.

## 11. Negative Controls

Register at least one control from every applicable class:

- output-equivalent lookup table;
- dependency collapse;
- history erasure;
- hidden rule modification;
- label-only semantics;
- unrestricted interpreter;
- hidden auxiliary state;
- provenance deletion;
- process-distinct but output-equivalent encoding.

For each control:

| ID | Invalid commitment | Expected verifier result | Failure implication |
|---|---|---|---|
| NC-001 | | Reject | |

If an invalid control passes, nontrivial constraint is not established.

## 12. Ablation and Hidden-Reintroduction Audit

Required for necessity claims.

For each removed primitive:

- forbidden aliases;
- forbidden equivalent relations;
- hidden-state audit;
- compiler audit;
- verifier-assumption audit;
- metadata audit;
- external-code audit;
- semantic-equivalence review.

A successful replacement counts against necessity when it preserves the contract at equal or lower total commitment.

## 13. Counterexample and Holdout Design

Describe:

- public development cases;
- private holdout cases;
- holdout custodian;
- generation method;
- target boundary classes;
- exposure controls;
- release procedure after execution.

The theory, metrics, and failure rules must be frozen before holdout exposure.

## 14. Execution Gates

Confirm before execution:

- [ ] claim frozen;
- [ ] scope frozen;
- [ ] theory frozen;
- [ ] observation contract frozen;
- [ ] competitors approved;
- [ ] metrics frozen;
- [ ] cost rules frozen;
- [ ] negative controls frozen;
- [ ] adjudication rules frozen;
- [ ] red-team review completed;
- [ ] holdout remains inaccessible;
- [ ] nonclaim language prepared.

Any unchecked gate keeps the study in intake or exploratory status.

## 15. Execution Record

Record:

- exact command or procedure;
- environment;
- implementation digests;
- input digests;
- output digests;
- deviations;
- failures;
- reruns;
- reasons for reruns;
- who had access to results at each stage.

## 16. Adjudication Log

Every dispute must record:

- disputed item;
- positions;
- governing preregistered rule;
- decision;
- adjudicator;
- whether the decision was known before unblinding;
- effect on the result.

## 17. Result Aggregation

Report the complete distribution across mappings and evaluators.

Do not report only the best mapping, majority result, or favorable resolved subset.

For sufficiency, distinguish:

- existential sufficiency: at least one valid mapping;
- reproducible sufficiency: all preregistered independent mappings valid.

Do not convert one into the other through aggregation.

## 18. Failure and Exclusion Record

List every:

- failed mapping;
- unresolved mapping;
- excluded case;
- discarded response;
- invalid run;
- protocol deviation;
- negative control that passed;
- scope challenge;
- theory change prompted by the study.

Nothing may be removed because it weakens the conclusion.

## 19. Evidential Classification

Select the maximum supported class:

- [ ] internal coherence
- [ ] internal implementation robustness
- [ ] bounded sufficiency
- [ ] nontrivial constraint
- [ ] local necessity
- [ ] comparative economy
- [ ] independent technical replication
- [ ] adversarial conceptual replication
- [ ] generalized universality argument
- [ ] bounded or universal conclusion

Provide the bridging argument for every class above the direct experiment output.

## 20. Claim-Ledger Update

Identify the affected claim-ledger entries and record:

- evidence added;
- evidence against;
- confidence direction;
- unresolved objections;
- scope changes;
- falsification status.

## 21. Nonclaim Audit

Before publication, identify claims the study does not establish.

At minimum address:

- truth of FAR;
- universality;
- necessity;
- minimality;
- superiority;
- external independence;
- commercial readiness.

## 22. Final Decision

State one of:

- supports the registered claim within scope;
- weakens the registered claim within scope;
- falsifies the registered claim within scope;
- unresolved;
- invalid due to protocol failure.

Do not replace this decision with a general narrative of success.