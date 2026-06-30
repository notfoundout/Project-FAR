# Notation

## Purpose

This document defines the symbols, identifiers, and naming conventions used throughout the formal theory of Project FAR.

Unless explicitly stated otherwise, all notation used elsewhere in Project FAR refers to the conventions established here.

---

# Mathematical Symbols

## Ω

**Ω** denotes the **Admissibility Structure**.

Ω classifies the admissibility status of every candidate admitted for consideration within an investigation.

---

# Statement Identifiers

Formal statements are assigned stable identifiers.

## Definitions

```text
D-IDENTIFIER
```

Example:

```text
D-REPRESENTATION
D-INVESTIGATION
```

---

## Axioms

```text
A-IDENTIFIER
```

Example:

```text
A-CONSISTENCY
```

---

## Conjectures

```text
C-IDENTIFIER
```

Example:

```text
C-UNIVERSAL-ARCHITECTURE
```

---

## Propositions

```text
P-IDENTIFIER
```

Example:

```text
P-REPRESENTATION-INDEPENDENCE
```

---

## Theorems

```text
T-IDENTIFIER
```

Example:

```text
T-ARCHITECTURE-INDEPENDENCE
```

---

# Proof Documents

Proof documents should follow the naming convention:

```text
proof-t-identifier.md
```

Example:

```text
proof-t-architecture-independence.md
```

---

# Dependencies

Whenever a formal statement depends upon another result, the dependency should be referenced using its identifier.

Example:

```text
Dependencies

- D-REPRESENTATION
- D-INTERPRETATION
- A-CONSISTENCY
- P-REPRESENTATION-INDEPENDENCE
- T-ARCHITECTURE-INDEPENDENCE
```

---

# Naming Conventions

Identifiers should:

- Remain stable over time.
- Be descriptive.
- Use uppercase letters.
- Separate words with hyphens.
- Never be reassigned to different statements.

---

# Design Principle

Stable identifiers ensure that references remain valid as the formal theory expands.

Whenever possible, references should use identifiers rather than document headings or page locations.
