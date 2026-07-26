# v1.0.0 versus v1.0.1 behavioral comparison

Status: **Research; derived analysis**

Both versions ran the **same single task twice**; the request's phrase “both frozen tasks” is disproven by the task record and final report. Equal 0/2 counts establish only `no_observed_resolution_difference`, not equivalence.

| Dimension | v1.0.0 | v1.0.1 | Evidence-bounded interpretation |
|---|---:|---:|---|
| Calls/steps | 31/31 each | 31/31 each | Same budget boundary. |
| pytest commands | 1, 1 | 1, 2 | Candidate r2 attempted one more pytest command; relevance unknown. |
| tracked repository paths | 0, 2 | 0, 0 | Baseline r2 uniquely changed tracked implementation/test paths; other patches were exploratory-root-only by package summary. |
| patch bytes | 2170, 3890 | 2843, 3288 | All nonempty and applied; size does not establish quality. |
| target outcome | fail, fail | fail, fail | No observed resolution difference. |
| neighboring tests | 9 pass each | 9 pass each | No observed regression in the reported PASS_TO_PASS set. |
| provider failures | none recorded in packages | none recorded in packages | Absence from aggregates is not proof of no transient event. |
| stopping | exit_cost | exit_cost | Larger bottleneck plausibly neutralized differences; causal effect unknown. |
| tokens/cost/time | unknown | unknown | Source records absent. |

v1.0.1 changed intended configuration fields as the final report records and changed observable command/path behavior, but exposure is too small to classify improvement or regression. Within-version variability is material. No general release-effect conclusion is supported.
