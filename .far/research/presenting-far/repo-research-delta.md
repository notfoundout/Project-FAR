# Canonical Repository State vs Latest Recoverable Research State

Status: **NONCANONICAL runtime research state.** This document changes no
canonical status, register, or claim. It records a comparison and nothing else.

- Canonical side: repository at `de5f1b23` (content-identical to `origin/main`
  tip `4bc964fd` plus the ingested reconstruction file).
- Research side: `.far/inbox/presenting-project-far.md`, as classified in
  `recovery-ledger.md`.

## Headline finding

**Current recovered evidence is insufficient to establish the exact mapping or
effect of Presenting FAR on canonical `OP-01`/`OP-02`/`OP-03` and related
claims. No canonical contradiction or supersession is currently established.**

An earlier version of this document concluded that the two research lines "do
not overlap." That conclusion is withdrawn. It inferred disjointness from
missing evidence, which is invalid. The two lines are at least substantively
adjacent:

- `OP-01` asks whether a non-vacuous **common reasoning architecture** exists
  outside the frozen UPP and W3 bounded classes. Presenting FAR's stated
  research question is the minimal architecture of reasoning, and its Turn 12
  records a surviving joint fragment `L_→` across LK proof search and CSP
  propagation — a candidate common-architecture result.
- `OP-02` asks whether Construct, Differentiate, Restrict are sufficient and
  irreducible outside `finite_coordinate_trace_v1`. Presenting FAR's Turn 2
  retyped **Construct** as a transformation/generator structure rather than a
  theory-valued function, and its Turn 4 replaced irredundant size with
  intrinsic minimum generating rank.
- `OP-03` asks whether Resolve, another fourth, or a fifth operator is
  irreducible. Presenting FAR's minimality step (Turn 13, step 7) is the same
  question approached without the FAR vocabulary in the premises.

Whether those bear on the canonical open problems as support, weakening,
refutation, or neither **cannot be determined**: the frozen targets (`T1`–`T8`),
the frozen source corpus (`𝔈₀`), and the adjudication protocol (`CDE-v1`,
`FDI1`–`FDI5`) are all `NOT_RECOVERED`. The relation is `MISSING_EVIDENCE`, not
`UNCHANGED` and not disjointness.

The two lines do differ in framing, and that difference is itself recoverable:

| | Canonical repository | Presenting FAR investigation |
|---|---|---|
| Question | Repair the bounded-v1 terminal derivation defects `XA-001`–`XA-005` and derive the strongest defensible successor theorem (`UPP-SR-001` / `OP-22`). | Discover the minimal architecture of reasoning without inserting Project FAR/RCCD into the premises. |
| Premises | FAR/FARA/RCCD vocabulary is the working frame. | FAR/RCCD explicitly demoted; RCCD is historical taxonomy, not a privileged target answer (Turn 13). |
| Frozen source | `f6645a77f3b0af0b12897fa9bc2c329cdb345261`. | `𝔈₀` — `NOT_RECOVERED`. |
| Targets | `SR-W0`–`SR-W8`. | `T1`–`T8`, `S1` — all `NOT_RECOVERED` except `S1`'s disposition history. |

## AUTHORITY_CONFLICT (recorded 2026-08-14)

An earlier version of this document stated that no `AUTHORITY_CONFLICT` was
found between canonical authority surfaces. **That was wrong**, and the claim is
withdrawn. A conflict exists and is recorded here rather than resolved, per
`AGENTS.md` §4 and `CLAUDE.md` §Authority: surface the conflict, do not silently
choose by recency or convenience, and do not rewrite it away.

`docs/project-status.md` §"Current authority navigation" ranks the surfaces:
`README.md` is #1, `project-status.md` is #2. Both are current authority. They
disagree about the standing of the central result.

| Surface | What it says | Location |
|---|---|---|
| `README.md` | "The registered Universal Proof Program `POST-TUE-UPP-001` is complete. Its terminal adjudication is: `strictly_weakened_relative_rccd_universality_theorem_proved_with_complete_dependency_audit_and_open_world_boundary`." No mention of the later defect finding. | `README.md:14-16` |
| `docs/governance/central-research-program.md` | "`POST-TUE-UPP-001` completed registered workstreams PR #281 through PR #296. The terminal result is: `…theorem_proved_with_complete_dependency_audit…`." No mention of the later defect finding. | `central-research-program.md:19-21` |
| `docs/project-status.md` | Adjudicated 2026-08-13: `FROZEN_V1_NOT_REFUTED_BUT_NOT_ESTABLISHED`. "the frozen registered derivation was found **defective** over part of its stated domain (`XA-001`–`XA-005`…)". Registers `UPP-SR-001`/`OP-22` as the successor repair. | `project-status.md:31-37` |

