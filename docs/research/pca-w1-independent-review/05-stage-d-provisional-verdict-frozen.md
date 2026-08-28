# PCA-W1 Independent Review — Stage D Provisional Verdict Freeze

Review program: `PCA-W1-INDEPENDENT-REVIEW`  
Immutable target: `14105775daf3c5713b134a728db2e1e53673af97`  
Verified target tree: `68f058199b7c94b707fd5fe978f1ef59d695ab00`  
Governing theory: `PROJECT-FAR-CORE-THEORY-1.1`  
Freeze identifier: `PCA-W1-D-20260828T171703Z`  
Freeze time: 2026-08-28T17:17:03Z  
Controlled unblinding status at freeze: **NOT STARTED**

## 1. Freeze declaration and status vocabulary

This is the irreversible pre-unblinding judgment.  It was written after the
Stage-A blind reconstruction, Stage-B ledger reconciliation, and Stage-C
independent external search, and before reading any prior Project FAR audit,
acceptance record, pull request, correction history, v1.0 material, regression
fixture, earlier reviewer conclusion, internal research, repository test, or
project memory.

The claim rows use only the required final vocabulary:

- `PROVED`: a complete argument follows under the row's exact stated scope and
  premises;
- `REFUTED`: an in-scope countermodel defeats the proposition;
- `OPEN`: the proposition is precise and evidence is available, but neither a
  proof nor a refutation is established;
- `UNDERDETERMINED`: the proposition's application premise, definition, or
  evidence is not available enough to choose proof or refutation; and
- `NOT APPLICABLE`: the item is not a truth-apt claim in the review scope.

The machine ledger's label `supported_derived` for FAR-CORE-014 is an internal
evidence classification, not one of these verdicts.  Before its locked source is
opened, it maps to `UNDERDETERMINED`, not `PROVED`.  No claim is assigned a
protocol-only `BLOCKED` or `HISTORICAL` label here.

## 2. Normalization and shared premises

The governing artifacts declare Set presentation, explicit totalized semantics,
fixed-contract evaluation, extensional exactness, and declared invariance.  I
make the following interpretations explicit rather than hiding them:

1. A representation is judged extensionally on its reachable image.  Unused
   ambient codomain labels carry no information about the source.  This is the
   normalization required for up-to-isomorphism uniqueness.
2. An exact observation contract is a total behavior `beta:X->B`; a
   representation is `r:X->R`; exact image-level sufficiency means some
   `d:im(r)->B` has `beta=d o r`.
3. “Least-informative” uses the factorization order: `r1` is no more informative
   than `r2` when `r1` factors through `r2` on reachable images.
4. For FAR-CORE-003, declared actions and tests have typed composition, and the
   context closure contains all continuations needed by the claim.
5. “Consequence-affecting omitted parameter” in FAR-CORE-011 means there are
   attainable states in one retained-representation fiber whose contract
   behaviors differ.  Merely omitting a syntactic field does not suffice.
6. Claims 013 and 014 contain application premises referenced but not stated in
   the allowed pre-unblinding artifacts.  I do not invent them.

If (1) is rejected in favor of a decoder total on an arbitrary ambient codomain,
the empty-source/empty-output counterexample in the hostile-test ledger defeats
the corresponding unqualified kernel theorem.  The extensional premise and the
information-order language support (1), but the edge is preserved as an
objection for controlled unblinding.

## 3. Verdict summary

