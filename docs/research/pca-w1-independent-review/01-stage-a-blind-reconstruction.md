# PCA-W1 Stage A — blind reconstruction ledger

Status: **STAGE A RECORDED; MACHINE LEDGER NOT YET READ**

Reviewer: OpenAI Codex agent (GPT-5-family identity exposed by the environment)

Review target: `14105775daf3c5713b134a728db2e1e53673af97`

## 1. Access boundary and integrity

At the time this record was frozen, repository content consulted was limited to:

1. the independent-review protocol;
2. the pinned v1.1 governing monograph; and
3. the permitted post-closure assurance rules, used only as procedure.

I had not read the machine ledger, v1.0, any audit or acceptance record, any PR material, any repository test or fixture, any prior internal research, or any earlier conclusion.

The Git data endpoint for the asserted target returned commit `14105775daf3c5713b134a728db2e1e53673af97` with tree `68f058199b7c94b707fd5fe978f1ef59d695ab00`. Its metadata response unavoidably also exposed the commit subject, author, parents, and the fact that it was a merge referring to PR #457 and a W1 correction. I did not open any parent, diff, PR, or history. The existence of that correction was already disclosed by the protocol and monograph, so this metadata added no theorem, defect, proof, or verdict content.

The exact UTF-8 bytes returned for the pinned monograph (with no extra trailing LF introduced by the local patch utility) hash to:

`91513dce21273364ef8ad24ebd1102e3b5957b513bbd5bc429f2b10917fa8239`

This matches the protocol. Integrity establishes the object reviewed, not its truth.

## 2. Reconstruction basis

The v1.1 monograph gives exact statements and proofs only for the corrected claims provisionally associated with `FAR-CORE-004` and `FAR-CORE-010`. For most other claims it says that v1.1 incorporates a prohibited historical document and provides only a short terminal-kernel description. Consequently, the reconstructions below are independent formalizations of those kernel descriptions. They are not silently treated as exact ledger wording. Claim-number allocation other than 004 and 010 is provisional until Stage B.

### 2.1 Common set-theoretic model

Let:

- `X` be a set of cases;
- `C` be an exact observation contract;
- `B_C` be the typed behavior space induced by the declared tests, contexts, outcomes, and semantics of `C`;
- `β_C : X → B_C` be the complete declared behavior map;
- `r : X → R` be a representation; and
- `im(r)` be its reachable image.

Define

`ker(f) = {(x,y) ∈ X×X | f(x)=f(y)}`.

The image-level definition of exact sufficiency is:

`r` is sufficient for `C` iff there exists `d : im(r) → B_C` such that `β_C = d ∘ r`.

Using `im(r)` is material. If a decoder is required on all of an arbitrary codomain `R`, kernel inclusion alone does not always provide an extension (for example, `X=∅`, `R≠∅`, and `B_C=∅`). Nothing observational depends on unreachable elements of `R`, so all minimality and uniqueness statements below are image-relative unless an inhabited-codomain extension premise is declared.

Say `r` is at least as informative as `s` when `s=h∘r` for some image-level map `h`; equivalently, for maps on the same `X`, `ker(r)⊆ker(s)`. Thus a least-informative sufficient representation has the largest kernel compatible with sufficiency.

## 3. Claim reconstructions and hostile checks

### FAR-CORE-001 — exact sufficiency/factorization (provisional allocation)

**Reconstructed proposition.** For all sets `X`, exact behavior maps `β:X→B`, and representations `r:X→R`, the following are equivalent:

1. `β` factors through `r` on `im(r)`;
2. `ker(r)⊆ker(β)`; and
3. every representation collision is behaviorally harmless: `r(x)=r(y) ⇒ β(x)=β(y)`.

**Proof reconstruction.** If `β=d∘r`, equality under `r` implies equality under `β`, so (1) implies (2). If (2) holds, define `d(r(x))=β(x)`. Kernel inclusion makes this well-defined, and it gives the factorization. Conditions (2) and (3) are identical after expanding the kernel definition.

**Quantifiers and premises.** Universal over sets and maps. No finiteness, probability, computability, or injectivity premise is needed. Exact equality is essential; approximate sufficiency requires a metric/loss/tolerance and is a different theorem.

