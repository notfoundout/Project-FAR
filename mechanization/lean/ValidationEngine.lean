import Std

/-!
# Project FAR validation-engine assurance model

This file proves the abstract safety properties required by the executable
validation engine. It does not claim a verified refinement from the Python
implementation to this model; that separate correspondence claim remains
explicitly out of scope.
-/

namespace FAR.Validation

inductive Status where
  | passed
  | failed
  | blocked
  deriving Repr, DecidableEq

/-- A check may run only after every declared dependency has passed. -/
def dependenciesPassed (dependencies : List Status) : Bool :=
  dependencies.all (· == Status.passed)

/-- Abstract execution decision for one check. -/
def decide (dependencies : List Status) (checkSucceeds : Bool) : Status :=
  if dependenciesPassed dependencies then
    if checkSucceeds then Status.passed else Status.failed
  else
    Status.blocked

/-- Passing is possible exactly when dependencies pass and the check succeeds. -/
theorem decide_passed_iff
    (dependencies : List Status)
    (checkSucceeds : Bool) :
    decide dependencies checkSucceeds = Status.passed ↔
      dependenciesPassed dependencies = true ∧ checkSucceeds = true := by
  simp [decide, dependenciesPassed]

/-- Any failed dependency forces the dependent check into the blocked state. -/
theorem failed_dependency_forces_block
    (dependencies : List Status)
    (checkSucceeds : Bool)
    (h : dependenciesPassed dependencies = false) :
    decide dependencies checkSucceeds = Status.blocked := by
  simp [decide, h]

/-- A blocked check cannot be reported as passed. -/
theorem blocked_ne_passed : Status.blocked ≠ Status.passed := by
  decide

/-- A run is successful only when every selected result is passed. -/
def runSuccessful (results : List Status) : Bool :=
  results.all (· == Status.passed)

/-- The aggregate succeeds exactly when every selected result passed. -/
theorem runSuccessful_iff_all_passed
    (results : List Status) :
    runSuccessful results = true ↔ ∀ status ∈ results, status = Status.passed := by
  induction results with
  | nil => simp [runSuccessful]
  | cons head tail ih =>
      simp [runSuccessful, ih]

/-- Successful runs contain no failed result. -/
theorem successful_run_has_no_failure
    (results : List Status)
    (h : runSuccessful results = true) :
    Status.failed ∉ results := by
  intro hFailed
  have hAll := (runSuccessful_iff_all_passed results).mp h
  have hImpossible := hAll Status.failed hFailed
  simp at hImpossible

/-- Successful runs contain no blocked result. -/
theorem successful_run_has_no_block
    (results : List Status)
    (h : runSuccessful results = true) :
    Status.blocked ∉ results := by
  intro hBlocked
  have hAll := (runSuccessful_iff_all_passed results).mp h
  have hImpossible := hAll Status.blocked hBlocked
  simp at hImpossible

structure Certificate where
  commit : String
  tree : String
  successful : Bool
  deriving Repr, DecidableEq

/-- Merge authorization binds the certificate to the exact checked commit/tree. -/
def Authorized
    (expectedCommit expectedTree : String)
    (certificate : Certificate) : Prop :=
  certificate.commit = expectedCommit ∧
  certificate.tree = expectedTree ∧
  certificate.successful = true

/-- An authorized certificate cannot be replayed for a different commit. -/
theorem authorization_binds_commit
    (expectedCommit expectedTree : String)
    (certificate : Certificate)
    (h : Authorized expectedCommit expectedTree certificate) :
    certificate.commit = expectedCommit := by
  exact h.1

/-- An authorized certificate cannot be replayed for a different tree. -/
theorem authorization_binds_tree
    (expectedCommit expectedTree : String)
    (certificate : Certificate)
    (h : Authorized expectedCommit expectedTree certificate) :
    certificate.tree = expectedTree := by
  exact h.2.1

/-- Authorization implies the recorded validation result is successful. -/
theorem authorization_requires_success
    (expectedCommit expectedTree : String)
    (certificate : Certificate)
    (h : Authorized expectedCommit expectedTree certificate) :
    certificate.successful = true := by
  exact h.2.2

end FAR.Validation
