# Governed FAR research corpus

Status: **Research infrastructure and generated Research synthesis; not Accepted theory or promotion authority**

This directory is the permanent interoperability layer between the existing living-research inbox, governed repository artifacts, and a reproducible current synthesis. It does not replace the living discovery, lifecycle, dependency, review, promotion, or implementation machinery.

The chain is:

`content-addressed sources → atomic findings → deduplicated mechanisms → scoped conclusions → current frontier`

`corpus-v1.0.json` is curated Research input. Every available repository source is bound to exact bytes and its last Git version; unavailable input is represented explicitly rather than reconstructed. `synthesis-v1.0.json` and `docs/research/current-research-frontier.md` are deterministic views. Run:

```bash
python tools/reconcile_research_corpus.py --write  # intentional regeneration
python tools/reconcile_research_corpus.py          # fail on stale or invalid state
```

## Safe external and scheduled-task intake

Freeze any externally obtained file without executing or interpreting it:

```bash
python tools/reconcile_research_corpus.py --ingest FILE --origin scheduled_task
```

The command copies exact bytes to `external/<sha256>.bin` and writes a receipt identifying the bytes as a discovery lead with `primary_evidence_verified: false`. It never adds a finding, executes content, or promotes status. A curator may register it only after independently verifying the underlying primary evidence and applying existing review/promotion governance. A summary or AI output cannot support an EVIDENCE finding. Missing historical output stays `missing`; it is never fabricated.

## Invalidation and governance

`make research-check` recomputes the canonical corpus hash and both views. A source mutation, withdrawal, missing dependency, duplicate identity, cycle, unsupported EVIDENCE label, stale view, or incomplete material-input accounting fails closed. Source withdrawal must be recorded as such and all dependent findings reclassified or removed; changing the source record invalidates the derived hash.

Architecture comparison uses the fixed six-way vocabulary requested by the corpus schema. It compares mechanisms literally against current FAR/Saturation surfaces; aliases do not create mechanisms, absent edges do not imply independence, and repetition does not strengthen evidence.

Automation has no scientific promotion authority. Any correction to Project FAR still requires the existing Question → Execution → Observation → Discovery → Replication → Acceptance → Promotion → Repository Change path and the protected living promotion/implementation controls.
