import Std

/-!
# Project FAR G3 epistemic maximality

This file formalizes the inaccessible-evidence boundary without treating hidden
reasoning as evidence for RCCD or for any competitor. When two source structures
have the same accessible observation but incompatible true classifications, no
observation-only classifier can be sound for both. Therefore inaccessible cases
must remain `unknown` unless additional discriminating access is supplied.
-/

namespace FAR.G3EpistemicMaximality

inductive Verdict where
  | pass
  | fail
  | unknown
  deriving Repr, DecidableEq

structure ObservationModel where
  Source : Type
  Observation : Type
  Label : Type
  observe : Source → Observation
  trueLabel : Source → Label

def Classifier (M : ObservationModel) := M.Observation → Option M.Label

def SoundFor (M : ObservationModel) (classifier : Classifier M) (source : M.Source) : Prop :=
  classifier (M.observe source) = some (M.trueLabel source)

def ObservationallyEquivalent (M : ObservationModel) (left right : M.Source) : Prop :=
  M.observe left = M.observe right

def StructurallyIncompatible (M : ObservationModel) (left right : M.Source) : Prop :=
  M.trueLabel left ≠ M.trueLabel right

/-- No observation-only classifier is sound for incompatible observational twins. -/
theorem indistinguishable_incompatible_sources_block_joint_soundness
    (M : ObservationModel)
    (classifier : Classifier M)
    (left right : M.Source)
    (hObserved : ObservationallyEquivalent M left right)
    (hIncompatible : StructurallyIncompatible M left right) :
    ¬ (SoundFor M classifier left ∧ SoundFor M classifier right) := by
  intro hSound
  unfold SoundFor at hSound
  unfold ObservationallyEquivalent at hObserved
  have hSome : some (M.trueLabel left) = some (M.trueLabel right) := by
    calc
      some (M.trueLabel left) = classifier (M.observe left) := hSound.1.symm
      _ = classifier (M.observe right) := congrArg classifier hObserved
      _ = some (M.trueLabel right) := hSound.2
  have hLabels : M.trueLabel left = M.trueLabel right := Option.some.inj hSome
  exact hIncompatible hLabels

/-- Evidence access sufficient to distinguish every incompatible alternative. -/
def DiscriminatingAccess (M : ObservationModel) (source : M.Source) : Prop :=
  ∀ alternative,
    StructurallyIncompatible M source alternative →
    ¬ ObservationallyEquivalent M source alternative

/-- A determinate verdict requires discriminating access and source-level soundness. -/
def DeterminateWarranted
    (M : ObservationModel)
    (classifier : Classifier M)
    (source : M.Source) : Prop :=
  DiscriminatingAccess M source ∧ SoundFor M classifier source

/-- Inaccessible or underdetermined cases remain Unknown. -/
def adjudicate
    (hasDiscriminatingAccess : Bool)
    (positiveEvidence : Bool)
    (defeatingEvidence : Bool) : Verdict :=
  if hasDiscriminatingAccess then
    if positiveEvidence then .pass
    else if defeatingEvidence then .fail
    else .unknown
  else
    .unknown

theorem inaccessible_adjudicates_unknown
    (positiveEvidence defeatingEvidence : Bool) :
    adjudicate false positiveEvidence defeatingEvidence = .unknown := by
  rfl

theorem inaccessible_never_adjudicates_pass
    (positiveEvidence defeatingEvidence : Bool) :
    adjudicate false positiveEvidence defeatingEvidence ≠ .pass := by
  simp [adjudicate]

theorem inaccessible_never_adjudicates_fail
    (positiveEvidence defeatingEvidence : Bool) :
    adjudicate false positiveEvidence defeatingEvidence ≠ .fail := by
  simp [adjudicate]

/-- An incompatible observational twin refutes discriminating access. -/
theorem incompatible_twin_refutes_discriminating_access
    (M : ObservationModel)
    (source twin : M.Source)
    (hObserved : ObservationallyEquivalent M source twin)
    (hIncompatible : StructurallyIncompatible M source twin) :
    ¬ DiscriminatingAccess M source := by
  intro hAccess
  exact (hAccess twin hIncompatible) hObserved

/-- G3 terminal epistemic-maximality boundary. -/
theorem g3_epistemic_maximality_theorem
    (M : ObservationModel)
    (classifier : Classifier M)
    (source twin : M.Source)
    (hObserved : ObservationallyEquivalent M source twin)
    (hIncompatible : StructurallyIncompatible M source twin) :
    ¬ DeterminateWarranted M classifier source := by
  intro hWarranted
  exact incompatible_twin_refutes_discriminating_access
    M source twin hObserved hIncompatible hWarranted.1

end FAR.G3EpistemicMaximality
