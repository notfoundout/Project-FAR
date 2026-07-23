import Std

namespace FAR.CanonicalUniversality.Bridge

/-- What the already-proved G1-G3 stack directly supports. -/
structure DirectlySupported where
  relativeSemanticComposition : Prop
  openWorldStructuralLowerBound : Prop
  epistemicMaximalityBoundary : Prop

/-- Canonical-strengthening bridges not derivable from G1-G3 alone. -/
structure RemainingBridges where
  uniqueFactorizationForFAR : Prop
  representationInvariantRecovery : Prop
  quotientSeparationForFAR : Prop
  allReasoningInvariantsDefinable : Prop
  everyAdmissibleExtensionConservative : Prop
  warrantedScopeEmbedsIntoFAR : Prop

inductive BridgeVerdict where
  | full
  | partial
  | blocked
  deriving Repr, DecidableEq

def adjudicate (direct : DirectlySupported) (remaining : RemainingBridges) : BridgeVerdict :=
  if direct.relativeSemanticComposition ∧
     direct.openWorldStructuralLowerBound ∧
     direct.epistemicMaximalityBoundary then
    if remaining.uniqueFactorizationForFAR ∧
       remaining.representationInvariantRecovery ∧
       remaining.quotientSeparationForFAR ∧
       remaining.allReasoningInvariantsDefinable ∧
       remaining.everyAdmissibleExtensionConservative ∧
       remaining.warrantedScopeEmbedsIntoFAR then
      .full
    else
      .partial
  else
    .blocked

/-- Existing G1-G3 evidence warrants partial strengthening, not full canonicality. -/
theorem g1_g2_g3_only_adjudicates_partial
    (direct : DirectlySupported)
    (hDirect : direct.relativeSemanticComposition ∧
      direct.openWorldStructuralLowerBound ∧
      direct.epistemicMaximalityBoundary)
    (remaining : RemainingBridges)
    (hMissing : ¬ (remaining.uniqueFactorizationForFAR ∧
      remaining.representationInvariantRecovery ∧
      remaining.quotientSeparationForFAR ∧
      remaining.allReasoningInvariantsDefinable ∧
      remaining.everyAdmissibleExtensionConservative ∧
      remaining.warrantedScopeEmbedsIntoFAR)) :
    adjudicate direct remaining = .partial := by
  simp [adjudicate, hDirect, hMissing]

/-- Full canonical universality requires all six FAR-specific bridge witnesses. -/
theorem full_requires_every_far_bridge
    (direct : DirectlySupported)
    (remaining : RemainingBridges)
    (hFull : adjudicate direct remaining = .full) :
    remaining.uniqueFactorizationForFAR ∧
    remaining.representationInvariantRecovery ∧
    remaining.quotientSeparationForFAR ∧
    remaining.allReasoningInvariantsDefinable ∧
    remaining.everyAdmissibleExtensionConservative ∧
    remaining.warrantedScopeEmbedsIntoFAR := by
  unfold adjudicate at hFull
  split at hFull <;> simp_all

end FAR.CanonicalUniversality.Bridge