| Claim | Frozen Stage-D verdict | Short basis |
|---|---|---|
| FAR-CORE-001 | PROVED | Kernel/factorization equivalence on the reachable image. |
| FAR-CORE-002 | PROVED | Observational quotient is least; mutual least factorizations give reachable-image isomorphism. |
| FAR-CORE-003 | PROVED | Continuation closure makes observational equivalence stable under declared actions. |
| FAR-CORE-004 | PROVED | Constant and injective contracts have incompatible least partitions on every nontrivial domain. |
| FAR-CORE-005 | PROVED | Invariants are antitone under inclusion of admitted transformations. |
| FAR-CORE-006 | PROVED | Lossless underlying-set codes are compatible with arbitrarily different source structures. |
| FAR-CORE-007 | PROVED | Faithful reification/tagging changes primitive vocabulary count. |
| FAR-CORE-008 | PROVED | A finite tagged dispatcher replaces a finite operator family within the admitted regime. |
| FAR-CORE-009 | PROVED | Two extensions agreeing on a proper finite panel can disagree off-panel. |
| FAR-CORE-010 | PROVED | `T` and the residue have different explicit parameter dependencies. |
| FAR-CORE-011 | PROVED | An attainable behavior collision in an omitted-parameter fiber violates exact factorization. |
| FAR-CORE-012 | PROVED | A contract distinguishing absence from Unknown forbids their representational collapse. |
| FAR-CORE-013 | UNDERDETERMINED | Generic derived-view theorem proved, but the canonical application equation is absent. |
| FAR-CORE-014 | UNDERDETERMINED | Exact representation/decoder classes and instance evidence are locked in unread PR #453. |

**Frozen terminal verdict for the full 14-claim closure bundle:**
`UNDERDETERMINED`.

This terminal verdict is not an average: twelve mathematical/non-entailment
claims are proved within their explicit scope, but the two application
instantiations cannot be certified from the pre-unblinding record.  The generic
kernel through FAR-CORE-012 is `PROVED`; the full named bundle is not.

## 4. Claim dossiers

### FAR-CORE-001 — exact sufficiency as factorization

**Exact proposition and quantifiers.**  For any Set-based exact contract
`beta:X->B` and representation `r:X->R`, `r` is exactly sufficient for `beta`
iff `beta` factors through `r` on `im(r)`.  Equivalently,
`ker(r) subseteq ker(beta)`.

**Premises.**  Total extensional behavior on `X`; equality is the observation
criterion; decoder required only on reachable representation values.

**Proof.**  A factorization `beta=d o r` immediately sends equal representation
values to equal behavior.  Conversely, if `r(x)=r(y)` implies
`beta(x)=beta(y)`, define `d(r(x))=beta(x)`.  Kernel inclusion makes `d`
well-defined and gives the required equation.

**Strongest countermodel search.**  A constant representation paired with a
two-valued behavior produces a collision and correctly fails sufficiency.  The
empty-source/unused-codomain example refutes only a stronger whole-codomain
extension claim, not this normalized proposition.

**Prior art.**  C-S01 (Blackwell comparison), C-S04 (Set quotients/coalgebra),
C-S11 (view determinacy), C-S12 (complete abstract interpretations).  These
make novelty implausible but do not substitute for the proof.

**Dependencies.**  Definitions only.

**Objections and limits.**  No computability, measurability, approximation,
noise, or out-of-distribution claim follows.  Arbitrary unused target labels are
ignored extensionally.

**Verdict:** `PROVED`.

**What would change it.**  An in-scope image-level factorization with a behavior
collision, or an exact governing definition requiring a total decoder over
arbitrary unreachable labels without an extension premise.

### FAR-CORE-002 — observational quotient is uniquely least-informative

**Exact proposition and quantifiers.**  For every Set-based exact contract
`beta:X->B`, the quotient `q:X->X/~beta`, where
`x~beta y` iff `beta(x)=beta(y)`, is sufficient and least in the factorization
order among sufficient representations; any other normalized least
representation is isomorphic to it on reachable images.  When `X` is finite it
also has minimum reachable cardinality.

**Premises.**  The normalization and information order in section 2; the
cardinality subclaim is limited to finite `X` as in the ledger.

**Proof.**  Behavior is constant on quotient classes, so it factors through
`q`.  If `r` is sufficient, `r(x)=r(y)` implies `x~beta y`, hence
`[x]_beta` is a well-defined function of `r(x)` and `q` factors through `r`.
Thus `q` is below every sufficient representation.  Two least normalized
representations factor through each other; the induced maps are inverse because
both representations are surjective onto their reachable images.  For finite
`X`, every sufficient representation has at least one value per behavior class.

