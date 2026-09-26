# Root-of-Trust Audit 2026-09

Status: **Research — root-of-trust audit record. It repairs verifiers, validators, and tooling; it changes no core-theory claim and upgrades no assurance dimension.**

Date: 2026-09-25

Audited base: `7fb4816e4aa53aed749b7008b46ba9393d3d29b2` (`main`, merge of PR #535), on branch `claude/far-root-of-trust-audit-nq1kxj`.

Reproduction evidence: [`research/root-of-trust-audit-2026-09/`](../../research/root-of-trust-audit-2026-09/README.md).

## 1. Question and method

The question: does Project FAR do what its specifications, mathematical claims, and acceptance criteria say, once those claims are reconstructed independently of the implementation and its validation machinery? Passing tests, green CI, earlier reviews, and internal consistency were not accepted as evidence.

The audit went roots-first:

1. **Repository-wide validation substrate.** This covers the local JSON Schema validator, the test runner, the health runner, `far_validation`, and the CI workflows.
2. **Core claims.** These are FAR-CORE-001..014 and their Lean statements.
3. **Reference verifiers.** These are `far-ir/2.0` (W3) and `far-ir/2.1` (W5).
4. **Campaign results.** These are W4 and W6, plus the application-layer scoring.

For the verifiers, one path derived expected behavior only from the specifications and theory, without reading implementation or tests. A second path read the implementation. The two were then compared.

Other oracles used:

- upstream `jsonschema` 4.22.0 in an isolated environment;
- hand derivation on small finite cases;
- exact-rational recomputation;
- a deliberately different equality predicate;
- hash-seed variation.

Every detection added or repaired by this audit, and the infrastructure findings listed in §7, was fault-injected in an isolated copy and restored afterwards.

**Environment limits.**

- **Lean toolchain.** The toolchain host was blocked by the network policy, so no Lean proof was compiled locally. Lean results below come either from reading the source or from the repository's CI workflow, as stated case by case.
- **Branch protection.** The live settings on `main` could not be read.

## 2. Dependency map

| Level | Component | What depends on it |
|---|---|---|
| 0 | Local `jsonschema` validator (`jsonschema/`) | Every schema check: far-ir 2.0/2.1, intake, epistemic, registries, the formalization ledger, and the W6 schema-only baseline. |
| 0 | CI gates, test runner, health runner, `far_validation` engine | Every "passes" statement in the repository. |
| 0 | FAR-CORE-001..014 prose and their Lean counterparts (W2) | Theory status; README and project-status assurance text. |
| 1 | `far-ir/2.0` verifier (`contract_v2.py`) and specification | W3 conformance, W4 records, the W6 FAR lane, commercial semantic audit, EFR-R2 frozen expected results. |
| 2 | `far-ir/2.1` verifier (`contract_v21.py`) and specification | W5 recorded result, EFR-R2. |
| 3 | W4 domain records, W6 experiment | Status documents and the W1–W6 claim/evidence matrix. |
| 4 | `far-epistemic/1.0` scoring | Application-layer learning records. |

## 3. Audit ledger

Status vocabulary:

- **ESTABLISHED**: independent evidence supports the claim within the stated assumptions.
- **FALSIFIED**: evidence shows the claim is wrong.
- **BOUNDED**: a narrower proposition is established.
- **INDETERMINATE**: the repository alone cannot decide the claim.

| # | Claim / component | Lvl | Prior basis | Independent oracle | Adversarial checks | Defect | Fix | Residual | Status |
|---|---|---|---|---|---|---|---|---|---|
| R0 | FAR-CORE-001, 002, 003, 004 and 011 hold as stated. | 0 | W1 review; W2 Lean. | Statement-by-statement comparison of Lean with the prose; the Lean kernel in CI run `36149124911`, which compiled every W2 module. | Checked each statement for vacuity, special-casing, and hypotheses that restate the conclusion. | None. The FAR-CORE-002 isomorphism statement does not state commutation with the projections. | — | These are standard results (calibration audit). | ESTABLISHED at the Lean statements |
| R1 | The local `jsonschema` is a Draft 2020-12 validator (it reported upstream version `4.22.0`). | 0 | Tests of implemented keywords; a version-string test. | Upstream `jsonschema` 4.22.0; the JSON Schema 2020-12 and ECMA-262 specs. | Keyword census of 41 schemas; 627-pair differential; probes P3, P5–P7. | It silently ignored `if`/`then`/`else`, `propertyNames`, `anyOf`, `not`, `contains`, `$ref` siblings, and unknown types. Python `$` and `.` semantics were used. | Implemented those keywords, ECMA `$`/`.`, and fail-closed schema checking. Version is now `4.22.0+far.local`. | Pre-audit committed documents: 0 disagreements before and after. The only disagreement is the audit's own ADV-50, where the local validator applies ECMA-262 `$` and upstream python-jsonschema does not. | FALSIFIED → repaired |
| R2 | The far-ir/2.0 verifier certifies an exact observational quotient only for the β-kernel partition (§3.3). | 1 | 4 conformance fixtures; unit tests. | Specification-only oracle (74 records); hand-derived partitions. | P1 and ADV-70 (repeated class ids); ADV-27 (overlap). | Classes were keyed by id: `{a},{b},{c,d}` with ids `k,k,y` was certified **PROVED** exact. An exact partition with a repeated id was rejected. Overlap produced relations from an arbitrary assignment. | Classes are identified by position. Added `DUPLICATE_QUOTIENT_CLASS`. Overlap now yields `QUOTIENT_NOT_PARTITION` and stops. | None known. | FALSIFIED → repaired |
| R3 | The verifier accepts only well-formed JSON. | 1 | None. | RFC 8259. | NaN; duplicate `outcome` keys. | Both records were **PASS**. With duplicate keys, a first-wins parser reads `REFUTED` where the verifier certified `PROVED`. | Strict intake: `UNREADABLE_CONTRACT`. In-memory non-finite numbers: `SCHEMA_CONSTRAINT_VIOLATION`. | The far-ir/2.1 intake remains lenient (see R5 residual). | FALSIFIED → repaired (2.0) |
| R4 | A `FROZEN` record carries an RFC 3339 freeze time (§5). | 1 | A schema `if/then` that was never enforced. | Spec text. | `frozen_at: null`; a non-RFC 3339 string. | Both accepted. | The schema `if/then` is now enforced; added `FREEZE_TIME_INVALID`. | Leap seconds are rejected (conservative). | FALSIFIED → repaired |
| R5 | far-ir/2.1 diagnostics are a normative, deterministic sequence. | 2 | Spec text; sequence tests run under one seed. | `PYTHONHASHSEED` variation. | Probe record under 8 seeds. | `METRIC_LOSS_DOMAIN_MISMATCH` and `LOSS_METRIC_MISMATCH` swapped order in 4 of 8 seeds. Cause: Python set iteration. | First-occurrence order. Output on 4122 audit records is unchanged. | far-ir/2.1 intake still accepts NaN and duplicate keys; its numeric fields are schema-restricted to rational strings. | FALSIFIED → repaired |
| R6 | far-ir/2.1 W5 semantics (metrics, loss, tolerance, Pareto vs least, exact recovery). | 2 | Conformance fixtures; W5 checker. | Specification-only two-route oracle. | 48 adversarial records; 4000 random records. | No semantic defect. The published metric-axiom order was ambiguous: 1211 of 4000 records differed in order only. | The specification now states the interleaved order, checked on 1218 records. | `ZERO_TOLERANCE_EXACT_BOUNDARY_FAILURE` is unreachable (a tautology given the earlier checks). | ESTABLISHED at scope; spec BOUNDED → clarified |
| R7 | The far-ir/2.0 specification determines the reference output (needed by EFR-R2). | 1 | Amendment v1.1. | The specification-only oracle. | Differential comparison. | Canonical JSON, value equality, and pair iteration order were undefined. `DECLARED_UNCHECKED` + `PROVED` passes without saying so. | The specification now defines them. | None known. | BOUNDED → clarified |
| R8 | W6: "blob pins prevent the schema-only and FAR-semantic lanes from silently changing after freeze." | 3 | The checker comment. | Git history. | Validator blob at protocol base `2cecf2e` vs `HEAD`. | The validator that runs the schema-only lane was never pinned and changed 4 times after the freeze. | Corrected the comment. The executed verifier bytes are preserved and W6 recomputes from them. | — | FALSIFIED (claim) |
| R9 | W6 result: schema-only 0/6, FAR audit 6/6, clean 6/6, oracle 12/12. | 3 | W6 checker; table oracle. | Own mutation; exact-rational equality; three validators. | Reproduced under the protocol-base, current, and upstream validators. | None. The result is fixed by construction (as the existing calibration audit states). | — | Not empirical utility. | ESTABLISHED at scope (a conformance result) |
| R10 | W4: six lossy collisions and six repaired factorizations. | 3 | W4 native recomputers. | Hand derivation of all 12 records. | — | None. These are two-case textbook examples. | — | Not open-domain evidence. | ESTABLISHED at scope |
| R11 | FAR-CORE-014 MLL bridge "end to end … without adding a narrative premise". | 0 | Ledger `FORMALIZED`; axiom audit. | Reading the Lean statements. | Compared the theorem types at `FARCoreV11SSS.lean:99` and `:366`. | `bounded_projected_decoder_failure` restated the summary lemma. The witness facts were discarded (`have _`), yet they changed the axiom fingerprint. | Added `summaries_match_mll_witnesses` and `mll_projected_decoder_failure`; corrected the docstring. | Kernel-checked in CI run `36149124911` (§6). | FALSIFIED (wording) → repaired |
| R12 | "14/14 FORMALIZED" means the prose claims are mechanized. | 0 | Formalization ledger; checker. | Reading statements against the prose. | — | Counterparts state less than the prose for 006, 007, 008, 009, 010, 012, 013 (LIM-052). The checker requires all 14 to be `FORMALIZED` and matches declarations by name only (LIM-053). | Recorded. | Label semantics. | BOUNDED |
| R13 | `python tools/run_tests.py` runs every test. | 0 | Runner rejects zero-test runs. | AST scan. | Ran the 38 uncollected functions. | 38 module-level `test_*` functions were never run. One failed: its golden output embedded `/workspace/Project-FAR`. | The runner collects them (`tmp_path` supported, other fixtures fail closed). The golden output is now path-independent. | — | FALSIFIED → repaired |
| R14 | The required merge gate cannot pass when validation fails. | 0 | Protected `merge-authority`. | GitHub documentation on required checks. | Workflow reading. | `merge-authority` `needs:` a job with no `if:`. An upstream failure makes it *skipped*, which counts as passing. | **Not applied** — protected artifact (§5). | LIM-050 | FALSIFIED; open |
| R15 | Validation output cannot be silently altered. | 0 | Assurance lock. | Fault injection. | Engine drops failures (E12); a check is removed from `pr-full` (E13). | The engine base class `engine.py` was unpinned while its subclass was pinned. Dropping a check from `pr-full` was undetected. | Pinned `engine.py`, `__init__.py`, and `diagnostics.py`. Added a profile-completeness test. | Cached local runs (LIM-051). | FALSIFIED → repaired (partly) |
| R16 | `sorry` cannot enter the Lean formalization unnoticed. | 0 | Line-start regex; axiom audit. | Fault injection (E5). | An inline `by sorry` in `FARCore.lean`. | Undetected by every Python check. Plain `lean` exits 0 on `sorry`. | Comment-aware token scan (tested on 12 cases); the W2 workflow now fails on a `sorry` warning. | `lean.yml` is protected (LIM-050). | FALSIFIED → repaired (partly) |
| R17 | `far-epistemic/1.0` Brier and log scoring. | 4 | Unit tests. | `Fraction` and `math.log`. | 40018 cases. | None. | — | — | ESTABLISHED |
| R18 | Generated indexes, inventories, and exports are current. | 0 | Generator `--check` modes. | Regenerated in a clean clone. | — | None. | — | — | ESTABLISHED |
| R19 | A new execution manifest declaring `result: pass` fails closed without FAR-EVIDENCE-CLOSURE-1.0 evidence. | 0 | Closure tests. | Fault injection. | `PASS `, ` pass`, `Passed\t`, and a YAML boolean. | Whitespace variants skipped every PASS check; the investigation index shows the result verbatim. | Result comparison strips whitespace and ignores case; non-string results are rejected. | No closed result vocabulary (LIM-058). | FALSIFIED → repaired |
| R20 | Other JSON intakes (far-ir/1.0 parser, Socratic records, `far-evidence`, commercial package). | 1 | — | RFC 8259; YAML 1.2 (unique keys). | Duplicate keys; `NaN`. | All accepted them last-wins; PyYAML also overwrote duplicate keys. | The far-ir/1.0 JSON and YAML parser, the Socratic loader, and `far-evidence` are now strict. | Commercial package and far-ir/2.1 intake (LIM-057). | FALSIFIED → repaired (partly) |
| R21 | The live `main` branch protection requires `merge-authority` and forbids bypass. | 0 | `configure_validation_protection.py`. | — | — | — | — | GitHub settings were not readable from this session. | INDETERMINATE |
| R22 | Novelty, external empirical utility, external replication. | — | Calibration audit. | — | — | — | — | Needs the external evidence that EFR-001 preregisters. | INDETERMINATE (outside the repository) |

## 4. Repairs and their blast radius

### 4.1 Local JSON Schema validator (R1)

The validator is used for every schema check and ships in the wheel.

- **Before.** Constraints declared in the `far-contract-v2`, `far-contract-v2.1`, `far-epistemic-v1`, `far-source-lineage-v1`, and `far-knowledge-graph-v1` schemas were never enforced. Source-lineage rules are re-enforced separately in Python, so that path was not exploitable.
- **After.** The validator implements every keyword the repository uses and raises at construction on any other keyword. The only repository schema it cannot evaluate is `evaluator-mapping-submission.schema.json` (non-local `$ref`), which is not validated by this validator anywhere.
- **Regression.** `tests/test_local_jsonschema_keyword_coverage.py`, with literal expectations from JSON Schema 2020-12 and ECMA-262. The 18 tests fail 24 times (plus 1 error) against the old validator.

### 4.2 far-ir/2.0 verifier (R2–R4, R7)

`contract_v2.py` now:

- identifies quotient classes by position and rejects repeated ids;
- treats overlap as non-partition;
- rejects non-JSON constants and duplicate keys;
- checks the RFC 3339 freeze time.

Blast radius:

- **Committed records.** No far-ir/2.0 record uses repeated class ids, overlap, NaN, duplicate keys, or a bad freeze time. W3 conformance (4/4), W4 (12 records), and W6 give identical results.
- **Specification and vocabulary.** The specification (§3, §3.3, §5, §9) and `diagnostic_vocabulary.py` publish the new rules.
- **Regression.** `FARContractV2RootOfTrustRegressionTests` in `tests/test_far_contract_v2.py`, with hand-derived sequences. All six tests fail against the old verifier.

### 4.3 far-ir/2.1 verifier (R5, R6)

- **Code.** `contract_v21.py` iterates required-behavior values in first-occurrence order.
- **Specification.** It now states the exact metric-axiom and loss-check order.
- **Regression.** `tests/test_far_contract_v21_determinism.py` runs 6 hash seeds in subprocesses. It fails on 4 of them against the executed verifier.

### 4.4 Frozen campaign inputs (authority conflict resolved explicitly)

W6 (`contract_v2.py`) and W5 (`contract_v21.py`) protected their verifiers by path. As a result, no defect in the canonical verifiers could ever be repaired.

The audit resolved this without rewriting any executed manifest:

1. The executed bytes are preserved byte-for-byte at:
   - `research/results/pca-w6-empirical-audit-utility/frozen-inputs/contract_v2.py` (git blob `31a4c00d`, sha256 `579f9b4d`);
   - `research/results/pca-w5-approximation-and-cost/frozen-inputs/contract_v21.py` (sha256 `a6814bfa`).
2. `tools/campaign_current_state.py` gained **frozen copies**. A frozen copy must match the executed manifest digest, or the check fails closed (`FROZEN_COPY_MISMATCH` or `FROZEN_COPY_MISSING`). A path cannot be both protected and frozen-copied.
3. W5 and W6 recompute from the frozen bytes. Both checkers also fail if the repaired live verifier diverges on any governed item. Fault injection: a tampered copy and a broken live verifier are each detected.
4. The live paths are declared as `verification_tooling` drift in the campaign supplements.

### 4.5 EFR-R2 input amendment (authority conflict)

The v1.1 amendment binds the exact bytes of both specifications. The reference-verifier repairs therefore require a new binding.

- **Candidate.** [`EFR-001-R2-INPUT-AMENDMENT-1.2`](../governance/external-falsification-and-replication-r2-input-amendment-v1.2.md) supersedes only v1.1's bound package. v1.0 and v1.1 are preserved unmodified.
- **Authority.** It becomes authoritative only when promoted to protected `main`.
- **Status.** `EFR-R2` remains `PREREGISTERED_NOT_EXECUTED`.

### 4.6 Validation infrastructure (R13, R15, R16)

- **Test runner.** `tools/run_tests.py` now collects module-level test functions. The suite grew from 1955 to about 2030 tests.
- **Health check.** `tools/repo_health_check.py` fails when a listed checker is missing instead of skipping it.
- **Masked failures.** The release-candidate and maintenance workflows no longer mask failures behind `tee`.
- **Local cache.** `make validate*` bypasses the unsound cache.
- **Profile completeness.** `tests/test_validation_profile_completeness.py` pins which checks the complete profiles may omit. Dropping `research.theorem-target` from `pr-full` now fails.
- **Assurance lock.** It now covers the engine base modules. Tampering with `engine.py` fails the bootstrap.
- **Documentation.** `docs/architecture/validator-assurance-hardening.md` no longer says the Python model checker corroborates the executable engine. It checks a separate abstraction.

### 4.7 Evidence-closure gate and other intakes (R19, R20)

- **Closure gate.** `tools/check_investigation_execution.py` normalizes `result` and rejects non-string values. The same `strict intake` pattern found in the far-ir/2.0 verifier also affected three more loaders:
  - the far-ir/1.0 parser (JSON, and YAML through a unique-key loader);
  - the Socratic-extension loader;
  - the `far-evidence` package reader.

  All three now reject duplicate keys and `NaN`/`Infinity`.
- **Regression.** Tests in `tests/test_investigation_execution_closure.py`, `tests/mechanization/test_parser.py`, `tests/test_socratic_epistemic_extensions.py`, and `tests/test_compare_adjudication.py`. Each fails against the pre-repair code.
- **Unchanged.** The released commercial package and the W5-frozen `far-ir/2.1` intake were left as they are (LIM-057).

## 5. Protected repairs not applied (maintainer action required)

`validation_bootstrap/assurance-lock.json` protects 31 files. A change may not authorize its own repin: authorizations are read only from `validation/test-weakening-waivers.json` in the comparison base. This audit therefore did not change any protected file.

The repairs below need an authorization merged to `main` first, followed by the change itself.

### 5.1 `merge-authority` skip (CRITICAL, LIM-050)

- **Path:** `.github/workflows/validator-assurance.yml`
- **Base sha256:** `02fd5b0e92615a85e8dc0d68a62ba19c440bc0fd47eb761798f6a16afbf498d1`
- **Authorized sha256 after applying exactly this diff:** `48a6ccca94f41dff029e86d65ff41e10b04236c5a7e6527e96f9bdc37cbf0b2b`

```diff
@@ -42,6 +42,7 @@ jobs:
               json.dumps(payload, indent=2, sort_keys=True), encoding='utf-8'
           )
           print(json.dumps(payload, indent=2, sort_keys=True))
+          raise SystemExit(0 if payload['successful'] else 1)
           PY2
       - name: Upload assurance hash audit
         uses: actions/upload-artifact@v4
@@ -129,12 +130,25 @@ jobs:
 
   merge-authority:
     needs: signed-cache-consumer
+    # merge-authority is the required status check. Without this condition a failed dependency
+    # makes it "skipped", which GitHub counts as a passing required check.
+    if: ${{ !cancelled() }}
     runs-on: ubuntu-latest
     timeout-minutes: 60
     env:
       FAR_VALIDATION_CACHE_SIGNING_KEY: ${{ secrets.FAR_VALIDATION_CACHE_SIGNING_KEY || github.token }}
       FAR_VALIDATION_TRUST_DOMAIN: project-far:${{ github.repository }}
     steps:
+      - name: Require every upstream assurance job to have succeeded
+        shell: bash
+        env:
+          UPSTREAM_RESULT: ${{ needs.signed-cache-consumer.result }}
+        run: |
+          set -euo pipefail
+          if [ "$UPSTREAM_RESULT" != "success" ]; then
+            echo "signed-cache-consumer result is '$UPSTREAM_RESULT'; merge authority requires success" >&2
+            exit 1
+          fi
       - uses: actions/checkout@v4
         with:
           fetch-depth: 0
```

The basis is GitHub's "Troubleshooting required status checks": a job that depends on a failed job "is skipped and may not block merging". Its documented remedy is to use `always()` with `needs`, and "successful check statuses are `success`, `skipped`, and `neutral`".

### 5.2 `sorry` gate in `lean.yml` (LIM-050)

Pipe each `lean` invocation through `tee` under `set -o pipefail`. Fail if the output contains `declaration uses 'sorry'`, as `far-core-v11-formalization.yml` now does.

### 5.3 Cache keys (LIM-051)

`far_validation/assured_engine.py::_cache_key` should include a digest of the repository sources a check can import. The conservative option is every tracked `*.py` file and every schema. Until then, only uncached runs are sound.

## 6. FAR-CORE-014 bridge: Lean status

Two theorems were added:

- `FARCoreV11.SSS.MLL.summaries_match_mll_witnesses`: each Boolean summary field agrees with the proved MLL property of its sequent.
- `FARCoreV11.SSS.MLL.mll_projected_decoder_failure`: no uniform monotone decoder applied to the projected profiles predicts `Derivable` correctly for both `sOr` and `sAnd`.

Their proofs use only the existing witness lemmas, `rfl`, and `decide` on closed Boolean facts.

**Kernel status: compiled and axiom-audited in CI.** No local Lean toolchain was available, so the repository's `far-core-v11-formalization.yml` was dispatched on this branch. Run `36149124911`, job `108117638464`, commit `a4c359f2`:

- Lean `v4.19.0` compiled all five W2 modules;
- no `declaration uses 'sorry'` warning was emitted;
- the runtime `#print axioms` output was `[propext, Quot.sound]` for both new theorems, matching the registered contract;
- the exact-axiom check and alignment tests passed.

That was a `workflow_dispatch` run, which does not satisfy a required check on a pull request.

With these theorems, the W2 status wording ("the witness proofs compose with the decoder theorem … without … adding a narrative premise") is true for the first time. The correction note in the W2 status document records that it was not true when first written.

## 7. Fault-injection experiments

| # | Injection | Expected | Observed after repair |
|---|---|---|---|
| F1 | Original local validator under the new keyword tests | fail | 24 failures, 1 error |
| F2 | Original `contract_v2.py` under the new regression tests | fail | 10 failing subtests |
| F3 | Original `contract_v21.py` under the determinism test | fail | seeds 1, 4, 5, 23 fail |
| F4 | Append bytes to the W6 frozen verifier copy | W6 fails | `W6_FROZEN_COPY_MISMATCH` and protocol-base drift |
| F5 | Disable the factorization check in the live verifier | W6 fails | divergence on 6 mutants |
| F6 | `theorem … := by sorry` in `FARCore.lean` | formalization check fails | exit 1 (inventory placeholder count) |
| F7 | Remove `research.theorem-target` from `pr-full` | a test fails | profile-completeness failure |
| F8 | Append bytes to `far_validation/engine.py` | bootstrap fails | `FAR-VAL-BOOT-001` |
| F9 | Stage failing inside `tee` (maintenance workflow logic) | exit ≠ 0 | exit 1, summary still written |
| F10 | Original `check_investigation_execution.py` with `PASS ` / ` pass` / `Passed\t` / `true` | a test fails | 4 failures |
| F11 | Original parser, Socratic loader, and `far-evidence` reader with duplicate keys and `NaN` | tests fail | each fails |

The infrastructure audit also reproduced the pre-repair failures:

- **E4b:** the hash-audit job exited 0 with a corrupted lock;
- **E6:** the `tee` pipeline masked a validator failure;
- **E7:** a stale cached PASS;
- **E8:** `--changed` skipped an affected check;
- **E9:** a vacuous checker was accepted by the structural oracle;
- **E10:** in-body skips passed the weakening detector.

E4b is §5.1. E7 and E8 are LIM-051. E9 and E10 are limits of the oracle and the weakening detector, recorded here.

## 8. Authority conflicts surfaced

1. **Frozen verifiers vs. defect repair.** Resolved by §4.4. The executed bytes remain verified; no manifest was rewritten.
2. **EFR-R2 v1.1 binding vs. corrected specifications.** Resolved by the candidate amendment v1.2. It is not authoritative until promoted.
3. **Independent-review status.** `theory/theorems/Project-FAR-Theory-Closure-v1.1.md` says "not independently reviewed". The later W1 records report a sealed I1 claimed-isolation review. This is surfaced, not rewritten: the theory document predates W1, and editing governing theory text is outside this audit.

## 9. Assurance vocabulary

Findings where the evidence does not support the exact word:

| Wording | Location | Finding |
|---|---|---|
| "end to end", "without adding a narrative premise" (FAR-CORE-014) | project status; W2 status | False as originally written; true since the §6 bridge theorems compiled. A dated correction is recorded in the W2 status document. |
| "prevents … lanes from silently changing after freeze" | W6 checker | False; corrected. |
| `machine_oracle_independent_of_far_verifier: true` | W6 results (protected) | Procedurally independent only. It shares canonical-JSON equality and table parsing. Independent reproduction with a different equality agrees. |
| "corroborates the executable state-machine design" | validator-assurance doc | The model checker never executes the engine; corrected. |
| `14/14 FORMALIZED`; `kernel_check: PASS` | — | Bounded by LIM-052 and LIM-053. |
| "Theory-closure validation"; `make semantic-check` | — | Mostly status and consistency checks, with asserted regression literals. They do not re-prove theory. |

## 10. Final validation

The run used a fresh clone of commit `772a9f7c`, the last commit that changes code or data. Everything after it changes only this report. All of the following exited 0:

- `python tools/run_tests.py` — 2031 tests;
- `make health`, `make research-check`, `make semantic-check`, `make docs-check`, `make links-check`;
- `make pca-w5-check` and `make pca-w6-check`;
- `python validation_bootstrap/verify.py` — 34 assurance files;
- `python -m far_validation weakening --base origin/main`;
- `python -m far_validation validate --profile pr-full --no-cache`;
- `oracle_far_ir_2_0/run_all.py`.

The reproduction scripts gave these results:

- `scripts/compare_verifiers.py` over 4000 regenerated random records: `PASS`, with 0 verdict and 0 multiset differences.
- `scripts/schema_differential.py`: 750 pairs and one disagreement, ADV-50, which is intended; see its header.

Lean was checked separately in CI run `36149124911` (§6).

## 11. What this audit does not establish

- It does not establish novelty, empirical utility, or external validity.
- It does not show the repaired verifiers are correct beyond the audited defects.
- It does not re-derive Lean kernel acceptance locally. The new theorems were checked only through the repository's CI workflow.
- It does not supply the live branch-protection settings.

The oracles are Project-FAR-internal, and their agreement is not external replication.
