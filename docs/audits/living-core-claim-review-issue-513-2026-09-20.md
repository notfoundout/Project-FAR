# Living core-claim review — issue #513 — 2026-09-20

Status: **Governed internal literature review — no FAR-CORE or EFR status change**

Issue: #513 (`Living repository: core-claim review queue`)

Reviewed source snapshot: permanent living-research inbox PR #490, head `2a2610f98c749e2836d23028f8e1aa8e2707f6e5`.

Scope note (2026-09-22): issue #513 is a live queue. Candidate `FAR-LIT-DD283139285EDBA1` was first seen on 2026-09-21, after the reviewed snapshot above, and is outside this audit. This audit resolves only the seven candidates present in the recorded snapshot; later queue entries require separate governed review. A later queue arrival does not invalidate or enlarge this frozen review snapshot.

## Governing question and contradiction threshold

The queue is controlled by `FAR-RQ-009`:

> After the completed independent W1 review, does any later evidence produce a reproducible contradiction to an exact FAR-CORE premise, proof step, or theorem?

The registered falsifier criterion is stricter than title- or topic-level similarity: a qualifying challenge must supply a minimized, reproducible counterexample satisfying the exact canonical premises and negating the exact conclusion. A paper using words such as *counterexample*, *representation*, *sufficient*, *equivalence*, *contract*, or *abstraction* is not a contradiction unless its result actually instantiates the governed FAR statement at the stated v1.1 scope.

The canonical comparison target is `PROJECT-FAR-CORE-THEORY-1.1`. In particular:

- `FAR-CORE-001`: for an exact contract, sufficiency is equivalent to factorization of required behavior through the representation;
- `FAR-CORE-002`: the fixed-contract observational quotient is the unique least-informative exact representation up to isomorphism;
- `FAR-CORE-003`: under declared action/test closure, observational equivalence is action-compatible;
- `FAR-CORE-004`: no single representation is least-informative sufficient for every varying observation contract on a nontrivial domain;
- `FAR-CORE-005`–`014`: retain their exact canonical scopes and are not reopened by merely related abstraction, regularity, equivalence, or counterexample results.

For each candidate below, review therefore asked the strongest adversarial question available from the source: can its actual theorem/example be encoded as a witness satisfying a FAR claim's premises while falsifying that claim's conclusion? If not, the candidate does not reopen FAR-CORE.

## Primary-source verification and dispositions

### `FAR-LIT-55D89C727719FCBF`

Source: Matthew S. Leibel, *A Stability Contract for Scalable Hybrid Computing: Minimal Sufficient Control of Component-Observable Hardware*, Preprints.org v1, DOI `10.20944/preprints202609.1101.v1`, posted 2026-09-15.

Primary source checked: https://www.preprints.org/manuscript/202609.1101

Source result: the paper defines a hardware stability/control obligation for analog/wave/hybrid computing. Under independent Gaussian drift it derives information/feedback scaling requirements, distinguishes acquisition depth from information rate and traffic, gives a projected heavy-ball control law for the declared monitor class, and states a routing-closure scaling condition. Its phrase *minimal sufficient control* concerns hardware maintenance resources under that model.

Adversarial FAR reconstruction: the paper does not provide a Set-based exact contract `(X, behavior/tests, representation, decoder)` in which a representation is sufficient without behavior factorization, nor does it construct an observational-equivalence quotient that fails least-informativeness or uniqueness. It does not claim a single representation is least-informative across every observation contract. Its resource lower bounds are model- and hardware-class-relative, not countermodels to the canonical quotient theorem. The paper is potentially useful downstream as a domain-specific example of explicit contract and resource assumptions, especially for `FAR-RQ-003`/W5, but that is application evidence, not a core contradiction.

Disposition: `ADJACENT_NO_CONTRADICTION`.

### `FAR-LIT-5B2A64208C5F9673`

Source: Edmund M. Clarke, *Counterexample-Guided Abstraction Refinement*, TIME 2003, DOI `10.1109/TIME.2003.1214874`.

Primary full text checked: https://www.cs.cmu.edu/~emc/papers/Conference%20Papers/Counterexample-guided%20Abstraction%20Refinement.pdf

