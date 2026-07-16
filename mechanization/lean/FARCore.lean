import Std

/-!
# Project FAR core mechanization

This file mechanizes T-003 as a conditional construction theorem. It does not
postulate T-003 as an axiom and it does not assert that every cognitive event is
in scope. Instead, a caller supplies an explicit scope predicate and the five
premises corresponding to Project FAR Axioms A1-A5.
-/

namespace FAR

/-- Primitive sort: an investigation in which a reasoning process occurs. -/
structure Investigation where
  name : String
  deriving Repr, DecidableEq

/-- Primitive sort: an explicit representation participating in reasoning. -/
structure Representation where
  id : String
  content : String
  deriving Repr, DecidableEq

/-- A recorded transition signature. -/
structure TransitionSignature where
  label : String
  deriving Repr, DecidableEq

/-- A reasoning process with any explicitly specified transition signatures. -/
structure ReasoningProcess where
  name : String
  specifiedTransitions : List TransitionSignature := []
  deriving Repr

/-- The Project FAR scope is explicit rather than definitionally true. -/
structure Scope where
  contains : ReasoningProcess → Prop

/-- Representational organization is indexed by the selected representation collection. -/
structure RepresentationalStructure (Rep : List Representation) where
  relates : Representation → Representation → Prop
  closedOnRepresentations :
    ∀ {source target : Representation},
      relates source target → source ∈ Rep ∧ target ∈ Rep

/-- Interpretation is indexed by both the investigation and representation collection. -/
structure Interpretation (I : Investigation) (Rep : List Representation) where
  meaning : (representation : Representation) → representation ∈ Rep → String
  investigationName : String := I.name

/-- A reasoning calculus governing admissible transition signatures. -/
structure ReasoningCalculus where
  permits : TransitionSignature → Prop

/-- A reasoning trace records the ordered transition signatures explicitly supplied by a process. -/
structure Trace where
  transitions : List TransitionSignature
  deriving Repr

/-- The canonical six-component FAR representation of a specific reasoning process. -/
structure FARRepresentation (R : ReasoningProcess) where
  I : Investigation
  Rep : List Representation
  repNonempty : Rep ≠ []
  S : RepresentationalStructure Rep
  Int : Interpretation I Rep
  C : ReasoningCalculus
  T : Trace
  traceMatchesProcess : T.transitions = R.specifiedTransitions

/--
The exact assumptions used to construct a T-003 representation.

* `investigation` corresponds to A4.
* `representations` and `representationsNonempty` correspond to A1.
* `representationStructure` corresponds to A2 and is indexed by the chosen `Rep`.
* `interpretation` corresponds to A3 and is indexed by the chosen `I` and `Rep`.
* `calculus` corresponds to A5.

No assumption is included for the trace: `traceOf` is constructed directly from
whatever transition sequence the process explicitly specifies, including the empty list.
-/
structure T003Premises (scope : Scope) where
  investigation :
    (R : ReasoningProcess) → scope.contains R → Investigation
  representations :
    (R : ReasoningProcess) → scope.contains R → List Representation
  representationsNonempty :
    (R : ReasoningProcess) → (h : scope.contains R) →
      representations R h ≠ []
  representationStructure :
    (R : ReasoningProcess) → (h : scope.contains R) →
      RepresentationalStructure (representations R h)
  interpretation :
    (R : ReasoningProcess) → (h : scope.contains R) →
      Interpretation (investigation R h) (representations R h)
  calculus :
    (R : ReasoningProcess) → scope.contains R → ReasoningCalculus

/-- Construct the trace without adding a sixth primitive existence axiom. -/
def traceOf (R : ReasoningProcess) : Trace :=
  { transitions := R.specifiedTransitions }

/--
T-003 — Representation Theorem.

