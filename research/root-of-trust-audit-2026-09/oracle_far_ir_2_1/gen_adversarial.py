"""Generate the adversarial far-ir/2.1 corpus from the registered frontier fixture.

Each record is written as a standalone far-ir/2.1 document to adversarial/<name>.json.
Expected outcomes, alternatives under ambiguous readings, and spec citations are
written to adversarial/expected.json. Unless `rehash=False`, the freeze hash is
recomputed after mutating the contract so that FREEZE_HASH_MISMATCH does not mask
the targeted defect (S21 Stage 1 / Gate 1).
"""
from __future__ import annotations

import copy
import json
import pathlib

from oracle import ROOT, contract_sha256

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "adversarial"
BASE = json.loads((ROOT / "conformance/far-ir-2.1/valid-frontier.json").read_text())

F, T = False, True


def ent(l, r, dist):
    return {"left": l, "right": r, "distance": dist}


def lossent(t, a, v):
    return {"truth": t, "action": a, "loss": v}


def dist(*pairs):
    return [{"action": a, "probability": p} for a, p in pairs]


def row(rv, *pairs):
    return {"representation_value": rv, "distribution": dist(*pairs)}


def costs(**kw):
    return [{"dimension_id": k, "value": v} for k, v in kw.items()]


def cand(cid, rows, cost_list):
    return {"id": cid, "decoder_table": rows, "costs": cost_list}


def appr(r):
    return r["contract"]["approximation"]


def evid(r):
    return r["report"]["evidence"]


def cands(r):
    return {c["id"]: c for c in evid(r)["candidates"]}


def claims(r, feasible, pareto, least, exact):
    e = evid(r)
    e["claimed_feasible"], e["claimed_pareto_minimal"] = feasible, pareto
    e["claimed_least_elements"], e["exact_recovery_claims"] = least, exact


def metric_with_x(dmap):
    """Metric over [false, true, "x"]; dmap gives (l, r) -> distance for x-pairs."""
    vals = [F, T, "x"]
    base = {(F, F): "0", (F, T): "1", (T, F): "1", (T, T): "0"}
    base.update(dmap)
    return {"kind": "finite_table_metric", "values": vals,
            "entries": [ent(l, r, base[(l, r)]) for l in vals for r in vals]}


CASES = []


def case(name, cite, expected, why, alternatives=(), rehash=True):
    def deco(fn):
        rec = copy.deepcopy(BASE)
        rec["id"] = rec["contract"]["id"] = "adv." + name.replace("_", ".")
        fn(rec)
        if rehash and rec["freeze"]["status"] == "FROZEN":
            rec["freeze"]["contract_sha256"] = contract_sha256(rec["contract"])
        CASES.append(dict(name=name, record=rec, expected=list(expected), why=why,
                          cite=cite, alternatives=[dict(a) for a in alternatives]))
        return fn
    return deco


TRI = "METRIC_TRIANGLE_FAILURE"
SYM = "METRIC_SYMMETRY_FAILURE"
SEP = "METRIC_SEPARATION_FAILURE"


# ---------------- Metric axioms (S21 §Frozen semantics item 1; §Metric table) ----------
@case("metric_triangle_single_shortcut", "S21 item 1; METRIC_TRIANGLE_FAILURE; Stage 2",
      [TRI, TRI],
      "d(f,t)=1 > d(f,x)+d(x,t)=1/4+1/4; only ordered triples (f,x,t),(t,x,f) fail. "
      "Symmetric, identity and separation hold; loss table over {f,t} unchanged.",
      [{"interp": {"triples": "unordered_endpoints"}, "codes": [TRI]}])
def _(r):
    appr(r)["metric"] = metric_with_x({(F, "x"): "1/4", ("x", F): "1/4", (T, "x"): "1/4",
                                       ("x", T): "1/4", ("x", "x"): "0"})


