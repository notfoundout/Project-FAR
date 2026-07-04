# FARE Mathematics Notation

## Purpose

This document records the standard notation used within the FARE mathematics layer.

Notation is descriptive only.

It does not introduce mathematical objects, assumptions, axioms, or theorems.

---

# General Rule

Mathematical notation in Markdown documents should use inline code notation rather than display mathematics.

Examples:

- `E`
- `E_1`
- `tau: E_1 -> E_2`
- `P = (tau_1, tau_2, ..., tau_n)`
- `d(E_1, E_2)`

---

# Standard Symbols

| Symbol | Meaning |
|---|---|
| `E` | An evaluation, or an evaluation space when explicitly stated by context. |
| `E_1`, `E_2`, `E_3` | Evaluations in a common evaluation space. |
| `tau` | An evaluation transformation. |
| `tau: E_1 -> E_2` | A transformation from evaluation `E_1` to evaluation `E_2`. |
| `id_E` | Identity transformation on `E`. |
| `P` | An evaluation path. |
| `P = (tau_1, tau_2, ..., tau_n)` | A path consisting of transformations `tau_1` through `tau_n`. |
| `Cost(tau)` | The cost assigned to transformation `tau`. |
| `Cost(P)` | The cost assigned to path `P`. |
| `d(E_1, E_2)` | Evaluation distance from `E_1` to `E_2`. |
| `infinity` | The distance assigned when no admissible path exists. |
| `N(E)` | A neighborhood system centered at `E`. |
| `U` | A neighborhood within a neighborhood system. |
| `S` | A sequence of evaluations, when used in convergence or limit contexts. |
| `Lim(S)` | The limit set of sequence `S`. |
| `E_hat` | A completed or extended evaluation space. |
| `i: E -> E_hat` | Inclusion map from `E` into `E_hat`. |
| `I` | An evaluation invariant. |

---

# Notes

Where notation is ambiguous, the local definition in the relevant document governs.

Notation shall not be used to smuggle in assumptions not present in the definitions.
