# R5 cross-context replication package

**Program ID:** `R5-CROSS-CONTEXT-001`
**Status:** `PROTOCOL FROZEN / EVIDENCE NOT YET COLLECTED`
**Repository base:** `3ba4986b86b6e211d9e01e78018ef8324297f86c`

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

The mutation packet `elicitation-packet-B-mutation-v1.0.md` follows the same path with a **different respondent** for cross-respondent comparison. Same respondent yields a within-respondent framing check only.

---

## Artifacts

| File | Purpose |
|---|---|
| `README.md` | This file; execution order |
| `preregistration-v1.0.json` | Frozen question reference, outcome space, falsification and strengthening conditions, prohibited inferences, stopping rule |
| `elicitation-packet-A-v1.0.md` | Blinded primary packet |
| `elicitation-packet-B-mutation-v1.0.md` | Alternative wording; prompt-sensitivity control |
| `contamination-questionnaire-v1.0.json` | Twelve items, six levels, asymmetry rule |
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

It cannot establish that R5 is obtainable, only that it is specified. It cannot close `LIM-031`: a faithful external execution supplies an externally authored answer but not an externally chosen question. It cannot make a single positive run establish universality. It cannot supply a comparison relation over formulations — none is established, and the withdrawn seven-dimension rubric is explicitly not reused. It cannot remove the residual structural hint in the A–I decomposition, which `package-audit-v1.0.md` §3 discloses as a known limitation of the instrument.