@case("metric_asymmetric_triangle_tight", "S21 item 1; METRIC_SYMMETRY_FAILURE",
      [SYM, SYM],
      "d(f,x)=1, d(x,f)=2. Triangle is tight, not violated: d(x,f)=2 = d(x,t)+d(t,f)=1+1 "
      "(non-strict '>' in METRIC_TRIANGLE_FAILURE).",
      [{"interp": {"pairs": "unordered"}, "codes": [SYM]}])
def _(r):
    appr(r)["metric"] = metric_with_x({(F, "x"): "1", ("x", F): "2", (T, "x"): "1",
                                       ("x", T): "1", ("x", "x"): "0"})


@case("metric_identity_failure", "S21 item 1; METRIC_IDENTITY_FAILURE",
      ["METRIC_IDENTITY_FAILURE"],
      "d(x,x)=1; all other x-distances 1; no triple violates (1 > 1+1 is false).")
def _(r):
    appr(r)["metric"] = metric_with_x({(F, "x"): "1", ("x", F): "1", (T, "x"): "1",
                                       ("x", T): "1", ("x", "x"): "1"})


@case("metric_degenerate_triangle_probe", "S21 METRIC_TRIANGLE_FAILURE 'for a declared triple'",
      ["METRIC_IDENTITY_FAILURE", TRI],
      "d(x,x)=1 > d(x,f)+d(f,x)=1/4+1/4: the only violating triple has l=r=x.",
      [{"interp": {"triples": "ordered_distinct_endpoints"}, "codes": ["METRIC_IDENTITY_FAILURE"]}])
def _(r):
    appr(r)["metric"] = metric_with_x({(F, "x"): "1/4", ("x", F): "1/4", (T, "x"): "1",
                                       ("x", T): "1", ("x", "x"): "1"})


@case("metric_pseudometric", "S21 item 1 (separation); §Exact boundary excludes pseudometrics",
      [SEP, SEP],
      "d(f,x)=d(x,f)=0 with f != x; d(x,t)=1; triangle holds everywhere.",
      [{"interp": {"pairs": "unordered"}, "codes": [SEP]}])
def _(r):
    appr(r)["metric"] = metric_with_x({(F, "x"): "0", ("x", F): "0", (T, "x"): "1",
                                       ("x", T): "1", ("x", "x"): "0"})


@case("metric_not_total_suppresses_axioms", "S21 METRIC_NOT_TOTAL 'Suppresses the four ... checks'",
      ["METRIC_NOT_TOTAL"],
      "Entry (x,x) missing; a 1/4-shortcut triangle violation is also present but suppressed. "
      "Loss pairs over {f,t} all have metric entries, so no METRIC_LOSS_DOMAIN_MISMATCH.")
def _(r):
    m = metric_with_x({(F, "x"): "1/4", ("x", F): "1/4", (T, "x"): "1/4",
                       ("x", T): "1/4", ("x", "x"): "0"})
    m["entries"] = [e for e in m["entries"] if not (e["left"] == "x" and e["right"] == "x")]
    appr(r)["metric"] = m


@case("metric_false_vs_zero_canonical_distinct", "S21 DUPLICATE_METRIC_VALUE 'canonical value'",
      [],
      "Values [false,true,0]: distinct as canonical JSON ('false' vs '0'); discrete metric. "
      "An implementation using host-language equality (False == 0) would instead emit "
      "DUPLICATE_METRIC_VALUE / DUPLICATE_METRIC_ENTRY codes (not machine-checked here).")
def _(r):
    vals = [F, T, 0]
    appr(r)["metric"] = {"kind": "finite_table_metric", "values": vals,
                         "entries": [ent(l, rr, "0" if i == j else "1")
                                     for i, l in enumerate(vals) for j, rr in enumerate(vals)]}


@case("duplicate_metric_value", "S21 DUPLICATE_METRIC_VALUE", ["DUPLICATE_METRIC_VALUE"],
      "values [false,true,false]; product over the declared set is still covered.")
def _(r):
    appr(r)["metric"]["values"].append(False)


# ---------------- Reference (S21 item 2; §Reference measure) -------------------------
@case("reference_sum_five_sixths", "S21 REFERENCE_NOT_PROBABILITY", ["REFERENCE_NOT_PROBABILITY"],
      "1/2 + 1/3 = 5/6 != 1.")
