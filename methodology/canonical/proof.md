# Canonical Proof Standard (CPS)

## Purpose

This document defines the requirements for accepting any proposition, construction, theorem, or formal object within Project FAR.

No result becomes canonical until it satisfies the Canonical Proof Standard.

---

## Acceptance Requirements

Every accepted result shall satisfy all of the following.

### 1. Explicit Statement

The proposition shall be stated unambiguously.

---

### 2. Accepted Dependencies

Every dependency shall already be accepted.

No future result may be cited.

---

### 3. Explicit Derivation

Every derivation step shall be explicit.

No implicit inference is permitted.

---

### 4. Non-Circularity

No step may depend directly or indirectly upon the proposition being proved.

---

### 5. Hidden Assumption Audit

Every assumption shall be explicitly identified.

Every assumption shall either:

- already be accepted;
- or become a new investigation.

---

### 6. Counterexample Audit

Attempt to construct a counterexample.

Failure to identify a counterexample does not constitute proof,

but successful counterexamples invalidate the proof.

---

### 7. Reconstruction Audit

An independent investigator using only accepted dependencies shall be capable of reproducing the proof.

---

### 8. Dependency Verification

Every dependency shall appear in the canonical dependency graph.

---

### 9. Reduction Audit

Attempt to remove every step.

If removal preserves validity,

that step shall be removed.

---

### 10. Final Verification

The proof shall survive:

- logical audit;
- dependency audit;
- reconstruction audit;
- falsification audit.

Only then may the proposition become canonical.

