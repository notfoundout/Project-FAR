# PCA-W1 Independent Review — Hostile Test and Countermodel Ledger

Review program: `PCA-W1-INDEPENDENT-REVIEW`  
Target: `14105775daf3c5713b134a728db2e1e53673af97`  
Prepared before Stage-D verdict freeze and before controlled unblinding.

## 1. Test conventions

This ledger consolidates the blind reconstructions, finite checks, and external
boundary research into explicit hostile tests.  A passing finite instance is
only a consistency check.  A countermodel is used only against a statement whose
scope includes it.  No repository test, prior audit, pull request, earlier
monograph, historical discussion, or application fixture has been read.

For an exact observation contract, write `beta:X -> B`, a representation
`r:X -> R`, and its reachable image `R* = im(r)`.  Image-level exact sufficiency
means that some `d:R* -> B` satisfies `beta = d o r`.  The representation order
is the factorization/information order, normalized to reachable images unless a
claim explicitly requires arbitrary unused codomain labels.

## 2. Claim-by-claim hostile tests

### FAR-CORE-001 — exact factorization

**Positive proof test.**  If `beta=d o r`, equal `r` values have equal `beta`
values.  Conversely, if `ker(r) subseteq ker(beta)`, define
`d(r(x))=beta(x)` on `R*`.  Kernel inclusion makes this well-defined and proves
image-level factorization.

**Collision countermodel to an overbroad sufficiency assertion.**  Let
`X={a,b}`, `r(a)=r(b)=rho`, and `beta(a)=0`, `beta(b)=1`.  No decoder can map
`rho` to both outputs.

**Total-whole-codomain edge.**  Let `X` be empty, `R={rho}`, and `B` be empty.
The unique maps `r:X->R` and `beta:X->B` have vacuous kernel inclusion, and the
image-level decoder `empty -> empty` exists.  No total map `R->B` exists.  Thus
the unqualified whole-codomain version needs `R=im(r)`, an inhabited `B`, or an
extension premise.  This is not a countermodel to the normalized image theorem.

**Falsifier for the normalized theorem.**  A concrete `x,y` with `r(x)=r(y)`
and `beta(x)!=beta(y)` together with a purported decoder, or a well-typed
image-level factorization with such a collision.

### FAR-CORE-002 — quotient minimality and uniqueness

Let `x ~beta y` iff `beta(x)=beta(y)` and let `q:X->X/~beta` be the quotient.
The behavior factors through `q`.  Every sufficient `r` satisfies
`ker(r) subseteq ~beta`; hence `[x]_beta` is a well-defined function of `r(x)`.
This places `q` below every sufficient representation in the information order.
If another normalized reachable representation is also least, mutual
factorizations are inverse bijections on reachable images.

**Unused-label countermodel to unnormalized uniqueness.**  Replace a least
representation `q:X->Q` by the same map regarded as landing in
`Q disjoint_union J`, where `J` is an arbitrary unreachable set.  Behavior and
information on `X` are unchanged, but whole codomains need not be isomorphic.
Uniqueness therefore concerns reachable images (or explicitly reduced
representations), not arbitrary ambient codomains.

**Measurable/statistical boundary.**  Landers–Rogge gives statistical families
without a minimal sufficient statistic.  That does not attack the extensional
Set quotient, but blocks promotion to unrestricted measurable/statistical
minimality.

**Cardinality boundary.**  For finite `X`, any sufficient `r` has at least as
many reachable values as `X/~beta`.  Infinite cardinal comparison is unnecessary
to the ledger's expressly finite cardinal-minimum subclaim.

### FAR-CORE-003 — dynamics and context closure

**Failure without closure/action compatibility.**  Let
`X={a,b,c}`, `beta(a)=beta(b)=0`, `beta(c)=1`, and one action `u` satisfy
`u(a)=a`, `u(b)=c`.  Current observations equate `a` and `b`, but their
successors are observably different, so the quotient transition is not
well-defined.

**Closure repair.**  Include every declared continuation test `t o u` whenever
`t` is admitted.  Equality on the resulting observation vector implies equality
after each action for every component test, so the equivalence is action stable
and the quotient dynamics descends.

**Non-necessity boundary.**  A constant observation has a one-class quotient,
which is stable under every total action even if the declared test set was not
constructed as a continuation closure.  Thus closure is a general sufficient
construction, not a logically necessary syntactic condition in every accidental
system.