def _(r):
    appr(r)["reference"]["weights"][1]["weight"] = "1/3"


@case("reference_missing_case", "S21 REFERENCE_COVERAGE_MISMATCH", ["REFERENCE_COVERAGE_MISMATCH"],
      "Only case.zero weighted (weight 1): sums to 1 but case.one undeclared "
      "(zero mass must be explicit, S21 item 2).")
def _(r):
    appr(r)["reference"]["weights"] = [{"case_id": "case.zero", "weight": "1"}]


# ---------------- Loss (S21 item 4; §Loss) -------------------------------------------
@case("loss_differs_from_metric", "S21 item 4; LOSS_METRIC_MISMATCH", ["LOSS_METRIC_MISMATCH"],
      "loss(false,true)=2 while d(false,true)=1.")
def _(r):
    appr(r)["loss"]["entries"][1]["loss"] = "2"


@case("loss_extra_entry_not_total", "S21 LOSS_NOT_TOTAL 'exactly'", ["LOSS_NOT_TOTAL"],
      "Extra loss row (truth 'x', action false) outside range x actions; value equals the "
      "(discrete) metric so no per-pair code under either iteration reading.")
def _(r):
    appr(r)["metric"] = metric_with_x({(F, "x"): "1", ("x", F): "1", (T, "x"): "1",
                                       ("x", T): "1", ("x", "x"): "0"})
    appr(r)["loss"]["entries"].append(lossent("x", F, "1"))


@case("stage2_accumulation_order", "S21 Stage 2 order",
      ["REFERENCE_NOT_PROBABILITY", "METRIC_IDENTITY_FAILURE", "LOSS_METRIC_MISMATCH",
       "DUPLICATE_COST_DIMENSION"],
      "One defect of each Stage 2 family; sequence must follow Stage 2 order.")
def _(r):
    a = appr(r)
    a["reference"]["weights"][1]["weight"] = "1/3"
    a["metric"] = metric_with_x({(F, "x"): "1", ("x", F): "1", (T, "x"): "1",
                                 ("x", T): "1", ("x", "x"): "1"})
    a["loss"]["entries"][1]["loss"] = "2"
    a["cost_preorder"]["dimensions"].append(copy.deepcopy(a["cost_preorder"]["dimensions"][0]))


@case("stage2_masks_candidates_and_frontier", "S21 Gate 2", ["REFERENCE_NOT_PROBABILITY"],
      "Reference defect plus a non-probability decoder and a false feasible claim: Gate 2 "
      "returns before candidates/frontier.")
def _(r):
    appr(r)["reference"]["weights"][1]["weight"] = "1/3"
    cands(r)["exact"]["decoder_table"][0]["distribution"][0]["probability"] = "1/2"
    evid(r)["claimed_feasible"] = ["exact"]


# ---------------- Probabilities & exact arithmetic (SCHEMA Probability; S21 §5-6) ----
@case("decoder_float_probability", "SCHEMA $defs.Probability (string pattern); S21 schema terminal",
      ["SCHEMA_CONSTRAINT_VIOLATION"], "probability 0.5 as a JSON number.", rehash=False)
def _(r):
    cands(r)["randomized"]["decoder_table"][0]["distribution"][0]["probability"] = 0.5


@case("decoder_decimal_string", "SCHEMA $defs.Probability", ["SCHEMA_CONSTRAINT_VIOLATION"],
      "probability '0.5' as a decimal string.", rehash=False)
def _(r):
    cands(r)["randomized"]["decoder_table"][0]["distribution"][0]["probability"] = "0.5"


@case("decoder_negative_probability", "SCHEMA $defs.Probability; S21 DECODER_NOT_PROBABILITY",
      ["SCHEMA_CONSTRAINT_VIOLATION"],
      "'-1/2' and '3/2' in one row (sum 1). The schema pattern forbids a sign, so the "
      "'negative entry' clause of DECODER_NOT_PROBABILITY is unreachable post-schema.",
      rehash=False)