For every reasoning process admitted by the supplied Project FAR scope, the
A1-A5 premises construct at least one six-component FAR representation.
-/
theorem t003_representation_theorem
    (scope : Scope)
    (premises : T003Premises scope) :
    ∀ R : ReasoningProcess, scope.contains R → Nonempty (FARRepresentation R) := by
  intro R hScope
  exact ⟨{
    I := premises.investigation R hScope
    Rep := premises.representations R hScope
    repNonempty := premises.representationsNonempty R hScope
    S := premises.representationStructure R hScope
    Int := premises.interpretation R hScope
    C := premises.calculus R hScope
    T := traceOf R
    traceMatchesProcess := rfl
  }⟩

/-- Constructive form of T-003, exposing the witness rather than only its existence. -/
def constructFARRepresentation
    (scope : Scope)
    (premises : T003Premises scope)
    (R : ReasoningProcess)
    (hScope : scope.contains R) : FARRepresentation R :=
  {
    I := premises.investigation R hScope
    Rep := premises.representations R hScope
    repNonempty := premises.representationsNonempty R hScope
    S := premises.representationStructure R hScope
    Int := premises.interpretation R hScope
    C := premises.calculus R hScope
    T := traceOf R
    traceMatchesProcess := rfl
  }

/-- The theorem's trace is empty exactly when the process specifies no transitions. -/
theorem constructed_trace_is_empty_iff
    (scope : Scope)
    (premises : T003Premises scope)
    (R : ReasoningProcess)
    (hScope : scope.contains R) :
    (constructFARRepresentation scope premises R hScope).T.transitions = [] ↔
      R.specifiedTransitions = [] := by
  simp [constructFARRepresentation, traceOf]

/-! ## T-003 assumption-minimality and adequacy audit -/

/-- A process specification is independent input against which a FAR tuple can be judged. -/
structure ProcessSpecification where
  process : ReasoningProcess
  investigation : Investigation
  representations : List Representation
  representationsNonempty : representations ≠ []
  requiredRelation : Representation → Representation → Prop
  relationClosed :
    ∀ {source target : Representation},
      requiredRelation source target →
        source ∈ representations ∧ target ∈ representations
  semantic : Representation → String
  admissible : TransitionSignature → Prop

/-- Canonical representation obtained from an independently supplied process specification. -/
def canonicalRepresentation (spec : ProcessSpecification) :
    FARRepresentation spec.process :=
  {
    I := spec.investigation
    Rep := spec.representations
    repNonempty := spec.representationsNonempty
    S := {
      relates := spec.requiredRelation
      closedOnRepresentations := spec.relationClosed
    }
    Int := {
      meaning := fun representation _ => spec.semantic representation
      investigationName := spec.investigation.name
    }
    C := { permits := spec.admissible }
    T := traceOf spec.process
    traceMatchesProcess := rfl
  }

/-- Structural preservation is stronger than merely inhabiting `FARRepresentation`. -/
def StructuralPreservation
    (spec : ProcessSpecification)
    (representation : FARRepresentation spec.process) : Prop :=
  representation.I = spec.investigation ∧
  representation.Rep = spec.representations ∧
  ∀ source target,
    representation.S.relates source target ↔ spec.requiredRelation source target

/-- Semantic preservation compares encoded meanings with independently specified meanings. -/
def SemanticPreservation
    (spec : ProcessSpecification)
    (representation : FARRepresentation spec.process) : Prop :=
  ∀ representationObject (membership : representationObject ∈ representation.Rep),
    representation.Int.meaning representationObject membership =
      spec.semantic representationObject

/-- Operational preservation compares admissible transitions extensionally. -/
def OperationalPreservation
    (spec : ProcessSpecification)
    (representation : FARRepresentation spec.process) : Prop :=
  ∀ transition,
    representation.C.permits transition ↔ spec.admissible transition

/-- Trace preservation is stated separately even though the base type already enforces it. -/
def TracePreservation
    (spec : ProcessSpecification)
    (representation : FARRepresentation spec.process) : Prop :=
  representation.T.transitions = spec.process.specifiedTransitions

/-- A faithful FAR representation preserves structure, semantics, operation, and trace. -/
def FaithfulRepresentation
    (spec : ProcessSpecification)
    (representation : FARRepresentation spec.process) : Prop :=
  StructuralPreservation spec representation ∧
  SemanticPreservation spec representation ∧
  OperationalPreservation spec representation ∧
  TracePreservation spec representation

