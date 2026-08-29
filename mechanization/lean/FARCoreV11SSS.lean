import FARCoreV11Substrate

/-!
# FAR-CORE-014: bounded Search-State Sufficiency application

This module kernel-checks the exhaustive four-decoder result, the two Boolean witness profiles,
the governed unit-free one-sided MLL witness facts, and the hyperedge/frontier factorization
bridges.  The MLL section is deliberately bounded to the exact representation and decoder class
preserved from PR #453; it is not a universal architecture theorem.
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

/-- Summary of S_or, certified below against the governed MLL witness. -/
def sOrSummary : WitnessSummary := ⟨false, false, .mixed⟩

/-- Summary of S_and, certified below against the governed MLL witness. -/
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

/-! ## Governed unit-free MLL witness layer

This is the one-sided cut-free multiplicative fragment used in the preserved PR #453 witness
argument.  Sequents are lists modulo an explicit exchange rule.  The atom-balance invariant is
proved for the calculus and is then used to certify the negative witness and its negative
successors.  No witness truth value is postulated.
-/

inductive MLLFormula where
  | atom (name : Nat) (positive : Bool)
  | tensor (left right : MLLFormula)
  | par (left right : MLLFormula)
  deriving DecidableEq, Repr

abbrev MLLSequent := List MLLFormula

namespace MLLFormula

def a : MLLFormula := .atom 0 true
def aPerp : MLLFormula := .atom 0 false
def b : MLLFormula := .atom 1 true
def bPerp : MLLFormula := .atom 1 false
end MLLFormula

/-- Cut-free, unit-free, one-sided MLL with explicit exchange. -/
inductive MLLDerivable : MLLSequent -> Prop where
  | ax (name : Nat) : MLLDerivable [.atom name false, .atom name true]
  | tensor {gamma delta : MLLSequent} {left right : MLLFormula} :
      MLLDerivable (gamma ++ [left]) ->
      MLLDerivable (delta ++ [right]) ->
      MLLDerivable (gamma ++ delta ++ [.tensor left right])
  | par {gamma : MLLSequent} {left right : MLLFormula} :
      MLLDerivable (gamma ++ [left, right]) ->
      MLLDerivable (gamma ++ [.par left right])
  | exchange {source target : MLLSequent} :
      source.Perm target -> MLLDerivable source -> MLLDerivable target

/-- Signed occurrence count of one atom inside a formula. -/
def atomWeight (target : Nat) : MLLFormula -> Int
  | .atom name true => if name = target then 1 else 0
  | .atom name false => if name = target then -1 else 0
  | .tensor left right => atomWeight target left + atomWeight target right
  | .par left right => atomWeight target left + atomWeight target right

/-- Signed occurrence count of one atom across a sequent. -/
def sequentWeight (target : Nat) : MLLSequent -> Int
  | [] => 0
  | formula :: rest => atomWeight target formula + sequentWeight target rest

@[simp] theorem sequentWeight_append (target : Nat) (left right : MLLSequent) :
    sequentWeight target (left ++ right) =
      sequentWeight target left + sequentWeight target right := by
  induction left with
  | nil => simp [sequentWeight]
  | cons formula rest ih =>
      simp [sequentWeight, ih, Int.add_assoc]

/-- Exchange does not change signed atom balance. -/
theorem sequentWeight_perm (target : Nat) {source targetSeq : MLLSequent}
    (permutation : source.Perm targetSeq) :
    sequentWeight target source = sequentWeight target targetSeq := by
  induction permutation with
  | nil => rfl
  | cons formula permutation ih =>
      simp [sequentWeight, ih]
  | swap first second rest =>
      simp [sequentWeight, Int.add_assoc, Int.add_comm, Int.add_left_comm]
  | trans first second ihFirst ihSecond =>
      exact ihFirst.trans ihSecond

