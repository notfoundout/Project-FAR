# External Falsification and Replication Program v1.0

Program ID: `EXTERNAL-FALSIFICATION-AND-REPLICATION-001` (`EFR-001`)

Status: **PREREGISTERED — NOT EXECUTED**

Proposed: 2026-09-05

Registration text finalized: 2026-09-06; the protected promotion event supplies the authoritative freeze timestamp.

Registration is proposed by PR #470; the protected-main promotion freezes its final reviewed bytes before any execution. Pre-merge review corrections are retained in that PR, not represented as amendments to an executed study.

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

Input seals precede the applicable execution; output seals follow execution and precede comparison/unblinding. Derivations, ratings, field outcomes, and search results are prospective outputs, never prerequisites for starting the test. Prospective field records receive an append-only input seal on enrollment before allocation is revealed. The fixed methods below permit only identities, dates, sources, and observations to be filled in later; they permit no later scientific design choices.

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

| ID | Question | Frozen sample / input | Acceptance criterion | Failure criterion | Invalid / inconclusive criterion |
|---|---|---|---|---|---|
| `EFR-R1` | Independent deductive replication | Two I3 teams; immutable v1.1 statements/premises; W1 verdicts, W1 reasoning, and W2 proof sources withheld until seal | Both teams return valid derivations for all 14 exact-scope claims and no unresolved material objection survives adjudication | Any team supplies a reproducible in-scope contradiction/countermodel or identifies an invalid proof step that survives adjudication | Exposure, collusion, missing disclosure, or use of withheld material |
| `EFR-R2` | Clean-room technical replication | Two independently authored implementations using only published W3/W5 specifications; expected outputs and repository implementations withheld; frozen baseline W3 conformance, W4 12-record, W5 control, and W6 primary/secondary packages | Both implementations agree with one another and the frozen expected result on every required item | Any valid item mismatch survives adjudication | Use of Project FAR implementation/checker/test/oracle/proof code, expected output, or another team's code |
| `EFR-H1` | Held-out external cases | Exactly 120 externally supplied cases: for each of six domains, 10 preservation and 10 material-loss cases | Overall at least 54/60 material-loss cases flagged and 54/60 preservation cases accepted, and at least 8/10 correct in each class in each domain | Any overall or per-domain threshold is missed | Provenance failure, label leakage, or post-unblinding selection/replacement |
| `EFR-A1` | Adversarial counterexamples | Exactly 60 schema-valid external challenges, 10 per domain, including at least 5 custodian-certified material-loss cases per domain | Every valid in-scope material-loss case is flagged; all outputs and failure codes are reported | One valid, in-scope, ground-truth material-loss case is accepted as preserving, or an output is silently dropped | Missing custodian ground truth, broken seal, or an out-of-scope case counted as success |
| `EFR-HD1` | Human disagreement | 24 external reviewers; 120 EFR-H1 cases; 1,440 ratings, six ratings per case per arm; randomized, domain/class-blocked, counterbalanced assignment | FAR-assisted pairwise material-disagreement rate is at least 10 percentage points lower and the two-sided 95% case-bootstrap interval for the reduction excludes 0; serious false-accept rate is noninferior within 2 percentage points | The 10-point effect, confidence criterion, or safety margin is missed | More than 5% missing, arm missingness differs by more than 2 points, or blinding/allocation fails |
| `EFR-U1` | Prospective real-world utility | Three external sites, 40 consecutive eligible investigations per site; 20 standard and 20 FAR-assisted allocations per site | Material escaped-defect rate falls by at least 5 absolute points and 20% relatively; the two-sided 95% site-stratified bootstrap interval excludes 0; no site worsens by more than 5 points; zero FAR-attributable serious harms | Any benefit, site, or harm gate is missed | Site loss, broken blinding, non-reconstructable allocation, or absent screening log |
| `EFR-C1` | Cost and burden | Measurements from EFR-HD1 and EFR-U1; no composite score | Every coordinate passes: median task-time ratio ≤1.50; training ≤8 hours/person; incremental direct cost ≤USD 100 per case in 2026 dollars; median increase ≤10/100 on each raw NASA-TLX dimension; zero severe burden events | Any coordinate exceeds its gate, is unavailable, or is replaced by a scalar aggregate | Broken measurement-ledger seal or provenance failure |
| `EFR-N1` | Novelty/prior art | Independent search through the frozen cutoff 2026-09-05 over scholarly literature, patents, standards, and cited/citing chains; four essential elements below | `NOT_FALSIFIED_BY_REGISTERED_SEARCH` only if no qualifying pre-cutoff source teaches every essential element in combination | `FALSIFIED` if one qualifying pre-cutoff source teaches all four elements in the claimed arrangement; neither outcome authorizes a novelty claim | Non-independent search, cutoff breach, missing query log, or incomplete required source class |

