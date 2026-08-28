import FARCoreV11Claims001To012
import FARCoreV11Omega
import FARCoreV11SSS

/-!
# Project FAR core v1.1 mutation and negative controls

These are executable countermodels to common stronger readings or premise deletions.  They
are not additional governing claims.  Each theorem should continue to compile; replacing a
guarded theorem with its stronger false reading would contradict one of these witnesses.
-/

namespace FARCoreV11Mutations

open FARCoreV11

/-! ## FAR-CORE-001--004 -/

/-- Removing kernel refinement makes factorization fail even on two finite cases. -/
theorem collision_without_factorization :
    ¬ ExactlySufficient (id : Bool -> Bool) (fun _ : Bool => Unit.unit) := by
  apply collision_refutes_sufficiency (id : Bool -> Bool) (fun _ : Bool => Unit.unit)
    (x := false) (y := true)
  · rfl
  · simp

/-- An identity representation can be sufficient yet strictly more informative than beta. -/
theorem strictly_more_informative_is_not_least :
    ¬ KernelEqual (id : Bool × Bool -> Bool × Bool) (fun pair => pair.1) := by
  intro hkernels
  have hcollision := (hkernels (false, false) (false, true)).mpr rfl
  simp at hcollision

/-- An insufficient constant representation has no image-level exact decoder. -/
theorem insufficient_map_has_no_factor :
    ¬ ∃ decoder : RepImage (fun _ : Bool => Unit.unit) -> Bool,
      ∀ x, decoder (imageValue (fun _ : Bool => Unit.unit) x) = x := by
  exact collision_without_factorization

/-- A singleton domain does not supply the distinct-case premise of FAR-CORE-004. -/
theorem singleton_does_not_witness_no_minimum :
    KernelEqual (id : Unit -> Unit) (fun _ : Unit => true) ∧
      KernelEqual (id : Unit -> Unit) (id : Unit -> Unit) := by
  constructor <;> intro x y <;> cases x <;> cases y <;> simp [KernelEqual]

/-! ## FAR-CORE-003 and FAR-CORE-005 -/

def coarseObservation (_test : Unit) (state : Bool × Bool) : Bool := state.1
def splittingAction (state : Bool × Bool) : Bool × Bool := (state.2, state.2)

/-- Without context closure, observational equivalence need not survive an action. -/
theorem missing_context_closure_breaks_descent :
    ObservationallyEquivalent coarseObservation (false, false) (false, true) ∧
      ¬ ObservationallyEquivalent coarseObservation
        (splittingAction (false, false)) (splittingAction (false, true)) := by
  constructor
  · intro test
    cases test
    rfl
  · intro hequivalent
    have := hequivalent Unit.unit
    simp [coarseObservation, splittingAction] at this

def flipBool : Bool -> Bool
  | false => true
  | true => false

/-- Reversing the invariance inclusion direction is false. -/
theorem reverse_invariance_inclusion_is_false :
    let smaller : (Bool -> Bool) -> Prop := fun _ => False
    let larger : (Bool -> Bool) -> Prop := fun transformation => transformation = flipBool
    let property : Bool -> Prop := fun value => value = false
    (∀ transformation, smaller transformation -> larger transformation) ∧
      InvariantUnder smaller property ∧ ¬ InvariantUnder larger property := by
  dsimp
  constructor
  · intro transformation hmember
    cases hmember
  constructor
  · intro transformation hmember
    cases hmember
  · intro hinvariant
    have hflip := hinvariant flipBool rfl false
    simp [flipBool] at hflip

/-! ## FAR-CORE-006--009 -/

/-- A noninjective encoding cannot have a source-recovering left inverse. -/
theorem encoding_without_injectivity_loses_recovery :
    ¬ ∃ decoder : Unit -> Bool, ∀ x, decoder Unit.unit = x := by
  rintro ⟨decoder, hdecoder⟩
  have := (hdecoder false).symm.trans (hdecoder true)
  simp at this

def asymmetricRelation (left right : Bool) : Prop := left = false ∧ right = true

def untypedIncidence
    (occurrence : FARCoreV11.RelationOccurrence asymmetricRelation) (value : Bool) : Prop :=
  occurrence.val.1 = value ∨ occurrence.val.2 = value

/-- Dropping typed argument positions makes the reified occurrence symmetric at recovery. -/
theorem untyped_incidence_does_not_recover_positions :
    asymmetricRelation false true ∧
      (∃ occurrence : FARCoreV11.RelationOccurrence asymmetricRelation,
        untypedIncidence occurrence false ∧ untypedIncidence occurrence true) ∧
      ¬ asymmetricRelation true false := by
  refine ⟨by simp [asymmetricRelation], ?_, by simp [asymmetricRelation]⟩
  exact ⟨⟨(false, true), by simp [asymmetricRelation]⟩,
    by simp [untypedIncidence], by simp [untypedIncidence]⟩

/-- Without an operator tag, one Unit argument cannot recover two distinct constants. -/
theorem dropping_operator_tag_causes_collision :
    ¬ ∃ dispatcher : Unit -> Bool,
      dispatcher Unit.unit = false ∧ dispatcher Unit.unit = true := by
  rintro ⟨dispatcher, hfalse, htrue⟩
  have := hfalse.symm.trans htrue
  simp at this

/-- Agreement on a panel does not imply coverage of its complement. -/
theorem coverage_premise_is_not_optional :
    let panel : List Unit := []
    (∀ x ∈ panel, True) ∧ ¬ (∀ _x : Unit, False) := by
  dsimp
  constructor
  · intro x hmember
    cases hmember
  · simp

/-! ## FAR-CORE-010--012 -/

/-- A fixed exact theory coexists with frame-sensitive residue. -/
theorem frame_changes_residue_not_exact_theory :
    let truth : Unit -> Bool -> Prop := fun _ _ => True
    let consequence : (Bool -> Prop) -> Bool -> Prop := id
    let frame₀ : Bool -> Prop := fun _ => False
    let frame₁ : Bool -> Prop := fun value => value = true
    CommonTheory truth = CommonTheory truth ∧
      Residue truth consequence frame₀ ≠ Residue truth consequence frame₁ := by
  dsimp
  constructor
  · rfl
  · apply residue_can_change_with_frame
      (truth := fun _ : Unit => fun _ : Bool => True)
      (consequence := id) (frame₀ := fun _ => False)
      (frame₁ := fun value => value = true) (sentence := true)
    · intro index
      trivial
    · simp
    · simp

/-- If behavior does not change, a constant representation can still be sufficient. -/
theorem no_behavior_change_no_refutation :
    ExactlySufficient (fun _ : Bool => Unit.unit) (fun _ : Bool => Unit.unit) := by
  refine ⟨fun _ => Unit.unit, ?_⟩
  intro x
  rfl

def absentUnknownBehavior : Bool -> EpistemicOutcome
  | false => .absent
  | true => .unknown

/-- Collapsing reachable absence and Unknown is exactly insufficient. -/
theorem absent_unknown_collapse_is_insufficient :
    ¬ ExactlySufficient absentUnknownBehavior (fun _ : Bool => Unit.unit) := by
  apply collision_refutes_sufficiency absentUnknownBehavior (fun _ : Bool => Unit.unit)
    (x := false) (y := true)
  · rfl
  · simp [absentUnknownBehavior]

end FARCoreV11Mutations
