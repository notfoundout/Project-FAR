# FAR Evidence-Closure Correction v1.0

Status: **Accepted internal methodology correction**

Date: 2026-09-22

## Question

Can a FAR investigation reach a correct claim-level disposition and still close too early because the workflow does not separately require bounded evidence saturation, surviving-claim analysis, and residual-uncertainty accounting?

## Execution

Current authority was traced through `AGENTS.md`, the research execution charter, project status, canonical map, the FAR workflow, FAR methodology, FAR investigation validation, the methodology audit protocol, and the operational FAR research/audit skills.

The closure path was then attacked for early-stop behavior after decisive evidence, denominator or estimand mismatch, indirect evidence substituted for mechanism-specific evidence, omitted measurement/classification uncertainty, omitted strongest opposing evidence, untested alternative explanations, unrecorded narrower surviving claims, and closure without a terminal bounded saturation pass.

## Observation

The existing methodology strongly governed pre-contract ambiguity and required bounded search/saturation before an under-specified input could be frozen into a comparison-contract family. It also required counterexample search, typed verdicts, limitations, and explicit closure status.

However, once substantive evaluation began, the canonical closure rule permitted `Resolved` when a resolution had been recorded under the stated resolution rule. It did not independently require that a decisive claim-level disposition be followed by a bounded post-evidence saturation pass or by explicit checks for denominator/directness mismatch, measurement limitations, strongest opposing evidence, alternative explanations, narrower surviving propositions, and residual uncertainty.

Therefore the methodology could produce a logically correct atomic verdict while still under-investigating the surrounding evidentiary structure.

## Discovery

Claim adjudication and investigation closure are different states.

A decisive witness, counterexample, proof, or authoritative record may settle an atomic claim before the investigation is ready to close. The adjudication remains valid at its exact scope, but methodological closure requires a second gate that demonstrates bounded evidence saturation and records what remains live.

The correction is represented by closure contract `FAR-EVIDENCE-CLOSURE-1.0` in the canonical FAR workflow.

## Accepted requirements

Before `Resolved` or `Provisionally resolved` closure under the corrected workflow, the investigation must:

1. preserve the exact atomic claim form and distinguish claim-level logical disposition from investigation closure;
2. record the decisive evidence and the exact proposition it establishes or refutes;
3. enumerate the applicable evidence/search classes and either execute each or mark it `NOT APPLICABLE` with a reason;
4. test whether the evidence uses the correct denominator, estimand, comparison class, mechanism, and level of directness for the claim being interpreted;
5. identify material measurement, classification, provenance, and ascertainment limitations;
6. seek and record the strongest support and strongest counterevidence still relevant after the initial disposition;
7. test material alternative explanations or inference paths where the claim form makes them relevant;
8. identify narrower, adjacent, conditional, or comparative propositions that survive even when a broader proposition has been adjudicated;
9. state residual uncertainty explicitly, including unresolved empirical questions that the decisive evidence does not answer;
10. execute a terminal bounded saturation pass over the registered applicable evidence/search classes, with no new material evidence, claim decomposition, alternative explanation, or residual-uncertainty item appearing in that terminal pass;
11. run the methodology audit before methodological closure.

If the terminal pass finds a new material item, the investigation remains open and the search frame must be updated before another closure attempt.

## Boundary and stopping rule

The correction does not require unbounded research. Every investigation retains a declared evidence cutoff, search frame, applicability decisions, and stopping rule. The terminal saturation pass establishes closure only relative to that bounded frame.

A universal or open-world completeness claim still requires its own exhaustive or formal justification. `FAR-EVIDENCE-CLOSURE-1.0` does not convert bounded search into proof of open-world completeness.

A decisive claim-level verdict may be recorded before the closure gate completes. If further research is unavailable or unjustified, the investigation may remain `Suspended`, `Incomplete`, `Unresolved`, or another applicable typed state while preserving the earlier atomic verdict at its exact scope.

## Machine-enforced execution boundary

For execution manifests created after this correction, `result: pass` is rejected unless the manifest carries an `evidence_closure` record bound to `FAR-EVIDENCE-CLOSURE-1.0`.

That record must include repository-backed closure evidence, the bounded search frame and stopping rule, applicable evidence/search classes, denominator/directness and measurement/classification checks, strongest support and counterevidence, alternative explanations, surviving propositions, residual uncertainty, terminal saturation evidence, and methodology-audit evidence. Empty substantive lists require an explicit basis. An executed evidence/search class requires evidence; a `NOT_APPLICABLE` class requires a reason. Terminal saturation fails closed if any new material evidence, claim decomposition, alternative explanation, or residual-uncertainty item is reported.

The execution validator preserves the two execution manifests that predate this correction without rewriting their historical records. The compatibility boundary is pinned to the exact existing Git blob identities for `VI-001` and `VI-002`; changing either historical manifest invalidates the exemption, and future manifests cannot self-declare legacy status or reuse it under a new ID.

## Promotion

The correction is promoted through:

- `frameworks/FAR/workflow.md` as the canonical closure contract and stage-sequence authority;
- `frameworks/FAR/methodology.md` as the governing closure-discipline principle;
- `frameworks/FAR/investigation-validation.md` as the methodological validation gate;
- `methodology/methodology-audit-protocol.md` as the self-audit requirement;
- `.claude/skills/far-clean-room-auditor/SKILL.md`;
- `.claude/skills/far-discovery-engine/SKILL.md`;
- `.claude/skills/far-research-orchestrator/SKILL.md`;
- `.claude/skills/far-research-quality-gate/SKILL.md`;
- `tools/check_investigation_execution.py` as the fail-closed execution-manifest boundary for future PASS declarations;
- `tools/check_far_evidence_closure.py` as cross-surface drift protection;
- `tests/test_investigation_execution_closure.py` and `tests/test_far_evidence_closure.py` as regression coverage.

## Re-evaluation rule

This correction does not retroactively rewrite historical investigation records or their recorded verdicts.

Any historical result reused as current evidence for a new `Resolved` or `Provisionally resolved` FAR investigation must satisfy the corrected closure gate for that new investigation. A prior investigation materially dependent on the newly identified failure mode should be flagged for re-audit before its closure status is relied on as evidence of current methodological completeness.

## Nonclaims

This correction does not establish:

- open-world evidence completeness;
- that every relevant evidence class can be known in advance;
- that bounded saturation proves source truth or source authority;
- that all measurement or classification error can be quantified;
- that every alternative explanation can be enumerated;
- that a terminal saturation pass is independent replication;
- external validation, novelty, priority, empirical utility, or commercial value;
- any change to Project FAR core-theory theorem status or `far-ir/2.x` semantics.