**Strongest countermodel search.**  Adding arbitrary unreachable labels defeats
whole-codomain uniqueness; this is excluded by extensional normalization.
C-S03 supplies a genuine measurable/statistical failure outside Set scope.

**Prior art.**  C-S01, C-S03, C-S04, C-S12.

**Dependencies.**  FAR-CORE-001 and ordinary quotient-set construction.

**Objections and limits.**  No canonical choice of labels is claimed; uniqueness
is up to isomorphism.  No unrestricted measurable or effective statistic result
follows.

**Verdict:** `PROVED`.

**What would change it.**  An in-scope sufficient representation through which
the quotient does not factor, or a governing requirement that ambient unused
codomain labels count toward isomorphism/information.

### FAR-CORE-003 — context closure and action-compatible equivalence

**Exact proposition and quantifiers.**  For declared actions and tests, closing
the observational test family under the declared action continuations makes
equality of all test results stable under every declared action; consequently
the equivalence quotient admits well-defined descended actions.

**Premises.**  Typed action/test composition; exact equality of all tests in the
closure; the closure includes each continuation used in the stability proof.

**Proof.**  Suppose states agree on every closed test.  For an action `a` and
any test `t`, closure contains `t o a`; equality on that component says the
`a`-successors agree on `t`.  Since this holds for every test, successors are
equivalent.  Thus each action maps equivalence classes to equivalence classes and
is well-defined on the quotient.

**Strongest countermodel search.**  In the three-state example from the hostile
ledger, current observation equates `a,b` but an action sends them to states with
different observations.  This validates the need for an action-stability/closure
premise.  A one-class quotient shows syntactic closure is sufficient, not
necessary in every accidental system.

**Prior art.**  C-S04, C-S13, C-S14, C-S18.

**Dependencies.**  FAR-CORE-001/002 for quotient language; the stability proof
itself is direct.

**Objections and limits.**  Partial, stochastic, nondeterministic, or
history-sensitive systems require separately declared semantics.  Necessity of
the syntactic construction is not claimed.

**Verdict:** `PROVED`.

**What would change it.**  A declared closed test/action system with equivalent
states whose same-action successors disagree on an admitted test.

### FAR-CORE-004 — no universal least representation across varying contracts

**Exact proposition and quantifiers.**  For every set `X` with at least two
elements, no single representation is simultaneously least-informative and
sufficient for every observation contract on `X`.  Universal sufficiency itself
is not denied.

**Premises.**  The varying contract class contains at least the constant and an
injective behavior on `X`; least-informative uses the factorization order.

**Proof.**  The constant contract's quotient has one class and is its least
representation.  The injective contract's quotient has singleton classes, so
every sufficient representation is injective.  No representation has both
one-class and singleton-class information on a nontrivial `X`.  The identity is
nevertheless sufficient for both, separating universal sufficiency from
universal minimality.

**Strongest countermodel search.**  Singleton/empty domains and contract classes
with only one observational partition admit a universal least representation;
both lie outside the stated hypotheses.  Finite enumeration checked the
obstruction for sizes 2–5.

**Prior art.**  C-S01 and the stronger but domain-specific non-identifiability in
C-S02.

**Dependencies.**  FAR-CORE-002's partition characterization.

**Objections and limits.**  The claim cannot be promoted to a fixed restricted
contract class that lacks both partitions, and it says nothing about a
universally sufficient nonminimal identity code.

**Verdict:** `PROVED`.

**What would change it.**  A nontrivial `X` and one representation proved least
for both the constant and injective contracts in the declared order.

### FAR-CORE-005 — antitone invariants

**Exact proposition and quantifiers.**  For compatible nested admitted
transformation classes `G subseteq H`, `Inv(H) subseteq Inv(G)`.

**Premises.**  Common object universe and common preservation semantics.

**Proof.**  A predicate preserved by every member of `H` is preserved by every
member of its subset `G`.

