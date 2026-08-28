#!/usr/bin/env python3
"""Independent finite checks for PCA-W1 Stage A.

No Project FAR code or fixtures are imported.  This exhaustively checks small
set-theoretic instances of factorization, quotient coarseness, incompatible
contract minima, and deterministic transition descent.
"""

from itertools import product


def functions(n, m):
    return list(product(range(m), repeat=n))


def kernel(f):
    return {(i, j) for i in range(len(f)) for j in range(len(f)) if f[i] == f[j]}


def factors_on_image(beta, rep):
    table = {}
    for x, rx in enumerate(rep):
        if rx in table and table[rx] != beta[x]:
            return False
        table[rx] = beta[x]
    return True


def factorization_checks():
    checked = 0
    for n in range(0, 5):
        for b_size in range(1, 4):
            for r_size in range(1, 4):
                for beta in functions(n, b_size):
                    for rep in functions(n, r_size):
                        checked += 1
                        lhs = factors_on_image(beta, rep)
                        rhs = kernel(rep) <= kernel(beta)
                        assert lhs == rhs
    return checked


def quotient_checks():
    checked = 0
    for n in range(0, 5):
        for b_size in range(1, 4):
            for beta in functions(n, b_size):
                q = beta  # same kernel as the canonical quotient
                assert factors_on_image(beta, q)
                for r_size in range(1, 4):
                    for rep in functions(n, r_size):
                        checked += 1
                        if factors_on_image(beta, rep):
                            # q must factor through every sufficient rep.
                            assert factors_on_image(q, rep)
                            assert kernel(rep) <= kernel(q)
    return checked


def incompatible_minima_checks():
    witnesses = []
    for n in range(2, 6):
        beta_constant = tuple(0 for _ in range(n))
        beta_injective = tuple(range(n))
        assert kernel(beta_constant) != kernel(beta_injective)
        witnesses.append((n, len(kernel(beta_constant)), len(kernel(beta_injective))))
    return witnesses


def descends(rep, transition):
    induced = {}
    for x, rx in enumerate(rep):
        target = rep[transition[x]]
        if rx in induced and induced[rx] != target:
            return False
        induced[rx] = target
    return True


def transition_checks():
    checked = 0
    for n in range(1, 5):
        for r_size in range(1, 4):
            for rep in functions(n, r_size):
                for transition in functions(n, n):
                    checked += 1
                    stable = all(
                        rep[x] != rep[y]
                        or rep[transition[x]] == rep[transition[y]]
                        for x in range(n)
                        for y in range(n)
                    )
                    assert descends(rep, transition) == stable
    return checked


if __name__ == "__main__":
    print("factorization instances:", factorization_checks())
    print("quotient comparison instances:", quotient_checks())
    print("constant/injective witnesses (n, |ker const|, |ker inj|):", incompatible_minima_checks())
    print("transition descent instances:", transition_checks())
    print("result: all represented finite checks passed")
