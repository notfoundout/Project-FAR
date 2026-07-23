# Refund Authorization Reference Domain v0.1

This reference domain demonstrates FAR decision integrity over an explicit, instrumented refund workflow.

## Policy

Automated approval requires all of the following:

1. the referenced order exists;
2. payment is confirmed;
3. the request is no more than 30 days after purchase;
4. no previous refund exists;
5. the requesting agent has refund authority;
6. the amount is no more than USD 500;
7. the applicable policy is exactly `refund-policy/2026-07`.

## Runtime disposition

- `justified` maps to `allow`;
- `unsupported` maps to `block`;
- `underdetermined` maps to `escalate`;
- `unverifiable` maps to `escalate`.

Missing information is represented as unknown and is never converted into false evidence. An observed failed requirement is represented as explicitly invalid and blocks the proposed action. Materially different compatible outcomes require escalation.

## Claim boundary

The implementation validates disclosed inputs under the frozen reference policy. It does not verify that upstream facts are true, infer hidden agent cognition, or establish legal compliance.