**Typing objection.**  Partial actions, nondeterminism, probability, and
history-sensitive tests require their own composition/equality semantics.  The
Set proof does not silently supply those.

### FAR-CORE-004 — no contract-independent least representation

For any `X` with distinct `a,b`, take a constant contract `beta_0` and an
injective contract `beta_1`.  The one-point representation is least for
`beta_0`.  Any representation sufficient for `beta_1` must be injective and
therefore cannot be isomorphic in information content to the one-point least
representation.  Hence no single representation is least sufficient for both,
although the identity is sufficient for both.

**Minimal hostile domain.**  Exhaustive enumeration for `|X|=2` confirms the
partition argument.  The proof extends to every larger nonempty `X` by the same
constant/injective pair.

**Boundary countermodels to omitted hypotheses.**  If `|X|<=1`, constant and
injective partitions coincide.  If the contract class is restricted to a
single observational partition, its quotient can be universally least within
that class.  Thus nontriviality and genuinely varying contracts are essential.

### FAR-CORE-005 — antitone invariants

For nested transformation classes `G subseteq H`, a predicate invariant under
every `h in H` is invariant under every `g in G`; therefore
`Inv(H) subseteq Inv(G)`.

**Strictness witness.**  On `{0,1}`, let `G={id}` and let `H` add the swap.  The
property “the selected value is 0” is `G`-invariant but not `H`-invariant.

**Equality boundary.**  A property invariant under all permutations belongs to
both sets, so strict inclusion is not guaranteed.

**Scope failure.**  For nonnested transformation classes or incompatible
actions/transport semantics, no antitone comparison follows.

### FAR-CORE-006 — encoding capacity versus native structure

Let a two-element group and a two-element left-zero semigroup use the same two
host tokens as lossless element codes.  Their encoders and image decoders can be
identical.  The source multiplications are nevertheless different and the
encoding equations alone impose no host operation preserving either one.

More generally, keep all underlying sets, injections, and decoders fixed while
varying an arbitrary source relation or operation.  Any claimed structural
conclusion that changes across those structures is not entailed by the code
data.

**Boundary.**  If a common signature and homomorphism/interpretation laws are
added, genuine shared structure may be proved.  The negative claim is not a
denial of that strengthened theorem.

**Definitional objection.**  “Native common structure” is not itself classified
until a signature, admissible morphisms, and semantics are declared.  The
rigorous core is the non-entailment of any specified structural conclusion from
injective coding plus decoding alone.

### FAR-CORE-007 — primitive vocabulary count

A Boolean presentation may use a conventional finite family such as
`{and,not}`, while an equivalent presentation uses a single Sheffer operation
from which those operations are defined.  Faithful reification/tagging can also
turn named primitives into data plus a generic interpreter.  Primitive-symbol
count changes while recoverable behavior is preserved.

**Boundary.**  Counts can be meaningful after fixing signature, sorts, arities,
allowed definitions, computational cost, continuity, or other presentation
rules.  Noninvariance is only under the declared reification/tagging regime.

### FAR-CORE-008 — finite operator count

Given finite operators `f_i` of declared finite arities, encode each admissible
argument tuple with tag `i` and define one dispatcher `D(i,args)=f_i(args)`.
Conversely, each original operator is recovered by fixing its tag.  The count
has changed without loss on the encoded domain.

**Boundary countermodel to overextension.**  Without admitted tags/products,
with a fixed homogeneous arity/sort, or with continuity/complexity constraints,
one dispatcher may be inadmissible.  An arbitrary infinite operator family does
not follow from the finite tagged-tuple construction.

### FAR-CORE-009 — finite panel versus open universality

Let `D_0` be a proper finite subset of an open target domain `D`; choose
`x* in D\D_0`.  Define two candidate laws that agree on every point of `D_0`
and disagree at `x*`.  All panel results are identical, while the universal
claims differ.  Therefore the finite observations alone do not entail the open
universal.

**Boundary.**  A coverage theorem, finite complete basis, induction principle,
parametric identifiability assumption, or probabilistic learning bound can
support a qualified generalization.  The claim does not deny those strengthened
arguments.

### FAR-CORE-010 — theory and residue dependencies

With fixed language `L` and fixed indexed models `M_i`,
`T=intersection_i Th_L(M_i)` contains no occurrence of `Gamma` in its
definition.  Thus changing only `Gamma` cannot change `T`.  The residue
`R_Gamma=T\Cn_L(Gamma)` explicitly depends on `Gamma`.

