---
name: far-clean-room-auditor
description: "Runs evidence-first clean-room audits across research, repositories, specifications, software, datasets, and mixed evidence. Resolves controlling authority, freezes exact claims and scope, separates evidence from assumptions and inference, seeks counterexamples, prevents overclaiming, and returns typed verdicts with material limits."
---

# FAR Clean-Room Auditor

Use this skill when the task is to audit, verify, falsify, reproduce, red-team, reconcile, or assess an exact claim or artifact.

This is an operational audit skill. It does not create Project FAR theory, evidence status, governance authority, or external-validation status. For Project FAR work, `AGENTS.md`, the research execution charter, current default-branch governance, and canonical repository sources remain controlling.

## Objective

Produce a conclusion that another reviewer can reproduce from the exact proposition, admitted sources, declared rules, and recorded tests. The audit must remain logically valid if the auditor's preferred conclusion is false.

## Non-negotiable rules

1. **Search before concluding.** Inspect the target, governing instructions, current state, relevant dependencies, and available evidence before assigning a verdict.
2. **Resolve controlling authority by role.** Separate authority for definitions, official state, procedure, observation, provenance, and methodology. A source may control one role and be weak for another.
3. **Freeze the exact claim before testing.** Preserve wording, quantifiers, domain, comparison class, assumptions, version/time, applicability, and explicit nonclaims. Do not silently repair, broaden, narrow, or reinterpret it.
4. **Atomize composite claims.** Audit materially separable conjuncts independently, then derive the parent result.
5. **Separate premise types.** Mark material premises as `EVIDENCE`, `DEFINITION/CONSTRAINT`, `ASSUMPTION`, `DERIVATION`, or `INFERENCE`.
6. **Keep evidence distinct from inference.** An inference is not upgraded into evidence by repetition, authority, agreement, or convenient placement in a canonical document.
7. **Make support and refutation claim-specific.** A claim is falsified only when its frozen refutation condition is met. One adverse observation is not automatically a counterexample to a probabilistic, causal, statistical, comparative, or threshold claim.
8. **Actively seek failure.** Search for contradictions, boundary cases, counterexamples, stronger comparators, alternative explanations, stale state, hidden assumptions, source conflicts, and negative executions.
9. **Treat absence as bounded.** `Not found` becomes `does not exist` only under a justified exhaustive, closed-world, or formal-completeness argument.
10. **Track provenance and lineage.** Record source identity, version/hash/date, location, transformation, retrieval path, and dependency lineage. Derivative sources do not become independent confirmations.
11. **Respect chronology.** Outcome-sensitive rules, comparison universes, authority precedence, and claim contracts must be fixed before evidence whose interpretation depends on them.
12. **Separate mutable epochs.** Do not combine state-bearing evidence across materially different target states. Recheck current state immediately before a current-state verdict.
13. **Never upgrade uncertainty.** Missing, inaccessible, conflicting, ambiguous, stale, or unexecuted evidence cannot count as positive support.
14. **Prefer the narrowest defensible conclusion.** Evidence for subset `A` does not verify a broader `A+B` claim. Insufficient support is normally `OPEN`, not `FALSIFIED`.
15. **Do not self-certify controls.** Labels such as `complete`, `fresh`, `independent`, `exhaustive`, `all requirements covered`, or `criterion frozen` require evidence; the label is not evidence for itself.
16. **Require proof closure.** A decisive verdict must be traceable through its actual supporting/refuting premises. A wrapper derivation cannot make its leaves stronger, broader, newer, more authoritative, or more independent than they are.
17. **Preserve conflicts.** Genuine incompatible admitted evidence remains visible. Do not average it away or discard the inconvenient side without a controlling rule.
18. **End with a typed verdict and material limits.** State the exact claim, decisive evidence, strongest attacks, verdict, and only the limits that materially constrain interpretation.

## Project FAR authority routing

For Project FAR audits, the coordinator performs this routing before preparing an isolated evaluator's packet. Before launch, reconcile the supplied-input restriction with applicable repository and task instructions; this skill does not create an exception to `AGENTS.md`. If those instructions cannot be reconciled, report the conflict and leave the affected independent stage blocked. An evaluator authorized to use only supplied inputs must use the supplied authority records rather than opening the live repository. If a required record is absent, record the dependency as blocked and return it to the coordinator; do not relax the isolation boundary to retrieve it.

For unrestricted internal audits and coordinator preparation:

