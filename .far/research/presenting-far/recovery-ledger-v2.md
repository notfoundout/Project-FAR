# Presenting Project FAR — Exact-Evidence Recovery Ledger v2

Status: **NONCANONICAL runtime research state.** Successor to
`recovery-ledger.md` (v1), which is preserved unamended. Produced 2026-08-14
after ingesting `.far/inbox/presenting-project-far-recovery-addendum-2026-08-14.md`.

## Correction to v1

v1 stated:

> the only occurrence of any Presenting FAR protocol identifier anywhere in the
> repository or on this machine is inside the reconstruction file itself.

That was true of **file-based search only** — the working tree, every reachable
object across all branches, and local session state. It was not true of all
recoverable evidence: retained prior-conversation records are a separate
channel, and searching them after the user supplied the shared-conversation URL
recovered substantially more protocol content.

The v1 wording implied a completeness it had not established. Every
`NOT_RECOVERED` verdict in v1 should be read as `NOT_RECOVERED_IN_REPOSITORY`,
and the builder now emits that narrower label.

## Source channels

| Channel | Artifact | Class |
|---|---|---|
| Primary reconstruction | `.far/inbox/presenting-project-far.md` | NONCANONICAL / INCOMPLETE RECONSTRUCTION |
| Recovery addendum | `.far/inbox/presenting-project-far-recovery-addendum-2026-08-14.md` | NONCANONICAL / RECOVERED CONVERSATION-STATE EVIDENCE |

The addendum is **not** a verbatim scrape of the shared-conversation URL: the
public fetch available to that recovery process did not expose the conversation
body. Its items are `RECONSTRUCTED-HIGH` unless labelled otherwise and must not
be upgraded to verbatim transcript.

## Revised recovery classification

### Improved by the addendum

| Identifier | v1 | v2 | What is now held |
|---|---|---|---|
| `SR-B2 v2` | `NOT_RECOVERED` (fact only) | `RECOVERED_PARTIALLY` | A finite search procedure: six fixed queries per OPEN target; ten results per query; up to five `NM-v1` near-matches eligible for follow-up; two title/author follow-ups per near-match; an `EXACT`/`DIRECT` positive permits early positive stop; `SOURCE-FAIL` requires exhausting all prescribed invocations; `S1` reruns from query 1. |
| `SR-B2 v1` | retired, no detail | `RECOVERED_PARTIALLY` | Retired as capability-infeasible. Under v1, `S1` stayed OPEN until finite retrieval was exhausted; strong negative-looking evidence could not produce `SOURCE-FAIL` before the registered search completed. |
| `NM-v1` | fact only | `RECOVERED_PARTIALLY` | Deliberately broad at retrieval: same **formal family**, **structural role**, or **provenance** qualifies a near-match for inspection. |
| `K-P1` | fact only | `RECOVERED_PARTIALLY` | Strict at final eligibility. A focused-LK paper may enter the `N1`/near-match pool and still fail admissibility. The two-stage design is broad recall, strict precision. |
| `FDI-v1` | `NOT_RECOVERED` | `RECOVERED_PARTIALLY` | A five-condition frontier-DI certificate for frozen `S1`, requiring source-defined partial derivations; an open-leaf frontier with its multiplicity/structure; one-step source-induced evolution; frontier-quotient well-definedness. Partial derivations alone explicitly insufficient. |
| `CDE-v1` | `NOT_RECOVERED` | `RECOVERED_PARTIALLY` | Permits canonical definitional expansions from source-defined structure **with no free methodological parameters**. Fixed at Turn 34. |
| `FDI1`–`FDI5` | `NOT_RECOVERED` | `RECOVERED_PARTIALLY` | Existence and role recovered; `FDI4` recorded as satisfied by `DI2`. The clause-by-clause mapping is **not** recovered, and the addendum explicitly forbids inventing it. |
| `DI1`–`DI6` | not previously identified | `RECOVERED_PARTIALLY` | An explicit direct-instantiation boundary, not an informal restriction. Excludes analyst-supplied primitive structure and cross-source assembly. `DI1` participates in the Turn 34 `DIRECT` classification. |
| Turn 24 | `GAP` | `RECOVERED_PARTIALLY` (state, not body) | Precondition stop: if `S1`/`S2` were non-READY, the `𝔈₀` shared-content fragments became **UNTESTABLE**; no substitute domain or fragment permitted; correct outcome a **PRECONDITION STOP** / domain-instantiation failure, not an invented replacement. |
| Turn 25 | disposition only | `RECOVERED_PARTIALLY` | The negative source result was procedural and exhaustion-bounded, not a free-form judgment. |
| Turn 34 | bare state transition | `RECOVERED_PARTIALLY` | Adjudication route: `FDI4` satisfied by `DI2`; `CDE-v1` fixed; **Liang–Miller member 2** classified `DIRECT` under `DI1` plus the `FDI1`–`FDI5` structure; `S1` READY; `c0` survived; remaining action recorded as **`S6 → S7`**. |
| Miller source | `NOT_RECOVERED` | `SOURCE-IDENTIFICATION-HIGH` | Dale Miller, *A Survey of the Proof-Theoretic Foundations of Logic Programming*, arXiv:2109.01483 (2021). |
| Liang–Miller source | not previously identified | `SOURCE-IDENTIFICATION-HIGH` | Chuck Liang and Dale Miller, *Focusing and Polarization in Intuitionistic Logic*, arXiv:0708.2252 (2007). |

