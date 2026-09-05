# External Falsification and Replication Program v1.0

Program ID: `EXTERNAL-FALSIFICATION-AND-REPLICATION-001` (`EFR-001`)

Status: **PREREGISTERED — NOT EXECUTED**

Registered: 2026-09-05

Predecessor: `POST-CLOSURE-001`, complete at its six registered scopes.

This is a separate successor program, not `PCA-W7` or “W7.” No external team, held-out case, human participant, field site, or result is represented as enrolled, collected, or completed by this preregistration.

## Purpose and authority

EFR-001 attempts to falsify or independently replicate only the bounded claims recorded in the [canonical W1–W6 matrix](w1-w6-claim-evidence-matrix-v1.0.md). It addresses the evidence classes that internally authored repository work cannot supply: I3 independent replication, held-out external cases, adversarial counterexamples, human disagreement, prospective real-world utility, externally observed cost/burden, and scoped novelty/prior-art testing.

The governing v1.1 core stays closed unless a reproducible contradiction to a stated premise, proof step, theorem, or derivation survives the adjudication rule below. A successful EFR test cannot establish a contract-free universal architecture, population-wide external validity, unrestricted human utility, novelty, commercial value, or FARO readiness.

The machine authority is [`external-falsification-and-replication-program-v1.0.json`](../../theory/evaluation/external-falsification-and-replication-program-v1.0.json). The staged input authority is [`external-falsification-and-replication-input-freeze-v1.0.json`](../../theory/evaluation/external-falsification-and-replication-input-freeze-v1.0.json).

## Frozen inputs and prospective case lock

The inherited evidence cutoff is exactly Git commit `195fc079d0a8993e4db3e063e09cf45d0bcd78c2`, tree `a01517ed65f45e62b3d47ffba9dc955fff2bae9b`. That tree is the only W1–W6 evidence baseline. The program, machine contract, matrix, and this protocol are separately content-addressed in the input-freeze record.

External cases and participant/site allocations do not yet exist and are not fabricated by this registration. Their **selection rules, stratum counts, endpoints, thresholds, exclusions, and analysis are frozen now**. Before any Project FAR author, implementation team, reviewer, or analyst receives unblinded contents, an independent custodian must:

1. create the complete case/label package for the applicable test;
2. record every file path, byte count, SHA-256, provenance statement, inclusion decision, and exclusion decision;
3. sign and timestamp a manifest;
4. commit or deposit that manifest in a read-only location; and
5. provide only blinded case identifiers to operators.

A missing case may not be replaced after unblinding. Corrupt or inaccessible files invalidate their entire predeclared stratum; correction requires a new protocol version and new complete stratum. Project FAR may not select, rewrite, relabel, or silently omit external cases. The empty intake slots in the freeze record are therefore an execution gate, not evidence.

## Independence and roles

An I3 replication team or custodian must be outside Project FAR control, must not have authored the relevant repository artifacts, and must disclose prior exposure, conflicts, funding, tools, and deviations. At least two replication teams must be from distinct organizations and may not exchange work before both submissions are sealed.

Roles are separated:

- custodians select, label, hash, and retain held-out cases;
- clean-room teams implement or re-derive from the permitted package;
- operators administer blinded studies;
- analysts run the frozen analysis without changing it;
- adjudicators resolve only predeclared validity questions while blinded to aggregate outcomes;
- Project FAR maintainers receive unblinded material only after all primary outputs are sealed.

An internal model, repeated repository run, differently prompted Project FAR agent, or implementation-diverse code written under Project FAR direction does not satisfy I3.

## Registered tests

