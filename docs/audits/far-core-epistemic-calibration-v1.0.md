# FAR Core Epistemic Calibration Audit v1.0

Status: **Research — calibration audit; no theory mutation**

Date: 2026-09-06

Target: current `PROJECT-FAR-CORE-THEORY-1.1`, W1–W6 assurance surfaces, and EFR-001 boundaries.

## Purpose

This audit calibrates what Project FAR has actually established, distinguishes mathematical correctness from mathematical novelty and practical utility, and prevents flat assurance labels from implying more than their underlying evidence.

It does **not** alter any FAR-CORE statement, reopen the terminal kernel, execute EFR-001, claim novelty, or convert internal evidence into I3 external evidence.

## Corrected overall assessment

- **Mathematical correctness:** strong at the governed scopes. No reproducible contradiction to FAR-CORE-001–014 is established here.
- **Mechanization:** real and kernel-checked, but heterogeneous in mathematical depth. `FORMALIZED` is a mechanization-status label, not a difficulty or novelty score.
- **Foundational mathematical novelty:** not established and likely limited because many core constructions instantiate standard mathematical patterns.
- **Integrated methodology novelty:** unresolved. Existing component prior art does not by itself decide whether the full FAR audit discipline is anticipated in combination.
- **Independent assurance:** W1 remains I1 claimed isolation; I2 and I3 are not established.
- **External empirical utility:** unestablished. W6 is a bounded internally authored semantic-detection/conformance result.
- **Commercial value:** unestablished and depends on external utility, burden, adoption, and differentiation evidence.

The most defensible present description is:

> Project FAR is a rigorously engineered contract-relative audit and representation methodology whose core mathematics is largely composed of standard or elementary structures, while the value and novelty of the integrated audit discipline remain external empirical and prior-art questions.

## 1. Mechanization-depth calibration

`14/14 FORMALIZED` is accurate only as a statement that all fourteen governed claims have Lean counterparts passing the registered kernel checks. It must not be read as `14 deep new theorems` or `14 independent discoveries`.

| Claim | Mechanization-depth class | Calibration |
|---|---|---|
| FAR-CORE-001 | definition + elementary kernel lemma | Exact sufficiency is defined by factorization on `rho[X]`; the substantive result is equivalence with kernel inclusion and the collision criterion. |
| FAR-CORE-002 | standard quotient / universal-property theorem | Canonical quotient, unique image-to-quotient factor, least-informative kernel equality, finite cardinal consequence. |
| FAR-CORE-003 | standard congruence/context-closure result | Declared continuation closure makes observational equivalence action-compatible. |
| FAR-CORE-004 | elementary incompatibility construction | Constant and injective contracts induce incompatible minima on any nontrivial domain. |
| FAR-CORE-005 | elementary monotonicity | Invariance under a larger admitted transformation class implies invariance under every subclass. |
| FAR-CORE-006 | standard transport-of-structure construction | Injection gives equivalence with the reachable image; source operations/relations can be transported. |
| FAR-CORE-007 | constructed semantic recovery + declared-count witness | Reification recovers the relation; unequal manually declared vocabulary profiles witness noninvariance. The current Lean code does not compute vocabulary count from a typed presentation syntax. |
| FAR-CORE-008 | standard tagged-sum/dispatcher encoding + declared-count witness | Split/combine recovery is proved; the primitive-count comparison uses declared presentation counts rather than a syntax-derived counting function. |
| FAR-CORE-009 | elementary finite-sample underdetermination | Two completions agree on the finite panel and disagree off-panel. |
| FAR-CORE-010 | definition/dependency statement + residue-change theorem | Frame-independence of exact common theory is definitional once `Gamma` is excluded from `T`; the companion theorem proves frame-relative residue can change. |
| FAR-CORE-011 | direct corollary of collision criterion | Omitting an active consequence-changing parameter produces an insufficiency witness. |
| FAR-CORE-012 | direct corollary of exact sufficiency | If the contract distinguishes `absent` from `unknown`, a sufficient representation cannot collapse them. |
| FAR-CORE-013 | project-specific definitional elimination | Canonical FARA Omega is a materialized view of classifications under the governed definition. |
| FAR-CORE-014 | bounded application / witness bridge | Search-State Sufficiency is a scoped factorization instance with a formalized bounded MLL witness surface, not a universal architecture theorem. |

