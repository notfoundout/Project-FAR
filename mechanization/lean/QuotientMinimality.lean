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

structure Isomorphism (A B : Type) where
  forward : A → B
  backward : B → A
  left_inv : ∀ x, backward (forward x) = x
  right_inv : ∀ y, forward (backward y) = y

theorem faithful_complete_quotient_is_kernel_up_to_equivalence
    (K : Kernel) (Q : Quotient K)
    (choose : Q.Target → K.State)
    (section : ∀ y, Q.map (choose y) = y)
    (separation : ∀ x y, ¬ K.distinguish x y → x = y) :
    Isomorphism K.State Q.Target := by
  refine { forward := Q.map, backward := choose, left_inv := ?_, right_inv := section }
  intro x
  apply separation
  apply Q.faithful
  exact section (Q.map x)

end FAR.CanonicalUniversality.QuotientMinimality
