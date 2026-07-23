import Std
import UPPSemanticKernel

/-!
# Grounded FAR canonicality countermodel

This file instantiates the actual `FrozenUPPSemantics` structure from G1. It does
not replace substantive predicates with Boolean labels.

The model has one target-class source (`center`) and three package values. Both
`left` and `right` are admissible, machinery-closed, and fully preserved for the
same source. Each is commitment-equivalent to the canonical encoding, exactly as
G1 requires, but they are not commitment-equivalent to each other.

The countermodel therefore shows that the frozen G1 semantics do not entail
pairwise equivalence, unique recovery, or unique factorization. The gap is caused
by the fact that `commitmentEquivalent` is required to be reflexive but is not
required to be symmetric or transitive.
-/

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

/-- A directed relation: every node relates to itself and every node relates to
`center`, but `left` and `right` do not relate to each other. -/
def groundedEquivalent (a b : Node) : Prop := a = b ∨ b = .center


def groundedPreservation (source candidate : Node) : PreservationVector :=
  if source = .center then allPass else
  if candidate = source then allPass else notAllPass


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
    preservationComplete := by intro source h; subst source; decide
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
  decide


theorem left_is_fully_qualified : QualifiedForCenter .left := by decide

theorem right_is_fully_qualified : QualifiedForCenter .right := by decide


theorem left_equivalent_to_canonical :
    groundedModel.commitmentEquivalent .left (groundedModel.encode .center) := by
  exact groundedModel.faithfulCandidateEquivalent
    .center .left rfl trivial trivial left_is_fully_qualified.2.2


theorem right_equivalent_to_canonical :
    groundedModel.commitmentEquivalent .right (groundedModel.encode .center) := by
  exact groundedModel.faithfulCandidateEquivalent
    .center .right rfl trivial trivial right_is_fully_qualified.2.2


theorem left_not_equivalent_to_right :
    ¬ groundedModel.commitmentEquivalent .left .right := by decide


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
