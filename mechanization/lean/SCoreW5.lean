import Std

/-!
# Project FAR bounded W5 theorem mechanization

This file machine-checks the bounded `S_core` assembly result. It formalizes a
finite, explicit source presentation, a fixed theorem-facing FARA target
interface, a uniform constructor, and the internal `Faithful_split` preservation
predicate.

The result is intentionally bounded. It does not prove that `S_core` contains
all reasoning, does not prove representation over `S_IRD`, does not establish
external process correspondence, and does not prove primitive necessity,
minimality, uniqueness, reasoning specificity, or universal structure.
-/

namespace FAR.SCoreW5

/-- Finite explicit source presentations used by the bounded theorem. -/
structure Source where
  configurations : List String
  commitments : List String
  stakes : List String
  grounds : List String
  admissibleTransitions : List String
  consequences : List String
  history : List String
  evidentialStatus : List String
  deriving Repr, DecidableEq

/-- The fixed theorem-facing FARA interface used for every bounded source. -/
structure Target where
  universe : List String
  positions : List String
  relations : List String
  representations : List String
  structureAxis : List String
  interpretation : List String
  investigation : List String
  calculus : List String
  state : List String
  transition : List String
  history : List String
  outcomes : List String
  result : List String
  provenance : List String
  deriving Repr, DecidableEq

/-- Explicit witness connecting each source preservation axis to the target. -/
structure Witness (source : Source) (target : Target) where
  configuration : target.state = source.configurations
  commitment : target.positions = source.commitments
  stake : target.investigation = source.stakes
  ground : target.provenance = source.grounds
  admissibility : target.calculus = source.admissibleTransitions
  consequence : target.result = source.consequences
  historical : target.history = source.history
  evidential : target.interpretation = source.evidentialStatus

/-- Internal faithful-representation predicate used by the W5 bounded theorem. -/
def FaithfulSplit (source : Source) (target : Target) (_witness : Witness source target) : Prop :=
  target.state = source.configurations ∧
  target.positions = source.commitments ∧
  target.investigation = source.stakes ∧
  target.provenance = source.grounds ∧
  target.calculus = source.admissibleTransitions ∧
  target.result = source.consequences ∧
  target.history = source.history ∧
  target.interpretation = source.evidentialStatus

/-- One uniform constructor into the same fixed target structure for all sources. -/
def encode (source : Source) : Target :=
  {
    universe := source.configurations ++ source.commitments ++ source.stakes
    positions := source.commitments
    relations := source.grounds
    representations := source.configurations ++ source.commitments
    structureAxis := source.grounds
    interpretation := source.evidentialStatus
    investigation := source.stakes
    calculus := source.admissibleTransitions
    state := source.configurations
    transition := source.admissibleTransitions
    history := source.history
    outcomes := source.consequences
    result := source.consequences
    provenance := source.grounds
  }

/-- Canonical preservation witness produced by the uniform constructor. -/
def encodeWitness (source : Source) : Witness source (encode source) :=
  {
    configuration := rfl
    commitment := rfl
    stake := rfl
    ground := rfl
    admissibility := rfl
    consequence := rfl
    historical := rfl
    evidential := rfl
  }

/-- The canonical witness satisfies all eight internal preservation clauses. -/
theorem encode_is_faithful (source : Source) :
    FaithfulSplit source (encode source) (encodeWitness source) := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- ASM-SC-001: one fixed target schema and one uniform constructor cover `S_core`. -/
theorem asm_sc_001_common_schema :
    ∀ source : Source, Nonempty (Target × Witness source (encode source)) := by
  intro source
  exact ⟨(encode source, encodeWitness source)⟩

/-- ASM-SC-002 / THM-CORE-REP-001: every bounded source has a faithful target witness. -/
theorem asm_sc_002_bounded_faithful_representation :
    ∀ source : Source,
      ∃ target : Target, ∃ witness : Witness source target,
        FaithfulSplit source target witness := by
  intro source
  exact ⟨encode source, encodeWitness source, encode_is_faithful source⟩

/-- The bounded impossibility alternative is refuted by the constructive witness. -/
theorem bounded_impossibility_refuted (source : Source) :
    ¬ (∀ target : Target, ∀ witness : Witness source target,
        ¬ FaithfulSplit source target witness) := by
  intro impossible
  exact impossible (encode source) (encodeWitness source) (encode_is_faithful source)

/-- ASM-SC-003: bounded theorem-family adjudication. -/
theorem asm_sc_003_theorem_family :
    (∀ source : Source,
      ∃ target : Target, ∃ witness : Witness source target,
        FaithfulSplit source target witness) ∧
    (∀ source : Source,
      ¬ (∀ target : Target, ∀ witness : Witness source target,
          ¬ FaithfulSplit source target witness)) := by
  constructor
  · exact asm_sc_002_bounded_faithful_representation
  · exact bounded_impossibility_refuted

/-- Exact quantified result registered by the W5 proof artifact. -/
theorem thm_core_rep_001 :
    ∀ source : Source,
      ∃ target : Target, ∃ witness : Witness source target,
        FaithfulSplit source target witness :=
  asm_sc_002_bounded_faithful_representation

end FAR.SCoreW5
