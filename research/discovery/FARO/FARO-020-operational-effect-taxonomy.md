# FARO Discovery Investigation

## Identifier

FARO-020

---

# Title

Operational Effect Taxonomy

---

## Status

In Progress

---

# Purpose

Classify the possible effects produced by reasoning operations.

The objective is to determine whether operational effects form a coherent taxonomy.

---

# Dependencies

- FARO-001 through FARO-019

---

# Central Question

What kinds of effects can a reasoning operation produce?

---

# Candidate Effect 1

State-transforming effect.

Description:

An operation changes the reasoning state.

Examples:

- adding a representation;
- removing a representation;
- revising an interpretation;
- changing admissibility status.

Status:

Supported.

---

# Candidate Effect 2

State-preserving effect.

Description:

An operation executes without changing the reasoning state.

Examples:

- consistency check;
- verification;
- inspection;
- replay.

Status:

Supported.

---

# Candidate Effect 3

Branch-generating effect.

Description:

An operation produces multiple admissible successor paths.

Examples:

- alternative hypotheses;
- competing derivations;
- scenario analysis.

Status:

Supported.

---

# Candidate Effect 4

Branch-pruning effect.

Description:

An operation removes or rejects one or more possible paths.

Examples:

- contradiction detection;
- inadmissibility classification;
- failed proof attempt.

Status:

Supported.

---

# Candidate Effect 5

Resolution-producing effect.

Description:

An operation produces a resolution for the investigation.

Examples:

- selecting a final candidate;
- accepting a proof;
- choosing a best explanation.

Status:

Supported.

---

# Candidate Effect 6

Termination-triggering effect.

Description:

An operation causes an investigation or reasoning path to terminate.

Examples:

- sufficient resolution reached;
- contradiction irrecoverable;
- resource limit reached.

Status:

Supported.

---

# Pattern Analysis

Operational effects appear to divide into six provisional classes:

1. transformation;
2. preservation;
3. branching;
4. pruning;
5. resolution production;
6. termination.

These classes describe what operations do to reasoning states, paths, and investigations.

---

# Observation

A single operation may produce more than one effect.

For example, contradiction detection may:

- preserve the current state;
- prune a branch;
- trigger termination.

Therefore, effect classes are not necessarily mutually exclusive.

---

# Provisional Conclusion

Reasoning operations produce classifiable effects.

State transition is only one operational effect among several.

FARO should therefore define operations and their possible effects rather than reducing operation to state transition alone.

---

# Remaining Questions

Future investigations should determine:

- whether this taxonomy is complete;
- whether effect classes can be reduced;
- whether effects require formal typing;
- whether effects obey invariants.

---

# Current Status

The operational effect taxonomy remains provisional.