def _(r):
    d = cands(r)["randomized"]["decoder_table"][0]["distribution"]
    d[0]["probability"], d[1]["probability"] = "-1/2", "3/2"


@case("tolerance_float", "SCHEMA $defs.NonnegativeRational", ["SCHEMA_CONSTRAINT_VIOLATION"],
      "tolerance 0.5 as a JSON number (hash recomputed so only the schema defect remains).")
def _(r):
    appr(r)["tolerance"] = 0.5


@case("decoder_sum_one_minus_1e-17_exact", "S21 DECODER_NOT_PROBABILITY 'exactly one'",
      ["DECODER_NOT_PROBABILITY"],
      "99999999999999999/10^17 + 0 != 1 exactly (binary64 would round it to 1.0).")
def _(r):
    cands(r)["exact"]["decoder_table"][0]["distribution"][0]["probability"] = \
        "99999999999999999/100000000000000000"


@case("near_exact_decoder_is_not_exact", "S21 §Exact boundary; EXACT_RECOVERY_SET_MISMATCH",
      ["EXACT_RECOVERY_SET_MISMATCH"],
      "Row sums to exactly 1 with 10^-17 on the wrong action: L(case.zero)=10^-17 > 0, so "
      "'exact' is feasible but not exact; exact-recovery set is empty.")
def _(r):
    d = cands(r)["exact"]["decoder_table"][0]["distribution"]
    d[0]["probability"], d[1]["probability"] = "99999999999999999/100000000000000000", \
        "1/100000000000000000"


@case("decoder_nonreduced_fractions_accept", "SCHEMA pattern admits '2/4'; S21 exact rationals", [],
      "'2/4','2/4' and '0/7'-style values are exact 1/2 and 0; record otherwise equals fixture.")
def _(r):
    for rw in cands(r)["randomized"]["decoder_table"]:
        for x in rw["distribution"]:
            x["probability"] = "2/4"
    cands(r)["exact"]["decoder_table"][0]["distribution"][1]["probability"] = "0/7"


@case("decoder_unknown_action_positive", "S21 DECODER_UNKNOWN_ACTION", ["DECODER_UNKNOWN_ACTION"],
      "r0 -> {false:1/2, 'abstain':1/2}; full row sums to 1.",
      [{"interp": {"decoder_sum_over_declared_only": True},
        "codes": ["DECODER_UNKNOWN_ACTION", "DECODER_NOT_PROBABILITY"]}])
def _(r):
    cands(r)["randomized"]["decoder_table"][0]["distribution"][1]["action"] = "abstain"


@case("decoder_unknown_action_zero_probability_probe", "S21 DECODER_UNKNOWN_ACTION 'assigns probability'",
      ["DECODER_UNKNOWN_ACTION"],
      "Exact candidate adds {'abstain': '0'}; whether an explicit zero is an 'assignment' is open.",
      [{"interp": {"unknown_action_zero_counts": False}, "codes": []}])
def _(r):
    cands(r)["exact"]["decoder_table"][0]["distribution"].append({"action": "abstain", "probability": "0"})


# ---------------- Tolerance boundary (S21 §Frozen semantics: 'at most') ---------------
@case("tolerance_boundary_float_trap_accept", "S21 'feasible exactly when aggregate is at most tolerance'",
      [],
      "randomized r0->{f:4/5,t:1/5}, r1->{f:2/5,t:3/5}: L=(1/5,2/5), E=1/10+1/5=3/10 = tol 3/10 "
      "=> feasible. binary64: 0.5*0.2+0.5*0.4 = 0.30000000000000004 > 0.3. dominated E=1/2 infeasible.")
def _(r):
    appr(r)["tolerance"] = "3/10"
    c = cands(r)["randomized"]
    c["decoder_table"] = [row("r0", (F, "4/5"), (T, "1/5")), row("r1", (F, "2/5"), (T, "3/5"))]
    claims(r, ["randomized", "exact"], ["randomized", "exact"], [], ["exact"])