**Strongest countermodel search.**  The identity-only class versus the class
also containing a swap gives strict inclusion.  Equal invariant sets show
strictness is not guaranteed.  Nonnested classes show why inclusion is needed.

**Prior art.**  C-S05 states the nested-transformation-group principle
classically; C-S02 supplies a modern domain example.

**Dependencies.**  Definitions only.

**Objections and limits.**  No comparison is asserted for unrelated
transformation classes, and “declared” cannot be omitted.

**Verdict:** `PROVED`.

**What would change it.**  Compatible `G subseteq H` and a predicate preserved
by all `H` transformations but not by some member of `G`.

### FAR-CORE-006 — encoding capacity does not establish native common structure

**Exact proposition and quantifiers.**  For source sets/structures `S_i`, host
`H`, injective encodings `e_i:S_i->H`, and image decoders satisfying
`d_i o e_i=id`, those equations establish lossless host capacity.  Without
additional preservation laws they do not logically entail any specified common
native operation, relation, axiom, primitive vocabulary, or semantics of the
sources.

**Premises.**  “Does not establish” is a non-entailment claim.  Any positive
structural conclusion must be stated in a signature and held fixed across the
countermodels.

**Proof/countermodel.**  Keep two-element sets, encoders, host tokens, and
decoders fixed.  Equip one source with group multiplication and the other with
left-zero semigroup multiplication, or vary an arbitrary source relation.  The
coding equations remain true while the proposed shared structural conclusion
changes.  Hence it is not entailed.

**Strongest countermodel search.**  Adding a common signature and requiring the
encodings to be homomorphisms can establish common structure; this is a
strengthened premise, not a counterexample.

**Prior art.**  C-S06, C-S07, C-S13.

**Dependencies.**  Elementary model variation; conceptually separates Set maps
from structure-preserving maps.

**Objections and limits.**  The phrase “native common structure” has no positive
classification without a signature/category.  The proved content is exactly the
non-entailment schema, not the claim that no sources ever share structure.

**Verdict:** `PROVED`.

**What would change it.**  A derivation of a nontrivial specified source
operation/relation solely from the injection and decoder equations, valid under
arbitrary structure variation.

### FAR-CORE-007 — primitive vocabulary count is noninvariant

**Exact proposition and quantifiers.**  Under admitted faithful
reification/tagging changes of presentation, the number of primitive vocabulary
items is not invariant.

**Premises.**  The transformation regime permits definitions, tags, and faithful
recovery of the original behavior/presentation.

**Proof/witness.**  Boolean algebra can be presented with multiple conventional
primitive operations or with one Sheffer operation from which they are defined.
More generally, primitive names can be reified as tags interpreted by a generic
operator, and unpacked back.  Behavior is faithfully recoverable while the
primitive-symbol count differs.

**Strongest countermodel search.**  A fixed signature and ban on reification
makes the count invariant by stipulation; that regime is outside the claim.

**Prior art.**  C-S07 and C-S15.

**Dependencies.**  FAR-CORE-006's structure/presentation distinction, though the
witness is independent.

**Objections and limits.**  Complexity, arity, sort, continuity, and description
length may change and can be meaningful under fixed rules.  The claim concerns
raw primitive count only.

**Verdict:** `PROVED`.

**What would change it.**  A proof that every faithful admitted
reification/tagging preserves primitive count, contradicting the explicit
one-basis/multiple-basis witness.

### FAR-CORE-008 — finite operator count is noninvariant

**Exact proposition and quantifiers.**  Every finite family of operators in the
declared tagged-tuple regime can be represented by a single dispatcher plus tags,
and recovered by fixing tags; therefore finite operator count is not invariant
under that regime.

**Premises.**  Finite family; admissible tagged tuples/sorts; dispatcher allowed;
exact recovery on encoded inputs.

**Proof.**  Define `D(i,args)=f_i(args)` on the tagged disjoint union of the
original operator domains.  Each `f_i` equals `args |-> D(i,args)`.  This
faithfully translates a many-operator presentation to a one-dispatcher
presentation.

