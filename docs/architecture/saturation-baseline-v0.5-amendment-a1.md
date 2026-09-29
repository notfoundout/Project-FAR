# Saturation Baseline v0.5 — Amendment A1

Status: Research / Provisional
Campaign: `SATURATION-FALSIFICATION-001`
Applies to: `docs/architecture/saturation-baseline-v0.5.md`
Base reviewed: `8618384efe4576580f65ff67b02b22bac43ffc51`

This amendment does not add a capability class and does not claim global saturation. It records the smallest specification and assurance-boundary repairs required by the bounded falsification campaign.

## Result

The capability-class inventory in v0.5 survives the seven tested findings. The stronger claim that v0.5 required no assurance/specification change does not survive. The findings therefore do not justify v0.6, but they do require the following explicit obligations.

### SF001-R1 — Independent evidentiary observation

For a consequential claim about an actor's externally observable execution, the actor's own record is not sufficient by itself to establish evidentiary status when the actor controls that record. Tamper evidence over a self-authored record authenticates that record; it does not establish omitted external events. Evidentiary status requires an observation path outside the audited actor's unilateral control or independent corroboration appropriate to the contract.

This is an assurance-boundary requirement, not a general rule that every proposition needs multiple sources.

### SF001-R2 — Composition assurance

Assurance of components in isolation does not entail assurance of their consequential composition. When outputs, privileges, state, instructions, or effects cross component/skill/agent boundaries, the relevant execution path or composition must itself be within the assurance scope. Component-level passes cannot be promoted into a composition-level pass without that check.

### SF001-R3 — Verified state admission

`proposed`, `validated`, and `admitted` are distinct states. A consequential generated proposal must not silently become canonical accepted state merely because validation metadata exists or a validator is scheduled. Admission requires the contractually required successful validation event. Rejected or unresolved proposals may remain in history with their non-admitted status preserved.

### SF001-R4 — Synthesis fidelity

Synthesis is a consequential transformation. Unless a new derivation is independently validated, a synthesized output must not increase support strength, widen scope, erase material disagreement, delete counterevidence, remove relevant uncertainty or abstention, manufacture consensus, or convert conditionals into unconditional conclusions relative to the admitted upstream state.

### SF001-R5 — Detection versus origin attribution

`detected_at` and `origin_attributed_to` are distinct. The first point where a defect becomes observable is not automatically its causal or correctable origin. Origin attribution must remain challengeable and must retain the evidence or intervention supporting the attribution. When origin is unknown, FAR must preserve that uncertainty rather than substituting the detection point.

### SF001-R6 — Availability, realization, and validity

Evaluation must not collapse:

1. availability/coverage — whether an adequate candidate or decisive evidence was present;
2. realization/selection — whether the system actually selected or produced the adequate result; and
3. validity/support — whether the selected result's support survives the applicable validation.

A success on one dimension cannot stand in for success on another.

### SF001-R7 — Checker trust-base qualification

A formal-validation record must retain enough information to identify the checker/toolchain and version used, together with known material trust-base limitations relevant to the claimed assurance. Discovery that a checker version is within the range of a soundness defect creates a limitation to investigate; it does not by itself establish that any specific checked theorem is false or that the exploit path was exercised.

## Interaction with v0.5 hard invariants

A1 makes consequences of existing v0.5 principles enforceable rather than adding a new ontology:

- `SF001-R1` strengthens the operational meaning of "FAR gets no epistemic privilege" and provenance/meta-assurance.
- `SF001-R2` makes inspectability and challengeability apply to consequential compositions, not just nodes considered separately.
- `SF001-R3` prevents certainty/status laundering during updating.
- `SF001-R4` applies epistemic conservation to rendering and synthesis.
- `SF001-R5` prevents distinct causal/diagnostic dimensions from being collapsed.
- `SF001-R6` prevents distinct evaluation dimensions from being collapsed.
- `SF001-R7` makes formal assurance retain its trusted-computing-base context.

## Change-control verdict

Under v0.5's own change-control logic, this campaign establishes changes at the specification/assurance-boundary level but does not establish a new first-class capability class or a required new extension interface. `NEW_CAPABILITY_CLASS_REQUIRED` is therefore not supported by this campaign.

## Nonclaims

This amendment does not change FAR-CORE, FARA's governed theorem, W1-W6 results, EFR status, #518 status, novelty/independence status, or commercial-readiness status. It does not establish that these seven findings exhaust future saturation attacks. It does not certify Lean 4.19.0 as unaffected by the disclosed kernel defect and does not claim any FAR theorem was invalidated by it.