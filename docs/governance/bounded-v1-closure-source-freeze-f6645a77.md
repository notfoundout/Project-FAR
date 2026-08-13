# Bounded-v1 Internal Closure Campaign — Source Freeze

Status: **Administrative freeze record.** Not a theory freeze, not a canonical definition change, not a new research result.

## Purpose

Records the common frozen source baseline for the bounded-v1 internal closure campaign: three blind first-pass lanes (Claude Lane A, Codex Lane B, GPT Lane C) each independently analyze the identical frozen repository state before any exchange of findings across lanes.

This document is itself an administrative freeze-record artifact. Creating it is not part of, and does not alter, the frozen source it describes, and it does not constitute a theory, canonical-definition, or governance change under `CLAUDE.md` / `AGENTS.md`.

## Governing standard

This freeze is made under [`docs/governance/evidence-replication-and-freeze-standard-v1.0.md`](evidence-replication-and-freeze-standard-v1.0.md). Per that standard:

- This source freeze itself confers no substantive result classification. Each artifact resulting from this campaign must receive exactly one primary evidence class according to what it actually establishes under the standard's evidence classes — **Exploratory**, **Confirmatory**, **Implementation**, **Replication**, **Boundary**, **Counterexample**, or **Unresolved** — as warranted by that artifact's own execution, not predicted in advance by this record.
- **Confirmatory** may not be assigned retrospectively and is not conferred merely by this source freeze.
- Lane isolation does not itself confer any replication layer. **Replication** may be assigned to a resulting artifact only if its execution independently satisfies the exact requirements of the specific replication layer (R1–R5) it claims.
- The three internal model-assisted lanes alone do not constitute R3 independent technical replication, R4 adversarial conceptual replication, R5 cross-context replication, or independent validation — nor does blindness between lanes, by itself, make any output independent validation.
- The more conservative classification controls until a dispute over evidence class, replication layer, or materiality is resolved (per the standard's Governance section).

## Frozen source baseline

| Field | Value |
|---|---|
| Frozen source commit (SHA-1) | `f6645a77f3b0af0b12897fa9bc2c329cdb345261` |
| Frozen root tree (SHA-1) | `a870c1213873158d288ba40bad3952c465e5acab` |
| Freeze date | 2026-08-13 |
| Repository | `notfoundout/Project-FAR` |
| Provenance | `origin/main` tip immediately after merge of PR #449 ("vendor `far-*` governance skills into the repository") |
| Repository state at freeze | Clean working tree; no uncommitted or untracked changes present when the freeze was recorded |

## Content-digest verification

The frozen source is a Git commit. Git's own content-addressed SHA-1 commit and tree hashes already constitute a deterministic, recursive digest over every file, path, and byte in the frozen tree. No supplementary file-by-file digest is required or produced by this record. Verification is exact and reproducible with:

```
git rev-parse f6645a77f3b0af0b12897fa9bc2c329cdb345261         # must print the commit SHA above
git rev-parse f6645a77f3b0af0b12897fa9bc2c329cdb345261^{tree}  # must print the tree SHA above
git diff --stat f6645a77f3b0af0b12897fa9bc2c329cdb345261 <candidate>   # empty output iff <candidate> is content-identical
```

Any content difference anywhere in the frozen tree, down to a single byte, changes the tree SHA and is therefore mechanically detectable. This record's own digests were recomputed directly from `f6645a77f3b0af0b12897fa9bc2c329cdb345261`, not from the administrative commit that adds this file.

## Protected package identity

Mapping the freeze standard's theory-freeze fields onto this source freeze:

- **Theory version / central result** — as declared by `docs/project-status.md` at the frozen commit: current phase `POST-TERM-EVAL-001` (Post-Terminal Public Evaluation Program v1.0); central result is the registered Universal Proof Program `POST-TUE-UPP-001`, terminal adjudication `strictly_weakened_relative_rccd_universality_theorem_proved_with_complete_dependency_audit_and_open_world_boundary`; framework status FARA/FAR/FARO/FARE/FARM recorded there as `Stable` (FARA/FAR/FARO/FARM) and `Frozen and requirement-driven` (FARE).
- **Vocabulary semantics** — [`docs/glossary/canonical-terminology.md`](../glossary/canonical-terminology.md) as it exists at the frozen commit. This file carries no independent semantic-version tag in the frozen source; its content is fixed and verifiable only via the frozen tree SHA above.
- **Definitions and admissibility rules** — [`theory/definitions/definitions.md`](../../theory/definitions/definitions.md) and [`frameworks/FARA/admissibility-structure.md`](../../frameworks/FARA/admissibility-structure.md) as they exist at the frozen commit; authoritative content is fixed by the frozen tree SHA, not restated here.
- **Compiler / verifier contracts** — none gate this campaign specifically. The frozen source's existing proof-object and dependency-registry mechanization (`theory/proof-objects/`, `theory/dependencies/dependency-registry.yaml`) is included as ordinary frozen content but is not itself an enforcement contract for this campaign.
- **Freeze commit** — `f6645a77f3b0af0b12897fa9bc2c329cdb345261`.
- **Freeze date** — 2026-08-13.
- **Authorized errata policy** — see Errata rule below.

The exact task, question, or artifact subset assigned to each lane is defined separately, at each lane's kickoff, by whoever authorizes that lane's execution. This record fixes only the common *source* all three lanes must analyze; it does not define, narrow, or authorize any lane's analytical scope, and it does not itself begin Lane A, Lane B, or Lane C.

## Prior verification referenced

PR #449 skill-environment verification, performed in this session immediately before this freeze: **PASS, 13/13** repository-scoped `far-*` skills discovered in a fresh session after removal of account-scoped copies (`far-canonical-source-resolver`, `far-claim-registry`, `far-contradiction-detector`, `far-counterexample-hunter`, `far-discovery-engine`, `far-embedding-tester`, `far-evidence-ledger`, `far-formalizer`, `far-prior-art-adversary`, `far-project-state-manager`, `far-research-orchestrator`, `far-research-quality-gate`, `far-theory-auditor`).

## Participating blind lanes

- Claude Lane A
- Codex Lane B
- GPT Lane C

## Isolation rule

No lane may receive, read, or be conditioned on another lane's findings, outputs, or intermediate reasoning before that lane completes and files its own first-pass report against this frozen source.

## Administrative-commit rule

Any commit created solely to record this freeze — including the commit that adds this document — is an **administrative freeze-record commit**. It is not part of, and never replaces, the frozen source analyzed by the three lanes. The frozen source that Claude Lane A, Codex Lane B, and GPT Lane C each analyze remains exactly `f6645a77f3b0af0b12897fa9bc2c329cdb345261` / tree `a870c1213873158d288ba40bad3952c465e5acab`, regardless of any later commit on this or any other branch.

## Material-change rule

Any material change to theory, theorem scope or premises, canonical definitions, relevant governance, or mechanization occurring after first-pass execution begins produces a new candidate baseline. It does not retroactively alter, invalidate, or improve findings already obtained against this frozen source. A materially changed baseline requires its own freeze record under this same standard; it does not amend this one.

## Errata rule

Errors discovered against this frozen source remain attributable to this source version (`f6645a77f3b0af0b12897fa9bc2c329cdb345261`) permanently. Repairing such an error requires an explicitly identified successor baseline (a new frozen commit with its own freeze record); it does not retroactively repair or reclassify findings recorded against this frozen source. This follows the freeze standard's Failure preservation rule: a failed or erroneous result under this frozen source keeps its original classification, and a later successful repair does not overwrite it.

## Evidence qualifier

This freeze enables **bounded internal model-assisted evaluation** of the frozen source by three model-assisted lanes. This source freeze alone does not establish, predict, or restrict which primary evidence class (per `docs/governance/evidence-replication-and-freeze-standard-v1.0.md`) any resulting artifact will receive; that classification is determined solely by what each artifact's own execution actually establishes, and may include Exploratory, Confirmatory, Implementation, Replication, Boundary, Counterexample, or Unresolved as warranted. This freeze alone does not confer independent validation, or any replication layer beyond what a given execution separately and independently satisfies. Findings from this campaign must not be described as independent validation, R3 independent technical replication, R4 adversarial conceptual replication, or R5 cross-context replication merely because the three lanes were blind to one another.

## Scope of this record

This record is itself an administrative freeze-record artifact. It:

- does not modify, reclassify, or reinterpret any frozen historical evidence, manifest, or canonical artifact;
- does not open, begin, or authorize Lane A, Lane B, or Lane C execution;
- does not change `main`, any theory content, Lean/mechanization content, or ADR-002;
- does not assert independent validation, any replication layer, or any claim promotion beyond what is stated above.

---

Freeze status: **SOURCE FROZEN — `f6645a77f3b0af0b12897fa9bc2c329cdb345261`**
