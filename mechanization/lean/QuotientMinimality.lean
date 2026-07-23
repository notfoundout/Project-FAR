import Std
namespace FAR.CanonicalUniversality.QuotientMinimality

structure Kernel where
  State : Type
  distinguish : State → State → Prop

structure Quotient (K : Kernel) where
  Target : Type
  map : K.State → Target
  faithful : ∀ x y, map x = map y → ¬ K.distinguish x y
  complete : ∀ x y, ¬ K.distinguish x y → map x = map y

/-- Separation states that only identical kernel states are structurally indistinguishable. -/
def Separated (K : Kernel) : Prop :=
  ∀ x y, ¬ K.distinguish x y → x = y

/-- A faithful quotient of a separated kernel cannot identify distinct kernel states. -/
theorem faithful_quotient_is_injective
    (K : Kernel) (Q : Quotient K) (hSeparated : Separated K) :
    ∀ x y, Q.map x = Q.map y → x = y := by
  intro x y hxy
  exact hSeparated x y (Q.faithful x y hxy)

/-- A complete quotient identifies exactly the structurally indistinguishable states. -/
theorem complete_quotient_characterizes_equivalence
    (K : Kernel) (Q : Quotient K) :
    ∀ x y, Q.map x = Q.map y ↔ ¬ K.distinguish x y := by
  intro x y
  constructor
  · exact Q.faithful x y
  · exact Q.complete x y

/-- Under separation, every faithful and complete quotient is minimal up to injective renaming. -/
theorem quotient_minimality
    (K : Kernel) (Q : Quotient K) (hSeparated : Separated K) :
    (∀ x y, Q.map x = Q.map y ↔ x = y) := by
  intro x y
  constructor
  · exact faithful_quotient_is_injective K Q hSeparated x y
  · intro h
    cases h
    rfl

end FAR.CanonicalUniversality.QuotientMinimality
