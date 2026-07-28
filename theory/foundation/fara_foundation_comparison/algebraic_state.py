"""Independent finite evaluator for the algebraic/state-transition candidate."""
from __future__ import annotations

import copy
import json
import sys
from fractions import Fraction

SIGNATURE_VERSION = "algebraic-state-transition/1.0"
OPERATION_KINDS = {
    "transition", "bayes", "derive", "retract", "assert", "query", "equation", "intervene",
    "increment", "replace_increment", "interpret", "classify", "merge_preserve", "quotient",
    "delete_constraint", "observe", "before", "prove", "bind", "authorize",
}


def validate(model):
    errors = []
    if model.get("candidate") != "algebraic-state-transition": errors.append("candidate tag mismatch")
    operations = model.get("operations", {})
    for name, operation in operations.items():
        if set(operation) != {"kind", "arguments"}: errors.append(f"ill-formed operation: {name}"); continue
        if operation["kind"] not in OPERATION_KINDS or not isinstance(operation["arguments"], dict): errors.append(f"undeclared operation: {name}")
    if any(name not in operations for name in model.get("program", [])): errors.append("program references undeclared operation")
    return errors


def _fraction(pair): return Fraction(pair[0], pair[1])


def _run(initial, operations, program, iteration_enabled=True):
    state = copy.deepcopy(initial); steps = []
    transition_names = [name for name in program if operations[name]["kind"] == "transition"]
    if transition_names:
        reachable = set(state.get("states", [])); changed = True
        while changed:
            changed = False
            for name in transition_names:
                args = operations[name]["arguments"]
                if args["source"] in reachable and args["target"] not in reachable:
                    reachable.add(args["target"]); steps.append(name); changed = True
            if not iteration_enabled:
                break
        state["states"] = sorted(reachable)
    for name in program:
        operation = operations[name]; opcode, args = operation["kind"], operation["arguments"]
        if opcode == "transition": continue
        if opcode == "bayes":
            nums = {key: _fraction(args["prior"][key]) * _fraction(args["likelihood"][key]) for key in args["prior"]}; total = sum(nums.values(), Fraction(0, 1)); state["posterior"] = {key: str(value / total) for key, value in sorted(nums.items())}
        elif opcode == "derive":
            facts = set(state.setdefault("facts", []));
            if args["premise"] in facts: facts.add(args["conclusion"])
            state["facts"] = sorted(facts)
        elif opcode == "retract": state["facts"] = sorted(set(state.setdefault("facts", [])) - {args["proposition"]})
        elif opcode == "assert": state["facts"] = sorted(set(state.setdefault("facts", [])) | {args["proposition"]})
        elif opcode == "query":
            facts = set(state.setdefault("facts", [])); state["query"] = {"proposition": args["proposition"], "entailed": args["proposition"] in facts, "explosion": args["explosion"]}
        elif opcode == "equation": state.setdefault("equations", {})[args["target"]] = args["source"]; state.setdefault("variables", {})[args["target"]] = state["variables"][args["source"]]
        elif opcode == "intervene":
            state.setdefault("variables", {})[args["variable"]] = args["value"]
            for target, source in state.get("equations", {}).items(): state["variables"][target] = state["variables"][source]
        elif opcode == "increment": state["value"] += state["increment"]; state.setdefault("results", []).append(state["value"])
        elif opcode == "replace_increment": state["increment"] = args["value"]
        elif opcode == "interpret": state.setdefault("interpretations", {})[args["token"]] = args["meaning"]; state.setdefault("meaning_history", []).append([args["token"], args["meaning"]])
        elif opcode == "classify":
            state.setdefault("classifications", []).append([args["ontology"], args["entity"], args["category"]]); categories = {row[2] for row in state["classifications"] if row[1] == args["entity"]}; state["conflict"] = len(categories) > 1
        elif opcode == "merge_preserve":
            rows = args["records"]; state["records"] = [{"id": value, "value": value} for value in rows] if rows and isinstance(rows[0], str) else copy.deepcopy(rows)
        elif opcode == "quotient":
            rep = args["representative"]; state["records"] = [row for row in state.get("records", []) if row["id"] == rep]; state["quotient"] = {alias: rep for alias in args["aliases"]}
        elif opcode == "delete_constraint": state["constraints"] = [x for x in state.get("constraints", []) if x != args["constraint"]]
        elif opcode == "observe": state.setdefault("observations", []).append({"source": args.get("source", "quotiented"), "value": args["value"]})
        elif opcode == "before":
            state.setdefault("before", []).append([args["earlier"], args["later"]]); events = set(state.get("events", [])); earlier = {x for x, _ in state["before"]}; later = {y for _, y in state["before"]}; state["minimal"] = sorted(events - later); state["maximal"] = sorted(events - earlier)
        elif opcode == "prove": state.setdefault("proofs", []).append({"id": args.get("proof_id", args["formula"]), "formula": args["formula"]})
        elif opcode == "bind": state.setdefault("bindings", {})[args["variable"]] = args["scope"]
        elif opcode == "authorize": state["authorization"] = {"source": args["source"], "claim": args["claim"], "admissible": state.get("authorities", {}).get(args["source"]) == "valid"}
        steps.append(name)
    return {"status": "Pass", "state": state, "steps": steps}