### EFR-R1 — independent deductive replication

Each team receives only the v1.1 theorem statements, definitions, declared premises, exact scopes, historical-artifact hash, and this protocol. W1 and W2 review/proof material stays withheld. Each team must submit derivations, countermodels, objections, an exposure declaration, and a machine-readable 14-row verdict ledger before unblinding.

A syntactic difference is not a replication failure. Adjudication asks whether each derivation establishes the exact governed statement from its declared premises, and whether each adverse witness satisfies the governed domain. Any surviving contradiction reopens only the affected statement and its dependants; it does not silently rewrite unrelated claims.

Teams have 60 calendar days from receipt of the permitted packet. Missing or inadequate derivations at that deadline fail replication (`NOT_REPLICATED`) without refuting a theorem. The custodian supplies statement-only excerpts, never the proof-containing theorem file or the matrix/review package. Prior access to withheld arguments disqualifies a team before enrollment; access after enrollment invalidates its attempt. Both technical teams likewise have 60 days to seal source and outputs. A timeout or missing output fails replication and cannot be adjudicated away as formatting.

### EFR-R2 — independent technical replication

Teams implement the published `far-ir/2.0` and `far-ir/2.1` semantics from scratch. They may use general-purpose languages and libraries, but not Project FAR verifier/checker/test source, generated expected outputs, W6 oracle source, or another team's code. Output schemas, environment lockfiles, source hashes, and complete logs are mandatory.

The all-items rule is deliberate: no accuracy average can hide a mismatch. A protocol breach is `INVALID/INCONCLUSIVE`, never a pass.

The custodian extracts every input named by the baseline W3 conformance index, W4 manifest, W5 campaign manifest, and W6 protocol, preserving hashes and removing only expected-result fields. The extraction map records every removed field and every original object ID. Both teams seal implementations before receiving the held-out execution inputs. Compare outcome, error category, and recomputed evidence as canonical JSON (sorted object keys; arrays retain order); diagnostic prose and timing are not comparison fields. Two independent adjudicators audit the extraction map before execution. No fixture may be silently omitted because it is difficult to implement.

### EFR-H1 and EFR-A1 — external and adversarial cases

Each domain stratum is fixed before access: formal logic, Bayesian/causal reasoning, argumentation, model-based reasoning, type theory, and proof theory. Custodians must establish the required behavior and preservation/loss label without using the Project FAR implementation under test. H1, A1, HD1, and U1 test exact `far-ir/2.0` finite-explicit contracts with literal canonical-JSON equality; approximate/tolerance decisions belong to R2 and are outside these human/external binary-loss endpoints. Cases must be representable under that frozen exact contract; excluded open-oracle, continuous, embodied, or changing-ontology cases remain reported as out of scope and are never counted as successes.

EFR-A1 is a direct falsification test. One accepted, valid, in-scope material-loss counterexample fails the zero-miss criterion even if every other item passes.

For H1, custodians screen pre-existing external records in ascending public creation timestamp, breaking ties by source identifier, and take the first ten eligible records per domain and class. Every screened record and exclusion is retained. Eligibility requires an independently sourced real domain problem, a finite-explicit behavior/representation table, and a determinate label; copied or transformed W4/W6 fixtures are excluded. Two independent domain judges label before any FAR run; a third resolves differences by a recorded majority with a checkable witness. Unresolved labels are excluded before sealing, never after outcomes are seen. FAR's exact baseline implementation is the tested system, with no tuning on H1 or A1.

For A1, independent red teams may inspect public specifications and seek counterexamples, but may not query the tested implementation before the complete challenge set is sealed. Budget is 60 person-hours per domain. In submission order, take the first five eligible material-loss challenges and the first five remaining eligible challenges per domain. Failure to supply the registered set is `INVALID/INCONCLUSIVE`, not a smaller successful campaign. Ground truth follows the same judge/witness rule. A1's adversarial selection supplies no population estimate.

