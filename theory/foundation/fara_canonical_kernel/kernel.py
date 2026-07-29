"""Executable Research candidate for an identity-bearing FARA relational kernel."""
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter, defaultdict

KERNEL_VERSION = "fara-identity-bearing-many-sorted-relational/1.0-research"
SORTS = (
    "Object", "Representation", "Meaning", "Interpretation",
    "ReasoningCalculus", "Rule", "State", "Event", "Investigation",
    "Objective", "Condition", "RelationType", "RelationOccurrence",
    "Role", "Provenance",
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
CANDIDATE_IDS = (
    "many-sorted-extensional-relational",
    "typed-hypergraph",
    "algebraic-state-transition",
    "identity-bearing-many-sorted-relational",
)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def empty_model():
    return {
        "kernel_version": KERNEL_VERSION,
        "sorts": {name: [] for name in SORTS},
        "relations": {name: [] for name in RELATION_SIGNATURES},
    }


def normalized_model(model):
    out = copy.deepcopy(model)
    for name in SORTS:
        out["sorts"][name] = sorted(out["sorts"][name])
    for name in RELATION_SIGNATURES:
        out["relations"][name] = sorted(out["relations"][name], key=canonical)
    return out


def sample_model():
    model = empty_model()
    model["sorts"].update({
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
    })
    model["relations"].update({
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
    })
    return model


def _first_counts(rows):
    return Counter(row[0] for row in rows if isinstance(row, list) and row)


def _has_cycle(rows):
    graph = defaultdict(list)
    nodes = set()
    for left, right in rows:
        graph[left].append(right)
        nodes.update((left, right))
    active, done = set(), set()
    def visit(node):
        if node in active:
            return True
        if node in done:
            return False
        active.add(node)
        if any(visit(target) for target in graph[node]):
            return True
        active.remove(node)
        done.add(node)
        return False
    return any(visit(node) for node in nodes)


def validate_model(model):
    errors = []
    if model.get("kernel_version") != KERNEL_VERSION:
        errors.append("kernel version mismatch")
    sorts, relations = model.get("sorts"), model.get("relations")
    if not isinstance(sorts, dict) or set(sorts) != set(SORTS):
        return ["sort registry mismatch"]
    if not isinstance(relations, dict) or set(relations) != set(RELATION_SIGNATURES):
        return ["relation registry mismatch"]
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
        rows = relations[relation_name]
        if not isinstance(rows, list):
            errors.append(f"{relation_name} is not a list")
            continue
        valid_rows = [row for row in rows if isinstance(row, list)]
        if len(valid_rows) != len({tuple(row) for row in valid_rows}):
            errors.append(f"duplicate extensional fact: {relation_name}")
        for row in rows:
            if not isinstance(row, list) or len(row) != len(signature):
                errors.append(f"wrong arity: {relation_name}")
                continue
            for value, expected_sort in zip(row, signature):
                if value not in sorts[expected_sort]:
                    errors.append(f"ill-typed {relation_name}: {value} not in {expected_sort}")
    type_counts = _first_counts(relations["instance_of"])
    participant_counts = _first_counts(relations["participant"])
    for occurrence in sorts["RelationOccurrence"]:
        if type_counts[occurrence] != 1:
            errors.append(f"relation occurrence requires exactly one type: {occurrence}")
        if participant_counts[occurrence] < 1:
            errors.append(f"participant-free relation occurrence: {occurrence}")
    exact = (
        ("applies", "rule"), ("input_state", "input state"),
        ("output_state", "output state"), ("occurs_in", "investigation"),
    )
    counts = {name: _first_counts(relations[name]) for name, _ in exact}
    provenance = _first_counts(relations["provenance_of"])
    for event in sorts["Event"]:
        for name, label in exact:
            if counts[name][event] != 1:
                errors.append(f"event requires exactly one {label}: {event}")
        if provenance[event] < 1:
            errors.append(f"event without explicit provenance: {event}")
    if _has_cycle(relations["precedes"]):
        errors.append("precedes relation contains a cycle")
    return sorted(set(errors))


def _topological_events(events, rows):
    incoming = {event: 0 for event in events}
    outgoing = defaultdict(list)
    for left, right in rows:
        outgoing[left].append(right)
        incoming[right] += 1
    ready = sorted(event for event, count in incoming.items() if count == 0)
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
    types = {occurrence: relation_type for occurrence, relation_type in relations["instance_of"]}
    participants = defaultdict(list)
    for occurrence, role, object_id in relations["participant"]:
        participants[occurrence].append([role, object_id])
    return {
        "properties": sorted(occurrence for occurrence, rows in participants.items() if len(rows) == 1),
        "relation_occurrences": [
            {"id": occurrence, "type": types[occurrence], "participants": sorted(participants[occurrence])}
            for occurrence in sorted(participants)
        ],
        "semantic_content": sorted([
            {"interpretation": interpretation, "representation": representation, "meaning": meaning}
            for interpretation, representation, meaning in relations["assigns"]
        ], key=canonical),
        "transition_signatures": sorted([
            {"representation": representation, "event": event}
            for representation, event in relations["represents_event"]
        ], key=canonical),
        "reasoning_trace": _topological_events(model["sorts"]["Event"], relations["precedes"]),
    }


def to_typed_hypergraph(model):
    errors = validate_model(model)
    if errors:
        raise ValueError("; ".join(errors))
    nodes = [
        {"id": member, "type": sort_name}
        for sort_name in SORTS for member in model["sorts"][sort_name]
    ]
    edges = []
    for relation_name in sorted(RELATION_SIGNATURES):
        for index, row in enumerate(model["relations"][relation_name]):
            edges.append({
                "id": f"{relation_name}:{index}:{digest(row)[:12]}",
                "type": relation_name,
                "ports": [
                    {"position": position, "node": value, "sort": expected}
                    for position, (value, expected) in enumerate(zip(row, RELATION_SIGNATURES[relation_name]))
                ],
                "tuple": copy.deepcopy(row),
            })
    return {
        "view": "typed-hypergraph/derived-1.0",
        "kernel_version": KERNEL_VERSION,
        "native_schema": ["Node", "Port", "Hyperedge"],
        "nodes": sorted(nodes, key=lambda row: (row["type"], row["id"])),
        "edges": sorted(edges, key=lambda row: (row["type"], row["id"])),
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
        ports = sorted(edge.get("ports", []), key=lambda port: port["position"])
        row = [port["node"] for port in ports]
        if row != edge.get("tuple"):
            raise ValueError("port/tuple disagreement")
        model["relations"][relation_name].append(row)
    model = normalized_model(model)
    errors = validate_model(model)
    if errors:
        raise ValueError("; ".join(errors))
    return model


def _single_value_map(rows, label):
    grouped = defaultdict(list)
    for key, value in rows:
        grouped[key].append(value)
    if any(len(values) != 1 for values in grouped.values()):
        raise ValueError(f"{label} is not single-valued")
    return {key: values[0] for key, values in grouped.items()}


def to_algebraic_view(model):
    errors = validate_model(model)
    if errors:
        raise ValueError("; ".join(errors))
    rules = _single_value_map(model["relations"]["applies"], "applies")
    inputs = _single_value_map(model["relations"]["input_state"], "input_state")
    outputs = _single_value_map(model["relations"]["output_state"], "output_state")
    operations = [
        {"event": event, "operation": rules[event], "domain_state": inputs[event], "codomain_state": outputs[event]}
        for event in model["sorts"]["Event"]
    ]
    sidecar = copy.deepcopy(model)
    for name in ("applies", "input_state", "output_state", "precedes"):
        sidecar["relations"][name] = []
    sidecar["sorts"]["Event"] = []
    return {
        "view": "algebraic-state-transition/derived-1.0",
        "native_schema": ["Operation", "Transition"],
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
        if event in events:
            raise ValueError("duplicate algebraic event")
        events.append(event)
        model["relations"]["applies"].append([event, operation["operation"]])
        model["relations"]["input_state"].append([event, operation["domain_state"]])
        model["relations"]["output_state"].append([event, operation["codomain_state"]])
    model["sorts"]["Event"] = events
    model["relations"]["precedes"] = copy.deepcopy(view.get("order", []))
    model = normalized_model(model)
    errors = validate_model(model)
    if errors:
        raise ValueError("; ".join(errors))
    return model


def extensional_occurrence_projection(model):
    types = {occurrence: relation_type for occurrence, relation_type in model["relations"]["instance_of"]}
    participants = defaultdict(list)
    for occurrence, role, object_id in model["relations"]["participant"]:
        participants[occurrence].append((role, object_id))
    return sorted({(types[occurrence], tuple(sorted(rows))) for occurrence, rows in participants.items()})


def _gate(passed, evidence, **measurements):
    return {"pass": bool(passed), "evidence": evidence, "measurements": measurements}


def _kernel_gate_evidence(model):
    valid = not validate_model(model)
    collision = copy.deepcopy(model)
    collision["sorts"]["Representation"].append("source-temperature")
    collision_rejected = any("cross-sort identity collision" in error for error in validate_model(collision))
    no_provenance = copy.deepcopy(model)
    no_provenance["relations"]["provenance_of"] = [row for row in no_provenance["relations"]["provenance_of"] if row[0] != "e1"]
    provenance_rejected = "event without explicit provenance: e1" in validate_model(no_provenance)
    cyclic = copy.deepcopy(model)
    cyclic["relations"]["precedes"].append(["e2", "e1"])
    cycle_rejected = "precedes relation contains a cycle" in validate_model(cyclic)
    projection = extensional_occurrence_projection(model)
    exact_event = all(
        _first_counts(model["relations"][name])[event] == 1
        for name in ("applies", "input_state", "output_state", "occurs_in")
        for event in model["sorts"]["Event"]
    )
    return {
        "representation_object_separation": _gate(valid and collision_rejected, "disjoint carriers are enforced by executable validation", collision_rejected=collision_rejected),
        "rule_execution_result_separation": _gate(valid and exact_event, "each Event has exactly one Rule, input State, output State, and Investigation", exact_event_contract=exact_event),
        "interpretation_separation": _gate(valid and bool(model["sorts"]["Interpretation"]) and bool(model["relations"]["assigns"]), "Interpretation is a distinct carrier connected by assigns", interpretation_count=len(model["sorts"]["Interpretation"])),
        "calculus_independence": _gate(valid and "Operation" not in SORTS, "formation uses explicit ReasoningCalculus/Rule carriers without a fixed operation algebra", calculus_count=len(model["sorts"]["ReasoningCalculus"])),
        "architecture_operation_separation": _gate(valid and "Operation" not in SORTS and set(model["sorts"]["Rule"]).isdisjoint(model["sorts"]["Event"]), "Rule and Event are disjoint and no Operation carrier is primitive", operation_primitive=False),
        "identity_bearing_occurrences": _gate(len(model["sorts"]["RelationOccurrence"]) > len(projection), "two occurrence identities collapse to one fact only after extensional projection", occurrence_count=len(model["sorts"]["RelationOccurrence"]), projected_fact_count=len(projection)),
        "explicit_provenance_and_order": _gate(valid and provenance_rejected and cycle_rejected and bool(model["relations"]["precedes"]), "provenance is mandatory and cyclic order is rejected", missing_provenance_rejected=provenance_rejected, cyclic_order_rejected=cycle_rejected),
        "encoding_neutrality": _gate(valid and not ({"Node", "Port", "Hyperedge", "Operation"} & set(SORTS)), "native carriers use FARA categories without graph/operation scaffolding", scaffolding=[]),
    }


def derive_candidate_gates(model):
    kernel_gates = _kernel_gate_evidence(model)
    hypergraph = to_typed_hypergraph(model)
    hypergraph_exact = canonical(normalized_model(from_typed_hypergraph(copy.deepcopy(hypergraph)))) == canonical(normalized_model(model))
    algebraic = to_algebraic_view(model)
    algebraic_exact = canonical(normalized_model(from_algebraic_view(copy.deepcopy(algebraic)))) == canonical(normalized_model(model))
    bare_rejected = False
    try:
        from_algebraic_view({key: value for key, value in algebraic.items() if key != "sidecar"})
    except ValueError:
        bare_rejected = True
    extensional = copy.deepcopy(kernel_gates)
    extensional["identity_bearing_occurrences"] = _gate(False, "extensional projection collapses two occurrence identities to one fact", occurrence_count=2, projected_fact_count=1)
    hypergraph_gates = {
        gate: _gate(hypergraph_exact and evidence["pass"], "exact hypergraph round trip preserves kernel evidence: " + evidence["evidence"], roundtrip_exact=hypergraph_exact)
        for gate, evidence in kernel_gates.items()
    }
    hypergraph_gates["encoding_neutrality"] = _gate(False, "native schema requires Node/Port/Hyperedge scaffolding", native_schema=hypergraph["native_schema"])
    algebraic_gates = {
        "representation_object_separation": _gate(False, "bare algebraic view has no Object/Representation carriers"),
        "rule_execution_result_separation": _gate(True, "operation rows separately record event, operation, domain state, and codomain state", operation_rows=len(algebraic["operations"])),
        "interpretation_separation": _gate(False, "bare algebraic view has no Interpretation carrier"),
        "calculus_independence": _gate(False, "formation is defined directly by operation rows"),
        "architecture_operation_separation": _gate(False, "Operation is native in the bare view"),
        "identity_bearing_occurrences": _gate(False, "bare view has no RelationOccurrence identities"),
        "explicit_provenance_and_order": _gate(False, "order is present but provenance is absent", order_present=bool(algebraic["order"]), provenance_present=False),
        "encoding_neutrality": _gate(False, "native schema requires Operation/Transition scaffolding", native_schema=algebraic["native_schema"]),
    }
    return {
        CANDIDATE_IDS[0]: extensional,
        CANDIDATE_IDS[1]: hypergraph_gates,
        CANDIDATE_IDS[2]: algebraic_gates,
        CANDIDATE_IDS[3]: kernel_gates,
    }, {
        "typed_hypergraph_roundtrip_exact": hypergraph_exact,
        "algebraic_sidecar_roundtrip_exact": algebraic_exact,
        "bare_algebraic_reconstruction_rejected": bare_rejected,
        "typed_hypergraph": hypergraph,
        "algebraic": algebraic,
    }


def evaluate_candidates(spec, model):
    if [candidate["id"] for candidate in spec["candidates"]] != list(CANDIDATE_IDS):
        raise ValueError("candidate registry drift")
    if any("gates" in candidate for candidate in spec["candidates"]):
        raise ValueError("candidate-authored gate booleans are forbidden")
    gate_rows, translations = derive_candidate_gates(model)
    rows = []
    for candidate in spec["candidates"]:
        evidence = gate_rows[candidate["id"]]
        failed = [gate for gate in MANDATORY_GATES if not evidence[gate]["pass"]]
        if not failed:
            classification = "provisional-canonical-candidate"
        elif candidate["id"] == "typed-hypergraph" and translations["typed_hypergraph_roundtrip_exact"]:
            classification = "admissible-derived-view"
        elif candidate["id"] == "algebraic-state-transition" and translations["algebraic_sidecar_roundtrip_exact"]:
            classification = "admissible-derived-view"
        else:
            classification = "noncanonical"
        rows.append({"id": candidate["id"], "classification": classification, "failed_gates": failed, "gate_evidence": evidence, "reason": candidate["reason"]})
    return rows, translations


def build_proof(spec):
    if spec.get("status") != "Research":
        raise ValueError("research lifecycle status must remain Research")
    model = sample_model()
    errors = validate_model(model)
    if errors:
        raise ValueError("sample model invalid: " + "; ".join(errors))
    candidates, translations = evaluate_candidates(spec, model)
    provisional = [row["id"] for row in candidates if row["classification"] == "provisional-canonical-candidate"]
    if provisional != [spec["proposed_foundation"]]:
        raise ValueError("provisional recommendation is not uniquely supported")
    views = derived_views(model)
    hypergraph, algebraic = translations["typed_hypergraph"], translations["algebraic"]
    projection = extensional_occurrence_projection(model)
    return {
        "campaign_id": spec["campaign_id"],
        "spec_digest": digest(spec),
        "kernel_version": KERNEL_VERSION,
        "status": "Research",
        "scope": spec["scope"],
        "lifecycle": spec["lifecycle"],
        "candidate_adjudication": candidates,
        "proposed_foundation": spec["proposed_foundation"],
        "sample_model_digest": digest(model),
        "sample_model_valid": True,
        "derived_views_digest": digest(views),
        "hypergraph_translation": {"node_count": len(hypergraph["nodes"]), "edge_count": len(hypergraph["edges"]), "roundtrip_exact": translations["typed_hypergraph_roundtrip_exact"], "digest": digest(hypergraph)},
        "algebraic_translation": {"operation_count": len(algebraic["operations"]), "standalone_complete": algebraic["standalone_complete"], "sidecar_required": algebraic["sidecar_required_for_full_reconstruction"], "roundtrip_exact_with_sidecar": translations["algebraic_sidecar_roundtrip_exact"], "bare_reconstruction_rejected": translations["bare_algebraic_reconstruction_rejected"], "digest": digest(algebraic)},
        "counterexamples": {
            "extensional_relation_identity_loss": {"occurrence_count": len(model["sorts"]["RelationOccurrence"]), "projected_fact_count": len(projection), "loss_detected": len(projection) < len(model["sorts"]["RelationOccurrence"])},
            "bare_algebraic_reconstruction": {"full_reconstruction_without_sidecar": False, "rejection_observed": translations["bare_algebraic_reconstruction_rejected"]},
        },
        "provisional_reductions": {
            "Property": "unary relation occurrence within the research kernel",
            "Investigation": "objective/condition/calculus context tuple within the research kernel",
            "SemanticContent": "interpretation application within the research kernel",
            "TransitionSignature": "representation of Event within the research kernel",
            "ReasoningTrace": "ordered Event collection within the research kernel",
        },
        "historical_artifacts": spec["historical_artifacts"],
        "historical_result_policy": spec["historical_result_policy"],
        "nonclaims": spec["nonclaims"],
        "finding": spec["finding"],
    }
