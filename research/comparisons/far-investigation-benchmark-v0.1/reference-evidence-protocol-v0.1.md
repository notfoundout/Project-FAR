# FAR Investigation Benchmark — Reference Evidence Protocol v0.1

Status: PREPARED / must be frozen before reference-set construction

## Purpose

Construct a bounded comparison set for evidence coverage without treating the panel as an omniscient gold standard.

## Firewall

Reference-evidence researchers receive the case prompt and source cutoff but no condition outputs. The complete reference set for a case is locked before any adjudicator receives outputs for that case.

## Search procedure

For each case, researchers execute the same frozen search budget:

1. one exact/near-exact claim query;
2. two neutral concept/entity queries;
3. one query targeting evidence consistent with the claim;
4. one query targeting evidence inconsistent with or limiting the claim;
5. backward/forward citation or source-chain traversal from the highest-authority responsive sources, up to the frozen tool-call budget.

Queries must not presuppose a verdict. Search logs and retrieval ranks are retained.

## Source hierarchy

Prefer primary records, official datasets, original studies, court/legislative materials, standards, direct transcripts, and contemporaneous records when they directly answer the proposition. High-quality syntheses may identify or contextualize primary evidence. Source authority is proposition-specific; institutional status alone does not make a source dispositive.

## Materiality

An evidence item is material only if adding, removing, or materially changing it could reasonably alter:

- the truth status of an atomic claim;
- the strength of an inference;
- a material alternative explanation;
- the justified uncertainty of the bottom-line conclusion.

Duplicative reports of the same underlying evidence are one evidence item unless independent replication itself is material.

## Saturation and bounds

The panel stops when both conditions hold: (a) the frozen search budget is exhausted or all query/source-chain steps are completed, and (b) the final two permitted search steps add no new material evidence item. If the budget ends before saturation, mark the reference set BOUNDED-NONSATURATED.

No reference set is described as complete. Every set is a bounded search product.

## Panel procedure

Two researchers independently nominate evidence items and proposition links. A third resolves disagreements over inclusion, materiality, and item validity. **All validity decisions and the final denominator are locked before any condition output is revealed to reference researchers or adjudicators.** After output exposure, an item cannot be deleted, invalidated, merged, split, or reweighted; a newly discovered reference-set defect is recorded as an integrity deviation and handled by the benchmark missingness/integrity rule. The final record preserves all nominations, exclusions, reasons, source identifiers, quotations only where copyright permits, dates, proposition links, and retrieval provenance.

## Output

Each item receives a stable ID, source identity, source date, access/retrieval record, proposition IDs, polarity (support / contradict / qualify / contextual), materiality reason, and panel disposition.

The reference panel does not assign the benchmark's final claim verdict.
