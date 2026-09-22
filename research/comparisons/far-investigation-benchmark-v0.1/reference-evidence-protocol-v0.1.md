# FAR Investigation Benchmark — Reference Evidence Protocol v0.1

Status: PREPARED / must be frozen before condition execution

## Purpose

Construct a bounded comparison set for evidence coverage without treating the panel as an omniscient gold standard.

## Firewall and chronology

Reference-evidence researchers receive the case prompt, frozen source cutoff, and frozen search configuration but no condition prompts beyond the shared case prompt and no condition outputs. The complete reference set, item-validity decisions, and M2 denominator for every final case are locked **before any condition run begins**.

Reference-evidence construction therefore occurs in S0. S1 cannot begin until the reference-evidence manifest for all 60 final cases is hashed into the campaign freeze.

## Search procedure

For each provisional case, researchers execute the same frozen search budget:

1. one exact/near-exact claim query;
2. two neutral concept/entity queries;
3. one query targeting evidence consistent with the claim;
4. one query targeting evidence inconsistent with or limiting the claim;
5. backward/forward citation or source-chain traversal from the highest-authority responsive sources, up to the frozen tool-call budget.

Queries must not presuppose a verdict. Search logs, exact query strings, retrieval ranks, provider/tool identity, and access timestamps are retained.

## Source cutoff

An evidence item is admissible only when the proposition-bearing source version existed on or before the frozen source cutoff. A living page materially changed after the cutoff is inadmissible unless the panel can bind an archived, versioned, or otherwise reproducible snapshot that existed by the cutoff. Publication date alone does not establish admissibility when the relevant page contents are mutable.

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

The panel stops when both conditions hold: (a) the frozen search budget is exhausted or all query/source-chain steps are completed, and (b) the final two permitted search steps add no new material evidence item. If the budget ends before saturation, mark the reference set `BOUNDED-NONSATURATED`.

No reference set is described as complete. Every set is a bounded search product.

## Panel procedure

Two researchers independently nominate evidence items and proposition links. A third resolves disagreements over inclusion, materiality, polarity, proposition linkage, and item validity. All validity decisions and the final denominator are locked before any condition output exists.

A valid final evidence item must have a stable item ID, reproducible source identity/version, source date or version boundary, access provenance, linked case proposition ID(s), polarity, materiality reason, and panel disposition. The final record preserves all nominations, exclusions, disagreements, resolutions, and retrieval provenance.

## Zero-denominator rule

A final benchmark case must have at least one valid material reference-evidence item. If a provisional selected case yields zero valid material items under the frozen search protocol, the case is ineligible for confirmatory M2 and is replaced **before S1** by the next eligible reserve in the same stratum. The replacement receives the complete reference-evidence procedure. Continue deterministically until the stratum again contains 10 final cases or the campaign becomes `BLOCKED` because its reserve is exhausted.

This replacement rule is procedural, not outcome-based: the panel still does not assign a final claim verdict.

## Frozen output

Before S1, produce:

- one immutable per-case reference-evidence record for each of the 60 final cases;
- `reference-evidence-manifest.json` binding every final case ID to its per-case record SHA-256 and positive denominator;
- the complete search log and panel dispositions required by the freeze contract.

After S1 begins, an item cannot be deleted, invalidated, merged, split, reweighted, or newly added for confirmatory M2. A newly discovered reference-set defect is recorded as an integrity deviation and handled under the preregistered missingness/integrity rule.

## M2 scoring boundary

A condition recovers an item only when its visible output or recorded source-to-claim structure identifies the same material evidence and connects it to the proposition, inference, alternative, or uncertainty boundary for which the frozen panel marked it material. Merely citing the same source somewhere in the output does not count.

The reference panel does not assign the benchmark's final claim verdict.
