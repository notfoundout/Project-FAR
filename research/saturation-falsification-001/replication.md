# SATURATION-FALSIFICATION-001 replication record

Status: Research / Provisional reconstruction

## Reconstruction boundary

The original Ultracode session committed an unpushed local head `f3bd22de` and stopped while exact-head validation was running. That object was never pushed to GitHub and is unavailable to this session. This record therefore reconstructs the campaign from the surviving transcript and canonical `main` at `8618384efe4576580f65ff67b02b22bac43ffc51`; it does not claim byte identity with the lost local head.

## Canonical baseline

The reviewed v0.5 artifact is `docs/architecture/saturation-baseline-v0.5.md`. It is Research/Provisional and already distinguishes broad capability classes, epistemic dimensions, provenance, validation, security, evaluation, synthesis, and meta-assurance. The hostile test is not whether each result can be named by one of those buckets, but whether the frozen specification already preserves and enforces the decision-relevant distinction.

The review must therefore allow the result `REPRESENTABLE_NO_CHANGE`. A new paper does not create a FAR delta when the literal frozen baseline already rejects the relevant counterexample.

## Source freeze

`findings-v1.0.json` contains the source manifest used by this reconstruction.

All six arXiv papers are bound to exact `v1` identities rather than versionless abstract URLs, with title, authors, submission timestamp, and retrieval date recorded. The versioned arXiv identity is the immutable paper binding for this campaign.

The mutable Lean sources are frozen by identity and retrieval metadata:

- issue #14576: GitHub issue id `4994570410`, node id `I_kwDOB7kabM8AAAABKbMYqg`, `updated_at=2026-07-28T13:39:10Z`, retrieved 2026-09-29;
- Lean 4.32.2 release notes: version-specific release identity dated 2026-07-28, retrieved 2026-09-29;
- Leonardo de Moura postmortem: dated 2026-08-01 source identity, retrieved 2026-09-29.

A later replication must use these frozen identities or explicitly record a source-version change.

## Counterexample method

The 25 fixtures in `counterexamples-v1.0.json` encode one distinction at a time using structured `facts`, plus expected `baseline_accepts` and `amended_accepts` results.

The permanent regression test does not infer closure from a rule heading. It executes rule-specific predicates over those facts. For `REPRESENTABLE_NO_CHANGE` findings, the baseline and amended predicates are identical and the negative cases are already rejected before A1.

The five actual A1 deltas are:

1. independent evidentiary observation;
2. composition assurance;
3. validated promotion into authoritative/reliance-bearing state;
4. detection versus origin attribution;
5. retention of known material checker/toolchain limitations.

## Frozen-baseline corrections

### Synthesis

v0.5 already requires synthesis to preserve qualifications, scope, uncertainty, disagreement, supporting and contradicting evidence, unresolved alternatives, source lineage, and status-time boundaries. It states that summaries must not strengthen claims beyond the underlying graph, and its implementation completion contract requires uncertainty and abstention to survive end to end. The original reconstruction's `old_accepts=true` values for SF-01 through SF-03 were wrong.

### CRV

v0.5 already states that evaluation is stage-specific and separately enumerates retrieval/high-recall coverage, evidence-support/contradiction accuracy, and adjudication accuracy. Its hard invariants prohibit collapsing distinct epistemic dimensions. The original reconstruction's `old_accepts=true` values for CRV-01 and CRV-02 were wrong.

### FARA admission terminology

FARA defines a candidate as an object "admitted for consideration"; candidate status does not imply admissibility. A1 therefore does not redefine `admitted`. The repaired rule governs promotion into **authoritative or reliance-bearing state** after required validation.

## Lean trust-base bound

FAR's governed mechanization pins Lean 4.19.0. Lean issue #14576 documents a checked-kernel soundness defect; Lean 4.32.2 release notes state that the point release fixes that defect. The dated postmortem describes the exploit as reachable through metaprogramming.

The earlier reconstruction stated that a raw repository search for `Lean.Meta`, `run_tac`, and `unsafe` had zero matches. That was false: raw `unsafe` matches exist, including text/comments and existing Lean material. This reconstruction makes no zero-match claim. A lexical grep cannot establish exploitability or non-exploitability.

Accordingly, the campaign records a checker-trust limitation only. It does not downgrade a FAR-CORE theorem, declare any governed proof invalid, or claim the absence of an exploit path. The actual v0.5 gap tested here is narrower: method/version provenance already exists, but known material trust-base limitations relevant to the assurance claim were not explicitly required to remain attached.

## Failure-origin bound

Who&When Pro v1 constructs failure-attribution trajectories by replaying a successful prefix and then injecting a controlled failure. SATURATION-FALSIFICATION-001 uses this only to justify preserving detection location separately from challengeable origin attribution; it does not claim the paper proves FAR's proposed schema.

## Scientific result

The seven findings do not force a new first-class capability class.

- Hearsay: `ASSURANCE_BOUNDARY_CHANGE`
- SkillCascade: `ASSURANCE_BOUNDARY_CHANGE`
- verification/reliance-state promotion: `SPECIFICATION_REPAIR`
- synthesis fidelity: `REPRESENTABLE_NO_CHANGE`
- failure-origin localization: `SPECIFICATION_REPAIR`
- CRV separation: `REPRESENTABLE_NO_CHANGE`
- Lean trust-base qualification: `SPECIFICATION_REPAIR`

Therefore:

- capability-class saturation: survives these seven attacks;
- no-change saturation: falsified by five bounded deltas, not seven;
- v0.6: not justified;
- Amendment A1: candidate Research/Provisional five-rule repair;
- FARA minimality: not adjudicated here;
- external utility: not tested here.

## Validation boundary

The reconstruction must be judged on the exact pushed branch head by the repository's normal protected validation. Any CI failure introduced by this reconstruction is controlling. Passing CI is not independent scientific replication.
