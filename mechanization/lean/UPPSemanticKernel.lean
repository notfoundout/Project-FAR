import Std

/-!
# Project FAR UPP end-to-end semantic kernel

This file closes remainder obligation G1 only. It places the complete registered
relative semantic composition inside one Lean proof object. All substantive
claims are explicit fields of `FrozenUPPSemantics`; no global axiom, `sorry`,
`admit`, unsafe declaration, finite-search generalization, G2 claim, or G3 claim
is introduced here.
-/

namespace FAR.UPPSemanticKernel

inductive Status where
  | pass
  | fail
  | unknown
  deriving Repr, DecidableEq

structure PreservationVector where
  structural : Status
  semantic : Status
  operational : Status
  dependency : Status
  informational : Status
  historical : Status
  queryTotality : Status
  failureUnknown : Status
  deriving Repr, DecidableEq

def PreservationVector.AllPass (p : PreservationVector) : Prop :=
  p.structural = .pass ∧
  p.semantic = .pass ∧
  p.operational = .pass ∧
  p.dependency = .pass ∧
  p.informational = .pass ∧
  p.historical = .pass ∧
  p.queryTotality = .pass ∧
  p.failureUnknown = .pass

/--
A single frozen semantic interface for the complete relative UPP dependency
chain. Each field is a declared theorem premise inherited from the completed
UPP workstreams. The terminal theorem below only composes these premises.
-/
structure FrozenUPPSemantics where
  Source : Type
  Package : Type

  inTargetClass : Source → Prop
  admissible : Package → Prop
  machineryClosed : Package → Prop
  preservation : Source → Package → PreservationVector
  commitmentEquivalent : Package → Package → Prop

  encode : Source → Package
  decode : Package → Source

  recoverableCommitment : Source → Prop
  constrainedEvolution : Source → Prop
  dependencyStructure : Source → Prop
  semanticInterpretation : Source → Prop
  historicalTrace : Source → Prop
  componentIndependent : Source → Prop
  nontrivial : Source → Prop
  relativelyMaximal : Source → Prop

  classConstruction :
    ∀ source, inTargetClass source → machineryClosed (encode source)
  representationAdmissible :
    ∀ source, inTargetClass source → admissible (encode source)
  preservationComplete :
    ∀ source, inTargetClass source →
      (preservation source (encode source)).AllPass

  sourceRoundTrip :
    ∀ source, decode (encode source) = source
  packageRoundTrip :
    ∀ package, encode (decode package) = package
  equivalenceReflexive :
    ∀ package, commitmentEquivalent package package

  commitmentNecessary :
    ∀ source, inTargetClass source → recoverableCommitment source
  evolutionNecessary :
    ∀ source, inTargetClass source → constrainedEvolution source
  dependencyNecessary :
    ∀ source, inTargetClass source → dependencyStructure source
  meaningNecessary :
    ∀ source, inTargetClass source → semanticInterpretation source
  historyNecessary :
    ∀ source, inTargetClass source → historicalTrace source
  independenceEstablished :
    ∀ source, inTargetClass source → componentIndependent source
  nontrivialityEstablished :
    ∀ source, inTargetClass source → nontrivial source
  frozenRuleMaximality :
    ∀ source, inTargetClass source → relativelyMaximal source

  faithfulCandidateEquivalent :
    ∀ source candidate,
      inTargetClass source →
      admissible candidate →
      machineryClosed candidate →
      (preservation source candidate).AllPass →
      commitmentEquivalent candidate (encode source)

/-- The complete registered per-source relative semantic conclusion. -/
structure RelativeSemanticConclusion
    (M : FrozenUPPSemantics) (source : M.Source) : Prop where
  admissible : M.admissible (M.encode source)
  closed : M.machineryClosed (M.encode source)
  preserved : (M.preservation source (M.encode source)).AllPass
  sourceReconstructed : M.decode (M.encode source) = source
  packageReconstructed :
    M.encode (M.decode (M.encode source)) = M.encode source
  selfEquivalent :
    M.commitmentEquivalent (M.encode source) (M.encode source)
  recoverableCommitment : M.recoverableCommitment source
  constrainedEvolution : M.constrainedEvolution source
  dependencyStructure : M.dependencyStructure source
  semanticInterpretation : M.semanticInterpretation source
  historicalTrace : M.historicalTrace source
  componentIndependent : M.componentIndependent source
  nontrivial : M.nontrivial source
  relativelyMaximal : M.relativelyMaximal source

/--
G1 terminal semantic composition.

For every source already admitted by the independently frozen target-class
predicate, the existing UPP premises compose into one kernel-checked relative
semantic conclusion.
-/
theorem g1_end_to_end_relative_semantic_theorem
    (M : FrozenUPPSemantics) :
    ∀ source, M.inTargetClass source → RelativeSemanticConclusion M source := by
  intro source hClass
  exact {
    admissible := M.representationAdmissible source hClass
    closed := M.classConstruction source hClass
    preserved := M.preservationComplete source hClass
    sourceReconstructed := M.sourceRoundTrip source
    packageReconstructed := M.packageRoundTrip (M.encode source)
    selfEquivalent := M.equivalenceReflexive (M.encode source)
    recoverableCommitment := M.commitmentNecessary source hClass
    constrainedEvolution := M.evolutionNecessary source hClass
    dependencyStructure := M.dependencyNecessary source hClass
    semanticInterpretation := M.meaningNecessary source hClass
    historicalTrace := M.historyNecessary source hClass
    componentIndependent := M.independenceEstablished source hClass
    nontrivial := M.nontrivialityEstablished source hClass
    relativelyMaximal := M.frozenRuleMaximality source hClass
  }

/-- Every faithful candidate is equivalent to the canonical encoding. -/
theorem faithful_candidate_equivalent_to_canonical
    (M : FrozenUPPSemantics)
    (source candidate : M.Package)
    (sourceObject : M.Source)
    (hClass : M.inTargetClass sourceObject)
    (hCandidateIsSourceEncoding : source = M.encode sourceObject)
    (hAdmissible : M.admissible candidate)
    (hClosed : M.machineryClosed candidate)
    (hPreserved : (M.preservation sourceObject candidate).AllPass) :
    M.commitmentEquivalent candidate source := by
  rw [hCandidateIsSourceEncoding]
  exact M.faithfulCandidateEquivalent sourceObject candidate hClass hAdmissible hClosed hPreserved

/-- Unknown cannot be silently counted as preservation success. -/
theorem unknown_semantic_dimension_not_all_pass
    (p : PreservationVector)
    (hUnknown : p.semantic = .unknown) :
    ¬ p.AllPass := by
  intro hAll
  have hPass : p.semantic = .pass := hAll.2.1
  rw [hUnknown] at hPass
  cases hPass

/-- Failure cannot be silently counted as preservation success. -/
theorem failed_operational_dimension_not_all_pass
    (p : PreservationVector)
    (hFail : p.operational = .fail) :
    ¬ p.AllPass := by
  intro hAll
  have hPass : p.operational = .pass := hAll.2.2.1
  rw [hFail] at hPass
  cases hPass

/-- Construction still requires independently supplied target-class membership. -/
theorem construction_requires_independent_class_membership
    (M : FrozenUPPSemantics)
    (source : M.Source)
    (hClass : M.inTargetClass source) :
    M.machineryClosed (M.encode source) :=
  M.classConstruction source hClass

end FAR.UPPSemanticKernel
