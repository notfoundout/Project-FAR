import Std

/- PCA-W5 bounded cost-order control. No universal scalarization is assumed. -/
namespace FAR.PCAW5

structure Cost where
  storage : Nat
  evaluation : Nat
  deriving DecidableEq

def leq (a b : Cost) : Prop := a.storage ≤ b.storage ∧ a.evaluation ≤ b.evaluation

def randomCost : Cost := ⟨1, 3⟩
def exactCost : Cost := ⟨3, 1⟩

theorem random_not_leq_exact : ¬ leq randomCost exactCost := by decide
theorem exact_not_leq_random : ¬ leq exactCost randomCost := by decide

theorem no_least_of_two : ¬ (leq randomCost exactCost ∨ leq exactCost randomCost) := by decide

-- With 0/1 metric loss, zero expected loss under positive case mass forces
-- each case loss to be zero; this is the finite two-case recovery boundary.
theorem zero_sum_boundary (a b : Nat) : a + b = 0 → a = 0 ∧ b = 0 := by
  intro sumEq
  cases a with
  | zero =>
      cases b with
      | zero => exact ⟨rfl, rfl⟩
      | succ _ => cases sumEq
  | succ _ =>
      cases b with
      | zero => cases sumEq
      | succ _ => cases sumEq

end FAR.PCAW5
