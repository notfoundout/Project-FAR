# FAR Evidence-Closure Defect Replication v1.0

Status: **Replication completed**

Date: 2026-09-22

## Objective

Reproduce, without application-specific subject matter, whether the pre-correction FAR repository permitted an investigation to declare a passing/resolved state after satisfying its registered execution steps while carrying no separate post-evidence closure record.

## Frozen target

The replication target is exact Project FAR commit:

`4e258fd3b7c5a80b6f7263ad6f2e085f913b1d2a`

Two controlling artifacts at that target were inspected by exact Git identity:

- `frameworks/FAR/workflow.md`, Git blob `2df3c1dadc4e0f7cbfc1e53d9160a77facc7d547`;
- `tools/check_investigation_execution.py`, Git blob `4d21937a471f55f3336d809a5378660e2a294c0c`.

## Question

Could a generic investigation satisfy the pre-correction machine PASS gate and the pre-correction `Resolved` closure rule without any distinct evidence-saturation, surviving-proposition, residual-uncertainty, or terminal saturation record?

## Execution

The frozen workflow closure rule was read directly. At the frozen target it defined `Resolved` as requiring only that “a resolution has been recorded under the stated resolution rule.” It contained no separate post-evidence closure contract.

The frozen execution validator was then reconstructed from its exact source. For a manifest whose `result` is `pass`, it required:

1. a non-empty `required_steps` list;
2. every required step to have a complete status;
3. every required step to carry repository-resolvable evidence;
4. every declared upstream dependency to have a canonical passing result.

The frozen validator contained no `evidence_closure` field, no evidence/search-class enumeration, no denominator/directness check, no measurement/classification ledger, no strongest-opposing-evidence requirement, no surviving-proposition or residual-uncertainty record, and no terminal per-class saturation pass.

A generic synthetic manifest can therefore satisfy every pre-correction PASS condition using one completed step, one repository-backed evidence artifact, and no upstream dependency while omitting every post-evidence closure obligation later defined by `FAR-EVIDENCE-CLOSURE-1.0`. Nothing in the frozen validator rejects that manifest for those omissions.

## Observation

The defect reproduces at the frozen target:

- claim/execution success and methodological closure were not machine-separated;
- the workflow authorized `Resolved` after a recorded resolution;
- the execution validator authorized `pass` after completed registered steps/evidence/dependencies;
- neither surface required a bounded post-evidence saturation gate.

This is sufficient to reproduce the structural early-closure path without depending on any particular application, dataset, claim, or prior conversation.

## Falsification check

The replication would fail if either frozen artifact already required a distinct post-evidence closure record or if a generic manifest satisfying the stated PASS conditions were rejected specifically for lacking such a record. Direct inspection of the frozen artifacts establishes neither condition.

The corrected repository adds the missing distinction and dedicated negative regressions. Those regressions are implementation evidence for the repair; they are not substituted for the frozen-target replication above.

## Replication result

**REPRODUCED.** At commit `4e258fd3b7c5a80b6f7263ad6f2e085f913b1d2a`, a generic investigation could satisfy the repository's PASS prerequisites and the workflow's `Resolved` rule without a separate post-evidence closure contract.

## Scope and nonclaims

This replication establishes only the existence of the structural premature-closure path in the frozen pre-correction methodology and validator.

It does not establish that every historical investigation closed prematurely; it does not re-evaluate any application-domain result; it does not establish open-world evidence completeness; and it does not change Project FAR core theory, `far-ir/2.x` semantics, external-validation status, novelty, utility, or commercial status.
