import Std

namespace FAR.CanonicalUniversality.Bridge

structure DirectlySupported where
  relativeSemanticComposition : Prop
  openWorldStructuralLowerBound : Prop
  epistemicMaximalityBoundary : Prop

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

def DirectlySupported.all (d : DirectlySupported) : Prop :=
  d.relativeSemanticComposition ∧
  d.openWorldStructuralLowerBound ∧
  d.epistemicMaximalityBoundary

def RemainingBridges.all (r : RemainingBridges) : Prop :=
  r.uniqueFactorizationForFAR ∧
  r.representationInvariantRecovery ∧
  r.quotientSeparationForFAR ∧
  r.allReasoningInvariantsDefinable ∧
  r.everyAdmissibleExtensionConservative ∧
  r.warrantedScopeEmbedsIntoFAR

noncomputable def adjudicate
    (direct : DirectlySupported) (remaining : RemainingBridges) : BridgeVerdict := by
  classical
  exact if direct.all then
    if remaining.all then .full else .partial
  else .blocked

theorem g1_g2_g3_only_adjudicates_partial
    (direct : DirectlySupported)
    (hDirect : direct.all)
    (remaining : RemainingBridges)
    (hMissing : ¬ remaining.all) :
    adjudicate direct remaining = .partial := by
  classical
  simp [adjudicate, hDirect, hMissing]

theorem full_requires_every_far_bridge
    (direct : DirectlySupported)
    (remaining : RemainingBridges)
    (hFull : adjudicate direct remaining = .full) :
    remaining.all := by
  classical
  by_contra hMissing
  have hNotFull : adjudicate direct remaining ≠ .full := by
    unfold adjudicate
    split <;> simp_all
  exact hNotFull hFull

end FAR.CanonicalUniversality.Bridge
