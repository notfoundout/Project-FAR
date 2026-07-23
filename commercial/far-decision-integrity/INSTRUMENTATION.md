# FAR instrumentation SDK

The instrumentation API records explicit application commitments and emits flat OpenInference-compatible spans accepted by `far-trace-ingest`.

```python
from far_decision_integrity.instrumentation import DecisionSession

with DecisionSession(
    "refund-1042",
    "issue_refund",
    "refund-policy/2026-07",
    "approve",
    {"kind": "financial_action", "amount": 100},
) as decision:
    decision.record_evidence(
        "payment",
        "Payment confirmed.",
        supports="approve",
        authorization_required=True,
    )
    decision.record_rule(
        "policy",
        "Refund policy authorizes the action.",
        supports="approve",
        relation="authorizes",
        authorization_required=True,
    )
    decision.record_conclusion("approve", "Approve refund.")

trace = decision.trace
```

`finish(claim_complete=True)` validates the graph, rejects unresolved unknowns, emits the trace, and immediately round-trips it through the FAR ingestion contract. The SDK does not infer facts, dependencies, authorization, or hidden reasoning. Applications must record those commitments explicitly.
