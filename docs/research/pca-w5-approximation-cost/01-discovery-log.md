# PCA-W5 Stage-A Discovery Log

Status: **COMPLETE — NO FAR MAPPING PERFORMED**

Query freeze commit: `11a93ba0db812ec849aac9b136be5d5538a0b44e`

Stage-B freeze time: `2026-08-30T18:16:49Z`

## Protocol integrity

The external search began only after the 18-query protocol was committed.

One execution error occurred: the first Acumen/Talarion call paraphrased `W5-Q-DE-01` rather than using the frozen text verbatim. That run is **inadmissible** and is retained only as a protocol/tool failure. Acumen was rerun with the exact frozen query; the exact rerun was also off-target and supplied no W5 evidence.

No Project FAR mapping was performed during Stage A.

## Frozen-query execution matrix

| Tool | Frozen queries executed | Disposition |
|---|---|---|
| Consensus | `W5-Q-DE-01`, `W5-Q-IT-01`, `W5-Q-BM-01`, `W5-Q-SL-01`, `W5-Q-MO-01`, `W5-Q-RC-01` | Discovery/triage only |
| SciSpace | `W5-Q-DE-02`, `W5-Q-IT-02`, `W5-Q-BM-02`, `W5-Q-SL-02`, `W5-Q-MO-02`, `W5-Q-RC-02` | Independent discovery/triage |
| Scite | `W5-Q-DE-03`, `W5-Q-IT-03`, `W5-Q-BM-03`, `W5-Q-SL-03`, `W5-Q-MO-03`, `W5-Q-RC-03` | Literature/citation-context discovery |
| Acumen/Talarion | exact `W5-Q-DE-01` after one quarantined paraphrased call | Failed/off-target lane |
| Primary-source web | source-specific follow-up only after frozen-query discovery | Identity and authoritative-page verification |
| Zotero | attempted capability route | Blocked in this runtime |
| Wolfram | none | Correctly deferred until Stage D |

All 18 preregistered native queries were exercised before source selection.

## Tool-lane observations

### Acumen/Talarion

Both runs returned largely unrelated current items rather than Le Cam/decision-experiment literature. The paraphrased first run is protocol-invalid. The exact rerun is valid as a search attempt but failed relevance. Neither contributes evidence.

### Consensus

The six assigned queries recovered relevant literature across:
- Le Cam/statistical-experiment comparison;
- rate–distortion;
- approximate system/bisimulation metrics;
- surrogate/excess-risk calibration;
- multiobjective/Pareto optimization;
- computational/statistical resource tradeoffs.

Consensus search output was used for recall only. Where a paper was selected, its identity and role were independently checked through author, publisher, repository, DOI, or other authoritative pages.

### SciSpace

The six assigned queries independently recovered:
- Le Cam deficiency/randomization literature;
- information bottleneck;
- probabilistic-system abstraction/simulation;
- task-aware/excess-risk representation literature;
- partial-order/Pareto optimization;
- MDL/description-complexity literature.

The lane was useful as an independent vocabulary and source-recall check.

### Scite

The six assigned queries recovered or contextualized:
- Blackwell/Le Cam and excess-risk literature;
- rate–distortion under declared distortion functions;
- model-reduction error bounds;
- target/surrogate risk relations;
- scalarization/preference dependence;
- statistical/computational tradeoffs.

A later Scite full-text request failed because Article Galaxy MCP access is not enabled. No unavailable text was inferred.

### Zotero

The installed Zotero skill documents a local-Desktop/helper workflow. In this chat runtime there is no Zotero tool namespace and no executable helper was exposed by a local helper-path probe. Therefore:
- no Zotero library was read;
- no source was imported into Zotero;
- no Zotero BibTeX export occurred;
- `references.bib` in this workstream is repository-managed, not Zotero-managed.

This is a retained environment limitation, not evidence failure.

## Selected-source verification

The Stage-B source manifest selects primary or authoritative sources only where their identities could be independently verified. Discovery summaries, citation counts, and tool-generated labels are not used as theorem proof.

Selected source families:

1. Statistical experiments / decision risk:
   - Le Cam (1964), *Sufficiency and Approximate Sufficiency*.
   - Blackwell (1953), *Equivalent Comparisons of Experiments*.
   - Torgersen (1991), *Comparison of Statistical Experiments*.
   - Mariucci (2016) only as an accessible expository cross-check.

2. Information theory:
   - Shannon (1959), *Coding Theorems for a Discrete Source With a Fidelity Criterion*.
   - Tishby, Pereira, and Bialek (1999), *The Information Bottleneck Method*.

3. Behavioral/model abstraction:
   - Girard and Pappas (2007), *Approximation Metrics for Discrete and Continuous Systems*.

4. Statistical learning:
   - Bartlett, Jordan, and McAuliffe (2006), *Convexity, Classification, and Risk Bounds*.

5. Multiobjective optimization:
   - Miettinen (1999), *Nonlinear Multiobjective Optimization*.
   - Miettinen and Mäkelä (2002), *On scalarizing functions in multiobjective optimization*.

6. Resource/cost:
   - Chandrasekaran and Jordan (2013), *Computational and Statistical Tradeoffs via Convex Relaxation*.
   - Hansen and Yu (2001), *Model Selection and the Principle of Minimum Description Length*.

## Rejected or quarantined material

- Recent 2026 “Le Cam + representation learning” preprints were not needed to establish foundational semantics and were not promoted into the native foundation.
- Recent applied rate–distortion, semantic-communication, LLM-loss, and benchmark papers were retained only as recall signals where appropriate.
- Generic surveys were not selected when a primary or authoritative source was available.
- Search failure or absence of a located framework is not novelty evidence.

## Stage-A conclusion

The native literatures do **not** present one obvious universal approximation/cost object. They use materially different structures:
- deficiency and bounded-loss risk over randomized procedures;
- probability-weighted distortion plus a tolerated distortion level;
- pseudometrics over metric transition systems;
- calibrated relationships between surrogate and target risk;
- Pareto/efficient order plus preference-dependent scalarization;
- separate computational, statistical, and description-complexity resources.

That observation is frozen as a literature result only. It is not yet a Project FAR architecture claim.
