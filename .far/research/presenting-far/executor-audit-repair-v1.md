# Executor Audit and Repair — v1

Status: **NONCANONICAL runtime record.** Repairs to the adversarial executor
audited at commit `9551f424c3a74571e313d27787f66e601ea0d722`. No canonical
theory, register, status surface, or frozen evidence is changed by any of this.

An external code audit raised thirteen findings. Each was treated as a
hypothesis and checked against the implementation before anything was changed.

## Verification summary

| # | Finding | Verdict | Where it lived |
|---|---|---|---|
| 1 | Round ceiling wrote a terminal disposition | **VERIFIED** | `orchestrator.run_target` tail |
| 2 | A challenged lane could defeat an objection by saying REJECT | **VERIFIED** | `_ACTION_TO_STATE[REJECT] -> ISSUE_REJECTED ∈ DEFEATED` |
| 3 | Action legality was not actor-sensitive | **VERIFIED** | `apply_action` took `actor` and never compared it to `raised_by` |
| 4 | Source requests and formal obligations did not block closure | **VERIFIED, worse than reported** | appended as strings into `Target.source_dependencies`, which was also the evidence-path list |
| 5 | Any terminal predecessor satisfied a dependency | **VERIFIED** | `next_target` / `select_target` used `is_terminal()` |
| 6 | Frozen source was git HEAD while evidence came from the working tree | **VERIFIED** | `_source_freeze()` vs `_evidence_loader` |
| 7 | Replay verified hashes only | **VERIFIED** | `replay_run` never re-ran parsers or the reducer |
| 8 | Live Claude lane was not sandboxed like calibration | **VERIFIED** | `cmd_run` built `ClaudeCodeProvider` with no `sandbox_cwd` |
| 9 | Live GPT provider had no strict schema | **VERIFIED** | `cmd_run` passed no schema; Chat Completions; alias recorded as model |
| 10 | REVISE revised an issue, not the target candidate | **VERIFIED** | no candidate object existed |
| 11 | The delta claimed the research lines "do not overlap" | **VERIFIED** | inferred disjointness from missing evidence |
| 12 | Calibration history must be preserved | **VERIFIED as a requirement**; no defect found | v1 and its MISS were intact and remain so |
| 13 | Re-audit after repair | executed | see falsification pass below |

None of the thirteen was refuted.

## Root causes

1. **Finding 1** — the loop had one exit path and it wrote a status. The
   execution and epistemic vocabularies were separated in the *type* system
   (`EXECUTION_FAILURES` vs `TARGET_STATUSES`) but the round ceiling bypassed
   that separation by calling `set_target_status(UNDERDETERMINED)` directly.
2. **Findings 2 and 3** — one root cause: the issue state machine had no notion
   of who owns an objection. Every action was available to every actor, so
   `REJECT` was simply the challenged party's terminal move.
3. **Finding 4** — first-pass `source_requests` were treated as annotations
   rather than obligations, and were appended to a field that already meant
   something else, so a lane's free text could reach the evidence loader.
4. **Finding 5** — the dependency edge was untyped: it carried a target id and
   nothing about what condition the downstream target needed.
5. **Finding 6** — the source identity and the source *bytes* came from two
   different places, and nothing compared them.
6. **Finding 7** — replay was written against the evidence store rather than
   against the run, so there was no reconstructed state to compare.
7. **Findings 8 and 9** — the calibration path had been hardened after the
   leakage incident and the live path had not been brought along with it.
8. **Finding 10** — repair was modelled at the issue level only, so there was
   no object to hold a proposed target version.
9. **Finding 11** — a negative conclusion was drawn from absent evidence.

## Repairs

### Issue lifecycle (findings 2, 3)

`REJECT` no longer exists. The lifecycle is now:

```
RAISED by owner
  -> REBUT by challenged party        (objection stays live)
  -> owner review: SUSTAIN | WITHDRAW | REVISE | COUNTEREXAMPLE
       WITHDRAW  -> defeated   (owner only; the sole argumentative defeat route)
       SUSTAIN   -> live disagreement
  -> CONCEDE by challenged party      -> objection stands against the target
  -> SETTLE_BY_EVIDENCE               -> deterministic/formal/source actors only,
                                         evidence reference mandatory
```

`OWNER_ACTIONS` and `CHALLENGED_ACTIONS` are disjoint where it matters, and
`check_action_legality` refuses an out-of-standing move. A lane cannot call
`settle_issue` at all. The prompt contract sent to each side lists exactly the
actions that side may legally take, and the strict output schema enumerates the
same set, so an illegal action is rejected at the parser as well as the ledger.

A conceded objection now *refutes* the target rather than clearing it: conceding
means the objection was right.

### Execution versus epistemics (finding 1)

`run_target` returns `ROUND_LIMIT` with `resumable=True`, leaves the disposition
where it was, preserves every live issue, and closes nothing. `EPISTEMIC_STOPS`
and `EXECUTION_STOPS` are disjoint sets and a test asserts it.

### Obligations (finding 4)

`Obligation` is a first-class ledger object with kind (`SOURCE`/`FORMAL`),
state, `required_by_protocol`, and mandatory `resolution_provenance`. An
unresolved required obligation forces `SOURCE_REQUIRED` or
`FORMAL_CHECK_REQUIRED`. Discharge requires an adjudicating actor and a
provenance reference — a lane cannot discharge its own obligation. First-pass
source requests no longer touch `frozen_evidence_paths`, which is now a separate
input-contract field.

### Typed dependencies (finding 5)

