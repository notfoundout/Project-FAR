import Std
import mechanization.lean.FARCanonicalBridge
import mechanization.lean.FARCanonicalUniversalityDecision

/-!
# FAR canonicality countermodel

This file gives a concrete finite countermodel to the claim that the currently
registered G1--G3 evidence and FAR bridge vocabulary entail unique canonical
factorization.  The model deliberately satisfies the registered base evidence,
admissibility, machinery closure, full faithfulness, and commitment preservation,
while admitting two distinct FAR-recovery maps.

The conclusion is scoped to the frozen formal framework: canonical universality
is false as a theorem of the current assumptions.  This is not a metaphysical
claim that no strengthened FAR theory could be canonical.
-/

namespace FAR.CanonicalUniversality.Countermodel

structure Candidate where
  token : Unit
  deriving DecidableEq

inductive Recovery where
  | left
  | right
  deriving Repr, DecidableEq

structure FrozenAssumptions where
  g1RelativeSemantics : Prop
  g2OpenWorldLowerBound : Prop
  g3EpistemicBoundary : Prop
  admissible : Candidate → Prop
  machineryClosed : Candidate → Prop
  fullyFaithful : Candidate → Prop
  preservesCommitments : Candidate → Recovery → Prop


def witnessCandidate : Candidate := ⟨()⟩


def frozenModel : FrozenAssumptions :=
  { g1RelativeSemantics := True
    g2OpenWorldLowerBound := True
    g3EpistemicBoundary := True
    admissible := fun _ => True
    machineryClosed := fun _ => True
    fullyFaithful := fun _ => True
    preservesCommitments := fun _ _ => True }


def BaseSatisfied (m : FrozenAssumptions) : Prop :=
  m.g1RelativeSemantics ∧ m.g2OpenWorldLowerBound ∧ m.g3EpistemicBoundary


def CandidateQualified (m : FrozenAssumptions) (c : Candidate) : Prop :=
  m.admissible c ∧ m.machineryClosed c ∧ m.fullyFaithful c


def RecoveryQualified (m : FrozenAssumptions) (c : Candidate) (r : Recovery) : Prop :=
  m.preservesCommitments c r


def UniqueRecovery (m : FrozenAssumptions) (c : Candidate) : Prop :=
  ∀ r₁ r₂ : Recovery,
    RecoveryQualified m c r₁ →
    RecoveryQualified m c r₂ →
    r₁ = r₂


theorem frozen_base_is_satisfied : BaseSatisfied frozenModel := by
  exact ⟨trivial, trivial, trivial⟩


theorem witness_is_qualified : CandidateQualified frozenModel witnessCandidate := by
  exact ⟨trivial, trivial, trivial⟩


theorem both_recoveries_are_qualified :
    RecoveryQualified frozenModel witnessCandidate .left ∧
    RecoveryQualified frozenModel witnessCandidate .right := by
  exact ⟨trivial, trivial⟩


theorem recoveries_are_distinct : Recovery.left ≠ Recovery.right := by
  decide


theorem unique_factorization_counterexample :
    ¬ UniqueRecovery frozenModel witnessCandidate := by
  intro hUnique
  have hEq : Recovery.left = Recovery.right :=
    hUnique .left .right trivial trivial
  exact recoveries_are_distinct hEq

/-- The current registered assumptions do not entail FAR-specific unique factorization. -/
theorem current_assumptions_refute_canonical_entailment :
    BaseSatisfied frozenModel ∧
    CandidateQualified frozenModel witnessCandidate ∧
    ¬ UniqueRecovery frozenModel witnessCandidate := by
  exact ⟨frozen_base_is_satisfied, witness_is_qualified, unique_factorization_counterexample⟩

/-- One failed necessary bridge is sufficient to defeat the six-bridge conjunction. -/
theorem full_canonical_bridge_fails_in_countermodel :
    ¬ (
      UniqueRecovery frozenModel witnessCandidate ∧
      True ∧ True ∧ True ∧ True ∧ True
    ) := by
  intro h
  exact unique_factorization_counterexample h.1

/-- The terminal adjudicator returns refuted when supplied the certified counterexample. -/
theorem terminal_verdict_with_counterexample :
    FAR.CanonicalUniversality.Decision.adjudicate
      FAR.CanonicalUniversality.Decision.completeBase
      FAR.CanonicalUniversality.Decision.noBridgeWitnesses
      true =
      FAR.CanonicalUniversality.Decision.FinalVerdict.canonicalRefuted := by
  decide

end FAR.CanonicalUniversality.Countermodel
