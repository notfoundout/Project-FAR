import «mechanization».lean.FARCore

/-!
# Independent process semantics and end-to-end FAR preservation

This module defines process models without using FAR representation types, compiles
those models into `ProcessSpecification`, constructs a FAR representation, and
proves preservation relative to explicit observable behavior.
-/

namespace FAR

structure ModelState where
  id : String
  meaning : String
  deriving Repr, DecidableEq

structure ModelTransition where
  label : String
  source : ModelState
  target : ModelState
  deriving Repr, DecidableEq

structure IndependentProcessModel where
  name : String
  investigation : String
  states : List ModelState
  statesNonempty : states ≠ []
  initial : ModelState
  initialInStates : initial ∈ states
  terminal : ModelState → Bool
  transitions : List ModelTransition
  transitionClosed :
    ∀ transition, transition ∈ transitions →
      transition.source ∈ states ∧ transition.target ∈ states
  observableTrace : List ModelTransition
  traceContained : ∀ transition, transition ∈ observableTrace → transition ∈ transitions

def encodeState (model : IndependentProcessModel) (state : ModelState) : Representation :=
  {
    id := state.id
    content :=
      state.meaning ++
      (if state = model.initial then "|initial" else "") ++
      (if model.terminal state then "|terminal" else "|nonterminal")
  }

def encodeTransition (transition : ModelTransition) : TransitionSignature :=
  { label := transition.label }

def extractedReasoningProcess (model : IndependentProcessModel) : ReasoningProcess :=
  {
    name := model.name
    specifiedTransitions := model.observableTrace.map encodeTransition
  }

def extractedRelation
    (model : IndependentProcessModel)
    (source target : Representation) : Prop :=
  ∃ transition, transition ∈ model.transitions ∧
    source = encodeState model transition.source ∧
    target = encodeState model transition.target

def extractedAdmissible
    (model : IndependentProcessModel)
    (signature : TransitionSignature) : Prop :=
  ∃ transition, transition ∈ model.transitions ∧ signature = encodeTransition transition

def extractProcessSpecification
    (model : IndependentProcessModel) : ProcessSpecification :=
  {
    process := extractedReasoningProcess model
    investigation := { name := model.investigation }
    representations := model.states.map (encodeState model)
    representationsNonempty := by
      intro h
      have : model.states = [] := by simpa using h
      exact model.statesNonempty this
    requiredRelation := extractedRelation model
    relationClosed := by
      intro source target h
      rcases h with ⟨transition, hTransition, rfl, rfl⟩
      obtain ⟨hSource, hTarget⟩ := model.transitionClosed transition hTransition
      constructor
      · exact List.mem_map.mpr ⟨transition.source, hSource, rfl⟩
      · exact List.mem_map.mpr ⟨transition.target, hTarget, rfl⟩
    semantic := fun representation => representation.content
    admissible := extractedAdmissible model
  }

def compileIndependentModel
    (model : IndependentProcessModel) :
    FARRepresentation (extractedReasoningProcess model) :=
  canonicalRepresentation (extractProcessSpecification model)

def EndToEndPreservation
    (model : IndependentProcessModel)
    (representation : FARRepresentation (extractedReasoningProcess model)) : Prop :=
  representation.I.name = model.investigation ∧
  representation.Rep = model.states.map (encodeState model) ∧
  (∀ transition, transition ∈ model.transitions →
    representation.S.relates
      (encodeState model transition.source)
      (encodeState model transition.target)) ∧
  (∀ signature,
    representation.C.permits signature ↔ extractedAdmissible model signature) ∧
  representation.T.transitions = model.observableTrace.map encodeTransition ∧
  (∀ state, state ∈ model.states →
    ∃ membership : encodeState model state ∈ representation.Rep,
      representation.Int.meaning (encodeState model state) membership =
        (encodeState model state).content)