### EFR-HD1 — human disagreement

Eligible reviewers are consenting adults aged at least 18, outside Project FAR control and artifact authorship, who can complete the frozen English-language materials without translation and whose existing environment passes the frozen conformance test. An applicable ethics/IRB determination must authorize recruitment. The sole domain-training qualification is completion of the registered four-hour course and correct classifications and witnesses on all twelve W4 qualification records: both records in every one of the six domains must pass. No degree, discipline, job title, prior experience, or operator judgement of expertise supplies an additional inclusion rule or substitutes for that qualification. Prior education and experience are recorded descriptively and cannot select participants or strata. This defines a trained finite-record reviewer population, not six-domain professional experts. Assignment uses a seed derived mechanically from the sealed complete HD1 input-manifest SHA-256, binding case metadata and reviewer roster. Each reviewer receives disjoint cases across arms, preventing recognition of a repeated case. The exact instructions, form and permitted rendering equivalence, four-hour training sequence, time limits, eligibility scoring, and adjudication rubric are committed now in the [human-study materials](../research/external-falsification-and-replication/01-human-study-materials.md) and content-addressed in the input freeze. Intake may attest rendering conformance and supply participant identities; it may not choose or change these materials.

Enroll the first 24 consenting, non-author reviewers who pass all 12 public W4 practice records after the fixed training: a two-hour native-table module followed by a two-hour FAR-report and qualification module, including the fixed breaks. Practice results and failed screening attempts are retained. Each task has the same native evidence, a binary preservation/loss response and a required witness; the FAR arm additionally sees the frozen verifier's diagnostic report. Both arms have a 20-minute limit. No conversational assistance or task-specific coaching is allowed. The interface must satisfy the frozen rendering equivalence in the materials: specified content, controls, timing, viewport, and geometry, with only the listed system-font/rasterization/wrapping variations. Participant environments are sampled and fixed under that rule before qualification; no new display contract or outcome-adaptive choice is permitted at intake.

Sort the six domain names and the two classes, shuffle the ten case IDs inside each stratum, and concatenate the strata. Shuffle the 24 reviewer IDs with the same seeded Python 3.12 `random.Random` stream. For case index c (0–119), FAR reviewers occupy positions (c+j) mod 24 for j=0–5; standard reviewers occupy (c+12+j) mod 24. Each reviewer therefore makes 30 decisions per arm on 60 distinct cases. Even reviewer positions take FAR first, odd positions standard first; generate each reviewer/arm task sequence with an independent seed: SHA-256 of ASCII `manifest_sha256 + "\nEFR-HD1\n" + reviewer_id + "\n" + arm + "\n"`, first 16 hex digits as an unsigned integer. Start from lexically sorted assigned case IDs and call `random.Random(seed).shuffle` once. Arm IDs are exactly `far` and `standard`. The frozen [allocation script](../../tools/efr_hd1_allocation.py) fixes every stratum/roster iteration and RNG call; it is normative and receives only the sealed input format documented in the materials. Publish the entire allocation before collecting ratings.

The materials fix ten six-task sessions, first-arm days 2–6 and second-arm days 8–12 after day-0 training, 09:00 local starts, fixed task/workload slots, ten-minute pair breaks, a no-rating day 7, and missing-session handling. Session timing, delays, and break rules are not left to operator choice.

“Material disagreement” means differing binary preservation/loss decisions where at least one decision conflicts with the sealed custodian label. Report raw arm counts, pairwise agreement, category-specific agreement, and Gwet's AC1 as a secondary descriptive statistic. Cohen's kappa may be reported but cannot determine acceptance because prevalence can distort it. The primary interval uses 10,000 case-level bootstrap resamples with the manifest-derived seed.

For each case/arm compute the fraction of its 15 unordered reviewer pairs that disagree, then average equally over all 120 cases. Reduction is standard minus FAR. A serious false accept is a preservation answer on a custodian-labelled loss case; its rate is the fraction of the 360 loss-case ratings per arm. Noninferiority requires the upper endpoint of the two-sided 95% interval for FAR minus standard false-accept rate to be at most 0.02. Resample the same cases jointly across arms within each of the 12 strata. At permissible missingness, each pair containing a missing FAR rating counts as disagreement and each pair containing a missing standard rating as agreement. For the separate false-accept endpoint, impute missing FAR decisions as wrong and missing standard decisions as correct; additionally report complete cases descriptively. These primary rules cannot turn missing FAR responses into a benefit.