**Strongest countermodel search.**  Fixed homogeneous signatures, arities,
continuity, cost, or no-tag rules can prohibit the dispatcher.  Infinite
families are not covered by the finite construction.

**Prior art.**  C-S15 is a concrete one-operation basis; the general proof is
the elementary tagged dispatcher.

**Dependencies.**  FAR-CORE-007's admitted presentation regime.

**Objections and limits.**  “One operator” may hide tag data and implementation
complexity; no cost invariance is asserted.

**Verdict:** `PROVED`.

**What would change it.**  A finite admitted family for which the typed tagged
disjoint union or dispatcher cannot be formed despite all stated premises.

### FAR-CORE-009 — a proper finite panel does not establish open universality

**Exact proposition and quantifiers.**  For a proper finite tested subset
`D0` of an open target domain `D`, agreement/success on `D0` alone does not
logically entail the corresponding universal claim on all of `D`.

**Premises.**  No independent coverage theorem, complete finite basis,
induction principle, identifiability restriction, or probabilistic
generalization premise is included in “alone.”

**Proof/countermodel.**  Choose `x* in D\D0`.  Two candidate behaviors can
agree on every tested point and disagree only at `x*`.  They yield identical
finite-panel evidence and opposite universal truth values.

**Strongest countermodel search.**  C-S09 shows that finite samples can support
probabilistic uniform generalization with explicit capacity assumptions.  That
does not refute the no-entailment proposition; it marks its boundary.

**Prior art.**  C-S08 and C-S09.

**Dependencies.**  Elementary model extension.

**Objections and limits.**  The claim does not deny mathematical induction,
finite exhaustive domains, formal coverage, or statistical confidence bounds.

**Verdict:** `PROVED`.

**What would change it.**  A logical rule deriving every open-domain universal
from arbitrary proper finite agreement without any extra premise.

### FAR-CORE-010 — exact common theory and residue parameter audit

**Exact proposition and quantifiers.**  With language `L`, interpretation/setup
`J`, index set `I`, and fixed models `M_i`,
`T_{L,J,I}=intersection_{i in I} Th_L(M_i)` is directly indexed by `L,J,I` and
not by `Gamma`.  The residue
`R_{L,J,I,Gamma}=T_{L,J,I}\Cn_L(Gamma)` additionally depends on `Gamma`.
Holding `L,J,I` and the models fixed, changing `Gamma` cannot change `T` and can
change `R`.

**Premises.**  Fixed consequence relation for `L`; declared convention for an
empty index set; all compared theories are typed in the same language.

**Proof.**  `Gamma` does not occur in the definition of `T` and does occur in
the subtracted closure defining `R`.  For a witness, take propositional atom
`p` and one model satisfying `p`.  Then `p in T`; it remains in the residue for
an empty premise set (assuming ordinary tautological closure) but is removed
when `Gamma={p}`.

**Strongest countermodel search.**  Changing the language, model panel, or
interpretation can change `T`; this is outside the fixed-parameter comparison.
Some changes of `Gamma` leave the residue unchanged, so the modal is “can,” not
“must.”

**Prior art.**  C-S10 makes signature/model/satisfaction dependencies explicit.

**Dependencies.**  Definitions of theory, consequence closure, and set
difference.

**Objections and limits.**  The residue need not be deductively closed.  The
empty-intersection convention and language translations must be stated in an
implementation.

**Verdict:** `PROVED`.

**What would change it.**  `Gamma` entering the governing definition of `T`, or
a fixed-`T` example where the residue definition is independent of every change
to `Cn_L(Gamma)` despite a sentence moving into/out of that closure.

### FAR-CORE-011 — omission of a consequence-affecting parameter

**Exact proposition and quantifiers.**  If an exact-contract representation
omits a parameter in the strong sense that two attainable states with identical
retained representation values differ in contractual behavior because of that
parameter, the representation is not sufficient.

**Premises.**  Attainability of both states; same representation fiber;
different behavior.  Recoverable, fixed, unreachable, or irrelevant omitted
fields do not meet “consequence-affecting” in this theorem.

