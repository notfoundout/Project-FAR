# USD-W1 Infinite-Carriers Extension Audit

## Scope integrity

- The source class is frozen as `S_inf_eff` before result classification.
- Admission uses effective presentation and preservation commitments, not FARA vocabulary or a desired universal kernel.
- Uncountable and non-effective cases remain explicit exclusions.

## Construction audit

- No new FARA primitive is added.
- Infinite carriers are not materialized as completed finite objects.
- The constructor is uniform across all admitted sources.
- Prefix enumeration, coherence maps, and recovery are counted as derived machinery.
- No case-specific decoder, unrestricted interpreter, or undeclared oracle is permitted.

## Preservation audit

The proof separately checks:

- totality of the uniform constructor over the frozen subclass;
- faithfulness for every finite prefix;
- commuting prefix embeddings;
- transition and admissibility preservation;
- commitment, ground, and dependency preservation;
- historical and revision coherence;
- rejection of finite truncation;
- rejection of oracle smuggling.

## Failure preservation

`INF-BOUNDARY-NONCOMP-001` is not repaired or converted into a favorable case. It remains outside the proved subclass. A later version may investigate it only after freezing any additional assumptions.

## Claim impact

The result resolves one additional `USD-W1-SCOPE-EXT` feature subclass and provides partial progress on `THM-IRD-EXT-001`. It does not resolve the full infinite-carriers family, `S_IRD`, or any universal-structure theorem.

## Terminal classification

`proper_subclass_only`