Both source identifications are lookups, not transcript wording. **Do not
collapse the two papers** without the original candidate ledger: the dialogue
may have used them as distinct members of a source/candidate set.

### Still `NOT_RECOVERED` exactly

- exact text of `T1`–`T8`;
- exact `𝔈₀` definition;
- exact frozen `S1` statement;
- exact `S2` statement and its disposition;
- exact `S6`/`S7` statements and the `S6 → S7` transition requirement;
- exact full `DI1`–`DI6` text;
- exact full `FDI1`–`FDI5` clause text and its phrase-to-label mapping;
- exact full `CDE-v1` definition;
- the six fixed `SR-B2 v2` queries;
- exact Turn 33 truncated ending (the addendum recovered no completion);
- verbatim message bodies for Turns 1, 6–11, 14, 16, 18–22, 24.

### Unchanged from v1

The Turn 33 verbatim excerpt remains the authoritative record for its content:
`DI3` withdrawn; nondeterminism compatible with a completely determined
transition relation; intra-sequent and frontier representation distinct; the
weakened negative source claim. The addendum adds nothing to it and removes
nothing from it.

## New live-state consequences

Two targets that v1 and v2 could not name now exist in the ledger:

- **`PFAR-S2`** — named by the Turn 24 precondition stop as a second gating
  S-target. Its disposition is unrecovered, and it gates the `𝔈₀` fragments
  independently of `S1`. **Do not infer S2's status from S1's.** Recorded
  `UNDERDETERMINED`.
- **`PFAR-S6-S7`** — the remaining action the investigation actually recorded
  after Turn 34. This is the first time the reconstruction names a specific
  successor step; v1 and v2 could only say the successor queue lived inside
  `T1`–`T8`. Recorded `SOURCE_REQUIRED`.

Naming the next action is not recovering it. `S6` and `S7` remain unexecutable
and must not be invented.

## Consequence for the queue

The missing-evidence set is materially smaller, and it is **still blocking**.
Autonomous Presenting FAR continuation remains unauthorized because the exact
frozen `𝔈₀`, `T1`–`T8`, and `S1` statement are unavailable — and the Turn 24
precondition stop makes that binding rather than inconvenient: without a
recovered `𝔈₀` and confirmed `S1`/`S2` readiness, the correct protocol outcome
is a precondition stop, not a substitute.

`PFAR-S1` stays `READY_UNDER_INTERNAL_PROTOCOL` on a recorded basis and stays
unauthorized for restart. `DI3` stays withdrawn.
