# Project Roadmap

This roadmap records gated future work. It is a planning surface, not theory or evidence, and it cannot authorize work that the Research Execution Charter or a registered program does not authorize.

## Current release and phase

Current published repository release: [`v1.0.0`](releases/project-far-v1.0.0.md).

Current program: [`POST-TERM-EVAL-001`](governance/post-terminal-public-evaluation-program-v1.0.md).

The Universal Proof Program `POST-TUE-UPP-001` is complete and its deductive queue is closed. There is no `UPP-W16`. Any stronger deductive theorem requires a separately registered program.

## Ordered post-terminal work

The current order follows the registered post-terminal evaluation program:

1. **`PTE-W1-INDEPENDENT-REVIEW` — next.** Prepare the exact terminal theorem, frozen premises, dependency audit, proof obligations, mechanization boundary, nonclaims, and reviewer-disclosure requirements for genuinely independent proof review.
2. **`PTE-W2-KERNEL-RECONSTRUCTION`.** Attempt one end-to-end proof-assistant reconstruction of the terminal semantic composition. If full reconstruction fails, preserve the strongest explicit obstruction and identify every external assumption that remains outside the kernel.
3. **`PTE-W3-COUNTERMODEL-SEARCH`.** Seek countermodels and scope challenges against class membership, admissibility, faithfulness, machinery closure, equivalence, component necessity, construction sufficiency, independence, maximality, and terminal composition. Failed challenges remain evidence; unresolved challenges remain `Unknown`.
4. **`PTE-W4-EMPIRICAL-REPLICATION`.** Obtain independent bounded replication under a frozen protocol. Project-authored or same-implementation-path execution is not independent replication and cannot establish the deductive theorem by itself.
5. **Application correspondence.** Test whether real systems actually satisfy the terminal theorem's premises and whether representation preserves the registered commitments. Application success or failure affects correspondence evidence, not the theorem automatically.

These workstreams may proceed only within their registered scope. Completion of one does not silently upgrade another evidence dimension.

## Current gates

Before claiming progress in a post-terminal channel:

- identify the exact theorem, premise, bounded result, or application claim under review;
- preserve the terminal theorem's frozen premise set and open-world boundary;
- preregister empirical execution when the governing protocol requires it;
- disclose evaluator independence and prior exposure;
- preserve negative results, failed reconstructions, ambiguity, and protocol deviations;
- issue a claim-impact record for confirmed defects;
- keep unresolved defects or observationally indistinguishable alternatives as `Unknown`;
- never use CI success, finite testing, internal replication, or absence of known counterexamples as proof of unrestricted claims.

## Theory and stronger-claim policy

Post-terminal evaluation is not a hidden continuation of the closed deductive program.

A stronger theorem, broader target class, weaker premise set, stronger maximality claim, or changed equivalence criterion requires a separately registered deductive program before derivation. It may not be smuggled into review, replication, application work, or maintenance.

## Engineering and experiments

Supporting engineering is justified only when required by an authorized evaluation channel, reproducibility obligation, security/integrity defect, or accepted repository-maintenance requirement.

Do not prioritize generic product expansion, another benchmark version, new dashboards, favorable-case accumulation, or speculative infrastructure merely because implementation is possible.

A new empirical run must have an authorized protocol, frozen inputs, acceptance/adjudication rules, provenance, independence classification, and evidence-preservation path before execution.

## Framework maintenance

FARA, FAR, FARO, FARE, and FARM remain maintained at their current governed scopes. Framework stability is not evidence for unrestricted universality or superiority. Changes to stable layers require the applicable change-control and provenance rules.

## Release track

- Current published repository release: [`v1.0.0`](releases/project-far-v1.0.0.md).
- The installable package version remains a separate surface governed by `pyproject.toml`.
- Historical release baselines remain preserved under [`releases/`](releases/).

Release packaging does not strengthen theorem assurance, independence, empirical validity, or application correspondence.

## Historical roadmap

The superseded pre-terminal roadmap, including the v0.4.0, anti-self-validation, REP/ADJ/W3.5, and earlier validation planning sequence, is preserved byte-for-byte at [`../archive/superseded/status/roadmap-pre-terminal-2026-08-10.txt`](../archive/superseded/status/roadmap-pre-terminal-2026-08-10.txt).

The `.txt` extension is deliberate: historical relative links remain part of the preserved bytes but are not presented as live repository documentation.

That snapshot is historical and does not define current priorities.

## Long-term objective

Determine the strongest justified account of the structure of explicit, auditable reasoning; expose the exact boundaries under which the terminal relative result holds; identify countermodels, unnecessary commitments, failed correspondences, and simpler rivals where they exist; and reduce or retract claims when evidence requires it.

Project success is measured by the accuracy and auditability of the final claim boundary, not by forcing Project FAR to survive criticism.