### EFR-U1 — prospective utility

Sites enroll consecutive eligible investigations and publish a screening log. Allocation is generated centrally from the sealed manifest seed, blocked by site. Blinded external adjudicators determine escaped material defects and serious harms using the frozen rubric. Withdrawals stay in their allocated arm for intention-to-treat analysis; a missing primary output counts as an escaped defect.

Enroll the first three consenting independent organizations with an existing routine documentary audit workflow, at least 40 forthcoming investigations, lawful access to the evidence, and an applicable ethics determination. Eligible investigations audit an existing finite record and a declared required behavior from one of the six domains; exclude consequential medical/legal/financial decisions, live interventions, missing consent, and open-oracle cases. Record exclusions prospectively. At each site enroll the next 40 eligible investigations within 180 days, with no outcome-based replacement. Failure to enroll all 40 makes that site's study inconclusive.

Before enrollment seal each site's existing standard procedure verbatim; the FAR arm adds only the fixed W3/W5 contract fields and baseline verifier report to that procedure. Training is the same four-hour course as HD1. Audit time limit is 60 minutes in both arms. For each site shuffle 20 standard and 20 FAR slots using the sealed roster-manifest seed; reveal only the next slot after its case is enrolled and hashed. Site weights are equal. An escaped material defect is a behavior-changing representation error that the final submitted audit fails to identify with a correct witness. Three external adjudicators, blinded to arm and aggregate rates, inspect source evidence and determine this binary endpoint by a recorded majority; all reasons and dissent remain public in deidentified form.

Reduction is standard minus FAR defect proportion; relative reduction divides that difference by the standard proportion. A zero standard proportion cannot pass the benefit gate. Use 10,000 resamples of investigations within each site and arm to form the interval for the equally site-weighted reduction. Each site's unrounded observed reduction must be at least −0.05. Assess harms through 30 days after each audit. Serious harm means death, hospitalization, permanent impairment, unauthorized sensitive-data disclosure, or an irreversible consequential action attributable to reliance on the FAR-assisted audit; any confirmed event or harm-related safety stop fails the safety gate. No such action is an intended part of this study.

Passing supports only a finite, three-site prospective result under the registered workflow and population. It does not establish general external validity, general professional benefit, safety certification, or deployment readiness.

### EFR-C1 — vector cost/burden

Time, training, direct cost, and each of the six raw NASA-TLX dimensions remain separate coordinates. No weighting or averaging across coordinates, currency conversion beyond the frozen 2026-USD rule, or post-hoc tradeoff can rescue a failed coordinate. The thresholds are program acceptance choices, not universal welfare or optimization theorems.

Apply every gate separately to HD1 and to each U1 site; pooling cannot rescue a failing site. Task time runs from first evidence display to submitted answer, including tool latency; timed-out tasks receive the full limit. Time ratio is median FAR minutes divided by median standard minutes (a zero denominator fails). Training is all attendance plus setup/practice time per person. Direct cost includes paid labor, training labor amortized over that participant's allocated cases, compute, licenses, and consumables; use a fixed accounting price of USD 50 per labor hour and require all nonlabor invoices denominated in USD. Amounts are nominal study-year dollars with a fixed 3% annual deflator: 2026 USD = nominal USD / 1.03^(invoice year − 2026). No exchange-rate choice is permitted. Incremental cost is mean FAR minus mean standard cost per case, capped at USD 100; report total and per-case costs too.

