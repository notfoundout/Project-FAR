# Living Autonomous Review v1

Status: proposed Research automation; no scientific authority until human merge.

## Objective

Close the gap between unattended discovery and protected promotion without granting automation merge authority. The system may discover, screen, attack, internally replicate, adjudicate, prepare exact correction payloads, and open reviewable PRs. A human remains the sole merge decision for every autonomous-review PR and every downstream promotion or implementation PR.

## Pipeline

`PR #490 candidate -> primary-source verification -> exact FAR claim binding -> screening -> adversarial attack -> separate internal replication -> adjudication -> bounded proposal generation -> exact-byte authorization package -> human-review PR`

After the review PR is merged, the existing scheduled Living Research Promotion and Living Research Implementation workflows remain responsible for constructing the downstream repository-change PRs.

## Authority boundary

- PR #490 remains Research-only and permanently noncanonical.
- Model outputs are untrusted Research proposals.
- A generated disposition, review row, proposal, or authorization has no protected authority before its review PR merges into `main`.
- Automation never merges the autonomous-review PR.
- Automation never merges downstream promotion or implementation PRs.
- Screening, attack, replication, and adjudication calls are internal same-provider checks; they do not count as external independence, external replication, or final external review.
- If primary-source verification fails, the candidate remains pending and only a retry record is persisted.
- If protected `main` or the exact candidate bytes move during review, publication fails closed.

## Project-change threshold

`PROJECT_CHANGE_REQUIRED` is eligible only when the model-backed package establishes all configured gates: verified primary source, exact FAR claim binding, premise match, scope match, reproducible attack, separate internal replication, matching claim identity, and at least one bounded scientific operation. Implementation changes require a separately declared implementation proposal and exact authorization.

## Human responsibility

The repository owner reviews and merges or rejects the generated PR. Human merge is the only operation that grants the generated review/authorization bytes protected status. This is intentionally the stopping point for automation.
