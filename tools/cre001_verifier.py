from __future__ import annotations

import argparse
import copy
import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any

Json = dict[str, Any]


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    trace: tuple[str, ...] = ()
    details: Json | None = None

    def as_dict(self) -> Json:
        result: Json = {"code": self.code, "message": self.message, "trace": list(self.trace)}
        if self.details is not None:
            result["details"] = self.details
        return result


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_model(model: Json) -> None:
    _require(model.get("format") == "cre001-execution-model-v1", "unsupported model format")
    _require(isinstance(model.get("variables"), dict) and model["variables"], "variables must be a nonempty object")
    _require(isinstance(model.get("transitions"), list) and model["transitions"], "transitions must be a nonempty array")
    _require(isinstance(model.get("outputs"), dict), "outputs must be an object")
    names: set[str] = set()
    variables = model["variables"]
    for name, spec in variables.items():
        _require(isinstance(name, str) and name, "variable names must be nonempty strings")
        _require(isinstance(spec, dict) and "initial" in spec, f"variable {name} requires initial")
        _require(spec.get("type") in {"boolean", "history"}, f"variable {name} has unsupported type")
        if spec["type"] == "boolean":
            _require(isinstance(spec["initial"], bool), f"variable {name} must have boolean initial value")
        else:
            _require(spec["initial"] == [], f"history variable {name} must start empty")
    for transition in model["transitions"]:
        _require(isinstance(transition, dict), "each transition must be an object")
        name = transition.get("name")
        _require(isinstance(name, str) and name and name not in names, "transition names must be unique nonempty strings")
        names.add(name)
        _require(isinstance(transition.get("guard", []), list), f"transition {name} guard must be an array")
        _require(isinstance(transition.get("guard_any", []), list), f"transition {name} guard_any must be an array")
        _require(isinstance(transition.get("updates", []), list), f"transition {name} updates must be an array")
        for condition in transition.get("guard", []) + transition.get("guard_any", []):
            _require(condition.get("variable") in variables, f"transition {name} guard references unknown variable")
            _require("equals" in condition, f"transition {name} guard condition requires equals")
        for update in transition.get("updates", []):
            _require(update.get("variable") in variables, f"transition {name} update references unknown variable")
            _require(update.get("operation") in {"set", "append"}, f"transition {name} has unsupported update operation")
            if update["operation"] == "append":
                _require(variables[update["variable"]]["type"] == "history", f"transition {name} append target must be history")
    terminal = model.get("terminal_condition")
    _require(isinstance(terminal, dict) and terminal.get("variable") in variables and "equals" in terminal, "invalid terminal condition")
    for output_name, output in model["outputs"].items():
        _require(isinstance(output, dict), f"output {output_name} must be an object")
        _require(output.get("kind") in {"variable", "status"}, f"output {output_name} has unsupported kind")
        if output["kind"] == "variable":
            _require(output.get("variable") in variables, f"output {output_name} references unknown variable")
        else:
            for variable in output.get("variables", []):
                _require(variable in variables, f"output {output_name} references unknown status variable")


def initial_state(model: Json) -> Json:
    return {name: copy.deepcopy(spec["initial"]) for name, spec in model["variables"].items()}


def _state_key(state: Json, variable_order: tuple[str, ...]) -> tuple[Any, ...]:
    values: list[Any] = []
    for name in variable_order:
        value = state[name]
        values.append(tuple(value) if isinstance(value, list) else value)
    return tuple(values)


def is_terminal(model: Json, state: Json) -> bool:
    condition = model["terminal_condition"]
    return state[condition["variable"]] == condition["equals"]


def enabled(model: Json, state: Json, transition: Json) -> bool:
    if is_terminal(model, state) and model.get("terminal_blocks_all_transitions", True):
        return False
    all_guard = all(state[item["variable"]] == item["equals"] for item in transition.get("guard", []))
    any_guard = transition.get("guard_any", [])
    return all_guard and (not any_guard or any(state[item["variable"]] == item["equals"] for item in any_guard))


def apply_transition(state: Json, transition: Json) -> Json:
    result = copy.deepcopy(state)
    for update in transition.get("updates", []):
        variable = update["variable"]
        if update["operation"] == "set":
            if "from" in update and result[variable] != update["from"]:
                raise ValueError(f"transition {transition['name']} expected {variable}={update['from']!r}")
            result[variable] = copy.deepcopy(update["value"])
        else:
            result[variable].append(copy.deepcopy(update["value"]))
    return result


def transition_map(model: Json) -> dict[str, Json]:
    return {transition["name"]: transition for transition in model["transitions"]}