@case("tolerance_strict_misread", "S21 'at most' (non-strict)",
      ["FEASIBLE_SET_MISMATCH", "PARETO_SET_MISMATCH", "LEAST_SET_MISMATCH"],
      "Claims computed with strict '<' at tol 1/2: feasible {exact} only. Recomputed: "
      "feasible {randomized, exact, dominated}, Pareto {randomized, exact}, least {}.")
def _(r):
    claims(r, ["exact"], ["exact"], ["exact"], ["exact"])


# ---------------- Cost preorder (S21 §Cost conclusions) ------------------------------
@case("cost_ties_two_least_accept", "S21 'below ... no greater on every coordinate'; least", [],
      "A,B exact with equal cost (2,2); C randomized (3,3). Pareto {A,B}; least {A,B} "
      "(preorder: ties are mutually below); exact {A,B}.")
def _(r):
    e = evid(r)
    ex = cands(r)["exact"]["decoder_table"]
    e["candidates"] = [cand("A", copy.deepcopy(ex), costs(storage="2", evaluation="2")),
                       cand("B", copy.deepcopy(ex), costs(storage="2", evaluation="2")),
                       cand("C", copy.deepcopy(cands(r)["randomized"]["decoder_table"]),
                            costs(storage="3", evaluation="3"))]
    claims(r, ["A", "B", "C"], ["A", "B"], ["A", "B"], ["A", "B"])


@case("cost_ties_claim_no_least", "S21 least element", ["LEAST_SET_MISMATCH"],
      "Same as cost_ties_two_least_accept but claims no least element (uniqueness assumed).")
def _(r):
    e = evid(r)
    ex = cands(r)["exact"]["decoder_table"]
    e["candidates"] = [cand("A", copy.deepcopy(ex), costs(storage="2", evaluation="2")),
                       cand("B", copy.deepcopy(ex), costs(storage="2", evaluation="2")),
                       cand("C", copy.deepcopy(cands(r)["randomized"]["decoder_table"]),
                            costs(storage="3", evaluation="3"))]
    claims(r, ["A", "B", "C"], ["A", "B"], [], ["A", "B"])


@case("incomparable_lexicographic_least_claim", "S21 'Costs are not silently scalarized'",
      ["LEAST_SET_MISMATCH"],
      "Fixture with least claimed ['randomized'] (storage-first lexicographic scalarization).")
def _(r):
    evid(r)["claimed_least_elements"] = ["randomized"]


@case("cost_order_permuted_accept", "S21 COST_COVERAGE_MISMATCH (coverage by dimension id)", [],
      "randomized lists costs as [evaluation=3, storage=1]. Keyed reading: (1,3), fixture result. "
      "A positional reader would get (3,1), tie with exact, making both least -> LEAST_SET_MISMATCH.")
def _(r):
    cands(r)["randomized"]["costs"].reverse()


@case("infeasible_cheap_candidate_least_probe", "S21 'A least element must be below every feasible candidate'",
      [],
      "Add cheap_wrong (0,0) with r0->true, r1->false: E=1 > 1/2, infeasible. Pareto ignores it "
      "(dominance only by feasible candidates). Least over feasible is empty.",
      [{"interp": {"least_requires_feasible": False}, "codes": ["LEAST_SET_MISMATCH"]}])
def _(r):
    evid(r)["candidates"].append(cand("cheap_wrong", [row("r0", (F, "0"), (T, "1")),
                                                     row("r1", (F, "1"), (T, "0"))],
                                      costs(storage="0", evaluation="0")))


@case("fixture_under_maximum_aggregation", "S21 aggregate max_x L_d(x); RESULTS 'observably different'",
      ["FEASIBLE_SET_MISMATCH"],
      "aggregation=maximum: dominated has max(0,1)=1 > 1/2, infeasible; Pareto {randomized, exact}, "
      "least {}, exact {exact} unchanged.")
def _(r):
    appr(r)["aggregation"] = "maximum"


