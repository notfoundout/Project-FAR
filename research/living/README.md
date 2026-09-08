# Project FAR living repository

Status: **Research infrastructure; never theory or evidence authority**

Research candidate only. Discovery or triage does not establish support, dispute, novelty, priority, external validity, utility, independence, theorem status, EFR result, or any other Project FAR claim/evidence disposition.

`FAR-LIVING-RESEARCH-001` and `FAR-LIVING-REPOSITORY-001` make the repository continuously self-reconciling without giving automation authority to manufacture scientific acceptance.

## What runs unattended

Every 30 minutes the scheduled workflow:

1. reads current protected `main` as governance authority;
2. searches newly indexed Crossref metadata against governed FAR research questions;
3. advances a deterministic historical backfill through older publication windows;
4. runs the same historical query/window through OpenAlex as a second scholarly index;
5. periodically performs a low-volume Open Library book search for historical philosophical, metaphysical, and logic sources that may not have DOI metadata;
6. applies deterministic signal and mathematical-bridge gates;
7. deduplicates across providers by normalized DOI when possible;
8. maps candidates to exact governed research questions and any FAR-CORE identifiers explicitly present in those questions/dependencies;
9. records source failures rather than treating them as empty evidence;
10. reconciles canonical claim, assurance, research-question, limitation, open-problem, dependency, and program surfaces by content hash;
11. derives the FAR-CORE dependency/reverse-impact graph from the canonical assurance ledger;
12. builds a non-authoritative core-claim review queue for high-attention candidates;
13. updates generated living-research and living-repository status pages;
14. validates the result before writing only to `automation/living-research-inbox`;
15. refreshes one permanent draft rolling PR. It never writes directly to protected `main` and the rolling inbox PR is never the promotion PR.

## Execution boundary

The scheduled job builds its working tree from protected `main` and carries only accumulated *data* (`inbox/`, `runs/`, `state-v1.0.json`, `repository-state-v1.0.json`) across from `automation/living-research-inbox`. Tools and configuration always come from `main`. The job never checks out and executes code from the inbox branch, which is not protected; doing so would let anyone able to push there run code under a write-scoped token on a schedule.

The branch is rebuilt as a single commit on current `main` each run, so the rolling PR stays a readable one-commit diff and cannot conflict with its own base.

## Permanent rolling PR

Steady-state operation uses one permanent draft PR for `automation/living-research-inbox`. `research/living/inbox/.rolling-pr-anchor.json` exists on that branch solely so the PR remains non-empty immediately after canonical snapshot promotion. The anchor is not a candidate or evidence item and must never be copied into a promotion snapshot.

Because the PR already exists, the scheduled `GITHUB_TOKEN` only refreshes it. No repository-wide permission to let GitHub Actions create or approve pull requests is required, and no privileged administrator token is required.

The permanent inbox PR must not be merged or closed during normal operation. If it disappears, the writer preserves research data on the branch and the governance step must fail closed until a human bootstraps one replacement permanent PR. Broadening automation authority is not the recovery path.

## Snapshot promotion

When reviewed Research-only state should enter canonical `main`, create a separate snapshot branch from current protected `main`, copy only the reviewed living-research state, explicitly exclude `.rolling-pr-anchor.json`, and open a normal promotion PR. That PR must pass the normal protected validation and `merge-authority` path. The permanent inbox PR remains open throughout.

Merging a Research-only snapshot does not itself establish support, dispute, novelty, external validity, utility, independence, theorem status, or EFR results.

## Attention terms are derived, never accumulated

Each provider's attention-term matches are stored on that provider's source entry and replaced whenever the provider is seen again; `triage.attention_terms` is recomputed as the union of those, filtered to the currently configured terms. A term removed from `attention_terms` in the configuration therefore clears on the next sighting instead of marking a candidate high-attention forever.

## Run-report validation

`tools/check_living_research.py` validates the newest 500 run reports. Reports are immutable and are validated when written, so every automatic path uses that bound; the full historical scan is `--all-runs`, reachable on demand through the workflow's `audit` dispatch mode. The `validate` mode dispatched after each unattended update stays bounded, because it runs as often as discovery does.

## PR-status boundary

Updates pushed by `GITHUB_TOKEN` do not manufacture protected PR status checks. Each unattended update dispatches bounded validation against the branch head for content assurance, but that dispatch is not a substitute for `merge-authority` and cannot make the permanent inbox canonical. Snapshot promotion uses a separate human-authored PR head so ordinary protected checks attach to the exact promoted bytes.

## Historical, philosophical, and metaphysical coverage

Historical backfill starts at the present and walks backward in ten-year publication windows to 1600. The query set covers sufficiency/statistics, quotient minimization, automata/Myhill-Nerode, bisimulation/coalgebra, abstract interpretation, Blackwell/decision theory, invariance, scientific representation, underdetermination, measurement theory, formal identity, grounding/dependence, formal ontology, logic/semantics, probability/decision, and formal language.

Philosophy and metaphysics are not admitted merely because they mention a broad theme. Lenses that could otherwise become unconstrained require an explicit bridge to formal or mathematical content such as logic, identity, relation, structure, equivalence, model, semantics, modality, order, category, algebra, measurement, probability, decision, or information.

Open Library is intentionally low-volume and used only for historical book discovery. It is not treated as a bulk scholarly backend or as evidence authority.

## Claim-change behavior

The living repository **can detect that a core claim may need to change** and calculate the downstream FAR-CORE claims that depend on it. A metadata result never constitutes a contradiction.

Canonical correction path:

`candidate → source verification → exact claim reconstruction → attack → replication → acceptance → promotion proposal → protected merge`

A reproducible contradiction satisfying the exact canonical premises may trigger the smallest affected reopening/correction path. The old claim remains recoverable through Git history.

The automation may enter only `DISCOVERED` by itself. Every later scientific lifecycle stage is governed. EFR remains separate and externally executed.

## Files

- `config-v1.0.json` — sources, governed questions, lenses, backfill, and triage.
- `state-v1.0.json` — incremental and historical cursors.
- `lifecycle-v1.0.json` — scientific stage-transition boundary.
- `repository-surfaces-v1.0.json` — canonical surfaces monitored for drift.
- `repository-state-v1.0.json` — generated reconciliation/impact state.
- `inbox/candidates/` — deduplicated source candidates.
- `runs/` — per-run query/result/rejection/failure provenance.
- `../../docs/research/living-research-status.md` — discovery status.
- `../../docs/research/living-repository-status.md` — repository reconciliation status.

## Commands

```bash
python tools/run_living_research.py
python tools/reconcile_living_repo.py
python tools/check_living_research.py
python -m unittest tests.test_living_research tests.test_living_research_workflow -v
```
