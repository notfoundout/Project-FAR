# dialogue-theory — an independent, non-FAR research record

**This directory is not a Project FAR artifact and carries no Project FAR authority.**

It records the autonomous closure of an independent theory/research programme constructed in a
supplied Claude↔GPT dialogue. Its object is *not* Project FAR, FARA, FARO, RCCD, or repository
completion. Repository governance controls file mutation here; it does not establish or
withhold authority over the mathematical content, and nothing in this directory establishes,
changes, or evidences any Project FAR theory, claim, status, or boundary.

Repository status and dialogue-theory status are kept strictly separate. Repository placement
is not epistemic authority.

## Terminal state

**BLOCKED** (hard blocker: no scholarly document host is reachable from this environment), with
all unblocked work completed and four proved retrieval-independent results.

Start with [`TERMINAL-REPORT.md`](TERMINAL-REPORT.md).

## Files

| File | Contents |
|---|---|
| [`PROTOCOL.md`](PROTOCOL.md) | The frozen experiment $\mathfrak{E}_0$, **recovered** from the verified transcripts with line-level locators. Not redesigned. |
| [`PROTOCOL-SUCCESSOR.md`](PROTOCOL-SUCCESSOR.md) | Separately versioned successor procedures, and the replacements considered and **rejected**, with reasons. |
| [`S6-PREREGISTRATION.md`](S6-PREREGISTRATION.md) | S6 retrieval parameters, fixed before any S6 search ran. |
| [`EVIDENCE.json`](EVIDENCE.json) | Corpus hash verification, target manifest, the executed SR-B2 v2 record for S6 and S7, near-match sets, and the findings ledger. |
| [`PROOFS.md`](PROOFS.md) | Theorems T1–T4 with proofs and countermodels, blocked obligations, and the hostile closure audit. |
| [`DIALOGUE-THEORY.md`](DIALOGUE-THEORY.md) | The extracted theory: **Branching-Internalisation Adequacy (BIA)**, with its scope, non-claims, and falsifiers. |
| [`TERMINAL-REPORT.md`](TERMINAL-REPORT.md) | Terminal classification, results, refutations, scope, unresolved items, and the minimal unblock action. |
| [`STATE.json`](STATE.json) / [`CHECKPOINT.md`](CHECKPOINT.md) | Machine-readable and compact resume state. |
| [`FAR-COMPARISON.md`](FAR-COMPARISON.md) | Written **last**. Relational classification only: partial overlap on one narrow question, otherwise independent. |

## Evidentiary discipline used throughout

- All three transcript SHA-256 hashes were verified against the supplied manifest before use.
- **Turn 36 is absent from the supplied corpus.** Its content is used only as the closure
  prompt's non-verbatim summary, labelled `RESUME-SUMMARY`. No Turn 36 text was reconstructed
  or quoted.
- No source content is asserted from training recall. Where a passage was returned by a search
  invocation but its host could not be inspected, it is marked **attribution unverified** and
  is never used to ground a positive or negative certificate.
- The frozen run's own defect (Turn 17's incorrect S6 determination check) is **preserved as
  observed**, not repaired.
- `OPEN` never counts as `NO`; novelty is never returned positive on an uncertified
  translation; failure, falsification, and `Unknown` are recorded as outcomes.