`Dependency(target_id, requires=[...], accept_recorded=False)`. The default
`requires` is `ESTABLISHED_TARGET_STATUSES`, so `REFUTED`, `SOURCE_REQUIRED`,
`GOVERNANCE_DECISION_REQUIRED`, `UNDERDETERMINED`, `BLOCKED`, and
`FORMAL_CHECK_REQUIRED` do not unlock anything. A redirect edge is expressible
but must be written down. Execution stops never write a status, so they cannot
satisfy an edge by construction.

Added beyond the finding: `Target.status_basis` distinguishes a disposition this
executor derived from one transcribed out of the reconstruction, and a recorded
disposition does not unlock downstream work unless an edge sets
`accept_recorded`. `PFAR-S1`'s READY is recorded, not derived.

### Frozen source (finding 6)

`GitFrozenSource` reads blobs with `git cat-file blob <commit>:<path>`; the
working tree is never consulted. `ManifestFrozenSource` verifies a SHA-256 per
file before returning it. Both refuse undeclared paths and reject traversal. The
campaign source lives in `campaign.json`, written by an explicit `freeze`
subcommand; `run` refuses to start without it, and there is no code path from
`git rev-parse HEAD` to a source identity.

### Replay (finding 7)

`replay()` gates on reducer/schema/protocol version, verifies the frozen source
identity, verifies raw *and* normalized evidence hashes, checks the baseline
digest, then re-runs the real orchestrator with replay-backed providers —
rebuilding prompts from the frozen source, re-parsing stored raw bytes, and
re-applying events through the same reducer — and compares the reconstructed
final digest against the recorded one. No provider is contacted and nothing is
appended to the store.

Two supporting changes were needed to make reconstruction exact: the ledger
digest now excludes wall-clock fields, and first-pass evidence is recorded
sequentially in lane order even though the two calls run concurrently, because
invocation ids appear in issue provenance.

### Lane isolation and strict output (findings 8, 9)

`ClaudeCodeProvider.available()` fails with `SOURCE_INTEGRITY_FAILURE` when no
sandbox cwd is set, so an unsandboxed live lane cannot run at all. `Read`,
`Glob`, and `Grep` joined the denied-tool list. `OpenAIProvider` targets
`/v1/responses` with `text.format.strict = true`, requires a schema by default,
and types `completed` / `incomplete` / refusal / `failed` / malformed
separately. The served `model` is recorded in preference to the requested alias.

### Candidate repair (finding 10)

`Candidate` records predecessor, version, proposed formulation, changed
propositions, justification, issues addressed and introduced, regression and
formal status, and successor identity. `materialize_successor` creates a new
target with `requires_fresh_blind_pass=True` and asserts the predecessor's
formulation is unchanged.

### Delta conclusion (finding 11)

The "do not overlap" conclusion is withdrawn in `repo-research-delta.md`.
`OP-01`, `OP-02`, and `OP-03` are reclassified `MISSING_EVIDENCE` with the
specific adjacencies named. `UPP-SR-001/SR-W1` is described as the next fully
specified, authorized executable research path while Presenting FAR is
source-blocked — not as a proven global critical path.

### Calibration (finding 12)

Unchanged, deliberately. `CAL-DI3-S1` v1, its preregistration digest, and its
recorded MISS are pinned by a test: any edit to a stimulus, marker, or failure
marker changes the digest and fails, and a separate test asserts the missed
marker group still exists and still mentions both `intra` and `frontier`.

## Falsification pass (finding 13)

Each property was attacked with a test that fails against the pre-repair
implementation:

| Property | Attack | Result |
|---|---|---|
| Execution/epistemic separation | exhaust rounds mid-disagreement | disposition unchanged, issues preserved, dependency unsatisfied, target still selectable |
| Objection ownership | challenged lane tries WITHDRAW/SUSTAIN/REVISE; owner tries REBUT/CONCEDE | `IllegalActionError` on all five |
| Unilateral rejection | every action in `CHALLENGED_ACTIONS`, exhaustively | none reaches a defeated state |
| Unresolved source/formal closure | defeat all objections, leave one obligation | `SOURCE_REQUIRED` / `FORMAL_CHECK_REQUIRED`, never READY |
| Dependency satisfaction | every terminal status as predecessor, exhaustively | only `READY_UNDER_INTERNAL_PROTOCOL` unlocks; recorded basis refused |
| Freeze integrity | mutate then delete the working-tree file mid-campaign | frozen bytes still served |
| Replay determinism | tamper raw, tamper normalized, change reducer/schema/protocol, drift source, wrong baseline, wrong final digest | fails closed on all six; clean replay reproduces the digest |
| Lane evidence equivalence | compare prompts byte-for-byte after the role preamble | identical |
| Candidate successor handling | materialise a candidate | predecessor unmutated, successor distinct, fresh blind pass required |
| Calibration immutability | pin the preregistration digest and the missed group | any softening fails the test |

## Remaining blockers to live execution

Unchanged by these repairs, and one added:

```
LIVE_GPT_BLOCKED: OPENAI_CREDENTIALS_REQUIRED
CALIBRATION_BELOW_PREREGISTERED_THRESHOLD: CAL-DI3-S1 group 1 missed
PRESENTING_FAR_QUEUE_BLOCKED: SOURCE_REQUIRED (E0, T1-T8, S1, SR-B2, CDE-v1, FDI1-FDI5)
CAMPAIGN_SOURCE_UNREGISTERED: run refuses to start until `freeze <commit>` records one
```

No live campaign was started.
