# Dependency Relation Properties

## Purpose

Determine the necessary properties of dependency relations within Project FAR.

The objective is to establish the formal characteristics that every valid dependency relation must satisfy.

---

# Motivation

Previous investigations identified multiple classes of dependency and proposed relationships among them.

Before constructing a formal dependency algebra, the dependency relation itself must be characterized.

---

# Central Question

What properties define a valid dependency relation?

---

# Candidate Property 1

Directionality.

Question:

Must every dependency possess direction?

Evaluation:

If Concept A depends upon Concept B, the reverse does not necessarily hold.

Dependency therefore distinguishes predecessor from successor.

Result:

Supported.

---

# Candidate Property 2

Irreflexivity.

Question:

Can a concept depend upon itself?

Evaluation:

A concept defined solely in terms of itself provides no explanatory reduction.

Circular dependence violates explanatory progress.

Result:

Provisionally Supported.

---

# Candidate Property 3

Antisymmetry.

Question:

Can two distinct concepts simultaneously depend upon one another?

Evaluation:

Mutual dependence produces a dependency cycle.

Such cycles prevent identification of foundational concepts.

Result:

Provisionally Supported.

---

# Candidate Property 4

Transitivity.

Question:

If A depends upon B, and B depends upon C, must A depend upon C?

Evaluation:

Some dependency classes appear transitive.

Others may not.

Result:

Undetermined.

Requires investigation for each dependency class independently.

---

# Candidate Property 5

Acyclicity.

Question:

Can a valid dependency graph contain cycles?

Evaluation:

Cycles eliminate the possibility of identifying primitive concepts.

The primitive identification methodology therefore favors acyclic dependency structures.

Result:

Supported.

---

# Pattern Analysis

Current evidence suggests valid dependency relations possess the following properties:

- directionality;
- irreflexivity;
- acyclicity.

Transitivity and antisymmetry require further investigation.

---

# Candidate Mathematical Structure

The dependency graph may constitute a directed acyclic graph.

Whether it additionally satisfies the properties of a partial order remains unresolved.

---

# Consequences

If dependency relations satisfy these properties:

- primitive concepts correspond to source nodes;
- derivable concepts correspond to reachable nodes;
- reconstruction follows graph traversal;
- dependency cycles identify theoretical defects.

---

# Decision Criteria

A dependency relation is acceptable only if it satisfies the required structural properties established by investigation.

---

# Provisional Conclusion

Current evidence supports treating dependency as a directed acyclic relation.

Additional investigations are required before stronger mathematical properties are accepted.

---

# Remaining Questions

Future investigations should determine:

- whether dependency forms a partial order;
- whether different dependency classes possess different algebraic properties;
- whether dependency composition admits formal theorems;
- whether dependency graphs possess canonical minimal forms.

---

# Current Status

The investigation remains active.

The mathematical structure of dependency remains under investigation.