**Strongest hostile attempt.** Requiring `d:R→B` rather than `d:im(r)→B` breaks the reverse implication in the empty-domain/empty-behavior example above. Requiring an effective decoder also breaks the bare set-theoretic result unless computability premises are added. Neither objection affects the image-level exact theorem.

**Dependencies.** Definitions only.

**Falsifier/reopening condition.** A pair with equal representation and unequal declared behavior refutes sufficiency; a claimed general factorization without a well-defined decoder refutes the proof.

### FAR-CORE-002 — canonical observational quotient (provisional allocation)

**Reconstructed proposition.** For fixed `β:X→B`, define `x~β y` iff `β(x)=β(y)` and let `qβ:X→Qβ=X/~β` be the quotient map. Then:

1. `qβ` is sufficient for `β`;
2. every sufficient `r` is at least as informative as `qβ`, because a unique image-level map `h:im(r)→Qβ` satisfies `qβ=h∘r`; and
3. every image-surjective least-informative sufficient representation is isomorphic to `qβ`.

**Proof reconstruction.** Define `d([x])=β(x)`; this is well-defined by the quotient relation. If `r` is sufficient, `ker(r)⊆ker(β)`, so `h(r(x))=[x]` is well-defined and unique on `im(r)`. A least-informative sufficient `r` must have `ker(r)=ker(β)`; equal kernels induce a unique bijection between their images commuting with the quotient maps.

**Quantifiers and premises.** Universal over exact set-valued behavior maps. “Unique” means up to isomorphism of reachable images. It is not literal uniqueness of labels or arbitrary codomains.

**Hostile tests.** Empty `X` causes no problem at the image level. Constant `β` yields one class; injective `β` yields one class per case. Adding unreachable junk to a representation codomain defeats whole-codomain uniqueness, and adding internal structure not preserved by the commuting bijection defeats stronger structural uniqueness. Those stronger readings are not proved.

**Dependencies.** FAR-CORE-001 plus elementary quotient construction.

**Falsifier/reopening condition.** A sufficient representation with a collision outside `ker(β)`, or a purported coarser sufficient quotient whose kernel strictly contains `ker(β)`.

### FAR-CORE-003 — dynamic/compositional descent (provisional allocation)

**Reconstructed proposition.** Let a deterministic transition system have transitions `δ_a:X→X`. A representation `r` admits well-defined abstract transitions `\barδ_a:im(r)→im(r)` satisfying `r∘δ_a=\barδ_a∘r` iff `ker(r)` is stable under every transition:

`r(x)=r(y) ⇒ r(δ_a(x))=r(δ_a(y))`.

If `r=qβ` for behavior defined by a test/context family, closure of that family under each relevant continuation is a sufficient premise for this stability, provided the contract semantics identifies the observation after `a` followed by any test with the corresponding continuation test at the original state.

**Proof reconstruction.** Descent immediately implies stability. Conversely define `\barδ_a(r(x))=r(δ_a(x))`; stability is exactly well-definedness. For a continuation-closed behavioral equivalence, equal behavior at `x,y` includes equality for every prefixed continuation, hence successor states agree under every admitted test and remain equivalent.

**Hostile countermodel.** Let `p,q` have equal currently observed output, but let action `a` send them to states with outputs 0 and 1. A contract containing only current-output tests identifies `p,q`; the quotient transition from their shared class is not well-defined. Adding the `a`-then-output continuation separates them.

**Boundary objection.** Literal necessity of syntactic continuation closure is too strong: stability may hold accidentally (for example, all transitions are constant) even when the declared family is not closed. The proved statement is an iff with kernel stability and a sufficient closure condition, not “closure is necessary in every system.” Nondeterministic, probabilistic, coalgebraic, or partial dynamics require a separately typed descent theorem.

**Dependencies.** Equivalence/kernel definitions; FAR-CORE-001 only if behavior sufficiency is also asserted.

**Falsifier/reopening condition.** Equal represented states with successors in different represented classes under a transition claimed to descend.

### FAR-CORE-004 — no contract-free simultaneous minimum

**Exact proposition available in v1.1.** For every set `X` with at least two elements, no single representation is simultaneously a least-informative sufficient representation for every exact observation contract on `X`.

