import Std
namespace FAR.CanonicalUniversality.MaximalKnowability

structure Theory where
  System : Type
  warranted : System → Prop

structure ScopeOrder (A B : Theory) where
  embedding : A.System → B.System
  preservesWarrant : ∀ x, A.warranted x → B.warranted (embedding x)

/-- Any warranted scope extension must exhibit an explicit warrant-preserving embedding. -/
theorem any_stronger_warranted_scope_requires_embedding
    (A B : Theory) (S : ScopeOrder A B) :
    ∀ x, A.warranted x → B.warranted (S.embedding x) := by
  intro x hx
  exact S.preservesWarrant x hx

/-- A claimed stronger theory without such an embedding has not established scope dominance. -/
theorem no_embedding_no_registered_scope_dominance
    (A B : Theory)
    (hNoEmbedding : ¬ Nonempty (ScopeOrder A B)) :
    ¬ Nonempty (ScopeOrder A B) := hNoEmbedding

end FAR.CanonicalUniversality.MaximalKnowability
