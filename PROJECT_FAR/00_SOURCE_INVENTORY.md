# 00 — Source Inventory (Archival Prompt 1 of 5)

**Status:** Archival record. Not authoritative for Project FAR theory, evidence, governance, or status.
**Scope of this prompt:** Turn 0 (framing) and Turns 1–12.
**Date of inventory:** 2026-08-15

---

## HEADLINE FINDING

**[NO SOURCE MATERIAL PRESENT — ENTIRE UPLOAD SET NOT RECOVERABLE]**

Zero source files were located. Every path named in the archival instruction is
absent from this environment, and a filesystem-wide content search for the
expected turn markers returned no matches.

Consequently:

- Step 1 (this inventory) is **complete**, recording total absence.
- Step 2 (`01_TURN_00_FRAMING.md`) is **BLOCKED — not written.**
- Step 3 (`02_TURNS_01-12_GPT.md`) is **BLOCKED — not written.**
- Step 4 (`03_TURNS_01-12_CLAUDE_INFERRED.md`) is **BLOCKED — not written.**

Steps 2–4 require verbatim extraction. With no source text on disk, any content
placed in those files would be fabricated. Per extraction rule 6 ("Absence is a
finding. Write `[NOT RECOVERABLE]` rather than filling a gap") and the Step 1
directive not to reconstruct missing turns, those files are deliberately not
created rather than created as speculative or empty stubs.

---

## PATH RESOLUTION NOTE

The instruction specifies output at `/repo/PROJECT_FAR/`. No `/repo` directory
exists in this environment. The Project FAR repository is checked out at
`/home/user/Project-FAR`, so `/repo/` has been resolved to the repository root
and this file written to `/home/user/Project-FAR/PROJECT_FAR/`.

`[AMBIGUOUS - see conflict report]` — This placement is an inference, not an
instruction. The repository already carries an `archive/` tree
(`archive/superseded/`, `archive/meta-theory/`) which may be the governed
location for historical records. Placement was not silently changed to
`archive/`; the literal instruction path was followed and the question is
flagged here for the operator to rule on.

---

## VERIFICATION LOG (evidence for the absence finding)

All claims below rest on these executed checks, not on assumption.

| # | Check | Result |
|---|---|---|
| 1 | `ls -la /mnt/user-data/uploads/` | `No such file or directory` |
| 2 | `ls -la /mnt/transcripts/` | `No such file or directory` |
| 3 | `ls -la /repo/` | `No such file or directory` |
| 4 | `find / -name 'journal.txt'` (excl. `/proc`, `/sys`) | no matches |
| 5 | `find /mnt -type f` | only `/mnt/skills/**` (Claude skills bundle); `/mnt/user-data/working/` and `/mnt/attach/` contain zero files |
| 6 | `grep -rl -iE 'GPT TURN [0-9]'` over `/mnt /home /root /tmp /var/tmp /opt` | no matches |
| 7 | filesystem-wide `grep -rl -iE` for the framing document's opening line (`You are Claude Opus 5 acting as`) across `*.md`, `*.txt`, `*.json` | no matches |
| 8 | `find . -iname 'PROJECT_FAR*' -o -iname '*SOURCE_INVENTORY*' -o -iname '*TURN_0*'` in repo | no matches (no prior archival output exists) |

Directories `/mnt/user-data/working/` and `/mnt/attach/` exist but are empty.
`/mnt/user-data/uploads/` — the stated source directory — does not exist at all.

---

## FILE → TURN MAPPING

| File | Bytes | Identified turn |
|------|-------|-----------------|
| — | — | **No files present. Mapping is empty.** |

Expected but not found (per KNOWN COVERAGE):

- One framing document whose first line begins `"You are Claude Opus 5 acting as..."` — **[FILE NOT PRESENT — re-upload required]**
- GPT turns 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12 — **[FILE NOT PRESENT — re-upload required]**

Total expected files: 12. Total files located: 0.

---

## COVERAGE OF TURNS 1–35

No turn in the range 1–35 has source coverage.

| Turn | Coverage | Status |
|------|----------|--------|
| 0 (framing) | none | `[FILE NOT PRESENT - re-upload required]` |
| 1 | none | `[FILE NOT PRESENT - re-upload required]` |
| 2 | none | `[FILE NOT PRESENT - re-upload required]` |
| 3 | none | `[FILE NOT PRESENT - re-upload required]` |
| 4 | none | `[FILE NOT PRESENT - re-upload required]` |
| 5 | none | `[FILE NOT PRESENT - re-upload required]` |
| 6 | none | `[FILE NOT PRESENT - re-upload required]` |
| 7 | none | `[FILE NOT PRESENT - re-upload required]` |
| 8 | none | `[ABSENT FROM ALL SOURCES]` (expected absent) |
| 9 | none | `[FILE NOT PRESENT - re-upload required]` |
| 10 | none | `[FILE NOT PRESENT - re-upload required]` |
| 11 | none | `[FILE NOT PRESENT - re-upload required]` |
| 12 | none | `[FILE NOT PRESENT - re-upload required]` |
| 13–35 | none | `[NOT RECOVERABLE]` — outside this prompt's scope **and** no source present |

### Explicitly required markers

- **Turns 1, 2, 6, 12:** `[FILE NOT PRESENT - re-upload required]`. Not
  reconstructed, per instruction.
- **Turn 8:** `[ABSENT FROM ALL SOURCES]`. This absence was expected and is
  therefore **not** evidence of upload failure; it is a property of the record.
- **Claude turns 1–12:** `[CLAUDE HALF NOT PRESENT IN ANY SOURCE]`. Expected
  absent. Because the GPT half is *also* absent, no inference basis exists
  either — see below.

---

## CONSEQUENCE FOR STEP 4 (inferred Claude positions)

`03_TURNS_01-12_CLAUDE_INFERRED.md` was to contain positions inferred from GPT's
replies, each quoting the GPT text the inference rests on. With no GPT text on
disk, there is no quotable basis for any inference. Writing that file would
produce unsourced assertions carrying an `[INFERRED]` label that implies an
evidential basis which does not exist.

**Claude turns 1–12: `[NOT RECOVERABLE]`.**

---

## LAYER SEPARATION

Per extraction rule 2, findings are separated into four layers that items never
move between. For this prompt:

- **(a) FROZEN SHELL** — `[NOT RECOVERABLE]` (no framing document on disk)
- **(b) POST-FREEZE PROCEDURE** — `[NOT RECOVERABLE]` (no turns on disk)
- **(c) FINDINGS** — one finding only: total source absence, evidenced by the
  Verification Log above.
- **(d) STATUSES** — all turns 0–35: no coverage. See coverage table.

No layer-(b) provenance lines are recorded, because no procedural item was
recovered to attribute to a turn.

---

## WHAT IS REQUIRED TO UNBLOCK

1. Re-upload the 12 expected files (framing document + GPT turns 1–7, 9–12) to a
   path readable from this session.
2. Supply `journal.txt` if a catalogued earlier transcript exists; its absence is
   currently unexplained and may itself indicate an incomplete upload.
3. Confirm the intended output root (`PROJECT_FAR/` at repository root vs. the
   existing `archive/` tree).

Prompts 2–5 of this archival sequence cannot produce sourced output until item 1
is satisfied.

---

## NON-CLAIMS

This document asserts nothing about Project FAR theory, prior art, subsumption
outcomes, or claim status. It records only what was and was not found on disk. No
turn content, definition, verdict, counterexample, or concession is reproduced,
summarised, or reconstructed anywhere in this file.