| ID | Question | Frozen sample / input | Acceptance criterion | Failure criterion |
|---|---|---|---|---|
| `EFR-R1` | Independent deductive replication | Two I3 teams; immutable v1.1 statements/premises; W1 verdicts, W1 reasoning, and W2 proof sources withheld until seal | Both teams return valid derivations for all 14 exact-scope claims and no unresolved material objection survives adjudication | Any team supplies a reproducible in-scope contradiction/countermodel or identifies an invalid proof step that survives adjudication |
| `EFR-R2` | Clean-room technical replication | Two independently authored implementations using only published W3/W5 specifications; expected outputs and repository implementations withheld; frozen baseline W3 conformance, W4 12-record, W5 control, and W6 primary/secondary packages | Both implementations agree with one another and the frozen expected result on every required item | Any valid item mismatch survives adjudication, or either implementation relies on withheld repository implementation/proof code |
| `EFR-H1` | Held-out external cases | Exactly 120 externally supplied cases: for each of six domains, 10 preservation and 10 material-loss cases | Overall at least 54/60 material-loss cases flagged and 54/60 preservation cases accepted, and at least 8/10 correct in each class in each domain | Any overall or per-domain threshold is missed; provenance/label leakage invalidates the test |
| `EFR-A1` | Adversarial counterexamples | Exactly 60 schema-valid external challenges, 10 per domain, including at least 5 custodian-certified material-loss cases per domain | Every valid in-scope material-loss case is flagged; all outputs and failure codes are reported | One valid, in-scope, ground-truth material-loss case is accepted as preserving, or an output is silently dropped |
| `EFR-HD1` | Human disagreement | 24 external reviewers; 120 EFR-H1 cases; 1,440 ratings, six ratings per case per arm; randomized, domain/class-blocked, counterbalanced assignment | FAR-assisted pairwise material-disagreement rate is at least 10 percentage points lower and the two-sided 95% case-bootstrap interval for the reduction excludes 0; serious false-accept rate is noninferior within 2 percentage points | The 10-point effect, confidence criterion, or safety margin is missed |
| `EFR-U1` | Prospective real-world utility | Three external sites, 40 consecutive eligible investigations per site; 20 standard and 20 FAR-assisted allocations per site | Material escaped-defect rate falls by at least 5 absolute points and 20% relatively; the two-sided 95% site-stratified bootstrap interval excludes 0; no site worsens by more than 5 points; zero FAR-attributable serious harms | Any benefit, site, or harm gate is missed |
| `EFR-C1` | Cost and burden | Measurements from EFR-HD1 and EFR-U1; no composite score | Every coordinate passes: median task-time ratio ≤1.50; training ≤8 hours/person; incremental direct cost ≤USD 100 per case in 2026 dollars; median increase ≤10/100 on each raw NASA-TLX dimension; zero severe burden events | Any coordinate exceeds its gate, is unavailable, or is replaced by a scalar aggregate |
| `EFR-N1` | Novelty/prior art | Independent search through the frozen cutoff 2026-09-05 over scholarly literature, patents, standards, and cited/citing chains; four essential elements below | `NOT_FALSIFIED_BY_REGISTERED_SEARCH` only if no qualifying pre-cutoff source teaches every essential element in combination | `FALSIFIED` if one qualifying pre-cutoff source teaches all four elements in the claimed arrangement; neither outcome authorizes a novelty claim |

### EFR-R1 — independent deductive replication

Each team receives only the v1.1 theorem statements, definitions, declared premises, exact scopes, historical-artifact hash, and this protocol. W1 and W2 review/proof material stays withheld. Each team must submit derivations, countermodels, objections, an exposure declaration, and a machine-readable 14-row verdict ledger before unblinding.

A syntactic difference is not a replication failure. Adjudication asks whether each derivation establishes the exact governed statement from its declared premises, and whether each adverse witness satisfies the governed domain. Any surviving contradiction reopens only the affected statement and its dependants; it does not silently rewrite unrelated claims.

### EFR-R2 — independent technical replication

Teams implement the published `far-ir/2.0` and `far-ir/2.1` semantics from scratch. They may use general-purpose languages and libraries, but not Project FAR verifier/checker/test source, generated expected outputs, W6 oracle source, or another team's code. Output schemas, environment lockfiles, source hashes, and complete logs are mandatory.

The all-items rule is deliberate: no accuracy average can hide a mismatch. A protocol breach is `INVALID/INCONCLUSIVE`, never a pass.

### EFR-H1 and EFR-A1 — external and adversarial cases

Each domain stratum is fixed before access: formal logic, Bayesian/causal reasoning, argumentation, model-based reasoning, type theory, and proof theory. Custodians must establish the required behavior and preservation/loss label without using the Project FAR implementation under test. Cases must be representable under the preregistered finite-explicit contract; excluded open-oracle, continuous, embodied, or changing-ontology cases remain reported as out of scope and are never counted as successes.

EFR-A1 is a direct falsification test. One accepted, valid, in-scope material-loss counterexample fails the zero-miss criterion even if every other item passes.

### EFR-HD1 — human disagreement

Eligible reviewers must have domain-relevant training, provide consent under an applicable ethics/IRB determination, and have no role in Project FAR artifact authorship. Assignment uses a seed derived mechanically from the sealed case-manifest SHA-256. Each reviewer receives disjoint cases across arms, preventing recognition of a repeated case. Instructions, interface, training, time limit, and adjudication rubric are fixed before recruitment.

“Material disagreement” means differing binary preservation/loss decisions where at least one decision conflicts with the sealed custodian label. Report raw arm counts, pairwise agreement, category-specific agreement, and Gwet's AC1 as a secondary descriptive statistic. Cohen's kappa may be reported but cannot determine acceptance because prevalence can distort it. The primary interval uses 10,000 case-level bootstrap resamples with the manifest-derived seed.

### EFR-U1 — prospective utility

