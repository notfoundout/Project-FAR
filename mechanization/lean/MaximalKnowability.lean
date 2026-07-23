import Std
namespace FAR.CanonicalUniversality.MaximalKnowability

structure Theory where
  System : Type
  warranted : System → Prop

structure ScopeOrder (A B : Theory) where
  include : A.System → B.System
  preservesWarrant : ∀ x, A.warranted x → B.warranted (include x)

theorem any_stronger_warranted_scope_requires_embedding
    (A B : Theory) (S : ScopeOrder A B) :
    ∀ x, A.warranted x → B.warranted (S.include x) :=
  S.preservesWarrant

end FAR.CanonicalUniversality.MaximalKnowability