Source result: the paper constructs an abstract model as an upper approximation of the concrete transition system for symbolic model checking. Satisfaction of the supported property in the abstract model transfers to the concrete model, while an abstract counterexample can be spurious because the abstraction admits behavior absent from the concrete system. The algorithm checks an abstract counterexample against the concrete model and, when it is spurious, refines the abstraction by splitting abstract state classes so the offending behavior is eliminated. For the counterexample forms treated by the paper, the refinement argument terminates with either a real counterexample or a model precise enough to verify the property.

Adversarial FAR reconstruction: CEGAR's coarse abstractions are intentionally over-approximating rather than exact representations of all concrete behavior relevant to the checked property. When omitted distinctions create a spurious result, the method restores distinctions by refinement. The paper therefore does not exhibit an exact representation that omits consequence-affecting distinctions while remaining exact, a representation strictly less informative than FAR's fixed-contract observational quotient while preserving the same exact contract, or an action/test-closed observational relation that violates FAR's compatibility premise. Its preservation and refinement results are strong adjacent prior art for abstraction, property-relative precision, and representation repair, but they do not instantiate a countermodel to `FAR-CORE-001`, `FAR-CORE-002`, `FAR-CORE-003`, or the remaining FAR-CORE claims under their stated premises.

Disposition: `ADJACENT_NO_CONTRADICTION`.

### `FAR-LIT-5E19D1DEF57C7EAB`

Source: Simranjeet Singh Bilkhu and Noah Mills Forman, *Counter-example to continuity of measure in uncountable unions*, arXiv `2509.07168` / later *Examples and Counterexamples* record DOI `10.1016/j.exco.2026.100231`.

Primary preprint record checked: https://arxiv.org/abs/2509.07168

Source result: the paper concerns continuity of measure. It constructs counterexamples when the usual countable increasing-union statement is extended to uncountable unions, including an ordinal construction and, under the continuum hypothesis, examples on the reals.

Adversarial FAR reconstruction: this result does not instantiate FAR's representation, behavior-factorization, observational-equivalence, action-closure, invariance, Unknown, or bounded Search-State premises. Its `counterexample` is to an uncountable-union generalization in measure theory, not to any FAR-CORE statement.

Disposition: `IRRELEVANT_FALSE_POSITIVE`.

### `FAR-LIT-89948AB45C87260F`

Source: Mariano Giaquinta, *Growth conditions and regularity, a counterexample*, *Manuscripta Mathematica* 59 (1987), DOI `10.1007/BF01158049`.

Primary institutional source record and abstract checked: https://ricerca.sns.it/handle/11384/116

Source result: the institutional abstract states that the paper shows the relevant growth conditions are necessary for local regularity of minimizers; the record identifies the result as a variational/PDE regularity counterexample.

Adversarial FAR reconstruction: the candidate's stated theorem/result is wholly in variational/PDE regularity. The inspected primary material does not instantiate a FAR observation contract, exact representation relation, quotient construction, or behavior-factorization witness. The disposition rests on that subject-and-premise mismatch; it does not assert an exhaustive inventory of uninspected full-text results.

Disposition: `IRRELEVANT_FALSE_POSITIVE`.

### `FAR-LIT-A2D5163E82DFF6CA`

Source: Francisco Santos, *A counterexample to the Hirsch Conjecture*, *Annals of Mathematics* 176(1) (2012), DOI `10.4007/annals.2012.176.1.7`.

Primary journal record checked: https://annals.math.princeton.edu/2012/176-1/p07

Source result: Santos constructs a 43-dimensional polytope with 86 facets whose graph diameter violates the Hirsch bound `n-d`, thereby refuting the Hirsch Conjecture.

Adversarial FAR reconstruction: the counterexample concerns polytope graph diameter. It neither instantiates nor negates any contract-relative factorization, observational quotient, invariance, action-closure, Unknown-preservation, or bounded Search-State statement in FAR-CORE.

Disposition: `IRRELEVANT_FALSE_POSITIVE`.

### `FAR-LIT-EF65407251DCB42E`

