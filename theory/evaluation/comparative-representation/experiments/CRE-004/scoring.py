"""Deterministic scoring for CRE-004 evaluator responses."""

from __future__ import annotations

from typing import Any, Mapping


FUNCTION_LABELS = {
    "stores_objects",
    "organizes_objects",
    "assigns_meaning",
    "defines_objective",
    "determines_permitted_steps",
}
VALID_DIFFERENCE_VALUES = {"yes", "no", "cannot_determine"}
VALID_CONFIDENCE_VALUES = {"certain", "likely", "unsure"}
VALID_CARRIERS = FUNCTION_LABELS | {"other", "cannot_determine"}
VALID_OTHER_FUNCTIONS = FUNCTION_LABELS | {"none", "cannot_determine"}


def _require_choice(response: Mapping[str, Any], key: str, allowed: set[str]) -> str:
    value = response.get(key)
    if value not in allowed:
        raise ValueError(f"{key} must be one of {sorted(allowed)}")
    return value


def score_response(response: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and score one response using only frozen decision rules."""

    source = _require_choice(response, "source_difference", VALID_DIFFERENCE_VALUES)
    translated = _require_choice(response, "translated_difference", VALID_DIFFERENCE_VALUES)
    confidence = _require_choice(response, "confidence", VALID_CONFIDENCE_VALUES)

    raw_carriers = response.get("difference_carriers", [])
    if not isinstance(raw_carriers, list) or len(raw_carriers) != len(set(raw_carriers)):
        raise ValueError("difference_carriers must be a list of unique choices")
    carriers = set(raw_carriers)
    if not carriers <= VALID_CARRIERS:
        raise ValueError("difference_carriers contains an unregistered choice")

    if translated == "yes" and not carriers:
        raise ValueError("a distinguishable translation requires at least one carrier")
    if translated != "yes" and carriers:
        raise ValueError("difference carriers are only allowed when translated_difference=yes")
    if "cannot_determine" in carriers and len(carriers) > 1:
        raise ValueError("cannot_determine cannot be combined with another carrier")

    other_function = response.get("other_function")
    if "other" in carriers:
        if other_function not in VALID_OTHER_FUNCTIONS:
            raise ValueError("other requires a registered other_function response")
    elif other_function is not None:
        raise ValueError("other_function is only allowed when other is selected")

    if "other" in carriers and other_function == "cannot_determine":
        hidden_reintroduction: bool | str = "unknown"
    elif "other" in carriers and other_function in FUNCTION_LABELS:
        hidden_reintroduction = True
    else:
        hidden_reintroduction = False

    if source == "no":
        classification = "invalid_case_response"
    elif source == "cannot_determine" or translated == "cannot_determine":
        classification = "unknown"
    elif translated == "no":
        classification = "fail"
    elif "cannot_determine" in carriers:
        classification = "unknown"
    elif "other" in carriers and other_function == "cannot_determine":
        classification = "unknown"
    else:
        classification = "pass"

    return {
        "classification": classification,
        "hidden_reintroduction": hidden_reintroduction,
        "functional_carriers": sorted(carriers & FUNCTION_LABELS),
        "confidence": confidence,
        "confidence_affects_score": False,
    }
