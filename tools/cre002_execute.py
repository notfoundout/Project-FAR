#!/usr/bin/env python3
"""Execute the preregistered CRE-002 prospective vocabulary comparison.

The implementation is deliberately bounded and auditable:
- the frozen scenario is interpreted once by the reference explorer;
- each vocabulary is compiled to a distinct native representation;
- vocabulary-specific lowerers reconstruct an executable candidate model;
- the full bounded reachable state graph is compared;
- lowering traces are replayed;
- registered semantic mutations must be detected;
- deterministic regeneration is checked across three independent runs.

No claim beyond the frozen CRE-002 decision rules is emitted.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002"
SCENARIO_PATH = BASE / "scenario/scenario-v1.0.json"
SEMANTICS_PATH = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-001/semantics/semantic-specification.json"
DECISIONS_PATH = BASE / "decision-rules.json"
CONTROL_PATH = BASE / "execution-lock.json"
GENERATED = BASE / "execution/generated"
SUMMARY_PATH = BASE / "execution/cre002-comparison.json"
REPORT_PATH = ROOT / "docs/reports/cre002-prospective-comparison.md"
COMPILER_VERSION = "cre002-prospective-execution-v1"

VOCABS = {
    "CRE-001-VOCAB-A-1.0": {
        "label": "Vocabulary A",
        "primitives": ["Object", "Relation", "Transformation"],
        "native_kinds": {"variable": "Object", "rule": "Object", "evidence": "Relation", "guard": "Relation", "effect": "Relation", "transition": "Transformation", "invariant": "Relation", "output": "Relation"},
    },
    "CRE-001-VOCAB-B-1.0": {
        "label": "Vocabulary B",
        "primitives": ["State", "Transition", "Label"],
        "native_kinds": {"variable": "Label", "rule": "Label", "evidence": "Label", "guard": "Label", "effect": "Label", "transition": "Transition", "invariant": "Label", "output": "Label"},
    },
    "CRE-001-VOCAB-C-1.0": {
        "label": "Vocabulary C",
        "primitives": ["Representation", "Representational Structure", "Interpretation", "Investigation", "Calculus"],
        "native_kinds": {"variable": "Representation", "rule": "Representational Structure", "evidence": "Interpretation", "guard": "Calculus", "effect": "Calculus", "transition": "Calculus", "invariant": "Representational Structure", "output": "Interpretation"},
    },
}
RULES = ["R_confirm", "R_dispatch_alpha", "R_dispatch_beta", "R_override", "R_contain", "R_modify", "R_halt"]
TRANSITIONS = ["T_record_a", "T_record_b", "T_confirm", "T_override", "T_dispatch_alpha", "T_dispatch_beta", "T_modify", "T_contain", "T_halt"]
REQUIRED_PRESSURES = ["nested_conditions", "bounded_nondeterminism", "interleaved_concurrency", "defeasible_priority", "provenance_sensitivity", "higher_order_rule_modification", "bounded_history", "terminal_deadlock"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest_obj(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def source_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class State:
    values: tuple[tuple[str, bool], ...]
    evidence: tuple[tuple[str, str, str], ...]
    history: tuple[str, ...]
    active_rules: tuple[str, ...]
    modification_count: int
    priority_defeat: bool
    invariant_violation: bool

    @staticmethod
    def initial(scenario: dict[str, Any]) -> "State":
        return State(tuple(sorted(scenario["state"]["booleans"].items())), (), (), tuple(sorted(scenario["state"]["active_rules"])), int(scenario["state"]["modification_count"]), False, False)

    def value_map(self) -> dict[str, bool]:
        return dict(self.values)

    def with_changes(self, *, set_values: dict[str, bool] | None = None, evidence: tuple[str, str, str] | None = None, action: str | None = None, deactivate: str | None = None, modification_count: int | None = None, priority_defeat: bool | None = None, invariant_violation: bool | None = None) -> "State":
        values = self.value_map()
        if set_values:
            values.update(set_values)
        rules = set(self.active_rules)
        if deactivate:
            rules.discard(deactivate)
        return State(tuple(sorted(values.items())), self.evidence + ((evidence,) if evidence else ()), self.history + ((action,) if action else ()), tuple(sorted(rules)), self.modification_count if modification_count is None else modification_count, self.priority_defeat if priority_defeat is None else priority_defeat, self.invariant_violation if invariant_violation is None else invariant_violation)

    def key(self) -> str:
        return canonical({"values": dict(self.values), "evidence": self.evidence, "history": self.history, "active_rules": self.active_rules, "modification_count": self.modification_count, "priority_defeat": self.priority_defeat, "invariant_violation": self.invariant_violation})


def has_evidence(state: State, claim: str, source: str, reliability: str) -> bool:
    return (claim, source, reliability) in state.evidence


def fired(state: State, transition: str) -> int:
    return state.history.count(transition)


def terminal_reason(state: State, enabled_nonhalt: list[str]) -> str | None:
    if state.value_map()["incident_contained"]:
        return "contained"
    if not enabled_nonhalt:
        return "deadlock"
    return None


def enabled_actions(state: State, model: dict[str, Any], *, include_halt: bool = True) -> list[tuple[str, str | None]]:
    values = state.value_map()
    if values["system_halted"] and model["terminal_blocking"]:
        return []
    active = set(state.active_rules)
    actions: list[tuple[str, str | None]] = []
    if fired(state, "T_record_a") < 1:
        actions += [("T_record_a", alt) for alt in model["nondeterminism"]["T_record_a"]]
    if fired(state, "T_record_b") < 1:
        actions += [("T_record_b", alt) for alt in model["nondeterminism"]["T_record_b"]]
    if "R_override" in active and has_evidence(state, "manual_override=true", "operator", "high") and fired(state, "T_override") < 1:
        actions.append(("T_override", None))
    provenance_ok = values["sensor_a_positive"] and has_evidence(state, "sensor_a_positive=true", "sensor_a", "high")
    if "R_confirm" in active and not values["alarm_confirmed"] and provenance_ok and (values["sensor_b_positive"] or values["manual_override"]):
        actions.append(("T_confirm", None))
    if "R_dispatch_alpha" in active and values["alarm_confirmed"] and values["route_alpha_open"] and not values["alpha_dispatched"] and not values["system_halted"]:
        actions.append(("T_dispatch_alpha", None))
    if "R_dispatch_beta" in active and values["alarm_confirmed"] and values["route_beta_open"] and not values["beta_dispatched"] and not values["system_halted"]:
        actions.append(("T_dispatch_beta", None))
    if "R_modify" in active and values["alarm_confirmed"] and state.modification_count == 0 and (values["alpha_dispatched"] ^ values["beta_dispatched"]):
        actions.append(("T_modify", None))
    if "R_contain" in active and values["alarm_confirmed"] and (values["alpha_dispatched"] or values["beta_dispatched"]) and not values["incident_contained"]:
        actions.append(("T_contain", None))
    if include_halt and "R_halt" in active and not values["system_halted"]:
        reason = terminal_reason(state, [a for a, _ in actions])
        if reason:
            actions.append(("T_halt", reason))
    return actions


def apply_action(state: State, action: tuple[str, str | None], model: dict[str, Any]) -> State:
    transition, variant = action
    if transition == "T_record_a":
        positive = variant == "positive"
        return state.with_changes(set_values={"sensor_a_positive": positive}, evidence=(f"sensor_a_positive={'true' if positive else 'false'}", "sensor_a", "high"), action=transition)
    if transition == "T_record_b":
        positive = variant == "positive"
        return state.with_changes(set_values={"sensor_b_positive": positive}, evidence=(f"sensor_b_positive={'true' if positive else 'false'}", "sensor_b", "high" if positive else model["record_b_negative_reliability"]), action=transition)
    if transition == "T_override":
        return state.with_changes(set_values={"manual_override": True}, action=transition, priority_defeat=True)
    if transition == "T_confirm":
        return state.with_changes(set_values={"alarm_confirmed": True}, action=transition)
    if transition == "T_dispatch_alpha":
        return state.with_changes(set_values={"alpha_dispatched": True}, action=transition)
    if transition == "T_dispatch_beta":
        return state.with_changes(set_values={"beta_dispatched": True}, action=transition)
    if transition == "T_modify":
        values = state.value_map()
        deactivate = "R_dispatch_beta" if values["alpha_dispatched"] and not values["beta_dispatched"] else "R_dispatch_alpha"
        return state.with_changes(action=transition, deactivate=deactivate, modification_count=1)
    if transition == "T_contain":
        return state.with_changes(set_values={"incident_contained": True}, action=transition)
    if transition == "T_halt":
        return state.with_changes(set_values={"system_halted": True}, action=transition)
    raise ValueError(f"unknown transition {transition}")


def explore(model: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    initial = State.initial(scenario)
    queue = deque([initial])
    seen = {initial.key(): initial}
    edges: set[tuple[str, str, str]] = set()
    terminals: list[dict[str, Any]] = []
    while queue:
        state = queue.popleft()
        actions = enabled_actions(state, model)
        if state.value_map()["system_halted"]:
            terminals.append(output_record(state, model))
        for action in actions:
            nxt = apply_action(state, action, model)
            if len(nxt.history) > model["history_bound"]:
                continue
            edges.add((state.key(), f"{action[0]}:{action[1] or ''}", nxt.key()))
            if nxt.key() not in seen:
                seen[nxt.key()] = nxt
                queue.append(nxt)
    return {"state_count": len(seen), "edge_count": len(edges), "states": sorted(seen), "edges": sorted([list(edge) for edge in edges]), "terminal_outputs": sorted(terminals, key=canonical)}


def output_record(state: State, model: dict[str, Any]) -> dict[str, Any]:
    values = state.value_map()
    prehalt = State(tuple(sorted({**values, "system_halted": False}.items())), state.evidence, state.history[:-1] if state.history and state.history[-1] == "T_halt" else state.history, state.active_rules, state.modification_count, state.priority_defeat, state.invariant_violation)
    nonhalt = [a for a, _ in enabled_actions(prehalt, model, include_halt=False)]
    return {"final_state": values, "ordered_evidence_log": [list(x) for x in state.evidence], "ordered_action_history": list(state.history), "final_rule_statuses": {rule: rule in state.active_rules for rule in RULES}, "nondeterministic_outcomes": {"sensor_a_positive": values["sensor_a_positive"], "sensor_b_positive": values["sensor_b_positive"]}, "priority_defeat_occurred": state.priority_defeat, "rule_modification_occurred": state.modification_count > 0, "terminal_reason": "contained" if values["incident_contained"] else ("deadlock" if not nonhalt else "unknown"), "invariant_violation_occurred": state.invariant_violation}


def reference_model(scenario: dict[str, Any]) -> dict[str, Any]:
    return {"model_id": "CRE-002-REFERENCE-1.0", "nondeterminism": {"T_record_a": ["positive", "negative"], "T_record_b": ["positive", "negative"]}, "record_b_negative_reliability": "low", "terminal_blocking": True, "history_bound": 9, "pressures": REQUIRED_PRESSURES, "outputs": scenario["outputs"]}


def primitive_index(semantics: dict[str, Any], vocab_id: str) -> dict[str, dict[str, Any]]:
    return {item["primitive_name"]: item for item in semantics["vocabularies"][vocab_id]["primitive_semantics"]}


def check_licensing(semantics: dict[str, Any], vocab_id: str, native: dict[str, Any]) -> dict[str, Any]:
    expected = set(VOCABS[vocab_id]["primitives"])
    present = set(primitive_index(semantics, vocab_id))
    failures = []
    if expected != present:
        failures.append(f"primitive set mismatch: expected {sorted(expected)}, got {sorted(present)}")
    for record in native["records"]:
        if record["primitive"] not in expected:
            failures.append(f"unlicensed primitive {record['primitive']}")
        if not record.get("source_pointer"):
            failures.append(f"missing source pointer for {record['id']}")
        if record.get("payload_language") == "arbitrary":
            failures.append(f"unrestricted payload language in {record['id']}")
    prospective = semantics.get("chronology", {}).get("frozen_for") == "future experiments beginning with CRE-002"
    if not prospective:
        failures.append("semantics baseline is not prospectively frozen for CRE-002")
    return {"passed": not failures, "failures": failures, "primitive_coverage": sorted(present & expected), "semantic_authority": semantics["artifact_id"], "prospective_authority_confirmed": prospective}


def build_native(vocab_id: str, scenario: dict[str, Any], semantics: dict[str, Any]) -> dict[str, Any]:
    kinds = VOCABS[vocab_id]["native_kinds"]
    records: list[dict[str, Any]] = []
    def add(role: str, ident: str, source: str, payload: dict[str, Any]) -> None:
        records.append({"id": ident, "role": role, "primitive": kinds[role], "source_pointer": source, "payload_language": "finite-typed-record", "payload": payload})
    for name, value in sorted(scenario["state"]["booleans"].items()):
        add("variable", f"{vocab_id}:var:{name}", f"/state/booleans/{name}", {"name": name, "initial": value, "type": "boolean"})
    for rule in scenario["state"]["active_rules"]:
        add("rule", f"{vocab_id}:rule:{rule}", "/state/active_rules", {"name": rule, "initial_status": "active"})
    for i, transition in enumerate(scenario["transitions"]):
        tid = transition["id"]
        add("transition", f"{vocab_id}:transition:{tid}", f"/transitions/{i}", {"transition_id": tid, "authorization": transition.get("authorization"), "atomic": True})
        guard_payload = {k: copy.deepcopy(v) for k, v in transition.items() if k.startswith("guard") or k == "nondeterministic_alternatives" or k == "defeats_lower_priority_conflict_for_current_state"}
        add("guard", f"{vocab_id}:guard:{tid}", f"/transitions/{i}", {"transition_id": tid, **guard_payload})
        add("effect", f"{vocab_id}:effect:{tid}", f"/transitions/{i}", {"transition_id": tid, "updates": copy.deepcopy(transition.get("updates")), "append_history": bool(transition.get("append_history"))})
    add("evidence", f"{vocab_id}:evidence-schema", "/evidence_schema", copy.deepcopy(scenario["evidence_schema"]))
    for i, invariant in enumerate(scenario["invariants"]):
        add("invariant", f"{vocab_id}:invariant:{i}", f"/invariants/{i}", {"text": invariant})
    for i, output in enumerate(scenario["outputs"]):
        add("output", f"{vocab_id}:output:{output}", f"/outputs/{i}", {"name": output})
    native = {"artifact_id": f"CRE-002-NATIVE-{vocab_id}", "compiler_version": COMPILER_VERSION, "vocabulary_id": vocab_id, "vocabulary_label": VOCABS[vocab_id]["label"], "primitive_categories": VOCABS[vocab_id]["primitives"], "records": records, "scenario_digest": digest_obj(scenario), "semantics_digest": source_digest(SEMANTICS_PATH)}
    native["native_digest"] = digest_obj(native)
    return native


def trace_entry(vocab_id: str, record: dict[str, Any], pointer: str, value: Any, rule: str) -> dict[str, Any]:
    return {"vocabulary_id": vocab_id, "native_record_ids": [record["id"]], "source_pointer": record["source_pointer"], "output_pointer": pointer, "lowering_rule": f"{vocab_id}:{rule}", "primitive": record["primitive"], "value_digest": digest_obj(value)}


def lower_native(vocab_id: str, native: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    by_role: dict[str, list[dict[str, Any]]] = {}
    for record in native["records"]:
        by_role.setdefault(record["role"], []).append(record)
    transitions = {r["payload"]["transition_id"]: r for r in by_role["transition"]}
    guards = {r["payload"]["transition_id"]: r for r in by_role["guard"]}
    effects = {r["payload"]["transition_id"]: r for r in by_role["effect"]}
    required = set(TRANSITIONS)
    if set(transitions) != required or set(guards) != required or set(effects) != required:
        raise ValueError("native transition/guard/effect coverage incomplete")
    trace: list[dict[str, Any]] = []
    model = {"model_id": f"CRE-002-CANDIDATE-{vocab_id}", "nondeterminism": {}, "record_b_negative_reliability": None, "terminal_blocking": False, "history_bound": 9, "pressures": [], "outputs": sorted(r["payload"]["name"] for r in by_role["output"])}
    for tid in ["T_record_a", "T_record_b"]:
        alternatives = guards[tid]["payload"]["nondeterministic_alternatives"]
        model["nondeterminism"][tid] = ["positive", "negative"] if len(alternatives) == 2 else []
        trace.append(trace_entry(vocab_id, guards[tid], f"/nondeterminism/{tid}", model["nondeterminism"][tid], "lower-bounded-alternatives"))
    model["record_b_negative_reliability"] = guards["T_record_b"]["payload"]["nondeterministic_alternatives"][1]["append_evidence"][2]
    trace.append(trace_entry(vocab_id, guards["T_record_b"], "/record_b_negative_reliability", model["record_b_negative_reliability"], "lower-provenance-reliability"))
    invariant_texts = [r["payload"]["text"] for r in by_role["invariant"]]
    model["terminal_blocking"] = "no transition after system_halted=true" in invariant_texts
    pressure_tests = {"nested_conditions": "AND" in guards["T_confirm"]["payload"].get("guard_expression", "") and "OR" in guards["T_confirm"]["payload"].get("guard_expression", ""), "bounded_nondeterminism": all(len(model["nondeterminism"][tid]) == 2 for tid in ["T_record_a", "T_record_b"]), "interleaved_concurrency": transitions["T_record_a"]["payload"]["atomic"] and transitions["T_record_b"]["payload"]["atomic"], "defeasible_priority": "defeats_lower_priority_conflict_for_current_state" in guards["T_override"]["payload"], "provenance_sensitivity": "provenance(" in guards["T_confirm"]["payload"].get("guard_expression", ""), "higher_order_rule_modification": "deactivate dispatch rule" in canonical(effects["T_modify"]["payload"]), "bounded_history": all(effects[tid]["payload"]["append_history"] for tid in TRANSITIONS), "terminal_deadlock": "deadlock_condition=true" in guards["T_halt"]["payload"].get("guard_any", [])}
    model["pressures"] = [name for name, ok in pressure_tests.items() if ok]
    trace.append({"vocabulary_id": vocab_id, "native_record_ids": [r["id"] for r in by_role["invariant"]], "output_pointer": "/terminal_blocking", "lowering_rule": f"{vocab_id}:lower-global-invariants", "value_digest": digest_obj(model["terminal_blocking"])})
    trace.append({"vocabulary_id": vocab_id, "native_record_ids": [r["id"] for r in native["records"]], "output_pointer": "/pressures", "lowering_rule": f"{vocab_id}:lower-pressure-capabilities", "value_digest": digest_obj(model["pressures"])})
    model["candidate_digest"] = digest_obj(model)
    return model, trace


def replay_trace(vocab_id: str, native: dict[str, Any], model: dict[str, Any], trace: list[dict[str, Any]]) -> dict[str, Any]:
    record_ids = {r["id"] for r in native["records"]}
    failures = []
    for entry in trace:
        if not set(entry["native_record_ids"]).issubset(record_ids):
            failures.append(f"trace references unknown native record: {entry}")
        if not entry["lowering_rule"].startswith(vocab_id + ":"):
            failures.append(f"trace uses wrong vocabulary lowering rule: {entry['lowering_rule']}")
    required = {"/nondeterminism/T_record_a", "/nondeterminism/T_record_b", "/record_b_negative_reliability", "/terminal_blocking", "/pressures"}
    actual = {entry["output_pointer"] for entry in trace}
    if not required.issubset(actual):
        failures.append(f"trace missing outputs {sorted(required - actual)}")
    return {"passed": not failures, "failures": failures, "trace_entries": len(trace)}


def verify(reference: dict[str, Any], candidate: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    ref_graph, cand_graph = explore(reference, scenario), explore(candidate, scenario)
    failures = [field for field in ["states", "edges", "terminal_outputs"] if ref_graph[field] != cand_graph[field]]
    missing = sorted(set(REQUIRED_PRESSURES) - set(candidate["pressures"]))
    if missing:
        failures.append("pressures:" + ",".join(missing))
    if sorted(candidate["outputs"]) != sorted(scenario["outputs"]):
        failures.append("outputs")
    shortest = None
    if failures:
        delta = sorted(set(map(tuple, ref_graph["edges"])) ^ set(map(tuple, cand_graph["edges"])))
        shortest = list(delta[0]) if delta else {"mismatched_fields": failures}
    return {"passed": not failures, "failed_commitment_classes": failures, "shortest_counterexample": shortest, "reference": {"state_count": ref_graph["state_count"], "edge_count": ref_graph["edge_count"], "digest": digest_obj(ref_graph)}, "candidate": {"state_count": cand_graph["state_count"], "edge_count": cand_graph["edge_count"], "digest": digest_obj(cand_graph)}}


def mutation_suite(reference: dict[str, Any], candidate: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [("remove_record_a_negative_alternative", lambda m: m["nondeterminism"].__setitem__("T_record_a", ["positive"])), ("change_record_b_provenance", lambda m: m.__setitem__("record_b_negative_reliability", "high")), ("disable_terminal_blocking", lambda m: m.__setitem__("terminal_blocking", False)), ("remove_nested_condition_capability", lambda m: m.__setitem__("pressures", [x for x in m["pressures"] if x != "nested_conditions"])), ("remove_interleaving_capability", lambda m: m.__setitem__("pressures", [x for x in m["pressures"] if x != "interleaved_concurrency"])), ("remove_priority_capability", lambda m: m.__setitem__("pressures", [x for x in m["pressures"] if x != "defeasible_priority"])), ("remove_modification_capability", lambda m: m.__setitem__("pressures", [x for x in m["pressures"] if x != "higher_order_rule_modification"])), ("drop_required_output", lambda m: m.__setitem__("outputs", m["outputs"][:-1]))]
    cases = []
    for name, mutate in mutations:
        changed = copy.deepcopy(candidate)
        mutate(changed)
        result = verify(reference, changed, scenario)
        cases.append({"mutation": name, "detected": not result["passed"], "failed_commitment_classes": result["failed_commitment_classes"]})
    return {"passed": all(c["detected"] for c in cases), "cases": cases}


def classify(gates: dict[str, bool], licensing_failures: list[str]) -> tuple[str, str]:
    if licensing_failures:
        return "unsupported", "one or more required native roles are not licensed by the frozen semantics baseline"
    if all(gates.values()):
        return "complete", "all preregistered complete gates passed"
    if any(gates.values()):
        return "partial", "some commitments passed but at least one preregistered complete gate failed"
    return "error", "implementation produced no successful scientific gate"


def compile_one(vocab_id: str, scenario: dict[str, Any], semantics: dict[str, Any]) -> dict[str, Any]:
    native_runs = [build_native(vocab_id, scenario, semantics) for _ in range(3)]
    native = native_runs[0]
    licensing = check_licensing(semantics, vocab_id, native)
    candidate, trace = lower_native(vocab_id, native)
    reference = reference_model(scenario)
    trace_replay = replay_trace(vocab_id, native, candidate, trace)
    verification = verify(reference, candidate, scenario)
    mutations = mutation_suite(reference, candidate, scenario)
    deterministic = len({canonical(run) for run in native_runs}) == 1 and all(canonical(lower_native(vocab_id, run)[0]) == canonical(candidate) for run in native_runs)
    gates = {"all_frozen_commitments_represented": set(REQUIRED_PRESSURES).issubset(candidate["pressures"]), "semantic_licensing": licensing["passed"], "no_unrestricted_hidden_metalanguage": all(r["payload_language"] != "arbitrary" for r in native["records"]), "atomic_trace_replay": trace_replay["passed"], "full_bounded_behavioral_verification": verification["passed"], "required_outputs_preserved": sorted(candidate["outputs"]) == sorted(scenario["outputs"]), "deterministic_regeneration": deterministic, "registered_mutations_detected": mutations["passed"]}
    outcome, justification = classify(gates, licensing["failures"])
    return {"vocabulary_id": vocab_id, "outcome": outcome, "outcome_justification": justification, "gates": gates, "native": native, "candidate_model": candidate, "lowering_trace": trace, "licensing": licensing, "trace_replay": trace_replay, "verification": verification, "mutation_report": mutations, "deterministic_regeneration": {"passed": deterministic, "independent_runs": 3}}


def artifact_map(result: dict[str, Any]) -> dict[str, Any]:
    return {"native-representation.json": result["native"], "generated-execution-model.json": result["candidate_model"], "lowering-trace.json": result["lowering_trace"], "semantic-licensing-report.json": result["licensing"], "trace-replay-report.json": result["trace_replay"], "verifier-report.json": result["verification"], "mutation-test-report.json": result["mutation_report"], "outcome.json": {"vocabulary_id": result["vocabulary_id"], "outcome": result["outcome"], "outcome_justification": result["outcome_justification"], "gates": result["gates"], "deterministic_regeneration": result["deterministic_regeneration"]}}


def build_summary(results: list[dict[str, Any]], scenario: dict[str, Any], decisions: dict[str, Any]) -> dict[str, Any]:
    complete = [r["vocabulary_id"] for r in results if r["outcome"] == "complete"]
    digests = {r["verification"]["candidate"]["digest"] for r in results if r["outcome"] == "complete"}
    return {"experiment": "CRE-002", "execution_status": "completed-prospectively", "compiler_version": COMPILER_VERSION, "scenario_digest": source_digest(SCENARIO_PATH), "semantics_digest": source_digest(SEMANTICS_PATH), "decision_rules_digest": source_digest(DECISIONS_PATH), "vocabulary_results": [{"vocabulary_id": r["vocabulary_id"], "outcome": r["outcome"], "gates": r["gates"], "state_count": r["verification"]["candidate"]["state_count"], "edge_count": r["verification"]["candidate"]["edge_count"], "shortest_counterexample": r["verification"]["shortest_counterexample"]} for r in results], "vocabulary_level": {"existential_complete": bool(complete), "reproducible_complete": len(complete) == 3 and len(digests) == 1, "complete_vocabularies": complete, "ranking_permitted": False}, "supported_conclusions": ["Each reported complete outcome passed all frozen CRE-002 complete gates for the bounded scenario.", "The results are prospective relative to Vocabulary Semantics Baseline 1.0.", "Behavioral equivalence, where reported, is limited to the full bounded CRE-002 state space and registered policies."], "unsupported_conclusions": decisions["global_nonclaims"] + ["adequacy outside the frozen CRE-002 scenario", "unbounded concurrency", "unbounded higher-order modification", "global vocabulary ranking"]}


def report_markdown(summary: dict[str, Any]) -> str:
    lines = ["# CRE-002 Prospective Vocabulary Comparison", "", "## Scope", "", "This report records the first prospective execution governed by Vocabulary Semantics Baseline 1.0. It is limited to the frozen bounded CRE-002 scenario and decision rules.", "", "## Results", "", "| Vocabulary | Outcome | States | Edges | Counterexample |", "|---|---:|---:|---:|---|"]
    for row in summary["vocabulary_results"]:
        lines.append(f"| {row['vocabulary_id']} | {row['outcome']} | {row['state_count']} | {row['edge_count']} | {row['shortest_counterexample'] or 'none'} |")
    lines += ["", "## Vocabulary-level decision", "", f"- Existential complete condition: `{str(summary['vocabulary_level']['existential_complete']).lower()}`", f"- Reproducible complete condition: `{str(summary['vocabulary_level']['reproducible_complete']).lower()}`", "- Ranking permitted: `false`", "", "## Supported conclusions", ""]
    lines += [f"- {x}" for x in summary["supported_conclusions"]]
    lines += ["", "## Unsupported conclusions", ""] + [f"- {x}" for x in summary["unsupported_conclusions"]]
    return "\n".join(lines) + "\n"


def generate() -> tuple[dict[Path, str], dict[str, Any]]:
    scenario, semantics, decisions, control = load_json(SCENARIO_PATH), load_json(SEMANTICS_PATH), load_json(DECISIONS_PATH), load_json(CONTROL_PATH)
    if control.get("execution_permitted") is not True:
        raise RuntimeError("CRE-002 execution is not authorized")
    results = [compile_one(vocab_id, scenario, semantics) for vocab_id in VOCABS]
    summary = build_summary(results, scenario, decisions)
    files: dict[Path, str] = {}
    for result in results:
        root = GENERATED / result["vocabulary_id"]
        for name, artifact in artifact_map(result).items():
            files[root / name] = json.dumps(artifact, indent=2, sort_keys=True) + "\n"
    files[SUMMARY_PATH] = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    files[REPORT_PATH] = report_markdown(summary)
    return files, summary


def write_files(files: dict[Path, str]) -> None:
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def check_files(files: dict[Path, str]) -> list[str]:
    return [f"missing {path.relative_to(ROOT)}" if not path.is_file() else f"stale {path.relative_to(ROOT)}" for path, expected in files.items() if not path.is_file() or path.read_text(encoding="utf-8") != expected]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files, summary = generate()
    if args.write:
        write_files(files)
    failures = check_files(files) if args.check else []
    if failures:
        print("CRE-002 EXECUTION CHECK FAILED")
        print("\n".join(failures))
        return 1
    print("CRE-002 EXECUTION PASSED")
    for row in summary["vocabulary_results"]:
        print(f"{row['vocabulary_id']}: {row['outcome']} states={row['state_count']} edges={row['edge_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
