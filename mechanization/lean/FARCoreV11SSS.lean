import FARCoreV11Substrate

/-!
# FAR-CORE-014: bounded Search-State Sufficiency application

This module kernel-checks the exhaustive four-decoder result, the two Boolean witness profiles,
and conditional hyperedge/frontier factorization bridges.  It deliberately does **not** assume
the PR #453 narrative MLL sequents as axioms.  End-to-end MLL closure remains obstructed until
MLL syntax, derivability, atom balance, and the two actual sequents are mechanized separately.
-/

namespace FARCoreV11.SSS

universe u v

/-- Boolean implication, used as the monotonicity order on the decoder chain. -/
def BoolImplies (lower upper : Bool) : Prop := lower = true -> upper = true

/-- A uniform monotone decoder on the chain `{0} <= {0,1} <= {1}`. -/
structure SuccessorDecoder where
  onZero : Bool
  onMixed : Bool
  onOne : Bool
  zeroToMixed : BoolImplies onZero onMixed
  mixedToOne : BoolImplies onMixed onOne

@[ext] theorem SuccessorDecoder.ext {left right : SuccessorDecoder}
    (hzero : left.onZero = right.onZero)
    (hmixed : left.onMixed = right.onMixed)
    (hone : left.onOne = right.onOne) : left = right := by
  cases left
  cases right
  simp_all

def termDecoder : SuccessorDecoder := ⟨false, false, false, by simp [BoolImplies], by simp [BoolImplies]⟩
def andDecoder : SuccessorDecoder := ⟨false, false, true, by simp [BoolImplies], by simp [BoolImplies]⟩
def orDecoder : SuccessorDecoder := ⟨false, true, true, by simp [BoolImplies], by simp [BoolImplies]⟩
def nonemptyDecoder : SuccessorDecoder := ⟨true, true, true, by simp [BoolImplies], by simp [BoolImplies]⟩

/-- The monotone three-Bool chain has exactly TERM, AND, OR, and NONEMPTY. -/
theorem four_monotone_decoders (decoder : SuccessorDecoder) :
    decoder = termDecoder ∨ decoder = andDecoder ∨
      decoder = orDecoder ∨ decoder = nonemptyDecoder := by
  cases hzero : decoder.onZero
  · cases hmixed : decoder.onMixed
    · cases hone : decoder.onOne
      · left
        apply SuccessorDecoder.ext <;>
          simp [termDecoder, hzero, hmixed, hone]
      · right
        left
        apply SuccessorDecoder.ext <;>
          simp [andDecoder, hzero, hmixed, hone]
    · have hone : decoder.onOne = true := decoder.mixedToOne hmixed
      right
      right
      left
      apply SuccessorDecoder.ext <;>
        simp [orDecoder, hzero, hmixed, hone]
  · have hmixed : decoder.onMixed = true := decoder.zeroToMixed hzero
    have hone : decoder.onOne = true := decoder.mixedToOne hmixed
    right
    right
    right
    apply SuccessorDecoder.ext <;>
      simp [nonemptyDecoder, hzero, hmixed, hone]

/-- The three nonempty successor truth-value sets available to a uniform decoder. -/
inductive SuccessorTruthShape where
  | zeroOnly
  | mixed
  | oneOnly
  deriving DecidableEq, Repr

def decodeShape (decoder : SuccessorDecoder) : SuccessorTruthShape -> Bool
  | .zeroOnly => decoder.onZero
  | .mixed => decoder.onMixed
  | .oneOnly => decoder.onOne

/-- Bounded Boolean data extracted from an actual search-state witness. -/
structure WitnessSummary where
  derivable : Bool
  terminal : Bool
  successorTruths : SuccessorTruthShape
  deriving DecidableEq, Repr

/-- Decoder prediction `T(S) OR g(V(S))`. -/
def decoderPrediction (decoder : SuccessorDecoder) (summary : WitnessSummary) : Bool :=
  summary.terminal || decodeShape decoder summary.successorTruths

/-- Summary of S_or after the separately certified MLL facts are supplied. -/
def sOrSummary : WitnessSummary := ⟨false, false, .mixed⟩