**Proof reconstruction.** Choose a constant behavior `β0`, whose least sufficient kernel is `X×X`, and an injective behavior `β1`, whose least sufficient kernel is the diagonal. A representation minimal for the first must identify every pair; a representation minimal for the second must identify none. Since `|X|≥2`, those requirements are incompatible.

**Quantifier attack.** The theorem is universal over nontrivial `X` and assumes the admitted contract class contains both exact behaviors. It fails on `|X|≤1`, where constant and injective kernels coincide. It does not deny a representation sufficient for every contract: the identity representation is universally sufficient. It does not rule out a minimum for a restricted contract family sharing one observational kernel.

**Dependencies.** FAR-CORE-002 or the same kernel argument directly.

**Falsifier/reopening condition.** A nontrivial domain and a single representation shown to have both universal sufficiency and contract-by-contract least informativeness, under a contract class containing constant and injective behaviors.

### FAR-CORE-005 — invariance is relative to admitted re-representation (provisional allocation)

**Reconstructed proposition.** Let `G` be the declared class/groupoid of admissible faithful re-presentations. A property is representation-independent relative to `G` exactly when it is invariant/transportable along every morphism in `G`. Which properties qualify can change when `G` changes.

**Proof reconstruction.** The first sentence is the operational definition of representation independence. For the second, take a presentation-sensitive property such as a chosen field name. It is invariant under the identity-only class and noninvariant under a class containing a faithful renaming.

**Hostile tests.** With `G` empty or identity-only, nearly everything is vacuously invariant; with all bijections, only structural invariants survive. If “faithful” is undefined, the result has no determinate extension. This claim does not select the correct `G` for an application and does not prove that any particular substantive property is invariant.

**Dependencies.** A declared presentation category/equivalence and a transport rule.

**Falsifier/reopening condition.** A claimed invariant that changes along an admitted morphism, or a claimed dependence on `G` when the compared classes induce exactly the same orbits.

### FAR-CORE-006 — faithful transport preserves factorization (provisional allocation)

**Reconstructed proposition.** Exact sufficiency is preserved by a semantics-preserving faithful change of presentation. Concretely, if `β=d∘r`, `e:X'→X`, `u:B→B'`, and `v:im(r)→R'` are bijective/faithful presentation maps, and

`β'=u∘β∘e`, `r'=v∘r∘e`,

then `β'=(u∘d∘v^{-1})∘r'` on the reachable image.

**Proof reconstruction.** Substitute the two definitions and cancel `v^{-1}v`. This is a commuting-diagram calculation.

**Hostile countermodel.** If `v` collapses two `r`-values whose behaviors differ, transport is not faithful and sufficiency is lost. If `u` or `e` fails to preserve the declared semantics/domain, the compared contracts are not the same observation problem. Mere host encodability is not enough.

**Dependencies.** FAR-CORE-001 plus explicit faithfulness/semantic-commutation premises.

**Falsifier/reopening condition.** An admitted faithful transport satisfying the declared commuting conditions that turns a valid factorization into a collision.

### FAR-CORE-007 — primitive counts are noninvariant under broad faithful encoding (provisional allocation)

**Reconstructed proposition.** A finite count of named primitive fields/sorts is not invariant under an admitted faithful re-presentation class that permits product packing and unpacking.

**Witness proof.** Two fields with values in `A` and `B` are faithfully equivalent to one field with values in `A×B`; pairing and projections are inverse. Any behavior on the pair transports to the packed form. The counted presentation primitives change from two to one while represented information does not.

**Hostile boundary.** Under a fixed typed signature that forbids product packing, or under a cost model that counts product components rather than surface fields, the chosen count may be invariant. The witness proves noninvariance for a declared class containing the encoding; it does not prove that no meaningful minimal basis exists under every language, type discipline, cost order, or equivalence.

**Dependencies.** FAR-CORE-005/006 and availability of the encoding/decoding maps.

**Falsifier/reopening condition.** A claim of invariance under a class that actually includes a faithful count-changing packing.

### FAR-CORE-008 — finite operator counts are noninvariant under broad faithful encoding (provisional allocation)

**Reconstructed proposition.** The number of named operators in a finite interface is not invariant under an admitted faithful re-presentation class that permits tagging, dispatch, currying, or definitional extension.