This table changes no proof status. It adds a separate dimension: **what kind of mathematical work the formalization represents**.

## 2. Prior-art normalization

This is an internal normalization, not EFR-N1 and not a novelty adjudication. It records known antecedent families so later publications and product claims do not accidentally treat standard components as original discoveries.

### Strong antecedent families

1. **Blackwell comparison of experiments.** Blackwell's comparison supplies decision-class-relative informativeness ordering and is already acknowledged by v1.1 as strong prior art. Primary reference: David Blackwell, “Equivalent Comparisons of Experiments,” *Annals of Mathematical Statistics* 24(2), 1953, 265–272, DOI `10.1214/aoms/1177729032`.
2. **Minimal sufficient statistics.** The standard notion of a minimal sufficient statistic is a coarsest sufficient reduction, expressible as a function of every other sufficient statistic. This is a direct antecedent family for contract-relative least-information reductions, although FAR's set-based behavior map is more general than classical statistical likelihood formulations.
3. **Myhill–Nerode and automata minimization.** Continuation indistinguishability induces an equivalence relation whose quotient yields a minimal automaton unique up to isomorphism. Primary historical anchor: Anil Nerode, “Linear Automaton Transformations,” *Proceedings of the AMS* 9(4), 1958, 541–544, DOI `10.1090/S0002-9939-1958-0135681-9`.
4. **Behavioral equivalence / coalgebraic minimization.** Modern coalgebraic minimization generalizes behavioral equivalence and quotient/minimization constructions across state-based systems. Example: Bezhanishvili et al., “Coalgebraic Minimization of Automata by Initiality and Finality,” *ENTCS* 325, 2016, 253–276, DOI `10.1016/j.entcs.2016.09.042`.
5. **Abstract interpretation.** Abstraction, information preservation/loss, and best abstractions relative to semantics have deep prior art. Primary anchor: Patrick Cousot and Radhia Cousot, “Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints,” POPL 1977, 238–252, DOI `10.1145/512950.512973`.
6. **Elementary set/model-theoretic constructions.** Quotients by kernels, transport of structure, signature reification, tagged sums, finite-extension countermodels, and intersection-of-theories constructions are standard mathematical devices rather than plausible standalone novelty claims.

### FAR-CORE normalization matrix

| Claim | Prior-art / conventional antecedent class | Residual Project FAR delta currently defensible |
|---|---|---|
| 001 | factorization, sufficient reduction, kernel inclusion | explicit contract schema and collision-as-audit rule across heterogeneous domains |
| 002 | quotient by observational equivalence; minimal sufficient reduction; automata minimization | one contract-relative presentation and audit vocabulary spanning multiple domains |
| 003 | congruence/contextual equivalence/right congruence | explicit requirement that continuation closure be declared in the audit contract |
| 004 | elementary consequence of contract variation | boundary theorem used to reject contract-free minimal-architecture claims |
| 005 | elementary subgroup/subclass monotonicity of invariance | governance use: force declaration of admitted re-representation class |
| 006 | transport of structure along embeddings/isomorphisms | audit warning that encodability is host capacity, not evidence of native common structure |
| 007 | relation reification / change of signature | explicit counterexample against primitive-count invariance in the FAR architecture debate |
| 008 | tagged coproduct/dispatcher encoding | explicit counterexample against fixed operator-count invariance |
| 009 | finite-sample underdetermination | formal governance prohibition on promoting finite heterogeneous panels to open-domain universality |
| 010 | common theory as intersection; frame-relative subtraction | explicit separation of `T_{L,J,I}` from `Gamma`-relative residue in cross-system comparison |
| 011 | hidden-variable / omitted-parameter collision | typed contract-lint rule and reproducible insufficiency witness |
| 012 | preservation of observable distinctions | first-class typed `Unknown`/absence audit rule |
| 013 | definitional/materialized-view elimination | correction of a specific Project FAR architectural overclaim about Omega |
| 014 | application of factorization criterion | bounded SSS/MLL bridge and its exact implementation/evidence package |