Mechanical check: `FROZEN_V1_NOT_REFUTED_BUT_NOT_ESTABLISHED`, `bounded-v1`,
`XA-00*`, `UPP-SR-001`, and `OP-22` each occur **zero** times in `README.md` and
zero times in `central-research-program.md`. They occur in `project-status.md`,
`open-problems-register.md`, `claim-status-matrix.md`,
`theorem-proof-status-register.md`, and `limitations-register.md`.

`project-status.md` is explicit that the terminal adjudication string "remains
the historical record for the frozen source; it is not silently rewritten." So
the two surfaces are not straightforwardly contradictory *about the frozen
record*. The conflict is about **presentation of current standing**: a reader
who stops at the higher-ranked surface (`README.md`) is told a theorem is proved
with a complete dependency audit, and is not told that a later dated authority
classifies that derivation as defective over part of its domain and has
registered a repair program for it.

**Affected inference, now stopped:** any claim that the repository's
current-authority surfaces agree on the standing of `POST-TUE-UPP-001`. That
claim is unresolved until governance rules on it.

**Not resolved here, deliberately.** Repairing `README.md` or
`central-research-program.md` would be a canonical documentation change, which
this noncanonical work is not authorized to make and which the charter forbids
choosing unilaterally. Registered in the live ledger as
`REPO-AUTHORITY-CONFLICT-001`, status `GOVERNANCE_DECISION_REQUIRED`,
unauthorized for autonomous execution.

**Provenance of the finding.** Surfaced by an independent parallel
reconstruction of this same investigation and verified here against the files
directly. This delta's own earlier "no conflict" claim was the defect.

## Authority-surface agreement elsewhere

**No canonical contradiction or supersession is currently established** by the
reconstruction either. That is a statement about what the recovered evidence
supports, not a finding that the investigation was irrelevant. The correct
classification for the `OP-01`/`OP-02`/`OP-03` relation is `MISSING_EVIDENCE`:
the reconstruction is substantively adjacent to all three, and the artifacts
that would fix the relation are absent.

## Per-item classification

| Item | Canonical status | Relation | Basis |
|---|---|---|---|
| `POST-TUE-UPP-001` terminal adjudication | Complete; terminal string preserved as historical record for the frozen source. | `UNCHANGED` | Presenting FAR never addressed it. |
| Bounded-v1 cross-audit finding `FROZEN_V1_NOT_REFUTED_BUT_NOT_ESTABLISHED` | Registered 2026-08-13. | `UNCHANGED` | Not addressed. |
| `UPP-SR-001` (`OP-22`) successor repair program | Registered; implementation not begun. | `REPO_AHEAD` | Fully specified canonically; entirely absent from the reconstruction. |
| `OP-06` / `PTE-W2` kernel reconstruction | Sequenced strictly after `SR-W7`. | `UNCHANGED` | Not addressed. |
| `FARA-FORMAL-KERNEL-001` Acceptance (scoped) | Accepted at v1.0 finite/explicit/auditable scope. | `UNCHANGED` | Not addressed. |
| `OP-01` non-vacuous common architecture | Open. | `MISSING_EVIDENCE` | Turn 12 records a surviving joint fragment `L_→` across LK proof search and CSP propagation — a candidate common-architecture result on the same question. Its definitions are `NOT_RECOVERED`, so whether it supports, weakens, or is orthogonal to `OP-01` is undetermined. Not `UNCHANGED`. |
| `OP-02` sufficiency/irreducibility of Construct, Differentiate, Restrict | Open. | `MISSING_EVIDENCE` | Turn 2 retyped **Construct** as a transformation/generator structure rather than a theory-valued function; Turn 4 replaced irredundant size with intrinsic minimum generating rank. Both bear directly on `OP-02`'s subject matter. The frozen formulations are absent, so the effect is undetermined. |
| `OP-03` irreducibility of Resolve / a fourth or fifth operator | Open. | `MISSING_EVIDENCE` | Turn 13 places minimality last in the sequence, approaching the same question without the FAR vocabulary in the premises. The minimality step's content is `NOT_RECOVERED`. |
| `OP-21` contract frontier | Executed; global comparison relation withdrawn. | `UNCHANGED` | Not addressed. |
| RCCD's role as a frame | Canonically the working vocabulary. | `TRANSCRIPT_AHEAD` | Turn 13 demoted RCCD to historical taxonomy **within the Presenting FAR protocol only**. This does not transfer: it is a methodological choice inside a separate, unrecoverable protocol, and nothing licenses applying it to canonical FARA/FAR. |
| `S1` / `DI3` / Turn 33 correction | No canonical counterpart exists. | `TRANSCRIPT_AHEAD` | Genuinely new. Recorded in the live ledger, not promoted. |
| `RC1` not freeze-safe; `RC2` repairs | No canonical counterpart. | `TRANSCRIPT_AHEAD` | Genuinely new, and `UNRESOLVED` past Turn 17 (`GAP`). |
| `T1`–`T8`, `𝔈₀`, `SR-B2`, `NM-v1`, `K-P1`, `FDI-v1`, `CDE-v1`, `FDI1`–`FDI5` | No canonical counterpart. | `MISSING_EVIDENCE` | Referenced by identifier only; defining text absent everywhere. |
| Three-lane blind first-pass method (`bounded-v1-closure-source-freeze-f6645a77`) | Accepted administrative practice, executed manually. | `SUPPORTED` | The Presenting FAR exchange independently ran the same shape — blind passes, frozen source, explicit concession, protocol repair — and it is the method this run automated. Method support, not theory support. |

