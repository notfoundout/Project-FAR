# Presenting Project FAR — Exact-Evidence Recovery Ledger

Status: **NONCANONICAL runtime research state.** Not Accepted, not Promoted, not
a canonical Project FAR artifact. Produced 2026-08-14.

Primary source: `.far/inbox/presenting-project-far.md` (itself labelled
NONCANONICAL / INCOMPLETE RECONSTRUCTION).

## Search performed

Every identifier below was searched over:

- the full working tree at `de5f1b23` (all paths, all file types);
- every reachable object across all branches of `notfoundout/Project-FAR`
  (`git grep` over `git rev-list --all`, plus `git log --all -S`);
- local session and agent state (`~/.claude/`, `/tmp/claude-*`, `/home/user/`).

Result: **the only occurrence of any Presenting FAR protocol identifier
anywhere in the repository or on this machine is inside the reconstruction file
itself.** Two commits contain that file (`d57dfec1` on
`origin/claude/presenting-far-transcript-ingest`, and its cherry-pick
`de5f1b23` on this branch); they are the same 301 lines.

Frozen evidence was read only. Nothing was modified during the search.

## Evidence classes

Three classes, never collapsed:

- `EXACT_TRANSCRIPT_EVIDENCE` — wording present in the reconstruction under the
  `VERBATIM-RECOVERED` label.
- `RECONSTRUCTED_RESEARCH_STATE` — substance present under `RECONSTRUCTED-HIGH`;
  wording is **not** a quotation.
- `MISSING_TRANSCRIPT_EVIDENCE` — marked `GAP`, or referenced by identifier
  with no defining text anywhere.

## Recovery classification