No row in this matrix establishes priority or non-novelty by itself. It establishes only that **component novelty must not be presumed**.

## 3. W1 calibration

The W1 campaign has a documented sealed protocol and deterministic evidence. Therefore `no method` is an incorrect criticism.

The correct limitation is stronger and narrower: W1's exposure record supports **I1 claimed isolation only**. Repository access was prohibited by instruction but not technically prevented, and the reviewer was not an externally controlled I3 replication team. W1 is therefore internal assurance evidence, not external independent validation.

## 4. W6 calibration

W6 is correctly bounded in its detailed documents but its historical workstream name can be misread.

The evidence class should be described as:

> **bounded internal controlled-artifact semantic-detection conformance**

The registered mutation directly targets the finite factorization condition the verifier is designed to check. The result verifies the implementation path and demonstrates detection power over JSON-Schema-only validation for that exact corpus and defect class. It does not estimate real-world sensitivity/specificity, human-review benefit, superiority, open-domain performance, or commercial value.

The historical identifier `PCA-W6-EMPIRICAL-AUDIT-UTILITY` remains immutable provenance and is not renamed retroactively.

## 5. EFR calibration

EFR-001 should remain the governed successor. Prior-art normalization is not a replacement for replication because novelty and correctness/utility are orthogonal dimensions.

The highest-information ordering for external resource expenditure is:

1. `EFR-R1` independent deductive replication;
2. `EFR-R2` independent technical reimplementation;
3. `EFR-A1` adversarial counterexamples;
4. `EFR-N1` independent bounded prior-art falsification;
5. only then high-cost human/site components `HD1`, `U1`, and `C1`, unless an external partner can execute them earlier without compromising the freeze.

This ordering is a resource-prioritization recommendation only. It does not change the registered EFR decision rule or authorize skipping any component.

## 6. Product and publication consequence

Until external evidence changes the state, Project FAR must not be marketed or published as newly discovered foundational mathematics of reasoning.

The strongest currently supportable product thesis is narrower:

> FAR may be valuable as an executable, scope-explicit audit discipline that turns semantic preservation claims into inspectable contracts, collision witnesses, provenance, typed failure reports, and assurance traces.

Product work should therefore test whether this integrated workflow catches costly defects, reduces disagreement, or improves audit quality enough to justify its burden. Mathematical correctness alone is not product-market evidence.

## 7. Archive reproducibility defect

The theory-dependency audit currently reads frozen source blobs from historical Git commit `5e8f27b617632a76e76760779dcbb24dedbb6786`. In a source archive without `.git` metadata and without an `origin`, `read_base_blob()` cannot reconstruct those inputs. This is a genuine reproducibility defect in that historical audit harness, not a theorem defect and not an EFR packet defect.

The permanent repair is to make the nine source-locked historical blobs self-contained in the current tree, verify each vendored byte sequence against the recorded Git blob SHA, prefer Git history when available, and fall back to the vendored exact bytes when history is unavailable. A regression test must execute the audit from a git-less copied tree and require equality with the committed result.

## Disposition

- Core theory: **unchanged**.
- W1 truth verdicts: **unchanged**; independence remains I1.
- W2 formalization statuses: **unchanged**; depth is now explicitly separated from mechanization status.
- W6 result: **unchanged**; evidence class should be labeled controlled semantic-detection conformance wherever summarized.
- EFR-001: **unchanged and not executed**.
- Novelty: **unestablished**.
- External utility: **unestablished**.
- Commercial value: **unestablished**.