1. Read `AGENTS.md` and `docs/governance/research-execution-charter.md`.
2. Resolve current state from `README.md`, `docs/project-status.md`, and `docs/CANONICAL_MAP.md`.
3. Read only the governance, theory, evidence, implementation, or historical artifacts materially required by the audit.
4. Treat repository presence as proof that an artifact exists, not proof that it is Accepted, canonical, current, or evidentially sufficient.
5. If purported current authorities conflict, stop the affected inference and report the conflict. Do not silently choose by recency, convenience, or prior conversation.
6. Conversation history, generated output, archived material, and unmerged branches are navigation aids unless current governance grants them authority.
7. Internal audit results do not satisfy external replication, independence, novelty, utility, or other governed stages merely because the audit is rigorous.

Use `far-canonical-source-resolver` first when repository authority is unclear. Use `far-theory-auditor` for a narrower logical attack on theory claims; use this skill when the audit also requires provenance, authority, state, evidence-lineage, reproducibility, or typed-verdict discipline.

## Isolation gate

Invoking this skill does not create evaluator isolation. Apply the [Isolation Classification Doctrine](../../../docs/doctrine/isolation-classification.md) and the target protocol before claiming completion of any independent-audit stage. A protocol can require stronger controls than the general doctrine.

- A pass in the construction session, including switching skills or adopting a reviewer role, is **I0 — No Isolation**. Use it for internal exploratory findings; it does not satisfy independent validation.
- **I1 — Claimed Isolation** requires a separately instantiated evaluation context receiving only the explicitly supplied frozen inputs, with repository access prohibited by instruction. Do not forward conversation history, prior verdicts, construction notes, or other material outside the registered packet. Record evaluator/context identity, supplied input hashes, exposure, and the access restriction. A fresh context alone does not establish the restriction.
- **I2 — Verified Isolation** additionally requires evidence that the environment technically prevents access beyond the supplied inputs. A promise, skill invocation, new agent, or shared-filesystem workspace is not that evidence.
- **I3 — External Independent Validation** requires independent researchers or external systems to reproduce the result without Project FAR controlling the evaluation or supplying its reasoning as the basis. A Project-FAR-orchestrated evaluator is not I3 merely because it uses another model.

If the required controls are unavailable or fail, disclose actual exposure, use only the class supported by evidence, and leave the required independent stage unsatisfied. Continue any useful authorized internal checks. Do not promote a claim on the premise that the missing stage completed. Preserve negative findings; isolation limits do not erase a counterexample or establish its correctness.

Every validation report must include an **Isolation Classification** section with the class, evaluation method, technical limitations, and whether repository access was prohibited by instruction or prevented technically. Report truth verdict, repository acceptance status, and isolation separately. Do not retroactively relabel historical reports solely to apply the doctrine.

When context or access-control evidence is absent, report **isolation class not established** and identify the missing evidence. Do not invent I0 or any stronger class; independent-stage completion is not established.

## Audit contract

Before substantive evaluation, record:

- **Object:** exact artifact, claim set, system, corpus, process, repository state, or dataset.
- **Question:** exact decision the audit must make.
- **Snapshot:** immutable commit/hash/version/release where possible; otherwise mutable identifier plus retrieval time.
- **Authority map:** which source controls each relevant role and why.
- **Exact claim:** wording, logical form, quantifiers, domain, comparison class, assumptions, applicability, time/version, and nonclaims.
- **Support condition:** evidence pattern that would satisfy the claim at the intended strength.
- **Refutation condition:** evidence pattern that would defeat the exact claim.
- **Search frame:** sources/locations searched, query or inspection strategy, cutoff, inclusion/exclusion rules, and stopping condition where completeness matters.
- **Adversarial obligations:** strongest plausible attacks that must be attempted.
- **Isolation boundary:** prior exposure, corpus/tool/communication isolation, intervention history, and claimed independence level if independence matters.

If outcome-sensitive criteria are chosen after seeing the result, classify the analysis as exploratory rather than confirmatory.

## Evidence ledger

For every material premise record:

| Field | Requirement |
|---|---|
| ID | Stable local identifier |
| Type | `EVIDENCE`, `DEFINITION/CONSTRAINT`, `ASSUMPTION`, `DERIVATION`, or `INFERENCE` |
| Source | Exact source or dependency premises |
| Version | Commit/hash/version/date when relevant |
| Scope | Which frozen claim(s) it bears on |
| Establishes | Narrow proposition directly licensed |
| Does not establish | Nearby stronger conclusions explicitly excluded |
| Quality | Relevance, validity, reliability |
| Lineage | Original source and transformations/copies |
| Time | Observation/retrieval/admission time where state matters |

Do not count copied reports, mirrors, summaries, or multiple derivations of one root source as independent corroboration.

## Claim-form checks

Identify the logical form before deciding what could verify or falsify it.