/-- The canonical constructor is faithful to every well-formed process specification. -/
theorem canonical_representation_is_faithful (spec : ProcessSpecification) :
    FaithfulRepresentation spec (canonicalRepresentation spec) := by
  constructor
  · exact ⟨rfl, rfl, fun _ _ => Iff.rfl⟩
  constructor
  · intro _ _
    rfl
  constructor
  · intro _
    exact Iff.rfl
  · rfl

/-- A placeholder object demonstrates that bare structural existence needs no A1-A5 premises. -/
def placeholderRepresentation : Representation :=
  { id := "placeholder", content := "unspecified" }

/-- Every process has a structurally well-typed placeholder FAR tuple. -/
def defaultFARRepresentation (R : ReasoningProcess) : FARRepresentation R :=
  {
    I := { name := "unspecified" }
    Rep := [placeholderRepresentation]
    repNonempty := by simp
    S := {
      relates := fun _ _ => False
      closedOnRepresentations := by
        intro _ _ impossible
        contradiction
    }
    Int := {
      meaning := fun _ _ => "unspecified"
      investigationName := "unspecified"
    }
    C := { permits := fun _ => False }
    T := traceOf R
    traceMatchesProcess := rfl
  }

/-- Minimality result: A1-A5 are unnecessary for bare tuple inhabitation in this encoding. -/
theorem unconditional_structural_existence :
    ∀ R : ReasoningProcess, Nonempty (FARRepresentation R) := by
  intro R
  exact ⟨defaultFARRepresentation R⟩

/-- T-003's assumptions select process-relative content; they do not create type inhabitation. -/
theorem t003_existence_is_not_assumption_minimal
    (scope : Scope)
    (premises : T003Premises scope)
    (R : ReasoningProcess)
    (hScope : scope.contains R) :
    Nonempty (FARRepresentation R) := by
  exact unconditional_structural_existence R

/-! ### Three concrete process specifications -/

private def mpPremise : Representation :=
  { id := "P", content := "P" }
private def mpRule : Representation :=
  { id := "P-implies-Q", content := "P → Q" }
private def mpConclusion : Representation :=
  { id := "Q", content := "Q" }
private def mpStep : TransitionSignature :=
  { label := "modus-ponens" }

def modusPonensSpecification : ProcessSpecification :=
  {
    process := {
      name := "modus ponens"
      specifiedTransitions := [mpStep]
    }
    investigation := { name := "derive Q" }
    representations := [mpPremise, mpRule, mpConclusion]
    representationsNonempty := by simp
    requiredRelation := fun source target =>
      (source = mpPremise ∧ target = mpConclusion) ∨
      (source = mpRule ∧ target = mpConclusion)
    relationClosed := by
      intro source target h
      rcases h with h | h
      · rcases h with ⟨rfl, rfl⟩
        simp [mpPremise, mpConclusion]
      · rcases h with ⟨rfl, rfl⟩
        simp [mpRule, mpConclusion]
    semantic := fun representation => representation.content
    admissible := fun transition => transition = mpStep
  }

private def triageObservation : Representation :=
  { id := "fever", content := "patient has fever" }
private def triageStep : TransitionSignature :=
  { label := "apply-triage-rule" }

def triageSpecification : ProcessSpecification :=
  {
    process := {
      name := "clinical triage"
      specifiedTransitions := [triageStep]
    }
    investigation := { name := "select urgency category" }
    representations := [triageObservation]
    representationsNonempty := by simp
    requiredRelation := fun source target =>
      source = triageObservation ∧ target = triageObservation
    relationClosed := by
      intro source target h
      rcases h with ⟨rfl, rfl⟩
      simp [triageObservation]
    semantic := fun representation => representation.content
    admissible := fun transition => transition = triageStep
  }

private def legalFact : Representation :=
  { id := "signed-contract", content := "a signed contract exists" }