Source: Patricia Bauman, *Equivalence of the Green's functions for diffusion operators in R^n: a counterexample*, *Proceedings of the American Mathematical Society* 91(1) (1984), DOI `10.1090/S0002-9939-1984-0735565-4`.

Primary publication identity was cross-checked against the DOI/journal record, and an author-uploaded copy of the article was inspected.

Source result: Bauman constructs a second-order uniformly elliptic diffusion operator with continuous coefficients for which a previously available Green-function equivalence/proportionality result does not extend from divergence-form operators; the example can produce a Green's function locally unbounded away from the pole.

Adversarial FAR reconstruction: `equivalence` here is analytic equivalence/proportionality of Green's functions for elliptic operators. It is not FAR's behavioral observational-equivalence relation induced by a fixed exact contract. The inspected article supplies no witness satisfying any FAR-CORE theorem's premises while negating its conclusion.

Disposition: `IRRELEVANT_FALSE_POSITIVE`.

### `FAR-LIT-F5985F3AEC6A66D8`

Source: Gianluca Barbon, *Debugging of Behavioural Models using Counterexample Analysis*, dissertation record DOI `10.70675/b5b35f21z02ffz4568z9d93z2e0068cc54e5`; closely corresponding published work by Barbon, Vincent Leroy, and Gwen Salaün, *IEEE Transactions on Software Engineering* 47(6), DOI `10.1109/TSE.2019.2915303`.

The exact dissertation identity and research-group full-text listing were checked through the CONVECS/Inria publication archive (PhD thesis, Université Grenoble Alpes, December 2018). The corresponding IEEE/HAL work (`hal-02145610`) was used only as corroboration for the counterexample-analysis method, not as a substitute for the dissertation's identity.

Source result: the work improves model-checking debugging by analysing counterexamples in behavioural models, identifying actions near transitions between erroneous and correct behavior, and abstracting/simplifying counterexamples to expose likely bug sources.

Adversarial FAR reconstruction: the work is adjacent to behavioral modelling, abstraction, and counterexample analysis, but the inspected primary/corroborating material does not state a general sufficiency theorem or observational-quotient minimality theorem. Its counterexamples are model-checker traces witnessing violation of temporal properties. No reviewed result provides an exact FAR contract in which factorization fails despite sufficiency, a smaller exact representation than the observational quotient, or a countermodel to FAR-CORE-003–014.

Disposition: `ADJACENT_NO_CONTRADICTION`.

## Claim-by-claim attack result

No candidate in the reviewed snapshot supplies the minimum witness needed to reopen any of the 14 claims:

- `FAR-CORE-001`: no exact-sufficiency/non-factorization witness.
- `FAR-CORE-002`: no exact representation strictly less informative than the observational quotient, and no non-isomorphic competing least element under the same contract.
- `FAR-CORE-003`: no declared action/test-closed observational relation that fails compatibility.
- `FAR-CORE-004`: no single representation proved least-informative sufficient across every varying observation contract on the governed nontrivial domain.
- `FAR-CORE-005`–`010`: no counterexample to the stated invariance, encoding, vocabulary/operator-count, finite-panel, or indexed-common-theory statements.
- `FAR-CORE-011`: no representation shown exact after omitting a parameter that changes required consequences. CEGAR is directionally consistent with the need to refine abstractions when omitted distinctions matter.
- `FAR-CORE-012`: no contradiction involving determinate absence versus `Unknown`.
- `FAR-CORE-013`: no argument that canonical FARA `Ω` is semantically non-eliminable.
- `FAR-CORE-014`: no result about the bounded PR #453 Search-State Sufficiency representation/decoder classes.

## Replication and adjudication

Issue #513 requires the path `verify primary source → reconstruct exact premises/conclusion → attack → replicate → adjudicate`. The dispositions above were therefore re-run in a second internal contradiction pass against the canonical claim scopes rather than accepted from discovery keywords, titles, or the first-pass wording. This replication is an internal repeatability check only; it is not external independence, EFR execution, or evidence that could satisfy any EFR replication requirement.

The replication pass used the following fail-closed witness tests:

- for `FAR-CORE-001`, require an exact fixed-contract representation that is sufficient while the required behavior does not factor through it;
- for `FAR-CORE-002`, require an exact representation strictly less informative than the canonical fixed-contract observational quotient, or a non-isomorphic competing least element under the same contract;
- for `FAR-CORE-003`, require the stated action/test-closure premises together with a failure of action compatibility;
- for `FAR-CORE-004`, require one representation proved least-informative sufficient across every varying observation contract on the governed nontrivial domain;
- for `FAR-CORE-005`–`014`, require a witness satisfying the exact registered premises of the attacked claim and negating its exact conclusion.

Where the inspected primary material itself identifies a theorem family that is plainly outside FAR's governed premises (for example, continuity of measure, variational/PDE regularity, or the Hirsch bound), the replicated screen is limited to rejecting the `FAR-RQ-009` candidate relation on that demonstrated premise mismatch. It does not convert a record/abstract-level inspection into a claim of exhaustive full-text analysis.

| Candidate | Replicated premise-match result | Adjudication |
|---|---|---|
| `FAR-LIT-55D89C727719FCBF` | No qualifying FAR-CORE witness; result remains hardware/control-resource scoped. | `ADJACENT_NO_CONTRADICTION` |
| `FAR-LIT-5B2A64208C5F9673` | No qualifying FAR-CORE witness; CEGAR abstraction/refinement is intentionally over-approximating until refined, not an exact-contract countermodel. | `ADJACENT_NO_CONTRADICTION` |
| `FAR-LIT-5E19D1DEF57C7EAB` | No qualifying FAR-CORE witness; counterexample is to uncountable-union continuity of measure. | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-89948AB45C87260F` | No qualifying FAR-CORE witness; counterexample is a variational/PDE regularity result. | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-A2D5163E82DFF6CA` | No qualifying FAR-CORE witness; counterexample is to the Hirsch graph-diameter bound. | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-EF65407251DCB42E` | No qualifying FAR-CORE witness; equivalence concerns Green's functions of elliptic operators. | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-F5985F3AEC6A66D8` | No qualifying FAR-CORE witness; counterexamples are model-checker traces used for debugging/abstraction. | `ADJACENT_NO_CONTRADICTION` |

Adjudication result: the second pass reproduces all seven first-pass dispositions and finds zero surviving exact-claim contradiction witnesses. Because no consequential contradiction survives premise matching, there is no result to advance into the living lifecycle's `REPLICATION_REQUIRED` / `ACCEPTANCE_READY` correction path. The seven rows remain review/queue memory only: they suppress repeated metadata-only review, preserve the raw candidate records, and confer no claim, theorem, novelty, EFR, external-independence, or promotion status.

## Final disposition set

| Candidate | Disposition |
|---|---|
| `FAR-LIT-55D89C727719FCBF` | `ADJACENT_NO_CONTRADICTION` |
| `FAR-LIT-5B2A64208C5F9673` | `ADJACENT_NO_CONTRADICTION` |
| `FAR-LIT-5E19D1DEF57C7EAB` | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-89948AB45C87260F` | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-A2D5163E82DFF6CA` | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-EF65407251DCB42E` | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-F5985F3AEC6A66D8` | `ADJACENT_NO_CONTRADICTION` |

`PROJECT_CHANGE_REQUIRED`: **0**.

`N1_PRIOR_ART_LEAD`: **0**. The Leibel paper postdates the frozen EFR-N1 cutoff of 2026-09-05, and the two formal-methods candidates are useful adjacent background but do not by this review establish the integrated four-element N1 arrangement or any novelty disposition.

## Result and limits

All seven candidates in the reviewed #513/#490 snapshot have now received a governed internal disposition sufficient to remove those seven records from the metadata-only core-claim review queue. The raw living-research candidate records remain preserved. Issue #513 remains open because the living queue has received at least one later candidate outside this snapshot. No FAR-CORE statement, proof, premise, theorem status, EFR input, EFR result, novelty status, or external-independence status changes.

This audit is an internal contradiction review, not EFR-R1/R2/N1 execution. It does not substitute for the independently controlled external program.