**Proof.**  The two states form a `ker(r)` pair not in `ker(beta)`, contradicting
FAR-CORE-001's necessary condition.  No decoder can return both behaviors from
the same representation value.

**Strongest countermodel search.**  If an omitted field `p` is deterministically
recoverable from retained `z`, then behavior depending on `p` can still factor
through `z`.  This defeats a merely syntactic omission claim and is why the
fiber-collision premise is explicit.

**Prior art.**  C-S11's view-determinacy collision criterion.

**Dependencies.**  FAR-CORE-001.

**Objections and limits.**  If the governing phrase “consequence-affecting” were
intended to include only global causal relevance without a retained-fiber
collision, the claim would be false; the target artifacts do not support that
broader reading.

**Verdict:** `PROVED`.

**What would change it.**  Two attainable same-representation states with
different behavior plus a valid exact decoder, or an unblinded definition that
uses the refuted merely syntactic reading.

### FAR-CORE-012 — absence and Unknown under distinguishing contracts

**Exact proposition and quantifiers.**  For any exact contract that assigns
different behavior to attainable absence and explicit-Unknown states, every
sufficient representation must preserve their distinction.

**Premises.**  Both states are attainable and the admitted fixed contract
distinguishes them.

**Proof.**  Collapsing them creates a representation collision with different
behavior, violating FAR-CORE-001.

**Strongest countermodel search.**  If no admitted contract distinguishes the
states or one state is unreachable, a representation may merge them without
loss.  This confirms the conditional scope.

**Prior art.**  C-S16 formalizes semantic differences among null/unknown
treatments and their query consequences.

**Dependencies.**  FAR-CORE-001/011.

**Objections and limits.**  No contract-independent ontology of missingness is
proved.  “Unknown” must be an explicit totalized semantic value, not a silent
meta-level failure.

**Verdict:** `PROVED`.

**What would change it.**  An admitted distinguishing contract and a sufficient
representation that identifies the two attainable states.

### FAR-CORE-013 — Omega as an eliminable derived materialized view

**Exact proposition and quantifiers.**  The ledger asserts that canonical FARA
`Omega` is a semantically eliminable derived materialized view.  The mathematical
form required is: on every consistent reachable state, `Omega=g(z)` for a
declared base state `z`, so projection `(z,Omega)|->z` is invertible on the graph
by `z|->(z,g(z))` and exact behavior factors through `z`.

**Premises actually available.**  Only the name “canonical FARA definition of
Omega” and the assertion that it is a derived view.  The definition/equation and
its domain are absent from the two allowed target artifacts.

**Conditional proof.**  If the graph premise holds, projection and reconstruction
are inverse on consistent reachable states, proving semantic eliminability.

**Strongest countermodel search.**  Equal `z` with two attainable `Omega`
values, an omitted dependency, or behaviorally relevant stale materialization
defeats eliminability.  The current record cannot decide whether any is allowed
by canonical FARA.

**Prior art.**  C-S11 and C-S17 establish generic view determinacy and
materialized-view patterns only.

**Dependencies.**  FAR-CORE-001 plus the missing application equation.

**Objections and limits.**  Calling a field “derived” is not evidence of a
single-valued total derivation over the claimed reachable domain.  Repository
usage or tests would be consistency evidence, not proof of the definition.

**Verdict:** `UNDERDETERMINED`.

**What would change it.**  An authoritative canonical definition and domain
proving `Omega=g(z)` on all relevant states would yield `PROVED`; an attainable
same-`z`/different-`Omega` counterexample affecting behavior would yield
`REFUTED`.

### FAR-CORE-014 — bounded Search-State Sufficiency

**Exact proposition and quantifiers.**  Only the representation and decoder
classes stated in PR #453 form a bounded supported/derived Search-State
Sufficiency factorization instance.  The claim is not about an open domain, any
other representation/decoder classes, or a universal architecture.

**Premises actually available.**  The ledger supplies the exact scope lock and
status label, but the classes, domain, behaviors, decoder equations, and evidence
are in PR #453, which is forbidden before controlled unblinding.

