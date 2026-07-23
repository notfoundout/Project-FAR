import Std
namespace FAR.CanonicalUniversality.Canonicality

structure CategoryModel where
  Object : Type
  Hom : Object → Object → Type
  id : (x : Object) → Hom x x
  comp : {x y z : Object} → Hom x y → Hom y z → Hom x z

structure CanonicalKernel (C : CategoryModel) where
  kernel : C.Object
  factors : (x : C.Object) → C.Hom x kernel
  unique : ∀ x (f : C.Hom x kernel), f = factors x

theorem unique_factorization
    (C : CategoryModel) (K : CanonicalKernel C) (x : C.Object) :
    ∃! f : C.Hom x K.kernel, True := by
  refine ⟨K.factors x, trivial, ?_⟩
  intro f _
  exact K.unique x f

end FAR.CanonicalUniversality.Canonicality
