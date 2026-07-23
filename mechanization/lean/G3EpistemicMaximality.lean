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

/-- A source model, its accessible observations, and the structural label at issue. -/
structure ObservationModel where
  Source : Type
  Observation : Type
  Label : Type
  observe : Source → Observation
  trueLabel : Source → Label

/-- An observation-only classifier has no hidden access to the source. -/
def Classifier (M : ObservationModel) := M.Observation → Option M.Label

/-- Soundness for one source requires the classifier to return its true label. -/
def SoundFor (M : ObservationModel) (classifier : Classifier M) (source : M.Source) : Prop :=
  classifier (M.observe source) = some (M.trueLabel source)

/-- Two sources are observationally indistinguishable. -/
def ObservationallyEquivalent (M : ObservationModel) (left right : M.Source) : Prop :=
  M.observe left = M.observe right

/-- The underlying structural classifications disagree. -/
def StructurallyIncompatible (M : ObservationModel) (left right : M.Source) : Prop :=
  M.trueLabel left ≠ M.trueLabel right

/--
No observation-only classifier can be sound for two observationally equivalent
sources whose true structural labels differ.
-/
theorem indistinguishable_incompatible_sources_block_joint_soundness
    (M : ObservationModel)
    (classifier : Classifier M)
    (left right : M.Source)
    (hObserved : ObservationallyEquivalent M left right)
    (hIncompatible : StructurallyIncompatible M left right) :
    ¬ (SoundFor M classifier left ∧ SoundFor M classifier right) := by
  intro hSound
  have hLeft := hSound.1
  have hRight := hSound.2
  unfold SoundFor at hLeft hRight
  unfold ObservationallyEquivalent at hObserved
  rw [hObserved] at hLeft
  rw [hLeft] at hRight
  injection hRight with hLabels
  exact hIncompatible hLabels.symm

/-- Evidence access sufficient to distinguish every incompatible alternative. -/
def DiscriminatingAccess (M : ObservationModel) (source : M.Source) : Prop :=
  ∀ alternative,
    StructurallyIncompatible M source alternative →
    ¬ ObservationallyEquivalent M source alternative

/--
A determinate observation-only classification is warranted only when all
structurally incompatible alternatives are observationally distinguishable.
-/
def DeterminateWarranted
    (M : ObservationModel)
    (classifier : Classifier M)
    (source : M.Source) : Prop :=
  DiscriminatingAccess M source ∧ SoundFor M classifier source

/-- Explicit adjudication preserves inaccessible or underdetermined cases as Unknown. -/
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

/-- Lack of discriminating access mechanically yields Unknown. -/
theorem inaccessible_adjudicates_unknown
    (positiveEvidence defeatingEvidence : Bool) :
    adjudicate false positiveEvidence defeatingEvidence = .unknown := by
  rfl

/-- Unknown is not silently promoted to Pass. -/
theorem inaccessible_never_adjudicates_pass
    (positiveEvidence defeatingEvidence : Bool) :
    adjudicate false positiveEvidence defeatingEvidence ≠ .pass := by
  decide

/-- Unknown is not silently promoted to Fail. -/
theorem inaccessible_never_adjudicates_fail
    (positiveEvidence defeatingEvidence : Bool) :
    adjudicate false positiveEvidence defeatingEvidence ≠ .fail := by
  decide

/--
Epistemic maximality boundary: if an incompatible observational twin exists,
then discriminating access is absent for that source.
-/
theorem incompatible_twin_refutes_discriminating_access
    (M : ObservationModel)
    (source twin : M.Source)
    (hObserved : ObservationallyEquivalent M source twin)
    (hIncompatible : StructurallyIncompatible M source twin) :
    ¬ DiscriminatingAccess M source := by
  intro hAccess
  exact (hAccess twin hIncompatible) hObserved

/--
Consequently no determinate warranted classification can be established for a
source with an incompatible observational twin.
-/
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
