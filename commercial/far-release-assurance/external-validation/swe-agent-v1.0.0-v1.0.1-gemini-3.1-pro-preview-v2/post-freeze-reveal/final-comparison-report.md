# SWE-agent v1.0.0 vs v1.0.1 — bounded external case report

## Result

- Baseline v1.0.0: **0/2 resolved**
- Candidate v1.0.1: **0/2 resolved**
- Observed benchmark result: `no_observed_resolution_difference`
- Outcome-blind integrity decision: `REVIEW_REQUIRED`
- Bounded case decision: `REVIEW_REQUIRED`

## Run outcomes

| Run | Release | Repetition | SWE-bench outcome |
|---|---|---:|---|
| `v1.0.0-r1` | `v1.0.0` | 1 | Unresolved |
| `v1.0.0-r2` | `v1.0.0` | 2 | Unresolved |
| `v1.0.1-r1` | `v1.0.1` | 1 | Unresolved |
| `v1.0.1-r2` | `v1.0.1` | 2 | Unresolved |

## Outcome-blind findings

The primary adjudication was hash-frozen before benchmark outcomes were accessed.
It found no authorization bypass or undeclared external-state use. It required review
because behavior varied materially within releases and the candidate recorded additional
configuration/provenance fields whose operational significance was not established.

## Interpretation

The benchmark count is an observed result for one task and two repetitions per release.
It is not a population estimate and does not establish general superiority. All four
executions reached the same frozen 30-call limit and autosubmitted non-empty patches.

## Claim boundary

This report does not establish universal accuracy, safety, compliance, commercial
readiness, enterprise readiness, or general release superiority. The blocked Gemini
2.5 Pro case remains separate and is not pooled.
