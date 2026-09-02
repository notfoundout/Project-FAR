# PCA-W6 Literature Basis and Design Rationale

Status: **Research support for frozen protocol**

Protocol freeze commit: `3813b9e3eb49562bd8b9f4d3179c3d9536831de6`

## Purpose

W6 tests one narrow operational proposition: whether an explicit semantic audit detects a registered material representational collision that a shape-only conformance check does not detect. The literature is used to motivate careful task-specific evaluation and to bound interpretation. It is not imported as evidence that Project FAR itself is useful.

## Relevant evidence

Structured review aids can improve error detection, but effects are task- and design-dependent rather than uniformly positive.

- Al-Khafaji et al. (2022), a systematic review of diagnostic checklists, found mixed effects across evaluated checklists: some studies improved diagnostic outcomes, some did not, and one was mixed. Task-oriented checklist components more often coincided with error reduction than broad cognitive prompts. DOI: `10.1136/bmjopen-2021-058219`.
- Stevenson et al. (2022) evaluated a structured medico-legal report audit tool and reported higher sensitivity for error detection than usual practice, while also finding category-dependent disagreement. DOI: `10.1016/j.jflm.2022.102359`.
- White et al. (2010) found that explicit, specific checklist instructions could materially change detection rates in a controlled medication-error simulation, while detection remained error-type dependent. DOI: `10.1136/qshc.2009.032862`.
- Kämmer et al. (2021) found that a differential-diagnosis checklist improved accuracy when the correct diagnosis was represented but did not improve and could slightly worsen performance when it was absent, demonstrating that structured aids can fail when their represented option space is wrong. DOI: `10.1111/medu.14596`.
- Gonçalves et al. (2020) preregistered an experiment comparing no guidance, a checklist, and a checklist-based strategy for professional code review, reflecting the same methodological need to compare explicit review procedures against a defined baseline rather than assume effectiveness from face validity. DOI: `10.1145/3379597.3387509`.

## Design consequences

The W6 protocol therefore uses the following constraints:

1. **Specific registered failure, not a generic checklist claim.** The injected defect is exactly a representation collision across cases with different required behavior.
2. **Negative controls.** The six unmodified repaired records must remain unflagged by the semantic audit.
3. **Positive controls.** Six deterministic mutants and the six already-frozen W4 lossy records are checked.
4. **Independent oracle.** A second implementation computes the collision property from the contract tables without calling the FAR semantic verifier or reading report labels.
5. **No population inference.** The corpus is finite and project-authored. Exact counts are reported rather than statistical generalization.
6. **No human-utility substitution.** Machine agreement, CI success, or artifact error detection is not treated as evidence that human disagreement falls or real-world decisions improve.

## Tool record

Literature discovery used Consensus, SciSpace, and Scite. Scite was also used to verify DOI-level bibliographic identity for the key checklist and code-review records. A Wolfram context request intended only as a descriptive-analysis sanity check returned an upstream `502`; no W6 inference depends on Wolfram output, and the failed invocation is retained here rather than silently represented as success.

The canonical bibliographic identities used by this workstream are recorded in `references.bib`.
