"""Executable identity-bearing many-sorted relational kernel for FARA v1.0."""
from __future__ import annotations

import copy
import hashlib
import json
from collections import defaultdict

KERNEL_VERSION = "fara-identity-bearing-many-sorted-relational/1.0"

SORTS = (
    "Object",
    "Representation",
    "Meaning",
    "Interpretation",
    "ReasoningCalculus",
    "Rule",
    "State",
    "Event",
    "Investigation",
    "Objective",
    "Condition",
    "RelationType",
    "RelationOccurrence",
    "Role",
    "Provenance",
)

RELATION_SIGNATURES = {
    "denotes": ("Representation", "Object"),
    "assigns": ("Interpretation", "Representation", "Meaning"),
    "contains_rule": ("ReasoningCalculus", "Rule"),
    "applies": ("Event", "Rule"),
    "input_state": ("Event", "State"),
    "output_state": ("Event", "State"),
    "occurs_in": ("Event", "Investigation"),
    "uses_calculus": ("Investigation", "ReasoningCalculus"),
    "objective_of": ("Investigation", "Objective"),
    "condition_of": ("Investigation", "Condition"),
    "instance_of": ("RelationOccurrence", "RelationType"),
    "participant": ("RelationOccurrence", "Role", "Object"),
    "precedes": ("Event", "Event"),
    "provenance_of": ("Event", "Provenance"),
    "represents_event": ("Representation", "Event"),
}

MANDATORY_GATES = (
    "representation_object_separation",
    "rule_execution_result_separation",
    "interpretation_separation",
    "calculus_independence",
    "architecture_operation_separation",
    "identity_bearing_occurrences",
    "explicit_provenance_and_order",
    "encoding_neutrality",
)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def normalized_model(model):
    out = copy.deepcopy(model)
    for sort_name in SORTS:
        out["sorts"][sort_name] = sorted(out["sorts"][sort_name])
    for relation_name in RELATION_SIGNATURES:
        out["relations"][relation_name] = sorted(
            out["relations"][relation_name], key=canonical
        )
    return out


def empty_model():
    return {
        "kernel_version": KERNEL_VERSION,
        "sorts": {name: [] for name in SORTS},
        "relations": {name: [] for name in RELATION_SIGNATURES},
    }


def sample_model():
    model = empty_model()
    model["sorts"].update(
        {
            "Object": ["source-temperature", "threshold"],
            "Representation": ["token-temp", "sig-e1", "sig-e2"],
            "Meaning": ["temperature-reading"],
            "Interpretation": ["interp-1"],
            "ReasoningCalculus": ["calc-1"],
            "Rule": ["rule-above"],
            "State": ["s0", "s1"],
            "Event": ["e1", "e2"],
            "Investigation": ["inv-1"],
            "Objective": ["decide-threshold"],
            "Condition": ["sensor-calibrated"],
            "RelationType": ["supports"],
            "RelationOccurrence": ["support-1", "support-2"],
            "Role": ["premise", "target"],
            "Provenance": ["sensor-A", "sensor-B"],
        }
    )
    model["relations"].update(
        {
            "denotes": [["token-temp", "source-temperature"]],
            "assigns": [["interp-1", "token-temp", "temperature-reading"]],
            "contains_rule": [["calc-1", "rule-above"]],
            "applies": [["e1", "rule-above"], ["e2", "rule-above"]],
            "input_state": [["e1", "s0"], ["e2", "s0"]],
            "output_state": [["e1", "s1"], ["e2", "s1"]],
            "occurs_in": [["e1", "inv-1"], ["e2", "inv-1"]],
            "uses_calculus": [["inv-1", "calc-1"]],
            "objective_of": [["inv-1", "decide-threshold"]],
            "condition_of": [["inv-1", "sensor-calibrated"]],
            "instance_of": [["support-1", "supports"], ["support-2", "supports"]],
            "participant": [
                ["support-1", "premise", "source-temperature"],
                ["support-1", "target", "threshold"],
                ["support-2", "premise", "source-temperature"],
                ["support-2", "target", "threshold"],
            ],
            "precedes": [["e1", "e2"]],
            "provenance_of": [["e1", "sensor-A"], ["e2", "sensor-B"]],
            "represents_event": [["sig-e1", "e1"], ["sig-e2", "e2"]],
        }
    )
    return model


