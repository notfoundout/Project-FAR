# Saturation Baseline v0.5 — Amendment A1

Status: Research / Provisional
Campaign: `SATURATION-FALSIFICATION-001`
Applies to: `docs/architecture/saturation-baseline-v0.5.md`
Base reviewed: `8618384efe4576580f65ff67b02b22bac43ffc51`

This amendment does not add a capability class and does not claim global saturation. It records only the specification and assurance-boundary deltas that survived hostile review against the literal frozen v0.5 text.

## Result

Seven findings were tested. Two—synthesis/provenance fidelity and coverage/realization/validity separation—were already explicitly required by v0.5 and are therefore `REPRESENTABLE_NO_CHANGE`. Five findings expose narrower obligations that were not explicit enough in the frozen baseline. None requires a new first-class capability class or v0.6.

### SF001-R1 — Independent evidentiary observation

For a consequential claim about an actor's externally observable execution, the actor's own record is not sufficient by itself to establish evidentiary status when the actor unilaterally controls the sole record. Tamper evidence over a self-authored record authenticates that record; it does not establish omitted external events. Evidentiary status requires an observation path outside the audited actor's unilateral control or independent corroboration appropriate to the contract.

This is an assurance-boundary requirement, not a general rule that every proposition needs multiple sources.

### SF001-R2 — Composition assurance

Assurance of components in isolation does not entail assurance of their consequential composition. When outputs, privileges, state, instructions, or effects cross component/skill/agent boundaries, the relevant execution path or composition must itself be within the assurance scope. Component-level passes cannot be promoted into a composition-level pass without that check.

### SF001-R3 — Validated reliance-state promotion

This rule does not redefine FARA's term "admitted for consideration." Candidate admission for consideration remains governed by FARA.

For a consequential generated proposal, proposal creation, validation outcome, and promotion into authoritative or reliance-bearing state are distinct events. A proposal must not silently become authoritative accepted state merely because validation metadata exists or a validator is scheduled. Promotion into authoritative or reliance-bearing state requires the contractually required successful validation event. Rejected or unresolved proposals may remain in history with their non-authoritative status preserved.

### SF001-R4 — Detection versus origin attribution

`detected_at` and `origin_attributed_to` are distinct. The first point where a defect becomes observable is not automatically its causal or correctable origin. An origin claim must remain challengeable and retain the evidence or intervention supporting that attribution. When origin is unknown, FAR must preserve that uncertainty rather than substituting the detection point.

### SF001-R5 — Checker trust-base qualification

v0.5 already requires consequential transformations to retain method/version and validation state, and its audit package includes model/protocol versions and validation records. This repair adds only the missing qualification obligation: when a known material checker/toolchain limitation is relevant to a formal-assurance claim, the limitation must remain attached to that claim or its assurance record.

Discovery that a checker version is within the range of a soundness defect creates a limitation to investigate; it does not by itself establish that any specific checked theorem is false or that the exploit path was exercised.

## Findings requiring no amendment

### Synthesis / provenance fidelity — `REPRESENTABLE_NO_CHANGE`

Frozen v0.5 already requires synthesis to preserve qualifications, scope, uncertainty, disagreement, supporting and contradicting evidence, unresolved alternatives, source lineage, and status-time boundaries. It also states that a summary must not strengthen a claim beyond the underlying graph, while the implementation completion contract requires uncertainty and abstention to survive end to end. The tested fabricated-consensus cases therefore do not establish a new specification repair.

### Coverage / realization / validity — `REPRESENTABLE_NO_CHANGE`

Frozen v0.5 already makes evaluation stage-specific, separately enumerates retrieval/high-recall coverage, evidence-support/contradiction accuracy, and adjudication accuracy, and its hard invariants prohibit collapsing distinct epistemic dimensions. The tested CRV cases therefore reinforce an existing requirement rather than establishing a new one.

## Interaction with v0.5 hard invariants

- `SF001-R1` sharpens the assurance boundary around provenance and meta-assurance for self-authored execution records.
- `SF001-R2` makes inspectability and challengeability apply to consequential compositions, not just components considered separately.
- `SF001-R3` prevents validation-status laundering during authoritative state promotion without changing FARA candidate admission.
- `SF001-R4` prevents detection location from being silently promoted into a causal/origin claim.
- `SF001-R5` preserves material trusted-computing-base limitations alongside the checker identity/version already required by v0.5.

## Change-control verdict

Under v0.5's own change-control logic, this campaign establishes two assurance-boundary changes and three specification repairs. It also establishes two `REPRESENTABLE_NO_CHANGE` findings. No tested finding establishes a missing first-class capability class or required extension interface. `NEW_CAPABILITY_CLASS_REQUIRED` and v0.6 are therefore not supported by this campaign.

## Nonclaims

This amendment does not change FAR-CORE, FARA's governed theorem, W1-W6 results, EFR status, #518 status, novelty/independence status, external-validity status, or commercial-readiness status. It does not establish that these seven findings exhaust future saturation attacks. It does not certify Lean 4.19.0 as unaffected by issue #14576 and does not claim any FAR theorem was invalidated by it.
