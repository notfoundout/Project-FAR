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

structure Witness where
  constructorId : String
  deriving Repr, DecidableEq

def FaithfulSplit (source : Source) (target : Target) (witness : Witness) : Prop :=
  witness.constructorId = "uniform-S_core-v1" ∧
  target.state = source.configurations ∧
  target.positions = source.commitments ∧
  target.investigation = source.stakes ∧
  target.provenance = source.grounds ∧
  target.calculus = source.admissibleTransitions ∧
  target.result = source.consequences ∧
  target.history = source.history ∧
  target.interpretation = source.evidentialStatus

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

def encodeWitness : Witness :=
  { constructorId := "uniform-S_core-v1" }

theorem encode_is_faithful (source : Source) :
    FaithfulSplit source (encode source) encodeWitness := by
  simp [FaithfulSplit, encode, encodeWitness]

theorem asm_sc_001_common_schema :
    ∀ source : Source, Nonempty (Target × Witness) := by
  intro source
  exact ⟨(encode source, encodeWitness)⟩

theorem asm_sc_002_bounded_faithful_representation :
    ∀ source : Source,
      ∃ target : Target, ∃ witness : Witness,
        FaithfulSplit source target witness := by
  intro source
  exact ⟨encode source, encodeWitness, encode_is_faithful source⟩

theorem bounded_impossibility_refuted (source : Source) :
    ¬ (∀ target : Target, ∀ witness : Witness,
        ¬ FaithfulSplit source target witness) := by
  intro impossible
  exact impossible (encode source) encodeWitness (encode_is_faithful source)

theorem asm_sc_003_theorem_family :
    (∀ source : Source,
      ∃ target : Target, ∃ witness : Witness,
        FaithfulSplit source target witness) ∧
    (∀ source : Source,
      ¬ (∀ target : Target, ∀ witness : Witness,
          ¬ FaithfulSplit source target witness)) := by
  constructor
  · exact asm_sc_002_bounded_faithful_representation
  · exact bounded_impossibility_refuted

theorem thm_core_rep_001 :
    ∀ source : Source,
      ∃ target : Target, ∃ witness : Witness,
        FaithfulSplit source target witness :=
  asm_sc_002_bounded_faithful_representation

end FAR.SCoreW5
