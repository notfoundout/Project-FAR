# R5 cross-context replication package

**Program ID:** `R5-CROSS-CONTEXT-001`
**Status:** `PROTOCOL FROZEN / EVIDENCE NOT YET COLLECTED`
**Package version:** `1.1`
**Evidence base (target pinned here):** `3ba4986b86b6e211d9e01e78018ef8324297f86c`
**Protocol initial commit:** `5d482a9c4cb760e3af6f2bcccff2e0461a971a9b`
See `preregistration-v1.0.json#provenance_sha_model` for each field's meaning and the self-reference limitation.

Nothing has been executed. No participant exists. No result is registered. This directory contains a protocol and the means to check it, and nothing else.

---

## What this tests

`LIM-031` records the dominant evidence deficit: no party outside the programme has ever chosen or evaluated a preservation contract for the universality question. `USD-W6` established that one agent cannot manufacture the missing independence, terminating at `internal_robustness_only`. No internally authored bridge can close it.

This package specifies an elicitation under which an uncontaminated party encounters the underlying problem without the programme's terminology, architecture, examples, target formulation, preferred answer, comparison dimensions, or historical conclusions — and answers it in their own vocabulary before seeing any of them.

---

## Execution order

Steps are ordered. None may be reordered, merged, or skipped.

| # | Step | Artifact | Role |
|---|---|---|---|
| 0 | Confirm authorisation to execute. **This package does not carry it.** | — | — |
| 1 | Run the package verifier; require `PASS` | `verify_r5_package.py` | executor |
| 2 | Select respondent; record the tier they qualify for | `evidence-tier-rules-v1.0.json` | executor |
| 3 | Complete the delivery checklist | `freeze-procedure-v1.0.md` §2 | deliverer |
| 4 | Deliver §2–§3 verbatim, nothing else | `elicitation-packet-A-v1.0.md` | → Role A |
| 5 | Role A answers; declares final | — | Role A |
| 6 | Preserve byte-for-byte, timestamp, SHA-256 | `freeze-procedure-v1.0.md` §3 | executor |
| 7 | Transcribe into the schema without interpreting | `role-a-output-schema-v1.0.json` | executor |
| 8 | Administer contamination questionnaire; assign level | `contamination-questionnaire-v1.0.json` | executor |
| 9 | *Optional:* architecture phase; separately frozen and hashed | schema, `optional_architecture_phase` | Role A |
| 10 | **Reveal gate.** Release programme material to Role B only | `reveal-packet-v1.0.md` | Role B |
| 11 | Map, both directions, preserving failures | `normalization-mapping-schema-v1.0.json` | Role B |
| 12 | Adjudicate against the frozen registry | `adjudication-procedure-v1.0.md`, `outcome-registry-v1.0.json` | Role C |
| 13 | Record the run manifest | `freeze-procedure-v1.0.md` §4 | executor |

Controls `B1` and `B2` follow the same path. Under this package's frozen campaign policy each arm is a **single descriptive pilot run**; any A/B difference is compatible with both a packet effect and a respondent effect, and **no causal framing claim is permitted**.

---

## Artifacts

