# SWE-agent v2 forensic postmortem

Status: **Research; evidence-bounded causal audit**
Date: 2026-07-26
Decision preserved: **`REVIEW_REQUIRED`**

## Executive finding

The authoritative experiment contains **one frozen task**, `scikit-learn__scikit-learn-14125`, not two tasks, with two repetitions for SWE-agent v1.0.0 and two for v1.0.1. All four produced nonempty, applicable patches, stopped at the identical 31-call `exit_cost` boundary, preserved nine reported PASS_TO_PASS tests, and failed the same required FAIL_TO_PASS test. Therefore the frozen result remains v1.0.0 **0/2**, v1.0.1 **0/2**, and `no_observed_resolution_difference`. This is not evidence of equivalence.

The deepest patch-level cause cannot be established from the repository. Exact trajectories, stdout/stderr, model messages, tool events, patches, predictions and grader logs are enumerated and authenticated by the frozen source lock but are not committed. The first incorrect assumption, missed signal, unsupported leap, wasted sequence and irreversible agent mistake are therefore **unknown for every run**. Calling any specific hypothesis the root cause would guess. What is established is narrower: each applied patch failed the oracle target; every trajectory exhausted the call budget; and external-only artifact retention prevents complete repository-only diagnosis.

## Method and authority

The audit inspected architecture, canonical terminology, framework/dependency boundaries, governance claim/limitations/question registers, project status, roadmap, decision log, stabilization audit, reproducibility guide, v2 protocol/configuration/locks, all v2 workflows, validation and report-generation code, every committed primary-freeze and reveal artifact, and the source artifact lock. The [authority map](swe-agent-v2-forensics/authority-map.md) distinguishes evidence from producer code and derived analysis. The [inventory](swe-agent-v2-forensics/evidence-inventory.json) records present and external-only artifacts with hashes and ambiguity; [provenance](swe-agent-v2-forensics/provenance-manifest.json) records the transformation boundary.

Frozen files were not transformed or regenerated. This audit neither reran the comparison nor executed a held-out task.

## Reconciled identity and outcomes

| Run | Blind identity | Task | Calls | Patch | Grader | Final |
|---|---|---|---:|---|---|---|
| `v1.0.0-r1` | System-A-r1 | scikit-learn-14125 | 31 | 2170 B, applies | target fails; 9 neighbors pass | unresolved |
| `v1.0.0-r2` | System-A-r2 | scikit-learn-14125 | 31 | 3890 B, applies | target fails; 9 neighbors pass | unresolved |
| `v1.0.1-r1` | System-B-r1 | scikit-learn-14125 | 31 | 2843 B, applies | target fails; 9 neighbors pass | unresolved |
| `v1.0.1-r2` | System-B-r2 | scikit-learn-14125 | 31 | 3288 B, applies | target fails; 9 neighbors pass | unresolved |

Task IDs, blinded IDs, revealed versions, repetitions and outcomes reconcile. The premise “both frozen tasks” is **disproven** by the authoritative task record and report; silently manufacturing a second task would corrupt the record.

## Chronology

Each machine timeline contains all 21 requested stages and all requested event fields. Known aggregate/final events are recorded; unavailable ordering is explicitly null/unknown. Human reconstructions explain the evidentiary boundary:

- [v1.0.0-r1](swe-agent-v2-forensics/timelines/v1.0.0-r1.md) ([JSON](swe-agent-v2-forensics/timelines/v1.0.0-r1.json))
- [v1.0.0-r2](swe-agent-v2-forensics/timelines/v1.0.0-r2.md) ([JSON](swe-agent-v2-forensics/timelines/v1.0.0-r2.json))
- [v1.0.1-r1](swe-agent-v2-forensics/timelines/v1.0.1-r1.md) ([JSON](swe-agent-v2-forensics/timelines/v1.0.1-r1.json))
- [v1.0.1-r2](swe-agent-v2-forensics/timelines/v1.0.1-r2.md) ([JSON](swe-agent-v2-forensics/timelines/v1.0.1-r2.json))

Exact pre-grading chronology fails closed as unavailable rather than being reconstructed from unordered counts.

## Per-run causal postmortem

The following applies separately to each of the four runs; run-specific paths/commands are in the linked timelines.

