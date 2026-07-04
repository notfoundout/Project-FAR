# FARE Mathematics Proofs

## Purpose

This directory contains active mathematical proofs within the FARE mathematics layer.

The proof library develops consequences of accepted mathematical definitions.

---

# Artifact Types

Definitions introduce objects.

Theorems establish properties of objects.

Lemmas establish reusable intermediate results.

Corollaries follow directly from accepted theorems.

Conjectures propose results that are not yet proven.

Examples illustrate mathematics but do not define or prove it.

---

# Dependency Ordering

Proofs shall depend only on earlier accepted dependencies.

No proof may depend on a Draft theorem.

No proof may depend on a conjecture.

No proof may depend on an archived legacy proof.

---

# Organization

```text
proofs/
├── README.md
├── foundations/
├── logic/
├── geometry/
├── topology/
├── analysis/
├── algorithms/
└── archive/
    └── legacy/
```

---

# Notes

The proof policy governs theorem acceptance and dependency rules.
