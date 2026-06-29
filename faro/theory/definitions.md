# FARO Definitions

## Purpose

This document defines the formal terminology used throughout FARO.

Unless explicitly stated otherwise, every technical term appearing elsewhere in FARO refers to the definitions established in this document.

Only canonical definitions belong in this document.

Candidate definitions remain within the research documents until formally accepted.

---

# Definition 1 — Operation

An **operation** is a formally specified mapping that accepts one or more admissible FAR objects as input and produces a formally defined output according to the rules of FARO.

---

# Definition 2 — Primitive Operation

A **primitive operation** is an operation whose behavior is not derivable from the remaining primitive operations within the operational architecture.

---

# Definition 3 — Derived Operation

A **derived operation** is an operation expressible as a finite composition of primitive operations.

---

# Definition 4 — Operational Expression

An **operational expression** is a well-formed syntactic object representing one or more FARO operations.

Operational expressions are generated according to the operational grammar.

---

# Definition 5 — Composition

**Composition** is the operation that combines operational expressions to produce a new operational expression.

---

# Definition 6 — Operational Equivalence

Two operational expressions are **operationally equivalent** if they produce identical operational behavior for every admissible input.

---

# Definition 7 — Rewrite Rule

A **rewrite rule** is a formally justified transformation that replaces one operational expression with an operationally equivalent expression.

---

# Definition 8 — Normal Form

A **normal form** is an operational expression to which no further rewrite rule applies.

---

# Definition 9 — Operational Semantics

**Operational semantics** assigns formal meaning to operational expressions.

---

# Definition 10 — Operational Proof

An **operational proof** is a finite sequence of justified inference steps establishing an operational statement according to the FARO proof system.