theorem compileIndependentModel_preserves_behavior
    (model : IndependentProcessModel) :
    EndToEndPreservation model (compileIndependentModel model) := by
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · intro transition hTransition
    exact ⟨transition, hTransition, rfl, rfl⟩
  constructor
  · intro signature
    exact Iff.rfl
  constructor
  · rfl
  · intro state hState
    let membership : encodeState model state ∈
        (compileIndependentModel model).Rep := by
      exact List.mem_map.mpr ⟨state, hState, rfl⟩
    exact ⟨membership, rfl⟩

def VerifiedCompilation
    (model : IndependentProcessModel)
    (representation : FARRepresentation (extractedReasoningProcess model)) : Prop :=
  EndToEndPreservation model representation

theorem verified_compiler_is_accepted (model : IndependentProcessModel) :
    VerifiedCompilation model (compileIndependentModel model) :=
  compileIndependentModel_preserves_behavior model

def lossyCompiler
    (model : IndependentProcessModel) :
    FARRepresentation (extractedReasoningProcess model) :=
  {
    I := { name := model.investigation }
    Rep := model.states.map (encodeState model)
    repNonempty := by
      intro h
      have : model.states = [] := by simpa using h
      exact model.statesNonempty this
    S := {
      relates := fun _ _ => False
      closedOnRepresentations := by intro _ _ h; contradiction
    }
    Int := {
      meaning := fun representation _ => representation.content
      investigationName := model.investigation
    }
    C := { permits := fun _ => False }
    T := { transitions := model.observableTrace.map encodeTransition }
    traceMatchesProcess := rfl
  }

theorem lossyCompiler_rejected_when_transition_exists
    (model : IndependentProcessModel)
    (transition : ModelTransition)
    (hTransition : transition ∈ model.transitions) :
    ¬ VerifiedCompilation model (lossyCompiler model) := by
  intro hVerified
  exact hVerified.2.2.1 transition hTransition

private def state (id meaning : String) : ModelState := { id := id, meaning := meaning }
private def edge (label : String) (source target : ModelState) : ModelTransition :=
  { label := label, source := source, target := target }

private def dP := state "P" "premise P"
private def dRule := state "P→Q" "deductive rule"
private def dQ := state "Q" "conclusion Q"
private def dStep := edge "modus-ponens" dP dQ

def deductiveModel : IndependentProcessModel :=
  {
    name := "deductive proof"
    investigation := "derive Q"
    states := [dP, dRule, dQ]
    statesNonempty := by simp
    initial := dP
    initialInStates := by simp [dP, dRule, dQ]
    terminal := fun s => s = dQ
    transitions := [dStep]
    transitionClosed := by
      intro transition h
      simp [dStep] at h
      subst transition
      simp [edge, dP, dRule, dQ, state]
    observableTrace := [dStep]
    traceContained := by simp
  }

private def lFact := state "fact" "signed agreement"
private def lException := state "exception" "duress defeats enforcement"
private def lResult := state "result" "obligation defeasibly established"
private def lApply := edge "apply-default" lFact lResult
private def lDefeat := edge "apply-exception" lException lResult

def defeasibleLegalModel : IndependentProcessModel :=
  {
    name := "defeasible legal analysis"
    investigation := "determine enforceability"
    states := [lFact, lException, lResult]
    statesNonempty := by simp
    initial := lFact
    initialInStates := by simp [lFact, lException, lResult]
    terminal := fun s => s = lResult
    transitions := [lApply, lDefeat]
    transitionClosed := by
      intro transition h
      simp [lApply, lDefeat] at h
      rcases h with rfl | rfl
      · simp [edge, lFact, lException, lResult, state]
      · simp [edge, lFact, lException, lResult, state]
    observableTrace := [lApply]
    traceContained := by simp [lApply, lDefeat]
  }

private def pPrior := state "prior" "prior probability 0.40"
private def pEvidence := state "evidence" "positive evidence"
private def pPosterior := state "posterior" "posterior probability 0.75"
private def pUpdate := edge "bayes-update" pPrior pPosterior
private def pDecide := edge "threshold-decision" pPosterior pPosterior