Sites enroll consecutive eligible investigations and publish a screening log. Allocation is generated centrally from the sealed manifest seed, blocked by site. Blinded external adjudicators determine escaped material defects and serious harms using the frozen rubric. Withdrawals stay in their allocated arm for intention-to-treat analysis; a missing primary output counts as an escaped defect.

Passing supports only a finite, three-site prospective result under the registered workflow and population. It does not establish general external validity, general professional benefit, safety certification, or deployment readiness.

### EFR-C1 — vector cost/burden

Time, training, direct cost, and each of the six raw NASA-TLX dimensions remain separate coordinates. No weighting, averaging, currency conversion beyond the frozen 2026-USD rule, or post-hoc tradeoff can rescue a failed coordinate. The thresholds are program acceptance choices, not universal welfare or optimization theorems.

### EFR-N1 — scoped prior-art falsification

The candidate combination is decomposed before searching:

1. a declared comparison contract determines a behavior map;
2. exact sufficiency is equivalent to factorization through a representation;
3. the kernel of the behavior map induces a unique least-informative exact quotient up to isomorphism; and
4. on a nontrivial domain no one representation is simultaneously least-informative for every unrestricted observation contract.

A source qualifies only if public before 2026-09-05, independently retrievable, and it teaches all four elements in combination rather than merely supplying separate component analogies. Searchers must retain queries, databases, dates, inclusion/exclusion decisions, claim charts, citations, and negative results. Partial anticipation is reported element by element.

Failure to locate an anticipating source is not proof of novelty. Patent-law novelty, priority, and legal conclusions remain outside this research program absent qualified legal review.

## Analysis, missingness, deviations, and stopping

All allocated items are analyzed. Unreturned machine output is a failure for that item. For human data, more than 5% missing ratings overall, more than a 2-point arm imbalance in missingness, loss of a site, broken blinding, label leakage, or a non-reconstructable allocation makes the affected test `INVALID/INCONCLUSIVE`; it cannot pass. Lesser missingness is reported and analyzed by intention to treat with the rules above.

Safety or ethics bodies may stop participation. A safety stop records failure of the relevant safety gate; it is not excluded. EFR-R1 stops for a surviving core contradiction, after preserving all completed evidence. EFR-A1 does not stop after the first miss because the full adversarial surface must still be reported.

Scientific deviations and execution incidents are separate ledgers. Any post-freeze change to a primary endpoint, threshold, sample/stratum count, inclusion/exclusion rule, allocation, missing-data rule, or analysis invalidates confirmatory status for that test. The original test and result remain visible. A change requires a new version, a new complete freeze, and a fresh run; favorable results may not be reclassified post hoc.

## Program decision rule

Results are componentwise. EFR-001 may record `REGISTERED_EXTERNAL_EFFECTIVENESS_SUPPORTED` only if EFR-R1, R2, H1, A1, HD1, U1, and C1 all pass exactly. Any failed or invalid component remains failed or inconclusive and blocks that aggregate label. EFR-N1 is orthogonal and never implied by effectiveness.

A passing component authorizes only its own registered-scope sentence. A failed component does not refute the core unless its evidence meets that core statement's premises and EFR-R1 adjudication. No averaging across components, evidence-tier relabeling, or “promising trend” overrides a threshold.

## Current disposition

All eight tests are `PREREGISTERED_NOT_EXECUTED`. Intake manifests are empty. External independence, external validity, human utility, real-world benefit, cost-effectiveness, novelty, and FARO readiness remain unestablished.

## Method sources

- [Center for Open Science, Registered Reports](https://www.cos.io/initiatives/registered-reports) — prospective review and outcome-independent acceptance.
- [Center for Open Science, preregistration](https://www.cos.io/initiatives/prereg) — timestamped, read-only study plans.
- [TOP Guidelines](https://www.cos.io/initiatives/top-guidelines) — transparent distinction between replication and other evidence.
- Werner et al., [“Reproduce, Replicate, Reevaluate”](https://doi.org/10.1609/aaai.v38i14.29515) — reproduction/replication/reevaluation distinctions.
- Hardwicke and Wagenmakers, [“Reducing bias, increasing transparency and calibrating confidence with preregistration”](https://doi.org/10.1038/s41562-022-01497-2).
- Bolton, Biltekoff, and Humphrey, [“The Mathematical Meaninglessness of the NASA Task Load Index”](https://doi.org/10.1109/THMS.2023.3263482) — reason to preserve workload dimensions instead of treating an arbitrary composite as measurement.
- Tan et al., [agreement-statistic prevalence analysis](https://doi.org/10.1016/j.jtocrr.2023.100618) — reason not to make kappa the sole human-agreement endpoint.
- [USPTO MPEP ` 2131](https://www.uspto.gov/web/offices/pac/mpep/s2131.html) — anticipation requires every element in the claim's arrangement; used only to define a falsifier, not to claim a legal conclusion.
