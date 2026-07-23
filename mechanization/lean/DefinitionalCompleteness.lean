import Std
namespace FAR.CanonicalUniversality.DefinitionalCompleteness

structure Kernel where
  State : Type

structure ReasoningInvariant (K : Kernel) where
  Value : Type
  evaluate : K.State → Value

structure CompleteBasis (K : Kernel) where
  Basis : Type
  encode : K.State → Basis
  define : (I : ReasoningInvariant K) → Basis → I.Value
  complete : ∀ (I : ReasoningInvariant K) (x : K.State), define I (encode x) = I.evaluate x

theorem every_registered_invariant_factors_through_basis
    (K : Kernel) (B : CompleteBasis K)
    (I : ReasoningInvariant K) :
    ∃ f : B.Basis → I.Value, ∀ x, f (B.encode x) = I.evaluate x := by
  exact ⟨B.define I, B.complete I⟩

end FAR.CanonicalUniversality.DefinitionalCompleteness
