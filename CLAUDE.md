# Project FAR — Claude Code Instructions

Operational guidance only. This file does not establish or change Project FAR theory, evidence, governance, status, or authority.

@AGENTS.md

## Authority

Before substantive work, read `docs/governance/research-execution-charter.md`.

For current project state, do not rely on memory or old status text. Start with:
- `README.md`
- `docs/project-status.md`
- `docs/CANONICAL_MAP.md`
- `docs/glossary/canonical-terminology.md`
- `docs/governance/framework-boundaries.md`
- `docs/governance/claim-status-matrix.md`
- `docs/governance/limitations-register.md`
- `docs/governance/open-problems-register.md`

Read only additional authoritative material relevant to the task. If authorities conflict, surface the conflict; do not silently choose or rewrite it away.

## 1. Think Before Changing

Before editing:
1. identify the requested outcome;
2. identify authoritative files and affected dependencies;
3. inspect existing implementation, tests, and conventions;
4. state material assumptions or ambiguity;
5. choose the smallest sufficient change;
6. define verifiable success criteria.

If evidence is insufficient, return `Unknown` or competing hypotheses rather than guessing. Prefer the simpler correct approach.

## 2. Simplicity First

Make the minimum complete change. Do not add speculative features, unnecessary abstractions, duplicate concepts, unrequested configurability, or new dependencies without demonstrated need.

Reuse existing mechanisms before creating new ones. Minimality never permits deleting unique information; preserve or archive it according to governance.

## 3. Surgical Changes

Every changed line must trace to the requested task or to a defect directly caused by that task.

Do not:
- refactor unrelated code;
- rewrite adjacent prose for style;
- reformat unrelated files;
- casually rename concepts;
- remove pre-existing dead code unless requested;
- alter frozen evidence or historical records for cosmetic consistency.

Match repository conventions. Remove only orphaned material created by your own change. Report unrelated defects separately instead of silently expanding scope.

## 4. Epistemic Discipline

Preserve `Accepted`, `Research`, `Provisional`, `Archive`, and `Unknown`.

Never promote a claim, theorem, primitive, dependency, methodology, experiment result, or framework status beyond its explicit evidence and authority.

Never convert:
- hypothesis → established result;
- bounded result → universal claim;
- observation → proof;
- methodological choice → derived theorem;
- framework stability → theoretical truth;
- successful software execution → proof of upstream theory;
- repository placement → epistemic authority.

Preserve scope restrictions, assurance levels, limitations, nonclaims, failed gates, and unresolved questions. Failure, falsification, and `Unknown` are valid outcomes.

## 5. Dependency Integrity

Canonical theory direction:

`foundations → shared theory → FARA → FAR → FARO`

Do not introduce circular or reverse justification. Downstream methodology, evidence, examples, papers, software, commercial material, and archive records do not prove upstream premises merely because they use them.

Do not infer additional dependencies from names alone; resolve them from current canonical governance. For upstream changes, check materially affected downstream references.

## 6. Research Discipline

Research precedes implementation when the task is a research question.

Do not start a new experiment merely because it is technically possible. First verify current requirements for registration/preregistration, frozen inputs, acceptance criteria, provenance, replication, claim boundaries, and evidence preservation.

Never modify frozen evidence to obtain a desired result. Never label internal replication as independent external validation unless an authoritative record establishes that status.

## 7. Goal-Driven Execution

Convert the task into explicit pass/fail conditions:
- bug fix: reproduce failure → fix → reproducer passes;
- refactor: establish behavior before → change → verify after;
- documentation: identify authority → change affected surfaces → semantic/link checks;
- theory: identify authority/dependencies → preserve claim boundaries → relevant research/semantic checks.

For multi-step work: change → verify → inspect → correct → repeat. Do not declare success from inspection alone when executable verification exists.

## 8. Verification

Use the narrowest relevant checks first, then broader checks when the change can affect wider guarantees.

Available commands include:
- `make docs-check`
- `make links-check`
- `make semantic-check`
- `make research-check`
- `make health-fast`
- `make health`
- `make test-fast`
- `make test`
- `make validate-changed`
- `make validate-full`

Before completion:
- inspect `git diff`;
- run `git diff --check`;
- run all task-relevant checks;
- investigate failures rather than rerunning blindly;
- confirm no unrelated files changed.

Never weaken, delete, skip, or rewrite a failing check merely to make the suite pass unless that check itself is the verified defect. If a required check cannot run, report the exact blocker and what remains unverified.

## 9. Canonical, Generated, and Historical Files

Determine a file's authority/status before editing it. Change authoritative sources rather than manually patching generated output. Regenerate derived artifacts with existing tooling when applicable.

Archive is historical evidence, not current authority, unless a current authoritative artifact explicitly incorporates it. Never create a second canonical location for the same concept.

## 10. Git and PR Discipline

Do not commit, push, open a PR, merge, force-push, or rewrite history unless the user authorizes that action.

When authorized:
- keep the branch and diff task-scoped;
- inspect the full diff before commit;
- report exact checks and results;
- preserve unresolved issues as unresolved;
- never merge to the default branch without explicit authorization.

PR descriptions must state what changed, why, evidence, verification, unresolved items, and claim/status impact.

## 11. Security and Reproducibility

Never expose or commit secrets. Do not bypass permissions, integrity checks, provenance controls, or reproducibility requirements.

Do not add network access, dependencies, external services, or nondeterminism unless required and justified. Prefer deterministic, replayable, auditable procedures.

## 12. Completion Standard

Complete means:
- requested outcome implemented;
- change is minimal and internally consistent;
- relevant authority/dependencies checked;
- relevant tests/checks pass or exact failures are reported;
- no unrelated diff remains;
- no unsupported claim promotion occurred;
- remaining uncertainty is labeled.

Final report: files changed; substantive result; checks and results; unresolved/`Unknown`; claim/status impact.
