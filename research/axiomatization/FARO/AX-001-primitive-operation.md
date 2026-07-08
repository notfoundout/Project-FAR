# FARO Axiomatization

## Identifier

AX-001

---

# Title

Primitive Operation

---

## Status

Draft

---

# Purpose

Determine whether operation can serve as the primitive concept of FARO.

The objective is to test whether operation can be treated as irreducible without circularity.

---

# Central Question

Can operation be defined without presupposing operation?

---

# Dependencies

Logical dependencies:

- `research/methodology/primitive-identification.md` — supplies the primitive-identification criteria used to evaluate operation as a primitive candidate.
- `research/discovery/FARO/FARO-026-reducibility-of-operation.md` — supplies the direct repository reduction evidence for operation.

Informative dependencies:

- `frameworks/FARO/theory/definitions.md` — provides current FARO terminology, including the accepted FARO definition of operation, but AX-001 evaluates primitive candidacy rather than adopting that definition as proof.
- `research/discovery/FARO/FARO-001-operational-necessity.md` through `research/discovery/FARO/FARO-025-operational-versus-architectural-constraints.md` — provide the research chain summarized by FARO-026 and explain why reducibility of operation became the active question. They are not direct logical dependencies of AX-001 except through FARO-026.

Historical dependencies:

- None identified.

Dependency audit note: AX-001 previously listed `FARO-001 through FARO-026`. The validation audit found that this overstated direct logical dependence. FARO-026 is the direct logical dependency for operation reducibility; FARO-001 through FARO-025 remain informative background because FARO-026 depends on and summarizes that chain.

---

# Candidate Primitive

Operation.

---

# Working Characterization

An operation is an executable act performed within a reasoning process.

This is not yet a formal definition.

It is a provisional characterization used to test whether a non-circular definition is possible.

---

# Reduction Attempts

## Attempt 1

Operation as state transition.

Result:

Rejected.

Some operations may preserve state.

---

## Attempt 2

Operation as representation modification.

Result:

Rejected.

Some operations inspect, verify, or evaluate without modifying representations.

---

## Attempt 3

Operation as calculus application.

Result:

Rejected.

Calculi describe or constrain operations but do not constitute operation itself.

---

# Provisional Result

Current evidence supports treating operation as a primitive of FARO.

This does not prove irreducibility.

---

# Next Step

AX-002 should identify the smallest candidate axiom set governing operation.