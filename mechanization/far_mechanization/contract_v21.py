"""far-ir/2.1 finite-explicit approximation and cost validation.

far-ir/2.1 is an additive envelope over an unchanged far-ir/2.0 record.  The
validator deliberately implements only declaration-relative finite checks.  It
does not infer a universal metric, loss, aggregation, tolerance, scalar cost,
unique optimum, empirical adequacy, or open-domain completeness.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

from .contract_v2 import validate_contract as validate_v2

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schemas" / "far-contract-v21.schema.json"
FORMAT_VERSION = "far-ir/2.1"
PRESERVED_V2_BLOB_SHA1 = "e424359f804d268210e0f65fdf2fd28efc7e616b"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str
    message: str
    path: tuple[object, ...] = ()


@dataclass(frozen=True, slots=True)
class ValidationResult:
    diagnostics: tuple[Diagnostic, ...]
    computed: Mapping[str, Any] | None = None

    @property
    def success(self) -> bool:
        return not self.diagnostics


def _q(value: str) -> Fraction:
    return Fraction(value)


def _qs(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _schema_errors(document: object) -> list[Diagnostic]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    return [
        Diagnostic("SCHEMA_CONSTRAINT_VIOLATION", error.message, tuple(error.path))
        for error in sorted(validator.iter_errors(document), key=lambda e: (tuple(e.path), e.message))
    ]


def _key(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _pair_loss(discrepancy: Mapping[str, Any], left: object, right: object) -> Fraction:
    if discrepancy["kind"] == "zero_one":
        return Fraction(0 if _key(left) == _key(right) else 1)
    matches = [
        _q(row["value"])
        for row in discrepancy.get("table", [])
        if _key(row["left"]) == _key(left) and _key(row["right"]) == _key(right)
    ]
    if len(matches) != 1:
        raise ValueError("finite_table discrepancy requires exactly one matching ordered pair")
    return matches[0]


def _source_case_ids(base_v2: Mapping[str, Any]) -> list[str]:
    domain = base_v2["contract"]["source_domain"]
    if domain["kind"] != "finite_explicit" or domain["status"] != "EXPLICIT":
        raise ValueError("far-ir/2.1 operational checks require an EXPLICIT finite_explicit source domain")
    ids = [str(row["id"]) for row in domain["cases"]]
    if len(ids) != len(set(ids)):
        raise ValueError("source-domain case ids must be unique")
    return ids


def _compute_approximation(document: Mapping[str, Any], errors: list[Diagnostic]) -> dict[str, Any] | None:
    spec = document["approximation_semantics"]
    base = document["base_v2"]
    try:
        case_ids = _source_case_ids(base)
    except ValueError as exc:
        errors.append(Diagnostic("W5_SCOPE_REQUIRES_FINITE_EXPLICIT", str(exc)))
        return None

    samples = spec["samples"]
    sample_ids = [str(row["case_id"]) for row in samples]
    if len(sample_ids) != len(set(sample_ids)):
        errors.append(Diagnostic("DUPLICATE_APPROXIMATION_CASE", "approximation sample case ids must be unique"))
    if set(sample_ids) != set(case_ids):
        errors.append(Diagnostic(
            "APPROXIMATION_CASE_COVERAGE_MISMATCH",
            f"samples must cover source domain exactly missing={sorted(set(case_ids)-set(sample_ids))} extra={sorted(set(sample_ids)-set(case_ids))}",
        ))
        return None
    by_id = {str(row["case_id"]): row for row in samples}

    decoder = spec["decoder_class"]
    kernel = decoder.get("randomized_kernel", [])
    if decoder["kind"] == "randomized" and not kernel:
        errors.append(Diagnostic("RANDOMIZED_KERNEL_REQUIRED", "randomized decoder class requires an explicit randomized_kernel"))
        return None
    for index, entry in enumerate(kernel):
        try:
            probs = [_q(row["probability"]) for row in entry["output_distribution"]]
        except (ValueError, ZeroDivisionError) as exc:
            errors.append(Diagnostic("INVALID_RANDOMIZED_KERNEL", f"kernel entry {index}: {exc}"))
            return None
        if any(p < 0 for p in probs) or sum(probs, Fraction(0)) != 1:
            errors.append(Diagnostic("INVALID_RANDOMIZED_KERNEL", f"kernel entry {index} probabilities must be nonnegative and sum exactly to 1"))
            return None

    losses: list[Fraction] = []
    for case_id in case_ids:
        row = by_id[case_id]
        try:
            loss = _pair_loss(spec["discrepancy"], row["target"], row["achieved"])
        except (ValueError, ZeroDivisionError) as exc:
            errors.append(Diagnostic("DISCREPANCY_UNDEFINED", f"case {case_id}: {exc}"))
            return None
        if loss < 0:
            errors.append(Diagnostic("NEGATIVE_DISCREPANCY", f"case {case_id} has negative discrepancy"))
        if spec["discrepancy"]["separating"] and loss == 0 and _key(row["target"]) != _key(row["achieved"]):
            errors.append(Diagnostic("SEPARATING_DISCREPANCY_CONTRADICTION", f"case {case_id} declares separating discrepancy but unequal values have zero loss"))
        losses.append(loss)

    agg = spec["aggregation"]
    kind = agg["kind"]
    threshold_raw = spec["tolerance"]["threshold"]
    if kind == "pointwise" or kind == "vector":
        achieved: Fraction | list[Fraction] = list(losses)
        if not isinstance(threshold_raw, list) or len(threshold_raw) != len(losses):
            errors.append(Diagnostic("VECTOR_TOLERANCE_SHAPE_MISMATCH", f"{kind} aggregation requires one threshold per case"))
            return None
        thresholds = [_q(v) for v in threshold_raw]
        within = all(loss <= threshold for loss, threshold in zip(losses, thresholds))
    elif kind == "worst_case":
        if isinstance(threshold_raw, list):
            errors.append(Diagnostic("SCALAR_TOLERANCE_REQUIRED", "worst_case aggregation requires scalar threshold"))
            return None
        achieved = max(losses)
        within = achieved <= _q(threshold_raw)
    elif kind == "expected":
        if isinstance(threshold_raw, list):
            errors.append(Diagnostic("SCALAR_TOLERANCE_REQUIRED", "expected aggregation requires scalar threshold"))
            return None
        weights = agg.get("reference_measure")
        if not weights:
            errors.append(Diagnostic("REFERENCE_MEASURE_REQUIRED", "expected aggregation requires an explicit reference_measure"))
            return None
        weight_ids = [str(row["case_id"]) for row in weights]
        if len(weight_ids) != len(set(weight_ids)) or set(weight_ids) != set(case_ids):
            errors.append(Diagnostic("REFERENCE_MEASURE_COVERAGE_MISMATCH", "reference_measure must cover source cases exactly once"))
            return None
        w = {str(row["case_id"]): _q(row["weight"]) for row in weights}
        if any(value < 0 for value in w.values()) or sum(w.values(), Fraction(0)) != 1:
            errors.append(Diagnostic("INVALID_REFERENCE_MEASURE", "reference weights must be nonnegative and sum exactly to 1"))
            return None
        achieved = sum((w[c] * losses[i] for i, c in enumerate(case_ids)), Fraction(0))
        within = achieved <= _q(threshold_raw)
    else:
        errors.append(Diagnostic("UNSUPPORTED_AGGREGATION", f"unsupported aggregation {kind}"))
        return None

    separating = bool(spec["discrepancy"]["separating"])
    zero = all(loss == 0 for loss in losses)
    positive_support = True
    if kind == "expected":
        weights = {str(row["case_id"]): _q(row["weight"]) for row in agg["reference_measure"]}
        positive_support = all(weights[c] > 0 for c in case_ids)
    exactness_certified = bool(
        spec["claims_exact_at_zero"]
        and separating
        and zero
        and (kind in {"pointwise", "vector", "worst_case"} or (kind == "expected" and positive_support))
    )
    if spec["claims_exact_at_zero"] and not separating:
        errors.append(Diagnostic("ZERO_LOSS_NONSEPARATING", "zero loss cannot certify exactness under a nonseparating discrepancy"))
    if spec["claims_exact_at_zero"] and kind == "expected" and not positive_support:
        errors.append(Diagnostic("ZERO_EXPECTED_LOSS_LACKS_FULL_SUPPORT", "expected zero requires positive support on every finite source case to certify exactness"))

    return {
        "case_ids": case_ids,
        "losses": losses,
        "achieved": achieved,
        "within": within,
        "exactness_certified": exactness_certified,
    }


def _coord_map(candidate: Mapping[str, Any]) -> dict[str, tuple[Fraction, str, str]]:
    result: dict[str, tuple[Fraction, str, str]] = {}
    for row in candidate["coordinates"]:
        cid = str(row["id"])
        if cid in result:
            raise ValueError(f"duplicate cost coordinate {cid}")
        result[cid] = (_q(row["value"]), str(row["unit"]), str(row["direction"]))
    return result


def _componentwise_leq(left: Mapping[str, tuple[Fraction, str, str]], right: Mapping[str, tuple[Fraction, str, str]]) -> bool:
    if set(left) != set(right):
        raise ValueError("componentwise candidates require identical coordinate ids")
    for cid in left:
        lv, lu, ld = left[cid]
        rv, ru, rd = right[cid]
        if lu != ru or ld != rd:
            raise ValueError(f"coordinate {cid} has incompatible unit/direction")
        if ld == "min" and lv > rv:
            return False
        if ld == "max" and lv < rv:
            return False
    return True


def _compute_cost(document: Mapping[str, Any], errors: list[Diagnostic]) -> dict[str, Any] | None:
    spec = document["cost_semantics"]
    candidates = spec["candidates"]
    ids = [str(row["id"]) for row in candidates]
    if len(ids) != len(set(ids)):
        errors.append(Diagnostic("DUPLICATE_COST_CANDIDATE", "cost candidate ids must be unique"))
        return None
    by_id = {str(row["id"]): row for row in candidates}

    leq: dict[tuple[str, str], bool] = {}
    if spec["comparison"]["kind"] == "componentwise":
        try:
            maps = {cid: _coord_map(by_id[cid]) for cid in ids}
            for left in ids:
                for right in ids:
                    leq[(left, right)] = _componentwise_leq(maps[left], maps[right])
        except (ValueError, ZeroDivisionError) as exc:
            errors.append(Diagnostic("INVALID_COMPONENTWISE_COST", str(exc)))
            return None
    else:
        rel = {(str(r["better_or_equal"]), str(r["worse_or_equal"])) for r in spec["comparison"].get("relations", [])}
        if any(a not in by_id or b not in by_id for a, b in rel):
            errors.append(Diagnostic("PREORDER_UNKNOWN_CANDIDATE", "explicit preorder references unknown candidate"))
            return None
        for cid in ids:
            rel.add((cid, cid))
        for a in ids:
            for b in ids:
                for c in ids:
                    if (a, b) in rel and (b, c) in rel and (a, c) not in rel:
                        errors.append(Diagnostic("PREORDER_NOT_TRANSITIVE", f"missing transitive relation {a}<={c}"))
                        return None
        leq = {(a, b): ((a, b) in rel) for a in ids for b in ids}

    def strict(a: str, b: str) -> bool:
        return leq[(a, b)] and not leq[(b, a)]

    minimal = [cid for cid in ids if not any(strict(other, cid) for other in ids if other != cid)]
    least = sorted(cid for cid in ids if all(leq[(cid, other)] for other in ids))
    unique_least_id = least[0] if len(least) == 1 else None

    selected = None
    scalar = spec.get("scalarization")
    if scalar is not None:
        weights = {str(row["coordinate_id"]): _q(row["weight"]) for row in scalar["weights"]}
        if any(w < 0 for w in weights.values()):
            errors.append(Diagnostic("NEGATIVE_SCALARIZATION_WEIGHT", "scalarization weights must be nonnegative"))
            return None
        if sum(weights.values(), Fraction(0)) == 0:
            errors.append(Diagnostic("ZERO_SCALARIZATION", "scalarization requires at least one positive weight"))
            return None
        scores: dict[str, Fraction] = {}
        try:
            maps = {cid: _coord_map(by_id[cid]) for cid in ids}
            if any(set(weights) != set(maps[cid]) for cid in ids):
                raise ValueError("scalarization weights must cover every cost coordinate exactly")
            for cid in ids:
                score = Fraction(0)
                for coord, weight in weights.items():
                    value, _unit, direction = maps[cid][coord]
                    score += weight * (value if direction == "min" else -value)
                scores[cid] = score
        except (ValueError, ZeroDivisionError) as exc:
            errors.append(Diagnostic("INVALID_SCALARIZATION", str(exc)))
            return None
        best = min(scores.values())
        winners = sorted(cid for cid, score in scores.items() if score == best)
        selected = winners[0] if len(winners) == 1 else None

    return {"minimal": sorted(minimal), "least": least, "unique_least": unique_least_id, "selected": selected}


def validate_contract(document: object) -> ValidationResult:
    errors = _schema_errors(document)
    if errors or not isinstance(document, Mapping):
        return ValidationResult(tuple(errors))
    base = document["base_v2"]
    v2 = validate_v2(base)
    if not v2.success:
        errors.extend(Diagnostic("BASE_V2_INVALID", f"{d.code}: {d.message}", ("base_v2",)+tuple(d.path)) for d in v2.diagnostics)
        return ValidationResult(tuple(errors))
    if base.get("format_version") != "far-ir/2.0":
        errors.append(Diagnostic("BASE_VERSION_MISMATCH", "base_v2 must remain far-ir/2.0"))
    if base["contract"]["mode"] != "approximate":
        errors.append(Diagnostic("BASE_MODE_NOT_APPROXIMATE", "far-ir/2.1 approximation envelope requires base_v2 contract.mode=approximate"))
    approx = base["contract"].get("approximation", {})
    if approx.get("w5_semantics_established") is not False:
        errors.append(Diagnostic("V2_BOUNDARY_CHANGED", "base_v2 must retain w5_semantics_established=false"))

    a = _compute_approximation(document, errors)
    c = _compute_cost(document, errors)
    if a is None or c is None:
        return ValidationResult(tuple(errors))

    report = document["report"]
    expected_losses = [_qs(v) for v in a["losses"]]
    if report["approximation"]["per_case_loss"] != expected_losses:
        errors.append(Diagnostic("APPROXIMATION_REPORT_LOSS_MISMATCH", f"expected {expected_losses}"))
    achieved = a["achieved"]
    expected_achieved = [_qs(v) for v in achieved] if isinstance(achieved, list) else _qs(achieved)
    if report["approximation"]["achieved"] != expected_achieved:
        errors.append(Diagnostic("APPROXIMATION_REPORT_AGGREGATE_MISMATCH", f"expected {expected_achieved}"))
    if report["approximation"]["within_tolerance"] != a["within"]:
        errors.append(Diagnostic("APPROXIMATION_REPORT_TOLERANCE_MISMATCH", f"expected {a['within']}"))
    if report["approximation"]["exactness_certified"] != a["exactness_certified"]:
        errors.append(Diagnostic("APPROXIMATION_REPORT_EXACTNESS_MISMATCH", f"expected {a['exactness_certified']}"))

    if sorted(report["cost"]["minimal_candidate_ids"]) != c["minimal"]:
        errors.append(Diagnostic("COST_REPORT_MINIMAL_SET_MISMATCH", f"expected {c['minimal']}"))
    if sorted(report["cost"]["least_candidate_ids"]) != c["least"]:
        errors.append(Diagnostic("COST_REPORT_LEAST_SET_MISMATCH", f"expected {c['least']}"))
    if report["cost"]["unique_least_candidate_id"] != c["unique_least"]:
        errors.append(Diagnostic("COST_REPORT_UNIQUE_LEAST_MISMATCH", f"expected {c['unique_least']}"))
    if report["cost"].get("scalarized_selected_candidate_id") != c["selected"]:
        errors.append(Diagnostic("COST_REPORT_SCALARIZATION_MISMATCH", f"expected {c['selected']}"))

    return ValidationResult(tuple(errors), computed={
        "losses": expected_losses,
        "achieved": expected_achieved,
        "within_tolerance": a["within"],
        "exactness_certified": a["exactness_certified"],
        "minimal_candidate_ids": c["minimal"],
        "least_candidate_ids": c["least"],
        "unique_least_candidate_id": c["unique_least"],
        "scalarized_selected_candidate_id": c["selected"],
    })


def load_and_validate(path: str | Path) -> ValidationResult:
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return ValidationResult((Diagnostic("UNREADABLE_CONTRACT", str(exc)),))
    return validate_contract(document)


def main(argv: Sequence[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(prog="python -m mechanization.far_mechanization.contract_v21")
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = load_and_validate(args.path)
    payload = {
        "success": result.success,
        "computed": result.computed,
        "diagnostics": [{"code": d.code, "message": d.message, "path": list(d.path)} for d in result.diagnostics],
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("PASS" if result.success else "FAIL")
        for diagnostic in result.diagnostics:
            print(f"{diagnostic.code}: {diagnostic.message}")
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
