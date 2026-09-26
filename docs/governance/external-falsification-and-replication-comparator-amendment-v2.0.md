# EFR-001 comparator amendment v2.0

Amendment ID: `EFR-001-COMPARATOR-AMENDMENT-2.0`

Program: `EXTERNAL-FALSIFICATION-AND-REPLICATION-001` (`EFR-001`), program version **2.0**

Status: **PREREGISTERED AMENDMENT — NOT EXECUTED**

Date: 2026-09-23

Machine authority: [`external-falsification-and-replication-comparator-amendment-v2.0.json`](../../theory/evaluation/external-falsification-and-replication-comparator-amendment-v2.0.json)

Materials: [EFR-001 v2.0 comparator study materials](../research/external-falsification-and-replication/04-comparator-study-materials-v2.0.md)

Amends: [External Falsification and Replication Program v1.0](external-falsification-and-replication-program-v1.0.md) as already amended for `EFR-R2` by [`EFR-001-R2-INPUT-AMENDMENT-1.1`](external-falsification-and-replication-r2-input-amendment-v1.1.md).

## 1. What this amendment does and does not touch

The frozen v1.0 program, its input freeze, and every content-addressed v1.0 object are **preserved byte-for-byte** as historical evidence; `tests/test_efr_comparator_amendment.py` fails closed if any of them drifts. The R2 v1.1 amendment is unchanged.

This amendment supersedes exactly three tests, which were never executed:

| Superseded (v1.0) | Replacement (v2.0) | Status of the v1.0 test |
|---|---|---|
| `EFR-HD1` human disagreement | `EFR-HD2` | `SUPERSEDED_NOT_EXECUTABLE` |
| `EFR-U1` prospective utility | `EFR-U2` | `SUPERSEDED_NOT_EXECUTABLE` |
| `EFR-C1` cost and burden | `EFR-C2` | `SUPERSEDED_NOT_EXECUTABLE` |

It also binds the **execution path** of the unamended `EFR-H1` and `EFR-A1` machine lane to the current strict `far-ir/2.0` verifier (§6). `EFR-R1`, `EFR-R2` (under v1.1), `EFR-H1`, `EFR-A1`, and `EFR-N1` keep every endpoint, threshold, sample, rule, and analysis.

## 2. The preregistration defect

`EFR-HD1` compared a FAR arm that received the verifier's report with a standard arm that received no machine output. `EFR-U1` did the same, adding FAR contract fields to its FAR arm only. For complete finite explicit tables, material loss is exactly a pair of cases sharing a representation value with different required behavior, so the verifier's report states the preservation/loss answer.

A pass under that design would therefore show at most that reviewers do better when handed a determinate answer. Any short collision-checking script would produce the same effect. The v1.0 design has no arm that separates FAR-specific benefit (its contract framing, fields, and report) from access to a generic determinate check. This is recorded as `LIM-048`.

## 3. Mandatory consequence

> **`EFR-HD1`, `EFR-U1`, and `EFR-C1` MUST NOT execute.** They cannot be run and then reinterpreted as FAR-specific evidence. Any data collected under them anyway would be a protocol breach, retained and disclosed, and would count toward no acceptance label.

`EFR-HD2`, `EFR-U2`, and `EFR-C2` may execute only under this amendment. As for v1.0 and v1.1, the protected-`main` promotion event supplies the authoritative freeze timestamp, and no participant, site, or case may be enrolled for these tests before that promotion.

The v2.0 allocation and analysis tools reject v1.0 input manifests (`test_id` must be `EFR-HD2` or `EFR-U2`), so a v1.0 HD1/U1 intake package cannot be fed through the v2.0 path.

## 4. Canonical state before this amendment

| Evidence | Recorded value |
|---|---|
| Status of every v1.0 registered test | `PREREGISTERED_NOT_EXECUTED` |
| v1.0 input-freeze slots for HD1/U1 | empty, awaiting independent custodian seal |
| Executed tests / external cases | none recorded in the canonical EFR authorities |

`tests/test_efr_comparator_amendment.py` checks these facts against the frozen v1.0 program and input-freeze records. As with v1.1, these checks prove only what the canonical EFR intake records; they do not prove the nonexistence of unregistered activity, which would fall under the v1.0 breach rules.