def execute(model):
    errors = validate(model)
    if errors: return {"status": "Fail", "errors": errors, "steps": []}
    return _run(model.get("initial", {}), model.get("operations", {}), model.get("program", []), model.get("iteration_enabled", True))


def _instructions(model):
    return [
        {"id": name, "opcode": model["operations"][name]["kind"], "arguments": copy.deepcopy(model["operations"][name]["arguments"])}
        for name in model.get("program", [])
    ]


def recover(model, execution):
    instructions = _instructions(model)
    return {
        "commitments": {
            "structural": {"instruction_ids": [x["id"] for x in instructions], "opcodes": [x["opcode"] for x in instructions], "identity_bearing_arguments": [copy.deepcopy(x["arguments"]) for x in instructions if x["opcode"] in {"merge_preserve", "observe", "prove"}]},
            "semantic": copy.deepcopy(model.get("semantic_map", {})),
            "operational": {"initial": copy.deepcopy(model.get("initial", {})), "instructions": instructions},
            "dependency": copy.deepcopy(model.get("dependency_map", [])),
            "information": copy.deepcopy(model.get("information_map", {})),
            "historical": copy.deepcopy(model.get("history", [])),
        },
        "result": copy.deepcopy(execution),
    }


def ablate(model, construct):
    out = copy.deepcopy(model)
    if construct == "identity":
        renamed = {}; program = []
        for index, name in enumerate(out.get("program", [])):
            new = f"op-{index}"; renamed[new] = out["operations"][name]; program.append(new)
        out["operations"] = renamed; out["program"] = program
    elif construct == "composition": out["iteration_enabled"] = False
    elif construct == "interpretation":
        keep = [name for name in out.get("program", []) if out["operations"][name]["kind"] != "interpret"]
        out["operations"] = {name: out["operations"][name] for name in keep}; out["program"] = keep; out["semantic_map"] = {}
    elif construct == "execution": out["operations"] = {}; out["program"] = []
    elif construct == "history": out["history"] = []
    elif construct == "ordering":
        keep = [name for name in out.get("program", []) if out["operations"][name]["kind"] != "before"]
        out["operations"] = {name: out["operations"][name] for name in keep}; out["program"] = keep; out["history"] = [{"id": row.get("id"), "after": None} for row in out.get("history", [])]
    elif construct == "source-representation-separation": out["semantic_map"] = {str(key): str(key) for key in out.get("semantic_map", {})}
    return out


def account(model):
    operations = model.get("operations", {}); program = model.get("program", [])
    return {
        "native": len(operations) + len(program),
        "derived": sum(operation["kind"] not in {"transition", "increment", "replace_increment", "quotient"} for operation in operations.values()),
        "identity": len(operations),
        "interpretation": sum(operation["kind"] == "interpret" for operation in operations.values()),
        "execution": len(program),
        "history": len(model.get("history", [])),
        "ordering": sum(operation["kind"] == "before" for operation in operations.values()),
        "external": 0,
        "opaque": 0,
        "repair": sum(operation["kind"] in {"observe", "prove", "merge_preserve"} for operation in operations.values()),
        "reconstruction": len(operations) + 7,
    }


def main():
    model = json.load(sys.stdin); print(json.dumps(execute(model), sort_keys=True)); return bool(validate(model))


if __name__ == "__main__": raise SystemExit(main())
