import Std
import mechanization.lean.FARCanonicalUniversalityDecision

/-!
# FAR canonicality countermodel

A concrete finite countermodel to the claim that the currently registered G1--G3
base evidence entails FAR-specific unique factorization. The model satisfies the
registered qualification flags and commitment-preservation condition while
admitting two distinct qualified recovery maps.

The result is scoped to the frozen framework. It does not preclude a strengthened
FAR theory from adding independently justified extensionality or quotient rules.
-/

namespace FAR.CanonicalUniversality.Countermodel

inductive Recovery where
  | left
  | right
  deriving Repr, DecidableEq

structure FrozenModel where
  g1RelativeSemantics : Bool
  g2OpenWorldLowerBound : Bool
  g3EpistemicBoundary : Bool
  admissible : Bool
  machineryClosed : Bool
  fullyFaithful : Bool
  leftPreservesCommitments : Bool
  rightPreservesCommitments : Bool
  deriving Repr, DecidableEq


def countermodel : FrozenModel :=
  { g1RelativeSemantics := true
    g2OpenWorldLowerBound := true
    g3EpistemicBoundary := true
    admissible := true
    machineryClosed := true
    fullyFaithful := true
    leftPreservesCommitments := true
    rightPreservesCommitments := true }


def baseSatisfied (m : FrozenModel) : Bool :=
  m.g1RelativeSemantics && m.g2OpenWorldLowerBound && m.g3EpistemicBoundary


def candidateQualified (m : FrozenModel) : Bool :=
  m.admissible && m.machineryClosed && m.fullyFaithful


def recoveryQualified (m : FrozenModel) : Recovery → Bool
  | .left => m.leftPreservesCommitments
  | .right => m.rightPreservesCommitments


def uniqueRecovery (m : FrozenModel) : Prop :=
  ∀ r₁ r₂ : Recovery,
    recoveryQualified m r₁ = true →
    recoveryQualified m r₂ = true →
    r₁ = r₂


theorem frozen_base_is_satisfied : baseSatisfied countermodel = true := by
  decide


theorem witness_is_qualified : candidateQualified countermodel = true := by
  decide


theorem both_recoveries_are_qualified :
    recoveryQualified countermodel .left = true ∧
    recoveryQualified countermodel .right = true := by
  decide


theorem recoveries_are_distinct : Recovery.left ≠ Recovery.right := by
  decide


theorem unique_factorization_counterexample :
    ¬ uniqueRecovery countermodel := by
  intro h
  have hEq : Recovery.left = Recovery.right := h .left .right (by decide) (by decide)
  exact recoveries_are_distinct hEq

/-- The frozen base and qualification assumptions coexist with failed uniqueness. -/
theorem current_assumptions_refute_canonical_entailment :
    baseSatisfied countermodel = true ∧
    candidateQualified countermodel = true ∧
    ¬ uniqueRecovery countermodel := by
  exact ⟨frozen_base_is_satisfied, witness_is_qualified, unique_factorization_counterexample⟩

/-- Failure of the necessary unique-factorization bridge defeats the full conjunction. -/
theorem full_canonical_bridge_fails_in_countermodel :
    ¬ (uniqueRecovery countermodel ∧ True ∧ True ∧ True ∧ True ∧ True) := by
  intro h
  exact unique_factorization_counterexample h.1

/-- The existing terminal adjudicator classifies a certified counterexample as refutation. -/
theorem terminal_verdict_with_counterexample :
    FAR.CanonicalUniversality.Decision.adjudicate
      FAR.CanonicalUniversality.Decision.completeBase
      FAR.CanonicalUniversality.Decision.noBridgeWitnesses
      true =
      FAR.CanonicalUniversality.Decision.FinalVerdict.canonicalRefuted := by
  decide

end FAR.CanonicalUniversality.Countermodel