**Witness proof.** Package operators `f_1,…,f_n` into a single dispatcher `U(i,x)=f_i(x)` over a tagged input type. Conversely, split a dispatcher into its tagged restrictions. With the tag and typing included, the two interfaces simulate each other exactly, but the surface operator count is `n` versus one.

**Hostile boundary.** The result is finite and language-relative. A fixed signature, restricted arities, prohibition on tags, complexity/cost accounting, or a requirement that definitional equivalence preserve named operations can make a count invariant by contract. The construction does not establish minimality or computational efficiency of the one-operator presentation.

**Dependencies.** FAR-CORE-005/006 and explicit admitted coding operations.

**Falsifier/reopening condition.** A surface-count necessity claim under an equivalence class that admits dispatcher packaging.

### FAR-CORE-009 — finite-panel/open-domain boundary (provisional allocation)

**Reconstructed proposition.** For a domain `D` with an untested element and no premise linking tested to untested elements, evidence that `P(i)` holds for every member of a finite panel `F⊂D` does not logically entail `∀i∈D P(i)`.

**Countermodel proof.** Interpret `P` as true on every element of `F` and false on one `j∈D\F`. This model satisfies all panel observations and falsifies the universal.

**Hostile boundary.** If `D=F`, if a proven finite basis is complete, or if an induction/compact characterization genuinely reduces the universal to the panel, finite evidence plus those premises can prove a universal. The theorem is a non-entailment absent coverage premises, not a ban on all finite proofs. “Open-domain” must therefore mean the target class is not extensionally exhausted by the panel.

**Dependencies.** Elementary model theory only.

**Falsifier/reopening condition.** A valid coverage theorem showing that the particular finite panel is complete for the declared open-domain property.

### FAR-CORE-010 — exact common theory and frame-subtracted residue

**Exact proposition available in v1.1.** Fix a logical signature `L`, index class `I`, and interpretation profiles `J=(J_i)` producing interpreted `L`-models `M_i`. Define

`T_{L,J,I}=⋂_{i∈I} Th_L(M_i)`

and, for an interface frame `Γ`,

`R_{L,J,I,Γ}=T_{L,J,I}\Cn_L(Γ)`.

Exact common theory is directly indexed by `L,J,I`, not by `Γ` when those objects/models are fixed. The frame-subtracted residue is additionally indexed by `Γ`.

**Proof reconstruction.** `Γ` is syntactically absent from the definition of `T`, so holding `L,J,I,M_i` fixed while changing only `Γ` cannot alter it. It occurs in the definition of `R`, and a change in its consequence closure can remove a different subset of `T`. First-order theories are invariant under `L`-isomorphism, so isomorphic replacements do not alter truth sets.

**Existence witness for residue change.** If `T` contains a non-logically-valid `φ`, then `Γ0=∅` leaves `φ` in the residue while `Γ1={φ}` removes it.

**Hostile tests and qualifications.**

- “Can change” is existential, not “must change”: different parameters can yield the same theory or residue.
- If `T` contains only logical validities, the displayed `φ` witness is unavailable, though the indexing statement remains true.
- Comparing theories after changing `L` requires a declared translation because the sentence universes differ.
- For empty `I`, an explicit convention for the empty intersection is required (normally all `L`-sentences).
- `T\Cn_L(Γ)` need not itself be deductively closed; calling it a “residue” is accurate, calling it a theory without further closure would not be.
- A frame used to construct or change `J` affects `T` only through that changed model/profile; it is not an independent index once the models are held fixed.

**Dependencies.** Definitions and ordinary first-order isomorphism invariance.

**Falsifier/reopening condition.** A derivation in which `Γ` changes exact `T` while every direct argument `L,J,I` and all selected models remain extensionally fixed.

### FAR-CORE-011 — consequence-affecting omitted parameters (provisional allocation)

**Reconstructed proposition.** If there exist cases `x,y` such that a representation gives `r(x)=r(y)` while the declared behavior differs, `β(x)≠β(y)`, and the difference is induced by a parameter not recoverable from `r`, then `r` is not sufficient.

**Proof reconstruction.** The pair is a direct violation of `ker(r)⊆ker(β)`, so no decoder can exist.

