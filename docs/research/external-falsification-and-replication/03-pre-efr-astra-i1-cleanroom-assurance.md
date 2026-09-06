# Pre-EFR Astra I1 clean-room assurance — 2026-09-06

Status: **Research / pre-EFR assurance evidence**

Record ID: `PRE-EFR-ASTRA-I1-CLEANROOM-2026-09-06`

This record preserves one Project-FAR-controlled clean-room adversarial audit conducted before any EFR-001 execution. It is **I1 claimed isolation**, not I2, not I3, and not an execution of `EXTERNAL-FALSIFICATION-AND-REPLICATION-001`.

The run used the content-addressed clean-room packet with SHA-256 `3b99dfc4f7ef220e518d6984c13d00eb10380024f135e53e1360d504e73821e5`. The packet integrity gate returned `VALID PACKET`. The evaluator reported no access to GitHub, web retrieval, withheld W1/W2 material, Project FAR implementation/proof material, or other unblinded evidence during the run, but technical impossibility of such access was not established. The run is therefore I1 under the accepted isolation doctrine.

## Sealed result

The sealed report was committed before any unblinding and has SHA-256:

`9c354031c7b944e89fdb17db50d03b7cc79f659df21cf50fe16df8f75cc10a1d`

Its preserved verdict distribution is:

| Verdict | Count | Claims |
|---|---:|---|
| `SURVIVES-ATTACK` | 12 | FAR-CORE-001–009, 011–013 |
| `FALSIFIED` | 0 | none |
| `INDETERMINATE` | 2 | FAR-CORE-010, FAR-CORE-014 |

Both indeterminate claims were explicitly recorded as packet defects rather than theorem counterexamples:

- `PD-010-SCOPE`: the supplied FAR-CORE-010 statement combined a fixed-parameter scope clause with a sentence discussing changes to those same parameters.
- `PD-014-MISSING-SCOPE`: the packet named PR #453's bounded representation/decoder classes without supplying enough exact definitions to independently reproduce the PR-specific claim.

The uploaded sealed audit bundle has SHA-256 `eff1a5a815a10ba73aa41b130a300702ac37dfce48fbcf9da7a019bcffacc2c9`. Its content-addressed evidence is indexed under [`pre-efr-astra-i1-2026-09-06/`](pre-efr-astra-i1-2026-09-06/). The source packet and sealed bundle are not promoted into EFR inputs by repository inclusion; their hashes are retained for provenance.

## Post-seal adjudication

The sealed result is not rewritten. A later canonical-source adjudication resolved only the two packet defects:

- **FAR-CORE-010 — `SURVIVES-ADJUDICATION`.** Current v1.1 governance states that exact common theory `T_{L,J,I}` depends on `L`, interpreted profiles/models `J`, and target class/index `I`; the frame-subtracted residue additionally depends on `Γ`; changing `Γ` alone with `L,J,I` and interpreted models fixed cannot change exact `T`. The clean-room finding therefore identified malformed packet wording, not a surviving contradiction.
- **FAR-CORE-014 — `SURVIVES-ADJUDICATION`.** The historical PR #453 research record supplies the missing bounded state/transition/decoder definitions: the rule-induced projected individual-sequent relation, four uniform monotone successor-set decoders, finite MLL witnesses, resource-labelled hyperedges, and frontier-multiset construction. W2 separately records the bounded SSS/MLL witness bridge as formalized. The clean-room indeterminacy therefore arose from missing packet inputs, not a surviving contradiction.

The post-seal adjudication artifacts are preserved as [`post-seal-adjudication.md`](pre-efr-astra-i1-2026-09-06/post-seal-adjudication.md) and [`post-seal-adjudication.json`](pre-efr-astra-i1-2026-09-06/post-seal-adjudication.json).

## Exact combined disposition

For theorem-defect triage only:

- 14/14 governed claims: **no surviving contradiction identified** after post-seal adjudication;
- 0/14 governed claims: falsified;
- 12/14 governed claims: reproduced within the sealed I1 run;
- 2/14 governed claims: resolved only by later canonical-source adjudication.

This evidence **must not** be restated as "14/14 independently reproduced in one clean-room run." It does not upgrade W1 isolation, establish I2 or I3, execute or satisfy EFR-R1, establish novelty/priority, or supply external/human/site/cost evidence. EFR-001 remains preregistered and unexecuted.

## Rerun rule

No rerun is required merely to determine whether this assurance exercise exposed a surviving contradiction in the governing core theory. A new clean-room run is required only if a future evidence claim specifically requires one clean-room evaluation to independently reproduce all 14 claims from a complete statement-only packet.

## Evidence integrity

The evidence index records the original packet, sealed report, uploaded bundle, uploaded verdict ledger, and post-seal adjudication hashes. Repository inclusion records provenance only. It does not promote this Research evidence into EFR execution or external validation.
