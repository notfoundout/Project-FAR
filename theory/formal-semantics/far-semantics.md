# FAR Formal Semantics

## Status

Initial semantic specification.

---

## Purpose

This document defines the first formal semantics for FAR objects.

The key relation is satisfaction:

```text
A ⊨ φ
```

where `A` is a FAR model and `φ` is a FAR statement or representation-level condition.

---

# 1. FAR Model

A FAR model has the form:

```text
A = <I, Rep, S, Int, C>
```

where:

- `I` supplies investigation context;
- `Rep` supplies representation objects;
- `S` supplies structural relations;
- `Int` maps representations to semantic content;
- `C` supplies admissibility rules.

---

# 2. Syntactic Objects

Syntactic objects are representations and relations before interpretation.

A syntactic object can be well-formed without being true, justified, admissible, or semantically resolved.

---

# 3. Semantic Assignment

An interpretation is a mapping:

```text
Int : Rep -> Meaning
```

relative to an investigation `I`.

The same representation may receive different meanings under different interpretations.

---

# 4. Satisfaction

A FAR model `A` satisfies a representation condition `φ`, written:

```text
A ⊨ φ
```

when `φ` holds under the investigation, structure, interpretation, and calculus supplied by `A`.

Examples:

```text
A ⊨ represented(r)
A ⊨ interpreted(r)
A ⊨ supports(r1, r2)
A ⊨ admissible(t)
A ⊨ semantically_equivalent(r1, r2)
```

---

# 5. Satisfaction Clauses

## Represented

```text
A ⊨ represented(r)
```

iff `r ∈ Rep`.

## Interpreted

```text
A ⊨ interpreted(r)
```

iff `r ∈ Rep` and `Int(r)` is defined.

## Structural Relation

```text
A ⊨ relation(type, r1, r2)
```

iff `(type, r1, r2) ∈ S`.

## Admissible Transition

```text
A ⊨ admissible(t)
```

iff `C` permits transition `t` under the current investigation and state.

## Semantic Equivalence

```text
A ⊨ r1 ≡sem r2
```

iff `Int(r1) = Int(r2)` or the supplied semantic-equivalence rule in `C` identifies them as equivalent.

---

# 6. Syntax/Semantics Distinction

Syntax answers:

```text
What objects and relations are written?
```

Semantics answers:

```text
What do those objects and relations mean under an interpretation?
```

Admissibility answers:

```text
Which transitions are allowed under the calculus?
```

Truth, validity, support, and resolution are not identical unless the calculus explicitly identifies them.

---

# 7. Semantic Failure

If `Int(r)` is undefined, FAR may still represent `r` syntactically.

However:

```text
A ⊭ interpreted(r)
```

This allows FAR to represent semantic defects rather than hiding them.

---

# 8. Scope

This semantics applies to explicit FAR objects encoded according to the formal language specification.

It does not claim to capture private, unreconstructed, or non-explicit mental events.
