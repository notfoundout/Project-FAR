# Live Continuation Gate — Decision

Status: **NONCANONICAL runtime record.** Evaluated 2026-08-14 against the
continuation freeze `v1`.

## Decision

**Live continuation NOT STARTED.** Two independent gates fail. Failing closed
is the correct outcome; neither failure is a theoretical result.

## Gate-by-gate

| Gate | Result | Evidence |
|---|---|---|
| Live theory-state reconstruction is coherent | PASS | `live-theory-state.json`; `python tools/check_live_research_state.py` → PASS. |
| Missing exact evidence recovered or explicitly bounded | PASS (bounded) | `recovery-ledger.md`. Every Presenting FAR protocol identifier is classified; none is invented. |
| Deterministic automation tests pass | PASS | 93 new tests; `make test-fast` 1468/1468. |
| Repository validation passes | PASS | `make validate-full` → SUCCESS (29 checks). |
| Provider credentials available | **FAIL** | `LIVE_GPT_BLOCKED: OPENAI_CREDENTIALS_REQUIRED`. The Claude lane is available and was exercised; the adversarial lane has no credential. A single-lane run is not the adversarial protocol and must not be presented as one. |
| Historical calibration satisfies preregistered criteria | **FAIL** | `CAL-DI3-S1` MISS on marker group 1 (intra-sequent vs frontier level distinction). See below. |
| Current governance permits execution | PARTIAL | Every Presenting FAR target is `SOURCE_REQUIRED` and unauthorized. `REPO-UPP-SR-001-W1` is canonically authorized (`OP-22` / `UPP-SR-001`) and dependency-valid, but executing it requires both lanes. |

## Calibration record

Preregistration digest `6e03129580bbd98bd5010819da3c5405a4e7e91c56f059b2af6066e833651374`,
identical across all three runs. **No acceptance criterion was revised at any
point**, before or after any observed result.

| Run | Outcome | Why |
|---|---|---|
| 1 | `EXECUTION_FAILURE` | Claude CLI turn budget too low; the harness, not the case. Not scorable. |
| 2 | Leakage detected; **not scorable as blind** | The lane had filesystem access and reported, unprompted, that it had read the recorded Turn 33 answer and the marker list. It was right, and it refused to let the run be scored as a pass. Recorded as a harness defect. Fix: all tools denied, cwd sandboxed outside the repository. |
| 3 | **MISS** (graded) | Groups 0 and 2 fired: the lane judged the argument invalid and reconstructed the determinacy/determinism/canonicity separation correctly. Group 1 did not fire: it treated lists/sets/multisets as *plurality across presentations, each internally determined*, rather than as a distinct analytical level from the frontier. That is a different repair from the historical one. |

The miss stands as a miss. The graded run is the run reported.

Interpretation, stated narrowly: on one case with one lane, the workflow
recovered the load-bearing half of the Turn 33 correction (the DI3 defeat) and
did not recover the second half (the level distinction). One case is not a
calibrated workflow, and a single-lane result says nothing about the two-lane
protocol.

## What would unblock continuation

1. `OPENAI_API_KEY` in the environment for the adversarial lane.
2. Additional calibration cases, which require the recovered Presenting FAR
   artifacts — currently only Turn 33 has enough exact source material to build
   a blind case from.
3. For the Presenting FAR queue specifically: external recovery of `𝔈₀`,
   `T1`–`T8`, the frozen `S1` statement, `SR-B2 v2`, `CDE-v1`, and
   `FDI1`–`FDI5` from the original ChatGPT export.

Items 1 and 3 are evidence-supply steps, not research. Item 2 depends on 3.

## Typed blockers

```
LIVE_GPT_BLOCKED: OPENAI_CREDENTIALS_REQUIRED
CALIBRATION_BELOW_PREREGISTERED_THRESHOLD: CAL-DI3-S1 group 1 missed
PRESENTING_FAR_QUEUE_BLOCKED: SOURCE_REQUIRED (E0, T1-T8, S1, SR-B2, CDE-v1, FDI1-FDI5)
```
