# PBTS-001 Independent Replication Calibration v1.0

## Status

Frozen competency calibration for prospective PBTS-001 independent replicators.

This exercise is unrelated to PB-001 labels, primary pairs, RUN-001 cases, and RUN-001 judgments. It standardizes the ability to read formal process specifications, separate observations from inferences, preserve history-sensitive distinctions, and identify unsupported repair.

## Administration

The calibration must be completed before the participant receives the PBTS-001 participant-facing bundle.

The participant receives only the six items and response form. The calibration scorer applies the frozen rubric. The raw response, score, scorer identity, date, and any retest are preserved.

Passing requires:

- at least five of six items correct;
- a correct response to CAL-04;
- no material external assistance that is not disclosed.

One retest is permitted using the same items in a separately randomized order after at least one day. The first failure remains preserved.

## Response format

For each item provide:

- selected answer;
- brief justification;
- any ambiguity or assumption;
- tools or assistance used.

## CAL-01 — Partial-order history

Events `a` and `b` are incomparable. Both precede `c`. A record serializes the events as `a,b,c` and another as `b,a,c`.

Which statement is best supported?

A. The two processes necessarily have different causal histories.

B. The two serializations may represent the same partial-order history if neither introduces an order between `a` and `b`.

C. The first serialization is canonical because `a` appears alphabetically first.

D. The histories are equivalent only if all state labels are identical.

## CAL-02 — Admissible versus observed transition

A system specification permits transitions `x→y` and `x→z`. One execution observes only `x→y`.

Which claim is justified?

A. The system permits only `x→y` because `x→z` was not observed.

B. The execution observed `x→y`, while the specification still permits `x→z` unless other evidence invalidates it.

C. `x→z` must have occurred in an unobserved branch.

D. The specification and execution are contradictory.

## CAL-03 — Endpoint equality

Two procedures end in the same state `s`. In Procedure 1, a prior authorization remains valid. In Procedure 2, the authorization was revoked and later recreated under a different authority.

Which representation is adequate?

A. One that stores only final state `s`.

B. One that preserves the history or provenance needed to distinguish the current authority of `s`.

C. One that adds a note only when an evaluator asks.

D. One that assumes recreated authorization is always equivalent.

## CAL-04 — Observation versus inference

A model outputs an answer and a fluent explanation. No instrumentation, source code, or correspondence proof links the explanation to the computation that produced the answer.

Which conclusion is justified?

A. The explanation is a verified internal trace.

B. The explanation proves the model used the stated intermediate steps.

C. The explanation is an observed report; stronger claims about internal production remain unsupported.

D. The model did not reason.

This is the critical item. Any answer other than C fails the calibration regardless of total score.

## CAL-05 — Hidden repair

A compact representation omits a dependency relation. During evaluation, a custom script reconstructs the dependency from an external table that contains the source system's full graph.

Which classification is best?

A. The representation preserved the dependency because the evaluator recovered it.

B. The dependency is recovered through external machinery and must be counted; if it was prohibited or uncounted, preservation is not established.

C. The external table is irrelevant metadata.

D. The representation is minimal because it is compact.

## CAL-06 — Unresolved evidence

Two admissible interpretations of an opaque process produce different classifications, and the observation contract cannot distinguish them.

Which action is appropriate?

A. Choose the more favorable interpretation.

B. Average the classifications numerically.

C. Mark the item unresolved or unknown and state what evidence would resolve it.

D. Reject the process from the domain.

## Frozen scoring rubric

- CAL-01: B
- CAL-02: B
- CAL-03: B
- CAL-04: C
- CAL-05: B
- CAL-06: C

A response is correct only when the selected answer is correct and the justification does not contradict the governing distinction.

## Calibration nonclaims

Passing this calibration does not establish:

- independence;
- expertise across all D1-D16 domains;
- agreement with PB-001;
- the validity of any PBTS-001 judgment;
- qualification for R3 without the separate independence audit.

## Record requirements

Each calibration record must contain:

- permanent record identifier;
- replicator slot;
- response version;
- answers and justifications;
- tools and assistance;
- score by item;
- total score;
- critical-item status;
- pass or fail;
- scorer identity;
- administration and scoring timestamps;
- retest linkage where applicable;
- immutable digest.
