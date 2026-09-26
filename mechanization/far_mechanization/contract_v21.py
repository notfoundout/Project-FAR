"""Decidable finite-explicit ``far-ir/2.1`` approximation/cost semantics.

JSON Schema validates document shape.  This module recomputes only claims that
are decidable from a finite record.  Arithmetic is exact, and malformed
semantic tables fail closed before they can influence a frontier result.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schemas" / "far-contract-v2.1.schema.json"
FORMAT_VERSION = "far-ir/2.1"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str
    message: str
    path: tuple[object, ...] = ()


@dataclass(frozen=True, slots=True)
class Result:
    diagnostics: tuple[Diagnostic, ...]

    @property
    def success(self) -> bool:
        return not self.diagnostics


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def contract_sha256(contract: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(contract).encode("utf-8")).hexdigest()


def _key(value: object) -> str:
    return canonical_json(value)


def _fraction(value: object) -> Fraction:
    return Fraction(str(value))


def _add(errors: list[Diagnostic], code: str, message: str) -> None:
    errors.append(Diagnostic(code, message))


def _unique_values(
    values: Sequence[object], label: str, errors: list[Diagnostic]
) -> dict[str, object]:
    indexed: dict[str, object] = {}
    for value in values:
        value_key = _key(value)
        if value_key in indexed:
            _add(errors, f"DUPLICATE_{label}", f"duplicate canonical value {value_key}")
        indexed[value_key] = value
    return indexed


def _case_table(
    rows: Sequence[Mapping[str, Any]], label: str, errors: list[Diagnostic]
) -> dict[str, object]:
    indexed: dict[str, object] = {}
    for row in rows:
        case_id = str(row["case_id"])
        if case_id in indexed:
            _add(errors, "DUPLICATE_CASE_VALUE", f"{label}: {case_id}")
        indexed[case_id] = row["value"]
    return indexed


def _schema_errors(document: object) -> list[Diagnostic]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    return [
        Diagnostic("SCHEMA_CONSTRAINT_VIOLATION", error.message, tuple(error.path))
        for error in sorted(
            validator.iter_errors(document), key=lambda item: (tuple(item.path), item.message)
        )
    ]


def validate_contract(document: object) -> Result:
    errors = _schema_errors(document)
    if errors or not isinstance(document, Mapping):
        return Result(tuple(errors))

    contract = document["contract"]
    evidence = document["report"]["evidence"]
    approximation = contract.get("approximation")
    if contract["mode"] != "approximate" or evidence["kind"] != "approximation_cost":
        _add(
            errors,
            "W5_MODE_EVIDENCE_REQUIRED",
            "far-ir/2.1 checked records require approximate mode and approximation_cost evidence",
        )
    if document["report"]["outcome"] != "PROVED":
        _add(
            errors,
            "CHECKED_EVIDENCE_OUTCOME_MISMATCH",
            "checked approximation evidence requires PROVED",
        )
    freeze = document["freeze"]
    if freeze["status"] != "FROZEN":
        _add(
            errors,
            "CHECK_REQUIRES_FROZEN_CONTRACT",
            "checked approximation evidence requires a frozen contract",
        )
    elif freeze.get("contract_sha256") != contract_sha256(contract):
        _add(errors, "FREEZE_HASH_MISMATCH", "contract hash")
    domain = contract["source_domain"]
    if domain["kind"] != "finite_explicit" or domain["status"] != "EXPLICIT":
        _add(
            errors,
            "CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN",
            "finite explicit domain required",
        )
    if contract["required_behavior"]["status"] != "EXPLICIT":
        _add(
            errors,
            "CHECK_REQUIRES_EXPLICIT_BEHAVIOR",
            "checked approximation evidence requires explicit required behavior",
        )
    if contract["representation"]["status"] != "EXPLICIT":
        _add(
            errors,
            "CHECK_REQUIRES_EXPLICIT_REPRESENTATION",
            "checked approximation evidence requires explicit representation",
        )
    case_ids = [str(case["id"]) for case in domain["cases"]]
    if len(case_ids) != len(set(case_ids)):
        _add(errors, "DUPLICATE_DOMAIN_CASE", "source-domain case ids must be unique")
    behavior = _case_table(contract["required_behavior"]["table"], "behavior", errors)
    representation = _case_table(contract["representation"]["table"], "representation", errors)
    if set(behavior) != set(case_ids) or set(representation) != set(case_ids):
        _add(
            errors,
            "CASE_TABLE_COVERAGE_MISMATCH",
            "behavior and representation must cover the domain exactly",
        )
    if approximation is None or errors:
        return Result(tuple(errors))

    weights: dict[str, Fraction] = {}
    for row in approximation["reference"]["weights"]:
        case_id = str(row["case_id"])
        if case_id in weights:
            _add(errors, "DUPLICATE_REFERENCE_CASE", case_id)
        weights[case_id] = _fraction(row["weight"])
    if set(weights) != set(case_ids):
        _add(errors, "REFERENCE_COVERAGE_MISMATCH", "reference must cover every case exactly")
    if any(weight < 0 for weight in weights.values()) or sum(weights.values()) != 1:
        _add(
            errors,
            "REFERENCE_NOT_PROBABILITY",
            "reference weights must be nonnegative and sum to one",
        )

    metric_values = _unique_values(
        approximation["metric"]["values"], "METRIC_VALUE", errors
    )
    metric: dict[tuple[str, str], Fraction] = {}
    for row in approximation["metric"]["entries"]:
        pair = (_key(row["left"]), _key(row["right"]))
        if pair in metric:
            _add(errors, "DUPLICATE_METRIC_ENTRY", str(pair))
        metric[pair] = _fraction(row["distance"])
    expected_metric = {(left, right) for left in metric_values for right in metric_values}
    if set(metric) != expected_metric:
        _add(errors, "METRIC_NOT_TOTAL", "metric must cover declared values exactly")
    else:
        for left in metric_values:
            if metric[left, left] != 0:
                _add(errors, "METRIC_IDENTITY_FAILURE", left)
            for right in metric_values:
                if metric[left, right] != metric[right, left]:
                    _add(errors, "METRIC_SYMMETRY_FAILURE", f"{left},{right}")
                if left != right and metric[left, right] == 0:
                    _add(errors, "METRIC_SEPARATION_FAILURE", f"{left},{right}")
                for middle in metric_values:
                    if metric[left, right] > metric[left, middle] + metric[middle, right]:
                        _add(
                            errors,
                            "METRIC_TRIANGLE_FAILURE",
                            f"{left},{middle},{right}",
                        )

    actions = _unique_values(approximation["loss"]["actions"], "LOSS_ACTION", errors)
    truths = {_key(value) for value in behavior.values()}
    loss: dict[tuple[str, str], Fraction] = {}
    for row in approximation["loss"]["entries"]:
        pair = (_key(row["truth"]), _key(row["action"]))
        if pair in loss:
            _add(errors, "DUPLICATE_LOSS_ENTRY", str(pair))
        loss[pair] = _fraction(row["loss"])
    if set(loss) != {(truth, action) for truth in truths for action in actions}:
        _add(errors, "LOSS_NOT_TOTAL", "loss must cover behavior range x action set exactly")
    for truth in truths:
        for action in actions:
            if (truth, action) not in metric:
                _add(errors, "METRIC_LOSS_DOMAIN_MISMATCH", f"{truth},{action}")
            elif (truth, action) in loss and metric[truth, action] != loss[truth, action]:
                _add(errors, "LOSS_METRIC_MISMATCH", f"{truth},{action}")

    dimensions = [row["id"] for row in approximation["cost_preorder"]["dimensions"]]
    if len(dimensions) != len(set(dimensions)):
        _add(errors, "DUPLICATE_COST_DIMENSION", "cost dimension ids must be unique")
    if errors:
        return Result(tuple(errors))

    candidates: dict[str, dict[str, Fraction]] = {}
    aggregate_loss: dict[str, Fraction] = {}
    exact_recovery: set[str] = set()
    used_representations = {_key(representation[case_id]) for case_id in case_ids}
    for candidate in evidence["candidates"]:
        candidate_id = str(candidate["id"])
        if candidate_id in candidates:
            _add(errors, "DUPLICATE_CANDIDATE", candidate_id)
            continue
        costs: dict[str, Fraction] = {}
        for row in candidate["costs"]:
            dimension_id = str(row["dimension_id"])
            if dimension_id in costs:
                _add(errors, "DUPLICATE_CANDIDATE_COST", f"{candidate_id}:{dimension_id}")
            costs[dimension_id] = _fraction(row["value"])
        if set(costs) != set(dimensions):
            _add(errors, "COST_COVERAGE_MISMATCH", candidate_id)

        decoder: dict[str, dict[str, Fraction]] = {}
        for row in candidate["decoder_table"]:
            representation_key = _key(row["representation_value"])
            if representation_key in decoder:
                _add(errors, "DUPLICATE_DECODER_ENTRY", candidate_id)
            distribution: dict[str, Fraction] = {}
            for item in row["distribution"]:
                action_key = _key(item["action"])
                if action_key in distribution:
                    _add(errors, "DUPLICATE_DECODER_ACTION", f"{candidate_id}:{action_key}")
                distribution[action_key] = _fraction(item["probability"])
            if set(distribution) - set(actions):
                _add(errors, "DECODER_UNKNOWN_ACTION", candidate_id)
            if any(value < 0 for value in distribution.values()) or sum(distribution.values()) != 1:
                _add(errors, "DECODER_NOT_PROBABILITY", candidate_id)
            decoder[representation_key] = distribution
        if set(decoder) != used_representations:
            _add(errors, "DECODER_COVERAGE_MISMATCH", candidate_id)

        if errors:
            # No malformed candidate may participate in a frontier calculation.
            continue
        per_case: list[tuple[Fraction, Fraction]] = []
        candidate_exact_on_support = True
        for case_id in case_ids:
            truth = _key(behavior[case_id])
            distribution = decoder[_key(representation[case_id])]
            case_loss = sum(
                (probability * loss[truth, action] for action, probability in distribution.items()),
                Fraction(),
            )
            per_case.append((weights[case_id], case_loss))
            case_is_in_exact_support = (
                approximation["aggregation"] == "maximum" or weights[case_id] > 0
            )
            if case_is_in_exact_support:
                candidate_exact_on_support = candidate_exact_on_support and case_loss == 0
        if approximation["aggregation"] == "maximum":
            aggregate = max(value for _weight, value in per_case)
        else:
            aggregate = sum((weight * value for weight, value in per_case), Fraction())
        aggregate_loss[candidate_id] = aggregate
        candidates[candidate_id] = costs
        if candidate_exact_on_support:
            exact_recovery.add(candidate_id)
    if errors:
        return Result(tuple(errors))

    tolerance = _fraction(approximation["tolerance"])
    feasible = {
        candidate_id
        for candidate_id, candidate_loss in aggregate_loss.items()
        if candidate_loss <= tolerance
    }

    def below(left: str, right: str) -> bool:
        return all(candidates[left][dimension] <= candidates[right][dimension] for dimension in dimensions)

    pareto = {
        candidate_id
        for candidate_id in feasible
        if not any(
            other != candidate_id
            and below(other, candidate_id)
            and not below(candidate_id, other)
            for other in feasible
        )
    }
    least = {
        candidate_id
        for candidate_id in feasible
        if all(below(candidate_id, other) for other in feasible)
    }
    claims = (
        ("claimed_feasible", feasible, "FEASIBLE_SET_MISMATCH"),
        ("claimed_pareto_minimal", pareto, "PARETO_SET_MISMATCH"),
        ("claimed_least_elements", least, "LEAST_SET_MISMATCH"),
        ("exact_recovery_claims", exact_recovery, "EXACT_RECOVERY_SET_MISMATCH"),
    )
    for field, computed, code in claims:
        claimed = set(evidence[field])
        if claimed != computed:
            _add(errors, code, f"claimed={sorted(claimed)} computed={sorted(computed)}")
    if tolerance == 0 and feasible != exact_recovery:
        _add(
            errors,
            "ZERO_TOLERANCE_EXACT_BOUNDARY_FAILURE",
            "zero tolerance feasible set must equal exact recovery set",
        )
    return Result(tuple(errors))


def load_and_validate(path: str | Path) -> Result:
    try:
        return validate_contract(json.loads(Path(path).read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as error:
        return Result((Diagnostic("UNREADABLE_CONTRACT", str(error)),))


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="python -m mechanization.far_mechanization.contract_v21"
    )
    parser.add_argument("path")
    args = parser.parse_args(argv)
    result = load_and_validate(args.path)
    print("PASS" if result.success else "FAIL")
    for diagnostic in result.diagnostics:
        print(f"{diagnostic.code}: {diagnostic.message}")
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
