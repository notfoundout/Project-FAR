# Live Continuation Gate — Decision v2

Status: **NONCANONICAL runtime record.** Successor to
`continuation-gate-decision.md` (v1), preserved unamended. Evaluated 2026-08-14
against continuation freeze v4 on PR #452.

## Decision

**Live continuation NOT STARTED.** One gate fails. Failing closed is correct;
the failure is a credential absence, not a theoretical result.

The v1 evaluation stopped at three failures. Two have since been cleared by
independent work, so this evaluation reaches the irreducible one.

## Gate-by-gate

| Gate | v1 | v2 | Evidence |
|---|---|---|---|
| Live theory-state reconstruction coherent | PASS | PASS | `check_live_research_state.py` → PASS; ledger digest `6fc00bad…`. |
| Missing exact evidence recovered or bounded | PASS | PASS | `recovery-ledger-v2.md`; addendum ingested; every item classified. |
| Deterministic automation tests pass | PASS | PASS | 251 executor tests; falsification sweep 10/10. |
| Repository validation passes | PASS | PASS | `validate-full` SUCCESS; `make test` 1626/1626. |
| **Campaign source registered** | n/a (gate did not exist) | **PASS** | `campaign.json` pins `git:0ca73cb0…:b95a559a…`; 4 declared evidence paths verified readable from the frozen commit. |
| Claude lane available | FAIL | **PASS** | Sandboxed provider reports available; CLI on PATH; all tools denied; cwd outside the repository. |
| **GPT lane available** | FAIL | **FAIL** | `LIVE_GPT_BLOCKED: OPENAI_CREDENTIALS_REQUIRED`. No `OPENAI_API_KEY` in the environment. Credentials were not requested and must not be. |
| Historical calibration satisfies preregistered criteria | FAIL | FAIL | `CAL-DI3-S1` MISS on marker group 1. Unchanged, unweakened, test-pinned. |
| Governance permits execution | PARTIAL | PARTIAL | Every `PFAR-*` target is unauthorized and source-blocked. `REPO-UPP-SR-001-W1` is canonically authorized and dependency-valid, but executing it requires both lanes. `REPO-AUTHORITY-CONFLICT-001` is `GOVERNANCE_DECISION_REQUIRED` and excluded from selection. |

## What the gate attempt actually did

Two invocations of `far_adversarial_run.py run`, both fail-closed, no provider
contacted:

1. Before registering a source: `SOURCE_INTEGRITY_FAILURE: no registered
   campaign source. Run 'freeze <commit>' first; the current HEAD is never used
   implicitly.`
2. After registering: `LIVE_GPT_BLOCKED: OPENAI_CREDENTIALS_REQUIRED`.

The first is now cleared. The second is irreducible without a credential.

## Frozen-source isolation verified live

Against the registered campaign, not a fixture:

- appended `TAMPERED` to `docs/governance/limitations-register.md` in the
  working tree;
- the frozen source still served the clean bytes from
  `0ca73cb0…`;
- working tree restored, `git status` clean.

## Preserved dispositions

`PFAR-S1` was not restarted and not re-derived. `DI3` re-sustain was attempted
programmatically and raised `IssueReopenError`. The six upheld `PFAR-RC1`
objections and five live `PFAR-RC2` repairs are unchanged.

## Typed blockers

```
LIVE_GPT_BLOCKED: OPENAI_CREDENTIALS_REQUIRED
CALIBRATION_BELOW_PREREGISTERED_THRESHOLD: CAL-DI3-S1 group 1 missed
PRESENTING_FAR_QUEUE_BLOCKED: SOURCE_REQUIRED (exact E0, T1-T8, S1, S2, S6/S7)
GOVERNANCE_DECISION_REQUIRED: REPO-AUTHORITY-CONFLICT-001
```

The first is the single gate standing between this state and a live two-lane
run on `REPO-UPP-SR-001-W1`. The remaining three are independent of it.
