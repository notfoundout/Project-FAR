import Std
import UPPSemanticKernel

namespace FAR.CanonicalUniversality.Countermodel

open FAR.UPPSemanticKernel

inductive Node where
  | center
  | left
  | right
  deriving Repr, DecidableEq


def allPass : PreservationVector :=
  { structural := .pass
    semantic := .pass
    operational := .pass
    dependency := .pass
    informational := .pass
    historical := .pass
    queryTotality := .pass
    failureUnknown := .pass }


def notAllPass : PreservationVector :=
  { structural := .fail
    semantic := .fail
    operational := .fail
    dependency := .fail
    informational := .fail
    historical := .fail
    queryTotality := .fail
    failureUnknown := .fail }


def groundedEquivalent (a b : Node) : Prop := a = b ∨ b = .center


def groundedPreservation (source candidate : Node) : PreservationVector :=
  if source = .center then allPass else
  if candidate = source then allPass else notAllPass


theorem allPass_is_all_pass : allPass.AllPass := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩


def groundedModel : FrozenUPPSemantics :=
  { Source := Node
    Package := Node
    inTargetClass := fun source => source = .center
    admissible := fun _ => True
    machineryClosed := fun _ => True
    preservation := groundedPreservation
    commitmentEquivalent := groundedEquivalent
    encode := id
    decode := id
    recoverableCommitment := fun _ => True
    constrainedEvolution := fun _ => True
    dependencyStructure := fun _ => True
    semanticInterpretation := fun _ => True
    historicalTrace := fun _ => True
    componentIndependent := fun _ => True
    nontrivial := fun _ => True
    relativelyMaximal := fun _ => True
    classConstruction := by intro source h; trivial
    representationAdmissible := by intro source h; trivial
    preservationComplete := by
      intro source h
      subst source
      simpa [groundedPreservation] using allPass_is_all_pass
    sourceRoundTrip := by intro source; rfl
    packageRoundTrip := by intro package; rfl
    equivalenceReflexive := by intro package; exact Or.inl rfl
    commitmentNecessary := by intro source h; trivial
    evolutionNecessary := by intro source h; trivial
    dependencyNecessary := by intro source h; trivial
    meaningNecessary := by intro source h; trivial
    historyNecessary := by intro source h; trivial
    independenceEstablished := by intro source h; trivial
    nontrivialityEstablished := by intro source h; trivial
    frozenRuleMaximality := by intro source h; trivial
    faithfulCandidateEquivalent := by
      intro source candidate hClass hAdmissible hClosed hPreserved
      subst source
      exact Or.inr rfl }


def QualifiedForCenter (candidate : Node) : Prop :=
  groundedModel.admissible candidate ∧
  groundedModel.machineryClosed candidate ∧
  (groundedModel.preservation .center candidate).AllPass


def PairwiseUniqueUpToRegisteredEquivalence : Prop :=
  ∀ a b, QualifiedForCenter a → QualifiedForCenter b →
    groundedModel.commitmentEquivalent a b


theorem grounded_model_is_actual_g1_model :
    groundedModel.inTargetClass .center ∧
    groundedModel.admissible (groundedModel.encode .center) ∧
    groundedModel.machineryClosed (groundedModel.encode .center) ∧
    (groundedModel.preservation .center (groundedModel.encode .center)).AllPass := by
  exact ⟨rfl, trivial, trivial, by simpa [groundedModel, groundedPreservation] using allPass_is_all_pass⟩


theorem left_is_fully_qualified : QualifiedForCenter .left := by
  exact ⟨trivial, trivial, by simpa [groundedModel, groundedPreservation] using allPass_is_all_pass⟩


theorem right_is_fully_qualified : QualifiedForCenter .right := by
  exact ⟨trivial, trivial, by simpa [groundedModel, groundedPreservation] using allPass_is_all_pass⟩


theorem left_equivalent_to_canonical :
    groundedModel.commitmentEquivalent .left (groundedModel.encode .center) := by
  exact groundedModel.faithfulCandidateEquivalent
    .center .left rfl trivial trivial left_is_fully_qualified.2.2


theorem right_equivalent_to_canonical :
    groundedModel.commitmentEquivalent .right (groundedModel.encode .center) := by
  exact groundedModel.faithfulCandidateEquivalent
    .center .right rfl trivial trivial right_is_fully_qualified.2.2


theorem left_not_equivalent_to_right :
    ¬ groundedModel.commitmentEquivalent .left .right := by
  intro h
  cases h with
  | inl hEq => cases hEq
  | inr hCenter => cases hCenter


theorem unique_factorization_counterexample :
    ¬ PairwiseUniqueUpToRegisteredEquivalence := by
  intro hUnique
  exact left_not_equivalent_to_right
    (hUnique .left .right left_is_fully_qualified right_is_fully_qualified)


theorem current_g1_semantics_do_not_entail_canonical_uniqueness :
    groundedModel.inTargetClass .center ∧
    QualifiedForCenter .left ∧ QualifiedForCenter .right ∧
    groundedModel.commitmentEquivalent .left (groundedModel.encode .center) ∧
    groundedModel.commitmentEquivalent .right (groundedModel.encode .center) ∧
    ¬ groundedModel.commitmentEquivalent .left .right ∧
    ¬ PairwiseUniqueUpToRegisteredEquivalence := by
  exact ⟨rfl, left_is_fully_qualified, right_is_fully_qualified,
    left_equivalent_to_canonical, right_equivalent_to_canonical,
    left_not_equivalent_to_right, unique_factorization_counterexample⟩

end FAR.CanonicalUniversality.Countermodel
