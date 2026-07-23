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

def FullCanonicalBridge
    (direct : DirectlySupported) (remaining : RemainingBridges) : Prop :=
  direct.all ∧ remaining.all

def PartialCanonicalBridge
    (direct : DirectlySupported) (remaining : RemainingBridges) : Prop :=
  direct.all ∧ ¬ remaining.all

theorem g1_g2_g3_only_support_partial_bridge
    (direct : DirectlySupported)
    (remaining : RemainingBridges)
    (hDirect : direct.all)
    (hMissing : ¬ remaining.all) :
    PartialCanonicalBridge direct remaining := by
  exact ⟨hDirect, hMissing⟩

theorem full_requires_every_far_bridge
    (direct : DirectlySupported)
    (remaining : RemainingBridges)
    (hFull : FullCanonicalBridge direct remaining) :
    remaining.all := by
  exact hFull.2

theorem partial_excludes_full
    (direct : DirectlySupported)
    (remaining : RemainingBridges)
    (hPartial : PartialCanonicalBridge direct remaining) :
    ¬ FullCanonicalBridge direct remaining := by
  intro hFull
  exact hPartial.2 hFull.2

end FAR.CanonicalUniversality.Bridge
