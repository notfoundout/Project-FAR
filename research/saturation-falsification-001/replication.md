# SATURATION-FALSIFICATION-001 replication record

Status: Research / Provisional reconstruction

## Reconstruction boundary

The original Ultracode session committed an unpushed local head `f3bd22de` and stopped while exact-head validation was running. That object was never pushed to GitHub and is unavailable to this session. This record reconstructs the campaign from the surviving transcript and canonical `main` at `8618384efe4576580f65ff67b02b22bac43ffc51`; it does not claim byte identity with the lost local head.

## Canonical baseline

The reviewed artifact is `docs/architecture/saturation-baseline-v0.5.md` at Git blob `9d398e01f915e4f368dee44d35e9bd98de5b82ff`.

The test is not whether a finding can be filed under a broad capability bucket. The test is whether the literal frozen baseline already has typed, non-opaque representation plus an enforcement/validation hook for the decision-relevant distinction.

## Final scientific result

All seven attacks are `REPRESENTABLE_NO_CHANGE`.

This reverses the intermediate five-rule Amendment A1 reconstruction. Hostile review showed that the intermediate campaign repeatedly confused “not named in the new paper's vocabulary” with “not representable/enforceable by v0.5.”

### Hearsay

v0.5 already has `SOURCE_LINEAGE`, `SOURCE_DEPENDENCE`, `ATTESTATION`, `PROVENANCE_RECORD`, typed evidence independence, `INDEPENDENCE_LIMITED`, and explicit evidence requirements. These surfaces can distinguish an actor-authored record from independent observation/corroboration and can make independence consequential to evidence sufficiency or assurance.

The paper remains useful as an implementation adversary: tamper evidence over an actor-owned record is not independent observation. That lesson does not require an architecture amendment.

### SkillCascade

v0.5 already has `DEPENDS_ON` / `DERIVED_FROM`, requires every consequential transformation to retain validation state, makes consequential relationships challengeable, and requires validator contracts for consequential transitions in the implementation completion contract.

The relevant inference is bounded: a consequential composition/path can be represented as its own dependency-bearing transformation or relation and therefore need not inherit a component's validation result. SkillCascade motivates composition-level adversarial tests in implementations that support such paths; it does not establish a missing first-class architecture primitive.

### Verification before reliance

v0.5 already defines fail-closed reliance states and allows `EXTERNAL_RELIANCE_READY` only through a recorded transition that validates every applicable assurance capability and binds the resulting assurance case to the exact adjudication version. The tested proposal/validation/reliance distinction is therefore already explicit.

### Synthesis

v0.5 already requires synthesis to preserve qualifications, scope, uncertainty, disagreement, supporting and contradicting evidence, unresolved alternatives, source lineage, and status-time boundaries. It forbids summaries from strengthening claims beyond the underlying graph.

### Failure origin

v0.5 already treats `CAUSES` as a challengeable consequential relation with provenance and validation state and sends causal claims through a specialized gate. A detection event can therefore remain separate from a causal/origin attribution without a new schema rule.

### Coverage / realization / validity

v0.5 already makes evaluation stage-specific and separately enumerates retrieval/high-recall coverage, evidence-support/contradiction accuracy, and adjudication accuracy/calibration. The tested dimensions are already non-collapsible.

### Lean trust base

v0.5 already requires method/version and validation state for consequential transformations; forbids downstream assurance beyond inherited uncertainty; applies the same discipline to FAR's formal outputs; and requires assurance cases to expose unresolved defeaters and limitations with evidence/validation links.

Issue #14576, the 4.32.2 release notes, and the postmortem establish a relevant Lean soundness defect and fix context. FAR's pin predates 4.32.2. This campaign does not establish that any governed FAR proof exercised the exploit path or is invalid.

The earlier reconstruction's raw zero-match grep claim was false and remains deleted.

## Mutable-source receipts

`source-receipts-v1.0.json` freezes the exact decisive excerpts used from the three mutable Lean web sources and records SHA-256 over the exact UTF-8 excerpt bytes. This is a bounded reproducibility receipt, not a full mirror of the external pages.

## Counterexample method

`counterexamples-v1.0.json` retains 25 attack/control scenarios, but it no longer simulates a fictional global `baseline_accepts` policy. Each scenario instead names the literal baseline anchors that already carry the distinction and records the bounded disposition `REPRESENTABLE_NO_CHANGE`.

The regression test verifies that:
1. all seven findings retain that bounded disposition;
2. Amendment A1 is present only as a `WITHDRAWN / NON-OPERATIVE` tombstone and contains no rule identifiers;
3. every cited baseline anchor literally exists in the baseline artifact;
4. every fixture is covered by anchors registered for its finding;
5. the mutable-source receipt hashes recompute exactly;
6. no v0.6, FAR-CORE, FARA, EFR, or empirical-status promotion is made.

These checks make accidental reintroduction of the disproven A1 story fail loudly. They do not turn the research interpretation into a theorem.

## Implementation boundary

Architecture absorption is not implementation completeness.

The existing subagent execution architecture already content-addresses tasks, binds reports to inputs, verifies runtime isolation declarations, preserves support/contradiction conflicts, and fails closed on several routing/provenance defects. This campaign does not claim that it already contains a dedicated SkillCascade-style composition adversary or an external observation substrate for every execution path.

Those are implementation-assurance questions to test under the applicable implementation/governance scope; their absence does not retroactively create a missing v0.5 architecture class or invariant.

## Bounded conclusion

- seven findings: `7/7 REPRESENTABLE_NO_CHANGE`;
- capability-class inventory: survives these seven attacks;
- bounded no-change hypothesis: survives these seven attacks;
- global saturation: not established;
- Amendment A1: `WITHDRAWN / NON-OPERATIVE`; no operative rules survive;
- v0.6: not justified;
- FARA minimality: not adjudicated here;
- EFR/#518: not executed;
- external utility: not tested.

## Validation boundary

The reconstruction must be judged on the exact pushed branch head by the repository's protected validation. CI success is necessary but is not independent scientific replication.