def probabilisticDecisionModel : IndependentProcessModel :=
  {
    name := "probabilistic decision"
    investigation := "update belief and decide"
    states := [pPrior, pEvidence, pPosterior]
    statesNonempty := by simp
    initial := pPrior
    initialInStates := by simp [pPrior, pEvidence, pPosterior]
    terminal := fun s => s = pPosterior
    transitions := [pUpdate, pDecide]
    transitionClosed := by
      intro transition h
      simp [pUpdate, pDecide] at h
      rcases h with rfl | rfl
      · simp [edge, pPrior, pEvidence, pPosterior, state]
      · simp [edge, pPrior, pEvidence, pPosterior, state]
    observableTrace := [pUpdate, pDecide]
    traceContained := by simp [pUpdate, pDecide]
  }

private def rOld := state "R1" "original active rule"
private def rProposal := state "proposal" "replace R1 with R1-prime"
private def rNew := state "R1-prime" "replacement active rule"
private def rUseOld := edge "infer-under-R1" rOld rProposal
private def rModify := edge "accept-rule-change" rProposal rNew
private def rUseNew := edge "infer-under-R1-prime" rNew rNew

def ruleModifyingModel : IndependentProcessModel :=
  {
    name := "rule-modifying reasoning"
    investigation := "reason while revising the active calculus"
    states := [rOld, rProposal, rNew]
    statesNonempty := by simp
    initial := rOld
    initialInStates := by simp [rOld, rProposal, rNew]
    terminal := fun s => s = rNew
    transitions := [rUseOld, rModify, rUseNew]
    transitionClosed := by
      intro transition h
      simp [rUseOld, rModify, rUseNew] at h
      rcases h with rfl | rfl | rfl
      · simp [edge, rOld, rProposal, rNew, state]
      · simp [edge, rOld, rProposal, rNew, state]
      · simp [edge, rOld, rProposal, rNew, state]
    observableTrace := [rUseOld, rModify, rUseNew]
    traceContained := by simp [rUseOld, rModify, rUseNew]
  }

theorem deductive_end_to_end :
    VerifiedCompilation deductiveModel (compileIndependentModel deductiveModel) :=
  verified_compiler_is_accepted deductiveModel

theorem defeasible_legal_end_to_end :
    VerifiedCompilation defeasibleLegalModel (compileIndependentModel defeasibleLegalModel) :=
  verified_compiler_is_accepted defeasibleLegalModel

theorem probabilistic_end_to_end :
    VerifiedCompilation probabilisticDecisionModel
      (compileIndependentModel probabilisticDecisionModel) :=
  verified_compiler_is_accepted probabilisticDecisionModel

theorem rule_modifying_end_to_end :
    VerifiedCompilation ruleModifyingModel (compileIndependentModel ruleModifyingModel) :=
  verified_compiler_is_accepted ruleModifyingModel

theorem lossy_deductive_rejected :
    ¬ VerifiedCompilation deductiveModel (lossyCompiler deductiveModel) := by
  exact lossyCompiler_rejected_when_transition_exists deductiveModel dStep
    (by simp [deductiveModel, dStep])

theorem lossy_legal_rejected :
    ¬ VerifiedCompilation defeasibleLegalModel (lossyCompiler defeasibleLegalModel) := by
  exact lossyCompiler_rejected_when_transition_exists defeasibleLegalModel lApply
    (by simp [defeasibleLegalModel, lApply])

theorem lossy_probabilistic_rejected :
    ¬ VerifiedCompilation probabilisticDecisionModel
      (lossyCompiler probabilisticDecisionModel) := by
  exact lossyCompiler_rejected_when_transition_exists probabilisticDecisionModel pUpdate
    (by simp [probabilisticDecisionModel, pUpdate])

theorem lossy_rule_modifying_rejected :
    ¬ VerifiedCompilation ruleModifyingModel (lossyCompiler ruleModifyingModel) := by
  exact lossyCompiler_rejected_when_transition_exists ruleModifyingModel rUseOld
    (by simp [ruleModifyingModel, rUseOld])

end FAR
