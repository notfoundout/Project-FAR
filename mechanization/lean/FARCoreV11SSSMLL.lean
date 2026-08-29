import FARCoreV11SSS

/-!
# FAR-CORE-014: governed MLL witness bridge

This file closes the application-only obstruction left in `FARCoreV11SSS.lean`.  It formalizes
exactly the cut-free, unit-free, one-sided MLL fragment and the two PR #453 witnesses used to
establish insufficiency of the rule-induced projected successor relation under the stated four
uniform monotone successor-set decoders.  It does not enlarge the representation or decoder
class and does not assert a universal architecture theorem.
-/

namespace FARCoreV11.SSS.MLL

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

/--
Cut-free, unit-free, one-sided MLL.  `exchange` is adjacent exchange; repeated applications
therefore generate arbitrary finite permutations without quotienting the syntax.
-/
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
      simp [sequentWeight, atomWeight]
  | tensor leftDerivation rightDerivation leftIH rightIH =>
      have hLeft := leftIH target
      have hRight := rightIH target
      simp [sequentWeight_append, sequentWeight, atomWeight] at hLeft hRight ⊢
      omega
  | par premise premiseIH =>
      have hPremise := premiseIH target
      simp [sequentWeight_append, sequentWeight, atomWeight] at hPremise ⊢
      omega
  | exchange premise premiseIH =>
      have hPremise := premiseIH target
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

/-- Zero-premise states are axiom conclusions, up to the only possible adjacent exchange. -/
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
The bounded SSS negative result, with the Boolean summaries now backed by the actual governed
MLL sequents and resource splits rather than treated as application premises.
-/
theorem bounded_projected_decoder_failure (decoder : SuccessorDecoder) :
    decoderPrediction decoder sOrSummary ≠ sOrSummary.derivable ∨
      decoderPrediction decoder sAndSummary ≠ sAndSummary.derivable := by
  have _ := sOr_witness_certified
  have _ := sAnd_witness_certified
  exact projected_successor_decoder_failure decoder

end FARCoreV11.SSS.MLL