**Change witness.**  In propositional language with atom `p`, take a one-model
panel in which `p` is true.  Then `p in T`.  With `Gamma=empty`, `p` is in the
residue; with `Gamma={p}`, it is not.  This proves that the residue *can*, not
must, change.

**Boundaries.**  Changing `L`, the index set, an interpretation, or a model can
change `T`.  Empty intersections require a declared convention.  The set
difference called a residue need not itself be deductively closed.  Comparing
different languages needs translations.

### FAR-CORE-011 — omitted consequence-affecting parameter

Let full states be `(z,p)` and let a proposed representation retain only `z`.
If attainable states `(z,p_0)` and `(z,p_1)` have different contractual behavior,
they collide in the representation and no exact decoder exists.  This is the
FAR-CORE-001 collision test.

**Boundary.**  A syntactically omitted parameter that is fixed, unreachable,
recoverable from `z`, or behaviorally irrelevant does not refute sufficiency.
“Consequence-affecting” must denote an attainable collision or equivalent
no-decoder argument.

### FAR-CORE-012 — absence versus Unknown

Let attainable states `x_abs` and `x_unk` denote absence and explicit Unknown,
and admit a contract with different outputs on them.  Any representation that
identifies the states violates the kernel condition and is insufficient.

**Boundary.**  If no admitted contract distinguishes them, or one state is
unreachable, exact sufficiency does not require preserving the distinction.
This is a conditional contract theorem, not a universal ontology of nulls.

### FAR-CORE-013 — eliminable derived view

For a base state `z` and a single-valued definition `Omega=g(z)`, the consistent
reachable state space is the graph `{(z,g(z))}`.  Projection to `z` and the map
`z |-> (z,g(z))` are inverse.  Every exact behavior on consistent states factors
through `z`; `Omega` is a derived materialized view in this formal sense.

**Countermodels to omitted application premises.**  If equal `z` values can
coexist with distinct attainable `Omega` values, if `Omega` depends on an
omitted parameter, or if a stored view may be stale and staleness affects the
contract, no function `g(z)` supplies the inverse.  Generic database literature
does not prove the canonical Project FAR equation.

**Pre-unblinding objection.**  The allowed v1.1 monograph and machine ledger
name a canonical definition but do not state it.  The generic graph theorem is
proved; its Project FAR instantiation is not yet auditable.

### FAR-CORE-014 — bounded Search-State Sufficiency

The exact scope is locked to *only the representation and decoder classes stated
in PR #453*, as a bounded supported/derived factorization instance, not a
universal architecture.  PR #453 remains unread before the Stage-D freeze.

**Generic pass condition.**  For every state in the locked domain and every
behavior in the locked target class, the stated decoder must reproduce the
behavior from the stated representation.  Equivalently, no two reachable states
identified by that representation may differ on any locked behavior.

**Generic hostile extension.**  Add a behavior outside the locked class that
distinguishes a representation collision, or add a representation/decoder class
not covered by the evidence.  That immediately defeats any universal promotion
while leaving the bounded instance untouched.

**Pre-unblinding objection.**  Neither the exact classes nor their instance
evidence appears in the Stage-A/B allowed artifacts.  No number of adjacent MDP
or predictive-state papers can fill that application-specific gap.

## 3. Finite computational cross-checks

The independently written Python enumerator committed with Stage A checked:

- 11,141 finite representation/behavior pairs for the factorization/kernel
  equivalence;
- 11,141 quotient-minimality comparisons;
- constant/injective universal-minimum obstructions for domain sizes 2 through
  5; and
- 26,122 finite transition/equivalence instances for the descent criterion.

All encoded instances passed.  The exact script and captured output are part of
the review evidence.  These runs support implementation consistency only; the
proofs and countermodels above carry the mathematical burden.

## 4. Objections carried into verdict freeze

1. FAR-CORE-001/002 must be read on reachable images or must add a total
   whole-codomain extension premise; otherwise empty/unreachable-label edges
   defeat the unqualified wording.
2. FAR-CORE-003 requires typed action/test composition; closure is sufficient,
   not universally necessary.
3. FAR-CORE-006's negative non-entailment is precise, but “native common
   structure” needs a declared structural language for positive use.
4. FAR-CORE-013 lacks its application equation before unblinding.
5. FAR-CORE-014 lacks its exact locked classes and evidence before unblinding;
   its scope must not change when those materials are opened.

No Stage-D claim status is assigned in this ledger.
