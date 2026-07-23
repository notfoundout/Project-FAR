import Std
namespace FAR.CanonicalUniversality.RepresentationInvariance

structure Presentation where
  Carrier : Type
  invariant : Carrier → Nat

structure Equivalent (A B : Presentation) where
  forward : A.Carrier → B.Carrier
  backward : B.Carrier → A.Carrier
  forward_preserves : ∀ x, B.invariant (forward x) = A.invariant x
  backward_preserves : ∀ y, A.invariant (backward y) = B.invariant y

theorem invariant_under_equivalent_presentation
    (A B : Presentation) (E : Equivalent A B) (x : A.Carrier) :
    B.invariant (E.forward x) = A.invariant x :=
  E.forward_preserves x

end FAR.CanonicalUniversality.RepresentationInvariance