For every C1 median, sort all allocated arm observations numerically as x[0] through x[n−1]. If n is odd, use x[n//2]; if n is even, use (x[n//2−1] + x[n//2]) / 2. Thus HD1 uses the mean of sorted positions 359 and 360 in each 720-rating arm, and each U1 site uses positions 9 and 10 in each 20-investigation arm. Missing observations fail the coordinate and are never dropped to change n. Parse recorded decimal measurements exactly as `fractions.Fraction` strings; elapsed times are recorded as integer milliseconds, rounded down once at capture, and converted to minutes by division by 60000. TLX inputs are integers. Medians, means, differences, ratios, labor accounting, and the deflator (`Fraction(103,100)` to the integer year offset) use exact rational arithmetic without intermediate or threshold rounding. Display rounding occurs only after the verdict. This fixed midpoint median is an operational statistic, not a claim that ordinal workload has an interval-scale interpretation.

Collect six separate 0–100 ratings after every task: mental demand, physical demand, temporal demand, unsuccessful performance (100 worst), effort, and frustration. For each dimension compare arm medians, FAR minus standard; each difference must be ≤10. No TLX composite is calculated. Severe burden means a participant withdrawal or safety stop explicitly attributed to physical or psychological study burden, or a burden event requiring medical care; any such event fails. Missing time/cost/training/TLX measurements fail the relevant coordinate, even when HD1 remains analyzable. These are operational study choices, not claims that workload is an interval scale or that the deflator estimates inflation.

### EFR-N1 — scoped prior-art falsification

The candidate combination is decomposed before searching:

1. a declared comparison contract determines a behavior map;
2. exact sufficiency is equivalent to factorization through a representation;
3. the kernel of the behavior map induces a unique least-informative exact quotient up to isomorphism; and
4. on a nontrivial domain no one representation is simultaneously least-informative for every unrestricted observation contract.

A source qualifies only if public before 2026-09-05, independently retrievable, and it teaches all four elements in combination rather than merely supplying separate component analogies. Searchers must retain queries, databases, dates, inclusion/exclusion decisions, claim charts, citations, and negative results. Partial anticipation is reported element by element.

Two I3 searchers independently run each of these exact quoted-string queries, with the publication cutoff 2026-09-05: `"sufficient representation" "factorization"`; `"observational quotient" "minimal"`; `"kernel" "quotient" "sufficient"`; `"Blackwell" "sufficiency"`; `"minimal sufficient statistic" "partition"`; `"universal" "observation" "minimal representation"`. Required services are Google Scholar (scholarly), Google Patents (patents), and the public ISO, IEEE Standards, and IETF indexes (standards). Inspect the first 100 relevance-ranked results per query/service, or every returned result if fewer; retain result order, dates, and exported records. Inspect every backward reference and every first-generation forward citation returned by Scholar (up to 100 per source) for any source matching at least two elements. Citation expansion stops after that one generation, regardless of result direction. Record inaccessible full text as unresolved; it blocks the no-falsifier search disposition if at least two elements are apparent. A required service unavailable or an incomplete search is inconclusive; no database substitution or early favorable stop is permitted.

For each candidate the chart records all four elements, their arrangement, exact page/section references, public-date evidence, and both searchers' decisions. The shared three-person adjudication panel must reproduce any proposed anticipation from that source. Component prior art is always reported even if no single-source four-element falsifier is found. The search budget is 60 calendar days; expiration with an incomplete required search is inconclusive. This is a deliberately bounded search test, not an exhaustive prior-art review.

Failure to locate an anticipating source is not proof of novelty. Patent-law novelty, priority, and legal conclusions remain outside this research program absent qualified legal review.

## Analysis, missingness, deviations, and stopping

All allocated items are analyzed. Unreturned machine output is a failure for that item. For human data, more than 5% missing ratings overall, more than a 2-point arm imbalance in missingness, loss of a site, broken blinding, label leakage, or a non-reconstructable allocation makes the affected test `INVALID/INCONCLUSIVE`; it cannot pass. Lesser missingness is reported and analyzed by intention to treat with the rules above.

All seeds use the unsigned integer represented by the first 16 hexadecimal characters of the applicable sealed input-manifest SHA-256; use separate Python 3.12 `random.Random(seed)` streams for allocation and analysis, with sorted IDs as input order. HD1 uses its complete input-manifest digest, including the roster and case metadata; the custodian script verifies the exact source bytes against the externally sealed digest before allocation. Bootstrap intervals are percentile intervals using sorted resample estimates at zero-based indices 249 and 9749. No rounding is applied at thresholds, no covariate adjustment is primary, and no optional subgroup can replace a registered endpoint. The fixed sample sizes and decision thresholds are prospective program choices, not asserted power guarantees.

### Exact bootstrap and field-allocation call schedules

All rates, differences, percentile sorting, and primary threshold comparisons use exact rational arithmetic from integer counts (Python `fractions.Fraction`), not rounded floating-point values. Convert to decimal only for display after the verdict. There are no random calls other than those specified here and in the frozen HD1 allocator.

HD1 analysis starts a fresh `random.Random(hd1_seed)` once. Precompute each case's integer disagreeing-pair count for each arm (out of 15), and false-accept count for each arm on loss cases (out of six), applying the frozen missingness rules first. Build strata in exactly the allocation script's `DOMAINS` order and `CLASSES` order, with each stratum's ten case IDs sorted lexically. The loop order is normative:

```python
rng = random.Random(hd1_seed)
for resample in range(10000):              # outermost loop
    sampled_cases = []
    for domain in DOMAINS:                # six fixed domain IDs
        for label in CLASSES:            # material_loss, then preservation
            stratum = sorted_ids[domain, label]
            for draw in range(10):
                sampled_cases.append(stratum[rng.randrange(10)])
    # The same 120 draws supply BOTH endpoints; no further random calls.
    reduction = Fraction(sum_std_pairs - sum_far_pairs, 120 * 15)
    false_accept_difference = Fraction(sum_far_false_accepts - sum_std_false_accepts, 60 * 6)
    # Store both fractions for this resample, then begin the next resample.
```

The four sums are over the sampled cases with multiplicity; false-accept sums use only the 60 sampled loss cases. Observed endpoints use the original 120 cases once each. Sort the 10,000 fractions independently for each endpoint and select indices 249 and 9749. Acceptance requires observed reduction ≥`Fraction(1,10)`, its lower percentile >0, and the false-accept difference's upper percentile ≤`Fraction(1,50)`, in addition to validity gates. No separate RNG stream or extra draw is used for the safety endpoint.

U1 site IDs are S01–S03 in eligible consent-timestamp order, breaking exact ties by legal organization name. Investigation IDs are the site ID plus the three-digit consecutive enrollment index. The complete site-roster manifest binds identities, SOP hashes, and allocation inputs; its independently sealed SHA-256 supplies `u1_seed`. Allocation starts a fresh `random.Random(u1_seed)`, iterates sites S01, S02, S03, and for each starts `slots = ["far"] * 20 + ["standard"] * 20`, calls `rng.shuffle(slots)` exactly once, and seals that site's slots. There are no intervening random calls; reveal slots only after prospective case enrollment.

U1 analysis uses a separate fresh stream with that same seed. For each site and arm, sort the 20 allocated investigation IDs lexically, including missing outputs as escaped defects. Loop exactly as follows:

```python
rng = random.Random(u1_seed)
for resample in range(10000):              # outermost loop
    counts = {}
    for site in ("S01", "S02", "S03"):
        for arm in ("far", "standard"):
            counts[site, arm] = 0
            for draw in range(20):
                case_id = sorted_ids[site, arm][rng.randrange(20)]
                counts[site, arm] += escaped_defect[case_id]  # integer 0 or 1
    reduction = Fraction(sum(counts[s, "standard"] - counts[s, "far"]
                             for s in ("S01", "S02", "S03")), 60)
    # Store the fraction, then begin the next resample; no extra random calls.
```

Use indices 249 and 9749 of sorted resample reductions. Observed reduction uses each original investigation once. Its absolute gate is ≥`Fraction(1,20)`; relative reduction is that observed difference divided by the observed standard-arm defect rate and must be ≥`Fraction(1,5)` (zero denominator fails). The lower percentile must exceed zero, each observed site reduction must be ≥`-Fraction(1,20)`, and the separately observed harm gate must pass. These loops fix computation; they do not authorize early stopping, refreezing labels, or changing the recorded sites/cases.

Before any execution name three independent adjudicators, none on an execution team or under Project FAR control. They see item-level witnesses and permitted scope only, with team/arm identity and aggregate outcomes withheld. A valid adverse finding requires a reproducible witness satisfying the declared premises, documented by at least two adjudicators. Unresolved validity disputes make the affected test inconclusive and block acceptance; disagreement is not permission to discard a negative observation. Output disagreements caused by a confirmed implementation error remain failures. Only a proved intake/protocol defect can yield invalidity, with the original output retained. Each test's acceptance is conjunctive; an unmet acceptance condition without a proved invalidity is failure (R1 non-replication is not automatically theorem refutation).

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
- [USPTO MPEP 2131](https://www.uspto.gov/web/offices/pac/mpep/s2131.html) — anticipation requires every element in the claim's arrangement; used only to define a falsifier, not to claim a legal conclusion.
