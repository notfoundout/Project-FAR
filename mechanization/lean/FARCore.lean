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

end FAR
