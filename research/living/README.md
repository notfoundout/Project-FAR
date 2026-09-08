# Project FAR living research loop

Status: **Research infrastructure; never theory or evidence authority**

`FAR-LIVING-RESEARCH-001` is an unattended discovery inbox. It searches open scholarly metadata on a schedule, binds results to already-governed Project FAR research questions, applies deterministic triage, deduplicates source identities, preserves rejected result identities/reasons and source failures, and maintains a rolling Research-only inbox.

It does **not** execute EFR, establish independence, prove or refute a FAR claim, establish novelty or priority, promote evidence, or change any theorem/assurance/governance disposition. A candidate becomes evidence only through a separate governed review and promotion path.

## Files

- `config-v1.0.json` — operational source/query bindings to governed research questions and epistemic-threat guards.
- `state-v1.0.json` — last completed source cursor and aggregate inbox state.
- `inbox/candidates/` — deduplicated candidate-source records. Filenames derive only from hashed source identity.
- `runs/` — immutable-per-run query/result/rejection/failure provenance.
- `../../docs/research/living-research-status.md` — generated human-readable status view.

## Failure semantics

If any source query fails, the run is `PARTIAL_SOURCE_FAILURE`, the failure is recorded, and the source cursor does **not** advance. Successful query results from that run remain preserved. The next run repeats an overlapping source window and deduplicates already-seen candidates. A source failure is never interpreted as an empty result set.

## Source

The default source is the public Crossref REST API. No paid service or API key is required. If `CROSSREF_MAILTO` is set, the job supplies it to Crossref's polite pool; the automation does not require that variable.

## Run locally

```bash
python tools/run_living_research.py
python -m unittest tests.test_living_research -v
```

The scheduled workflow maintains `automation/living-research-inbox` and one rolling pull request so unattended discovery can continue without direct write authority over protected `main`.
