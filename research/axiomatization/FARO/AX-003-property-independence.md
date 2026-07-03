# FARO Axiomatization

## Identifier

AX-003

---

# Title

Property Independence

---

## Status

Draft

---

# Purpose

Determine whether the candidate properties identified in AX-002 are logically independent.

The objective is to eliminate redundant candidate axioms.

---

# Central Question

Can any candidate property be derived from the others?

---

# Dependencies

- AX-001 — Primitive Operation
- AX-002 — Properties of Operation

---

# Background

AX-002 identified three candidate necessary properties.

- Executability
- Applicability
- Operational Effect

Before elevating these properties to axioms, each must be tested for logical independence.

---

# Candidate Property 1

Executability

Question:

Can executability be derived from applicability and operational effect?

Analysis:

An operation may be applicable to a reasoning state.

An operation may also possess an intended operational effect.

Neither condition guarantees that execution can actually occur.

Applicability and effect therefore do not imply executability.

Result:

Not derivable.

---

# Candidate Property 2

Applicability

Question:

Can applicability be derived from executability and operational effect?

Analysis:

An executable operation possessing an operational effect must still possess some domain over which execution is possible.

Without applicability, execution cannot occur.

Executability therefore presupposes applicability.

Result:

Potentially derivable.

Further investigation required.

---

# Candidate Property 3

Operational Effect

Question:

Can operational effect be derived from executability and applicability?

Analysis:

An executable operation may be applicable.

However, if execution produces no identifiable consequence, the operation cannot be distinguished from non-execution.

Operational effect is therefore not implied.

Result:

Not derivable.

---

# Preliminary Dependency Graph

Executability

↓

Applicability

?

Operational Effect

Current dependency remains unresolved.

---

# Observation

The candidate properties do not presently appear equally fundamental.

Applicability may prove reducible.

Executability and operational effect currently appear stronger candidates for primitive status.

---

# Current Conclusion

No candidate property has yet been accepted as an axiom.

Applicability requires additional investigation before independence can be established.

---

# Next Step

AX-004 shall determine whether applicability is primitive or follows necessarily from executability.