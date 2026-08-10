# SWE-agent v3 failure and arithmetic contract

Status: **Research — prospective pre-execution contract**  
Program ID: `FAR-SWE-V3-001`  
Execution authorized: **No**

This file originated as the v1.1 amendment that closed two design ambiguities. The current machine-readable authority is now standalone: `failure-arithmetic-amendment-v1.1.json` prospectively governs replacement/terminal-reason classification and exact arithmetic for FAR-SWE-V3-001 without depending on historical snapshot provenance.

It governs only:

1. the definition of a replacement-eligible infrastructure-invalid run and terminal-reason classification;
2. the numeric representation and comparison rules for primary estimates, bootstrap estimates, quantiles, and classification thresholds.

`historical-authority-v1.0.json` is archival context only. It intentionally does not self-prove that its snapshots occurred at the claimed historical commit, and current failure/arithmetic validity does not depend on that claim. Current authority for unrelated subjects comes from the current integrity-rooted design artifacts.

## Replacement boundary

A run may receive one same-slot replacement only when its terminal reason is one of the five closed-list pre-arm infrastructure reasons and every pre-exposure eligibility fact is true. In particular, no capsule or placebo bytes may have been mounted or read, no model request may have been accepted, no repository command may have run, no outcome may have been revealed, and the failure must be independent of task, arm, and capsule content.

Provider timeouts or failures after request acceptance, harness failures after exposure, budget exhaustion, and agent failures are unresolved or invalid under the frozen taxonomy and are never replacement-eligible. Grader infrastructure failures cause regrading of the same frozen evidence bundle, not an agent rerun. Any unlisted reason is invalid and nonreplaceable; execution stops until a prospective amendment is frozen.

## Exact arithmetic

Every probability, task contrast, bootstrap replicate, quantile interpolation, and threshold comparison uses reduced exact rational arithmetic over arbitrary-precision integers. Binary outcomes are exact integers. Sorting uses cross multiplication. Tail probabilities are exactly `1/40` and `39/40`; the practical threshold is exactly `1/10`. Floating-point values and displayed decimals never determine a classification.

## Verification

```bash
python research/external-validation/swe-agent-v3/verify_amendment_v1_1.py
python -m unittest tests.test_swe_agent_v3_amendment_v1_1 -v
```
