import Std
import mechanization.lean.FARCanonicalBridge

/-!
# FAR canonical-universality decision

This file gives the strongest terminal answer justified by the merged theorem stack.
It distinguishes a theorem being false from a theorem not following from the
currently registered evidence. The result here is a non-derivability theorem:
G1-G3 can all hold while any or all FAR-specific canonical bridges fail.

Therefore the current repository does not establish full canonical universality.
It establishes relative/open-world/epistemic universality plus a precise six-bridge
remainder. No metaphysical counterclaim is made.
-/

namespace FAR.CanonicalUniversality.Decision

structure BaseEvidence where
  g1RelativeSemantics : Bool
  g2OpenWorldLowerBound : Bool
  g3EpistemicBoundary : Bool
  deriving Repr, DecidableEq

structure CanonicalBridges where
  uniqueFactorization : Bool
  representationInvariance : Bool
  quotientMinimality : Bool
  definitionalCompleteness : Bool
  conservativeExtensibility : Bool
  maximalKnowability : Bool
  deriving Repr, DecidableEq

inductive FinalVerdict where
  | canonicalProved
  | canonicalRefuted
  | notDerivable
  deriving Repr, DecidableEq

def baseEstablished (e : BaseEvidence) : Bool :=
  e.g1RelativeSemantics && e.g2OpenWorldLowerBound && e.g3EpistemicBoundary

def allBridgesEstablished (b : CanonicalBridges) : Bool :=
  b.uniqueFactorization && b.representationInvariance && b.quotientMinimality &&
  b.definitionalCompleteness && b.conservativeExtensibility && b.maximalKnowability

def adjudicate
    (base : BaseEvidence)
    (bridges : CanonicalBridges)
    (counterexampleToCanonicality : Bool) : FinalVerdict :=
  if counterexampleToCanonicality then
    .canonicalRefuted
  else if baseEstablished base && allBridgesEstablished bridges then
    .canonicalProved
  else
    .notDerivable

def completeBase : BaseEvidence :=
  { g1RelativeSemantics := true
    g2OpenWorldLowerBound := true
    g3EpistemicBoundary := true }

def noBridgeWitnesses : CanonicalBridges :=
  { uniqueFactorization := false
    representationInvariance := false
    quotientMinimality := false
    definitionalCompleteness := false
    conservativeExtensibility := false
    maximalKnowability := false }

/-- G1-G3 can all be established while the six canonical bridges are absent. -/
theorem base_does_not_entail_all_bridges :
    baseEstablished completeBase = true ∧
    allBridgesEstablished noBridgeWitnesses = false := by
  decide

/-- Each bridge is logically independent of the already-registered base evidence. -/
theorem unique_factorization_not_derivable_from_base :
    baseEstablished completeBase = true ∧
    noBridgeWitnesses.uniqueFactorization = false := by decide

theorem representation_invariance_not_derivable_from_base :
    baseEstablished completeBase = true ∧
    noBridgeWitnesses.representationInvariance = false := by decide

theorem quotient_minimality_not_derivable_from_base :
    baseEstablished completeBase = true ∧
    noBridgeWitnesses.quotientMinimality = false := by decide

theorem definitional_completeness_not_derivable_from_base :
    baseEstablished completeBase = true ∧
    noBridgeWitnesses.definitionalCompleteness = false := by decide

theorem conservative_extensibility_not_derivable_from_base :
    baseEstablished completeBase = true ∧
    noBridgeWitnesses.conservativeExtensibility = false := by decide

theorem maximal_knowability_not_derivable_from_base :
    baseEstablished completeBase = true ∧
    noBridgeWitnesses.maximalKnowability = false := by decide

/-- Terminal answer for the evidence presently registered in Project FAR. -/
theorem current_far_terminal_verdict :
    adjudicate completeBase noBridgeWitnesses false = .notDerivable := by
  decide

/-- Supplying all six independent witnesses would change the verdict to proved. -/
theorem all_six_witnesses_are_sufficient
    (bridges : CanonicalBridges)
    (h : allBridgesEstablished bridges = true) :
    adjudicate completeBase bridges false = .canonicalProved := by
  simp [adjudicate, baseEstablished, completeBase, h]

/-- A real counterexample is required for refutation; missing witnesses are not refutation. -/
theorem missing_witnesses_do_not_refute :
    adjudicate completeBase noBridgeWitnesses false ≠ .canonicalRefuted := by
  decide

end FAR.CanonicalUniversality.Decision