**Proof obligation.**  For every reachable state and behavior in the locked
class, the locked decoder must reproduce the behavior from the locked
representation; equivalently, no locked representation fiber may contain a
locked behavior collision.

**Strongest countermodel search.**  Any collision inside the locked classes
refutes the instance.  A behavior or architecture outside those classes can
refute a universal promotion but cannot refute this exact bounded claim.  No
in-scope instance can be constructed without reading the locked definitions.

**Prior art.**  C-S13 and C-S14 show mature adjacent state-abstraction and
predictive-state theories but cannot establish this application instance.  The
exact phrase search returned no relevant scholarly hit; that is not novelty
proof.

**Dependencies.**  FAR-CORE-001 plus the unread PR-#453 representation/decoder
specification and instance evidence.

**Objections and limits.**  The ledger's `supported_derived` label is not a
proof.  The scope must remain exactly PR-#453-bounded after unblinding even if
the evidence is persuasive.

**Verdict:** `UNDERDETERMINED`.

**What would change it.**  Complete locked definitions and a fiber-by-fiber
factorization proof would yield `PROVED`; an in-class behavior collision would
yield `REFUTED`; incomplete but precise evidence after unblinding could yield
`OPEN`.

## 5. Dependency and terminal-risk matrix

| Claim | Direct dependencies | Failure propagation |
|---|---|---|
| 001 | Set/image definitions | Would undermine 002, 011–014 factorization arguments. |
| 002 | 001, quotient construction | Would undermine least-representation language and part of 004. |
| 003 | typed closure/action stability | Local to dynamic quotient claims and any 014 use of them. |
| 004 | 002/partition order | Local to universal-minimum obstruction. |
| 005 | transformation-class inclusion | Local to invariance claims. |
| 006 | encoding equations vs structure | Bounds any host-capacity conclusion. |
| 007 | admitted presentation transformations | Local to primitive-count noninvariance. |
| 008 | finite tagged dispatcher | Local to finite operator-count noninvariance. |
| 009 | proper finite/open-domain distinction | Bounds any finite-panel universal conclusion. |
| 010 | explicit theory/residue definitions | Governs dependency declarations in logical comparisons. |
| 011 | 001 plus attainable collision | Feeds 012 and application sufficiency checks. |
| 012 | 001/011 plus distinguishing contract | Local to absence/Unknown preservation. |
| 013 | 001 plus canonical `Omega` equation | Missing application premise keeps full bundle underdetermined. |
| 014 | 001 plus exact PR-#453 classes/evidence | Missing application premise keeps full bundle underdetermined. |

## 6. Mandatory objection ledger at freeze

1. Reachable-image normalization must be confirmed; otherwise pathological
   ambient-codomain edges affect 001/002.
2. FAR-CORE-003 must not be promoted from sufficient context closure to a claim
   that the syntactic closure is necessary in every system.
3. FAR-CORE-004 must retain its exact nontrivial-domain and varying-contract
   hypotheses and must not be misreported as denial of universal sufficiency.
4. FAR-CORE-006 establishes non-entailment from bare codes, not that no common
   structure can ever be supplied by stronger morphism premises.
5. FAR-CORE-009 does not attack formally justified or probabilistic
   generalization with declared assumptions.
6. FAR-CORE-010's theory does not depend on `Gamma`; only the residue does.
7. FAR-CORE-011 requires an attainable retained-fiber collision, not syntactic
   omission alone.
8. FAR-CORE-013 and 014 remain application-underdetermined at freeze.
9. FAR-CORE-014's exact scope is immutable: only PR #453's stated representation
   and decoder classes, bounded supported/derived factorization, never a
   universal architecture.

## 7. Controlled-unblinding rule

After this file is committed and its content hash is recorded, Stage E may open
the protocol-authorized internal materials.  Stage E will classify prior
findings as independently reproduced, matched only after unblinding, or not
reproduced; identify genuinely new objections; and state any post-unblinding
verdict changes without modifying or replacing this frozen record.
