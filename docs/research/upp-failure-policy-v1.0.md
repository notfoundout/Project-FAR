# Universal Proof Failure Policy

A proof failure is evidence about the theorem, not permission to change the standard until RCCD passes.

For every failed obligation, the responsible workstream must select one or more of the following dispositions:

1. correct an implementation defect without changing the frozen semantics;
2. expose and justify a previously implicit assumption;
3. weaken the theorem and record the exact lost scope;
4. revise or extend RCCD;
5. accept a counterexample and classify universality as defeated;
6. classify the result as blocked by an indispensable unproved assumption.

The following responses are prohibited:

- adding supportive examples as a substitute for the failed derivation;
- redefining the target class using the failed RCCD property;
- moving required structure into an uncharged decoder, scheduler, codebook, oracle, history, or interpretation map;
- treating an automated search timeout as proof of nonexistence;
- treating successful compilation as proof of a theorem not represented in the proof object;
- silently narrowing a universal quantifier;
- changing terminal outcomes after seeing the result without superseding the protocol.