/-- Summary of S_and after the separately certified MLL facts are supplied. -/
def sAndSummary : WitnessSummary := ⟨true, false, .mixed⟩

/-- Every uniform decoder fails one of the two bounded truth profiles. -/
theorem projected_successor_decoder_failure (decoder : SuccessorDecoder) :
    decoderPrediction decoder sOrSummary ≠ sOrSummary.derivable ∨
      decoderPrediction decoder sAndSummary ≠ sAndSummary.derivable := by
  cases hprediction : decoderPrediction decoder sOrSummary
  · right
    simp [decoderPrediction, sOrSummary, sAndSummary, decodeShape] at hprediction ⊢
    exact hprediction
  · left
    simp [decoderPrediction, sOrSummary, sAndSummary, decodeShape] at hprediction ⊢

/-- Negative control: a decoder that inspects the state can simply return its answer. -/
def stateInspectingDecoder (summary : WitnessSummary) : Bool := summary.derivable

theorem unrestricted_decoder_counterexample (summary : WitnessSummary) :
    stateInspectingDecoder summary = summary.derivable := by
  rfl

/-! ## Conditional factorization bridges -/

/-- Projected hyperedges preserve each jointly generated premise family. -/
abbrev HyperedgeView (State : Type u) := List (List State)

/-- The standard AND/OR behavior read from a hyperedge view. -/
def hyperedgeDecoder {State : Type u} (derivable : State -> Prop)
    (view : HyperedgeView State) : Prop :=
  ∃ premises ∈ view, ∀ premise ∈ premises, derivable premise

/--
Conditional part of FAR-CORE-014: the exact rule-instance characterization makes the
hyperedge view sufficient.  The characterization is visible as a premise, not an axiom.
-/
theorem hyperedge_factorization {State : Type u}
    (derivable : State -> Prop) (hyperedges : State -> HyperedgeView State)
    (ruleCharacterization : ∀ state,
      derivable state ↔ hyperedgeDecoder derivable (hyperedges state)) :
    ExactlySufficient derivable hyperedges := by
  refine ⟨fun represented => hyperedgeDecoder derivable represented.val, ?_⟩
  intro state
  apply propext
  exact (ruleCharacterization state).symm

/-- The information exposed by an empty/frontier state plus its binary successors. -/
structure FrontierView (Frontier : Type u) where
  isEmpty : Prop
  successors : Frontier -> Prop

def frontierView {Frontier : Type u} (empty : Frontier -> Prop)
    (step : Frontier -> Frontier -> Prop) (frontier : Frontier) : FrontierView Frontier where
  isEmpty := empty frontier
  successors := step frontier

def frontierDecoder {Frontier : Type u} (closable : Frontier -> Prop)
    (view : FrontierView Frontier) : Prop :=
  view.isEmpty ∨ ∃ next, view.successors next ∧ closable next

/--
Conditional part of FAR-CORE-014: the governed frontier recursion makes the frontier/binary
step view sufficient.  No claim about the missing MLL derivation kernel is hidden here.
-/
theorem frontier_factorization {Frontier : Type u}
    (closable empty : Frontier -> Prop) (step : Frontier -> Frontier -> Prop)
    (frontierRecursion : ∀ frontier,
      closable frontier ↔ empty frontier ∨
        ∃ next, step frontier next ∧ closable next) :
    ExactlySufficient closable (frontierView empty step) := by
  refine ⟨fun represented => frontierDecoder closable represented.val, ?_⟩
  intro frontier
  apply propext
  exact (frontierRecursion frontier).symm

/-- Explicit guard against the withdrawn claim that binary relations fail on every state type. -/
theorem frontier_binary_relation_is_not_refuted {Frontier : Type u}
    (closable empty : Frontier -> Prop) (step : Frontier -> Frontier -> Prop)
    (frontierRecursion : ∀ frontier,
      closable frontier ↔ empty frontier ∨
        ∃ next, step frontier next ∧ closable next) :
    ExactlySufficient closable (frontierView empty step) :=
  frontier_factorization closable empty step frontierRecursion

end FARCoreV11.SSS