- **Universal claim:** one valid in-scope counterexample falsifies it; positive verification requires proof or justified exhaustive coverage.
- **Existential claim:** one valid witness can establish existence; failure to find a witness does not establish nonexistence unless the domain is closed and exhaustively checked.
- **Negative existential:** requires exhaustive/closed-world/formal completeness to verify.
- **Probabilistic/statistical claim:** apply the frozen statistical estimand and decision rule; individual adverse cases may be expected under the claim.
- **Causal claim:** require explicit identification assumptions and test plausible alternative explanations; association alone is insufficient.
- **Comparative/superiority claim:** freeze comparator set, metric, population/domain, and decision rule before evaluation.
- **Conformance claim:** enumerate authoritative applicable requirements and trace every material requirement to assessment evidence.
- **Current-state claim:** require authoritative state evidence and a freshness check inside the same target epoch.
- **Completeness/novelty/prior-art claim:** define the search universe and cutoff; open-world search normally yields bounded support, not exhaustive verification.
- **Normative claim:** freeze the normative criterion separately from factual premises; empirical evidence alone cannot establish the criterion.
- **Formal theorem:** identify logic, premises/axioms, definitions, derivation, and any machine/kernel assumptions. Successful execution alone is not premise-free proof.

## Adversarial phase

Attempt, as applicable:

- direct contradiction;
- smallest counterexample;
- domain-boundary counterexample;
- stale/superseded authority;
- conflicting controlling sources;
- hidden premise removal;
- circular dependency;
- alternative causal explanation;
- stronger comparator;
- source-lineage collapse;
- duplicate evidence presented as independent;
- outcome-sensitive rule chosen post hoc;
- mutation/state drift;
- missing requirement;
- search-universe narrowing;
- evidence from the wrong version or epoch;
- claim-scope drift;
- inference presented as direct observation;
- CI/test success presented as proof of a broader research claim.

A successful attack changes the verdict only to the extent licensed by the exact frozen claim and refutation rule.

## Verdict vocabulary

Use the target protocol's mandated verdict vocabulary and decision rules when it supplies them; preserve exact recorded labels without silently translating their meanings. Otherwise use exactly one primary verdict for each atomic claim:

- **VERIFIED** — the exact claim is established within its frozen scope by deductive proof, justified exhaustive closed-world checking, direct authoritative record/state evidence, or complete conformance evidence. This does not imply broader empirical generalization.
- **SUPPORTED** — defeasible empirical, statistical, causal, historical, predictive, comparative, or bounded-search evidence satisfies the frozen evidentiary rule at the stated strength.
- **FALSIFIED** — the frozen refutation condition is satisfied by admitted evidence.
- **OPEN** — admitted evidence satisfies neither support nor refutation.
- **BLOCKED** — a required source, environment, permission, gate, or test is unavailable and prevents adjudication. Finish independent checks before using this verdict.
- **UNDERDETERMINED** — multiple materially different admissible interpretations/models/metrics/standards remain and no controlling rule selects among them.
- **NOT APPLICABLE** — the claim or test does not apply to the frozen object under the declared scope.

`HISTORICAL`, `SUPERSEDED`, `STALE`, and similar labels describe evidence/state; they are not truth verdicts.

## Overclaim lint

Before finalizing, test every sentence for these invalid promotions:

- bounded result -> universal result;
- internal result -> external result;
- successful execution -> theoretical proof;
- formal proof -> empirical utility;
- replication -> independence;
- repeated source -> independent corroboration;
- no counterexample found -> proof;
- schema validity -> semantic correctness;
- repository placement -> authority;
- authoritative statement -> external-world truth;
- correlation -> causation;
- search failure -> nonexistence;
- finite corpus performance -> population performance;
- novelty search -> priority claim;
- evidence quantity -> evidence quality.

Rewrite or narrow any sentence that crosses one of these boundaries without a separate warrant.

## Final report

Lead with the verdict. Then provide:

1. **Frozen claim** — exact wording and scope.
2. **Authority** — controlling sources and any material conflicts.
3. **Decisive evidence** — what directly establishes or refutes the claim.
4. **Reasoning** — explicit derivations/inferences, with assumptions named.
5. **Adversarial results** — strongest attacks attempted and whether they succeeded.
6. **Verdict** — one typed verdict per atomic claim.
7. **Material limits** — only limitations that could change interpretation or generalization.
8. **Required correction** — smallest complete correction when the audited object fails.

For Project FAR validation, include the Isolation Classification report required above and state explicitly whether the applicable independent-audit stage is satisfied. Recommendations do not themselves change governed claim status.

Never end with a stronger summary claim than the evidence ledger and atomic verdicts license.
