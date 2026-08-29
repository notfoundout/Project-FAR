import FARCoreV11Substrate

/-!
# FAR-CORE-014: bounded Search-State Sufficiency application

This module kernel-checks the exhaustive four-decoder result, the actual bounded MLL witness
sequents and resource splits, and the conditional hyperedge/frontier factorization bridges used
by FAR-CORE-014.  Its scope is deliberately application-bounded: cut-free, unit-free one-sided
MLL, the stated projected-successor representation, and the stated uniform monotone decoder
class.  It is not a universal architecture theorem.
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

/-- Summary of S_or, certified against the MLL witness below. -/
def sOrSummary : WitnessSummary := ⟨false, false, .mixed⟩

/-- Summary of S_and, certified against the MLL witness below. -/
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
step view sufficient.  The recursion is explicit as a premise.
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

/-! ## Governed MLL witness bridge -/

namespace MLL

inductive Formula where
  | atom (name : Nat) (positive : Bool)
  | tensor (left right : Formula)
  | par (left right : Formula)
  deriving DecidableEq, Repr

abbrev Sequent := List Formula

namespace Formula

def a : Formula := .atom 0 true
def aPerp : Formula := .atom 0 false
def b : Formula := .atom 1 true
def bPerp : Formula := .atom 1 false
end Formula

/-- Cut-free, unit-free, one-sided MLL with adjacent exchange. -/
inductive Derivable : Sequent -> Prop where
  | ax (name : Nat) : Derivable [.atom name false, .atom name true]
  | tensor {gamma delta : Sequent} {left right : Formula} :
      Derivable (gamma ++ [left]) ->
      Derivable (delta ++ [right]) ->
      Derivable (gamma ++ delta ++ [.tensor left right])
  | par {gamma : Sequent} {left right : Formula} :
      Derivable (gamma ++ [left, right]) ->
      Derivable (gamma ++ [.par left right])
  | exchange {pre post : Sequent} {first second : Formula} :
      Derivable (pre ++ first :: second :: post) ->
      Derivable (pre ++ second :: first :: post)

/-- Signed occurrence count of one atom in a formula. -/
def atomWeight (target : Nat) : Formula -> Int
  | .atom name true => if name = target then 1 else 0
  | .atom name false => if name = target then -1 else 0
  | .tensor left right => atomWeight target left + atomWeight target right
  | .par left right => atomWeight target left + atomWeight target right

/-- Signed occurrence count of one atom across a sequent. -/
def sequentWeight (target : Nat) : Sequent -> Int
  | [] => 0
  | formula :: rest => atomWeight target formula + sequentWeight target rest

@[simp] theorem sequentWeight_append (target : Nat) (left right : Sequent) :
    sequentWeight target (left ++ right) =
      sequentWeight target left + sequentWeight target right := by
  induction left with
  | nil => simp [sequentWeight]
  | cons formula rest ih =>
      simp [sequentWeight, ih, Int.add_assoc]

/-- Atom balance is an invariant of every derivation in the governed fragment. -/
theorem derivable_atom_balance {sequent : Sequent}
    (derivation : Derivable sequent) (target : Nat) :
    sequentWeight target sequent = 0 := by
  induction derivation with
  | ax name =>
      by_cases h : name = target <;>
        simp [sequentWeight, atomWeight, h]
  | tensor leftDerivation rightDerivation leftIH rightIH =>
      have hLeft := leftIH
      have hRight := rightIH
      simp only [sequentWeight_append, sequentWeight, atomWeight, Int.add_zero] at hLeft hRight ⊢
      calc
        _ = (sequentWeight target gamma + atomWeight target left) +
            (sequentWeight target delta + atomWeight target right) := by ac_rfl
        _ = 0 := by rw [hLeft, hRight]; rfl
  | par premise premiseIH =>
      have hPremise := premiseIH
      simpa [sequentWeight_append, sequentWeight, atomWeight, Int.add_assoc] using hPremise
  | exchange premise premiseIH =>
      have hPremise := premiseIH
      simpa [sequentWeight_append, sequentWeight, Int.add_assoc, Int.add_comm, Int.add_left_comm] using hPremise

open Formula

/-- PR #453 negative witness. -/
def sOr : Sequent := [aPerp, aPerp, .tensor a b]

/-- PR #453 positive witness. -/
def sAnd : Sequent := [aPerp, bPerp, .tensor a b]

/-- `S_or` is underivable by the atom-balance invariant. -/
theorem sOr_not_derivable : ¬ Derivable sOr := by
  intro derivation
  have balance := derivable_atom_balance derivation 0
  simp [sOr, a, aPerp, b, atomWeight, sequentWeight] at balance

/-- `S_and` is derivable by the split `{aPerp} | {bPerp}`. -/
theorem sAnd_derivable : Derivable sAnd := by
  simpa [sAnd, a, aPerp, b, bPerp] using
    (Derivable.tensor
      (gamma := [Formula.atom 0 false])
      (delta := [Formula.atom 1 false])
      (left := Formula.atom 0 true)
      (right := Formula.atom 1 true)
      (Derivable.ax 0)
      (Derivable.ax 1))

