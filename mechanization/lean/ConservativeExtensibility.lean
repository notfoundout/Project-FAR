import Std
namespace FAR.CanonicalUniversality.ConservativeExtensibility

structure Kernel where
  State : Type
  valid : State → Prop

structure Extension (K : Kernel) where
  ExtendedState : Type
  embed : K.State → ExtendedState
  project : ExtendedState → K.State
  conservative : ∀ x, project (embed x) = x
  preservesValidity : ∀ x, K.valid x → K.valid (project (embed x))

theorem kernel_embeds_conservatively
    (K : Kernel) (E : Extension K) :
    (∀ x, E.project (E.embed x) = x) ∧
    (∀ x, K.valid x → K.valid (E.project (E.embed x))) := by
  exact ⟨E.conservative, E.preservesValidity⟩

end FAR.CanonicalUniversality.ConservativeExtensibility