**Hostile boundary.** Syntactic omission alone is not enough. An omitted parameter may be functionally determined by represented values, irrelevant on the reachable domain, or ignored by the contract. “Consequence-affecting” must include an attainable collision witness, not merely a causal story.

**Dependencies.** FAR-CORE-001.

**Falsifier/reopening condition.** A valid decoder despite the claimed consequence-changing collision would expose an inconsistent premise; absent a collision, the omission objection remains open rather than refuting sufficiency.

### FAR-CORE-012 — determinate absence versus epistemic Unknown (provisional allocation)

**Reconstructed proposition.** Whenever the contract assigns different behavior to a determinate-absence case and an epistemic-Unknown case, every sufficient representation must distinguish those cases.

**Proof reconstruction.** Collapsing them creates equal `r` values and unequal `β` values, contradicting FAR-CORE-001.

**Hostile boundary.** If the contract intentionally coalesces the outcomes, if only one case is reachable, or if “Unknown” is not a value at the same semantic type, no separation follows. The theorem is contract-conditional and does not prescribe a universal data-model ontology.

**Dependencies.** FAR-CORE-001.

**Falsifier/reopening condition.** A sufficient factorization that collapses two reachable cases the contract demonstrably distinguishes.

### FAR-CORE-013 — canonical Ω elimination (provisional allocation)

**Reconstructed proposition.** If a stored component `Ω` is exactly a deterministic function `g(z)` of retained base state `z`, then the graph representation `(z,g(z))` and `z` are isomorphic on reachable states. Materializing `Ω` adds no observational information; it can be eliminated and recomputed for every behavior defined on consistent states.

**Proof reconstruction.** Projection `(z,g(z))↦z` and graph insertion `z↦(z,g(z))` are mutual inverses on the graph of `g`. Factorizations transport across this bijection.

**Hostile boundary.** The allowed Stage-A sources do not define canonical FARA `Ω`, its base state, or its derivation. If `Ω` can be independently edited, stale, nondeterministic, historically versioned, or directly observed as a stored artifact rather than its recomputed value, projection need not preserve behavior. Thus the generic conditional theorem is proved, but its application to canonical `Ω` cannot yet be checked.

**Dependencies.** FAR-CORE-006 plus the unverified premise `Ω=g(z)` on the entire reachable domain.

**Falsifier/reopening condition.** Two reachable consistent cases with equal retained base state and different contract-relevant `Ω`, or absence of a total declared derivation.

### FAR-CORE-014 — SSS bounded supported classification (provisional allocation; scope deliberately not expanded)

**Reconstructed proposition/obligation.** The monograph describes SSS only as a **bounded supported factorization instance** and labels the claim `SUPPORTED/DERIVED`, not as a universal theorem. The maximum defensible reconstruction is: for one declared bounded SSS case set and observation contract, the SSS representation has evidence of the factorization/collision-free condition; no open-domain, global-minimality, uniqueness, empirical-success, or contract-free conclusion follows.

**Proof obligation.** Identify the exact bounded domain, representation, behavior map, decoder or exhaustive collision analysis, and provenance of support. None is present in the allowed Stage-A text, so no application proof can be reconstructed yet.

**Hostile boundary.** A finite checked panel cannot establish an open-domain SSS universal (FAR-CORE-009). A host capable of encoding SSS artifacts does not establish native structure. Supported/derived evidence must not be promoted to `PROVED` unless an exact factorization proof is supplied.

**Dependencies.** At least FAR-CORE-001 and FAR-CORE-009; possibly FAR-CORE-013 if `Ω` is part of SSS, but that cannot be assumed before reconciliation.

**Falsifier/reopening condition.** A bounded in-scope collision, a missing/partial decoder, or any ledger scope broader than the evidence.

## 4. Premise and dependency graph

