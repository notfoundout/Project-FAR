"""Independent finite evaluator for the many-sorted relational candidate."""
from __future__ import annotations

import copy
import json
import sys
from fractions import Fraction

SIGNATURE_VERSION = "many-sorted-relational/1.0"
SORTS = ("Entity", "Token", "Meaning", "Rule", "State", "Event", "Objective", "Condition", "Relation")
OPCODES = {
    "transition", "bayes", "derive", "retract", "assert", "query", "equation", "intervene",
    "increment", "replace_increment", "interpret", "classify", "merge_preserve", "quotient",
    "delete_constraint", "observe", "before", "prove", "bind", "authorize",
}


def validate(model):
    errors = []
    if model.get("candidate") != "many-sorted-relational":
        errors.append("candidate tag mismatch")
    if not isinstance(model.get("rules"), list):
        errors.append("rules must be a finite list")
        return errors
    seen = set()
    for rule in model["rules"]:
        if set(rule) != {"id", "opcode", "arguments"}:
            errors.append("ill-formed typed rule")
            continue
        if rule["id"] in seen:
            errors.append("duplicate rule identity")
        seen.add(rule["id"])
        if rule["opcode"] not in OPCODES or not isinstance(rule["arguments"], dict):
            errors.append(f"undeclared opcode: {rule.get('opcode')}")
    return errors


def _fraction(pair):
    return Fraction(pair[0], pair[1])


def _run(initial, rules, least_fixed_point=True):
    state = copy.deepcopy(initial)
    steps = []
    transitions = [rule for rule in rules if rule["opcode"] == "transition"]
    if transitions:
        reachable = set(state.get("states", []))
        # Finite least fixed point: rule tuple ordering cannot change reachability.
        changed = True
        while changed:
            changed = False
            for rule in transitions:
                args = rule["arguments"]
                if args["source"] in reachable and args["target"] not in reachable:
                    reachable.add(args["target"])
                    steps.append(rule["id"])
                    changed = True
            if not least_fixed_point:
                break
        state["states"] = sorted(reachable)
    for rule in rules:
        opcode, args = rule["opcode"], rule["arguments"]
        if opcode == "transition":
            continue
        if opcode == "bayes":
            nums = {key: _fraction(args["prior"][key]) * _fraction(args["likelihood"][key]) for key in args["prior"]}
            total = sum(nums.values(), Fraction(0, 1)); state["posterior"] = {key: str(value / total) for key, value in sorted(nums.items())}
        elif opcode == "derive":
            facts = set(state.setdefault("facts", []))
            if args["premise"] in facts: facts.add(args["conclusion"])
            state["facts"] = sorted(facts)
        elif opcode == "retract": state["facts"] = sorted(set(state.setdefault("facts", [])) - {args["proposition"]})
        elif opcode == "assert": state["facts"] = sorted(set(state.setdefault("facts", [])) | {args["proposition"]})
        elif opcode == "query":
            facts = set(state.setdefault("facts", [])); state["query"] = {"proposition": args["proposition"], "entailed": args["proposition"] in facts, "explosion": args["explosion"]}
        elif opcode == "equation":
            state.setdefault("equations", {})[args["target"]] = args["source"]; state.setdefault("variables", {})[args["target"]] = state["variables"][args["source"]]
        elif opcode == "intervene":
            state.setdefault("variables", {})[args["variable"]] = args["value"]
            for target, source in state.get("equations", {}).items(): state["variables"][target] = state["variables"][source]
        elif opcode == "increment": state["value"] += state["increment"]; state.setdefault("results", []).append(state["value"])
        elif opcode == "replace_increment": state["increment"] = args["value"]
        elif opcode == "interpret": state.setdefault("interpretations", {})[args["token"]] = args["meaning"]; state.setdefault("meaning_history", []).append([args["token"], args["meaning"]])
        elif opcode == "classify":
            state.setdefault("classifications", []).append([args["ontology"], args["entity"], args["category"]]); categories = {row[2] for row in state["classifications"] if row[1] == args["entity"]}; state["conflict"] = len(categories) > 1
        elif opcode == "merge_preserve":
            rows = args["records"]
            state["records"] = [{"id": value, "value": value} for value in rows] if rows and isinstance(rows[0], str) else copy.deepcopy(rows)
        elif opcode == "quotient":
            rep = args["representative"]; state["records"] = [row for row in state.get("records", []) if row["id"] == rep]; state["quotient"] = {alias: rep for alias in args["aliases"]}
        elif opcode == "delete_constraint": state["constraints"] = [x for x in state.get("constraints", []) if x != args["constraint"]]
        elif opcode == "observe": state.setdefault("observations", []).append({"source": args.get("source", "quotiented"), "value": args["value"]})
        elif opcode == "before":
            state.setdefault("before", []).append([args["earlier"], args["later"]]); events = set(state.get("events", [])); earlier = {x for x, _ in state["before"]}; later = {y for _, y in state["before"]}; state["minimal"] = sorted(events - later); state["maximal"] = sorted(events - earlier)
        elif opcode == "prove": state.setdefault("proofs", []).append({"id": args.get("proof_id", args["formula"]), "formula": args["formula"]})
        elif opcode == "bind": state.setdefault("bindings", {})[args["variable"]] = args["scope"]
        elif opcode == "authorize": state["authorization"] = {"source": args["source"], "claim": args["claim"], "admissible": state.get("authorities", {}).get(args["source"]) == "valid"}
        steps.append(rule["id"])
    return {"status": "Pass", "state": state, "steps": steps}