| Identifier | Class | Recovery | What is actually held |
|---|---|---|---|
| Claude Turn 33 body | `EXACT_TRANSCRIPT_EVIDENCE` | `RECOVERED_PARTIALLY` | Verbatim through "I now think S1 is more likely to reach READY than I" — the source truncates mid-sentence. The final clause is **not** recovered and must not be completed. |
| `DI3` | `EXACT_TRANSCRIPT_EVIDENCE` | `RECOVERED_EXACTLY` (as refuted) | The argument and its defeat are stated verbatim in Turn 33: it ran across Turns 25, 28, 31, 32 and conflated "no canonical deterministic search strategy" with "transition relation not completely determined". Withdrawn. |
| `DF-02b` revised wording | `EXACT_TRANSCRIPT_EVIDENCE` | `RECOVERED_EXACTLY` | "No eligible source encountered so far has been certified to determine the frozen frontier-level search structure." |
| Intra-sequent / frontier distinction | `EXACT_TRANSCRIPT_EVIDENCE` | `RECOVERED_EXACTLY` | Turn 33 §4 concession: lists/sets/multisets inside one sequent is a different level from frontier representation. |
| `S1` (frozen statement) | `MISSING_TRANSCRIPT_EVIDENCE` | `NOT_RECOVERED` | Only two constraints survive, both from Turn 33: transitions are all one-rule backward applications, and the target requires a completely determined transition relation at the frontier level. The frozen text itself is absent. |
| `S1` disposition history | `RECONSTRUCTED_RESEARCH_STATE` | `RECOVERED_PARTIALLY` | OPEN under `SR-B2` at Turn 25; DI3 withdrawn at Turn 33; moved to READY by GPT Turn 34 under the then-current frozen protocol. Turn 34's wording is not recovered. |
| `T1`–`T8` | `MISSING_TRANSCRIPT_EVIDENCE` | `NOT_RECOVERED` | Only that GPT Turn 4 froze them alongside intrinsic minimum generating rank and a translation-rank spectrum. No definitions. |
| `𝔈₀` | `MISSING_TRANSCRIPT_EVIDENCE` | `NOT_RECOVERED` | Only its position in the Turn 13 sequence (freeze `𝔈₀` → native extraction → witnesses → joint profiles → common theory → frame/prior-art comparison → minimality). Contents absent. |
| `RC1` | `MISSING_TRANSCRIPT_EVIDENCE` | `RECOVERED_PARTIALLY` | Contract text absent. Turn 15 verdict recovered: not safe to hash/freeze. Six blockers recovered by name: instance-class quantification, undefined interpretation grammar, RCCD-driven lexical exclusion, dialogue-derived `c0` calibration, `S11`/`C3` mismatch, frame leakage. |
| `RC2` | `MISSING_TRANSCRIPT_EVIDENCE` | `RECOVERED_PARTIALLY` | Contract text absent (Turn 16 is a `GAP`). Turn 17 verdict recovered: still not safe to hash. Five required repairs recovered, including the determination invariant `a = a' ⇒ 𝒮_{i,a} = 𝒮_{i,a'}`. Whether they were discharged is unrecoverable (Turns 18–22 `GAP`). |
| `SR-B2` | `MISSING_TRANSCRIPT_EVIDENCE` | `RECOVERED_PARTIALLY` | v1 judged infeasible and retired; v2 frozen as executable (Turn 26). Neither version's text exists. |
| `NM-v1` | `MISSING_TRANSCRIPT_EVIDENCE` | `RECOVERED_PARTIALLY` | Only that broad `NM-v1` retrieval was retained while `K-P1` was made strict (Turn 27). No definition. |
| `K-P1` | `MISSING_TRANSCRIPT_EVIDENCE` | `RECOVERED_PARTIALLY` | Only that it was made strict (Turn 27). No criterion. |
| `FDI-v1` | `MISSING_TRANSCRIPT_EVIDENCE` | `NOT_RECOVERED` | Only that Turn 32 introduced it into the final-determination/source adjudication machinery for S1. |
| `CDE-v1` | `MISSING_TRANSCRIPT_EVIDENCE` | `NOT_RECOVERED` | Named only in Turn 34 as part of the determination structure used to move S1 to READY. |
| `FDI1`–`FDI5` | `MISSING_TRANSCRIPT_EVIDENCE` | `NOT_RECOVERED` | Named only in Turn 34. No criteria. |
| "Direct instantiation" | `RECONSTRUCTED_RESEARCH_STATE` | `RECOVERED_PARTIALLY` | Turn 23: specialization plus source-internal definitional expansion; excludes new primitive structure and cross-source assembly. |
| Six-query retrieval rule | `RECONSTRUCTED_RESEARCH_STATE` | `RECOVERED_PARTIALLY` | Turn 28: all six queries mandatory, so selective retrieval cannot silently decide an outcome. The six queries themselves are absent. |
| `D1`, `L_→`, `P1`, `P2`, `c0` | `MISSING_TRANSCRIPT_EVIDENCE` | `RECOVERED_PARTIALLY` | Turn 12: `D1` accepted; a small joint fragment `L_→` across LK proof search and CSP propagation survived; `P2` joint interpretation must precede `P1` content testing; joint-profile tuples must be indexed; the `c0` prediction was likely content-empty. No definitions. |
| `S2`, `S7`, `G2`, `G3`, `S11`, `C3` | `MISSING_TRANSCRIPT_EVIDENCE` | `RECOVERED_PARTIALLY` | Named in the Turn 15 and Turn 17 audits with their required repairs. No defining text. |
| RCCD demotion | `RECONSTRUCTED_RESEARCH_STATE` | `RECOVERED_PARTIALLY` | Turn 13: RCCD demoted to historical taxonomy/reference point, not a premise or privileged target answer. |
| Miller (LK proof search source) | — | `NOT_RECOVERED` | Cited in Turn 33 ("1000 choices", "proofs are formless"). The source artifact is not in the repository and no eligible-source record exists. |
| Turns 1, 6–11, 14, 16, 18–22, 24 | `MISSING_TRANSCRIPT_EVIDENCE` | `NOT_RECOVERED` | Explicit `GAP` markers. Absence of a recorded turn is **not** evidence that the turn did not occur. |

## Consequence

The Presenting FAR line has **no recoverable frozen protocol and no recoverable
frozen source corpus**. Concretely:

1. No successor target after `S1` can be identified, because the successor
   queue lives inside `T1`–`T8`.
2. No blind first pass can be executed for any Presenting FAR target, because
   `𝔈₀` defines the eligible evidence both lanes must receive and it is absent.
3. No adjudication can be run under the historical protocol, because `CDE-v1`
   and `FDI1`–`FDI5` are absent.

This is a `SOURCE_REQUIRED` boundary, not a theoretical stalemate. The missing
artifacts exist outside this repository — in the original ChatGPT project
conversation — and recovering them is an evidence-supply step, not research.

## What is nevertheless established

The Turn 33 correction is recovered exactly and is load-bearing:

- absence of a canonical deterministic LK search strategy does **not** imply
  absence of a completely determined transition relation;
- nondeterminism is compatible with a fully specified transition relation;
- intra-sequent and frontier representation are distinct analytical levels;
- `DI3` is withdrawn and must never be re-run;
- the strongest surviving negative source claim is the weakened one.

`S1` is recorded as `READY_UNDER_INTERNAL_PROTOCOL` and is **not** authorized
for restart. That disposition is internal to the Presenting FAR protocol. It is
not Project FAR Acceptance and carries no canonical authority.