## 5. Replacement tests

The comparator arm, `checker`, receives the output of the frozen [generic table-consistency checker](../../tools/efr_generic_collision_checker.py). That script imports no Project FAR code and uses no Project FAR terminology. It lists every pair of cases sharing a representation value with different required behavior, or else one required-behavior value per representation value. For finite explicit tables it reaches the same classification as the FAR verifier. The FAR arm's report is the current strict verifier output (`contract_v2_strict`).

**Primary contrasts are FAR versus checker.** FAR versus standard and checker versus standard are reported descriptively only. They can never satisfy an acceptance criterion, because they cannot separate FAR-specific benefit from answer access.

| ID | Frozen sample / input | Acceptance criterion | Failure criterion | Invalid / inconclusive criterion |
|---|---|---|---|---|
| `EFR-HD2` | 60 external reviewers; the 120 EFR-H1 cases; three arms (`far`, `checker`, `standard`); six ratings per case per arm, 2,160 ratings; each reviewer rates 36 distinct cases, 12 per arm; each of the six arm orders used by exactly ten reviewers | Checker-minus-FAR pairwise material-disagreement rate is at least 5 percentage points; the lower nominal 95% crossed case/reviewer percentile of that reduction exceeds 0; the upper percentile of FAR-minus-checker serious false-accept rate is at most 2 percentage points | Any of these is missed | More than 5% of ratings missing; any two arms' missingness differs by more than 2 points of 720; broken blinding, label leakage, or non-reconstructable allocation |
| `EFR-U2` | Three external sites; 60 consecutive eligible investigations per site; 20 per arm per site, shuffled once per site from the sealed roster seed | Equal-site-weighted checker-minus-FAR escaped-defect proportion is at least 5 absolute points and at least 20% of the checker proportion; its lower nominal 95% site-worker/investigation percentile exceeds 0; no site's observed checker-minus-FAR reduction is below −5 points; zero FAR-attributable serious harms | Any benefit, site, or harm gate is missed | Site loss, broken blinding, non-reconstructable allocation, or absent screening log |
| `EFR-C2` | Measurements from `EFR-HD2` and each `EFR-U2` site | Every v1.0 C1 coordinate gate applies with the **checker** arm in place of the standard arm: median task-time ratio FAR/checker ≤ 1.50; training ≤ 8 hours per person; incremental direct cost FAR minus checker ≤ USD 100 per case (2026 dollars); each raw NASA-TLX median increase FAR minus checker ≤ 10; zero severe burden events | Any coordinate exceeds its gate, is unavailable, or is replaced by a scalar aggregate | Broken measurement-ledger seal or provenance failure |

Everything else about `EFR-HD2` follows v1.0 `EFR-HD1`, and everything else about `EFR-U2` and `EFR-C2` follows v1.0 `EFR-U1` and `EFR-C1`. That covers eligibility, ethics, the four-hour course and twelve-record qualification, rendering equivalence, time limits, the binary response and witness, material-disagreement and escaped-defect definitions, adjudication, harm definitions, missingness and invalidity rules, exact rational arithmetic, percentile indices 249 and 9749, 10,000 resamples, the cost-attribution and deflator rules, and all scope and nonclaim statements. It applies unchanged except for these deltas:

- **Arms and ratings.** Three arms replace two. HD2 has 60 reviewers and 2,160 ratings: 120 is a multiple of 60, so the cyclic allocation is exactly balanced (a 36-reviewer design was rejected because 120 cases cannot be spread evenly over 36 positions). Each U2 site has 60 investigations and at most 40 workers, assigned by the cyclic rule `(i-1) mod N` over `i = 1..60`.
- **Allocation.** HD2 uses cyclic positions `(c + 20k + j) mod 60` for arm index `k` (`far` = 0, `checker` = 1, `standard` = 2) and `j = 0..5`. Per-reviewer, per-arm task seeds use the label `EFR-HD2`. U2 shuffles `["far"]*20 + ["checker"]*20 + ["standard"]*20` once per site, in site order S01, S02, S03, from a fresh `random.Random(u2_seed)`.
- **Missingness imputation.** A missing FAR rating or output is always imputed against FAR: a disagreeing pair, a wrong loss-case answer, or an escaped defect. A missing checker or standard rating or output is imputed in that arm's favor. Missing FAR data can therefore never produce a FAR-specific benefit.
- **Crossed resampling.** Resampling follows the v1.0 loops with the third arm drawn in the same pass. For HD2 that is 12 strata × 10 case draws, then 60 reviewer draws. For U2 it is, per site, `N` worker draws followed by 20 investigation draws for each arm in the order `far`, `checker`, `standard`.
- **U2 zero-weight resamples.** v1.0 declared the whole U1 test `INVALID_UNESTIMABLE_RESAMPLE` if any resample drew only zero-weight workers for an arm. Simulation of the frozen v1.0 loop on correctly executed synthetic studies shows that happens by chance alone in about 100% of studies with 5 workers per site, about 48% with 10, and about 20% with 20. That is a defect in the v1.0 analysis rule, not a property of any study. U2 instead resolves such a resample conservatively: the FAR arm's rate is 1 and a comparator or standard arm's rate is 0. It never discards or redraws a resample, and it reports the count. Chance can therefore only make a FAR-specific pass harder, never easier or invalid. In simulation the worst case over 20 studies was 106 of 10,000 resamples, below the 250 that could by themselves set the lower percentile.
- **Cost attribution.** C2 charges FAR-specific preparation (projection, contract transcription, FAR report production) to FAR tasks only. It charges comparator-specific preparation (neutral table extraction, checker report production) to checker tasks only. It publishes all three arms' costs. Enrolled-person training is spread over that person's 36 HD2 tasks; HD2 non-person-attributable overhead is spread over 2,160 ratings; U2 site overhead is spread over the site's 60 investigations. Each HD2 arm median uses sorted positions 359 and 360 of 720, and each U2 site/arm median uses positions 9 and 10 of 20, exactly as in v1.0.

The normative scripts are [`efr_hd2_allocation.py`](../../tools/efr_hd2_allocation.py), [`efr_hd2_analysis.py`](../../tools/efr_hd2_analysis.py), [`efr_u2_analysis.py`](../../tools/efr_u2_analysis.py), and the [generic checker](../../tools/efr_generic_collision_checker.py). They are content-addressed in the machine authority. Synthetic unit fixtures verify scheduling, tamper rejection, and imputation direction only, and do not count as execution.

## 6. H1/A1 execution-path binding

The v1.0 H1/A1 machine lane replaces every supplied report with the frozen candidate factorization, whose evidence is `CHECKED_FINITE_EXPLICIT`, and then runs the baseline command. Under this amendment the lane runs `python -m mechanization.far_mechanization.contract_v2_strict RECORD --json` instead, and fails closed on any derived record whose evidence is not `CHECKED_FINITE_EXPLICIT`.

For such records the strict and baseline verifiers return identical diagnostics ([current verification rule](../specification/far-ir-2.0-current-verification.md)), so no H1/A1 endpoint, threshold, prediction, or outcome can change. The binding only ensures that the unchecked-`PROVED` gap (`LIM-047`) cannot occur on the current execution path. `tests/test_efr_comparator_amendment.py` checks the equivalence on the U1 projection and the W4 records.

The generic checker's H1/A1 classifications are additionally reported as a descriptive concordance statistic. They are not an acceptance criterion.

## 7. Program decision rule

`EFR-001` may record `REGISTERED_EXTERNAL_EFFECTIVENESS_SUPPORTED` only if `EFR-R1`, `EFR-R2` (v1.1), `EFR-H1`, `EFR-A1`, `EFR-HD2`, `EFR-U2`, and `EFR-C2` all pass exactly. `EFR-N1` stays orthogonal. v1.0's componentwise, no-averaging, and no-relabeling rules are unchanged.

## 8. What this amendment does not establish

This amendment executes nothing and makes no test more likely to pass. It does not establish external independence, replication, human utility, FAR-specific benefit, novelty, or any assurance upgrade. The comparator makes a FAR-specific benefit **harder** to demonstrate than under v1.0. That is intended: it is the only way a pass could mean what v1.0's labels implied. `OP-28` remains open.