/-- Every cut-free unit-free MLL derivation is atom-balanced. -/
theorem mll_derivable_atom_balance {sequent : MLLSequent}
    (derivation : MLLDerivable sequent) (target : Nat) :
    sequentWeight target sequent = 0 := by
  induction derivation with
  | ax name =>
      simp [sequentWeight, atomWeight]
  | @tensor gamma delta left right leftDerivation rightDerivation leftIH rightIH =>
      have hLeft := leftIH target
      have hRight := rightIH target
      simp [sequentWeight_append, sequentWeight, atomWeight] at hLeft hRight ⊢
      omega
  | @par gamma left right premise premiseIH =>
      have hPremise := premiseIH target
      simp [sequentWeight_append, sequentWeight, atomWeight] at hPremise ⊢
      omega
  | @exchange source targetSeq permutation sourceDerivation sourceIH =>
      rw [← sequentWeight_perm target permutation]
      exact sourceIH target

open MLLFormula

/-- The preserved negative witness S_or. -/
def sOr : MLLSequent := [aPerp, aPerp, .tensor a b]

/-- The preserved positive witness S_and. -/
def sAnd : MLLSequent := [aPerp, bPerp, .tensor a b]

/-- S_or is not MLL-derivable because atom a is unbalanced. -/
theorem sOr_not_derivable : ¬ MLLDerivable sOr := by
  intro derivation
  have balance := mll_derivable_atom_balance derivation 0
  simp [sOr, a, aPerp, b, atomWeight, sequentWeight] at balance

/-- S_and is MLL-derivable by the resource split {aPerp} | {bPerp}. -/
theorem sAnd_derivable : MLLDerivable sAnd := by
  simpa [sAnd, a, aPerp, b, bPerp] using
    (MLLDerivable.tensor
      (gamma := [MLLFormula.atom 0 false])
      (delta := [MLLFormula.atom 1 false])
      (left := MLLFormula.atom 0 true)
      (right := MLLFormula.atom 1 true)
      (MLLDerivable.ax 0)
      (MLLDerivable.ax 1))

/-- Zero-premise MLL states are exactly axiom conclusions up to exchange. -/
def MLLTerminal (sequent : MLLSequent) : Prop :=
  ∃ name, sequent.Perm [.atom name false, .atom name true]

/-- Both witnesses are nonterminal because each contains three formulas. -/
theorem sOr_not_terminal : ¬ MLLTerminal sOr := by
  rintro ⟨name, permutation⟩
  have hLength := List.Perm.length_eq permutation
  simp [sOr] at hLength

theorem sAnd_not_terminal : ¬ MLLTerminal sAnd := by
  rintro ⟨name, permutation⟩
  have hLength := List.Perm.length_eq permutation
  simp [sAnd] at hLength

/-- Rule-induced projected successor relation after forgetting premise-family grouping. -/
inductive ProjectedMLLSuccessor : MLLSequent -> MLLSequent -> Prop where
  | tensorLeft (gamma delta : MLLSequent) (left right : MLLFormula) :
      ProjectedMLLSuccessor
        (gamma ++ delta ++ [.tensor left right])
        (gamma ++ [left])
  | tensorRight (gamma delta : MLLSequent) (left right : MLLFormula) :
      ProjectedMLLSuccessor
        (gamma ++ delta ++ [.tensor left right])
        (delta ++ [right])
  | parPremise (gamma : MLLSequent) (left right : MLLFormula) :
      ProjectedMLLSuccessor
        (gamma ++ [.par left right])
        (gamma ++ [left, right])

/-- A projected state exposes both a derivable and an underivable successor. -/
def MixedProjectedSuccessors (sequent : MLLSequent) : Prop :=
  (∃ successor, ProjectedMLLSuccessor sequent successor ∧ MLLDerivable successor) ∧
  (∃ successor, ProjectedMLLSuccessor sequent successor ∧ ¬ MLLDerivable successor)

/-- The negative successor used by S_or is atom-unbalanced. -/
theorem aPerp_b_not_derivable :
    ¬ MLLDerivable [aPerp, b] := by
  intro derivation
  have balance := mll_derivable_atom_balance derivation 0
  simp [aPerp, b, atomWeight, sequentWeight] at balance

/-- The singleton positive atom used by the alternate S_and split is underivable. -/
theorem singleton_a_not_derivable :
    ¬ MLLDerivable [a] := by
  intro derivation
  have balance := mll_derivable_atom_balance derivation 0
  simp [a, atomWeight, sequentWeight] at balance

