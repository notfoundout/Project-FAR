"""Frozen crossed case/reviewer HD1 numerical gates; no study data bundled."""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
import random
import sys

try:
    from .efr_hd1_allocation import allocate, ARMS, CLASSES, DOMAINS
except ImportError:  # Direct CLI execution.
    from efr_hd1_allocation import allocate, ARMS, CLASSES, DOMAINS


def prepare(manifest_bytes, manifest_sha256, ratings_bytes, ratings_sha256):
    allocation = allocate(manifest_bytes, manifest_sha256)
    if hashlib.sha256(ratings_bytes).hexdigest() != ratings_sha256:
        raise ValueError("sealed ratings digest mismatch")
    data = json.loads(manifest_bytes)
    outputs = json.loads(ratings_bytes)
    if outputs.get("input_manifest_sha256") != manifest_sha256:
        raise ValueError("ratings refer to another input manifest")
    expected = {(row['reviewer_id'], case, arm)
                for row in allocation['allocation'] for arm in ARMS
                for case in row['tasks'][arm]}
    answers = {}
    for row in outputs['ratings']:
        key = row['reviewer_id'], row['case_id'], row['arm']
        if key not in expected or key in answers:
            raise ValueError("duplicate or unallocated rating")
        if row['decision'] not in (None, 'preservation', 'material_loss'):
            raise ValueError("invalid decision")
        answers[key] = row['decision']
    if set(answers) != expected:
        raise ValueError("every allocated rating requires a row, including missing decisions")
    groups = {}
    for case in data['cases']:
        for arm in ARMS:
            rows = sorted((r, answer) for (r, c, a), answer in answers.items()
                          if c == case['id'] and a == arm)
            pairs = [(r, s, int((a != b) if a is not None and b is not None else arm == 'far'))
                     for (r, a), (s, b) in combinations(rows, 2)]
            loss = []
            if case['class'] == 'material_loss':
                loss = [(r, int(answer == 'preservation' if answer is not None else arm == 'far'))
                        for r, answer in rows]
            groups[case['id'], arm] = pairs, loss
    missing = {arm: sum(answer is None for (_, _, a), answer in answers.items() if a == arm)
               for arm in ARMS}
    return data, groups, missing


def endpoints(groups, case_weights, reviewer_weights):
    disagreement, false_accept = {}, {}
    for arm in ARMS:
        pair_num = pair_den = loss_num = loss_den = 0
        for case, count in case_weights.items():
            pairs, losses = groups[case, arm]
            for r, s, disagrees in pairs:
                weight = count * reviewer_weights[r] * reviewer_weights[s]
                pair_num += weight * disagrees
                pair_den += weight
            for r, wrong in losses:
                weight = count * reviewer_weights[r]
                loss_num += weight * wrong
                loss_den += weight
        if not pair_den or not loss_den:
            raise ValueError("unestimable crossed resample; no redraw is permitted")
        disagreement[arm] = Fraction(pair_num, pair_den)
        false_accept[arm] = Fraction(loss_num, loss_den)
    return (disagreement['standard'] - disagreement['far'],
            false_accept['far'] - false_accept['standard'])


def analyze(manifest_bytes, manifest_sha256, ratings_bytes, ratings_sha256):
    data, groups, missing = prepare(manifest_bytes, manifest_sha256, ratings_bytes, ratings_sha256)
    result = {'input_manifest_sha256': manifest_sha256, 'ratings_sha256': ratings_sha256,
              'missing': missing, 'full_protocol_validity_still_required': True}
    if (Fraction(sum(missing.values()), 1440) > Fraction(1, 20)
            or Fraction(abs(missing['far'] - missing['standard']), 720) > Fraction(1, 50)):
        return dict(result, numerical_disposition='INVALID_MISSINGNESS')
    reviewers = sorted(data['reviewers'])
    strata = [sorted(c['id'] for c in data['cases'] if c['domain'] == d and c['class'] == label)
              for d in DOMAINS for label in CLASSES]
    observed = endpoints(groups, {c['id']: 1 for c in data['cases']}, {r: 1 for r in reviewers})
    rng = random.Random(int(manifest_sha256[:16], 16))
    reductions, safety = [], []
    for resample in range(10000):
        cases = Counter()
        for stratum in strata:
            for draw in range(10):
                cases[stratum[rng.randrange(10)]] += 1
        workers = Counter(reviewers[rng.randrange(24)] for draw in range(24))
        try:
            reduction, harm = endpoints(groups, cases, workers)
        except ValueError:
            return dict(result, numerical_disposition='INVALID_UNESTIMABLE_RESAMPLE',
                        invalid_resample_index=resample)
        reductions.append(reduction)
        safety.append(harm)
    reductions.sort()
    safety.sort()
    bounds = [reductions[249], reductions[9749], safety[249], safety[9749]]
    passed = observed[0] >= Fraction(1, 10) and bounds[0] > 0 and bounds[3] <= Fraction(1, 50)
    return dict(result, numerical_disposition='NUMERICAL_GATES_PASS' if passed else 'NUMERICAL_GATES_FAIL',
                observed=[str(x) for x in observed], percentile_bounds=[str(x) for x in bounds],
                resamples=10000, interval='nominal crossed case/reviewer perturbation; no exact coverage claim')


def main():
    if sys.version_info[:2] != (3, 12) or len(sys.argv) != 5:
        raise SystemExit('Python 3.12 required: efr_hd1_analysis.py INPUT INPUT_SHA256 RATINGS RATINGS_SHA256')
    result = analyze(Path(sys.argv[1]).read_bytes(), sys.argv[2], Path(sys.argv[3]).read_bytes(), sys.argv[4])
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
