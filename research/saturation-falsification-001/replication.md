# SATURATION-FALSIFICATION-001 replication record

Status: Research / Provisional reconstruction

## Reconstruction boundary

The original Ultracode session committed an unpushed local head `f3bd22de` and stopped while exact-head validation was running. That object was never pushed to GitHub and is unavailable to this session. This record therefore reconstructs the campaign from the surviving transcript and canonical `main` at `8618384efe4576580f65ff67b02b22bac43ffc51`; it does not claim byte identity with the lost local head.

## Canonical baseline

The reviewed v0.5 artifact is `docs/architecture/saturation-baseline-v0.5.md`. It is Research/Provisional and already distinguishes broad capability classes, epistemic dimensions, provenance, validation, security, evaluation, synthesis, and meta-assurance. The hostile test was not whether each new result could be named by one of those buckets, but whether the existing specification explicitly preserved and enforced the decision-relevant distinction.

## Source bindings

- Hearsay / independent agent-record evidence: https://arxiv.org/abs/2609.32495
- SkillCascade / cross-skill composition: https://arxiv.org/abs/2609.30383
- Verification as an architectural layer: https://arxiv.org/abs/2609.31937
- Active provenance / synthesis fidelity: https://arxiv.org/abs/2609.31422
- Who&When Pro / failure-origin localization: https://arxiv.org/abs/2607.09996
- CRV coverage-realization-validity distinction: https://arxiv.org/abs/2609.32924
- Lean kernel bug: https://github.com/leanprover/lean4/issues/14576
- Lean postmortem: https://leodemoura.github.io/blog/2026-8-1-postmortem-for-kernel-soundness-bug-14576/

The disposition record paraphrases only bounded implications used by this campaign. A future independent review should reconstruct those implications from the primary sources rather than treating this document as source authority.

## Counterexample method

The 25 fixtures in `counterexamples-v1.0.json` encode one distinction at a time. `old_accepts` means the case is not explicitly rejected by the pre-amendment obligations tested here; it does not mean every possible implementation conforming to v0.5 would necessarily accept the case. `amended_accepts` is the expected result under Amendment A1.

The permanent regression test verifies:

1. all seven findings are present exactly once;
2. only the campaign's frozen disposition vocabulary is used;
3. no finding is promoted to `NEW_CAPABILITY_CLASS_REQUIRED`;
4. all seven amendment rules exist literally;
5. 25 fixtures are present and every negative counterexample is closed by the corresponding rule;
6. controls remain accepted;
7. campaign nonclaims keep FAR-CORE, EFR, #518, novelty, independence, and commercial status unchanged;
8. the Lean result is qualified rather than promoted to theorem invalidity.

## Lean trust-base bound

FAR's governed mechanization pins Lean 4.19.0. Lean disclosed kernel soundness bug #14576, and the documented fix appears in Lean 4.32.2, so the pinned FAR version predates that fix and the issue is relevant to the trusted checker boundary. A bounded code search of canonical `main` for `Lean.Meta`, `run_tac`, and `unsafe` returned no repository-tracked matches. This scan is not proof that an exploit path is impossible and is not an independent re-check of every transitive toolchain component.

Accordingly, the campaign records a checker-trust limitation only. It does not downgrade a FAR-CORE theorem, declare any governed proof invalid, or claim the absence of an exploit path.

## Failure-origin bound

Who&When Pro defines failure attribution around a decisive step produced by exact successful-prefix replay followed by a controlled failure injection. The project description defines the decisive step as the earliest action whose correction would have changed the failed outcome, and reports that models often label an error by its visible symptom rather than its cause. SATURATION-FALSIFICATION-001 uses this only to justify preserving detection location separately from origin attribution; it does not claim the paper proves FAR's proposed schema.

## Scientific result

The seven findings fail to force a new first-class capability class. They do force explicit specification/assurance obligations that the pre-amendment v0.5 text did not state strongly enough. The bounded result is therefore:

- capability-class saturation: survives these seven attacks;
- no-change saturation: falsified;
- v0.6: not justified;
- Amendment A1: candidate Research/Provisional repair;
- FARA minimality: not adjudicated here;
- external utility: not tested here.

## Validation boundary

The reconstruction must be judged on the exact pushed branch head by the repository's normal protected validation. Any CI failure introduced by this reconstruction is controlling. Passing CI is not independent scientific replication.
