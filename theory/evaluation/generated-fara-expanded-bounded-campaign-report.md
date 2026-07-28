# Expanded bounded FARA executable campaign

Status: Research

Base: `b05e48f204e273938ef406168b83cafc0958f9a0`. Maximum carrier size: **4**.

## Explicit bounds and cost
- arity 1: 31 interpretations; per carrier [{'carrier_size': 0, 'interpretations': 1}, {'carrier_size': 1, 'interpretations': 2}, {'carrier_size': 2, 'interpretations': 4}, {'carrier_size': 3, 'interpretations': 8}, {'carrier_size': 4, 'interpretations': 16}]
- arity 2: 66067 interpretations; per carrier [{'carrier_size': 0, 'interpretations': 1}, {'carrier_size': 1, 'interpretations': 2}, {'carrier_size': 2, 'interpretations': 16}, {'carrier_size': 3, 'interpretations': 512}, {'carrier_size': 4, 'interpretations': 65536}]
- paired reduct models: 70
- foundation executions: 57
- ablation executions: 336
- round-trip records: 12

## Changed conclusions
- **derivability:** all seven targets remain non-derivable within the explicitly enumerated axes and paired-reduct search only
- **ablations:** 21 executable ablations reproduced; inference remains bounded
- **translations:** 57 translation/reconstruction traces reproduced
- **round_trips:** 12 bounded round-trip records reproduced
- **preservation:** six-dimensional bounded preservation matrix reproduced; failures and partial results retained
- **pareto:** multiple foundations remain Pareto-incomparable
- **core:** multiple non-equivalent coherent formalizations remain
- **external_cases:** {'oracle': 'Unknown', 'continuous': 'Unknown', 'hybrid': 'Unknown', 'embodied': 'Unknown'}

## Boundary
Oracle, continuous, hybrid, and embodied cases remain Unknown. Results are confined to the declared finite axes.

## Nonclaims
- no universality claim
- no uniqueness claim
- no global superiority claim
- no global minimality claim
- no necessity claim
- no completeness claim
- no inference beyond the explicit finite bounds
- no independent-replication claim
