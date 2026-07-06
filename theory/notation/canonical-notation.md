# Canonical Notation

## Purpose

This document fixes the notation used across Project FAR proofs, model theory, examples, and audits.

No proof should introduce a conflicting meaning for these symbols without explicitly declaring a local override.

---

# Core Tuple

A FAR representation of a reasoning process `R` is written:

```text
FAR(R) = <I, Rep, S, Int, C, T>
```

where:

| Symbol | Meaning |
|---|---|
| `R` | A scoped explicit reasoning process |
| `I` | Investigation |
| `Rep` | Set or ordered collection of representations |
| `S` | Representational structure over `Rep` |
| `Int` | Interpretation assigning semantic content to representations within `I` |
| `C` | Reasoning calculus governing admissible transitions |
| `T` | Reasoning trace |

---

# Model Notation

A FAR model is written:

```text
A = <I, Rep, S, Int, C>
```

A model satisfies a statement `φ` when:

```text
A ⊨ φ
```

This means `φ` holds under the structure, interpretation, investigation, and calculus supplied by `A`.

A class of models `K` satisfies `φ` when:

```text
K ⊨ φ
```

This means every model in `K` satisfies `φ`.

---

# Mapping Notation

A representation mapping is written:

```text
M: Rep1 -> Rep2
```

A mapping preserves semantic content when:

```text
Int1(r) = Int2(M(r))
```

for every mapped representation `r`.

---

# Equivalence Notation

Semantic equivalence is written:

```text
r ≡sem r'
```

Structural equivalence is written:

```text
S ≡str S'
```

Model equivalence relative to a preservation profile `Q` is written:

```text
A ≡Q B
```

Canonical representation equivalence is written:

```text
FAR(R)1 ≡can FAR(R)2
```

---

# Transition Notation

A transition is written:

```text
t: state_i -> state_j
```

A calculus permits a transition when:

```text
C ⊢ t
```

A transition signature is written:

```text
Sig(t) = <source, rule, target, status, order>
```

where:

| Component | Meaning |
|---|---|
| `source` | Initial reasoning state |
| `rule` | Applied rule or rule class |
| `target` | Resulting reasoning state |
| `status` | Admissible, inadmissible, or unresolved |
| `order` | Position in the reasoning trace |

---

# Normal Form Notation

The canonical normal form of a FAR representation is written:

```text
NF(FAR(R))
```

or simply:

```text
NF(R)
```

when no ambiguity exists.

---

# Scope Notation

A process belongs to Project FAR scope when:

```text
R ∈ Scope(FAR)
```

This means the process is explicit enough to identify an investigation, representations, structure, interpretation, and calculus.

---

# Prohibition

The same symbol must not be used for two different canonical meanings in the same document.
