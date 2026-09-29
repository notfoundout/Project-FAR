# SATURATION-FALSIFICATION-001

Status: Research / Provisional reconstruction
Base: `8618384efe4576580f65ff67b02b22bac43ffc51`

This campaign reconstructs the interrupted SATURATION-FALSIFICATION-001 run from the surviving transcript and the canonical repository. It is not a byte-for-byte recovery of the unpushed local commit `f3bd22de`.

## Question

Can Saturation Baseline v0.5 represent **and enforce** the decision-relevant distinctions introduced by the selected recent findings without changing a first-class capability class, invariant, assurance boundary, or extension interface?

Broad category fit is not sufficient. A finding counts as absorbed only when the frozen architecture can preserve the relevant identity, semantics, uncertainty, provenance, dependency, validation behavior, and decision-relevant counterfactuals without laundering them through generic metadata or an opaque validator.

## Corrected dispositions

| Finding | Disposition | Minimal consequence |
|---|---|---|
| Hearsay / independent evidentiary observation | `ASSURANCE_BOUNDARY_CHANGE` | A self-authored execution record cannot alone establish evidentiary status when the audited actor unilaterally controls the sole record. |
| SkillCascade / cross-skill composition | `ASSURANCE_BOUNDARY_CHANGE` | Assurance must cover consequential compositions, not only components in isolation. |
| Verification before reliance-state promotion | `SPECIFICATION_REPAIR` | A consequential proposal cannot enter authoritative/reliance-bearing state before the contractually required successful validation event. |
| Synthesis / provenance fidelity | `REPRESENTABLE_NO_CHANGE` | v0.5 already preserves disagreement, uncertainty, contradicting evidence, alternatives, source lineage, and forbids synthesis from strengthening underlying claims. |
| Who&When Pro / failure-origin localization | `SPECIFICATION_REPAIR` | `detected_at` and `origin_attributed_to` are distinct; origin attribution requires challengeable evidence or intervention support. |
| CRV coverage / realization / validity | `REPRESENTABLE_NO_CHANGE` | v0.5 already makes evaluation stage-specific and separates coverage, evidence-support accuracy, and adjudication accuracy. |
| Lean kernel trust-base finding | `SPECIFICATION_REPAIR` | v0.5 already requires checker method/version; A1 adds retention of known material checker/toolchain limitations relevant to the assurance claim. |

No finding in this campaign requires a new first-class capability class. Therefore this campaign does **not** justify v0.6.

## Result

The capability-class inventory survives these seven attacks. The strong no-change reading still fails, but for a narrower reason than the first reconstruction claimed: five findings require explicit assurance/specification deltas, while two are already absorbed by the literal v0.5 baseline.

This is a bounded result. It does not establish that v0.5 is globally saturated, that these seven findings exhaust the search space, or that the repaired architecture is minimal.

## Review corrections incorporated

The hostile review found that the first reconstruction overstated three items:

1. the synthesis fixtures were already rejected by v0.5 and are now `REPRESENTABLE_NO_CHANGE`;
2. the CRV fixtures were already separated by v0.5 and are now `REPRESENTABLE_NO_CHANGE`;
3. checker identity/version was already required by v0.5, so the Lean negative case now isolates omission of a **known material limitation** while retaining checker identity/version.

It also removed the false zero-match Lean scan, disambiguated reliance-state promotion from FARA candidate admission, froze paper sources to exact arXiv `v1` identities, and replaced heading-only fixture checks with structured executable predicates.

## Nonclaims

- No FAR-CORE claim, premise, theorem, W1-W6 result, independence status, novelty status, external-validity status, or commercial-readiness status changes.
- FARA primitive/minimality questions remain separate.
- EFR and #518 remain unexecuted by this campaign.
- The Lean finding does not establish that any governed FAR proof is invalid.
- No customer utility or competitive moat is demonstrated.

## Artifacts

- `findings-v1.0.json` — source-bound disposition record plus frozen source manifest.
- `counterexamples-v1.0.json` — 25 bounded attack/control fixtures with structured facts.
- `replication.md` — reconstruction, source-freeze, and verification record.
- `docs/architecture/saturation-baseline-v0.5-amendment-a1.md` — provisional five-rule amendment.
- `tests/test_saturation_falsification_001.py` — structural checks plus executable baseline/amendment fixture semantics.

## Acceptance rule

This reconstruction is candidate material until the exact branch head passes the repository's required protected validation. Green CI is necessary but not sufficient for scientific acceptance; an independent review should still reconstruct each source-to-disposition inference.