| Node | Core premise | Direct downstream use |
|---|---|---|
| D1 | Exact contract induces typed `β:X→B` | 001, 002, 004, 011, 012, 014 |
| D2 | Image-level decoder / kernel criterion | 001 |
| C001 | Factorization iff harmless collisions | 002, 006, 011, 012, 014 |
| C002 | Canonical quotient and coarseness | 004 |
| D3 | Transition-kernel stability / continuation semantics | 003 |
| D4 | Nontrivial `X`; constant and injective contracts admitted | 004 |
| D5 | Declared faithful re-presentation class | 005, 006, 007, 008 |
| C005/C006 | Invariance and transport | 007, 008, 013 |
| D6 | Proper finite panel with no coverage theorem | 009, limits 014 |
| D7 | Fixed `L,J,I,M`; ordinary FOL semantics | 010 |
| D8 | Reachable behavior-changing collision | 011, 012 |
| D9 | Exact total derivation `Ω=g(z)` on reachable states | 013 |
| D10 | Exact bounded SSS contract and support corpus | 014 |

Claims 001, 002, 004, 011, and 012 form one kernel/factorization family. Claim 003 adds dynamics and cannot be obtained from static sufficiency without stability. Claims 005–008 and 013 require an explicit presentation/equivalence class. Claims 009 and 010 are logically independent of the factorization family except when used to limit application claims. Claim 014 is an application classification and cannot strengthen any upstream theorem.

## 5. Stage-A countermodel ledger

| ID | Attack | Result and claim impact |
|---|---|---|
| A-CM-001 | `X=∅`, `R≠∅`, `B=∅` with a total decoder demanded on all `R` | Kernel inclusion holds but no `R→B` exists; 001 must be image-level or add an extension premise. |
| A-CM-002 | Add unreachable junk to the codomain of a minimal quotient | Whole-codomain uniqueness fails; 002 uniqueness is for reachable images/up to commuting isomorphism. |
| A-CM-003 | Equal current observations, action sends states to differently observed successors | Static quotient does not descend; 003 needs transition stability/continuation closure. |
| A-CM-004 | `|X|≤1` | Constant and injective minima coincide; 004's nontrivial-domain premise is necessary. |
| A-CM-005 | Identity-only versus rename-admitting presentation class | A field-name property switches from invariant to noninvariant; 005 is class-relative. |
| A-CM-006 | “Transport” collapses behaviorally different representation values | Sufficiency fails; 006 needs faithfulness and semantic commutation. |
| A-CM-007 | Fixed typed language forbids packing | Primitive count may be invariant by contract; 007 is conditional on admitted coding. |
| A-CM-008 | Fixed operator signature forbids tags/dispatch | Operator count may be invariant by contract; 008 is conditional on admitted coding. |
| A-CM-009 | Predicate true on finite panel and false at an untested point | Refutes panel-to-open-universal entailment; supports 009's boundary. |
| A-CM-010 | Change `Γ` while holding all direct arguments fixed | Exact `T` is unchanged by definition; residue may or may not change. |
| A-CM-011 | Omitted parameter is recoverable or behaviorally irrelevant | Syntactic omission alone does not refute sufficiency; 011 needs a collision. |
| A-CM-012 | Contract coalesces absence and Unknown | No mandatory distinction; 012 is exactly contract-conditional. |
| A-CM-013 | Independently editable/stale `Ω` | Elimination can lose information; 013 needs the exact derivation premise. |
| A-CM-014 | Bounded panel silently promoted to open SSS domain | Promotion invalid; preserve bounded supported scope. |

## 6. Independent finite computation

A fresh Python script imported no repository code or fixtures. It exhaustively checked small finite cases:

- 11,141 combinations for factorization iff kernel inclusion;
- 11,141 sufficient-representation/quotient comparisons;
- constant versus injective minima for domain sizes 2 through 5; and
- 26,122 representation/transition combinations for descent iff kernel stability.

All represented checks passed. These computations are consistency/witness evidence for the encoded finite cases only; the general results rest on the proofs above.

## 7. Stage-A unresolved obligations carried forward

1. Reconcile every provisional claim number and exact scope against the machine ledger without rewriting this record.
2. Determine whether the ledger defines decoders on reachable images or arbitrary codomains.
3. Determine the exact dynamic theorem and whether continuation closure is a sufficient condition or asserted as literal necessity.
4. Determine the admitted equivalence/translation class for claims 005–008.
5. Obtain the formal definition and derivation premise for canonical `Ω`.
6. Preserve the exact bounded, supported/derived scope of FAR-CORE-014 and identify its declared contract/evidence.
7. Independently research prior art and counterexamples from claim-derived search terms only.

No Stage-D verdict is frozen in this document.