def validate_model(model):
    errors = []
    if model.get("kernel_version") != KERNEL_VERSION:
        errors.append("kernel version mismatch")
    sorts = model.get("sorts")
    relations = model.get("relations")
    if not isinstance(sorts, dict) or set(sorts) != set(SORTS):
        errors.append("sort registry mismatch")
        return sorted(set(errors))
    if not isinstance(relations, dict) or set(relations) != set(RELATION_SIGNATURES):
        errors.append("relation registry mismatch")
        return sorted(set(errors))

    owner = {}
    for sort_name, members in sorts.items():
        if not isinstance(members, list):
            errors.append(f"{sort_name} carrier is not a list")
            continue
        if len(members) != len(set(members)):
            errors.append(f"duplicate identity in {sort_name}")
        for member in members:
            if not isinstance(member, str) or not member:
                errors.append(f"invalid identity in {sort_name}")
            if member in owner:
                errors.append(f"cross-sort identity collision: {member}")
            owner[member] = sort_name

    for relation_name, signature in RELATION_SIGNATURES.items():
        rows = relations.get(relation_name, [])
        if not isinstance(rows, list):
            errors.append(f"{relation_name} is not a list")
            continue
        if len(rows) != len({tuple(row) for row in rows if isinstance(row, list)}):
            errors.append(f"duplicate extensional fact: {relation_name}")
        for row in rows:
            if not isinstance(row, list) or len(row) != len(signature):
                errors.append(f"wrong arity: {relation_name}")
                continue
            for value, expected_sort in zip(row, signature):
                if value not in sorts[expected_sort]:
                    errors.append(
                        f"ill-typed {relation_name}: {value} not in {expected_sort}"
                    )

    occurrences = set(sorts["RelationOccurrence"])
    typed_occurrences = {row[0] for row in relations["instance_of"] if len(row) == 2}
    participant_occurrences = {
        row[0] for row in relations["participant"] if len(row) == 3
    }
    for occurrence in occurrences:
        if occurrence not in typed_occurrences:
            errors.append(f"untyped relation occurrence: {occurrence}")
        if occurrence not in participant_occurrences:
            errors.append(f"participant-free relation occurrence: {occurrence}")

    events = set(sorts["Event"])
    applied = {row[0] for row in relations["applies"] if len(row) == 2}
    inputs = {row[0] for row in relations["input_state"] if len(row) == 2}
    outputs = {row[0] for row in relations["output_state"] if len(row) == 2}
    investigations = {row[0] for row in relations["occurs_in"] if len(row) == 2}
    for event in events:
        if event not in applied:
            errors.append(f"event without rule: {event}")
        if event not in inputs or event not in outputs:
            errors.append(f"event without explicit input/output state: {event}")
        if event not in investigations:
            errors.append(f"event outside investigation: {event}")

    if _has_cycle(relations["precedes"]):
        errors.append("precedes relation contains a cycle")
    return sorted(set(errors))


def _has_cycle(rows):
    edges = defaultdict(list)
    nodes = set()
    for left, right in rows:
        edges[left].append(right)
        nodes.update((left, right))
    visiting, visited = set(), set()

    def visit(node):
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(next_node) for next_node in edges[node]):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in nodes)


def _topological_events(events, rows):
    incoming = {event: 0 for event in events}
    outgoing = defaultdict(list)
    for left, right in rows:
        outgoing[left].append(right)
        incoming[right] += 1
    ready = sorted(event for event, degree in incoming.items() if degree == 0)
    ordered = []
    while ready:
        event = ready.pop(0)
        ordered.append(event)
        for target in sorted(outgoing[event]):
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
                ready.sort()
    if len(ordered) != len(events):
        raise ValueError("cyclic event order")
    return ordered


def derived_views(model):
    errors = validate_model(model)
    if errors:
        raise ValueError("; ".join(errors))
    relations = model["relations"]
    occurrence_types = {row[0]: row[1] for row in relations["instance_of"]}
    participants = defaultdict(list)
    for occurrence, role, object_id in relations["participant"]:
        participants[occurrence].append([role, object_id])
    properties = [
        occurrence for occurrence, rows in participants.items() if len(rows) == 1
    ]
    semantic_content = [
        {
            "interpretation": interpretation,
            "representation": representation,
            "meaning": meaning,
        }
        for interpretation, representation, meaning in relations["assigns"]
    ]
    transition_signatures = [
        {"representation": representation, "event": event}
        for representation, event in relations["represents_event"]
    ]
    return {
        "properties": sorted(properties),
        "relation_occurrences": [
            {
                "id": occurrence,
                "type": occurrence_types[occurrence],
                "participants": sorted(participants[occurrence]),
            }
            for occurrence in sorted(participants)
        ],
        "semantic_content": sorted(semantic_content, key=canonical),
        "transition_signatures": sorted(transition_signatures, key=canonical),
        "reasoning_trace": _topological_events(
            model["sorts"]["Event"], relations["precedes"]
        ),
    }