def execute(model):
    errors = validate(model)
    if errors:
        return {"status": "Fail", "errors": errors, "steps": []}
    return _run(model.get("initial", {}), model["rules"], model.get("least_fixed_point", True))


def _structural(rules):
    return {
        "instruction_ids": [rule["id"] for rule in rules],
        "opcodes": [rule["opcode"] for rule in rules],
        "identity_bearing_arguments": [
            copy.deepcopy(rule["arguments"])
            for rule in rules
            if rule["opcode"] in {"merge_preserve", "observe", "prove"}
        ],
    }


def recover(model, execution):
    rules = copy.deepcopy(model["rules"])
    return {
        "commitments": {
            "structural": _structural(rules),
            "semantic": copy.deepcopy(model.get("semantic_relations", {})),
            "operational": {"initial": copy.deepcopy(model.get("initial", {})), "instructions": rules},
            "dependency": copy.deepcopy(model.get("dependency_relations", [])),
            "information": copy.deepcopy(model.get("information_relations", {})),
            "historical": copy.deepcopy(model.get("history_relations", [])),
        },
        "result": copy.deepcopy(execution),
    }


def ablate(model, construct):
    out = copy.deepcopy(model)
    if construct == "identity":
        for index, rule in enumerate(out.get("rules", [])): rule["id"] = f"rule-{index}"
    elif construct == "composition": out["least_fixed_point"] = False
    elif construct == "interpretation": out["rules"] = [r for r in out.get("rules", []) if r["opcode"] != "interpret"]; out["semantic_relations"] = {}
    elif construct == "execution": out["rules"] = []
    elif construct == "history": out["history_relations"] = []
    elif construct == "ordering": out["rules"] = [r for r in out.get("rules", []) if r["opcode"] != "before"]; out["history_relations"] = [{"id": row.get("id"), "after": None} for row in out.get("history_relations", [])]
    elif construct == "source-representation-separation":
        out["semantic_relations"] = {str(k): str(k) for k in out.get("semantic_relations", {})}
    return out


def account(model):
    rules = model.get("rules", [])
    return {
        "native": len(rules) + len(model.get("dependency_relations", [])),
        "derived": sum(r["opcode"] not in {"transition", "derive", "retract", "assert", "query"} for r in rules),
        "identity": len({r["id"] for r in rules}),
        "interpretation": sum(r["opcode"] == "interpret" for r in rules),
        "execution": len(rules),
        "history": len(model.get("history_relations", [])),
        "ordering": sum(r["opcode"] == "before" for r in rules),
        "external": 0,
        "opaque": 0,
        "repair": sum(r["opcode"] in {"merge_preserve", "prove"} for r in rules),
        "reconstruction": 6,
    }


def main():
    model = json.load(sys.stdin); print(json.dumps(execute(model), sort_keys=True)); return bool(validate(model))


if __name__ == "__main__":
    raise SystemExit(main())
