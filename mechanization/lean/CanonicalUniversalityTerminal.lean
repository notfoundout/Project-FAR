import Std
namespace FAR.CanonicalUniversality.Terminal

structure StrengtheningObligations where
  canonicality : Prop
  representationInvariance : Prop
  quotientMinimality : Prop
  definitionalCompleteness : Prop
  conservativeExtensibility : Prop
  maximalKnowability : Prop

structure Established (O : StrengtheningObligations) : Prop where
  hCanonicality : O.canonicality
  hInvariance : O.representationInvariance
  hMinimality : O.quotientMinimality
  hCompleteness : O.definitionalCompleteness
  hExtensibility : O.conservativeExtensibility
  hKnowability : O.maximalKnowability

def CanonicalUniversality (O : StrengtheningObligations) : Prop :=
  O.canonicality ∧ O.representationInvariance ∧ O.quotientMinimality ∧
  O.definitionalCompleteness ∧ O.conservativeExtensibility ∧ O.maximalKnowability

theorem canonical_universality_terminal_theorem
    (O : StrengtheningObligations) (h : Established O) :
    CanonicalUniversality O := by
  exact ⟨h.hCanonicality, h.hInvariance, h.hMinimality,
    h.hCompleteness, h.hExtensibility, h.hKnowability⟩

/-- Failure of any independent obligation blocks the full terminal conjunction. -/
theorem missing_canonicality_blocks_terminal
    (O : StrengtheningObligations) (h : ¬ O.canonicality) :
    ¬ CanonicalUniversality O := by
  intro hall
  exact h hall.1

end FAR.CanonicalUniversality.Terminal