/-- Zero-premise states are axiom conclusions up to adjacent exchange. -/
def Terminal (sequent : Sequent) : Prop :=
  ∃ name,
    sequent = [.atom name false, .atom name true] ∨
    sequent = [.atom name true, .atom name false]

theorem sOr_not_terminal : ¬ Terminal sOr := by
  rintro ⟨name, h | h⟩ <;> simp [sOr] at h

theorem sAnd_not_terminal : ¬ Terminal sAnd := by
  rintro ⟨name, h | h⟩ <;> simp [sAnd] at h

/-- Rule-induced projection after forgetting which premises belong to the same rule instance. -/
inductive ProjectedSuccessor : Sequent -> Sequent -> Prop where
  | tensorLeft (gamma delta : Sequent) (left right : Formula) :
      ProjectedSuccessor
        (gamma ++ delta ++ [.tensor left right])
        (gamma ++ [left])
  | tensorRight (gamma delta : Sequent) (left right : Formula) :
      ProjectedSuccessor
        (gamma ++ delta ++ [.tensor left right])
        (delta ++ [right])
  | parPremise (gamma : Sequent) (left right : Formula) :
      ProjectedSuccessor
        (gamma ++ [.par left right])
        (gamma ++ [left, right])

/-- The projected successor truth set contains both 0 and 1. -/
def MixedSuccessors (sequent : Sequent) : Prop :=
  (∃ successor, ProjectedSuccessor sequent successor ∧ Derivable successor) ∧
  (∃ successor, ProjectedSuccessor sequent successor ∧ ¬ Derivable successor)

theorem aPerp_b_not_derivable : ¬ Derivable [aPerp, b] := by
  intro derivation
  have balance := derivable_atom_balance derivation 0
  simp [aPerp, b, atomWeight, sequentWeight] at balance

theorem singleton_a_not_derivable : ¬ Derivable [a] := by
  intro derivation
  have balance := derivable_atom_balance derivation 0
  simp [a, atomWeight, sequentWeight] at balance

/-- `S_or` has one provable and one unprovable projected successor. -/
theorem sOr_mixed_successors : MixedSuccessors sOr := by
  constructor
  · refine ⟨[aPerp, a], ?_, ?_⟩
    · simpa [sOr, a, aPerp, b] using
        (ProjectedSuccessor.tensorLeft
          [Formula.atom 0 false] [Formula.atom 0 false]
          (Formula.atom 0 true) (Formula.atom 1 true))
    · simpa [a, aPerp] using Derivable.ax 0
  · refine ⟨[aPerp, b], ?_, aPerp_b_not_derivable⟩
    simpa [sOr, a, aPerp, b] using
      (ProjectedSuccessor.tensorRight
        [Formula.atom 0 false] [Formula.atom 0 false]
        (Formula.atom 0 true) (Formula.atom 1 true))

/-- `S_and` has one provable and one unprovable projected successor. -/
theorem sAnd_mixed_successors : MixedSuccessors sAnd := by
  constructor
  · refine ⟨[aPerp, a], ?_, ?_⟩
    · simpa [sAnd, a, aPerp, b, bPerp] using
        (ProjectedSuccessor.tensorLeft
          [Formula.atom 0 false] [Formula.atom 1 false]
          (Formula.atom 0 true) (Formula.atom 1 true))
    · simpa [a, aPerp] using Derivable.ax 0
  · refine ⟨[a], ?_, singleton_a_not_derivable⟩
    simpa [sAnd, a, aPerp, b, bPerp] using
      (ProjectedSuccessor.tensorLeft
        [] [Formula.atom 0 false, Formula.atom 1 false]
        (Formula.atom 0 true) (Formula.atom 1 true))

/-- The exact negative witness profile used by `sOrSummary`. -/
theorem sOr_witness_certified :
    ¬ Derivable sOr ∧ ¬ Terminal sOr ∧ MixedSuccessors sOr :=
  ⟨sOr_not_derivable, sOr_not_terminal, sOr_mixed_successors⟩

/-- The exact positive witness profile used by `sAndSummary`. -/
theorem sAnd_witness_certified :
    Derivable sAnd ∧ ¬ Terminal sAnd ∧ MixedSuccessors sAnd :=
  ⟨sAnd_derivable, sAnd_not_terminal, sAnd_mixed_successors⟩

/--
The bounded SSS negative result, with the Boolean summaries backed by the actual governed MLL
sequents and resource splits rather than treated as application premises.
-/
theorem bounded_projected_decoder_failure (decoder : SuccessorDecoder) :
    decoderPrediction decoder sOrSummary ≠ sOrSummary.derivable ∨
      decoderPrediction decoder sAndSummary ≠ sAndSummary.derivable := by
  have _ := sOr_witness_certified
  have _ := sAnd_witness_certified
  exact projected_successor_decoder_failure decoder

end MLL

end FARCoreV11.SSS
