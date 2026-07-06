# Failure and Downgrade Conditions

## Purpose

This document defines when a Project FAR theorem, proposition, lemma, or derived concept must be rejected, downgraded, or deprecated.

---

# Immediate Rejection Conditions

A proposed theorem must be rejected if any of the following hold:

1. It has no stated scope.
2. It uses undefined technical terms.
3. It depends on an unregistered derived concept.
4. It uses notation contrary to the canonical notation without declaring an override.
5. It directly depends on itself.
6. Its proof does not establish its statement.
7. It contradicts an established theorem without declaring itself revisionary.

---

# Downgrade Conditions

An Established theorem must be downgraded if any of the following are discovered:

1. Missing dependency.
2. Circular dependency.
3. Overbroad scope.
4. Invalid inference step.
5. Unregistered technical concept used essentially.
6. Conflict with canonical notation.
7. Stronger theorem replaces it and changes its role.
8. Underlying definition is revised.
9. Supporting axiom is revised or removed.
10. Falsification test succeeds against the theorem's stated scope.

---

# Downgrade Targets

## Established to Verified

Use when the theorem is probably correct but needs catalog, audit, dependency, or notation repair.

## Established to Proposed

Use when the theorem has a plausible statement but its proof no longer satisfies verification requirements.

## Established to Draft

Use when the theorem requires major rewriting.

## Established to Deprecated

Use when the theorem should no longer be used as a canonical dependency.

---

# Required Downgrade Record

Every downgrade must record:

```text
Theorem:
Old status:
New status:
Date:
Failed condition:
Reason:
Required repair:
Affected downstream dependencies:
```

---

# Restoration Rule

A downgraded theorem may be restored only after:

1. the failed condition is repaired;
2. the proof verification checklist is rerun;
3. the dependency graph is updated;
4. the circularity audit is updated;
5. the theorem catalog records the restored status.

---

# Falsification Rule

If a falsification test succeeds within a theorem's stated scope, the theorem must be downgraded or revised.

If the test succeeds only outside the theorem's stated scope, the theorem may remain Established but its limitations must be clarified.