## What the newer investigation actually changed

Four things, all inside the Presenting FAR protocol and none canonical:

1. **A defeated argument.** `DI3` was withdrawn. Absence of a canonical
   deterministic LK search strategy does not entail absence of a completely
   determined transition relation. This must never be re-run.
2. **A weakened negative claim.** "The calculus does not determine search
   structure" was replaced by "no eligible source encountered so far has been
   certified to determine the frozen frontier-level search structure."
3. **A level distinction.** Intra-sequent representation (lists/sets/multisets)
   is a different analytical level from frontier representation.
4. **A target disposition.** `S1` moved to `READY_UNDER_INTERNAL_PROTOCOL`
   (GPT Turn 34). Internal only; not Acceptance, and recorded in the ledger as
   a transcribed disposition rather than one this executor derived.

No canonical repository artifact is established as obsolete by any of this. Nor
is any established as unaffected: the `OP-01`/`OP-02`/`OP-03` relation is
undetermined pending recovery of the frozen Presenting FAR artifacts.

## Repository obligations that remain valid

All of them. Specifically `OP-22`/`UPP-SR-001` (`SR-W1`–`SR-W8`), `OP-06`
sequencing, `PTE-W1` independent review, `PTE-W3` countermodel search, `PTE-W4`
independent bounded replication, and every open `UQ-*`. Nothing recovered
discharges any of them.

`OP-01`, `OP-02`, and `OP-03` remain open and additionally carry an open
question about their own relation to the Presenting FAR line, which recovery of
the frozen artifacts would settle.

## Defeated attacks that must never be rerun

- `DI3` in all four of its forms (Turns 25, 28, 31, 32).
- The DF-02b overreach ("the calculus does not determine search structure").
- The intra-sequent/frontier conflation.

These are recorded as terminal-defeated in the live ledger and the ledger
mechanically refuses to return them to `OPEN`.

## Next executable research path

This section identifies what can be executed next. It is **not** a proven global
critical path to theory closure: a path claim of that kind would require knowing
the Presenting FAR line's effect on `OP-01`/`OP-02`/`OP-03`, and that is exactly
what the missing artifacts prevent.

Presenting FAR's own queue is source-blocked at step 0. The shortest
dependency-valid executable route from the current live state is therefore:

```
[A] Recover the exact 𝔈₀, T1-T8, S1 and S2 statements, and the exact S6/S7
    text, from the original ChatGPT export.           SOURCE_REQUIRED (external)
        |
        |  (blocks every Presenting FAR successor target. Turn 24 makes this
        |   binding rather than inconvenient: with 𝔈₀ absent or S1/S2 readiness
        |   unconfirmed, the protocol's correct outcome is a PRECONDITION STOP,
        |   no substitute domain or fragment is permitted, and inventing the
        |   definitions is forbidden.)
        v
[B] S6 -> S7, the successor step Turn 34 actually recorded  BLOCKED on [A]

Independent, and not blocked by [A]:

[C] UPP-SR-001 / SR-W1  determinate-absence representation   OPEN, authorized
        v
[D] UPP-SR-001 / SR-W2  weakest true W9 successor theorem    OPEN, blocked on [C]
        v
[E] SR-W3 / SR-W4 degenerate W8 / W11
        v
[F] SR-W5 recomposition -> SR-W6 regression -> SR-W7 validation and freeze
        v
[G] OP-06 kernel reconstruction (strictly after SR-W7)
```

`UPP-SR-001/SR-W1` is **the next fully specified, authorized executable research
path while Presenting FAR is source-blocked**. It is not the proven global
critical path to final theory closure, and it is not first merely because the
repository registers it. It is first among executable options because the
Presenting FAR queue cannot start without externally supplied evidence, and
`SR-W2`–`SR-W8` are blocked behind `SR-W1` by the program's own declared
sequencing. Whether `[A]` would, once recovered, reorder this queue is
undetermined.

Branches `[A]` and `[C]` are independent as far as execution goes and may run
concurrently. Running `[C]` does not contaminate `[B]`'s blind evaluation: they
share no target, no frozen source, and no registered issue.