# ---------------- Zero mass / exact boundary (S21 §Exact boundary) --------------------
def _zero_mass(r, aggregation, exact_claim, feasible_claim):
    a = appr(r)
    a["reference"]["weights"][0]["weight"], a["reference"]["weights"][1]["weight"] = "1", "0"
    a["tolerance"], a["aggregation"] = "0", aggregation
    claims(r, feasible_claim, ["exact"], ["exact"], exact_claim)


@case("zero_mass_expected_support_relative_accept", "S21 §Exact boundary (support-relative)", [],
      "mu=(1,0), tol 0, expected: dominated E=1*0+0*1=0 -> feasible and exact on support; "
      "randomized E=1/2. feasible=exact={exact,dominated}; Pareto=least={exact}.")
def _(r):
    _zero_mass(r, "expected", ["exact", "dominated"], ["exact", "dominated"])


@case("zero_mass_full_domain_exact_claim", "S21 'zero-mass cases ... cannot be inferred from a zero aggregate'",
      ["EXACT_RECOVERY_SET_MISMATCH"],
      "As above but claims exact recovery = {exact} (full-domain inference). No "
      "ZERO_TOLERANCE_EXACT_BOUNDARY_FAILURE: the recomputed sets agree; only the claim is wrong.")
def _(r):
    _zero_mass(r, "expected", ["exact"], ["exact", "dominated"])


@case("zero_mass_under_maximum", "S21 §Exact boundary: maximum inspects every case",
      ["FEASIBLE_SET_MISMATCH", "EXACT_RECOVERY_SET_MISMATCH"],
      "mu=(1,0), tol 0, maximum: dominated max loss 1 -> infeasible, not exact. Claims copied "
      "from the expected-aggregation reading.")
def _(r):
    _zero_mass(r, "maximum", ["exact", "dominated"], ["exact", "dominated"])


def _collision(r, aggregation, tol):
    c = r["contract"]
    c["representation"]["table"][1]["value"] = "r0"
    appr(r)["aggregation"], appr(r)["tolerance"] = aggregation, tol
    evid(r)["candidates"] = [
        cand("always_false", [row("r0", (F, "1"), (T, "0"))], costs(storage="1", evaluation="1")),
        cand("always_true", [row("r0", (F, "0"), (T, "1"))], costs(storage="2", evaluation="2")),
        cand("coin", [row("r0", (F, "1/2"), (T, "1/2"))], costs(storage="3", evaluation="3")),
    ]


@case("collision_zero_tolerance_vacuous_least_probe", "S21 least; §Exact boundary", [],
      "r(case.zero)=r(case.one)=r0 with different beta: every decoder has E=1/2. tol 0 -> "
      "feasible = exact = Pareto = least = {} (all claims empty).",
      [{"interp": {"least_requires_feasible": False}, "codes": ["LEAST_SET_MISMATCH"]}])
def _(r):
    _collision(r, "expected", "0")
    claims(r, [], [], [], [])


@case("collision_maximum_randomization_accept", "S21 max aggregation; randomized decoders", [],
      "maximum, tol 1/2: always_false/always_true have max loss 1; coin has max 1/2 -> the "
      "randomized decoder is the unique feasible, Pareto and least candidate; exact {}.")
def _(r):
    _collision(r, "maximum", "1/2")
    claims(r, ["coin"], ["coin"], ["coin"], [])


@case("collision_maximum_expected_claims", "S21 aggregation rule",
      ["FEASIBLE_SET_MISMATCH", "PARETO_SET_MISMATCH", "LEAST_SET_MISMATCH"],
      "Same record, claims computed under expected aggregation (all feasible; always_false least).")
def _(r):
    _collision(r, "maximum", "1/2")
    claims(r, ["always_false", "always_true", "coin"], ["always_false"], ["always_false"], [])


# ---------------- Candidates, gating (S21 Stage 3, Gates 3-4) ------------------------
@case("duplicate_candidate_skips_its_errors", "S21 DUPLICATE_CANDIDATE 'later candidate is skipped'",
      ["DUPLICATE_CANDIDATE"],
      "4th candidate reuses id 'exact' and has a 3/4-sum row; skipped, so no DECODER_NOT_PROBABILITY.")