def to_typed_hypergraph(model):
    errors = validate_model(model)
    if errors:
        raise ValueError("; ".join(errors))
    nodes = []
    for sort_name in SORTS:
        nodes.extend(
            {"id": member, "type": sort_name}
            for member in model["sorts"][sort_name]
        )
    edges = []
    for relation_name in sorted(RELATION_SIGNATURES):
        for index, row in enumerate(model["relations"][relation_name]):
            edges.append(
                {
                    "id": f"{relation_name}:{index}:{row[0]}",
                    "type": relation_name,
                    "ports": [
                        {"position": position, "node": value, "sort": expected_sort}
                        for position, (value, expected_sort) in enumerate(
                            zip(row, RELATION_SIGNATURES[relation_name])
                        )
                    ],
                    "tuple": copy.deepcopy(row),
                }
            )
    return {
        "view": "typed-hypergraph/derived-1.0",
        "kernel_version": KERNEL_VERSION,
        "nodes": sorted(nodes, key=lambda row: (row["type"], row["id"])),
        "edges": sorted(
            edges,
            key=lambda row: (row["type"], row["id"], canonical(row["tuple"])),
        ),
    }


def from_typed_hypergraph(view):
    if view.get("view") != "typed-hypergraph/derived-1.0":
        raise ValueError("unsupported hypergraph view")
    model = empty_model()
    for node in view.get("nodes", []):
        if node.get("type") not in SORTS:
            raise ValueError("unknown node sort")
        model["sorts"][node["type"]].append(node["id"])
    edge_ids = [edge.get("id") for edge in view.get("edges", [])]
    if len(edge_ids) != len(set(edge_ids)):
        raise ValueError("duplicate hyperedge identity")
    for edge in view.get("edges", []):
        relation_name = edge.get("type")
        if relation_name not in RELATION_SIGNATURES:
            raise ValueError("unknown edge type")
        ordered_ports = sorted(
            edge.get("ports", []), key=lambda port: port["position"]
        )
        row = [port["node"] for port in ordered_ports]
        if row != edge.get("tuple"):
            raise ValueError("port/tuple disagreement")
        model["relations"][relation_name].append(row)
    model = normalized_model(model)
    errors = validate_model(model)
    if errors:
        raise ValueError("; ".join(errors))
    return model


def to_algebraic_view(model):
    errors = validate_model(model)
    if errors:
        raise ValueError("; ".join(errors))
    rules = {event: rule for event, rule in model["relations"]["applies"]}
    inputs = {event: state for event, state in model["relations"]["input_state"]}
    outputs = {event: state for event, state in model["relations"]["output_state"]}
    operations = [
        {
            "event": event,
            "operation": rules[event],
            "domain_state": inputs[event],
            "codomain_state": outputs[event],
        }
        for event in model["sorts"]["Event"]
    ]
    sidecar = copy.deepcopy(model)
    for relation_name in ("applies", "input_state", "output_state"):
        sidecar["relations"][relation_name] = []
    sidecar["sorts"]["Event"] = []
    return {
        "view": "algebraic-state-transition/derived-1.0",
        "operations": operations,
        "order": copy.deepcopy(model["relations"]["precedes"]),
        "sidecar": sidecar,
        "standalone_complete": False,
        "sidecar_required_for_full_reconstruction": True,
    }


def from_algebraic_view(view):
    if view.get("view") != "algebraic-state-transition/derived-1.0":
        raise ValueError("unsupported algebraic view")
    if "sidecar" not in view:
        raise ValueError("full reconstruction requires explicit sidecar")
    model = copy.deepcopy(view["sidecar"])
    events = []
    for operation in view.get("operations", []):
        event = operation["event"]
        events.append(event)
        model["relations"]["applies"].append([event, operation["operation"]])
        model["relations"]["input_state"].append(
            [event, operation["domain_state"]]
        )
        model["relations"]["output_state"].append(
            [event, operation["codomain_state"]]
        )
    model["sorts"]["Event"] = sorted(events)
    model["relations"]["precedes"] = copy.deepcopy(view.get("order", []))
    model = normalized_model(model)
    errors = validate_model(model)
    if errors:
        raise ValueError("; ".join(errors))
    return model