| Required finding | Evidence class | Finding |
|---|---|---|
| First incorrect assumption | unknown | Ordered reasoning absent. |
| First missed signal | unknown | Command outputs/messages absent. |
| First unsupported leap | unknown | Cannot identify from counts. |
| First wasted action sequence | unknown | No order/duration/content. |
| First point recovery became unlikely | inferred | Budget autosubmission at call 31 ended further recovery; when likelihood declined is unknown. |
| First irreversible mistake | unknown | No earlier action is proven irreversible; termination froze the trajectory. |
| Proximate failure | directly derived | Applied patch failed `test_type_of_target_pandas_sparse`. |
| Root-cause candidate | inferred | Budget may have truncated correction, but a wrong hypothesis/model-policy limitation competes. Confidence medium because termination is observed while the counterfactual benefit is not. Falsified/weakly supported by a trace showing intentional completion with no viable next step; strengthened by a checkpoint containing an unexecuted viable correction. |
| Deepest supported root cause | unknown | Patch semantics and reasoning are inaccessible. |
| Stopping reason | observed | `submitted (exit_cost)`. |
| Plausible path to resolution | unknown | A functioning grader and passing neighbors do not prove that the agent found a viable fix. |
| Remediability | directly derived | Artifact retention, status classification and pre-submit target gates are controllable; resolution itself is not guaranteed. |
| Future requirement | directly derived | REQ-P0-002, REQ-P0-003 and REQ-P1-001. |

The machine [cause-to-control matrix](swe-agent-v2-forensics/cause-to-control.json) gives per-run support, contradiction, alternatives, confidence reasoning, confirmation/falsification conditions, layers, controls, tests, cost, risk and priority.

## Layered findings

- **Agent/model/prompt/policy:** the patches did not resolve the target. Whether misunderstanding, navigation, localization, hypothesis, design or implementation caused that result is insufficiently evidenced.
- **Controller/experiment design:** uniform 31-call budget termination is observed; its causal impact is inferred with medium confidence, not proven.
- **Test strategy:** the retained grader target discriminated every patch. Historical test discovery/execution is unknown.
- **Artifact pipeline/infrastructure:** authoritative source content is external-only. This directly causes diagnostic insufficiency, not benchmark failure.
- **Provider/quota:** no frozen package records a provider/quota terminal failure. Earlier free-tier access failure is a separate episode. Absence from aggregates does not disprove transient effects.
- **Grader:** patches applied consistently and reports agree. Oracle mismatch is not supported, but raw logs are unavailable.
- **Workflow:** later stabilization fixed outer-success/internal-75 masking. No evidence makes that historical defect the cause of these four `exit_cost` submissions.
- **Experiment design:** one task/two repetitions cannot support equivalence, superiority or general performance claims; a floor effect is plausible, not established.

## Behavioral and adequacy conclusions

The [behavioral comparison](swe-agent-v2-forensics/behavioral-comparison.md) shows actual differences despite equal scores: v1.0.0-r2 alone touched tracked implementation/test paths; command mixes and exploratory coverage varied; v1.0.1-r2 issued two pytest commands. Within-version variation and tiny exposure prevent attributing those differences to release. The [task assessment](swe-agent-v2-forensics/task-difficulty.md) concludes that 0/2 versus 0/2 is informative only for these trajectories and cannot establish equivalence or population performance.

## Detailed registers

- [Failure taxonomy A–AC](swe-agent-v2-forensics/failure-taxonomy.json)
- [Provider and infrastructure](swe-agent-v2-forensics/provider-infrastructure.md)
- [Patch and prediction](swe-agent-v2-forensics/patch-prediction-analysis.md)
- [Testing behavior](swe-agent-v2-forensics/testing-behavior.md)
- [Missed recovery opportunities](swe-agent-v2-forensics/missed-recovery-opportunities.md)
- [Counterfactual replay](swe-agent-v2-forensics/counterfactual-replay.md)
- [Future requirements](swe-agent-v2-forensics/future-v3-requirements.json)
- [Limitations](swe-agent-v2-forensics/limitations.md)
- [Unresolved questions](swe-agent-v2-forensics/unresolved-questions.md)

P0 requirements prevent invalid execution/conclusions and evidence loss; P1 requirements gate patch submission on discriminating evidence; P2 requirements improve testing/study adequacy; P3 improves future policy analysis. These are constraints only. No v3 architecture, controller, prompt, multi-agent review, candidate generation or repository intelligence is designed or implemented.

## Counterfactual conclusion

Durable evidence would have made the failures more diagnosable. Explicit budget/status semantics would have prevented mistaken operational conclusions. A target-test gate would have rejected each exact failing submission if the target were available before submission. None of these facts proves that another transition would resolve the task. The [counterfactual report](swe-agent-v2-forensics/counterfactual-replay.md) preserves that distinction.

## Final bounded conclusion

**Observed:** four applicable patches, four target failures, four budget terminations, 0/2 for each release. **Directly derived:** `no_observed_resolution_difference`; `REVIEW_REQUIRED`. **Inferred:** budget and test policy are plausible contributors, with alternatives retained. **Unknown:** first agent failure points and deepest patch-level causes. **Disproven:** equivalence, empty patches, nonapplying patches, two-task membership, and any claim that operational completion proves resolution. **Assumed:** no causal claim relies on an assumption; speculative recovery options are labeled as such.