def _(r):
    bad = copy.deepcopy(cands(r)["exact"])
    bad["decoder_table"][0]["distribution"][0]["probability"] = "3/4"
    evid(r)["candidates"].append(bad)


@case("candidate_errors_accumulate", "S21 Stage 3 (later candidates still checked)",
      ["COST_COVERAGE_MISMATCH", "DECODER_NOT_PROBABILITY"],
      "randomized lacks 'evaluation'; dominated r1 row sums to 1/2.")
def _(r):
    cands(r)["randomized"]["costs"].pop()
    cands(r)["dominated"]["decoder_table"][1]["distribution"][0]["probability"] = "1/2"


@case("decoder_coverage_masks_frontier", "S21 DECODER_COVERAGE_MISMATCH; Gate 4",
      ["DECODER_COVERAGE_MISMATCH"],
      "exact lacks the r1 row; a false 'ghost' feasible claim is not reported (Gate 4).")
def _(r):
    cands(r)["exact"]["decoder_table"].pop()
    evid(r)["claimed_feasible"].append("ghost")


@case("decoder_extra_unused_representation", "S21 DECODER_COVERAGE_MISMATCH 'exactly'",
      ["DECODER_COVERAGE_MISMATCH"], "exact adds a row for unused representation value r2.")
def _(r):
    cands(r)["exact"]["decoder_table"].append(row("r2", (F, "1"), (T, "0")))


@case("claim_unknown_candidate_id", "S21 FEASIBLE_SET_MISMATCH", ["FEASIBLE_SET_MISMATCH"],
      "claimed_feasible includes non-existent 'ghost'.")
def _(r):
    evid(r)["claimed_feasible"].append("ghost")


# ---------------- Stage 1 (S21 intake/mode/freeze/tables) ----------------------------
@case("freeze_hash_masks_decoder_error", "S21 Gate 1; S20 §9.8", ["FREEZE_HASH_MISMATCH"],
      "tolerance changed without re-hashing, plus a non-probability decoder row.", rehash=False)
def _(r):
    appr(r)["tolerance"] = "1/3"
    cands(r)["exact"]["decoder_table"][0]["distribution"][0]["probability"] = "1/2"


@case("draft_contract", "S21 CHECK_REQUIRES_FROZEN_CONTRACT", ["CHECK_REQUIRES_FROZEN_CONTRACT"],
      "freeze.status DRAFT with null time/hash (schema-valid).")
def _(r):
    r["freeze"].update(status="DRAFT", frozen_at=None, contract_sha256=None)


@case("outcome_refuted", "S21 CHECKED_EVIDENCE_OUTCOME_MISMATCH", ["CHECKED_EVIDENCE_OUTCOME_MISMATCH"],
      "report.outcome REFUTED with approximation_cost evidence.")
def _(r):
    r["report"]["outcome"] = "REFUTED"


@case("mode_exact", "S21 W5_MODE_EVIDENCE_REQUIRED", ["W5_MODE_EVIDENCE_REQUIRED"],
      "contract.mode = exact (approximation block retained).")
def _(r):
    r["contract"]["mode"] = "exact"


@case("representation_declared", "S21 CHECK_REQUIRES_EXPLICIT_REPRESENTATION",
      ["CHECK_REQUIRES_EXPLICIT_REPRESENTATION"], "representation.status = DECLARED.")
def _(r):
    r["contract"]["representation"]["status"] = "DECLARED"


@case("behavior_missing_case", "S21 CASE_TABLE_COVERAGE_MISMATCH", ["CASE_TABLE_COVERAGE_MISMATCH"],
      "required_behavior table omits case.one (representation still complete).")
def _(r):
    r["contract"]["required_behavior"]["table"].pop()


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    index = []
    for c in CASES:
        path = OUT / f"{c['name']}.json"
        path.write_text(json.dumps(c["record"], indent=2) + "\n")
        index.append({k: c[k] for k in ("name", "expected", "alternatives", "cite", "why")}
                     | {"file": f"adversarial/{path.name}"})
    (OUT / "expected.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"wrote {len(CASES)} records + expected.json")