def extensional_occurrence_projection(model):
    """Erase occurrence identities to expose duplicate-edge loss."""
    types = {row[0]: row[1] for row in model["relations"]["instance_of"]}
    participants = defaultdict(list)
    for occurrence, role, object_id in model["relations"]["participant"]:
        participants[occurrence].append((role, object_id))
    return sorted(
        {
            (types[occurrence], tuple(sorted(rows)))
            for occurrence, rows in participants.items()
        }
    )


def evaluate_candidates(spec):
    output = []
    for candidate in spec["candidates"]:
        gates = candidate["gates"]
        missing = [gate for gate in MANDATORY_GATES if gates.get(gate) is not True]
        classification = (
            "canonical-candidate"
            if not missing
            else "admissible-derived-view"
            if candidate.get("derived_view_admissible") is True
            else "noncanonical"
        )
        output.append(
            {
                "id": candidate["id"],
                "classification": classification,
                "failed_gates": missing,
                "reason": candidate["reason"],
            }
        )
    return output


def build_proof(spec):
    model = sample_model()
    errors = validate_model(model)
    if errors:
        raise ValueError("sample model invalid: " + "; ".join(errors))
    views = derived_views(model)
    hypergraph = to_typed_hypergraph(model)
    hypergraph_roundtrip = from_typed_hypergraph(copy.deepcopy(hypergraph))
    algebraic = to_algebraic_view(model)
    algebraic_roundtrip = from_algebraic_view(copy.deepcopy(algebraic))
    extensional = extensional_occurrence_projection(model)
    candidates = evaluate_candidates(spec)
    selected = [
        row for row in candidates if row["classification"] == "canonical-candidate"
    ]
    if [row["id"] for row in selected] != [spec["selected_foundation"]]:
        raise ValueError(
            "canonical selection is not uniquely admitted by the frozen gates"
        )
    return {
        "campaign_id": spec["campaign_id"],
        "spec_digest": digest(spec),
        "kernel_version": KERNEL_VERSION,
        "status": "Accepted",
        "scope": spec["scope"],
        "candidate_adjudication": candidates,
        "selected_foundation": spec["selected_foundation"],
        "sample_model_digest": digest(model),
        "sample_model_valid": not errors,
        "derived_views_digest": digest(views),
        "hypergraph_translation": {
            "node_count": len(hypergraph["nodes"]),
            "edge_count": len(hypergraph["edges"]),
            "roundtrip_exact": canonical(normalized_model(hypergraph_roundtrip))
            == canonical(normalized_model(model)),
            "digest": digest(hypergraph),
        },
        "algebraic_translation": {
            "operation_count": len(algebraic["operations"]),
            "standalone_complete": algebraic["standalone_complete"],
            "sidecar_required": algebraic[
                "sidecar_required_for_full_reconstruction"
            ],
            "roundtrip_exact_with_sidecar": canonical(
                normalized_model(algebraic_roundtrip)
            )
            == canonical(normalized_model(model)),
            "digest": digest(algebraic),
        },
        "counterexamples": {
            "extensional_relation_identity_loss": {
                "occurrence_count": len(model["sorts"]["RelationOccurrence"]),
                "projected_fact_count": len(extensional),
                "loss_detected": len(extensional)
                < len(model["sorts"]["RelationOccurrence"]),
            },
            "bare_algebraic_reconstruction": {
                "full_reconstruction_without_sidecar": False,
                "lost_commitments": [
                    "source/representation sort separation",
                    "interpretation",
                    "investigation context",
                    "provenance",
                    "relation occurrence identity",
                ],
            },
        },
        "derived_status": {
            "Property": "derived unary relation occurrence",
            "Investigation": (
                "derived objective/condition/calculus context tuple; "
                "records may carry identity"
            ),
            "SemanticContent": "derived interpretation application",
            "TransitionSignature": "derived representation of Event",
            "ReasoningTrace": "derived ordered Event collection",
        },
        "historical_artifacts": spec["historical_artifacts"],
        "historical_result_policy": spec["historical_result_policy"],
        "nonclaims": spec["nonclaims"],
        "conclusion": spec["conclusion"],
    }
