# Governed FAR research corpus

Status: **Research infrastructure and generated Research synthesis; not Accepted theory or promotion authority**

This directory is the permanent interoperability layer between the existing living-research inbox, governed repository artifacts, and a reproducible current synthesis. It does not replace the living discovery, lifecycle, dependency, review, promotion, or implementation machinery.

The chain is:

`content-addressed sources → atomic findings → deduplicated mechanisms → scoped conclusions → current frontier`

`corpus-v1.0.json` declares source-bound observations and conclusion rules, not synthesis results. The reconciler objectively inventories governed research paths, current living candidates, frozen external receipts, and exact PR snapshots; an unclassified material path fails validation. It then normalizes and deduplicates atomic findings, derives mechanism support, hashes every conclusion's transitive dependencies, and builds the frontier. Every available repository source is bound to exact bytes and its Git version; unavailable input is represented explicitly rather than reconstructed. `synthesis-v1.0.json` and `docs/research/current-research-frontier.md` are deterministic views. Run:

```bash
python tools/reconcile_research_corpus.py --write  # intentional regeneration
python tools/reconcile_research_corpus.py          # fail on stale or invalid state
```

## Safe external and scheduled-task intake

Freeze any externally obtained file without executing or interpreting it:

```bash
python tools/reconcile_research_corpus.py --ingest FILE --origin scheduled_task
```

The command copies exact bytes to `external/<sha256>.bin`, writes a receipt identifying the bytes as a discovery lead with `primary_evidence_verified: false`, and immediately refreshes `research/living/corpus-reconciliation-v1.0.json`. It never adds a finding, executes content, or promotes status. A curator may register it only after independently verifying the underlying primary evidence and applying existing review/promotion governance. A summary or AI output cannot support an EVIDENCE finding. Missing historical output stays `missing`; it is never fabricated.

The unattended living-research runner refreshes the same reconciliation after every discovery run. Its workflow then regenerates the synthesis/frontier using protected-main code and commits those Research-only views to the permanent inbox branch. Candidate metadata remains an untrusted lead until governed review verifies primary evidence.

## Invalidation and governance

`make research-check` recomputes the inventory, canonical corpus hash, dependency hashes, and both views. A source mutation, withdrawal, correction, contradiction, missing dependency, duplicate identity/mechanism, cycle, unsupported EVIDENCE label, stale view, unclassified material input, or incomplete material-input accounting fails closed. Withdrawal/correction removes affected support and automatically makes dependent conclusions and frontier entries unresolved unless other active source-bound support remains.

Architecture comparison uses the fixed six-way vocabulary requested by the corpus schema. It compares mechanisms literally against current FAR/Saturation surfaces; aliases do not create mechanisms, absent edges do not imply independence, and repetition does not strengthen evidence.

Automation has no scientific promotion authority. Any correction to Project FAR still requires the existing Question → Execution → Observation → Discovery → Replication → Acceptance → Promotion → Repository Change path and the protected living promotion/implementation controls.