def compare_schema(reference: Json, candidate: Json) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    ref_variables = reference["variables"]
    cand_variables = candidate["variables"]
    for name in sorted(set(ref_variables) - set(cand_variables)):
        diagnostics.append(Diagnostic("missing_variable", f"candidate is missing variable {name}", details={"variable": name}))
    for name in sorted(set(cand_variables) - set(ref_variables)):
        diagnostics.append(Diagnostic("extra_variable", f"candidate adds variable {name}", details={"variable": name}))
    for name in sorted(set(ref_variables) & set(cand_variables)):
        if ref_variables[name] != cand_variables[name]:
            diagnostics.append(Diagnostic("variable_mismatch", f"variable {name} differs", details={"reference": ref_variables[name], "candidate": cand_variables[name]}))
    ref_transitions = transition_map(reference)
    cand_transitions = transition_map(candidate)
    for name in sorted(set(ref_transitions) - set(cand_transitions)):
        diagnostics.append(Diagnostic("missing_transition", f"candidate is missing transition {name}", details={"transition": name}))
    for name in sorted(set(cand_transitions) - set(ref_transitions)):
        diagnostics.append(Diagnostic("extra_transition", f"candidate adds transition {name}", details={"transition": name}))
    for name in sorted(set(ref_transitions) & set(cand_transitions)):
        ref_transition = ref_transitions[name]
        cand_transition = cand_transitions[name]
        if (ref_transition.get("guard", []), ref_transition.get("guard_any", [])) != (cand_transition.get("guard", []), cand_transition.get("guard_any", [])):
            diagnostics.append(Diagnostic("guard_mismatch", f"guard differs for {name}", details={"reference": {"all": ref_transition.get("guard", []), "any": ref_transition.get("guard_any", [])}, "candidate": {"all": cand_transition.get("guard", []), "any": cand_transition.get("guard_any", [])}}))
        if ref_transition.get("updates", []) != cand_transition.get("updates", []):
            diagnostics.append(Diagnostic("update_mismatch", f"updates differ for {name}", details={"reference": ref_transition.get("updates", []), "candidate": cand_transition.get("updates", [])}))
    defaults = {
        "terminal_blocks_all_transitions": True,
        "invariants": [],
        "ambiguity_policy": {},
    }
    for field, code in (("terminal_condition", "terminal_condition_mismatch"), ("terminal_blocks_all_transitions", "terminal_policy_mismatch"), ("outputs", "output_mismatch"), ("invariants", "invariant_mismatch"), ("ambiguity_policy", "ambiguity_policy_mismatch")):
        ref_value = reference.get(field, defaults.get(field, {}))
        cand_value = candidate.get(field, defaults.get(field, {}))
        if ref_value != cand_value:
            diagnostics.append(Diagnostic(code, f"{field} differs", details={"reference": ref_value, "candidate": cand_value}))
    return diagnostics


def shortest_behavioral_counterexample(reference: Json, candidate: Json, max_depth: int = 12) -> Diagnostic | None:
    variable_order = tuple(reference["variables"])
    if tuple(candidate["variables"]) != variable_order:
        return None
    ref_state = initial_state(reference)
    cand_state = initial_state(candidate)
    queue = deque([(ref_state, cand_state, tuple())])
    seen = {(_state_key(ref_state, variable_order), _state_key(cand_state, variable_order))}
    ref_transitions = transition_map(reference)
    cand_transitions = transition_map(candidate)
    common_names = sorted(set(ref_transitions) & set(cand_transitions))
    while queue:
        current_ref, current_cand, trace = queue.popleft()
        ref_enabled = {name for name in common_names if enabled(reference, current_ref, ref_transitions[name])}
        cand_enabled = {name for name in common_names if enabled(candidate, current_cand, cand_transitions[name])}
        if ref_enabled != cand_enabled:
            return Diagnostic("enabled_set_mismatch", "enabled transitions diverge", trace, {"reference_enabled": sorted(ref_enabled), "candidate_enabled": sorted(cand_enabled), "reference_state": current_ref, "candidate_state": current_cand})
        if len(trace) >= max_depth:
            continue
        for name in sorted(ref_enabled):
            try:
                next_ref = apply_transition(current_ref, ref_transitions[name])
            except ValueError as exc:
                return Diagnostic("reference_execution_error", str(exc), trace + (name,))
            try:
                next_cand = apply_transition(current_cand, cand_transitions[name])
            except ValueError as exc:
                return Diagnostic("candidate_execution_error", str(exc), trace + (name,))
            if next_ref != next_cand:
                return Diagnostic("post_state_mismatch", f"state diverges after {name}", trace + (name,), {"reference_state": next_ref, "candidate_state": next_cand})
            key = (_state_key(next_ref, variable_order), _state_key(next_cand, variable_order))
            if key not in seen:
                seen.add(key)
                queue.append((next_ref, next_cand, trace + (name,)))
    return None


def verify(reference: Json, candidate: Json, max_depth: int = 12) -> Json:
    validate_model(reference)
    validate_model(candidate)
    diagnostics = compare_schema(reference, candidate)
    counterexample = shortest_behavioral_counterexample(reference, candidate, max_depth=max_depth)
    if counterexample is not None:
        diagnostics.append(counterexample)
    categories = {
        "structural": not any(item.code in {"missing_variable", "extra_variable", "variable_mismatch", "missing_transition", "extra_transition"} for item in diagnostics),
        "operational": not any(item.code in {"guard_mismatch", "update_mismatch", "terminal_condition_mismatch", "terminal_policy_mismatch", "enabled_set_mismatch", "post_state_mismatch", "candidate_execution_error"} for item in diagnostics),
        "historical": not any(item.code in {"update_mismatch", "post_state_mismatch", "invariant_mismatch"} for item in diagnostics),
        "information": not any(item.code == "output_mismatch" for item in diagnostics),
        "ambiguity_policy": not any(item.code == "ambiguity_policy_mismatch" for item in diagnostics),
    }
    return {
        "verifier": "cre001-deterministic-verifier-v1",
        "result": "pass" if not diagnostics else "fail",
        "max_depth": max_depth,
        "checks": {name: "pass" if passed else "fail" for name, passed in categories.items()},
        "diagnostics": [item.as_dict() for item in diagnostics],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare a CRE-001 candidate execution model with the frozen reference model.")
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--max-depth", type=int, default=12)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    reference = json.loads(args.reference.read_text(encoding="utf-8"))
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    report = verify(reference, candidate, max_depth=args.max_depth)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
