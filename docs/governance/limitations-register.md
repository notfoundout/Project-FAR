# Limitations Register

Status: **Accepted governance register**

| ID | Limitation | Scope | Status |
|---|---|---|---|
| LIM-001 | SWE-agent v2 covers one task, two repetitions per release, and four budget-limited runs. | Empirical | Open; prohibits population claims. |
| LIM-002 | Equal observed 0/2 counts do not demonstrate equivalence. | Statistical | Open; requires an equivalence design. |
| LIM-003 | Source artifact availability is external to Git. | Reproducibility | Open; committed lock remains verifiable. |
| LIM-004 | SWE-ReX revisions are not verifiable in frozen trajectories. | Provenance | Historically unfixable. |
| LIM-005 | Hosted runner, action tags, package services and model endpoint are external/mutable trust dependencies. | Supply chain | Historically unfixable for v2. |
| LIM-006 | Sequential runs are isolated but not demonstrated statistically independent. | Experimental design | Open. |
| LIM-007 | End-to-end UPP composition is not one kernel-checked proof object. | Proof assurance | Open. |
| LIM-008 | Universality and maximality are relative to frozen premises and registered challenges. | Theory | Bounded only. |
| LIM-009 | Framework stability labels do not establish universal correctness, necessity or superiority. | Repository semantics | Enforced claim boundary. |

New limitations require an evidence citation and may be closed only by a recorded execution, not by wording changes.