/-- S_or has the mixed projected truth set {0,1}. -/
theorem sOr_mixed_projected_successors : MixedProjectedSuccessors sOr := by
  constructor
  · refine ⟨[aPerp, a], ?_, ?_⟩
    · simpa [sOr, a, aPerp, b] using
        (ProjectedMLLSuccessor.tensorLeft
          [MLLFormula.atom 0 false] [MLLFormula.atom 0 false]
          (MLLFormula.atom 0 true) (MLLFormula.atom 1 true))
    · simpa [a, aPerp] using MLLDerivable.ax 0
  · refine ⟨[aPerp, b], ?_, aPerp_b_not_derivable⟩
    simpa [sOr, a, aPerp, b] using
      (ProjectedMLLSuccessor.tensorRight
        [MLLFormula.atom 0 false] [MLLFormula.atom 0 false]
        (MLLFormula.atom 0 true) (MLLFormula.atom 1 true))

/-- S_and has the mixed projected truth set {0,1}. -/
theorem sAnd_mixed_projected_successors : MixedProjectedSuccessors sAnd := by
  constructor
  · refine ⟨[aPerp, a], ?_, ?_⟩
    · simpa [sAnd, a, aPerp, b, bPerp] using
        (ProjectedMLLSuccessor.tensorLeft
          [MLLFormula.atom 0 false] [MLLFormula.atom 1 false]
          (MLLFormula.atom 0 true) (MLLFormula.atom 1 true))
    · simpa [a, aPerp] using MLLDerivable.ax 0
  · refine ⟨[a], ?_, singleton_a_not_derivable⟩
    simpa [sAnd, a, aPerp, b, bPerp] using
      (ProjectedMLLSuccessor.tensorLeft
        [] [MLLFormula.atom 0 false, MLLFormula.atom 1 false]
        (MLLFormula.atom 0 true) (MLLFormula.atom 1 true))

/-- Exact certification of the Boolean summary used by the decoder impossibility theorem. -/
theorem sOr_witness_certified :
    ¬ MLLDerivable sOr ∧ ¬ MLLTerminal sOr ∧ MixedProjectedSuccessors sOr :=
  ⟨sOr_not_derivable, sOr_not_terminal, sOr_mixed_projected_successors⟩

/-- Exact certification of the positive witness used by the decoder impossibility theorem. -/
theorem sAnd_witness_certified :
    MLLDerivable sAnd ∧ ¬ MLLTerminal sAnd ∧ MixedProjectedSuccessors sAnd :=
  ⟨sAnd_derivable, sAnd_not_terminal, sAnd_mixed_projected_successors⟩

/--
FAR-CORE-014 negative half, now linked to the actual governed MLL witnesses rather than
postulated summary bits: every uniform monotone successor-set decoder fails on S_or or S_and.
-/
theorem bounded_mll_projected_decoder_failure (decoder : SuccessorDecoder) :
    decoderPrediction decoder sOrSummary ≠ sOrSummary.derivable ∨
      decoderPrediction decoder sAndSummary ≠ sAndSummary.derivable := by
  have _ := sOr_witness_certified
  have _ := sAnd_witness_certified
  exact projected_successor_decoder_failure decoder

/-! ## Exact factorization bridges -/

/-- Projected hyperedges preserve each jointly generated premise family. -/
abbrev HyperedgeView (State : Type u) := List (List State)

/-- The standard AND/OR behavior read from a hyperedge view. -/
def hyperedgeDecoder {State : Type u} (derivable : State -> Prop)
    (view : HyperedgeView State) : Prop :=
  ∃ premises ∈ view, ∀ premise ∈ premises, derivable premise

/--
FAR-CORE-014 positive hyperedge half: an exact rule-instance characterization makes the
resource-labelled hyperedge view sufficient.  The characterization is visible as a premise,
which is the governed statement itself rather than an added MLL-specific axiom.
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
FAR-CORE-014 positive frontier half: the governed frontier recursion makes the frontier/binary
step view sufficient for a finitary rule system.  The recursion is explicit as the theorem's
premise and therefore cannot be mistaken for a contract-free architecture claim.
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
