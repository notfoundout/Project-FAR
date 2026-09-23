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

The executable replication is `tests/test_far_evidence_closure_replication.py`. It fails closed unless Git resolves `4e258fd3b7c5a80b6f7263ad6f2e085f913b1d2a:tools/check_investigation_execution.py` to exact blob `4d21937a471f55f3336d809a5378660e2a294c0c`. It then loads and executes those frozen validator bytes against a generic synthetic PASS manifest containing one completed required step, one repository-backed evidence artifact, no upstream dependency, and no `evidence_closure` field.

The frozen validator returns no validation errors for that manifest. The same manifest is then passed to the current validator, which rejects it because `FAR-EVIDENCE-CLOSURE-1.0` is absent. This directly executes both sides of the correction boundary rather than inferring the old behavior from source inspection alone.

## Observation

The defect reproduces at the frozen target:

- claim/execution success and methodological closure were not machine-separated;
- the workflow authorized `Resolved` after a recorded resolution;
- the exact frozen execution validator accepts the generic synthetic `pass` manifest without an evidence-closure record;
- the current validator rejects the same manifest for lacking `FAR-EVIDENCE-CLOSURE-1.0`;
- neither pre-correction controlling surface required a bounded post-evidence saturation gate.

This reproduces the structural early-closure path without depending on any particular application, dataset, claim, or prior conversation.

## Falsification check

The replication fails if the frozen path resolves to any blob other than the pinned validator blob, if the exact frozen validator rejects the generic manifest, or if the current validator accepts the same manifest without `FAR-EVIDENCE-CLOSURE-1.0`. The executable regression enforces all three conditions.

The corrected repository adds the missing distinction and dedicated negative regressions. Those regressions are implementation evidence for the repair; they do not replace execution of the exact frozen validator above.

## Replication result

**REPRODUCED.** At commit `4e258fd3b7c5a80b6f7263ad6f2e085f913b1d2a`, the exact frozen validator accepts a generic investigation satisfying its PASS prerequisites without a separate post-evidence closure contract, while the corrected validator rejects the same manifest.

## Scope and nonclaims

This replication establishes only the existence of the structural premature-closure path in the frozen pre-correction methodology and validator.

It does not establish that every historical investigation closed prematurely; it does not re-evaluate any application-domain result; it does not establish open-world evidence completeness; and it does not change Project FAR core theory, `far-ir/2.x` semantics, external-validation status, novelty, utility, or commercial status.
