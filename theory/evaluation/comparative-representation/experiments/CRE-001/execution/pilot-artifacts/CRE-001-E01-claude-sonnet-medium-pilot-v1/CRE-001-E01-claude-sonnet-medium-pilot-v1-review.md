# CRE-001-E01 Claude Sonnet Medium Pilot v1 Review

Status: Preserved review complete; correction required; noncanonical.
Experiment: CRE-001.
Assignment: CRE-001-E01.
Evaluator: CRE-001-EVALUATOR-CLAUDE-SONNET-MEDIUM-01.
Submission: CRE-001-SUBMISSION-E01-CLAUDE-SONNET-MEDIUM-01.
Pilot type: single-prompt isolated AI evaluator pilot.
Canonical CRE-001 primary mapping: false.

## Raw artifact preservation status

The raw evaluator output was not present in the repository checkout available to this review and was not included as a byte-preservable JSON artifact in the task context. Therefore this review does not create, normalize, repair, or substitute a raw evaluator JSON artifact.

Required next action before immutable raw preservation can be complete: add the exact evaluator JSON byte-for-byte, except unavoidable final newline normalization, as `CRE-001-E01-claude-sonnet-medium-pilot-v1.raw.json` in this pilot-artifact record, then record its checksum in the adjacent metadata file.

## Administrative status

- This is pilot output, not an official canonical CRE-001 primary mapping.
- Calibration was self-assessed.
- Calibration and experimental materials were exposed in one prompt.
- No comparative or vocabulary-level conclusion is permitted.
- The review is an internal-validity review only.
- The artifact is noncanonical, unadjudicated, and ineligible for canonical ingestion.

## Strengths

The evaluator reportedly:

- produced valid structured output;
- used only the assigned primitive categories;
- declared derived constructs;
- represented propositions, rule statuses, transitions, history, modification, and terminal branches;
- preserved the raw output's own assumptions and limitations;
- attempted canonicalization and complexity accounting.

## Required corrections

### A. Incorrect CIR clause references

C-HIST-2 incorrectly references L14, L21, L27, and L34 as the clauses supporting the `p_checked=true` dependency.

The relevant clauses are:

- L17: T_check sets `p_checked=true`;
- L19: T_accept requires `p_checked=true`;
- L25: T_reject requires `p_checked=true`;
- L31: T_disable_reject requires `p_checked=true`.

C-STATUS-2 incorrectly references L33 for the R_reject status update. The actual status-update clause is L36. L49 is the duplicate/cross-reference.

### B. Invalid or unsupported clause count

The submitted L=55 is not accepted as verified.

At minimum:

- L10 combines five independently meaningful rule-status fields;
- L2 aggregates eight derived declarations without a consistent rule for whether index declarations count toward L;
- several explicit prohibition clauses are absent or only implicitly represented;
- duplicate-merging decisions are not consistently documented.

A full recount from the corrected CIR is required.

### C. Derived-construct indispensability not demonstrated

The submitted D=8 is not accepted as verified.

In particular:

- `TerminalLabel` may be redundant with `p_halted=true` plus the no-outgoing-transition condition;
- `OutputSummaryLabel` may be derivable rather than indispensable.

The evaluator must test each construct for indispensability and report any construct retained only for convenience.

### D. Prohibited-transition occurrence is underrepresented

The scenario requires preserving whether a prohibited transition occurred.

The output does not define:

- attempted versus executed prohibited transitions;
- a violation event;
- a persistent violation variable or history item;
- exact trigger semantics.

Explicit handling or an Unknown/Partial assessment is required.

### E. Unterminated-output semantics are incomplete

The evaluator did not fully define how unterminated output is produced for a non-halted finite run or prefix.

An explicit rule or a declared ambiguity is required.

### F. Repeatability of T_disable_reject is unresolved

The listed preconditions for `T_disable_reject` remain true after its first execution unless `R_reject=active` is treated as an additional condition.

The evaluator must:

- identify this as a scenario ambiguity;
- avoid silently adding a precondition;
- explain both interpretations;
- downgrade operational preservation if the ambiguity cannot be resolved from the frozen scenario.

### G. Acceptance-after-modification branch is not explicitly represented

A valid branch appears to be:

- T_check;
- T_disable_reject;
- T_accept;
- T_halt.

The evaluator must represent this reachable branch or explicitly prove that the transition schemas already preserve it without relying only on illustrative paths.

### H. Preservation result is overstated

The submitted all-Pass vector and existential-sufficiency result are not accepted as justified.

This review's provisional assessment is:

- p_s: Pass;
- p_m: Pass or Partial;
- p_o: Partial;
- p_d: Pass;
- p_i: Partial;
- p_h: Pass;
- existential sufficiency: false pending correction.

These provisional review findings do not replace the evaluator's original scores in any raw artifact.

### I. Calibration includes interpretive additions

The calibration inferred:

- a global no-history-rewrite restriction;
- example meanings of ineligibility.

These are minor calibration assumptions, not fatal defects.

## Noncanonical status rationale

This pilot is noncanonical because it was a single-prompt isolated AI evaluator pilot, not an official primary mapping; calibration was self-assessed; calibration and experimental materials were exposed together; the output is unadjudicated; correction is required; canonical CRE-001 primary mapping is false; and raw evaluator preservation is pending until exact raw JSON is supplied.

## Next action

Evaluator correction pass after exact raw-output preservation. The evaluator has not been rerun by this documentation update.
