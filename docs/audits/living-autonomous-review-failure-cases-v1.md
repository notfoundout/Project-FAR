# Living Autonomous Review — fail-closed cases

The autonomous review path must stop without granting scientific authority when any of the following occurs:

- the permanent living-research PR is missing, closed, not draft, retargeted, or no longer bound to `automation/living-research-inbox`;
- protected `main` advances after the review base is frozen;
- the exact candidate bytes change during review;
- the candidate lacks a usable primary-source URL or exact FAR-CORE claim binding;
- URL-context retrieval does not verify the primary source;
- generated claim IDs fall outside the candidate's governed claim set;
- screening, attack, replication, and adjudication disagree in a way the deterministic contract cannot reconcile;
- `PROJECT_CHANGE_REQUIRED` is proposed without premise match, scope match, a reproducible attack, internal replication, or nonempty scientific operations;
- a generated target is outside the existing promotion or implementation write surface;
- a generated payload does not match its declared hash or current-main preimage;
- a generated review, proposal, or authorization collides with an existing protected identifier;
- an autonomous-review PR is already open and awaiting human disposition;
- downstream promotion or implementation validation fails.

A fail-closed event may persist bounded retry/provenance data to the noncanonical living inbox when safe, but it must not change protected scientific status and must not merge any PR.