| File | Purpose |
|---|---|
| `README.md` | This file; execution order |
| `preregistration-v1.0.json` | Frozen question reference, outcome space, falsification and strengthening conditions, prohibited inferences, stopping rule |
| `elicitation-packet-A-v1.0.md` | Blinded primary packet |
| `elicitation-packet-B1-reword-v1.1.md` | Semantic-preserving reword; surface-form sensitivity |
| `elicitation-packet-B2-ablation-v1.1.md` | Decomposition ablation; tests whether the A–I axes shape the answer |
| `participant-surface-v1.1.json` | The complete participant-facing surface `S1`–`S7` |
| `target-pin-v1.1.json` | **RESTRICTED.** Target pinned to the evidence-base commit with per-file hashes |
| `contamination-questionnaire-v1.0.json` | Twelve items, six levels, descriptive-vs-independence two-value model |
| `role-a-output-schema-v1.0.json` | Structured transcription; `unsettled` is valid |
| `freeze-procedure-v1.0.md` | Roles, delivery checklist, freeze-before-reveal, manifest fields, execution controls |
| `reveal-packet-v1.0.md` | **RESTRICTED.** Release gate and Role B prohibitions |
| `normalization-mapping-schema-v1.0.json` | Mapping fields, both directions, failed mappings, mapper declarations |
| `adjudication-procedure-v1.0.md` | Primary comparison, neutral relations, anti-reconstruction scale, outcome assignment |
| `outcome-registry-v1.0.json` | `O1`–`O12` with per-outcome evidence requirements |
| `evidence-tier-rules-v1.0.json` | `T1`–`T5`, each with an explicit `cannot_establish` list; class `X1` recorded as **not** an execution tier; `LIM-031` closure analysis |
| `provenance-manifest-v1.0.json` | Hashes and consumed dispositions |
| `package-audit-v1.0.md` | Adversarial audit, negative control, clean-room read, residual risk |
| `verify_r5_package.py` | **RESTRICTED.** Mechanical blinding, structure, and state check |

### Restricted artifacts

`reveal-packet-v1.0.md` and `verify_r5_package.py` must never reach Role A. The verifier names the banned terms in order to detect them; showing it to a respondent would disclose the entire watchlist.

---

## Stopping rule

The package is complete when another investigator can execute it without making any new methodological decision that could materially affect the result. If the executor must decide what the question means, what counts as contamination, when to reveal, how to freeze, how to compare, how to score, or which outcomes count — it is **not** frozen. Each of those is fixed in the artifacts above.

**`T5` and the stopping rule.** `T5` means an independent organization preregistering **faithful execution of this protocol** — procedural and organizational independence with no methodological alteration. Seven administrative additions are permitted and nine alterations create a new protocol version instead. Independently designing a *different* protocol is class `X1`, which is **not** an execution tier of this package.

---

## What this package cannot do

It cannot establish that R5 is obtainable, only that it is specified. It cannot close `LIM-031`, and it cannot address `LIM-032` at all. Its blinding claim is **lexical only**: no registered watchlist term occurs in the mechanically checked participant-facing text. That is not proof of no semantic leakage; the clean-room read is a separate, non-mechanical judgement. It cannot make a single positive run establish universality. It cannot supply a comparison relation over formulations — none is established, and the withdrawn seven-dimension rubric is explicitly not reused. It cannot remove the residual structural hint in the A–I decomposition, which `package-audit-v1.0.md` §3 discloses as a known limitation of the instrument.

---

## File and hash model

**18 tracked files = 17 frozen payload artifacts + 1 verifier (tooling); 17 of them hashed.** Earlier revisions said "fourteen artifacts" ambiguously: `REQUIRED_ARTIFACTS` excluded the verifier while the manifest excluded *itself*, so the two counts named **different sets**.

- The manifest hashes a **declared list**, never a directory scan. A directory scan would silently admit stray files such as `__pycache__` contents into the freeze.
- The manifest cannot hash itself — writing the hash would change the bytes being hashed — so it is excluded from its own list and its integrity is checked via git. That is why 17 files are hashed, not 18.
- The verifier **is** hashed by the manifest, so tooling drift is detectable, but it is not a payload artifact.

## Separate adversarial review gate

Before any evidence-critical protocol here is merged or executed:

1. the author declares the package complete;
2. a **logically separate adversarial review pass** occurs, in a fresh context or by a separate reviewer;
3. every finding is resolved;
4. the full semantic sweep reruns;
5. only then may merge-readiness be declared.

**This is a process-quality gate, not an epistemic independence claim.** A same-model fresh-context review is *not* independent evidence and must never be reported as such.

**Why it exists:** across two review rounds, multiple substantive defects survived author self-audit, and **two defects were introduced by the repairs themselves** — an outcome list overcorrected to 6:0 negative, and a blinding verifier that passed vacuously. Single-pass self-audit is demonstrably unreliable for this package.