private def legalStep : TransitionSignature :=
  { label := "apply-contract-rule" }

def legalSpecification : ProcessSpecification :=
  {
    process := {
      name := "contract analysis"
      specifiedTransitions := [legalStep]
    }
    investigation := { name := "determine contractual obligation" }
    representations := [legalFact]
    representationsNonempty := by simp
    requiredRelation := fun source target =>
      source = legalFact ∧ target = legalFact
    relationClosed := by
      intro source target h
      rcases h with ⟨rfl, rfl⟩
      simp [legalFact]
    semantic := fun representation => representation.content
    admissible := fun transition => transition = legalStep
  }

theorem modus_ponens_instance_is_faithful :
    FaithfulRepresentation modusPonensSpecification
      (canonicalRepresentation modusPonensSpecification) :=
  canonical_representation_is_faithful modusPonensSpecification

theorem triage_instance_is_faithful :
    FaithfulRepresentation triageSpecification
      (canonicalRepresentation triageSpecification) :=
  canonical_representation_is_faithful triageSpecification

theorem legal_instance_is_faithful :
    FaithfulRepresentation legalSpecification
      (canonicalRepresentation legalSpecification) :=
  canonical_representation_is_faithful legalSpecification

/-! ### Negative adequacy examples -/

/-- A tuple can be structurally valid while assigning the wrong investigation and semantics. -/
def corruptedModusPonensRepresentation :
    FARRepresentation modusPonensSpecification.process :=
  {
    I := { name := "unrelated investigation" }
    Rep := modusPonensSpecification.representations
    repNonempty := modusPonensSpecification.representationsNonempty
    S := {
      relates := modusPonensSpecification.requiredRelation
      closedOnRepresentations := modusPonensSpecification.relationClosed
    }
    Int := {
      meaning := fun _ _ => "corrupted meaning"
      investigationName := "unrelated investigation"
    }
    C := { permits := fun _ => False }
    T := traceOf modusPonensSpecification.process
    traceMatchesProcess := rfl
  }

/-- Structural typing alone does not imply investigation preservation. -/
theorem corrupted_mp_fails_structural_preservation :
    ¬ StructuralPreservation modusPonensSpecification
        corruptedModusPonensRepresentation := by
  intro h
  have investigationEquality := h.1
  simp [corruptedModusPonensRepresentation, modusPonensSpecification] at investigationEquality

/-- Structural typing alone does not imply semantic preservation. -/
theorem corrupted_mp_fails_semantic_preservation :
    ¬ SemanticPreservation modusPonensSpecification
        corruptedModusPonensRepresentation := by
  intro h
  have meaningEquality := h mpPremise (by simp [corruptedModusPonensRepresentation, modusPonensSpecification, mpPremise])
  simp [corruptedModusPonensRepresentation, modusPonensSpecification, mpPremise] at meaningEquality

/-- Structural typing alone does not imply operational preservation. -/
theorem corrupted_mp_fails_operational_preservation :
    ¬ OperationalPreservation modusPonensSpecification
        corruptedModusPonensRepresentation := by
  intro h
  have transitionEquality := h mpStep
  simp [corruptedModusPonensRepresentation, modusPonensSpecification, mpStep] at transitionEquality

/-- Consequently, a well-typed six-component tuple need not be faithful. -/
theorem corrupted_mp_is_not_faithful :
    ¬ FaithfulRepresentation modusPonensSpecification
        corruptedModusPonensRepresentation := by
  intro h
  exact corrupted_mp_fails_structural_preservation h.1

/-- Exact audit conclusion: construction and preservation are distinct theorems. -/
theorem structural_existence_does_not_imply_faithfulness :
    Nonempty (FARRepresentation modusPonensSpecification.process) ∧
    ∃ representation : FARRepresentation modusPonensSpecification.process,
      ¬ FaithfulRepresentation modusPonensSpecification representation := by
  constructor
  · exact unconditional_structural_existence modusPonensSpecification.process
  · exact ⟨corruptedModusPonensRepresentation, corrupted_mp_is_not_faithful⟩

end FAR
