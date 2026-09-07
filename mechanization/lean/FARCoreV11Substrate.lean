import Std

/-!
# Project FAR core theory v1.1: exact-contract substrate

This module formalizes FAR-CORE-001--003 under the exact, Set-based contract used by the
governing theory.  A decoder is required only on the reachable image of a representation.
Nothing here selects an observation contract or asserts contract-free minimality.
-/

namespace FARCoreV11

universe u v w

/-- The reachable part of a representation (defined without a mathlib dependency). -/
abbrev RepImage {X : Type u} {R : Type w} (rho : X -> R) :=
  {represented : R // ∃ x, rho x = represented}

/-- A source value regarded as a member of the reachable representation image. -/
def imageValue {X : Type u} {R : Type w} (rho : X -> R) (x : X) : RepImage rho :=
  ⟨rho x, ⟨x, rfl⟩⟩

/-- Exact sufficiency is factorization through a decoder on the reachable image. -/
def ExactlySufficient {X : Type u} {B : Type v} {R : Type w}
    (beta : X -> B) (rho : X -> R) : Prop :=
  ∃ decoder : RepImage rho -> B, ∀ x, decoder (imageValue rho x) = beta x

/-- Every collision of `rho` must also be a collision of the declared behavior. -/
def KernelRefines {X : Type u} {B : Type v} {R : Type w}
    (rho : X -> R) (beta : X -> B) : Prop :=
  ∀ ⦃x y⦄, rho x = rho y -> beta x = beta y

/-- Two maps induce exactly the same collision relation. -/
def KernelEqual {X : Type u} {B : Type v} {R : Type w}
    (rho : X -> R) (beta : X -> B) : Prop :=
  ∀ x y, rho x = rho y ↔ beta x = beta y

/-- Function injectivity, kept local so the file depends only on Lean/Std. -/
def IsInjective {A : Type u} {B : Type v} (f : A -> B) : Prop :=
  ∀ ⦃x y⦄, f x = f y -> x = y

/-- Function surjectivity, kept local so the file depends only on Lean/Std. -/
def IsSurjective {A : Type u} {B : Type v} (f : A -> B) : Prop :=
  ∀ y, ∃ x, f x = y

/-- A small explicit isomorphism record; no imported equivalence library is required. -/
structure Isomorphism (A : Type u) (B : Type v) where
  toFun : A -> B
  invFun : B -> A
  left_inv : ∀ x, invFun (toFun x) = x
  right_inv : ∀ y, toFun (invFun y) = y

/-- A bijection supplies an explicit isomorphism (using choice for the inverse). -/
noncomputable def isomorphismOfBijective {A : Type u} {B : Type v}
    (f : A -> B) (hinjective : IsInjective f) (hsurjective : IsSurjective f) :
    Isomorphism A B where
  toFun := f
  invFun := fun y => Classical.choose (hsurjective y)
  left_inv := by
    intro x
    apply hinjective
    exact Classical.choose_spec (hsurjective (f x))
  right_inv := by
    intro y
    exact Classical.choose_spec (hsurjective y)

/-- FAR-CORE-001: exact factorization is equivalent to kernel refinement. -/
theorem exact_factorization_criterion {X : Type u} {B : Type v} {R : Type w}
    (beta : X -> B) (rho : X -> R) :
    ExactlySufficient beta rho ↔ KernelRefines rho beta := by
  constructor
  · rintro ⟨decoder, hdecoder⟩ x y hxy
    rw [← hdecoder x, ← hdecoder y]
    apply congrArg decoder
    apply Subtype.ext
    exact hxy
  · intro hrefines
    classical
    let decoder : RepImage rho -> B := fun represented =>
      beta (Classical.choose represented.property)
    refine ⟨decoder, ?_⟩
    intro x
    apply hrefines
    exact Classical.choose_spec (imageValue rho x).property

/-- FAR-CORE-001 negative direction: a behavior-separating collision refutes sufficiency. -/
theorem collision_refutes_sufficiency {X : Type u} {B : Type v} {R : Type w}
    (beta : X -> B) (rho : X -> R) {x y : X}
    (representationCollision : rho x = rho y)
    (behaviorSeparation : beta x ≠ beta y) :
    ¬ ExactlySufficient beta rho := by
  rintro ⟨decoder, hdecoder⟩
  apply behaviorSeparation
  rw [← hdecoder x, ← hdecoder y]
  apply congrArg decoder
  apply Subtype.ext
  exact representationCollision

/-! ## FAR-CORE-002: the observational quotient -/

/-- Equality of declared behavior as a Setoid on source cases. -/
def behaviorSetoid {X : Type u} {B : Type v} (beta : X -> B) : Setoid X where
  r x y := beta x = beta y
  iseqv := {
    refl := fun _ => rfl
    symm := fun h => h.symm
    trans := fun hxy hyz => hxy.trans hyz
  }

/-- The exact observational quotient induced by `beta`. -/
abbrev ObservationalQuotient {X : Type u} {B : Type v} (beta : X -> B) :=
  Quotient (behaviorSetoid beta)

/-- Canonical projection to the observational quotient. -/
def quotientRep {X : Type u} {B : Type v} (beta : X -> B) (x : X) :
    ObservationalQuotient beta :=
  Quotient.mk (behaviorSetoid beta) x

/-- Behavior descends exactly to the observational quotient. -/
def quotientBehavior {X : Type u} {B : Type v} (beta : X -> B) :
    ObservationalQuotient beta -> B :=
  Quotient.lift beta (fun _ _ h => h)

/-- FAR-CORE-002: the observational quotient itself is exactly sufficient. -/
theorem quotient_is_sufficient {X : Type u} {B : Type v} (beta : X -> B) :
    ExactlySufficient beta (quotientRep beta) := by
  refine ⟨fun represented => quotientBehavior beta represented.val, ?_⟩
  intro x
  rfl

/-- The canonical factor from any kernel-refining representation image to the quotient. -/
noncomputable def factorToQuotient {X : Type u} {B : Type v} {R : Type w}
    (rho : X -> R) (beta : X -> B) :
    RepImage rho -> ObservationalQuotient beta :=
  fun represented => quotientRep beta (Classical.choose represented.property)

theorem factorToQuotient_agrees {X : Type u} {B : Type v} {R : Type w}
    (rho : X -> R) (beta : X -> B) (hrefines : KernelRefines rho beta) (x : X) :
    factorToQuotient rho beta (imageValue rho x) = quotientRep beta x := by
  apply Quotient.sound
  exact hrefines (Classical.choose_spec (imageValue rho x).property)

/-- FAR-CORE-002: every sufficient image has a unique map to the observational quotient. -/
theorem observational_quotient_universal {X : Type u} {B : Type v} {R : Type w}
    (beta : X -> B) (rho : X -> R) (hsufficient : ExactlySufficient beta rho) :
    ∃ factor : RepImage rho -> ObservationalQuotient beta,
      (∀ x, factor (imageValue rho x) = quotientRep beta x) ∧
      ∀ other : RepImage rho -> ObservationalQuotient beta,
        (∀ x, other (imageValue rho x) = quotientRep beta x) -> other = factor := by
  let hrefines := (exact_factorization_criterion beta rho).mp hsufficient
  refine ⟨factorToQuotient rho beta,
    factorToQuotient_agrees rho beta hrefines, ?_⟩
  intro other hother
  funext represented
  obtain ⟨x, hx⟩ := represented.property
  have represented_eq : represented = imageValue rho x := by
    apply Subtype.ext
    exact hx.symm
  rw [represented_eq, hother x]
  exact (factorToQuotient_agrees rho beta hrefines x).symm

/-- A sufficient representation image always maps surjectively to the exact quotient. -/
theorem factorToQuotient_surjective {X : Type u} {B : Type v} {R : Type w}
    (beta : X -> B) (rho : X -> R) (hsufficient : ExactlySufficient beta rho) :
    IsSurjective
      (factorToQuotient rho beta) := by
  intro quotientValue
  refine Quotient.inductionOn quotientValue (fun x => ?_)
  exact ⟨imageValue rho x,
    factorToQuotient_agrees rho beta
      ((exact_factorization_criterion beta rho).mp hsufficient) x⟩

theorem factorToQuotient_injective_of_kernel_equal
    {X : Type u} {B : Type v} {R : Type w}
    (rho : X -> R) (beta : X -> B) (hkernels : KernelEqual rho beta) :
    IsInjective (factorToQuotient rho beta) := by
  intro represented₁ represented₂ hequal
  apply Subtype.ext
  rw [← Classical.choose_spec represented₁.property,
    ← Classical.choose_spec represented₂.property]
  apply (hkernels _ _).mpr
  exact congrArg (quotientBehavior beta) hequal

/-- Kernel equality makes the universal factor an isomorphism, i.e. least-informative. -/
noncomputable def leastInformativeImageEquiv
    {X : Type u} {B : Type v} {R : Type w}
    (rho : X -> R) (beta : X -> B) (hkernels : KernelEqual rho beta) :
    Isomorphism (RepImage rho) (ObservationalQuotient beta) := by
  let hrefines : KernelRefines rho beta := fun {_ _} h => (hkernels _ _).mp h
  let hsufficient : ExactlySufficient beta rho :=
    (exact_factorization_criterion beta rho).mpr hrefines
  exact isomorphismOfBijective (factorToQuotient rho beta)
    (factorToQuotient_injective_of_kernel_equal rho beta hkernels)
    (factorToQuotient_surjective beta rho hsufficient)

/-- `rho` is a least-informative exact-sufficient representation for `beta`: it is exactly
sufficient, and every exactly sufficient representation is at least as informative, i.e. every
collision of that representation is already a collision of `rho`.

The comparison class is representations into `Type u`, the universe of the case type `X`.  That
is the universe of the observational quotient, so the class always contains the canonical
minimal representative; it is not a claim about representations in larger universes. -/
def LeastInformativeSufficient {X : Type u} {B : Type v} {R : Type w}
    (beta : X -> B) (rho : X -> R) : Prop :=
  ExactlySufficient beta rho ∧
    ∀ (S : Type u) (sigma : X -> S), ExactlySufficient beta sigma -> KernelRefines sigma rho

/-- Least-informative sufficiency is exactly kernel equality with the declared behavior.

This is the bridge the governing prose assumes.  `FAR-CORE-002` and `FAR-CORE-004` are stated
about least-informative sufficient representations, while the substrate theorems are stated
about kernel equality; the governing ledger records `least informative means ker rho equals
ker beta` as a premise.  This theorem derives that identification instead of assuming it, so
the kernel-equality results carry the minimality claims they are cited for. -/
theorem leastInformativeSufficient_iff_kernelEqual
    {X : Type u} {B : Type v} {R : Type w} (beta : X -> B) (rho : X -> R) :
    LeastInformativeSufficient beta rho ↔ KernelEqual rho beta := by
  constructor
  · rintro ⟨hsufficient, hminimal⟩ x y
    have hrefines : KernelRefines rho beta :=
      (exact_factorization_criterion beta rho).mp hsufficient
    constructor
    · intro representationCollision
      exact hrefines representationCollision
    · intro behaviorAgreement
      exact hminimal (ObservationalQuotient beta) (quotientRep beta)
        (quotient_is_sufficient beta) (Quotient.sound behaviorAgreement)
  · intro hkernels
    have hrefines : KernelRefines rho beta := fun {_ _} h => (hkernels _ _).mp h
    refine ⟨(exact_factorization_criterion beta rho).mpr hrefines, ?_⟩
    intro S sigma hsigma
    exact fun {x y} representationCollision =>
      (hkernels x y).mpr
        ((exact_factorization_criterion beta sigma).mp hsigma representationCollision)

/-- The minimum is attained, so `LeastInformativeSufficient` is not vacuous. -/
theorem quotient_is_least_informative_sufficient {X : Type u} {B : Type v} (beta : X -> B) :
    LeastInformativeSufficient beta (quotientRep beta) := by
  refine (leastInformativeSufficient_iff_kernelEqual beta (quotientRep beta)).mpr ?_
  intro x y
  constructor
  · intro representationCollision
    -- `quotientBehavior` computes on `quotientRep`, so this avoids `Quotient.exact` and keeps
    -- the kernel dependency set equal to that of `leastInformativeImageEquiv`.
    exact congrArg (quotientBehavior beta) representationCollision
  · intro behaviorAgreement
    exact Quotient.sound behaviorAgreement

/-! ## FAR-CORE-003: declared context closure -/

/-- Indistinguishability by every declared test/context. -/
def ObservationallyEquivalent {T : Type u} {X : Type v} {V : Type w}
    (obs : T -> X -> V) (x y : X) : Prop :=
  ∀ test, obs test x = obs test y

/-- The Setoid generated by declared observational equivalence. -/
def observationSetoid {T : Type u} {X : Type v} {V : Type w}
    (obs : T -> X -> V) : Setoid X where
  r := ObservationallyEquivalent obs
  iseqv := {
    refl := fun _ _ => rfl
    symm := fun h test => (h test).symm
    trans := fun hxy hyz test => (hxy test).trans (hyz test)
  }

/-- Every test after the action is represented by a declared pre-action test. -/
def ContextClosedFor {T : Type u} {X : Type v} {V : Type w}
    (obs : T -> X -> V) (action : X -> X) : Prop :=
  ∀ test, ∃ continued : T, ∀ x, obs test (action x) = obs continued x

/-- FAR-CORE-003: typed semantic continuation closure makes the action compatible. -/
theorem action_preserves_observational_equivalence
    {T : Type u} {X : Type v} {V : Type w}
    (obs : T -> X -> V) (action : X -> X)
    (hclosed : ContextClosedFor obs action) {x y : X}
    (hequivalent : ObservationallyEquivalent obs x y) :
    ObservationallyEquivalent obs (action x) (action y) := by
  intro test
  obtain ⟨continued, hcontinued⟩ := hclosed test
  rw [hcontinued x, hcontinued y]
  exact hequivalent continued

/-- The action descended to observational-equivalence classes. -/
def descendAction {T : Type u} {X : Type v} {V : Type w}
    (obs : T -> X -> V) (action : X -> X)
    (hclosed : ContextClosedFor obs action) :
    Quotient (observationSetoid obs) -> Quotient (observationSetoid obs) :=
  Quotient.lift
    (fun x => Quotient.mk (observationSetoid obs) (action x))
    (fun _ _ h => Quotient.sound
      (action_preserves_observational_equivalence obs action hclosed h))

end FARCoreV11
