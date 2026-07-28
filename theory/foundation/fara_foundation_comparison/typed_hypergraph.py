"""Independent finite evaluator for the typed-hypergraph candidate."""
from __future__ import annotations

import copy
import json
import sys
from fractions import Fraction

SIGNATURE_VERSION = "typed-hypergraph/1.0"
NODE_TYPES = ("instruction", "entity", "token", "meaning", "rule", "state", "objective", "condition")
EDGE_TYPES = {
    "transition", "bayes", "derive", "retract", "assert", "query", "equation", "intervene",
    "increment", "replace_increment", "interpret", "classify", "merge_preserve", "quotient",
    "delete_constraint", "observe", "before", "prove", "bind", "authorize",
}


def validate(model):
    errors = []
    if model.get("candidate") != "typed-hypergraph": errors.append("candidate tag mismatch")
    nodes = model.get("nodes", {})
    if any(node_type not in NODE_TYPES for node_type in nodes.values()): errors.append("undeclared node type")
    seen = set()
    for edge in model.get("edges", []):
        if set(edge) != {"id", "type", "arguments"}: errors.append("ill-formed hyperedge"); continue
        if edge["id"] in seen: errors.append("duplicate edge identity")
        seen.add(edge["id"])
        if edge["id"] not in nodes: errors.append("edge identity lacks node declaration")
        if edge["type"] not in EDGE_TYPES or not isinstance(edge["arguments"], dict): errors.append(f"undeclared edge type: {edge.get('type')}")
    return errors


def _fraction(pair): return Fraction(pair[0], pair[1])


def _run(initial, edges, path_closure=True):
    state = copy.deepcopy(initial); steps = []
    transitions = [edge for edge in edges if edge["type"] == "transition"]
    if transitions:
        reachable = set(state.get("states", [])); changed = True
        while changed:
            changed = False
            for edge in transitions:
                args = edge["arguments"]
                if args["source"] in reachable and args["target"] not in reachable:
                    reachable.add(args["target"]); steps.append(edge["id"]); changed = True
            if not path_closure:
                break
        state["states"] = sorted(reachable)
    for edge in edges:
        opcode, args = edge["type"], edge["arguments"]
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
        steps.append(edge["id"])
    return {"status": "Pass", "state": state, "steps": steps}


def execute(model):
    errors = validate(model)
    if errors: return {"status": "Fail", "errors": errors, "steps": []}
    return _run(model.get("initial", {}), model.get("edges", []), model.get("path_closure", True))


def _instructions(edges):
    return [{"id": edge["id"], "opcode": edge["type"], "arguments": copy.deepcopy(edge["arguments"])} for edge in edges]


def recover(model, execution):
    instructions = _instructions(model.get("edges", []))
    return {
        "commitments": {
            "structural": {"instruction_ids": [x["id"] for x in instructions], "opcodes": [x["opcode"] for x in instructions], "identity_bearing_arguments": [copy.deepcopy(x["arguments"]) for x in instructions if x["opcode"] in {"merge_preserve", "observe", "prove"}]},
            "semantic": copy.deepcopy(model.get("semantic_nodes", {})),
            "operational": {"initial": copy.deepcopy(model.get("initial", {})), "instructions": instructions},
            "dependency": copy.deepcopy(model.get("dependency_edges", [])),
            "information": copy.deepcopy(model.get("information_nodes", {})),
            "historical": copy.deepcopy(model.get("history_edges", [])),
        },
        "result": copy.deepcopy(execution),
    }


def ablate(model, construct):
    out = copy.deepcopy(model)
    if construct == "identity":
        for index, edge in enumerate(out.get("edges", [])):
            old = edge["id"]; new = f"edge-{index}"; edge["id"] = new; out.get("nodes", {}).pop(old, None); out.setdefault("nodes", {})[new] = "instruction"
    elif construct == "composition": out["path_closure"] = False
    elif construct == "interpretation": out["edges"] = [edge for edge in out.get("edges", []) if edge["type"] != "interpret"]; out["semantic_nodes"] = {}
    elif construct == "execution": out["edges"] = []; out["nodes"] = {key: value for key, value in out.get("nodes", {}).items() if value != "instruction"}
    elif construct == "history": out["history_edges"] = []
    elif construct == "ordering": out["edges"] = [edge for edge in out.get("edges", []) if edge["type"] != "before"]; out["history_edges"] = [{"id": row.get("id"), "after": None} for row in out.get("history_edges", [])]
    elif construct == "source-representation-separation": out["semantic_nodes"] = {str(key): str(key) for key in out.get("semantic_nodes", {})}
    return out


def account(model):
    edges = model.get("edges", []); nodes = model.get("nodes", {})
    return {
        "native": len(nodes) + len(edges) * 2,
        "derived": sum(edge["type"] in {"transition", "before", "equation"} for edge in edges),
        "identity": len({edge["id"] for edge in edges}),
        "interpretation": sum(edge["type"] == "interpret" for edge in edges),
        "execution": len(edges),
        "history": len(model.get("history_edges", [])),
        "ordering": sum(edge["type"] == "before" for edge in edges),
        "external": 1 if any(edge["type"] == "transition" for edge in edges) else 0,
        "opaque": 0,
        "repair": 0,
        "reconstruction": len(edges) + 6,
    }


def main():
    model = json.load(sys.stdin); print(json.dumps(execute(model), sort_keys=True)); return bool(validate(model))


if __name__ == "__main__": raise SystemExit(main())
