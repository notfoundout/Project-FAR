# SATURATION-FALSIFICATION-001

Status: Research / Provisional reconstruction
Base: `8618384efe4576580f65ff67b02b22bac43ffc51`

This campaign reconstructs the interrupted SATURATION-FALSIFICATION-001 run from the surviving transcript and the canonical repository. It is not a byte-for-byte recovery of the unpushed local commit `f3bd22de`.

## Question

Can Saturation Baseline v0.5 represent **and enforce** the decision-relevant distinctions introduced by the selected recent findings without changing a first-class capability class, invariant, assurance boundary, or extension interface?

Broad category fit is not sufficient. A finding counts as absorbed only when the current architecture can preserve the relevant identity, semantics, uncertainty, provenance, dependency, validation behavior, and decision-relevant counterfactuals without laundering them through generic metadata or an opaque validator.

## Dispositions

| Finding | Disposition | Minimal consequence |
|---|---|---|
| Hearsay / independent evidentiary observation | `ASSURANCE_BOUNDARY_CHANGE` | An actor's self-authored record cannot alone establish evidentiary status for claims about that actor's externally observable execution. |
| SkillCascade / cross-skill composition | `ASSURANCE_BOUNDARY_CHANGE` | Assurance must cover consequential compositions, not only components in isolation. |
| Verification before state admission | `SPECIFICATION_REPAIR` | Preserve `proposed`, `validated`, and `admitted` as distinct states; validation metadata alone must not silently canonicalize a proposal. |
| Synthesis / provenance fidelity | `SPECIFICATION_REPAIR` | Synthesis may not strengthen support, erase disagreement, or manufacture consensus relative to the accepted epistemic state. |
| Who&When Pro / failure-origin localization | `SPECIFICATION_REPAIR` | `detected_at` and `origin_attributed_to` are distinct; origin attribution requires challengeable evidence. |
| CRV coverage / realization / validity | `SPECIFICATION_REPAIR` | Availability, realization/selection, and validity/support are separate evaluation dimensions. |
| Lean kernel trust-base finding | `SPECIFICATION_REPAIR` | A checked artifact must retain checker identity/version and bounded trusted-computing-base limitations; affected-version membership alone does not invalidate a proof. |

No finding in this campaign requires a new first-class capability class. Therefore this campaign does **not** justify v0.6.

## Result

The strong no-change saturation reading is falsified: current v0.5 does not state all required assurance/specification obligations explicitly enough. The capability-class inventory survives this campaign. Amendment A1 records the narrow repairs without adding a capability row.

This is a bounded result. It does not establish that v0.5 is globally saturated, that these seven findings exhaust the search space, or that the repaired architecture is minimal.

## Nonclaims

- No FAR-CORE claim, premise, theorem, W1-W6 result, independence status, novelty status, external-validity status, or commercial-readiness status changes.
- FARA primitive/minimality questions remain separate.
- EFR and #518 remain unexecuted by this campaign.
- The Lean finding does not establish that any governed FAR proof is invalid.
- No customer utility or competitive moat is demonstrated.

## Artifacts

- `findings-v1.0.json` — source-bound disposition record.
- `counterexamples-v1.0.json` — 25 bounded regression fixtures.
- `replication.md` — reconstruction and verification record.
- `docs/architecture/saturation-baseline-v0.5-amendment-a1.md` — provisional amendment.
- `tests/test_saturation_falsification_001.py` — permanent structural and semantic regression checks.

## Acceptance rule

This reconstruction is candidate material until the exact branch head passes the repository's required protected validation. Green CI is necessary but not sufficient for scientific acceptance; an independent review should still reconstruct each source-to-disposition inference.
