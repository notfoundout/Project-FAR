# PTE-W1 Independent Proof Review Protocol v1.0

## Status

This protocol is frozen. External execution has not yet occurred. The current evidential result is `Unknown`, not support and not defeat.

## Review object

The sole review object is the exact `UPP-W15-v1.0` strictly weakened relative RCCD theorem and its frozen dependency chain. Reviewers must not silently replace it with an unrestricted universality claim, an application claim, or a claim that the complete semantic theorem is one kernel-checked proof object.

## Independence rule

A review counts as independent only when the reviewer or review team:

- did not author Project FAR or the reviewed proof packages;
- is not organizationally controlled by the project author;
- discloses funding, collaboration, personal, employment, and publication conflicts;
- discloses prior exposure to mappings, results, review summaries, and candidate artifacts;
- discloses all software, language models, proof assistants, and external help used;
- has demonstrated competence reading formal specifications, state-transition systems, semantic preservation claims, and proof obligations.

Project-authored agents may prepare materials, run internal adversarial checks, and reproduce calculations. They cannot certify their own work as independent review.

## Frozen claim ledger

Every admissible review must issue a finding for each of these claims:

1. target class and scope;
2. faithfulness contract;
3. machinery closure;
4. commitment equivalence;
5. five component-necessity lemmas;
6. component independence;
7. relative sufficiency;
8. relative maximality;
9. terminal weakened outcome;
10. mechanization boundary;
11. open-world boundary;
12. `Unknown` discipline.

A review that omits, duplicates, merges, or silently redefines a claim is inadmissible.

## Finding schema

For each claim the reviewer records:

- reviewed: `Yes`, `No`, or `Unknown`;
- sound: `Yes`, `No`, or `Unknown`;
- material defect: `Yes`, `No`, or `Unknown`;
- exact evidence references;
- a reasoned explanation;
- any counterexample, failed derivation, hidden assumption, or reconstruction discrepancy.

The full submission also records theorem version, artifact digests, reviewer declaration, conflict statement, tool statement, and dependency-coverage statement.

## Adjudication

- Eligibility or disclosure failure: `inadmissible`.
- Unresolved independence, competence, artifact identity, or finding: `blocked/Unknown`.
- A material defect in target scope, faithfulness, sufficiency, or the terminal conclusion: presumptive retraction review.
- Other material defects: revision or narrowing review.
- Complete sound findings: independent-review evidence upgrade only. They do not create proof-assistant evidence, empirical replication, application correspondence, or a stronger theorem.

## Defect severity

A defect is critical when it defeats the theorem’s stated conclusion or makes the target class, faithfulness contract, or construction vacuous. It is major when it invalidates a material dependency but permits a narrower theorem. It is minor when it concerns exposition or non-material implementation details. Severity never overrides the three-valued finding itself.

## Anti-repair controls

After a submission begins, the project may not change the theorem object, target class, equivalence rule, machinery boundary, scoring rule, or admissibility criteria to rescue the claim. Any revision creates a new version and leaves the original review record immutable.

## Completion boundary

This workstream completes the review package and adjudication machinery. It does not claim that an independent review has been performed. The next action is `PTE-W1-EXTERNAL-REVIEW-EXECUTION`.
