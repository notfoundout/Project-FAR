"""Independent spec-derived reference oracle for far-ir/2.1 (PCA-W5).

Derived ONLY from:
  docs/specification/far-ir-2.1-approximation-cost.md   (cited as S21 §...)
  docs/specification/far-ir-2.0-contract.md             (cited as S20 §...)
  schemas/far-contract-v2.1.schema.json                  (cited as SCHEMA)
  docs/research/pca-w5-approximation-and-cost/*.md       (cited as PROTO / RESULTS)
No project implementation code was read. Every point where the spec is silent is
an explicit, switchable interpretation in `Interp` so the ambiguity is visible and
machine-checkable rather than silently decided.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import pathlib
import re
import sys
from dataclasses import dataclass, field
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[3]
# The repository root contains a local `jsonschema/` shim (project code). Independence
# requires upstream jsonschema: drop repo-root/cwd entries before importing and assert.
sys.path[:] = [p for p in sys.path if p not in ("", ".") and pathlib.Path(p).resolve() != ROOT]
import jsonschema  # noqa: E402

if ROOT in pathlib.Path(jsonschema.__file__).resolve().parents:
    raise SystemExit(f"refusing repository-local jsonschema at {jsonschema.__file__}")

SCHEMA = json.loads((ROOT / "schemas/far-contract-v2.1.schema.json").read_text())
_VALIDATOR = jsonschema.Draft202012Validator(SCHEMA)

# SCHEMA $defs.Probability / NonnegativeRational (identical patterns).
_RATIONAL = re.compile(r"^(0|[1-9][0-9]*)(/[1-9][0-9]*)?$")


def rational(text: str) -> Fraction:
    """Parse by hand (NOT Fraction(str), which would also accept '0.5', '-1', ' 1')."""
    if not isinstance(text, str) or not _RATIONAL.fullmatch(text):
        raise ValueError(f"not a schema rational: {text!r}")
    num, _, den = text.partition("/")
    return Fraction(int(num), int(den) if den else 1)


def canon(value) -> str:
    """Canonical JSON identity. Empirically reproduces both fixture freeze hashes
    (sorted keys, compact separators); ensure_ascii is undetermined by the data."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def contract_sha256(contract: dict) -> str:
    return hashlib.sha256(canon(contract).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Interp:
    """Readings for points the spec leaves open. Defaults = most literal reading."""

    # S21 §Metric: "d(l,r) != d(r,l) for a declared pair" / "d(l,r) == 0 for distinct
    # declared values" -- ordered pairs (l != r) or unordered pairs {l, r}?
    pairs: str = "ordered"  # or "unordered"
    # "d(l,r) > d(l,m) + d(m,r) for a declared triple" -- all ordered triples in V^3,
    # or only triples with l != r (degenerate endpoints skipped)?
    triples: str = "ordered_all"  # or "ordered_distinct_endpoints" or "unordered_endpoints"
    # S21 §Cost conclusions: "A least element must be below every feasible candidate."
    # Must a least element itself be feasible?
    least_requires_feasible: bool = True
    # S21 DECODER_UNKNOWN_ACTION "assigns probability to an action outside the set":
    # does an explicit probability "0" on an undeclared action count?
    unknown_action_zero_counts: bool = True
    # S21 DECODER_NOT_PROBABILITY: sum over all row entries, or only declared actions?
    decoder_sum_over_declared_only: bool = False


@dataclass
class Result:
    codes: list = field(default_factory=list)
    detail: dict = field(default_factory=dict)


def _repeats(keys):
    """Yield once per repeated occurrence (2nd, 3rd, ...) -- 'once per offending item'."""
    seen = set()
    for k in keys:
        if k in seen:
            yield k
        seen.add(k)


def _uniq(keys):
    out, seen = [], set()
    for k in keys:
        if k not in seen:
            out.append(k)
            seen.add(k)
    return out


def verify(record, interp: Interp = Interp()) -> Result:
    res = Result()
    codes = res.codes

    # ---- Schema (S21 §Evaluation order: "Schema errors are terminal") ----
    errors = list(_VALIDATOR.iter_errors(record))
    if errors:
        codes.extend(["SCHEMA_CONSTRAINT_VIOLATION"] * len(errors))
        res.detail["schema_errors"] = sorted(
            (("/".join(map(str, e.absolute_path))), e.message[:120]) for e in errors
        )
        return res

    c, rep = record["contract"], record["report"]
    ev = rep["evidence"]

    # ---- Stage 1 (S21 §Evaluation order, Stage 1) ----
    if c["mode"] != "approximate" or ev["kind"] != "approximation_cost":
        codes.append("W5_MODE_EVIDENCE_REQUIRED")
    if ev["kind"] == "approximation_cost" and rep["outcome"] != "PROVED":
        codes.append("CHECKED_EVIDENCE_OUTCOME_MISMATCH")
    fr = record["freeze"]
    if fr["status"] != "FROZEN":
        codes.append("CHECK_REQUIRES_FROZEN_CONTRACT")
    elif fr["contract_sha256"] != contract_sha256(c):
        codes.append("FREEZE_HASH_MISMATCH")
    sd = c["source_domain"]
    if sd["kind"] != "finite_explicit" or sd["status"] != "EXPLICIT":
        codes.append("CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN")
    if c["required_behavior"]["status"] != "EXPLICIT":
        codes.append("CHECK_REQUIRES_EXPLICIT_BEHAVIOR")
    if c["representation"]["status"] != "EXPLICIT":
        codes.append("CHECK_REQUIRES_EXPLICIT_REPRESENTATION")
    case_ids = [x["id"] for x in sd["cases"]]
    codes.extend("DUPLICATE_DOMAIN_CASE" for _ in _repeats(case_ids))
    for tbl in (c["required_behavior"]["table"], c["representation"]["table"]):
        codes.extend("DUPLICATE_CASE_VALUE" for _ in _repeats(r["case_id"] for r in tbl))
    for tbl in (c["required_behavior"]["table"], c["representation"]["table"]):
        if {r["case_id"] for r in tbl} != set(case_ids):
            codes.append("CASE_TABLE_COVERAGE_MISMATCH")
    # Gate 1
    if "approximation" not in c or codes:
        return res

    a = c["approximation"]
    X = _uniq(case_ids)
    beta = {r["case_id"]: r["value"] for r in c["required_behavior"]["table"]}
    repv = {r["case_id"]: r["value"] for r in c["representation"]["table"]}

    # ---- Stage 2: reference ----
    w_rows = a["reference"]["weights"]
    codes.extend("DUPLICATE_REFERENCE_CASE" for _ in _repeats(w["case_id"] for w in w_rows))
    if {w["case_id"] for w in w_rows} != set(X):
        codes.append("REFERENCE_COVERAGE_MISMATCH")
    weights = [rational(w["weight"]) for w in w_rows]
    if any(v < 0 for v in weights) or sum(weights, Fraction(0)) != 1:
        codes.append("REFERENCE_NOT_PROBABILITY")
    mu = {}
    for w in w_rows:
        mu.setdefault(w["case_id"], rational(w["weight"]))

    # ---- Stage 2: metric ----
    m = a["metric"]
    codes.extend("DUPLICATE_METRIC_VALUE" for _ in _repeats(canon(v) for v in m["values"]))
    codes.extend(
        "DUPLICATE_METRIC_ENTRY"
        for _ in _repeats((canon(e["left"]), canon(e["right"])) for e in m["entries"])
    )
    V = _uniq(canon(v) for v in m["values"])
    d = {}
    for e in m["entries"]:
        d.setdefault((canon(e["left"]), canon(e["right"])), rational(e["distance"]))
    if not all((l, r) in d for l in V for r in V):
        codes.append("METRIC_NOT_TOTAL")
        res.detail["metric_axioms"] = "suppressed"
    else:
        codes.extend("METRIC_IDENTITY_FAILURE" for v in V if d[(v, v)] != 0)
        pairs = (
            [(l, r) for l in V for r in V if l != r]
            if interp.pairs == "ordered"
            else list(itertools.combinations(V, 2))
        )
        codes.extend("METRIC_SYMMETRY_FAILURE" for l, r in pairs if d[(l, r)] != d[(r, l)])
        codes.extend("METRIC_SEPARATION_FAILURE" for l, r in pairs if d[(l, r)] == 0)
        tri_fail = [
            (l, mm, r)
            for l, mm, r in itertools.product(V, V, V)
            if d[(l, r)] > d[(l, mm)] + d[(mm, r)]
        ]
        # Independent route: one-step shortest-path relaxation. A pair can be
        # shortened through some midpoint iff it is the endpoint pair of a failing triple.
        relaxed = {
            (l, r) for l in V for r in V if min(d[(l, k)] + d[(k, r)] for k in V) < d[(l, r)]
        }
        assert relaxed == {(l, r) for l, _, r in tri_fail}, "triangle routes disagree"
        if interp.triples == "ordered_distinct_endpoints":
            tri_fail = [t for t in tri_fail if t[0] != t[2]]
        elif interp.triples == "unordered_endpoints":
            tri_fail = _uniq((frozenset((t[0], t[2])), t[1]) for t in tri_fail)
        codes.extend("METRIC_TRIANGLE_FAILURE" for _ in tri_fail)
        res.detail["triangle_failures"] = len(tri_fail)

    # ---- Stage 2: loss ----
    lo = a["loss"]
    codes.extend("DUPLICATE_LOSS_ACTION" for _ in _repeats(canon(x) for x in lo["actions"]))
    codes.extend(
        "DUPLICATE_LOSS_ENTRY"
        for _ in _repeats((canon(e["truth"]), canon(e["action"])) for e in lo["entries"])
    )
    A = _uniq(canon(x) for x in lo["actions"])
    R = _uniq(canon(beta[x]) for x in X)  # behavior range = image of beta
    loss = {}
    for e in lo["entries"]:
        loss.setdefault((canon(e["truth"]), canon(e["action"])), rational(e["loss"]))
    required = [(t, act) for t in R for act in A]
    if set(loss) != set(required):
        codes.append("LOSS_NOT_TOTAL")
    for pair in required:
        if pair not in d:
            codes.append("METRIC_LOSS_DOMAIN_MISMATCH")
        elif pair in loss and loss[pair] != d[pair]:
            codes.append("LOSS_METRIC_MISMATCH")

    # ---- Stage 2: cost dimensions ----
    dims = [x["id"] for x in a["cost_preorder"]["dimensions"]]
    codes.extend("DUPLICATE_COST_DIMENSION" for _ in _repeats(dims))
    # Gate 2
    if codes:
        return res

    # ---- Stage 3: candidates, in declared order ----
    used_reps = set(canon(repv[x]) for x in X)
    Aset = set(A)
    seen, admitted = set(), []
    for cand in ev["candidates"]:
        if cand["id"] in seen:
            codes.append("DUPLICATE_CANDIDATE")  # later candidate skipped entirely
            continue
        seen.add(cand["id"])
        codes.extend("DUPLICATE_CANDIDATE_COST" for _ in _repeats(k["dimension_id"] for k in cand["costs"]))
        if {k["dimension_id"] for k in cand["costs"]} != set(dims):
            codes.append("COST_COVERAGE_MISMATCH")
        reps_seen = set()
        for row in cand["decoder_table"]:
            rv = canon(row["representation_value"])
            if rv in reps_seen:
                codes.append("DUPLICATE_DECODER_ENTRY")
            reps_seen.add(rv)
            acts = [canon(x["action"]) for x in row["distribution"]]
            codes.extend("DUPLICATE_DECODER_ACTION" for _ in _repeats(acts))
            for x in row["distribution"]:
                if canon(x["action"]) not in Aset and (
                    interp.unknown_action_zero_counts or rational(x["probability"]) != 0
                ):
                    codes.append("DECODER_UNKNOWN_ACTION")
            ps = [
                rational(x["probability"])
                for x in row["distribution"]
                if not interp.decoder_sum_over_declared_only or canon(x["action"]) in Aset
            ]
            if any(p < 0 for p in ps) or sum(ps, Fraction(0)) != 1:
                codes.append("DECODER_NOT_PROBABILITY")
        if reps_seen != used_reps:
            codes.append("DECODER_COVERAGE_MISMATCH")
        if not codes:  # Gate 3 (shared, never-cleared sequence)
            admitted.append(cand)
    # Gate 4
    if codes:
        res.detail["admitted_before_gate4"] = [x["id"] for x in admitted]
        return res

    # ---- Frontier recomputation ----
    tol = rational(a["tolerance"])
    agg = a["aggregation"]
    per = {}
    for cand in admitted:
        # S21: L_d(x) sums over the declared action set. An undeclared action can only
        # reach here with probability 0 (under unknown_action_zero_counts=False).
        dec = {
            canon(row["representation_value"]): {
                canon(x["action"]): rational(x["probability"])
                for x in row["distribution"]
                if canon(x["action"]) in Aset
            }
            for row in cand["decoder_table"]
        }
        L = {
            x: sum(
                (p * loss[(canon(beta[x]), act)] for act, p in dec[canon(repv[x])].items()),
                Fraction(0),
            )
            for x in X
        }
        if agg == "expected":
            value = sum((mu[x] * L[x] for x in X), Fraction(0))
            # Independent route: group by representation value, then by action.
            alt = Fraction(0)
            for rv, dist in dec.items():
                for act, p in dist.items():
                    alt += p * sum(
                        (mu[x] * loss[(canon(beta[x]), act)] for x in X if canon(repv[x]) == rv),
                        Fraction(0),
                    )
            assert alt == value, "expected-loss routes disagree"
            support = [x for x in X if mu[x] > 0]
        else:
            value = max(L.values())
            assert value == sorted(L.values())[-1]
            support = list(X)
        exact = all(L[x] == 0 for x in support)
        # Independent route via separation: zero loss <=> all mass on beta(x).
        exact_alt = all(dec[canon(repv[x])].get(canon(beta[x]), 0) == 1 for x in support)
        assert exact == exact_alt, "exact-recovery routes disagree"
        costs = {k["dimension_id"]: rational(k["value"]) for k in cand["costs"]}
        per[cand["id"]] = {
            "case_loss": {x: str(v) for x, v in L.items()},
            "aggregate": value,
            "feasible": value <= tol,  # S21: "at most the frozen tolerance" (non-strict)
            "exact": exact,
            "cost": tuple(costs[k] for k in dims),  # keyed by id, ordered by declaration
        }

    ids = [x["id"] for x in admitted]
    F = [i for i in ids if per[i]["feasible"]]
    cost = {i: per[i]["cost"] for i in ids}

    def below(p, q):
        return all(a_ <= b_ for a_, b_ in zip(cost[p], cost[q]))

    def strictly(p, q):
        return below(p, q) and not below(q, p)

    pareto_bf = {i for i in F if not any(strictly(j, i) for j in F if j != i)}
    # Independent route: lexicographic sort + skyline sweep.
    frontier = []
    for i in sorted(F, key=lambda k: cost[k]):
        if not any(strictly(j, i) for j in frontier):
            frontier.append(i)
    assert pareto_bf == set(frontier), "Pareto routes disagree"

    pool = F if interp.least_requires_feasible else ids
    least_bf = {i for i in pool if all(below(i, j) for j in F)}
    if interp.least_requires_feasible:
        # Independent route: least elements are exactly the feasible candidates whose
        # cost equals the coordinatewise minimum (meet) of the feasible cost vectors.
        meet = tuple(min(cost[i][k] for i in F) for k in range(len(dims))) if F else None
        assert least_bf == {i for i in F if cost[i] == meet}, "least routes disagree"
    exact_set = {i for i in ids if per[i]["exact"]}

    res.detail.update(
        candidates={k: {**v, "aggregate": str(v["aggregate"]), "cost": [str(z) for z in v["cost"]]} for k, v in per.items()},
        feasible=sorted(F),
        pareto=sorted(pareto_bf),
        least=sorted(least_bf),
        exact_recovery=sorted(exact_set),
    )
    if set(ev["claimed_feasible"]) != set(F):
        codes.append("FEASIBLE_SET_MISMATCH")
    if set(ev["claimed_pareto_minimal"]) != pareto_bf:
        codes.append("PARETO_SET_MISMATCH")
    if set(ev["claimed_least_elements"]) != least_bf:
        codes.append("LEAST_SET_MISMATCH")
    if set(ev["exact_recovery_claims"]) != exact_set:
        codes.append("EXACT_RECOVERY_SET_MISMATCH")
    if tol == 0 and set(F) != exact_set:
        # Provably unreachable for a record reaching this point: aggregates are sums
        # or maxima of nonnegative terms, so aggregate <= 0 <=> zero loss on support.
        codes.append("ZERO_TOLERANCE_EXACT_BOUNDARY_FAILURE")
    return res
