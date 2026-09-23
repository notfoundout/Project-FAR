# FAR Saturation Baseline v0.4 — Delta Investigation

Status: Accepted for bounded promotion  
Investigation ID: FAR-SAT-v0.4  
Baseline repository ref: `4e258fd3b7c5a80b6f7263ad6f2e085f913b1d2a`

## Question

Which capability classes discovered during the saturation harvest are objectively required but not already representable by canonical Project FAR contracts?

## Execution

The live repository was searched against the v0.4 capability inventory. Existing canonical artifacts were treated as controlling. Candidate additions were eliminated when an existing FAR primitive already represented the requirement.

The audit explicitly checked:

- `schemas/far-knowledge-graph-v1.schema.json`
- `schemas/far-intake-v1.schema.json`
- `schemas/far-evidence-adjudication-v1.schema.json`
- `frameworks/FAR/workflow.md`
- `methodology/research-doctrine.md`
- `docs/governance/research-execution-charter.md`
- `far_validation/`
- `tests/`

## Observations

Existing FAR already represents claim/evidence/argument graphs, assumptions, rebuttal/undercut relations, interpretation changes, typed source restrictions, saturation rounds, search stopping rules, exclusions, parameter provenance, post-freeze outcomes, contradiction handling, and an explicit `Unknown`/`unresolved` boundary.

The following candidate features therefore failed necessity and are not promoted as new primitives:

- translation provenance: reducible to interpretation + derivation/provenance;
- generic search stopping: already present in intake;
- generic meta-assurance graph vocabulary: reducible to existing claim/argument/evidence graph;
- generic contradiction representation: already present;
- generic evidence uncertainty: already present in bounded claim/evidence states;
- forecast and prospective-commitment objects: not yet required by an active FAR execution.

Four gaps survived reduction:

1. **Source dependence lineage.** Existing evidence/source objects do not require representing copying, syndication, common origin, or an independence key. Apparent source count can therefore overstate independent corroboration.
2. **Bitemporal state.** Existing records do not require separating when a proposition/evidence state is valid in the world from when FAR learned or recorded that state.
3. **Explicit abstention.** Existing `unresolved` adjudication is a human/policy disposition over a comparison. It does not encode a verifier's deliberate refusal to adjudicate, its reason, or the assurance boundary that caused it.
4. **Audit self-assurance profile.** Existing graph primitives can represent an assurance argument, but no contract requires a completed FAR audit to state whether source integrity, interpretation fidelity, search coverage, evidence adjudication, inference adjudication, reproducibility, unresolved defeaters, and hostile-source isolation were actually checked.

A cross-cutting security requirement also survived reduction: **source content must be treated as untrusted data, never as control instructions**.

## Discovery

For general-purpose evidence and argument verification, the four surviving gaps and hostile-source boundary are necessary to preserve FAR's existing invariants:

- no manufactured certainty;
- no collapse of source count into source independence;
- no collapse of historical truth-state into current knowledge-state;
- no forced adjudication when prerequisites are inadequate;
- no epistemic privilege for FAR's own output;
- no control authority granted to evidence under review.

## Falsifiability

This result is falsified if an existing canonical FAR contract can represent each surviving requirement without loss of the distinctions above and without relying on unstructured metadata.

## Promotion Boundary

This investigation authorizes only composable assurance contracts and validators for the surviving gaps. It does not redesign FARA/FARO, change accepted theory, or make claims about external-world truth.
